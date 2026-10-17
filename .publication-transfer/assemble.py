"""Hash-bound one-time import of checked proper-time commits; never writes main."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

HEAD = 'd64f6e184ce1ed1a4c67eb27d77b7a0ac2dbd087'
TREE = '1707fb9278f49b740708880d0dbc6ab61dc087c4'
BASE = '3194841d8db19d4ca3b4eacf5c41fdf21cdf7a99'
TARGET = 'publication/proper-time-complete-20261017'
BUNDLE_SHA256 = '49c1ea9cb5a824a37db7ed63f9147862621241a7603b76ee9b8049a709efac6e'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()

manifest = json.loads(Path('.publication-transfer/manifest.json').read_text())
bundle = bytearray()
for part in manifest['parts']:
    data = Path(part['path']).read_bytes()
    require(len(data) == part['size'], 'chunk size')
    require(hashlib.sha256(data).hexdigest() == part['sha256'], 'chunk sha256')
    bundle.extend(data)
require(len(bundle) == 2057964 == manifest['size'], 'bundle size')
require(hashlib.sha256(bundle).hexdigest() == BUNDLE_SHA256 == manifest['sha256'], 'bundle sha256')
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp)/'publication.bundle'
    path.write_bytes(bundle)
    git('bundle', 'verify', str(path))
    require(git('bundle', 'list-heads', str(path)) == HEAD+' refs/heads/'+TARGET, 'bundle head')
    git('fetch', str(path), 'refs/heads/'+TARGET)
require(git('rev-parse', HEAD+'^{tree}') == TREE, 'publication tree')
git('merge-base', '--is-ancestor', BASE, HEAD)
paths = git('ls-tree', '-r', '--name-only', HEAD).splitlines()
require(not any(p.startswith('.publication-transfer/') or p == '.github/workflows/proper-time-transport.yml' for p in paths), 'transport leaked into publication')
remote = git('ls-remote', '--heads', 'origin', 'refs/heads/'+TARGET)
require(not remote or remote.split()[0] == HEAD, 'target branch changed; inspect before retry')
git('push', 'origin', HEAD+':refs/heads/'+TARGET)
print(json.dumps(dict(status='PASS_EXACT_HISTORY_PUBLICATION', commit=HEAD, tree=TREE, bundle_sha256=BUNDLE_SHA256, branch=TARGET), indent=2))
