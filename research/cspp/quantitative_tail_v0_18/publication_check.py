"""Check immutable publication bytes and replay scientific results in isolation."""
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
    for name, asset in meta.get('supplemental_assets', {}).items():
        data = (HERE / name).read_bytes()
        require(sha(HERE / name) == asset['sha256'], 'supplement hash: ' + name)
        require(data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) > 1000, 'nonempty PNG supplement')
    archive = HERE / 'CSPP_Quantitative_Restmajoranten_v0_18.zip'
    package = HERE / 'quantitative_tail_v0_18'
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'ZIP CRC')
        names = z.namelist()
        require(len(names) == len(set(names)) == 22, 'original package inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and p.parts[0] == package.name, 'safe package path')
            require((HERE / name).read_bytes() == z.read(name), 'original bytes: ' + name)
        before = {name: sha(HERE / name) for name in names}
    lines = (package / 'SHA256SUMS').read_text().splitlines()
    require(len(lines) == 21, 'original manifest inventory')
    for line in lines:
        digest, name = line.split('  ', 1)
        require(sha(package / name) == digest, 'original manifest: ' + name)
    require((package / 'report/Quantitative_Restmajoranten_v0_18.pdf').read_bytes() ==
            (HERE / 'Quantitative_Restmajoranten_v0_18.pdf').read_bytes(), 'same report at publication root')
    check = json.loads((package / 'results/CHECKS.json').read_text())
    require(check['status'] == 'PASS' and check['precision_overlaps'] == 857 and check['negative_controls'] == 3,
            'declared validation scope')
    for bits in (128, 192):
        result = json.loads((package / f'results/BOUNDS_{bits}.json').read_text())
        require(result['status'] == {'METHOD': 'HOLD', 'G1': 'HOLD', 'fresh_confirmation': 'NOT_RUN',
                                    'per_realization_accuracy': 'NOT_CERTIFIED'}, 'scientific HOLD')
        require(result['new_random_calls'] == 0, 'no new random data')
    if replay:
        subprocess.run([sys.executable, '-B', str(package / 'reproduce.py')], check=True)
    for name, digest in before.items():
        require(sha(HERE / name) == digest, 'published bytes unchanged: ' + name)
    print('Publication integrity PASS: PDF, ZIP, 22 original files, 21 manifest entries; scientific HOLD preserved', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
