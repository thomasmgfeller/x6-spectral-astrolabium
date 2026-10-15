"""Verify preserved original GitHub artifact bytes and their full inner inventory."""
import hashlib
import json
from pathlib import Path,PurePosixPath
import stat
import zipfile

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'docs/agent-archive/2026-10-15'

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)

def verify():
    d=json.loads((BASE/'ARCHIVE.json').read_text());checked=[]
    for a in d['artifacts']:
        p=BASE/a['name'];require(not p.is_symlink(),'linked archive')
        data=p.read_bytes();require(len(data)==a['original_bytes'] and sha(data)==a['sha256'] and a['github_digest']=='sha256:'+sha(data),'original GitHub archive mismatch')
        with zipfile.ZipFile(p) as z:
            names=z.namelist();require(len(names)==len(set(names)),'duplicate ZIP member')
            require(set(names)==set(a['internal_files_sha256'])|{'SHA256.json'},'incomplete ZIP')
            for info in z.infolist():
                n=PurePosixPath(info.filename)
                require(not n.is_absolute() and '..' not in n.parts and not stat.S_ISLNK(info.external_attr>>16) and info.file_size<=8_000_000,'unsafe ZIP member')
            inventory=json.loads(z.read('SHA256.json'))
            hashes=inventory.get('files',{k:v for k,v in inventory.items() if type(v)is str and len(v)==64})
            require(hashes==a['internal_files_sha256'],'inner inventory changed')
            for n,h in hashes.items():require(sha(z.read(n))==h,'inner file mismatch: '+n)
            report=z.read('report.json');require(report==(BASE/(p.stem+'-report.json')).read_bytes(),'report projection mismatch')
            require(json.loads(report)['status']==a['report_status'],'status mismatch')
        checked.append({'artifact_id':a['artifact_id'],'sha256':sha(data),'files':len(names),'status':'BYTE_AND_INVENTORY_PASS'})
    require(len(checked)==3,'selected archive set')
    return {'status':'PASS_AGENT_PRESERVATION','artifacts':checked,'scientific_reanalysis':'NOT_PERFORMED','external_review':'NOT_PERFORMED'}

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
