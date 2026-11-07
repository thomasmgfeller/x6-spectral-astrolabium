"""Check package bytes, source identities, frozen plan and physical claim boundary."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCE_MAIN='2b422800dcc0bd79643e1c946069acf8875a5291'
PLAN_SHA='682435483bb05733b6a60591bcd1d0d19e869e303f5c6ccddc4893647e698b27'
PDF='CST_DUST_Vergangenheitskragen_Stationaritaet_Randzustaende_v0_1.pdf'
ALLOWED={'README.md','DERIVATION.md','NOTICE','LICENSE','plan.json','plan.sha256','provenance.json',
    'collar_contract.json','analyze.py','replay.py','verify_package.py','package.py','build_report.py',PDF,
    'inputs/variation_DERIVATION.md','inputs/reference_DERIVATION.md','inputs/ward_contract.json',
    'inputs/ward_DERIVATION.md','inputs/exact_core.py','results/stationary_collar.json',
    'results/boundary_sensitivity.json','results/finite_width_states.json','results/return_amplitude_bounds.json',
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
    c=json.loads((ROOT/'collar_contract.json').read_text());v=json.loads((ROOT/'results/verification.json').read_text())
    for doc in [c,v]:
        require(set(doc['physical_gates'])==GATES and set(doc['physical_gates'].values())=={'HOLD'},'Eight HOLD gates')
        for key in ['physical_constraint_quantization_derived','physical_boundary_state_derived','paid_compute','n5_production']:
            require(doc[key] is False,'Conditional claim '+key)
    require(c['scope']['free_elements']==1 and c['scope']['extra_boundary_action'] is False,'Conditional single-free-element scope')
    require(c['stationary_witness']['isolated_saddle'] is False,'No isolated saddle')
    require(c['stationary_witness']['boundary_reactions_required'] is True,'Boundary reactions retained')
    require(c['finite_width_state']['physical_preparation_derived'] is False,'Kinematic packet only')
    require(c['finite_width_state']['sharp_limit_is_normalized_L2_state'] is False,'No normalized sharp L2 limit')
    require(c['return_contract']['physical_detector_derived'] is False,'Conditional return contract')
    require(c['return_contract']['full_geometric_or_semiclassical_limit_derived'] is False,'No physical limit promotion')
    require(c['return_contract']['iterated_limits_commute'] is False,'Boundary and phase limits do not commute')
    require(v['chain_cases']==216 and v['joint_stationary_cases']==135 and v['boundary_perturbation_cases']==2187,'Declared controls')
    require(v['packet_cases']==3 and v['return_amplitude_bounds']==12,'Packet controls')
    require(len(v['negative_controls'])==9 and all(x['status']=='REJECTED' for x in v['negative_controls']),'Negative controls')
    replay=json.loads((ROOT/'results/replay.json').read_text())
    require(replay['status']=='PASS_BYTE_IDENTICAL' and replay['scientific_files']==5,'Replay receipt')
    for name,s in replay['sha256'].items():require(sha((ROOT/'results'/name).read_bytes())==s,'Replay hash '+name)
    return {'status':'PASS_PACKAGE','files':len(ALLOWED),'pinned_sources':6,'physical_gates':'8 HOLD','source_main':SOURCE_MAIN}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
