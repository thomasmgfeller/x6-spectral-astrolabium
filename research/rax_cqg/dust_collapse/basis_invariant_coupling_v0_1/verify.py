"""Check hashes and replay numerical files without overwriting deliverables."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'SHA256SUMS.json').read_text())
    for name,digest in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Hash mismatch: '+name)
    with tempfile.TemporaryDirectory() as tmp:
        dest=Path(tmp)/'replay';shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('__pycache__','*.log'))
        subprocess.run([sys.executable,'-B','compute.py'],cwd=dest,check=True)
        subprocess.run([sys.executable,'-B','tests.py'],cwd=dest,check=True,stdout=subprocess.DEVNULL)
        # The independent-control log is checked by assertions. Byte replay of
        # block files (including rationalized trial vectors) uses the recorded
        # numerical environment; other BLAS builds can choose different vectors.
        files=('quadrature.json','uniform.json','cancellation_control.json')
        for name in files:
            if (dest/'results'/name).read_bytes()!=(ROOT/'results'/name).read_bytes():
                raise RuntimeError('Replay differs: '+name)
    print(json.dumps({'status':'PASS','hashes':len(manifest),'byte_identical_numerical_files':list(files),'control_groups':13}))

if __name__=='__main__':main()
