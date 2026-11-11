"""Intentional release builder, not an incoming-package integrity verifier."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json')
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    target=ROOT/'MANIFEST.sha256.json'
    target.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    out=ROOT.parent/'CST_DUST_Amplitudenexistenz_v0_1_Pruefpaket.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files+[target]):
            info=zipfile.ZipInfo(ROOT.name+'/'+str(p.relative_to(ROOT)),date_time=(2026,11,11,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes())
    print(out)
