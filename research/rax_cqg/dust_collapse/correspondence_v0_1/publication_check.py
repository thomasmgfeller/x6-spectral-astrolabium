"""Check immutable evidence and replay reference calculations without editing it."""
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
NAME = 'CST_DUST_Korrespondenz_v0_1'
PREFIX = NAME + '/'
ZIP_HASH = '15c048f7b77ff07ed8809e97d2277af37a3af149cb933a9a58c38a884e130b39'
PDF_HASH = '2bd3e8c9cb8bf67b182ab7c08043e6fac17db7add8012318d46afcbe923f6f4b'
PLAN_HASH = 'f3f77a306380b24bb761e0a2c2708833ea6d6c723b82467a08f725e9abd8cdb1'
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
                and math.isfinite(actual)
                and math.isclose(expected, actual, abs_tol=1e-12, rel_tol=2e-10), path)
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
    return [{k: value(v) for k, v in row.items()}
            for row in csv.DictReader(io.StringIO(data.decode()))]


def check_records(work):
    spec = importlib.util.spec_from_file_location('correspondence_parent_gate',
                                                work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    records = json.loads((work/'results/checkpoint_P3_records.json').read_text())
    expected = json.loads((work/'results/checkpoint_P3_audits.json').read_text())
    require(len(records) == len(expected) == 60, 'P3 record count')
    manifest = work/'results/run_manifest.json'
    evaluated = []
    contexts = set()
    for record in records:
        context = record['checkpoint_context']
        contexts.add((context['density_ratio'], context['M'], context['x']))
        require(record['execution'] == 'NOT_RUN'
                and record['run_manifest_sha256'] == sha(manifest.read_bytes()), 'P3 provenance')
        result = gate.evaluate(record, work/'inputs/parent_contract.json', manifest)
        require(result['record_valid'] and result['decisions'] == {g:'HOLD' for g in GATES},
                'P3 record invalid or physical decision promoted')
        evaluated.append({'context': context, **result})
    require(contexts == {(d,m,t) for d in [1,2,4,8] for m in ['1/4','1','4']
                         for t in ['0','1/4','1/2','3/4','1']}, 'P3 grid')
    compare(expected, evaluated, 'P3 parent audits')
    manifest_data = json.loads(manifest.read_text())
    for name, digest in manifest_data['source_sha256'].items():
        require(sha((work/name).read_bytes()) == digest, 'Executed source: '+name)


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 40 and z.testzip() is None, 'ZIP inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(PREFIX),
                    'Unsafe archive path')
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
        require(sha(pdf) == PDF_HASH and pdf == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(),
                'PDF bytes')
        dependencies = {
            'parent_contract.json': 'model_contract_v0_1/contract.json',
            'parent_gate.py': 'model_contract_v0_1/gate.py',
            'current_plan.json': 'current_calibration_v0_1/plan.json',
            'current_verification.json': 'current_calibration_v0_1/results/verification.json',
            'current_observables.py': 'current_calibration_v0_1/observables.py',
            'current_checkpoint_P2.json': 'current_calibration_v0_1/results/checkpoint_P2_audit.json',
        }
        provenance = json.loads(read('inputs/provenance.json'))
        require(provenance['parent_main_commit'] == 'eabb4ece77563b049caa3a30bacd7b75b850d3a8',
                'Parent publication commit')
        require(set(provenance['sha256']) == set(dependencies), 'Input inventory')
        for name, path in dependencies.items():
            data = read('inputs/'+name)
            require(data == (ROOT.parent/path).read_bytes()
                    and sha(data) == provenance['sha256'][name], 'Predecessor input: '+name)
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0],
                'Frozen plan')
        plan = json.loads(read('plan.json'))
        require(plan['parent_contract_sha256'] == sha(read('inputs/parent_contract.json')), 'Parent pin')
        require(plan['primary_tolerances'] == {
            'R':.05,'rho':.05,'H':.05,'a_ddot_over_a':.05,'mass_or_flux_over_M':.02,
            'initial_velocity_and_mass_response':.05,'last_two_physical_levels':.025}, 'Tolerances')
        result = json.loads(read('results/verification.json'))
        require(result['guard_controls'] == 26 and result['new_random_draws'] == 0
                and result['new_CST_ensembles'] == 0 and result['paid_runs'] is False, 'Scope/counts')
        require(result['physical_correspondence'] == 'HOLD_NOT_ELIGIBLE'
                and result['physical_execution'] == 'NOT_RUN' and result['regularity'] == 'HOLD',
                'Scientific decision promoted')
        levels = result['numerical_reference_levels']
        require([r['steps'] for r in levels] == [128,256,512,1024]
                and [r['passed_numerical_cap'] for r in levels] == [54,58,60,60]
                and sum(r['comparisons'] for r in levels) == 240, 'Reference cases')
        require(levels[-1]['max_relative_enclosure_error'] < .005, 'Finest numerical budget')
        require(len(csv_rows(read('results/derivative_exact_bounds.csv'))) == 90, 'Rational cases')
        require(all(r['certification'] == 'HOLD_SUFFICIENT_BOUND_TOO_WIDE'
                    for r in result['inherited_density_derivative_budget']), 'Derivative scope')
        check_records(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-correspondence-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                subprocess.run([sys.executable, '-O', '-B', str(work/'run.py')], check=True,
                               capture_output=True, text=True, cwd=work)
                check_records(work)
                expected_results = {name[len(PREFIX):] for name in names
                                    if name.startswith(PREFIX+'results/')}
                actual_results = {str(p.relative_to(work)) for p in (work/'results').rglob('*')
                                  if p.is_file()}
                require(expected_results == actual_results, 'Replayed result inventory')
                for relative in sorted(expected_results):
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative.endswith('.csv'):
                        compare(csv_rows(expected), csv_rows(actual), relative)
                    elif relative.endswith('.json'):
                        a, b = json.loads(expected), json.loads(actual)
                        if relative == 'results/run_manifest.json':
                            require(set(b['versions']) == {'python','numpy','scipy'}
                                    and all(isinstance(v,str) and v for v in b['versions'].values()),
                                    'Runtime versions missing')
                            a.pop('versions'); b.pop('versions')
                        elif relative == 'results/checkpoint_P3_records.json':
                            # Both sets of manifest links were verified by check_records.
                            for record in a+b:
                                record.pop('run_manifest_sha256')
                        compare(a, b, relative)
                    else:
                        require(expected == actual, relative)
    print('PASS: original ZIP, 40 members, complete hashes, PDF, predecessor inputs, frozen plan, '
          'all 60 P3 records and separate physical HOLD decisions'
          + ('; isolated replay of every result agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
