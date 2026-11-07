"""Verify allowlist, contents, source identity, and conditional claim boundary."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
FROZEN_PLAN='ed1552e6f65e16aeb142190e02a095af357e40888cb17e77501de86ecc5a4b4d'
SOURCE_MAIN='c77cb607db23a043cd4965ee4efeb206eda22f8e'
PDF='CST_DUST_Observablenalgebra_Superselektion_Phasenreferenz_v0_1.pdf'
ALLOWED={'README.md','DERIVATION.md','NOTICE','LICENSE','plan.json','plan.sha256','provenance.json',
    'algebra_contract.json','analyze.py','replay.py','verify_package.py','package.py','build_report.py',PDF,
    'inputs/selection_contract.json','inputs/stratum_DERIVATION.md','inputs/variation_DERIVATION.md','inputs/exact_core.py',
    'results/algebra_and_conservation.json','results/finite_reference_effects.json',
    'results/reference_budgets.json','results/verification.json','results/replay.json'}
GATES={'MODEL','BOUNDARY','CURRENT','CORRESPONDENCE','TRAPPING','REGULARITY','EXTENSION','BOUNCE'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def verify():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    require(set(manifest['files'])==ALLOWED,'Exact package allowlist')
    require(manifest['source_main']==SOURCE_MAIN,'Main identity')
    for name,info in manifest['files'].items():
        b=(ROOT/name).read_bytes()
        require(len(b)==info['bytes'] and sha(b)==info['sha256'],'Manifest file '+name)
    require(sha((ROOT/'plan.json').read_bytes())==FROZEN_PLAN,'Pinned frozen plan')
    require((ROOT/'plan.sha256').read_text().split()[0]==FROZEN_PLAN,'Plan sidecar')
    provenance=json.loads((ROOT/'provenance.json').read_text())
    require(provenance['source_main']==SOURCE_MAIN and len(provenance['inputs'])==5,'Pinned sources')
    for name,info in provenance['inputs'].items():
        require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Source blob '+name)
        require('/blob/'+SOURCE_MAIN+'/' in info['source_url'],'Commit-pinned URL')
    contract=json.loads((ROOT/'algebra_contract.json').read_text())
    for key in ['physical_algebra_selected','physical_charge_derived','physical_reference_prepared',
                'physical_detector_derived','paid_compute','n5_production']:
        require(contract[key] is False,'Conditional contract '+key)
    require(contract['charge_is_dust_mass'] is False and contract['single_use_only'] is True,'Charge and reference scope')
    result=json.loads((ROOT/'results/verification.json').read_text())
    for doc in [contract,result]:
        require(set(doc['physical_gates'])==GATES and set(doc['physical_gates'].values())=={'HOLD'},'Eight HOLD gates')
    require(result['reference_effect_cases']==336 and result['born_and_twirl_controls']==2016,'Declared exact controls')
    require(len(result['negative_controls'])==8 and all(x['status']=='REJECTED' for x in result['negative_controls']),'Negative controls')
    replay=json.loads((ROOT/'results/replay.json').read_text())
    require(replay['status']=='PASS_BYTE_IDENTICAL' and replay['scientific_files']==4,'Replay receipt')
    for name,s in replay['sha256'].items():require(sha((ROOT/'results'/name).read_bytes())==s,'Replay hash '+name)
    return {'status':'PASS_PACKAGE','files':len(ALLOWED),'pinned_sources':5,'physical_gates':'8 HOLD','source_main':SOURCE_MAIN}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
