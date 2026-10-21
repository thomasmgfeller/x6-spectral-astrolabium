"""SPDX-License-Identifier: Apache-2.0"""
import json
import subprocess
import numpy as np
from ca_common import HERE,ROOT,cfg,source_check,history,model,load_results,sha,encode,compare,close,old,order_check
from ca_model import predict,evaluate,intervals
from ca_analyze import analyze
from ca_controls import check

def gitfile(commit,path):return subprocess.check_output(['git','show',commit+':'+str(path.relative_to(ROOT))],cwd=ROOT)
def main():
    f=source_check();c=cfg();source=f['commit']
    subprocess.run(['git','merge-base','--is-ancestor',source,'HEAD'],cwd=ROOT,check=True)
    assert subprocess.check_output(['git','rev-parse',source+'^'],cwd=ROOT,text=True).strip()==c['parent_commit']
    for name,h in f['files'].items():assert sha(gitfile(source,ROOT/name))==h,name
    assert json.loads(gitfile(source,HERE/'source_pins.json'))['files']==f['files']
    executions,rows=load_results();archived=history();assert [r['index'] for r in rows]==list(range(c['historical_attempts']))
    for e in executions:
        assert e['status']=='COMPLETE' and e['source_commit']==source
        assert e['seconds']<=c['wall_seconds_per_worker'] and e['peak_mib']<=c['memory_mib_per_worker']
        assert e['assigned_indices']==list(range(e['worker'],len(rows),c['workers']))
        assert [int(r['file'][6:9]) for r in e['records']]==e['assigned_indices']
    maximum=0.;solves=truths=hashes=0;_,oc,_,_=old.ec.config()
    for row,previous in zip(rows,archived):
        assert (row['historical_phase'],row['historical_index'],row['seed'])==(previous['phase'],previous['index'],previous['seed'])
        p=row['prediction'];assert sha(encode(p).encode())==row['prediction_seal']
        cloud=previous['cloud'];fresh=predict(cloud['intrinsic'],cloud['observed_order'],model())
        assert fresh['status']==p['status']==previous['prediction']['status']
        if p['status']=='COMPLETE':
            assert set(p['variants'])==set(c['candidates'])
            for n in c['candidates']:
                a=fresh['variants'][n];b=p['variants'][n];assert a['status']==b['status']
                aq=intervals(np.vstack((np.zeros(3),a['features'])));bq=intervals(np.vstack((np.zeros(3),b['features'])))
                np.testing.assert_allclose(aq,bq,atol=c['optimizer_atol'],rtol=c['optimizer_rtol'])
                maximum=max(maximum,float(np.max(abs(aq-bq))));solves+=1
                close(a['covariance_condition'],b['covariance_condition'])
                assert order_check(np.vstack((np.zeros(3),b['features'])),cloud['observed_order'])['passed']
            z=old.ec.coordinates_only(old.cfg()['rho'],row['seed'],oc);s=cloud['selection']['selected']
            close(z[[s['root']]+s['support']]-z[s['root']],previous['true_support_points']);truths+=1
            hashes+=old.ec.digest(z)==cloud['coordinates_sha256']
        compare(evaluate(previous,p,model()),row['evaluation'])
    summary=analyze(rows);compare(summary,json.loads((HERE/'results/summary.json').read_text()))
    print(json.dumps(dict(verification='PASS_NUMERICAL_REPLAY',records=len(rows),truth_replayed=truths,
        coordinate_byte_hash_matches=int(hashes),optimizations_replayed=solves,maximum_interval_reoptimization_difference=maximum,
        frozen_files=len(f['files']),controls=check(),decision=summary['decision'],new_simulations=0,
        limits='Archived observations are development only; fresh numerical replay is not an independent statistical confirmation.')))
if __name__=='__main__':main()
