"""Check package bytes, source identities, frozen plan and physical claim boundary."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCE_MAIN='0ee861d67f7d28e2c2762ef01e70f428796f1f53'
PLAN_SHA='e492ce4b3735ff4c1f346f2e2d3606e416c9509a6f9743477472064a18392c08'
PDF='CST_DUST_Uhrsymmetrie_Constraints_Atomgrenze_v0_1.pdf'
ALLOWED={'README.md','DERIVATION.md','NOTICE','LICENSE','plan.json','plan.sha256','provenance.json',
    'constraint_contract.json','analyze.py','replay.py','verify_package.py','package.py','build_report.py',PDF,
    'inputs/variation_DERIVATION.md','inputs/reference_DERIVATION.md','inputs/algebra_contract.json',
    'inputs/four_element_DERIVATION.md','inputs/exact_core.py','results/clock_symmetry.json',
    'results/constraint_domain.json','results/ward_boundary.json','results/density_atom_limit.json',
    'results/verification.json','results/replay.json'}
GATES={'MODEL','BOUNDARY','CURRENT','CORRESPONDENCE','TRAPPING','REGULARITY','EXTENSION','BOUNCE'}
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def verify():
    m=json.loads((ROOT/'manifest.json').read_text())
    require(set(m['files'])==ALLOWED,'Exact package allowlist')
    require(m['source_main']==SOURCE_MAIN,'Source Main')
    for name,info in m['files'].items():
        b=(ROOT/name).read_bytes();require(len(b)==info['bytes'] and sha(b)==info['sha256'],'Manifest '+name)
    require(sha((ROOT/'plan.json').read_bytes())==PLAN_SHA==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'provenance.json').read_text())
    require(prov['source_main']==SOURCE_MAIN and len(prov['inputs'])==6,'Six pinned sources')
    for name,info in prov['inputs'].items():
        require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Source blob '+name)
        require('/blob/'+SOURCE_MAIN+'/' in info['source_url'],'Pinned source URL')
    c=json.loads((ROOT/'constraint_contract.json').read_text());v=json.loads((ROOT/'results/verification.json').read_text())
    for doc in [c,v]:
        require(set(doc['physical_gates'])==GATES and set(doc['physical_gates'].values())=={'HOLD'},'Eight HOLD gates')
        for key in ['physical_constraint_quantization_derived','physical_sector_charge_derived','paid_compute','n5_production']:
            require(doc[key] is False,'Conditional claim '+key)
    require(c['strong_phase_limit']['fixed_finite_n_only'] is True,'Finite-n limit scope')
    require(c['strong_phase_limit']['physical_semiclassical_limit_derived'] is False,'No physical semiclassical promotion')
    require(c['new_density_integration_saving'] is False,'No duplicate saving claim')
    require(v['action_cases']==270 and v['ward_coefficient_controls']==117,'Declared controls')
    require(len(v['negative_controls'])==8 and all(x['status']=='REJECTED' for x in v['negative_controls']),'Negative controls')
    replay=json.loads((ROOT/'results/replay.json').read_text())
    require(replay['status']=='PASS_BYTE_IDENTICAL' and replay['scientific_files']==5,'Replay receipt')
    for name,s in replay['sha256'].items():require(sha((ROOT/'results'/name).read_bytes())==s,'Replay hash '+name)
    return {'status':'PASS_PACKAGE','files':len(ALLOWED),'pinned_sources':6,'physical_gates':'8 HOLD','source_main':SOURCE_MAIN}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
