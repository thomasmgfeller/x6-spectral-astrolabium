"""Check the immutable calibration snapshot and replay in a temporary directory."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Staubstrom_Kalibrierung_v0_1'
PREFIX = NAME+'/'
ZIP_HASH = '27d3331f9fd4f70d00e62e97b4b72a99c5b21de864c1b2c04fa25aa15754aa8f'
PDF_HASH = '2f0b60b793fccbd55dbb2ad3033a41fa1dd3df556ce29a76d93c793d77908851'
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare(expected, actual, path='result'):
    if isinstance(expected, float):
        require(isinstance(actual, (float, int)) and not isinstance(actual, bool)
                and math.isfinite(actual) and math.isclose(expected, actual, abs_tol=1e-10, rel_tol=2e-9), path)
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


def csv_rows(data):
    def value(v):
        try:
            return float(v)
        except ValueError:
            return v
    return [{k: value(v) for k, v in row.items()} for row in csv.DictReader(io.StringIO(data.decode()))]


def check_record(work):
    spec = importlib.util.spec_from_file_location('current_parent_gate', work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    record = json.loads((work/'results/checkpoint_P2_record.json').read_text())
    result = gate.evaluate(record, work/'inputs/parent_contract.json', work/'results/run_manifest.json')
    require(result['record_valid'], 'P2 contract record invalid')
    require(result['decisions'] == {g:'HOLD' for g in GATES}, 'P2 physical gate promoted')
    compare(json.loads((work/'results/checkpoint_P2_audit.json').read_text()), result, 'P2 parent audit')


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 38 and z.testzip() is None, 'ZIP inventory')
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
        parent = ROOT.parent/'model_contract_v0_1'
        require(read('inputs/parent_contract.json') == (parent/'contract.json').read_bytes(), 'Parent contract changed')
        require(read('inputs/parent_gate.py') == (parent/'gate.py').read_bytes(), 'Parent gate changed')
        plan = json.loads(read('plan.json'))
        require(sha(read('plan.json')) == read('plan.sha256').decode().split()[0], 'Frozen plan hash')
        require(plan['parent_contract_sha256'] == sha(read('inputs/parent_contract.json')), 'Parent contract pin')
        provenance = json.loads(read('provenance.json'))
        for name, digest in provenance['input_sha256'].items():
            require(sha(read('inputs/'+name)) == digest, 'Input provenance: '+name)
        summary = json.loads(read('results/verification.json'))
        require(summary['graph']['controls'] == 86 and summary['mass_flux']['mass_cases'] == 420
                and summary['mass_flux']['flux_cases'] == 144, 'Current reference counts')
        require(summary['exposure']['base_cells'] == 315 and summary['poisson']['family_size'] == 1260
                and summary['covariance']['matrices'] == 12, 'Calibration counts')
        require(summary['new_dynamical_CST_ensembles'] == summary['poisson']['new_random_draws'] == 0, 'Ensemble scope')
        require(all(summary[k] == 'HOLD' for k in ['CST_CURRENT','CST_REGULARITY','singularity_resolution']), 'Claim scope')
        levels = summary['poisson']['levels']
        require([r['density_ratio'] for r in levels] == [1,2,4,8], 'Refinement levels')
        require([r['joint_pass_probability_lower'] >= .95 for r in levels] == [False,False,True,True], 'Precision decisions')
        ref = json.loads(read('results/reference_decisions.json'))
        require(ref['metric_regularity'] == 'PASS_FIXED_REFERENCE_WINDOW_ONLY'
                and ref['inference_at_zero'] == 'HOLD_WITH_UNBOUNDED_DENSITY_INTERVAL', 'Separate regularity decisions')
        check_record(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-current-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                for script in ['calibrate.py', 'audit_checkpoint.py']:
                    subprocess.run([sys.executable, '-B', str(work/script)], check=True,
                                   capture_output=True, text=True, cwd=work)
                check_record(work)
                for name in names:
                    relative = name[len(PREFIX):]
                    if not relative.startswith('results/'):
                        continue
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative.endswith('.csv'):
                        compare(csv_rows(expected), csv_rows(actual), relative)
                    elif relative.endswith('.json'):
                        a, b = json.loads(expected), json.loads(actual)
                        if relative == 'results/run_manifest.json':
                            require(set(b['versions']) == {'python','numpy','scipy'}
                                    and all(isinstance(v,str) and v for v in b['versions'].values()), 'Runtime versions missing')
                            a.pop('versions'); b.pop('versions')
                        elif relative == 'results/checkpoint_P2_record.json':
                            # The replay manifest records the actual runner versions.
                            a.pop('run_manifest_sha256'); b.pop('run_manifest_sha256')
                        compare(a, b, relative)
    print('PASS: original ZIP, 38 members, complete hashes, PDF, parent contract, frozen plan, P2 HOLD decisions'
          + ('; isolated replay of all calibration results agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
