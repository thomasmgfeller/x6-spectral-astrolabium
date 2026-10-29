"""Create a checksum-complete review package; omit transient Python files."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'CSPP_Skalarer_Kandidat_v0_25_Pruefpaket.zip'
def eligible(p):
    return p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS' and p.suffix!='.pyc'
def main():
    meta={'version':'0.25','base_commit':'4c755221b76364c02beca5e7a40c0f8d50931375',
      'entrypoint':'python3 reproduce.py','scientific_result':'REJECT_FOR_CONTINUATION_TWO_SCALE_SCREEN',
      'METHOD':'HOLD','G1':'HOLD','new_random_clouds':0,
      'publication':'not performed in this step','integrity_file':'SHA256SUMS',
      'report':'report/Skalarer_Kandidat_Zweiskalenpruefung_v0_25.pdf'}
    (ROOT/'PACKAGE.json').write_text(json.dumps(meta,indent=2)+'\n')
    files=sorted(p for p in ROOT.rglob('*') if eligible(p))
    sums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n' for p in files)
    (ROOT/'SHA256SUMS').write_text(sums)
    files.append(ROOT/'SHA256SUMS')
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,str(Path('cspp_v025')/p.relative_to(ROOT)))
    with zipfile.ZipFile(OUT) as z:
        if z.testzip() is not None:raise RuntimeError('ZIP integrity failed')
        for line in sums.splitlines():
            sha,path=line.split('  ',1)
            if hashlib.sha256(z.read('cspp_v025/'+path)).hexdigest()!=sha:raise RuntimeError('ZIP hash failed')
    print(json.dumps({'path':str(OUT),'files':len(files),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'bytes':OUT.stat().st_size},indent=2))
if __name__=='__main__':main()
