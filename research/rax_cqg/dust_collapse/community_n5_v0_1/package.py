"""Build the source manifest and deterministic self-contained community ZIP."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
FILES=['README.md','MATHEMATICS.md','LICENSE','NOTICE','prepare.py','worker.py',
       'controls.py','kernel.cpp','plan.json','controls_result.json','environment.json',
       'provenance.json','package.py']+[f'inputs/{name}.py' for name in
       ['geometry','gauss','intervals_fp','memory','intervals','bounds']]

def build():
    result=json.loads((ROOT/'controls_result.json').read_text())
    if result['status']!='PASS_CONTROLS_ONLY' or result['production_n5_field_integrals_executed']:
        raise RuntimeError('Require completed short controls and no production execution')
    for name,info in json.loads((ROOT/'provenance.json').read_text())['unchanged'].items():
        data=(ROOT/name).read_bytes()
        sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if sha!=info['git_blob']:raise RuntimeError('Inherited source identity: '+name)
    manifest={'schema':'cst-dust-n5-community-manifest-v1',
              'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(FILES)}}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    archive=ROOT/'CST_DUST_N5_Community_v0_1.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(FILES+['manifest.json']):
            info=zipfile.ZipInfo(name,date_time=(2026,11,7,12,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,(ROOT/name).read_bytes(),compresslevel=9)
    data=archive.read_bytes()
    print(json.dumps({'archive':archive.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                      'members':len(FILES)+1},indent=2))

if __name__=='__main__':build()
