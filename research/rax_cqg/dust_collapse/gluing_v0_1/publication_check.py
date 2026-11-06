"""Check original gluing artifacts and replay exact results without editing them."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Verklebungsregel_v0_1'
PREFIX = NAME + '/'
ZIP_HASH = '83112d1528246189892e741e73cfc19ecc58b8cc7561421a9901b4d6ea836054'
PDF_HASH = '59158543b05c4d533416b0190bb5dfefcaaf2f2204363f12a471684b1c0d5e76'
PLAN_HASH = '67f4c8fad70b29f6ac745c6a05a45ff91510397d7ed0383d8d27c4cde6c81cb4'
PARENT = 'bc8c154be60c483c8a5a8f085c1b3b0668d8afa1'
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
    require(data['physical_execution'] == 'NOT_RUN'
            and data['exact_finite_enumeration'] == 'RUN'
            and data['new_dynamic_CST_ensembles'] == data['new_random_draws'] == 0
            and data['parent_main_commit'] == PARENT and data['plan_sha256'] == PLAN_HASH,
            'Execution scope/provenance')
    require(set(data['source_sha256']) == {'gluing.py', 'analyze.py', 'verify_independent.py'},
            'Executed source inventory')
    for name, digest in data['source_sha256'].items():
        require(sha((work/name).read_bytes()) == digest, 'Executed source: '+name)
    spec = importlib.util.spec_from_file_location('gluing_parent_gate', work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    rec = load(work, 'results/checkpoint_P5_record.json')
    require(rec['checkpoint_id'] == 'P5' and rec['execution'] == 'NOT_RUN'
            and rec['run_manifest_sha256'] == sha(manifest.read_bytes()), 'P5 provenance')
    evaluated = gate.evaluate(rec, work/'inputs/parent_contract.json', manifest)
    require(evaluated['record_valid'] and evaluated['decisions'] == {g: 'HOLD' for g in GATES}
            and evaluated['physical_claim_automatically_authorized'] is False,
            'Physical gate promoted')
    require(evaluated == load(work, 'results/checkpoint_P5_audit.json'), 'Archived P5 audit')
    result = load(work, 'results/verification.json')
    counts = {'labeled_orders': 4473, 'unlabeled_orders': 87, 'partition_checks': 130116,
              'smoothed_checks': 6372, 'current_checks': 130116,
              'naive_additivity_failures': 122960, 'cross_only_failures': 45888,
              'associativity_checks': 7998, 'marked_measure_sectors': 10,
              'marked_orbit_checks': 1549, 'kernel_pairs': 4,
              'discrete_variation_identities': 32, 'nonidentity_move_instances': 400,
              'controls': 13, 'separate_gate_policy_controls': 5,
              'new_dynamic_CST_ensembles': 0, 'new_random_draws': 0, 'new_sprinklings': 0}
    require(all(result[k] == v for k, v in counts.items()), 'Exact evidence inventory')
    expected = {'action_composition': 'PASS_EXACT_FINITE_IDENTITY',
                'measure_composition': 'PASS_CONDITIONAL_COUNTING_MEASURE',
                'finite_variation_identity': 'PASS_EXACT_FINITE_IDENTITY',
                'physical_CST_junction': 'HOLD_NOT_DERIVED',
                'physical_CST_bounce': 'HOLD_NOT_RUN', 'physical_CST_regularity': 'HOLD',
                'physical_CST_extension': 'HOLD'}
    require(all(result[k] == v for k, v in expected.items())
            and result['all_exact_residuals_zero'] is True and result['paid_runs'] is False,
            'Scientific scope')
    control = load(work, 'results/controls.json')
    require(len(control) == 13 and all(c['pass'] and c['actual'] == c['expected'] for c in control),
            'Structure controls')
    guard = load(work, 'results/gate_negative_controls.json')
    protected = set(load(work, 'inputs/parent_contract.json')['decision_rules']['finite_observations_not_accepted_for'])
    require(len(guard) == 5 and {g['requirement'] for g in guard} == protected
            and all(g['decision'] == 'HOLD' and g['test'] == 'PASS'
                    and g['synthetic_policy_fixture_only'] is True for g in guard), 'Policy controls')
    independent = load(work, 'results/independent_verification.json')
    require(independent['status'] == 'PASS_IMPLEMENTATION_CROSSCHECK'
            and independent['total_orders'] == 4473 and independent['total_partition_checks'] == 130116
            and independent['physical_ensemble'] is False, 'Independent implementation')
    witness = load(work, 'results/coarse_state_counterexample.json')
    require(witness['N'] == 3 and witness['F4_both'] == 1
            and witness['at_z_i_upper'] == ['1', '0']
            and witness['at_z_i_lower'] == ['1', '2'], 'Coarse-state counterexample')


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 35 and z.testzip() is None, 'Archive inventory')
        for name in names:
            path = PurePosixPath(name)
            require(not path.is_absolute() and '..' not in path.parts and name.startswith(PREFIX),
                    'Unsafe archive member')
            require((ROOT/name[len(PREFIX):]).read_bytes() == z.read(name), 'Original bytes: '+name)

        def read(relative):
            return z.read(PREFIX+relative)

        listed = set()
        for line in read('SHA256SUMS').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            require(name not in listed and sha(read(name)) == digest, 'Member hash: '+name)
            listed.add(name)
        require({PREFIX+n for n in listed} == set(names)-{PREFIX+'SHA256SUMS'}, 'Incomplete hashes')
        require(sha(read(NAME+'.pdf')) == PDF_HASH
                and read(NAME+'.pdf') == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(), 'Report bytes')
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0], 'Frozen plan')
        plan = json.loads(read('plan.json'))
        require(plan['acceptance']['all_integer_rational_polynomial_residuals'] == 'EXACT_ZERO'
                and plan['acceptance']['no_floating_tolerance'] is True
                and plan['carrier']['dimension_selection'] == 'NONE; not physical 4D ensembles', 'Plan scope')
        dependencies = {
            'parent_contract.json': 'model_contract_v0_1/contract.json',
            'parent_gate.py': 'model_contract_v0_1/gate.py',
            'weighting_contract.json': 'history_weighting_v0_1/contract.json',
            'boundary_decision.json': 'boundary_completion_v0_1/results/closure_decision.json',
            'boundary_derivation.md': 'boundary_completion_v0_1/DERIVATION.md',
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
        require(receipt['isolated_replay'] == 'PASS_BYTE_IDENTICAL_RESULTS'
                and receipt['result_files'] == len(expected_results) == 14
                and {'results/'+n for n in receipt['sha256']} == expected_results,
                'Original replay receipt')
        for name, digest in receipt['sha256'].items():
            require(sha(read('results/'+name)) == digest, 'Original replay digest: '+name)
        check_scope(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-gluing-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                for p in (work/'results').iterdir():
                    p.unlink()
                for script in ('analyze.py', 'verify_independent.py'):
                    subprocess.run([sys.executable, '-O', '-B', str(work/script)], cwd=work,
                                   check=True, capture_output=True, text=True)
                check_scope(work)
                actual_results = {p.relative_to(work).as_posix() for p in (work/'results').rglob('*') if p.is_file()}
                require(actual_results == expected_results, 'Replayed output inventory')
                for relative in sorted(expected_results):
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative == 'results/run_manifest.json':
                        a, b = json.loads(expected), json.loads(actual)
                        require(isinstance(b['python'], str) and b['python'], 'Missing runtime version')
                        a.pop('python'); b.pop('python')
                        require(a == b, relative)
                    elif relative == 'results/checkpoint_P5_record.json':
                        a, b = json.loads(expected), json.loads(actual)
                        # Both record-to-manifest links were checked before normalization.
                        a.pop('run_manifest_sha256'); b.pop('run_manifest_sha256')
                        require(a == b, relative)
                    else:
                        require(expected == actual, relative)
    print('PASS: original ZIP and 35 members, PDF, complete hashes, predecessor inputs, '
          'fixed plan, independent finite checks and all eight separate physical HOLD decisions'
          + ('; isolated replay of all 14 result files agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
