"""Verify original boundary evidence and replay without editing the publication."""
import argparse
import csv
from decimal import Decimal
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Innen_Aussen_Anschluss_v0_1'
PREFIX = NAME + '/'
ZIP_HASH = 'e70bc1bb5c3c5565ff5becb519b2d593df853a3efb893f4c5bccb1f9a5f21e13'
PDF_HASH = '0688bc1738c1fd920d7da6e15c24b979921dd0f8c464c81dccb6fcc0a2ea7e57'
PLAN_HASH = 'aef4cf42edd0456b0249a9113623c42545e2edb68d274eb0292a6cd2b7da5c3f'
PARENT = 'bb59cc03e762b5b2133f4f12fdd975b219bf4406'
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_records(work):
    spec = importlib.util.spec_from_file_location('boundary_parent_gate',
                                                work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    manifest = work/'results/run_manifest.json'
    data = json.loads(manifest.read_text())
    require(data['physical_execution'] == 'NOT_RUN' and data['new_CST_ensembles'] == 0
            and data['parent_main_commit'] == PARENT and data['plan_sha256'] == PLAN_HASH
            and data['evidence_class'] == 'CLASSICAL_EXACT_AND_CONDITIONAL_DIAGNOSTICS'
            and data['versions']['sympy'] == '1.14.0', 'Execution scope/provenance')
    require(data['contract_sha256'] == sha((work/'inputs/parent_contract.json').read_bytes()),
            'Contract provenance')
    require(set(data['source_sha256']) == {'analyze.py', 'symbolic_checks.py', 'intervals.py'},
            'Executed source inventory')
    for name, digest in data['source_sha256'].items():
        require(sha((work/name).read_bytes()) == digest, 'Executed source: '+name)
    records = json.loads((work/'results/checkpoint_P5_records.json').read_text())
    audits = json.loads((work/'results/checkpoint_P5_audits.json').read_text())
    require(len(records) == len(audits) == 60, 'P5 count')
    actual, matrix = [], set()
    for record in records:
        context = record['checkpoint_context']
        require(record['execution'] == 'NOT_RUN' and record['checkpoint_id'] == 'P5'
                and record['run_manifest_sha256'] == sha(manifest.read_bytes()), 'P5 provenance')
        require(context['spatial_scope'] == 'INTERIOR_SURFACE_ALL_EXTERIOR', 'P5 domain')
        matrix.add((context['density_ratio'], context['M'], context['x']))
        result = gate.evaluate(record, work/'inputs/parent_contract.json', manifest)
        require(result['record_valid'] and result['decisions'] == {g: 'HOLD' for g in GATES},
                'Invalid record or promoted physical gate')
        actual.append({'context': context, **result})
    require(matrix == {(d, m, t) for d in [1, 2, 4, 8] for m in ['1/4', '1', '4']
                       for t in ['0', '1/4', '1/2', '3/4', '1']}, 'Complete planned P5 matrix')
    require(actual == audits, 'Archived decisions disagree with unchanged parent gate')


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 41 and z.testzip() is None, 'Archive inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(PREFIX),
                    'Unsafe archive member')
            require((ROOT/name[len(PREFIX):]).read_bytes() == z.read(name), 'Original bytes: '+name)

        def read(relative):
            return z.read(PREFIX+relative)

        listed = set()
        for line in read('SHA256SUMS.txt').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            require(name not in listed and sha(read(name)) == digest, 'Member hash: '+name)
            listed.add(name)
        require({PREFIX+n for n in listed} == set(names)-{PREFIX+'SHA256SUMS.txt'},
                'Incomplete member hashes')
        pdf = read(NAME+'.pdf')
        require(sha(pdf) == PDF_HASH and pdf == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(),
                'Published PDF differs')
        dependencies = {
            'parent_contract.json': 'model_contract_v0_1/contract.json',
            'parent_gate.py': 'model_contract_v0_1/gate.py',
            'expansion_plan.json': 'expansion_trapping_v0_1/plan.json',
            'expansion_verification.json': 'expansion_trapping_v0_1/results/verification.json',
            'expansion_derivation.md': 'expansion_trapping_v0_1/DERIVATION.md',
            'reference_regularity.json': 'correspondence_v0_1/results/reference_regularity.json',
            'legacy_derivation.md': 'regularity_v0_2/DERIVATION.md',
        }
        provenance = json.loads(read('inputs/provenance.json'))
        require(provenance['parent_main_commit'] == PARENT
                and set(provenance['input_sha256']) == set(dependencies), 'Predecessor inventory')
        for name, path in dependencies.items():
            data = read('inputs/'+name)
            require(data == (ROOT.parent/path).read_bytes()
                    and sha(data) == provenance['input_sha256'][name], 'Predecessor: '+name)
        require(read('intervals.py') == (ROOT.parent/'expansion_trapping_v0_1/intervals.py').read_bytes()
                and sha(read('intervals.py')) == provenance['intervals_sha256'], 'Inherited arithmetic')
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0],
                'Frozen plan')
        plan = json.loads(read('plan.json'))
        require(plan['numerical'] == {'decimal_precision': 60, 'root_bisections': 100,
                'identity_residual_cap': '1e-20', 'not_physical_tolerance': True}, 'Technical cap')
        require(plan['physical_CST']['execution'] == 'NOT_RUN'
                and plan['physical_CST']['regularity_separate'] is True, 'Physical scope')
        result = json.loads(read('results/verification.json'))
        counts = {'symbolic_identities': 34, 'junction_cases': 15, 'exterior_cases': 75,
                  'EF_cases': 9, 'event_horizon_cases': 3, 'conditional_nonvacuum_cases': 20,
                  'causal_cut_cases': 27, 'label_permutations': 24, 'decision_controls': 19,
                  'P5_records': 60, 'new_CST_ensembles': 0, 'new_random_draws': 0}
        require(all(result[k] == v for k, v in counts.items()), 'Evidence inventory')
        require(result['all_physical_gates'] == 'HOLD' and result['physical_execution'] == 'NOT_RUN'
                and result['paid_runs'] is False
                and Decimal(result['max_reference_residual']) < Decimal('1e-20'), 'Result scope/cap')
        symbolic = json.loads(read('results/symbolic_checks.json'))
        require(len(symbolic) == 34 and all(r['exact_residual'] == '0' for r in symbolic),
                'Exact algebra')
        controls = json.loads(read('results/decision_controls.json'))
        require(len(controls) == 19 and all(r['pass'] is True and r['observed'] == r['expected']
                                          for r in controls), 'Decision controls')
        for name, n in {'classical_junction.csv': 15, 'classical_exterior.csv': 75,
                        'EF_horizon_crossing.csv': 9, 'conditional_classical_event_horizon.csv': 3,
                        'conditional_nonvacuum_junction.csv': 20, 'causal_cut_controls.csv': 27}.items():
            require(len(list(csv.DictReader(io.StringIO(read('results/'+name).decode())))) == n,
                    'Case inventory: '+name)
        decision = json.loads(read('results/closure_decision.json'))
        expected = {
            'classical_finite_ball_junction': 'CLOSED_FOR_DECLARED_EINSTEIN_DUST_REFERENCE',
            'classical_singularity_resolution': 'FAIL_FOR_EXPLICIT_CLASSICAL_FUTURE_COMPLETION',
            'legacy_bounce_to_vacuum': 'FAIL_NO_SHELL_JUNCTION',
            'legacy_static_nonvacuum': 'CONDITIONAL_GEOMETRIC_CONSTRUCTION_ONLY',
            'physical_CST_boundary': 'HOLD_NOT_ELIGIBLE',
            'physical_CST_extension': 'HOLD', 'physical_CST_regularity': 'HOLD',
            'physical_execution': 'NOT_RUN',
        }
        require(all(decision[k] == v for k, v in expected.items()), 'Scientific scope promoted')
        check_records(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-boundary-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                # Remove archived results: every result must be generated by this execution.
                for p in (work/'results').iterdir():
                    p.unlink()
                subprocess.run([sys.executable, '-O', '-B', str(work/'analyze.py')],
                               cwd=work, check=True, capture_output=True, text=True)
                check_records(work)
                expected_results = {n[len(PREFIX):] for n in names if n.startswith(PREFIX+'results/')}
                actual_results = {p.relative_to(work).as_posix() for p in (work/'results').rglob('*')
                                  if p.is_file()}
                require(actual_results == expected_results and len(actual_results) == 15,
                        'Replayed output inventory')
                for relative in sorted(expected_results):
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative == 'results/run_manifest.json':
                        a, b = json.loads(expected), json.loads(actual)
                        require(isinstance(b['versions']['python'], str) and b['versions']['python'],
                                'Runtime version missing')
                        a['versions'].pop('python'); b['versions'].pop('python')
                        require(a == b, relative)
                    elif relative == 'results/checkpoint_P5_records.json':
                        a, b = json.loads(expected), json.loads(actual)
                        # Each record-to-manifest link was validated before normalization.
                        for record in a+b:
                            record.pop('run_manifest_sha256')
                        require(a == b, relative)
                    else:
                        require(expected == actual, relative)
    print('PASS: original ZIP, 41 members, complete hashes, PDF, predecessor inputs, '
          'frozen plan, 34 identities, all 60 P5 records and independent physical HOLD decisions'
          + ('; isolated replay of all 15 result files agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
