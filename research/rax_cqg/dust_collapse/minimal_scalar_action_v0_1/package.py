"""Build a deterministic archive of this explicit candidate (not a verifier)."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
PDF = 'CST_DUST_Gemeinsamer_Skalarwirkungsansatz_v0_1.pdf'
ARCHIVE = 'CST_DUST_Gemeinsamer_Skalarwirkungsansatz_v0_1_Pruefpaket.zip'
MANIFEST = 'MANIFEST.sha256.json'
GENERATED = {'.aux', '.log', '.out', '.toc', '.pyc', '.zip'}


def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts
                  and not any(part.startswith('.') for part in p.relative_to(ROOT).parts)
                  and p.suffix not in GENERATED
                  and p.name not in {MANIFEST, 'report.pdf'})


def main():
    if not (ROOT/PDF).is_file():
        raise SystemExit('Render, inspect and copy the report PDF before packaging.')
    entries = files()
    record = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in entries}
    (ROOT/MANIFEST).write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    with zipfile.ZipFile(ROOT/ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as z:
        for p in sorted(entries+[ROOT/MANIFEST]):
            name = 'minimal_scalar_action_v0_1/'+str(p.relative_to(ROOT))
            info = zipfile.ZipInfo(name, date_time=(2026,11,11,0,0,0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes(), compresslevel=9)
    print(json.dumps({'archive':str(ROOT/ARCHIVE), 'files':len(record)+1,
                      'sha256':hashlib.sha256((ROOT/ARCHIVE).read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
