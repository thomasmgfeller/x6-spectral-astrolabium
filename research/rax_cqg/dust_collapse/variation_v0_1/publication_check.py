"""Check original variation artifacts and replay without modifying evidence."""
import argparse
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Physikalische_Variation_v0_1'
PREFIX = NAME + '/'
ZIP_HASH = '655e760e46c2b676ba6dc0499271293feabb12acda97d291433f416ea2fbe848'
PDF_HASH = '091b2eb54ecf342caaa5376227ffe56f5660780673d29c01564f1408f01342f9'
PLAN_HASH = '65ea55b1f64e7f0e577927922e502bd97f16b017335042eb33d6d35e318db743'
PARENT = '9fa170dfd604be3847004ea2bdbe8587ada5d068'
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(work, name):
    return json.loads((work/name).read_text())


def check_scope(work):
    manifest = work/'results/run_manifest.json'
    data = json.loads(manifest.read_text())
    require(data['finite_candidate_checks'] == 'RUN'
            and data['physical_4D_dust_dynamics'] == 'NOT_RUN'
            and data['new_physical_4D_ensembles'] == data['random_draws'] == 0
            and data['parent_main_commit'] == PARENT and data['plan_sha256'] == PLAN_HASH,
            'Execution scope/provenance')
    require(set(data['source_sha256']) == {'variation.py', 'analyze.py'}, 'Executed sources')
    for name, digest in data['source_sha256'].items():
        require(sha((work/name).read_bytes()) == digest, 'Executed source: '+name)
    spec = importlib.util.spec_from_file_location('variation_parent_gate', work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    rec = load(work, 'results/checkpoint_P1_record.json')
    require(rec['checkpoint_id'] == 'P1' and rec['execution'] == 'RUN'
            and rec['scope']['model_id'] == 'CST-DUST-V1-RAW-K'
            and 'not full physical CST' in rec['scope']['domain']
            and rec['run_manifest_sha256'] == sha(manifest.read_bytes()), 'Scoped P1 provenance')
    item = rec['gates']['MODEL']['quantum_consistency']
    require(item['outcome'] == 'VIOLATED' and item['evidence_kind'] == 'ANALYTIC_COUNTEREXAMPLE',
            'Candidate-specific negative result')
    evaluated = gate.evaluate(rec, work/'inputs/parent_contract.json', manifest)
    expected = {g: 'FAIL' if g == 'MODEL' else 'HOLD' for g in GATES}
    require(evaluated['record_valid'] and evaluated['decisions'] == expected
            and evaluated['physical_claim_automatically_authorized'] is False, 'Physical scope')
    require(evaluated == load(work, 'results/checkpoint_P1_audit.json'), 'Archived P1 audit')
    result = load(work, 'results/verification.json')
    counts = {'orders': 4473, 'product_identities': 22095, 'clock_derivatives': 22095,
              'density_derivatives': 22095, 'constant_shift_checks': 22095,
              'matter_partitions': 130116, 'cut_balances': 130116, 'label_checks': 5377,
              'geometry_moves': 1240, 'admissible_interval_orders': 24,
              'conditional_exterior_cases': 9, 'controls': 10,
              'new_physical_4D_ensembles': 0, 'new_sprinklings': 0, 'random_draws': 0}
    require(all(result[k] == v for k, v in counts.items()), 'Evidence inventory')
    statuses = {'exact_variation_residuals': 'ZERO',
                'matter_action': 'DEFINED_CANDIDATE_NOT_PHYSICALLY_QUALIFIED',
                'joint_geometry_matter_variation': 'PASS_EXACT_FINITE_IDENTITIES',
                'raw_kernel_evolution': 'FAIL_FOR_DECLARED_KINEMATIC_INNER_PRODUCTS',
                'physical_CST_model': 'HOLD', 'effective_causal_junction': 'HOLD_NOT_DERIVED',
                'physical_common_exterior': 'HOLD_NOT_SOLVED', 'regularity': 'HOLD',
                'global_bounce': 'HOLD_NOT_RUN'}
    require(all(result[k] == v for k, v in statuses.items()) and result['paid_runs'] is False,
            'Scientific claim changed')
    controls = load(work, 'results/controls.json')
    require(len(controls) == 10 and all(c['pass'] and c['observed'] == c['expected'] for c in controls),
            'Structural controls')
    norm = load(work, 'results/normalization_counterexample.json')
    lo, hi = map(Decimal, norm['fixed_normalization_Z_pi_pi_interval'])
    require(norm['candidate'] == 'CST-DUST-V1-RAW-K' and norm['boundary_inner_products'] == 'I_2'
            and norm['decision'] == 'FAIL_RAW_KERNEL_AS_CLOSED_EVOLUTION'
            and Decimal(norm['Re_gram_01_lower']) > Decimal('0.5')
            and Decimal('0') < lo < hi < Decimal('1'), 'Certified scoped counterexample')
    require(Decimal(norm['gram_entry_absolute_error_bound'])
            > Decimal(norm['gram_series_absolute_error_bound']) > 0, 'Displayed error accounting')
    response = load(work, 'results/schur_response.json')
    require(response['L_EE'] == '-4' and response['L_effective'] == [['-55/16', '-17/16'], ['-17/16', '145/16']]
            and 'no dust mass-shell or vacuum metric solved' in response['scope'], 'Conditional response scope')


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 29 and z.testzip() is None, 'Archive inventory')
        for name in names:
            path = PurePosixPath(name)
            require(not path.is_absolute() and '..' not in path.parts and name.startswith(PREFIX),
                    'Unsafe archive member')
            require((ROOT/name[len(PREFIX):]).read_bytes() == z.read(name), 'Original bytes: '+name)

        def read(relative):
            return z.read(PREFIX+relative)

        listed = set()
        for line in read('MANIFEST.sha256').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            require(name not in listed and sha(read(name)) == digest, 'Member hash: '+name)
            listed.add(name)
        require({PREFIX+n for n in listed} == set(names)-{PREFIX+'MANIFEST.sha256'}, 'Incomplete manifest')
        require(sha(read(NAME+'.pdf')) == PDF_HASH
                and read(NAME+'.pdf') == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(), 'Report bytes')
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0], 'Frozen plan')
        plan = json.loads(read('plan.json'))
        require(plan['candidate'] == 'CST-DUST-V1-RAW-K'
                and plan['precision']['integer_rational_residual'] == 'EXACT_ZERO'
                and plan['precision']['no_fitted_tolerance'] is True
                and 'analytic failure mechanism identified before computation' in plan['freeze'], 'Plan scope')
        dependencies = {
            'parent_contract.json': 'model_contract_v0_1/contract.json',
            'parent_gate.py': 'model_contract_v0_1/gate.py',
            'weighting_contract.json': 'history_weighting_v0_1/contract.json',
            'gluing.py': 'gluing_v0_1/gluing.py',
            'gluing_verification.json': 'gluing_v0_1/results/verification.json',
        }
        provenance = json.loads(read('inputs/provenance.json'))
        require(provenance['parent_main_commit'] == PARENT
                and set(provenance['input_sha256']) == set(dependencies), 'Predecessor inventory')
        for name, path in dependencies.items():
            data = read('inputs/'+name)
            require(data == (ROOT.parent/path).read_bytes()
                    and sha(data) == provenance['input_sha256'][name], 'Predecessor: '+name)
        expected_results = {n[len(PREFIX):] for n in names if n.startswith(PREFIX+'results/')}
        receipt = json.loads(read('REPLAY.json'))
        require(receipt['all_byte_identical'] is True
                and receipt['result_file_count'] == len(expected_results) == 10
                and {v['file'] for v in receipt['files']} == expected_results, 'Original replay receipt')
        for item in receipt['files']:
            require(item['byte_identical'] is True and sha(read(item['file'])) == item['sha256'],
                    'Original replay digest: '+item['file'])
        check_scope(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-variation-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                for p in (work/'results').iterdir():
                    p.unlink()
                subprocess.run([sys.executable, '-O', '-B', str(work/'analyze.py')], cwd=work,
                               check=True, capture_output=True, text=True)
                check_scope(work)
                actual_results = {p.relative_to(work).as_posix() for p in (work/'results').rglob('*') if p.is_file()}
                require(actual_results == expected_results, 'Replayed output inventory')
                for relative in sorted(expected_results):
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative == 'results/run_manifest.json':
                        a, b = json.loads(expected), json.loads(actual)
                        require(isinstance(b['python'], str) and b['python'], 'Runtime version')
                        a.pop('python'); b.pop('python')
                        require(a == b, relative)
                    elif relative == 'results/checkpoint_P1_record.json':
                        a, b = json.loads(expected), json.loads(actual)
                        # Manifest references were validated independently above.
                        a.pop('run_manifest_sha256'); b.pop('run_manifest_sha256')
                        require(a == b, relative)
                    else:
                        require(expected == actual, relative)
    print('PASS: original ZIP and 29 members, PDF, complete hashes, predecessor inputs, '
          'fixed plan, exact finite variations and scoped MODEL FAIL / seven HOLD decisions'
          + ('; isolated replay of all ten result files agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
