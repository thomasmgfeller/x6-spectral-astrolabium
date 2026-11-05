"""Check the immutable weighting release and replay its finite reference."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
ZIP = 'CST_Staubball_Historiengewichtung_v0_1_Pruefpaket.zip'
PDF = 'CST_Staubball_Historiengewichtung_v0_1.pdf'
ZIP_HASH = 'f2a6f1972c0cec72f96c374da04201e4fbf3f03a0dedc66a01368f38950e55bf'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def same_result(a, b, path='result'):
    if isinstance(a, float):
        require(isinstance(b, (float, int)) and math.isfinite(b)
                and math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-11), path)
    elif isinstance(a, dict):
        require(isinstance(b, dict) and a.keys() == b.keys(), path+' keys')
        for k in a:
            same_result(a[k], b[k], path+'.'+k)
    elif isinstance(a, list):
        require(isinstance(b, list) and len(a) == len(b), path+' size')
        for i, (x, y) in enumerate(zip(a, b)):
            same_result(x, y, path+f'[{i}]')
    else:
        require(type(a) is type(b) and a == b, path)

def run(replay):
    archive = ROOT.parent/'packages'/ZIP
    require(digest(archive.read_bytes()) == ZIP_HASH, 'original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 12 and z.testzip() is None, 'ZIP inventory')
        for name in names:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe ZIP path')
            require((ROOT/name).read_bytes() == z.read(name), 'expanded file differs: '+name)
        for line in z.read('SHA256SUMS').decode().splitlines():
            h, name = line.split(maxsplit=1)
            require(digest(z.read(name)) == h, 'member SHA256: '+name)
        require(z.read(PDF) == (ROOT.parent/'reports'/PDF).read_bytes(), 'report copy changed')
        previous = ROOT.parent/'packages/CST_Staubball_Kopplungsscan_v0_2_Pruefpaket.zip'
        require(digest(previous.read_bytes()) == '93741d09f47c87fc757653886f6c93fb42b8699b9830c66639b195bf05457ee0', 'original coupling archive changed')
        with zipfile.ZipFile(previous) as old:
            for name in ('development.csv', 'holdout.csv'):
                require(z.read('inputs/'+name) == old.read('source/'+name), 'source table differs')
        require(z.read('inputs/candidate_snapshot.json') ==
                (ROOT.parent/'bounce_closure_v0_1/candidate_snapshot.json').read_bytes(), 'closure snapshot differs')
        contract = json.loads(z.read('contract.json'))
        result = json.loads(z.read('results/verification.json'))
        require(contract['status'] == result['scientific_status'] ==
                'CONDITIONAL_REFERENCE_DERIVED_CST_MEASURE_OPEN', 'reference claim changed')
        require(contract['old_candidate_decision_preserved'] ==
                'CLOSED_REJECTED_FOR_DOMINANT_BOUNCE', 'old decision changed')
        require(result['new_bounce_test'] == 'NOT_RUN' and result['cst_measure'] ==
                result['singularity_resolution'] == 'HOLD', 'physical status changed')
        require(sum(r['unlabeled'] for r in result['quotients']) == 87, 'class count changed')
        require(not result['floating_point_checks_are_rigorous_interval_certificates'], 'numerical scope changed')
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-history-weighting-') as tmp:
                work = Path(tmp)
                z.extractall(work)
                proc = subprocess.run([sys.executable, str(work/'verify.py')],
                                      check=True, capture_output=True, text=True)
                fresh = json.loads((work/'results/verification.json').read_text())
                same_result(result, fresh)
                require(json.loads(proc.stdout) == fresh, 'replay output mismatch')
    print('PASS: unchanged ZIP, 12 members, PDF, prior sources and claim boundaries' +
          ('; finite reference replay matches' if replay else ''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
