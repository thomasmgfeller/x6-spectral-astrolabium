"""Verify immutable v0.19 publication bytes and optional isolated replay."""
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
    package = HERE / 'cspp_v019'
    archive = HERE / 'CSPP_Quellnormen_Intervallgeometrie_v0_19.zip'
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'ZIP CRC')
        names = z.namelist()
        require(len(names) == len(set(names)) == meta['package_file_count'] == 25,
                'original package inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and p.parts[0] == package.name,
                    'safe package path')
            require((HERE / name).read_bytes() == z.read(name), 'original package bytes: ' + name)
        before = {name: sha(HERE / name) for name in names}
    manifest = (package / 'SHA256SUMS').read_text().splitlines()
    require(len(manifest) == meta['package_manifest_entries'] == 24, 'package manifest inventory')
    for line in manifest:
        digest, name = line.split('  ', 1)
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts, 'safe manifest path')
        require(sha(package / name) == digest, 'package SHA256: ' + name)
    require((package / 'report/Quellnormen_Intervallgeometrie_v0_19.pdf').read_bytes() ==
            (HERE / 'Quellnormen_Intervallgeometrie_v0_19.pdf').read_bytes(), 'same published PDF')
    checks = json.loads((package / 'results/CHECKS.json').read_text())
    for field, expected in {'status': 'PASS', 'precision_overlap_count': 960,
                            'source_identity_checks': 35, 'certified_quadrature_checks': 1,
                            'conditional_kernel_checks': 49, 'negative_controls': 3}.items():
        require(checks[field] == expected, 'validation scope: ' + field)
    for bits in (384, 512):
        result = json.loads((package / f'results/BOUNDS_{bits}.json').read_text())
        require(result['status'] == meta['scientific_status'], 'scientific HOLD')
        require(result['new_random_calls'] == 0, 'no new random data')
        require(len(result['windows']) == 2 and all(len(w['archives']) == 4 for w in result['windows']),
                'two windows and four archives')
    if replay:
        subprocess.run([sys.executable, '-B', str(package / 'reproduce.py')], check=True)
    for name, digest in before.items():
        require(sha(HERE / name) == digest, 'publication unchanged: ' + name)
    print('Publication integrity PASS: PDF, ZIP, 25 original files, 24 hashes; scientific HOLD preserved', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
