"""Create a deterministic archive after analysis, replay and PDF validation."""
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Alpha_Abhaengige_Normrestschranke_v0_1_Pruefpaket.zip'
files = sorted(p for p in ROOT.rglob('*') if p.is_file()
               and not any(x in p.parts for x in ('__pycache__','previews'))
               and p.suffix != '.pyc' and p.name != 'MANIFEST.sha256')
manifest = ROOT/'MANIFEST.sha256'
manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+
                          p.relative_to(ROOT).as_posix()+'\n' for p in files))
files.append(manifest)
archive = ROOT.parent/NAME
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):
        info = zipfile.ZipInfo(ROOT.name+'/'+p.relative_to(ROOT).as_posix(),(2026,11,7,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info,p.read_bytes())
print({'archive':str(archive),'members':len(files),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
