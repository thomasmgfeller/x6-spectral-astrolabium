#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
def demand(ok,msg):
    if not ok: raise ValueError(msg)
manifest=json.loads((root/'manifest.json').read_text())
for name,digest in manifest['files'].items():
    demand(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'Integrity: '+name)
expected=(root/'plan.sha256').read_text().split()[0]
demand(hashlib.sha256((root/'plan.json').read_bytes()).hexdigest()==expected,'Plan hash')
for row in json.loads((root/'provenance.json').read_text())['files']:
    b=(root/row['path']).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    demand(actual==row['git_blob_sha1'],'Source identity: '+row['path'])
c=json.loads((root/'stationarity_contract.json').read_text())
demand(len(c['physical_gates'])==8 and all(v=='HOLD' for v in c['physical_gates'].values()),'Physical gate changed without evidence')
for k,v in c['claims'].items():
    demand(v is False,'Unsupported claim: '+k)
demand(c['paid_compute'] is False and c['n5_production'] is False,'Scope drift')
demand(c['mathematical_results']['full_stationarity_excluded'] is True,'Missing certified finite-class exclusion')
demand(c['mathematical_results']['bound_claimed_sharp'] is False,'Unsupported sharpness claim')
actual_files={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.suffix not in ('.zip','.pyc') and '__pycache__' not in p.parts and p.name!='manifest.json'}
demand(actual_files==set(manifest['files']),'Manifest file-set mismatch')
print(json.dumps({'integrity':'PASS','manifest_files':len(manifest['files']),'inherited_source_blobs':4,'physical_gates':'HOLD'}))
