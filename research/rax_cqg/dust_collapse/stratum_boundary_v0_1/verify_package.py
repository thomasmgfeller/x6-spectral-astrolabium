"""Offline integrity and scope checks for the stratum-boundary release."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCE_MAIN='4ed1a338f875172f8eb92798e8a8e9046a126f5f'
PLAN_SHA='723af1a22163c6f89426a59ccf999e82b2b44b74b4d15b9c842855ffaa56cf2d'
STEM='CST_DUST_Stratumwechsel_Randkopplung_Zustandsauswahl_v0_1'
FILES=('README.md','DERIVATION.md','LICENSE','NOTICE','provenance.json','plan.json','plan.sha256',
       'selection_contract.json','analyze.py','replay.py','build_report.py','verify_package.py','package.py',
       'inputs/matter_DERIVATION.md','inputs/variation_DERIVATION.md','inputs/coupling_contract.json',
       'inputs/coupling_DERIVATION.md','inputs/exact_core.py','results/block_and_graph.json',
       'results/boundary_identities.json','results/clock_and_action.json','results/verification.json',
       'results/replay.json',STEM+'.pdf')
SOURCES={'inputs/matter_DERIVATION.md':'b9584d6d5eebedac98b21f7a6d70ec411c068da5',
         'inputs/variation_DERIVATION.md':'575cf59e0813b59927792a3ee508ef9b0df00a6f',
         'inputs/coupling_contract.json':'02b4389fef476492052dabff4b5af1102befb7fc',
         'inputs/coupling_DERIVATION.md':'0053bd348455cf6e237692987b88fa08b86e1a1d',
         'inputs/exact_core.py':'d33b86c0c18c9103007508c2be09378c4e1174d8',
         'LICENSE':'d645695673349e3947e8e5ae42332d0ac3164cd7'}
GATES=dict.fromkeys(['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION'],'HOLD')
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha256(data):return hashlib.sha256(data).hexdigest()
def read(name):return json.loads((ROOT/name).read_text())
def verify():
    manifest=read('manifest.json')
    require(manifest['schema']=='cst-dust-stratum-boundary-manifest-v0.1','Manifest schema')
    require(manifest['source_main']==SOURCE_MAIN and set(manifest['files'])==set(FILES),'Release file set/source')
    for name in FILES:
        b=(ROOT/name).read_bytes()
        require(manifest['files'][name]=={'bytes':len(b),'sha256':sha256(b)},'Release bytes: '+name)
    require(sha256((ROOT/'plan.json').read_bytes())==PLAN_SHA,'Frozen plan')
    require((ROOT/'plan.sha256').read_text().split()[0]==PLAN_SHA,'Plan digest file')
    provenance=read('provenance.json')
    require(provenance['source_main']==SOURCE_MAIN and set(provenance['inputs'])==set(SOURCES),'Source set')
    for name,expected in SOURCES.items():
        b=(ROOT/name).read_bytes();g=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(g==expected==provenance['inputs'][name]['git_blob'],'Source identity: '+name)
        require('/blob/'+SOURCE_MAIN+'/' in provenance['inputs'][name]['source_url'],'Source URL')
    c=read('selection_contract.json');v=read('results/verification.json');p=read('plan.json')
    for obj in (c,v,p):
        require(obj['physical_gates']==GATES,'Physical gates remain HOLD')
        require(obj['paid_compute'] is False and obj['n5_production'] is False,'Cost/production limits')
    require(c['source_main']==SOURCE_MAIN and c['physical_detector_derived'] is False,'Contract source/scope')
    require(c['inherited_action_quantization']=='NOT_DERIVED','No inherited quantization claim')
    require(c['block_preserving_effects']['sharp_error']=='1/2','Sharp stratum bound')
    require(c['boundary_family']['physical_selection']=='NOT_DERIVED','No physical boundary selection')
    require(c['boundary_family']['old_bounded_V_budget_applicable'] is False,'Unbounded trace qualification')
    require(c['clock_completion']['density_only_effect_error']=='1','Full clock complement')
    require(c['action_potential_test']['constant_target_eigenstate_for_eta_nonzero'] is False,'Potential residual')
    require(v['status']=='PASS_CONDITIONAL_STRATUM_BOUNDARY_AUDIT' and v['plan_sha256']==PLAN_SHA,'Audit identity')
    require(v['physical_cst_coupling']=='NOT_DERIVED' and v['boundary_family']=='ADDITIONAL_DIAGNOSTIC_MODEL','Evidence class')
    require(v['continuum_convergence_certified'] is False,'Finite analogue scope')
    counts={'block_effect_controls':36,'boundary_graph_controls':72,'exact_cayley_unitarities':72,
            'finite_mixing_cases':54,'green_identity_controls':216,'flux_balances':72,'clock_controls':6,
            'action_point_controls':45,'action_potential_controls':9}
    require(all(v[k]==n for k,n in counts.items()),'Exact control counts')
    require(len(v['negative_controls'])==7 and all(x['status']=='REJECTED' for x in v['negative_controls']),'Negative controls')
    replay=read('results/replay.json');names={'block_and_graph.json','boundary_identities.json','clock_and_action.json','verification.json'}
    require(replay['status']=='PASS_BYTE_IDENTICAL' and replay['scientific_files']==4 and set(replay['sha256'])==names,'Replay scope')
    require(replay['external_replication'] is False and replay['n5_production'] is False,'Replay evidence limits')
    for name in names:require(replay['sha256'][name]==sha256((ROOT/'results'/name).read_bytes()),'Replay digest: '+name)
    require((ROOT/(STEM+'.pdf')).read_bytes().startswith(b'%PDF-'),'PDF signature')
    return {'status':'PASS_PACKAGE','manifest_files':len(FILES),'pinned_sources':len(SOURCES),
            'scientific_files':4,'physical_gates':'8 HOLD','source_main':SOURCE_MAIN}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
