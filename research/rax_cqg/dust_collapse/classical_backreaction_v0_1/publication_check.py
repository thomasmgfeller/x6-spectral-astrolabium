"""Verify immutable release bytes, source binding and a temporary numerical replay."""
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
NAME = 'CST_Staubball_Klassik_Rueckwirkung_v0_1'
ZIP_HASH = 'd2cfaa782e42a319fa248cfbbacbf6e79ce6bcb6ada02471f72c0f350bae1f80'
PDF_HASH = '7ad167b131959cc6f15026c6925bc7c33d297eca1152fb65ce5b269f2d3daa6c'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compare(expected, actual, path='result'):
    if isinstance(expected, float):
        require(isinstance(actual, (int, float)) and math.isfinite(actual)
                and math.isclose(expected, actual, abs_tol=2e-10, rel_tol=1e-10), path)
    elif isinstance(expected, dict):
        require(isinstance(actual, dict) and expected.keys() == actual.keys(), path+' keys')
        for key in expected:
            if path == 'result' and key == 'environment':
                continue  # Python patch versions and compatible runtime metadata may differ.
            compare(expected[key], actual[key], path+'.'+key)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(expected) == len(actual), path+' length')
        for i, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, path+f'[{i}]')
    else:
        require(type(expected) is type(actual) and expected == actual, path)


def run(replay):
    archive = ROOT.parent/'packages'/f'{NAME}_Pruefpaket.zip'
    require(digest(archive.read_bytes()) == ZIP_HASH, 'Original release ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 23 and z.testzip() is None, 'ZIP inventory')
        for name in names:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe ZIP path')
            require((ROOT/name).read_bytes() == z.read(name), 'Expanded bytes differ: '+name)
        listed = set()
        for line in z.read('SHA256SUMS').decode().splitlines():
            h, name = line.split(maxsplit=1)
            require(name not in listed and digest(z.read(name)) == h, 'Member hash: '+name)
            listed.add(name)
        require(listed == set(names)-{'SHA256SUMS'}, 'Hash inventory coverage')
        pdf = z.read(f'{NAME}.pdf')
        require(digest(pdf) == PDF_HASH and pdf == (ROOT.parent/'reports'/f'{NAME}.pdf').read_bytes(), 'Report changed')
        history = ROOT.parent/'history_weighting_v0_1'
        require(z.read('inputs/history_weighting/contract.json') == (history/'contract.json').read_bytes(), 'Prior contract changed')
        for filename in ('development.csv', 'holdout.csv'):
            require(z.read('inputs/history_weighting/'+filename) == (history/'inputs'/filename).read_bytes(), 'History input changed')
        previous = ROOT.parent/'packages/Staubball_C_Zwei_Massen_Pruefpaket.zip'
        require(digest(previous.read_bytes()) == 'a6240c9662af13d4409fefb9b6d569412e391f843fcd480d1baea16f89aed031', 'Prior mass archive changed')
        with zipfile.ZipFile(previous) as old:
            for path in ('design.json', 'README.md', 'amplitudes.json', 'fixed_audit.json', 'inputs/symmetry_orbit.csv', 'inputs/growth.csv'):
                require(z.read('inputs/family_C/'+Path(path).name) == old.read(path), 'Family C input differs: '+path)
        result = json.loads(z.read('results/verification.json'))
        decisions = result['decisions']
        require(decisions == {
            'reference_classical': 'PASS_CONDITIONAL',
            'reference_semiclassical': 'PASS_FINITE_BENCHMARK',
            'reference_mass_response': 'PASS_CONDITIONAL',
            'full_CST_classical_limit': 'HOLD', 'full_CST_backreaction': 'HOLD',
            'singularity_resolution': 'NOT_ESTABLISHED', 'new_bounce_test': 'NOT_RUN'
        }, 'Scientific decision changed')
        require(len(result['semiclassical']) == 90 and len(result['classical_RK']) == 9, 'Reference coverage')
        contract = json.loads(z.read('inputs/history_weighting/contract.json'))
        require(contract['old_candidate_decision_preserved'] == 'CLOSED_REJECTED_FOR_DOMINANT_BOUNCE', 'Old decision changed')
        require(not result['family_C']['interval_certification_repeated'], 'Interval scope changed')
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-classical-') as tmp:
                work = Path(tmp); z.extractall(work)
                process = subprocess.run([sys.executable, str(work/'verify.py')], check=True, capture_output=True, text=True)
                fresh = json.loads((work/'results/verification.json').read_text())
                compare(result, fresh)
                require(json.loads(process.stdout)['decisions'] == decisions, 'Replay decision output')
    print('PASS: unchanged ZIP, 23 members, PDF, prior sources and claim boundaries'
          + ('; classical, quantum and mass-response replay matches' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
