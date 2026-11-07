#!/usr/bin/env python3
"""Check unchanged artifacts, source provenance, claim scope and exact replay."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
NAME = 'CST_DUST_Normpfad_Kohaerenter_Quotient_v0_1'
ZIP_HASH = '64f615f4db62231db334817652dd7d5da7b291e7a1cbc9e49540bc8a26f51c60'
PDF_HASH = '541ca9e30ebdd9ee5abd39d6d5a53375d65fd84d1eed389a768a623caed7d428'
PLAN_HASH = '91d43a2e7a0a5e457546ac42d7f6b284baca9c88b05716babe40d209b1450818'
PARENT = '573084d007ae96d82eb6c241df6ae1d572523418'
EXACT = {'diagonal_norms.json', 'horizon_controls.json', 'coherent_quotient.json',
         'coherent_contraction.json', 'verification.json'}
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_scope(read):
    result = json.loads(read('results/verification.json'))
    require(result['source_commit'] == PARENT and result['plan_sha256'] == PLAN_HASH,
            'Source and plan')
    require(set(result['physical_decisions']) == GATES and
            set(result['physical_decisions'].values()) == {'HOLD'}, 'Eight physical HOLDs')
    require(result['formal_proof_checker'] is False and
            result['new_dynamical_CST_ensembles'] is False and
            result['physical_parameter_selected'] is False, 'Claim scope')
    require(result['source_files'] == 6, 'Six source files')
    require(result['scoped_decisions'] == {
        'DIAGONAL_AUXILIARY_NORM_PATH_EXISTENCE': 'PASS_CONSTRUCTIVE_ALL_STAGES',
        'UNIQUENESS_FROM_POSITIVITY_AND_COVARIANCE': 'FAIL',
        'HARMONIC_TERMINAL_HORIZON_INDEPENDENCE': 'PASS_EXACT_CONDITIONAL',
        'UNIFORMLY_BOUNDED_INHERITED_COHERENT_CONTRACTION': 'FAIL_IN_DECLARED_DIAGONAL_CLASS',
        'UNMARKED_COHERENT_QUOTIENT_DESCENT': 'PASS_EXACT',
        'DIAGONAL_QUOTIENT_ISOMETRY_ALL_STATES': 'FAIL_AT_TWO_TO_THREE_ELEMENTS',
        'NONDIAGONAL_UNMARKED_QUOTIENT_METRICS': 'PASS_CONSTRUCTIVE_UNQUALIFIED_PHYSICALLY',
        'PHYSICAL_PRODUCT_AND_QUANTUM_MEASURE_EXTENSION': 'HOLD'}, 'Scoped decisions')
    diagonal = json.loads(read('results/diagonal_norms.json'))
    require(diagonal['natural_counts'] == [1, 1, 2, 7, 40, 357, 4824], 'Natural-order census')
    require(diagonal['checks'] == {
        'independent_DAGs': 33868, 'edge_probability_comparisons': 15696,
        'transition_recursions': 1224, 'metric_recursions': 1224,
        'positive_metric_values': 15696, 'normalization_sums': 21}, 'Exact norm controls')
    for row in diagonal['records']:
        lower = F(row['sum_inverse_extensions'])
        for sample in row['percolation']:
            require(F(sample['dual_norm_squared']) >= lower**2 and
                    F(sample['auxiliary_state_norm_squared']) == 1, 'Dual norm control')
    horizon = json.loads(read('results/horizon_controls.json'))
    require(horizon['exact_harmonic_checks'] == 17118 and
            len(horizon['nonharmonic_controls']) == 10, 'Horizon controls')
    require(horizon['harmonic_ratio_chain_over_antichain'] ==
            {'1/4': '1/12', '1/2': '1/4', '3/4': '3/4'}, 'Different relative norms')
    quotient = json.loads(read('results/coherent_quotient.json'))
    require(quotient['class_counts'] == [1, 1, 2, 5, 16, 63] and quotient['checks'] == {
        'orbit_aut_counts': 88, 'representative_independent_columns': 51,
        'endpoint_amplitudes': 87, 'left_inverse_entries': 287}, 'Coherent quotient controls')
    require(quotient['B_2_to_3'] == [
        ['1/3', '0'], ['4/3', '1/3'], ['1', '0'], ['0', '1/2'], ['0', '1']], 'Common-child matrix')
    require(quotient['forced_diagonal_metric_offdiagonal'] == '4*d_mixed/9', 'Positive cross term')
    require(len(quotient['constructive_metric_checks']) == 8 and
            all(F(p) > 0 for row in quotient['constructive_metric_checks']
                for p in row['positive_LDL_pivots']), 'Positive finite full metrics')
    require(quotient['uniform_bounds'] == 'NOT_PROVED' and
            quotient['physical_event_algebra'] == 'NOT_SELECTED', 'Quotient scope')
    contract = json.loads(read('norm_contract.json'))
    require(contract['diagonal_class']['normalization'] == 'h_0(empty)=1' and
            contract['coherent_quotient']['full_marked_field_quotient'] == 'NOT_CONSTRUCTED',
            'Norm and marked-field scope')


def run(replay=False):
    archive = ROOT.parent / 'packages' / (NAME + '_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        prefix = NAME + '/'
        require(len(names) == len(set(names)) == 28 and z.testzip() is None, 'Archive inventory')
        for name in names:
            rel = PurePosixPath(name)
            require(not rel.is_absolute() and '..' not in rel.parts and name.startswith(prefix),
                    'Safe archive member')
            require(z.read(name) == (ROOT / name[len(prefix):]).read_bytes(),
                    'Original member bytes: ' + name)
        read = lambda p: z.read(prefix + p)
        listed = set()
        for line in read('MANIFEST.sha256').decode().splitlines():
            digest, rel = line.split(maxsplit=1)
            require(rel not in listed and sha(read(rel)) == digest, 'Manifest entry: ' + rel)
            listed.add(rel)
        require({prefix + rel for rel in listed} == set(names) - {prefix + 'MANIFEST.sha256'},
                'Complete manifest')
        require(sha(read(NAME + '.pdf')) == PDF_HASH and read(NAME + '.pdf') ==
                (ROOT.parent / 'reports' / (NAME + '.pdf')).read_bytes(), 'PDF copies')
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0],
                'Frozen plan')
        provenance = json.loads(read('inputs/provenance.json'))
        require(provenance['commit'] == PARENT and len(provenance['files']) == 6, 'Provenance')
        for name, entry in provenance['files'].items():
            rel = PurePosixPath(entry['path'])
            require(not rel.is_absolute() and '..' not in rel.parts, 'Safe source path')
            data = read('inputs/' + name)
            require(data == (REPO / entry['path']).read_bytes() and sha(data) == entry['sha256'],
                    'Byte-identical source: ' + name)
        receipt = json.loads(read('results/replay.json'))
        require(receipt['isolated_replay'] == 'PASS' and receipt['result_files'] == 5 and
                {item['name'] for item in receipt['checks']} == EXACT, 'Replay inventory')
        for item in receipt['checks']:
            require(item['byte_identical'] and item['sha256'] == sha(read('results/' + item['name'])),
                    'Replay digest')
        check_scope(read)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cst-normpath-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp) / NAME
                subprocess.run([sys.executable, '-O', '-B', 'replay.py'], cwd=work,
                               check=True, capture_output=True, text=True)
                require((work / 'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 28 members, PDF, six byte-identical sources and eight physical HOLDs' +
          ('; five exact results reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
