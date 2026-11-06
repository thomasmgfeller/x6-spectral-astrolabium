"""Preserve the source snapshot and replay the scoped regularity calculations."""
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
NAME = 'CST_Staubball_Regularitaet_Rand_Verfeinerung_v0_2'
PREFIX = 'CST_Regularitaet_v0_2/'
ZIP_HASH = 'beb729d24357204edfaf54455940bbf399b2651b599e71b2dedae95c754a9e00'
PDF_HASH = '899f2157cc4125cb85caca189f6743917448cbbd773492470e808bc7a755c635'
DECISIONS = {
    'first_inverse_moment': 'BOUNDED_WITHIN_DIRICHLET_ENERGY_CLASS',
    'second_inverse_moment_dynamic_protection': 'COUNTEREXAMPLE_PROVED',
    'effective_interior_at_fixed_nu': 'REGULAR_CONDITIONALLY',
    'nu_to_zero_uniform_curvature': 'FAIL_FOR_STATED_SCALING',
    'smooth_Schwarzschild_matching': 'EXCLUDED_UNDER_STATED_ASSUMPTIONS',
    'CST_singularity_resolution': 'HOLD',
    'CST_refinement_ensemble': 'NOT_RUN',
    'global_causal_extension': 'HOLD',
    'new_horizon_or_black_hole_claim': 'NONE',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compare(expected, actual, path='result'):
    if isinstance(expected, float):
        require(isinstance(actual, (float, int)) and math.isfinite(actual)
                and math.isclose(expected, actual, abs_tol=1e-8, rel_tol=1e-9), path)
    elif isinstance(expected, dict):
        require(isinstance(actual, dict) and expected.keys() == actual.keys(), path+' keys')
        for key in expected:
            if path == 'result' and key == 'versions':
                continue
            compare(expected[key], actual[key], path+'.'+key)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(expected) == len(actual), path+' length')
        for i, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, path+f'[{i}]')
    else:
        require(type(expected) is type(actual) and expected == actual, path)


def csv_rows(text):
    return [{key: float(value) for key, value in row.items()}
            for row in csv.DictReader(io.StringIO(text))]


def run(replay):
    archive = ROOT.parent/'packages'/f'{NAME}_Pruefpaket.zip'
    require(digest(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 32 and z.testzip() is None, 'ZIP inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(PREFIX), 'Unsafe path')
            relative = name[len(PREFIX):]
            require((ROOT/relative).read_bytes() == z.read(name), 'Expanded bytes changed: '+relative)

        def read(relative):
            return z.read(PREFIX+relative)

        listed = set()
        for line in read('SHA256SUMS').decode().splitlines():
            h, name = line.split(maxsplit=1)
            require(name not in listed and digest(read(name)) == h, 'Member hash: '+name)
            listed.add(name)
        require({PREFIX+n for n in listed} == set(names)-{PREFIX+'SHA256SUMS'}, 'Incomplete manifest')
        pdf = read(NAME+'.pdf')
        require(digest(pdf) == PDF_HASH and pdf == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(),
                'Report bytes changed')
        contract = json.loads(read('contract.json'))
        require(contract['decisions'] == DECISIONS, 'Scientific scope changed')
        result = json.loads(read('results/verification.json'))
        require(result['status'] == 'SCOPED_RESULTS_ONLY_CST_REGULARITY_HOLD', 'Overall status')
        require(result['exact'] == {
            'T_b': '35/158', 'V_b': '77/79', 'A': '7/4', 'J': '7/2', 'E': '79/20',
            'inverse_second_initial': '16/15', 'inverse_first_initial': '4/5',
        }, 'Exact counterexample changed')
        coverage = {'moments.csv': 6, 'cutoff.csv': 11, 'spectral.csv': 5,
                    'physical_scale.csv': 4, 'numerical_refinement.csv': 4,
                    'finite_ball.csv': 19, 'tail_controls.csv': 24}
        saved = {name: csv_rows(read('results/'+name).decode()) for name in coverage}
        for name, count in coverage.items():
            require(len(saved[name]) == count, name+' coverage')
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-regularity-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable, str(work/'verify.py')], check=True,
                               capture_output=True, text=True)
                compare(result, json.loads((work/'results/verification.json').read_text()))
                for name, expected in saved.items():
                    compare(expected, csv_rows((work/'results'/name).read_text()), name)
    print('PASS: unchanged ZIP, 32 members, complete hashes, PDF and scoped scientific decisions'
          + ('; numerical replay and all seven CSV files agree' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
