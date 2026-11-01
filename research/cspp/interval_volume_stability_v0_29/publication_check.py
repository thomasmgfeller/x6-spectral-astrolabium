"""Verify immutable v0.29 evidence and replay the exact checks in isolation."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'cspp_v029'

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
    require(len(files) == meta['package_files'] == 18, 'File inventory differs')
    with zipfile.ZipFile(ROOT / 'CSPP_Intervallvolumen_Pfadstabilitaet_v0_29_Pruefpaket.zip') as z:
        members = [item for item in z.infolist() if not item.is_dir()]
        require(len(members) == len(files), 'Archive size differs')
        names = set()
        for item in members:
            path = PurePosixPath(item.filename)
            require(not path.is_absolute() and '..' not in path.parts, 'Unsafe archive path')
            require(path.parts[0] == 'cspp_v029', 'Wrong archive prefix')
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
    require(len(checksums) == meta['checksum_entries'] == 17, 'Checksum count differs')
    require(set(checksums) == set(files) - {'SHA256SUMS'}, 'Checksum inventory differs')
    require(all(files[p] == h for p, h in checksums.items()), 'Checksum differs')
    pdf = 'Intervallvolumen_Pfadstabilitaet_v0_29.pdf'
    require((ROOT / pdf).read_bytes() == (PACKAGE / 'report' / pdf).read_bytes(),
            'Report copies differ')
    status = read(PACKAGE / 'STATUS.json')
    result = read(PACKAGE / 'results/RESULTS.json')
    require(meta['METHOD'] == meta['G1'] == status['method'] == status['g1'] ==
            result['method'] == result['g1'] == 'HOLD', 'Scientific gates changed')
    require(meta['new_random_clouds'] == status['new_random_clouds'] ==
            result['new_random_clouds'] == 0, 'New random clouds claimed')
    expected = {
        'github_publication': 'NOT_PERFORMED_IN_THIS_STEP',
        'poisson_volume_envelope': 'ANALYTIC_DENSITY_UNIFORM_EXPECTED_ABSOLUTE_WEIGHT',
        'single_chain_factorization': 'PROVED_WITH_MECKE_INSERTIONS_AND_DISJOINT_ADJACENT_INTERVALS',
        'domain_scope': 'COMPLETE_CAUSAL_INTERVALS_CAUSAL_DIAMONDS_INCLUDED',
        'arbitrary_clipped_domains': 'V028_CONSTANT_ENVELOPE_REMAINS_APPLICABLE',
        'finite_time_history_bound': 'POSITIVE_VOLTERRA_MAJORANT_WITH_CERTIFIED_NUMERICAL_ENCLOSURES',
        'primary_density_scope': 'FIXED_Q_RHO_GE_3_OVER_PI',
        'operator_and_physical_task': 'UNCHANGED',
        'cancellation_between_distinct_paths': 'NOT_ESTABLISHED',
        'overlapping_path_covariance': 'NOT_CONTROLLED',
        'practical_original_error_budget': 'NOT_CERTIFIED',
        'actual_kg_residuals': 'NOT_EVALUATED',
        'theta_21_accuracy_rejection_v025': 'UNCHANGED',
        'time_uniform_bound': 'NOT_ESTABLISHED_POSITIVE_MAJORANT_DIVERGES',
        'infinite_history': 'NOT_CONTROLLED',
        'global_spatial_maximum': 'NOT_CONTROLLED',
        'degree_5_candidate': 'NOT_RUN',
        'proof_assistant': 'NOT_PERFORMED',
        'external_peer_review': 'NOT_PERFORMED',
    }
    for key, value in expected.items():
        require(status[key] == value, 'Scientific scope changed: ' + key)
    require(result['sources_verified'] == 6 and result['conditional_thinning_checks'] == 200,
            'Audit counts differ')
    require(result['chain_audit'] == {
        'orders_by_size': {'1':1,'2':2,'3':7,'4':40,'5':357},
        'chains':2164, 'multi_edge_chains':457}, 'Chain audit differs')
    require(len(result['rational_poisson_crosschecks']) == 10 and
            len(result['negative_controls']) == 8 and len(result['budgets']) == 2,
            'Crosscheck or budget counts differ')
    require(result['settings'] == [[120,32,16],[120,64,32],[160,64,32]] and
            len(result['runs']) == 6, 'Enclosure settings differ')
    require(result['constant_kernel_regressions'] == [
        {'theta':0,'constant_kernel_encloses_v028':True,'radial_shell_cone_checks':101},
        {'theta':21,'constant_kernel_encloses_v028':True,'radial_shell_cone_checks':101}],
        'Analytic regression counts differ')
    require(result['scope'] == {
        'q':'3/(16*pi)','rho_floor':'3/pi','T':'9/4','H':'4','delta':'1/100',
        'Q':'1','output_budget':'1/1000',
        'domain':'complete causal intervals; causal diamonds included'}, 'Physical scope changed')
    require(status['baseline_commit'] == result['base_commit'] == meta['base_commit'] ==
            read(PACKAGE / 'evidence/SOURCES.json')['commit'] ==
            '9a12332fa898408a71fb09128abdc467f84bf0b7', 'Scientific baseline changed')
    candidate = next(row for row in result['budgets'] if row['theta'] == 21)
    require(Fraction(candidate['B_joint']['upper_fraction']) < 34820 and
            Fraction(candidate['v028_to_v029_bound_ratio']['B_joint']['lower_fraction']) >
            Fraction(235,100), 'Displayed headline not supported by certified intervals')
    require(Fraction(candidate['eta_active']['lower_fraction']) >= Fraction('3.10e-6') and
            Fraction(candidate['eta_joint']['lower_fraction']) >= Fraction('2.87e-8'),
            'Displayed conditional input budgets not conservative')
    receipt = read(PACKAGE / 'REPLAY.json')
    require(receipt['result'] == 'PASS' and receipt['byte_identical_results'] and
            receipt['all_package_files_unchanged'] and receipt['assertions_disabled'],
            'Development replay receipt differs')
    require(receipt['results_sha256'] == digest(PACKAGE / 'results/RESULTS.json') and
            receipt['reproduce_sha256'] == digest(PACKAGE / 'reproduce.py'),
            'Replay receipt hashes differ')
    print('PASS: original ZIP, 18 files, 17 checksums, report copies and scoped HOLD status')


def replay():
    before = snapshot(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='cspp-v029-replay-') as tmp:
        copy = Path(tmp) / 'cspp_v029'
        shutil.copytree(PACKAGE, copy)
        subprocess.run([sys.executable, '-I', '-O', '-B', str(copy / 'reproduce.py'), '--check'],
                       check=True, cwd=tmp, timeout=900)
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
