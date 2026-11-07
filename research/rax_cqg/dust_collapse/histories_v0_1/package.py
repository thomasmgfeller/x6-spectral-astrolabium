#!/usr/bin/env python3
"""Create a deterministic source/report/results package with complete hashes."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NAME='CST_DUST_Positive_Historien_Schnittkonsistenz_v0_1'
def main():
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and
      not any(x in {'previews','__pycache__'} for x in p.relative_to(ROOT).parts)
      and p.name!='MANIFEST.sha256')
    (ROOT/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
    files.append(ROOT/'MANIFEST.sha256')
    dest=ROOT.parent/(NAME+'_Pruefpaket.zip')
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files):
            info=zipfile.ZipInfo(NAME+'/'+p.relative_to(ROOT).as_posix(),date_time=(2026,11,7,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(dest) as z:
        if z.testzip() is not None:raise RuntimeError('Archive CRC')
        for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
            digest,rel=line.split(maxsplit=1)
            if hashlib.sha256(z.read(NAME+'/'+rel)).hexdigest()!=digest:raise RuntimeError(rel)
    print(json.dumps({'archive':str(dest),'members':len(files),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
