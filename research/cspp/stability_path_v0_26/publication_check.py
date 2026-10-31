"""Verify immutable v0.26 artifacts and replay exact checks in isolation."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'cspp_v026'

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
    with zipfile.ZipFile(ROOT / 'CSPP_Stabilitaet_Pfadkriterium_v0_26_Pruefpaket.zip') as z:
        members = [item for item in z.infolist() if not item.is_dir()]
        require(len(members) == len(files), 'Archive size differs')
        names = set()
        for item in members:
            path = PurePosixPath(item.filename)
            require(not path.is_absolute() and '..' not in path.parts, 'Unsafe archive path')
            require(path.parts[0] == 'cspp_v026', 'Wrong archive prefix')
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
    pdf = 'Stabilitaet_Pfadkriterium_v0_26.pdf'
    require((ROOT / pdf).read_bytes() == (PACKAGE / 'report' / pdf).read_bytes(),
            'Report copies differ')
    status = read(PACKAGE / 'STATUS.json')
    result = read(PACKAGE / 'results/RESULTS.json')
    require(meta['METHOD'] == meta['G1'] == status['method'] == status['g1'] == 'HOLD',
            'Scientific gates changed')
    require(meta['new_random_clouds'] == 0 and status['new_ensemble'] == 'NOT_RUN',
            'New random clouds claimed')
    require(status['github_publication'] == 'NOT_PERFORMED_IN_THIS_STEP',
            'Historical publication flag changed')
    for key, expected in {
        'all_realization_linf_bound':'EXCLUDED_FOR_DEFINED_NONTRIVIAL_INTERVAL_KERNEL_CLASS',
        'physical_gcb_uniform_positive_bound':'OPEN',
        'typical_realization_instability':'NOT_ESTABLISHED',
        'kg_detector_error':'NOT_EVALUATED',
        'degree_5_candidate':'NOT_RUN',
        'external_peer_review':'NOT_PERFORMED',
    }.items():
        require(status[key] == expected, 'Scientific scope changed: ' + key)
    require(result['status'] == 'PASS', 'Recorded checks failed')
    require(result['checks'] == {
        'source_hashes':3, 'exact_fan_cases':144, 'exact_cell_cases':30,
        'negative_controls':4, 'overlapping_rational_alpha_intervals':3},
        'Recorded check counts differ')
    require(result['base_commit'] == meta['base_commit'] ==
            'c156dab194bbe144101382b813112eee339e0e7a', 'Scientific baseline changed')
    print('PASS: original ZIP, 15 files, 14 checksums, report copies and scoped HOLD status')

def replay():
    before = snapshot(PACKAGE)
    with tempfile.TemporaryDirectory(prefix='cspp-v026-replay-') as tmp:
        copy = Path(tmp) / 'cspp_v026'
        shutil.copytree(PACKAGE, copy)
        # -I ignores PYTHONOPTIMIZE; no -O is propagated from this wrapper.
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        subprocess.run([sys.executable, '-I', '-B', str(copy / 'reproduce.py'), '--check'],
                       check=True, env=env, cwd=tmp, timeout=120)
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
