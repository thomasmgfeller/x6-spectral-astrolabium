"""Verify original quantum-structure evidence and replay without changing it."""
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
NAME = 'CST_DUST_Zustandsraum_Constraints_v0_1'
PREFIX = NAME + '/'
ZIP_HASH = '734d37c423208a0362d5ef1997364ae178be30b5e9c64b657006261592695624'
PDF_HASH = '3242dcacd9251eb1b653690fa57d6e7418616fee225de05f29c1df514aaf3712'
PLAN_HASH = '95412203ca3292d9dfb51d8b7e0628230c0cb783ff174e2a98668a5c6a22fa3e'
PARENT = '3595df81b8655a5183cdbf5c5da077aef51e4259'
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
    require(data['finite_mathematical_checks'] == 'RUN'
            and data['physical_4D_dynamics'] == 'NOT_RUN'
            and data['new_physical_4D_ensembles'] == data['random_draws'] == 0
            and data['parent_main_commit'] == PARENT and data['plan_sha256'] == PLAN_HASH,
            'Execution scope/provenance')
    require(set(data['source_sha256']) == {'quantum_structure.py', 'analyze.py'}, 'Executed sources')
    for name, digest in data['source_sha256'].items():
        require(sha((work/name).read_bytes()) == digest, 'Executed source: '+name)
    spec = importlib.util.spec_from_file_location('quantum_structure_parent_gate', work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    for key, candidate in [('quotient', 'CST-DUST-QS1-RELABEL'),
                           ('common_metric', 'CST-DUST-V1-RAW-K-COMMON-M')]:
        rec = load(work, 'results/checkpoint_P1_'+key+'_record.json')
        require(rec['checkpoint_id'] == 'P1' and rec['execution'] == 'RUN'
                and rec['scope']['model_id'] == candidate
                and rec['run_manifest_sha256'] == sha(manifest.read_bytes()), 'Scoped P1 provenance')
        if key == 'common_metric':
            item = rec['gates']['MODEL']['quantum_consistency']
            require(item['outcome'] == 'VIOLATED' and item['evidence_kind'] == 'ANALYTIC_COUNTEREXAMPLE',
                    'Candidate-specific negative result')
        evaluated = gate.evaluate(rec, work/'inputs/parent_contract.json', manifest)
        expected = {g: 'FAIL' if key == 'common_metric' and g == 'MODEL' else 'HOLD' for g in GATES}
        require(evaluated['record_valid'] and evaluated['decisions'] == expected
                and evaluated['physical_claim_automatically_authorized'] is False, 'Physical scope')
        require(evaluated == load(work, 'results/checkpoint_P1_'+key+'_audit.json'), 'Archived P1 audit')
    result = load(work, 'results/verification.json')
    counts = {'labeled_order_support_states': 3671, 'group_action_instances': 85035,
              'orbit_blocks': 234, 'projector_rows': 3671, 'joint_action_checks': 4817,
              'nonzero_mass_shell_polynomials': 7249, 'positive_metric_controls': 1,
              'negative_metric_controls': 1, 'relational_unitarity_checks': 4,
              'relational_composition_checks': 16, 'distributional_constraint_samples': 4,
              'underdetermination_witnesses': 1,
              'new_physical_4D_ensembles': 0, 'new_sprinklings': 0, 'random_draws': 0}
    require(all(result[k] == v for k, v in counts.items()), 'Evidence inventory')
    statuses = {'relabel_projector': 'PASS_EXACT_AUXILIARY_CONSTRUCTION',
                'ordinary_L2_Euler_constraints': 'TRIVIAL_ON_NONEMPTY_DUST_SUPPORT',
                'raw_K_common_metric': 'FAIL_EVERY_COMMON_POSITIVE_METRIC',
                'physical_state_space': 'HOLD_DYNAMICAL_REDUCTION_NOT_DEFINED',
                'CST_relational_Hamiltonian': 'HOLD_NOT_DERIVED', 'causal_junction': 'HOLD',
                'common_exterior': 'HOLD', 'regularity': 'HOLD', 'global_bounce': 'HOLD_NOT_RUN'}
    require(all(result[k] == v for k, v in statuses.items()) and result['paid_runs'] is False,
            'Scientific claim changed')
    certificate = load(work, 'results/common_metric_certificate.json')
    lo, hi = map(Decimal, certificate['trace_determinant_ratio']['imag_interval'])
    d_lo, d_hi = map(Decimal, certificate['determinant_norm_squared'])
    require(certificate['candidate'] == 'CST-DUST-V1-RAW-K'
            and certificate['identification'] == '(0,1) -> (2,3) by translation; one common positive definite Hermitian M'
            and certificate['decision'] == 'FAIL_EVERY_COMMON_POSITIVE_METRIC'
            and lo < hi < 0 and 0 < d_lo < d_hi, 'Certified common-metric obstruction')
    controls = load(work, 'results/reference_controls.json')
    reference = controls['relational_reference']
    require(reference['status'] == 'PASS_MATHEMATICAL_REFERENCE_NOT_CST_DERIVATION'
            and reference['norm_checks'] == 4 and reference['composition_checks'] == 16
            and reference['constraint_sample_checks'] == 4, 'Reference is not CST-derived')


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 34 and z.testzip() is None, 'Archive inventory')
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
        require(plan['candidate'] == 'CST-DUST-QS1-RELABEL'
                and plan['precision']['fitted_tolerances'] is False
                and 'structural obstructions anticipated before numerical certification' in plan['freeze'], 'Plan scope')
        dependencies = {
            'parent_contract.json': 'model_contract_v0_1/contract.json',
            'parent_gate.py': 'model_contract_v0_1/gate.py',
            'variation.py': 'variation_v0_1/variation.py',
            'gluing.py': 'gluing_v0_1/gluing.py',
            'previous_plan.json': 'variation_v0_1/plan.json',
            'previous_normalization.json': 'variation_v0_1/results/normalization_counterexample.json',
            'previous_verification.json': 'variation_v0_1/results/verification.json',
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
        require(receipt['status'] == 'PASS_BYTE_IDENTICAL_ISOLATED_REPLAY'
                and receipt['result_files'] == len(expected_results) == 13
                and {'results/'+n for n in receipt['result_sha256']} == expected_results,
                'Original replay receipt')
        for name, digest in receipt['result_sha256'].items():
            require(sha(read('results/'+name)) == digest, 'Original replay digest: '+name)
        check_scope(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-quantum-structure-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                for p in (work/'results').iterdir():
                    p.unlink()
                subprocess.run([sys.executable, '-O', '-B', str(work/'analyze.py')], cwd=work,
                               check=True, capture_output=True, text=True)
                check_scope(work)
                actual_results = {p.relative_to(work).as_posix() for p in (work/'results').rglob('*') if p.is_file()}
                require(actual_results == expected_results, 'Replayed output inventory')
                records = {'results/checkpoint_P1_'+k+'_record.json' for k in ('quotient', 'common_metric')}
                for relative in sorted(expected_results):
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative == 'results/run_manifest.json':
                        a, b = json.loads(expected), json.loads(actual)
                        require(isinstance(b['python'], str) and b['python'], 'Runtime version')
                        a.pop('python'); b.pop('python')
                        require(a == b, relative)
                    elif relative in records:
                        a, b = json.loads(expected), json.loads(actual)
                        # Each manifest reference was independently checked above.
                        a.pop('run_manifest_sha256'); b.pop('run_manifest_sha256')
                        require(a == b, relative)
                    else:
                        require(expected == actual, relative)
    print('PASS: original ZIP and 34 members, PDF, complete hashes, predecessor inputs, '
          'fixed plan, label reduction and separate HOLD / common-metric FAIL decisions'
          + ('; isolated replay of all 13 result files agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
