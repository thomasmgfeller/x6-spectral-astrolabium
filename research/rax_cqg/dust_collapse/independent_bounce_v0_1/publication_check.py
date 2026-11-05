"""Check immutable source artifacts and replay the sealed reference forecast."""
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
NAME = 'CST_Staubball_Unabhaengige_Bounce_Vorhersage_v0_1'
ZIP_HASH = 'b3940e6522b8b99563f69a782cf10e3f322c5629bc6792f74bbba0a218f0435d'
PDF_HASH = 'aea4366af2c9d6eee24667179efb945601f8132ea86307b7d56b145cb61c7791'
STATUS = {
    'early_moment_reference_forecast': 'PASS',
    'full_CST_bounce': 'HOLD_NOT_ELIGIBLE',
    'singularity_resolution': 'NOT_ESTABLISHED',
    'old_dominant_candidate': 'CLOSED_REJECTED_FOR_DOMINANT_BOUNCE',
    'independent_experimental_or_external_replication': False,
}


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
            if path == 'result' and key in ('environment', 'runtime_seconds'):
                continue
            compare(expected[key], actual[key], path+'.'+key)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(expected) == len(actual), path+' length')
        for i, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, path+f'[{i}]')
    else:
        require(type(expected) is type(actual) and expected == actual, path)


def csv_rows(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    for row in rows:
        for key, value in row.items():
            try:
                row[key] = float(value)
            except ValueError:
                pass
    return rows


def run(replay):
    archive = ROOT.parent/'packages'/f'{NAME}_Pruefpaket.zip'
    require(digest(archive.read_bytes()) == ZIP_HASH, 'Original release ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 22 and z.testzip() is None, 'ZIP inventory')
        prefix = ROOT.name+'/'
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts
                    and name.startswith(prefix), 'Unsafe ZIP path')
            relative = name[len(prefix):]
            require((ROOT/relative).read_bytes() == z.read(name), 'Expanded bytes differ: '+relative)

        def read(relative):
            return z.read(prefix+relative)

        listed = set()
        for line in read('SHA256SUMS').decode().splitlines():
            h, name = line.split(maxsplit=1)
            require(name not in listed and digest(read(name)) == h, 'Member hash: '+name)
            listed.add(name)
        require({prefix+n for n in listed} == set(names)-{prefix+'SHA256SUMS'}, 'Hash inventory coverage')
        pdf = read(f'{NAME}.pdf')
        require(digest(pdf) == PDF_HASH
                and pdf == (ROOT.parent/'reports'/f'{NAME}.pdf').read_bytes(), 'Report changed')
        for name, previous in {
            'classical_reference_result.json': 'classical_backreaction_v0_1/results/verification.json',
            'history_weighting_contract.json': 'history_weighting_v0_1/contract.json',
        }.items():
            require(read('inputs/'+name) == (ROOT.parent/previous).read_bytes(), 'Prior source changed: '+name)
        for filename, sealed in [('plan.json', 'PLAN_SHA256'), ('forecast.json', 'FORECAST_SHA256')]:
            require(digest(read(filename)) == read(sealed).decode().split()[0], filename+' seal')
        result = json.loads(read('results/verification.json'))
        require(result['status'] == STATUS, 'Scientific decision changed')
        require(len(result['decisions']) == 10
                and all(d['status'] == 'PASS' and d['errors_decrease'] for d in result['decisions']), 'Ten reference gates')
        require(len(result['cases']) == 30, 'Three refinement levels')
        require(sum(len(x['rows']) for x in result['spectral_crosschecks']) == 50, 'Spectral coverage')
        boundary = result['controls']['boundary_comparison']
        require(len(boundary) == 2 and sum(len(x['neumann_late_checks']) for x in boundary) == 6, 'Boundary coverage')
        require(len(result['controls']['gaussian_wall_slopes']) == 8
                and len(result['controls']['cutoffs']) == 7, 'Regularity coverage')
        saved_csv = {n: csv_rows(read('results/'+n).decode())
                     for n in ('late_traces.csv', 'prediction_errors.csv')}
        require(len(saved_csv['late_traces.csv']) == 7230
                and len(saved_csv['prediction_errors.csv']) == 30, 'CSV coverage')
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-bounce-forecast-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/ROOT.name
                subprocess.run([sys.executable, str(work/'verify.py')], check=True,
                               capture_output=True, text=True)
                compare(result, json.loads((work/'results/verification.json').read_text()))
                for name, expected in saved_csv.items():
                    compare(expected, csv_rows((work/'results'/name).read_text()), name)
    print('PASS: unchanged ZIP, 22 members, PDF, prior sources, sealed forecasts and scientific scope'
          + ('; 30 runs, controls and 7230 readouts reproduced' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
