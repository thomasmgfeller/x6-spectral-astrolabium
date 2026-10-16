"""One-time, hash-bound transport of the already verified original archive."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

EXPECTED_TREE = '17af2f3b7f40ce6a67b6cc80e9a15ae9cd49210d'
SOURCE = '9aca530f2bd0b8ec68e7262013a5c8b3c8bce575'
MAIN = '1f2a1eb5102e9cd28eecb41c5603a5fd08e16501'
TARGET_BRANCH = 'research/proper-time-run-v1'

def git(*args, **kwargs):
    return subprocess.check_output(['git', *args], text=True, **kwargs).strip()

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

manifest = json.loads(Path('.publication-transfer/chunks.json').read_text())
archive = bytearray()
for part in manifest:
    data = Path(part['path']).read_bytes()
    require(len(data) == part['size'], 'chunk length: ' + part['path'])
    require(hashlib.sha256(data).hexdigest() == part['sha256'], 'chunk hash: ' + part['path'])
    archive.extend(data)
require(len(archive) == 40894957, 'archive length')
require(hashlib.sha256(archive).hexdigest() == '5c05a2ccd03058942371aed4692108da728e195f1c884b4605166c923844da5b', 'original archive hash')
path = Path('research/lorentz_proper_time/results/records.json.gz')
require(not path.exists(), 'do not replace an existing archive')
path.write_bytes(archive)
metadata = json.loads(Path('research/lorentz_proper_time/results/RESULTS.json').read_text())
for name, digest in metadata['files'].items():
    require(hashlib.sha256((path.parent / name).read_bytes()).hexdigest() == digest, 'result hash: ' + name)
for name, digest in metadata['sources'].items():
    data = Path(name).read_bytes()
    require(hashlib.sha256(data).hexdigest() == digest, 'source hash: ' + name)
    frozen = subprocess.check_output(['git', 'show', SOURCE + ':' + name])
    require(data == frozen, 'frozen source differs: ' + name)
git('rm', '-r', '--', '.publication-transfer', '.github/workflows/proper-time-transfer.yml')
git('add', '--', str(path))
tree = git('write-tree')
require(tree == EXPECTED_TREE, 'publication tree differs from checked local snapshot: ' + tree)
remote = git('ls-remote', '--heads', 'origin', 'refs/heads/' + TARGET_BRANCH)
require(remote.split()[0] == SOURCE, 'publication branch moved; inspect before retry')
git('config', 'user.name', 'Codex')
git('config', 'user.email', 'codex@openai.com')
commit = git('commit-tree', tree, '-p', SOURCE, '-p', MAIN, input='research: publish verified proper-time results and original data archive\n\nReassembled seven transport chunks; all original hashes and the complete\nvalidated publication tree match. Frozen computation and raw data unchanged.\n')
git('push', 'origin', commit + ':refs/heads/' + TARGET_BRANCH)
print(json.dumps({'status':'PASS_EXACT_ARCHIVE_PUBLICATION', 'archive_sha256':hashlib.sha256(archive).hexdigest(), 'tree':tree, 'commit':commit, 'branch':TARGET_BRANCH}, indent=2))
