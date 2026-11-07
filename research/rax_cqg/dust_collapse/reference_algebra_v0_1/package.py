"""Create manifest and a deterministic allowlisted ZIP; does not render the PDF."""
from pathlib import Path
import hashlib,json,zipfile
from verify_package import ALLOWED,SOURCE_MAIN,verify
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Observablenalgebra_Superselektion_Phasenreferenz_v0_1_Pruefpaket.zip'
files={}
for name in sorted(ALLOWED):
    b=(ROOT/name).read_bytes();files[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(ROOT/'manifest.json').write_text(json.dumps({'schema':'cst-dust-reference-package-v0.1','source_main':SOURCE_MAIN,'files':files},indent=2,sort_keys=True)+'\n')
verify()
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in sorted(ALLOWED|{'manifest.json'}):
        info=zipfile.ZipInfo(name,(2026,11,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        info.create_system=3;info.external_attr=0o100644<<16
        z.writestr(info,(ROOT/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
print(json.dumps({'file':str(OUT),'members':len(ALLOWED)+1,'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
