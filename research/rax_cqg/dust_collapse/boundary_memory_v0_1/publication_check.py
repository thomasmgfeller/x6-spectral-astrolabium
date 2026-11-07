#!/usr/bin/env python3
"""Check unchanged artifacts, source provenance, claim scope and exact replay."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
NAME = 'CST_DUST_Randgedaechtnis_Fortsetzung_v0_1'
ZIP_HASH = '1181a8f8242f503cb48db4415b0efe06c70d307bc057ebcf00cf7dfaace80fda'
PDF_HASH = '6113e53f2ecaaa70f2498c41bbb1e64464f6a824d286b698c57c33308b7ef5cd'
PLAN_HASH = '9079923b05523664d420fb1de8505a0117bdd26ee1c615994b0929e9b8ea6e48'
PARENT = '886052d8eb9d619da91896d23e0a7ede511ef30f'
EXACT = {'finite_growth.json', 'counting_measure.json', 'memory_counterexamples.json',
         'boundary_norms.json', 'verification.json'}
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
            result['new_dynamical_CST_ensembles'] is False, 'Claim scope')
    require(result['source_files'] == 7, 'Seven source files')
    require(result['scoped_decisions'] == {
        'FULL_PAST_ACTION_UPDATE': 'PASS_EXACT',
        'NATURAL_LABEL_COUNTING_REWRITE': 'PASS_CONDITIONAL_ON_INHERITED_MEASURE',
        'FIXED_TOP_LAYER_COLLAR_EXACT_CLOSURE': 'FAIL_FOR_ALL_FUTURE_IDEALS',
        'COMMON_SCALAR_COUNTING_NORM': 'FAIL',
        'LOCAL_NORMALIZATION_PRESERVES_ORIGINAL_AMPLITUDES': 'FAIL',
        'FIXED_HORIZON_PULLBACK': 'PASS_CONDITIONAL_ON_CHOSEN_TERMINAL_PRODUCT',
        'PHYSICAL_BOUNDARY_PRODUCT_AND_INFINITE_CONTINUATION': 'HOLD'}, 'Scoped decisions')
    growth = json.loads(read('results/finite_growth.json'))
    require(growth['total_natural_orders'] == 408 and growth['checks'] == {
        'ideal_extensions': 407, 'rational_action_cases': 2442,
        'direct_gravity_comparisons': 408, 'linear_extension_counts': 408,
        'growth_exchange_cases': 268, 'growth_exchange_field_cases': 536,
        'terminal_closures': 816}, 'Exact growth controls')
    require(len(json.loads(read('results/counting_measure.json'))['sectors']) == 6,
            'Six exact label sums')
    require(len(json.loads(read('results/memory_counterexamples.json'))['cases']) == 8,
            'Eight collar witnesses')
    norms = json.loads(read('results/boundary_norms.json'))
    require(norms['counting_product_norm_factors'] == {
        'one_internal': '5/4', 'chain_two': '49/36', 'antichain_two': '2'}, 'Norm witness')
    require(norms['locally_normalized_path_weight_squares'] == ['16/245', '2/45'] and
            norms['equal_corrected_amplitudes_before_normalization'] == '1/3',
            'Local normalization changes original amplitudes')
    require(norms['metric_checks'] == 30 and norms['physical_terminal_metric'] == 'NOT_SELECTED',
            'Conditional finite-horizon products')
    contract = json.loads(read('boundary_contract.json'))
    require(contract['physical_inner_product']['status'] == 'NOT_SELECTED' and
            contract['status'] == 'EXACT_REPRESENTATION_PHYSICAL_SELECTION_OPEN', 'State contract')


def run(replay=False):
    archive = ROOT.parent / 'packages' / (NAME + '_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        prefix = NAME + '/'
        require(len(names) == len(set(names)) == 30 and z.testzip() is None, 'Archive inventory')
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
        require(provenance['commit'] == PARENT and len(provenance['files']) == 7, 'Provenance')
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
            with tempfile.TemporaryDirectory(prefix='cst-boundary-memory-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp) / NAME
                subprocess.run([sys.executable, '-O', '-B', 'replay.py'], cwd=work,
                               check=True, capture_output=True, text=True)
                require((work / 'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 30 members, PDF, seven byte-identical sources and eight physical HOLDs' +
          ('; five exact results reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
