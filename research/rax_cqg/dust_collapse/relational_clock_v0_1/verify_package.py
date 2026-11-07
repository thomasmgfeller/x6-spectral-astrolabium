"""Verify every declared package member against its SHA-256 checksum."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
count = 0
for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
    digest,name = line.split('  ',1)
    path = (ROOT/name).resolve()
    if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise RuntimeError('Package integrity failure: '+name)
    count += 1
print(f'PASS: {count} SHA-256 checksums')
