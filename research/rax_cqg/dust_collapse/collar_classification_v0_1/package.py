#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parent
files=sorted(p for p in root.rglob('*') if p.is_file() and p.suffix not in ('.zip','.pyc') and '__pycache__' not in p.parts and p.name!='manifest.json')
m={'algorithm':'sha256','files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
files.append(root/'manifest.json')
path=root/'CST_DUST_Randdaten_Klassifikation_Stoerungsgrenzen_v0_1_Pruefpaket.zip'
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):
        info=zipfile.ZipInfo(str(p.relative_to(root)),(2026,11,8,12,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
        z.writestr(info,p.read_bytes(),compresslevel=9)
print(json.dumps({'zip':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'files':len(files)}))
