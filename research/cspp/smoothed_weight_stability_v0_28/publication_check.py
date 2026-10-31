"""Verify immutable v0.28 evidence and replay the exact checks in isolation."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'cspp_v028'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def snapshot(path):
    return {str(p.relative_to(path)): digest(p)
            for p in path.rglob('*') if p.is_file()}

def check():
    meta = read(ROOT / 'PUBLICATION.json')
    for name, sha in meta['artifacts'].items():
        require(digest(ROOT / name) == sha, 'Artifact hash differs: ' + name)
    files = snapshot(PACKAGE)
    require(len(files) == meta['package_files'] == 17, 'File inventory differs')
    with zipfile.ZipFile(ROOT / 'CSPP_Geglaettete_Intervallgewichte_v0_28_Pruefpaket.zip') as z:
        members = [item for item in z.infolist() if not item.is_dir()]
        require(len(members) == len(files), 'Archive size differs')
        names = set()
        for item in members:
            path = PurePosixPath(item.filename)
            require(not path.is_absolute() and '..' not in path.parts, 'Unsafe archive path')
            require(path.parts[0] == 'cspp_v028', 'Wrong archive prefix')
            relative = str(PurePosixPath(*path.parts[1:]))
            require(relative not in names, 'Duplicate archive member')
            names.add(relative)
            require((PACKAGE / relative).read_bytes() == z.read(item),
                    'Archive bytes differ: ' + relative)
        require(names == set(files), 'Archive inventory differs')
    checksums = {}
    for line in (PACKAGE / 'SHA256SUMS').read_text().splitlines():
        sha, path = line.split('  ', 1)
        require(path not in checksums, 'Duplicate checksum')
        checksums[path] = sha
    require(len(checksums) == meta['checksum_entries'] == 16, 'Checksum count differs')
    require(set(checksums) == set(files) - {'SHA256SUMS'}, 'Checksum inventory differs')
    require(all(files[p] == h for p, h in checksums.items()), 'Checksum differs')
    pdf = 'Geglaettete_Intervallgewichte_Stabilitaetsbudget_v0_28.pdf'
    require((ROOT / pdf).read_bytes() == (PACKAGE / 'report' / pdf).read_bytes(),
            'Report copies differ')
    status = read(PACKAGE / 'STATUS.json')
    result = read(PACKAGE / 'results/RESULTS.json')
    require(meta['METHOD'] == meta['G1'] == status['method'] == status['g1'] ==
            result['method'] == result['g1'] == 'HOLD', 'Scientific gates changed')
    require(meta['new_random_clouds'] == status['new_random_clouds'] ==
            result['new_random_clouds'] == 0, 'New random clouds claimed')
    require(status['github_publication'] == 'NOT_PERFORMED_IN_THIS_STEP',
            'Historical publication flag changed')
    expected = {
        'binomial_composition':'ANALYTIC_IDENTITY_WITH_EXACT_FINITE_CHECKS',
        'global_smoothed_weight_suprema':'SIX_EXACT_CERTIFICATES_WITH_ANALYTIC_INFINITE_TAILS',
        'primary_density_scope':'FIXED_Q_RHO_GE_3_OVER_PI',
        'operator_and_physical_task':'UNCHANGED',
        'captured_cancellation':'SIGNED_LAYER_CONTRIBUTIONS_INSIDE_EACH_SMOOTHED_WEIGHT',
        'cancellation_between_distinct_paths':'NOT_ESTABLISHED',
        'practical_original_error_budget':'NOT_CERTIFIED',
        'actual_kg_residuals':'NOT_EVALUATED',
        'theta_21_accuracy_rejection_v025':'UNCHANGED',
        'time_uniform_bound':'NOT_ESTABLISHED',
        'infinite_history':'NOT_CONTROLLED',
        'c0_floor':'LIMITATION_OF_SCALAR_ENTRY_ENVELOPE_METHOD_NOT_PHYSICAL_LOWER_BOUND',
        'degree_5_candidate':'NOT_RUN',
        'proof_assistant':'NOT_PERFORMED',
        'external_peer_review':'NOT_PERFORMED',
    }
    for key, value in expected.items():
        require(status[key] == value, 'Scientific scope changed: ' + key)
    require(result['sources_verified'] == 5 and result['total_integer_weights'] == 1782 and
            result['semigroup_checks'] == 648, 'Audit counts differ')
    require(result['graph_checks'] == {'operator_cases':2442,'frozen_history_cases':2442},
            'Graph check counts differ')
    require(len(result['certificates']) == 6 and len(result['negative_controls']) == 6 and
            len(result['budgets']) == 10, 'Certificate or budget counts differ')
    for row in result['budgets']:
        require(row['precision_checks'] == [40,60,80], 'Precision checks differ')
    require(result['scope'] == {'q':'3/(16*pi)','rho_floor':'3/pi','T':'9/4','H':'4',
                               'delta':'1/100','output_budget':'1/1000'}, 'Physical scope changed')
    require(status['baseline_commit'] == result['base_commit'] == meta['base_commit'] ==
            read(PACKAGE / 'evidence/SOURCES.json')['commit'] ==
            '63c8be4df882316a7629907a5da3ee012e47e309', 'Scientific baseline changed')
    print('PASS: original ZIP, 17 files, 16 checksums, report copies and scoped HOLD status')


def replay():
    before = snapshot(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='cspp-v028-replay-') as tmp:
        copy = Path(tmp) / 'cspp_v028'
        shutil.copytree(PACKAGE, copy)
        subprocess.run([sys.executable, '-I', '-O', '-B', str(copy / 'reproduce.py'), '--check'],
                       check=True, cwd=tmp, timeout=120)
        require(snapshot(copy) == before, 'Replay changed package bytes')
    require(snapshot(PACKAGE) == before, 'Published package changed')
    print('PASS: isolated exact replay, byte-identical results and unchanged evidence')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    check()
    if args.replay:
        replay()
