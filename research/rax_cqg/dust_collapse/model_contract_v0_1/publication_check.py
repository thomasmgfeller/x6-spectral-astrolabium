"""Check the published contract snapshot and replay without changing archive bytes."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Model_Contract_v0_1'
PREFIX = NAME+'/'
ZIP_HASH = 'e6bca27187a434ab2b6f974458d41306d0cc7bf2529ef8a71eef0a769e354f8d'
PDF_HASH = '03e178e4c4e5ee2053cdd8d7b786e18680aad9fddfe307efd12b35b8e7e05361'
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare(expected, actual, path='result'):
    if isinstance(expected, float):
        require(isinstance(actual, (float, int)) and math.isfinite(actual)
                and math.isclose(expected, actual, abs_tol=1e-12, rel_tol=1e-12), path)
    elif isinstance(expected, dict):
        require(isinstance(actual, dict) and expected.keys() == actual.keys(), path+' keys')
        for key in expected:
            compare(expected[key], actual[key], path+'.'+key)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(expected) == len(actual), path+' length')
        for i, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, path+f'[{i}]')
    else:
        require(type(expected) is type(actual) and expected == actual, path)


def rows(text):
    return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(io.StringIO(text))]


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 20 and z.testzip() is None, 'ZIP inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(PREFIX), 'Unsafe path')
            require((ROOT/name[len(PREFIX):]).read_bytes() == z.read(name), 'Expanded bytes: '+name)

        def read(relative):
            return z.read(PREFIX+relative)

        listed = set()
        for line in read('SHA256SUMS').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            require(name not in listed and sha(read(name)) == digest, 'Member hash: '+name)
            listed.add(name)
        require({PREFIX+n for n in listed} == set(names)-{PREFIX+'SHA256SUMS'}, 'Incomplete hashes')
        pdf = read(NAME+'.pdf')
        require(sha(pdf) == PDF_HASH and pdf == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(), 'PDF bytes')
        provenance = json.loads(read('inputs/provenance.json'))
        for entry in provenance['project_sources']:
            data = read('inputs/'+entry['file'])
            blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(blob == entry['git_blob_sha'] and sha(data) == entry['sha256'], 'Source provenance')
        contract = json.loads(read('contract.json'))
        require(contract['id'] == 'CST-DUST-MC-001' and contract['version'] == '0.1.0', 'Contract identity')
        require(contract['protocol_status'] == 'SPECIFIED', 'Protocol status')
        require(contract['physical_model_status'] == 'HOLD_INCOMPLETE_CST_DYNAMICS', 'Model scope')
        require(contract['current_cst_status'] == {g: 'HOLD' for g in GATES}, 'Scientific decisions')
        require(contract['singularity_resolution'] == 'HOLD' and not contract['new_cst_ensembles_run'], 'Claim scope')
        require(all(x['regularity_required'] for x in contract['checkpoint_schedule']), 'Checkpoint independence')
        require(len(contract['candidate_closure']) == 7 and
                all(x['status'] == 'OPEN' for x in contract['candidate_closure']), 'Open model obligations')
        result = json.loads(read('results/verification.json'))
        require(result['decision_control_cases'] == 17 and result['new_cst_ensembles'] == 0, 'Control counts')
        require(result['reference_controls']['cases'] == 15 and result['reference_controls']['identities_per_case'] == 5,
                'Reference coverage')
        require(result['test_status'] == 'PASS_PROTOCOL_AND_REFERENCE_CONTROLS_ONLY', 'Evidence class')
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-cst-dust-contract-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                subprocess.run([sys.executable, str(work/'build_contract.py')], check=True, capture_output=True, text=True)
                require((work/'contract.json').read_bytes() == read('contract.json'), 'Contract regeneration')
                subprocess.run([sys.executable, str(work/'verify.py')], check=True, capture_output=True, text=True)
                for relative in ['results/verification.json', 'results/decision_controls.json',
                                 'results/checkpoint_P0_decision.json', 'examples/run_manifest.json',
                                 'examples/checkpoint_P0.json']:
                    compare(json.loads(read(relative)), json.loads((work/relative).read_text()), relative)
                compare(rows(read('results/reference_values.csv').decode()),
                        rows((work/'results/reference_values.csv').read_text()), 'reference CSV')
                p = subprocess.run([sys.executable, str(work/'gate.py'), str(work/'examples/checkpoint_P0.json')],
                                   check=True, capture_output=True, text=True)
                compare(json.loads(read('results/checkpoint_P0_decision.json')), json.loads(p.stdout), 'CLI decision')
    print('PASS: original ZIP, 20 members, complete hashes, source provenance, PDF and scoped HOLD decisions'
          + ('; contract, 15 reference cases, 17 decision controls and CLI replay agree' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
