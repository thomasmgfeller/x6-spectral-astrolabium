"""Verify exact release bytes, frozen plan and claim boundary."""
from pathlib import Path,PurePosixPath
import hashlib,json
ROOT=Path(__file__).resolve().parent
PLAN='9366a5b204007fda0c38592a54d0b98e945696e63902511dc80719fc527d32e1'
BASE='c04214b9b6397abe9384bbcd728998b5c6b75173'
def require(ok,message):
    if not ok:raise RuntimeError(message)
def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    require(manifest['schema']=='cst-dust-operational-closure-manifest-v0.1','Manifest schema')
    for name,entry in manifest['files'].items():
        p=PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts,'Unsafe path')
        b=(ROOT/name).read_bytes()
        require(len(b)==entry['size'],'Size mismatch: '+name)
        require(hashlib.sha256(b).hexdigest()==entry['sha256'],'Hash mismatch: '+name)
    require(hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()==PLAN,'Frozen plan')
    require((ROOT/'plan.sha256').read_text().split()[0]==PLAN,'Plan sidecar')
    prov=json.loads((ROOT/'provenance.json').read_text())
    require(prov['source_main']==BASE,'Source revision')
    for name,entry in prov['inputs'].items():
        b=(ROOT/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==entry['git_blob'],'Source identity: '+name)
    contract=json.loads((ROOT/'operational_contract.json').read_text())
    result=json.loads((ROOT/'results/verification.json').read_text())
    require(contract['status']=='CONDITIONAL_REFERENCE_ONLY','Contract claim boundary')
    require(result['physical_selection_law']=='NOT_DERIVED','Physical selection claim')
    require(contract['physical_gates']==result['physical_gates'],'Consistent physical gates')
    require(len(contract['physical_gates'])==8 and set(contract['physical_gates'].values())=={'HOLD'},'Physical gates remain HOLD')
    require(contract['n5_production'] is False and result['n5_production_run'] is False,'No n=5 production')
    output={'status':'PASS_PACKAGE_INTEGRITY','hashed_files':len(manifest['files']),
            'pinned_sources':len(prov['inputs']),'frozen_plan':'UNCHANGED','physical_gates':'8 HOLD',
            'limitation':'Internal integrity, not proof of authorship or external replication.'}
    print(json.dumps(output,indent=2,sort_keys=True));return output
if __name__=='__main__':main()
