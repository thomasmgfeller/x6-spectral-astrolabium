"""Package the publication with deterministic paths and timestamps."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = 'CST_DUST_Randvertrag_Gaussprojektion_v0_1_Pruefpaket.zip'


def main():
    paths = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and '__pycache__' not in p.parts
                   and p.suffix not in ('.pyc', '.zip')
                   and p.name != 'SHA256SUMS.json')
    manifest = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in paths}
    (ROOT / 'SHA256SUMS.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    with zipfile.ZipFile(ROOT / ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for p in sorted(paths + [ROOT / 'SHA256SUMS.json']):
            entry = zipfile.ZipInfo(ROOT.name + '/' + p.relative_to(ROOT).as_posix(),
                                    (2026, 11, 11, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, p.read_bytes(), compresslevel=9)
    print(f'{len(paths)} files plus manifest packaged; physical gates HOLD')


if __name__ == '__main__':
    main()
