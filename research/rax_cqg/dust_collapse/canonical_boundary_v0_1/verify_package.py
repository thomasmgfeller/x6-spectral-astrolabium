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
c=json.loads((root/'canonical_contract.json').read_text())
demand(all(v=='HOLD' for v in c['physical_gates'].values()),'Physical gate changed without evidence')
for k in ('physical_preparation_derived','physical_inner_product_selected','physical_constraint_algebra_derived','physical_hamiltonian_derived','physical_exterior_derived','bounce_derived','finite_density_integral_is_delta_projection','null_atom_restricted_to_moment_surface'):
    demand(c['claims'][k] is False,'Unsupported claim: '+k)
demand(c['paid_compute'] is False and c['n5_production'] is False,'Scope drift')
print(json.dumps({'integrity':'PASS','manifest_files':len(manifest['files']),'inherited_source_blobs':5,'physical_gates':'HOLD'}))
