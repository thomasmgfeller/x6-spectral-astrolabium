#!/usr/bin/env python3
"""Create the review archive with deterministic paths and timestamps."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent
ARCHIVE='CST_DUST_Materieblock_Vorpruefung_v0_1_Pruefpaket.zip'

def main():
    paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                 and p.suffix not in ('.pyc','.zip') and p.name!='SHA256SUMS.json')
    manifest={'algorithm':'sha256','excluded':['SHA256SUMS.json',ARCHIVE],
              'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (ROOT/'SHA256SUMS.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for p in sorted(paths+[ROOT/'SHA256SUMS.json']):
            info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),(2026,11,11,0,0,0))
            info.create_system=3;info.external_attr=0o100644<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(f'{len(paths)} files plus manifest; {ROOT/ARCHIVE}')

if __name__=='__main__':main()
