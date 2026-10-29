"""Check immutable v0.20 publication bytes, scope and optional full replay."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(replay=False):
    meta = json.loads((HERE / 'PUBLICATION.json').read_text())
    for name, digest in meta['artifact_sha256'].items():
        require(sha(HERE / name) == digest, 'artifact hash: ' + name)
    package = HERE / 'cspp_v020'
    archive = HERE / 'CSPP_Lokale_aeussere_History_v0_20_Pruefpaket.zip'
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'ZIP CRC')
        names = z.namelist()
        require(len(names) == len(set(names)) == meta['package_file_count'] == 53,
                'original package inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and p.parts[0] == package.name,
                    'safe package path')
            require((HERE / name).read_bytes() == z.read(name), 'original package bytes: ' + name)
        before = {name: sha(HERE / name) for name in names}
    manifest = (package / 'SHA256SUMS').read_text().splitlines()
    require(len(manifest) == meta['package_manifest_entries'] == 52, 'manifest inventory')
    for line in manifest:
        digest, name = line.split('  ', 1)
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts, 'safe manifest path')
        require(sha(package / name) == digest, 'package SHA256: ' + name)
    require((package / 'report/Lokale_aeussere_History_v0_20.pdf').read_bytes() ==
            (HERE / 'Lokale_aeussere_History_v0_20.pdf').read_bytes(), 'same published PDF')
    checks = json.loads((package / 'results/CHECKS.json').read_text())
    require(checks['status'] == 'PASS', 'scientific controls passed')
    for field, expected in {'physical_ball_overlaps': 6810, 'integer_count_checks': 1698,
                            'negative_controls': 3, 'table_point_checks': 243,
                            'source_blobs': 6, 'majorant_stability_checks': 64}.items():
        require(checks['counters'][field] == expected, 'validation scope: ' + field)
    require(checks['internal_run_checks'] == {'cap_quadratures': 55, 'direct_poisson_sums': 63},
            'independent numerical controls')
    receipt = json.loads((package / 'REPLAY.json').read_text())
    require(receipt == {'isolated_replay': 'PASS', 'byte_identical_result_files': 21}, 'replay receipt')
    for bits in (128, 192):
        result = json.loads((package / f'results/LOCAL_{bits}.json').read_text())
        require(result['status'] == meta['scientific_status'], 'scientific HOLD')
        require(result['new_random_calls'] == 0, 'no new random data')
        require(len(result['roots']) == 8 and len(result['archives']) == 4, 'fixed probe and archive inventory')
        require(sum(len(r['probes']) for r in result['archives']) == 1698, 'fixed causal probes')
        for row in result['archives']:
            require([l['grid'] for l in row['levels']] == [2, 4], 'declared cell partitions')
            require(all(len(l['windows']) == 2 for l in row['levels']), 'both complete detector windows')
    if replay:
        subprocess.run([sys.executable, '-B', str(package / 'reproduce.py')], check=True)
    for name, digest in before.items():
        require(sha(HERE / name) == digest, 'publication unchanged: ' + name)
    print('Publication integrity PASS: PDF, ZIP, 53 original files, 52 hashes; scientific HOLD preserved', flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
