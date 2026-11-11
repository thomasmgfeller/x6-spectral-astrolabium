#!/usr/bin/env python3
"""Create a deterministic package, excluding its own ZIP and digest manifest."""
from pathlib import Path
import hashlib
import io
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = 'CST_DUST_Ausgewaehlte_Hilfsbasis_Normierungspruefung_v0_1_Pruefpaket.zip'
MANIFEST = 'SHA256SUMS.json'

def files(root=ROOT):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and p.relative_to(root).as_posix() not in {ARCHIVE, MANIFEST}
                  and '__pycache__' not in p.parts and p.suffix != '.pyc')

def archive_bytes(root=ROOT):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as z:
        for p in sorted(files(root) + [root/MANIFEST]):
            info = zipfile.ZipInfo(p.relative_to(root).as_posix(), (2026, 11, 11, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())
    return stream.getvalue()

def main():
    entries = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in files()}
    manifest = {'algorithm': 'sha256', 'excluded': [MANIFEST, ARCHIVE], 'files': entries}
    (ROOT/MANIFEST).write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    data = archive_bytes()
    (ROOT/ARCHIVE).write_bytes(data)
    print(f'Packaged {len(entries)} source/evidence files plus manifest; ZIP sha256={hashlib.sha256(data).hexdigest()}')

if __name__ == '__main__':
    main()
