"""Verify saved bytes, then replay the deterministic analytic checks."""
from pathlib import Path
import hashlib, subprocess, sys

root=Path(__file__).resolve().parent
entries=(root/'SHA256SUMS').read_text().splitlines()
for line in entries:
    digest,name=line.split('  ',1)
    p=root/name
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
result=root/'results/ANALYTIC_CHECKS.json'
old=result.read_bytes()
subprocess.run([sys.executable,str(root/'analytic.py')],check=True)
assert result.read_bytes()==old,'analytic replay differs'
print(f'PASS: {len(entries)} file hashes; byte-identical analytic replay.')
