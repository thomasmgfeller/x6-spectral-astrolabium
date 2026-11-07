"""Verify the released audit package without network access or dependencies."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PLAN_SHA256 = '03319eb1a504c3a8c619030a35bb1fd2ae48b673b30d5ba3919d7a77753d3281'
SOURCE_MAIN = '7398a19f90e0c3736e2041b7f1480fc9223bbf9e'
PDF = 'CST_DUST_Detektorkopplung_Historienmischung_v0_1.pdf'
FILES = (
    'README.md', 'DERIVATION.md', 'LICENSE', 'NOTICE', 'provenance.json',
    'plan.json', 'plan.sha256', 'coupling_contract.json',
    'analyze.py', 'replay.py', 'build_report.py', 'verify_package.py', 'package.py',
    'inputs/previous_contract.json', 'inputs/previous_derivation.md', 'inputs/previous_core.py',
    'results/controlled_effects.json', 'results/feedback_preparation.json',
    'results/obstruction_and_mixing.json', 'results/verification.json', 'results/replay.json', PDF,
)
SOURCE_BLOBS = {
    'inputs/previous_contract.json': '7c44ef9f7a01767b19a6bc528814db16ed89146c',
    'inputs/previous_derivation.md': '8ea6a272ef519227316acbae03463c831cd6cfa4',
    'inputs/previous_core.py': 'd33b86c0c18c9103007508c2be09378c4e1174d8',
    'LICENSE': 'd645695673349e3947e8e5ae42332d0ac3164cd7',
}
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def read_json(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def verify():
    manifest = read_json('manifest.json')
    require(manifest['schema'] == 'cst-dust-coupling-manifest-v0.1', 'Manifest schema')
    require(manifest['source_main'] == SOURCE_MAIN, 'Manifest source')
    require(set(manifest['files']) == set(FILES), 'Exact release file set')
    for name in FILES:
        data = (ROOT / name).read_bytes()
        item = manifest['files'][name]
        require(item == {'sha256': sha256(data), 'bytes': len(data)}, 'Release bytes: ' + name)

    require(sha256((ROOT / 'plan.json').read_bytes()) == PLAN_SHA256, 'Frozen analysis plan')
    require((ROOT / 'plan.sha256').read_text().split()[0] == PLAN_SHA256, 'Plan digest file')
    provenance = read_json('provenance.json')
    require(provenance['source_main'] == SOURCE_MAIN, 'Pinned Main')
    require(set(provenance['inputs']) == set(SOURCE_BLOBS), 'Pinned source set')
    for name, expected in SOURCE_BLOBS.items():
        data = (ROOT / name).read_bytes()
        identity = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(identity == expected == provenance['inputs'][name]['git_blob'], 'Git source: ' + name)
        require('/blob/' + SOURCE_MAIN + '/' in provenance['inputs'][name]['source_url'], 'Source URL')

    contract = read_json('coupling_contract.json')
    result = read_json('results/verification.json')
    plan = read_json('plan.json')
    for obj in (contract, result, plan):
        require(obj['physical_gates'] == dict.fromkeys(GATES, 'HOLD'), 'All eight gates remain HOLD')
    require(contract['source_main'] == SOURCE_MAIN, 'Contract source')
    require(contract['verdict']['record_preserving'] == 'EXCLUDED_FOR_TARGET_ERROR_BELOW_ONE_HALF', 'Restricted verdict')
    require(contract['verdict']['optimal_norm_error'] == '1/2', 'Sharp error bound')
    require(contract['necessary_mixing']['sufficient'] is False, 'Necessary is not sufficient')
    require(contract['necessary_mixing']['optimal_speed_limit_claim'] is False, 'No optimal speed limit claim')
    for key in ('n5_production', 'paid_compute', 'physical_detector_derived'):
        require(contract[key] is False, 'Contract scope: ' + key)
    witness = contract['finite_witness']
    require(witness['status'] == 'ALGEBRAIC_CONTROL_ONLY', 'Finite witness scope')
    require(witness['physical_cst_derivation'] is False and witness['full_hilbert_space_certified'] is False, 'No physical/full-space certification')
    require(witness['leakage_counterexample'] == {'compressed_error': '0', 'full_space_error': '1'}, 'Full-space counterexample')

    require(result['status'] == 'PASS_RESTRICTED_COUPLING_AUDIT', 'Audit status')
    require(result['plan_sha256'] == PLAN_SHA256, 'Audit plan identity')
    expected_counts = {'joint_unitaries': 75, 'controlled_pointer_cases': 900,
        'direct_joint_controls': 900, 'adaptive_instruments': 25, 'adaptive_branches': 100,
        'nonzero_conditioned_branches': 81, 'diagonal_grid_cases': 25,
        'weighted_obstruction_controls': 3, 'rational_mixing_controls': 6}
    require(all(result[k] == v for k, v in expected_counts.items()), 'Control counts')
    require(result['physical_mixing_coupling'] == 'NOT_DERIVED', 'Physical coupling remains open')
    require(result['n5_production_run'] is False and result['external_replication'] is False, 'Evidence scope')
    require(len(result['negative_controls']) == 7 and all(x['status'] == 'REJECTED' for x in result['negative_controls']), 'Seven negative controls')
    replay = read_json('results/replay.json')
    names = {'controlled_effects.json', 'feedback_preparation.json', 'obstruction_and_mixing.json', 'verification.json'}
    require(replay['status'] == 'PASS_BYTE_IDENTICAL' and replay['scientific_files'] == 4, 'Replay status')
    require(set(replay['sha256']) == names, 'Replay file set')
    for name in names:
        require(replay['sha256'][name] == sha256((ROOT / 'results' / name).read_bytes()), 'Replay digest: ' + name)
    require((ROOT / PDF).read_bytes().startswith(b'%PDF-'), 'PDF signature')
    return {'status': 'PASS_PACKAGE', 'manifest_files': len(FILES), 'pinned_source_files': len(SOURCE_BLOBS),
            'scientific_files': len(names), 'physical_gates': '8 HOLD', 'source_main': SOURCE_MAIN}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, sort_keys=True))
