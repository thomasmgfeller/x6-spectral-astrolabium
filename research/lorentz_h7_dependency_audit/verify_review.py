"""Check evidence bindings and review coverage, not semantic review judgments."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def require(ok,message):
    if not ok:raise ValueError(message)
def read(name):return json.loads((HERE/name).read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)


def main():
    review,scan,probes=map(read,['review.json','scan.json','probes.json'])
    base=review['base_commit'];require(base==scan['base_commit']==probes['base_commit'],'base revision mismatch')
    registry=json.loads(git('show',base+':MODULE_REGISTRY.json'))
    ids=[m['id'] for m in review['modules']]
    require(len(ids)==len(set(ids))==review['registered_modules']==len(registry['modules']),'module count')
    require(set(ids)=={m['id'] for m in registry['modules']},'module coverage')
    for m in review['modules']:
        e=m['evidence'];git('cat-file','-e',e['commit']+':'+e['path'])
        require(bool(m['reason']) and bool(m['method']),'empty review reason')
    result=json.loads(git('show',base+':research/lorentz_n7_complete/results/RESULTS.json'))
    require(review['hypothesis_status']==result['hypothesis_status']=='REFUTED_BY_COUNTEREXAMPLE','hypothesis mismatch')
    for name,expected in probes['sources'].items():require(hashlib.sha256(git('show',name)).hexdigest()==expected,'probe source mismatch '+name)
    require(len(probes['checks'])==6 and all(c['status']=='PASS' for c in probes['checks']),'probe status')
    require(len(probes['pairs'])==3 and all(p['H7_equal'] and not p['isomorphic'] for p in probes['pairs']),'witness results')
    require(scan['counts']['inventory_entries']==len(scan['inventory']),'inventory count')
    require(scan['counts']['files_with_matches']==len(scan['matches']),'retrieval count')
    inventory={r['location']:r for r in scan['inventory']}
    require(len(inventory)==len(scan['inventory']),'duplicate inventory location')
    for m in review['modules']:
        e=m['evidence'];suffix='@'+e['commit']+':'+e['path']
        require(any(k.endswith(suffix) for k in inventory),'review source not inventoried')
    print(json.dumps({'status':'PASS_EVIDENCE_BINDINGS_AND_39_MODULE_COVERAGE','scope':'Does not mechanically prove semantic dependency judgments'}))


if __name__=='__main__':main()
