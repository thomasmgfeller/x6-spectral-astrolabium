"""Deterministic distributable; numeric evidence never rewritten here."""
import hashlib,json,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def eligible(p):
    return p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.log','.pyc'] and p.name!='SHA256SUMS'
def package():
    files=sorted(p for p in HERE.rglob('*') if eligible(p))
    entries=[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files if p.name!='PACKAGE.json']
    (HERE/'PACKAGE.json').write_text(json.dumps({'schema':'cspp.finite-exterior-package/0.22','file_count_excluding_manifest_and_package_metadata':len(entries),'files':entries},indent=2,sort_keys=True)+'\n')
    files=sorted(p for p in HERE.rglob('*') if eligible(p))
    (HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(HERE))+'\n' for p in files))
    files.append(HERE/'SHA256SUMS');out=HERE.parent/'output/CSPP_Endliche_Aussenhistory_v0_22_Pruefpaket.zip';out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files):
            info=zipfile.ZipInfo('cspp_v022/'+str(p.relative_to(HERE)),date_time=(2026,10,29,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for p in files:assert z.read('cspp_v022/'+str(p.relative_to(HERE)))==p.read_bytes()
    print(json.dumps({'path':str(out),'files':len(files),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':package()
