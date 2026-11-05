"""Verify package-file integrity, not physical measurements or calibration."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'SHA256.json').read_text())
for name,expected in manifest['files'].items():
 p=(ROOT/name).resolve()
 if not p.is_relative_to(ROOT) or not p.is_file():raise SystemExit('Missing/unsafe file: '+name)
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 if h.hexdigest()!=expected:raise SystemExit('Digest mismatch: '+name)
print(f"PASS: {len(manifest['files'])} file hashes; physical qualification NOT_RUN")
