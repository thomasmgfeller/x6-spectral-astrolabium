"""Verify immutable v0.27 evidence and replay the exact checks in isolation."""
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
PACKAGE = ROOT / 'cspp_v027'

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
    require(len(files) == meta['package_files'] == 15, 'File inventory differs')
    with zipfile.ZipFile(ROOT / 'CSPP_Dichteuniforme_Finite_Zeit_v0_27_Pruefpaket.zip') as z:
        members = [item for item in z.infolist() if not item.is_dir()]
        require(len(members) == len(files), 'Archive size differs')
        names = set()
        for item in members:
            path = PurePosixPath(item.filename)
            require(not path.is_absolute() and '..' not in path.parts, 'Unsafe archive path')
            require(path.parts[0] == 'cspp_v027', 'Wrong archive prefix')
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
    require(len(checksums) == meta['checksum_entries'] == 14, 'Checksum count differs')
    require(set(checksums) == set(files) - {'SHA256SUMS'}, 'Checksum inventory differs')
    require(all(files[p] == h for p, h in checksums.items()), 'Checksum differs')
    pdf = 'Dichteuniforme_Finite_Zeit_Stabilitaet_v0_27.pdf'
    require((ROOT / pdf).read_bytes() == (PACKAGE / 'report' / pdf).read_bytes(),
            'Report copies differ')
    status = read(PACKAGE / 'STATUS.json')
    result = read(PACKAGE / 'results/RESULTS.json')
    require(meta['METHOD'] == meta['G1'] == status['method'] == status['g1'] ==
            result['method'] == result['g1'] == 'HOLD', 'Scientific gates changed')
    require(meta['new_random_clouds'] == 0 and
            status['new_poisson_ensemble'] == result['new_poisson_ensemble'] == 'NOT_RUN',
            'New random clouds claimed')
    require(status['github_publication'] == 'NOT_PERFORMED_IN_THIS_STEP',
            'Historical publication flag changed')
    expected = {
        'finite_time_local_poisson_bound':'ANALYTIC_PROOF_WITH_EXACT_FINITE_CHECKS',
        'density_uniformity':'FIXED_Q_RHO_GE_Q_FIXED_FINITE_TIME_PER_DENSITY_PROBABILITY',
        'spatial_uniformity':'FIXED_PROBE_OR_FIXED_DETERMINISTIC_DETECTOR_MEASURE_ONLY',
        'frozen_finite_history_bound':'ANALYTIC_PROOF_WITH_EXACT_INTEGRAL_CHECKS',
        'global_spatial_maximum_uniformity':'EXCLUDED_FOR_DEFINED_NONTRIVIAL_INTERVAL_KERNELS',
        'time_uniform_bound':'NOT_ESTABLISHED',
        'infinite_history':'NOT_CONTROLLED',
        'signed_path_cancellation_bound':'OPEN',
        'practical_error_budget':'NOT_CERTIFIED_CONSTANTS_REMAIN_LARGE',
        'theta_21_accuracy_rejection_v025':'UNCHANGED',
        'physical_kg_output_error':'NOT_EVALUATED',
        'degree_5_candidate':'NOT_RUN',
        'external_peer_review':'NOT_PERFORMED',
    }
    for key, value in expected.items():
        require(status[key] == value, 'Scientific scope changed: ' + key)
    require(result['finite'] == {
        'orders_by_size':{'1':1,'2':2,'3':7,'4':40,'5':357},
        'total_orders':407, 'operator_cases':3256, 'frozen_history_cases':3256,
        'strict_signed_vs_positive_rows':8064}, 'Finite check counts differ')
    require(result['source_hashes_verified'] == 3 and
            result['integrals']['cone_identities'] == 24 and
            result['integrals']['history_identities'] == 48 and
            len(result['negative_controls']) == 6, 'Audit counts differ')
    require(len(result['bounds']) == 8, 'Numerical table differs')
    for row in result['bounds']:
        require(row['precision_checks'] == [40,60,80], 'Precision checks differ')
        if row['T'] == '9/4':
            require(row['history_precision_checks'] == [40,60,80], 'History precision differs')
    require(status['baseline_commit'] == meta['base_commit'] ==
            read(PACKAGE / 'evidence/SOURCES.json')['commit'] ==
            '268516fb5758e87822a5c6302163e2e35d52f641', 'Scientific baseline changed')
    print('PASS: original ZIP, 15 files, 14 checksums, report copies and scoped HOLD status')

def replay():
    before = snapshot(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='cspp-v027-replay-') as tmp:
        copy = Path(tmp) / 'cspp_v027'
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
