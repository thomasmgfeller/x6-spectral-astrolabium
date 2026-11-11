from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
for name,expected in manifest.items():
    actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
    if actual!=expected: raise SystemExit('HASH MISMATCH: '+name)
data=(root/'inputs/gluing.py').read_bytes()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob!='d4c9ebdf640040a5fa1f00042d709c7b572aac5e':
    raise SystemExit('INHERITED GIT BLOB MISMATCH')
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)
    for script in ('analyze.py','run_checks.py'):
        subprocess.run([sys.executable,str(root/script),'--out',str(out)],check=True,cwd=root)
    for name in ('carriers.json','checks.json'):
        if (root/'results'/name).read_bytes()!=(out/name).read_bytes():
            raise SystemExit('REPRODUCTION MISMATCH: '+name)
print(f'{len(manifest)} hashes verified; inherited Git blob matched; two result files byte-identical')
