#!/usr/bin/env python3
"""Package the reproducible audit, excluding transient previews and run output."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
EXCLUDED={'preview','__pycache__'}
files=[p for p in ROOT.rglob('*') if p.is_file() and not (set(p.relative_to(ROOT).parts)&EXCLUDED)
       and p.name not in {'MANIFEST.sha256','run_stdout.json'} and p.suffix!='.zip']
files=sorted(files,key=lambda p:str(p.relative_to(ROOT)))
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files)
(ROOT/'MANIFEST.sha256').write_text(manifest)
files.append(ROOT/'MANIFEST.sha256')
dest=ROOT.parent/'CST_DUST_Eichstruktur_Randkonsistenz_v0_1_Pruefpaket.zip'
prefix='CST_DUST_Eichstruktur_Randkonsistenz_v0_1'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,prefix+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(dest) as z:
    if z.testzip() is not None:raise RuntimeError('ZIP integrity failed')
    for p in files:
        if z.read(prefix+'/'+p.relative_to(ROOT).as_posix())!=p.read_bytes():
            raise RuntimeError('ZIP member mismatch')
print(json.dumps({'zip':str(dest),'members':len(files),'bytes':dest.stat().st_size,
                  'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}))
