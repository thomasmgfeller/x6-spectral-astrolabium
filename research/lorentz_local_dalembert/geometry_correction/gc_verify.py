"""SPDX-License-Identifier: Apache-2.0"""
import json
import subprocess
import numpy as np
from gc_common import HERE,BASE,ROOT,cfg,model,ec,sha,encode,source_check,load_phase,close,compare,order_check
from gc_model import predict,evaluate,intervals
from gc_calibrate import calibrate
from gc_analyze import analyze
from gc_controls import check

def gitfile(commit,path):return subprocess.check_output(['git','show',commit+':'+str(path.relative_to(ROOT))],cwd=ROOT)
def main():
    frozen=source_check();source=frozen['commit'];c=cfg()
    subprocess.run(['git','merge-base','--is-ancestor',source,'HEAD'],cwd=ROOT,check=True)
    for name,h in frozen['files'].items():assert sha(gitfile(source,ROOT/name))==h,name
    schedule=json.loads((HERE/'seed_schedule.json').read_text())
    old=json.loads((BASE/'geometry_groups/seed_schedule.json').read_text())
    excluded=set(old['excluded_prior_seeds'])|{r['geometry_seed'] for phase in ['calibration','test'] for r in old[phase]}
    assert excluded==set(schedule['excluded_prior_seeds']) and schedule['eligible_population']==2**32-len(excluded)
    phases={};hash_matches=0;truth_replayed=0;max_difference=0.;optimizations=0
    _,oc,_,_=ec.config()
    for phase in ['calibration','test']:
        executions,rows=load_phase(phase)
        assert len(rows)==c['clouds_per_phase']
        assert [(r['index'],r['seed']) for r in rows]==[(r['index'],r['geometry_seed']) for r in schedule[phase]]
        assert all(r['seed'] not in excluded for r in rows)
        for e in executions:
            assert e['status']=='COMPLETE' and e['source_commit']==source
            assert e['seconds']<=c['wall_seconds_per_worker'] and e['peak_mib']<=c['memory_mib_per_worker']
            assert e['assigned_indices']==list(range(e['worker'],c['clouds_per_phase'],c['workers']))
            if phase=='calibration':assert e['execution_commit']==source
            else:
                subprocess.run(['git','merge-base','--is-ancestor',e['execution_commit'],'HEAD'],cwd=ROOT,check=True)
                for filename in ['frozen_calibration.json','source_freeze.json']:
                    assert gitfile(e['execution_commit'],HERE/filename)==(HERE/filename).read_bytes()
        for r in rows:
            cloud=r['cloud'];stored=r['prediction'];p=predict(cloud['intrinsic'],cloud['observed_order'],model())
            assert sha(encode(stored).encode())==r['prediction_seal'];assert p['status']==stored['status']
            if p['status']=='COMPLETE':
                for v in c['variants']:
                    fresh=p['variants'][v];saved=stored['variants'][v];assert fresh['status']==saved['status']
                    a=np.asarray(fresh['interval_centre']);b=np.asarray(saved['interval_centre'])
                    np.testing.assert_allclose(a,b,atol=c['optimizer_replay_atol'],rtol=c['optimizer_replay_rtol'])
                    max_difference=max(max_difference,float(np.max(abs(a-b))))
                    if v!='baseline':optimizations+=1
                    points=np.vstack((np.zeros(3),saved['features']))
                    assert order_check(points,cloud['observed_order'])['passed'];close(intervals(points),b)
                for key in ['interval_sd','gram_sd','blocks','covariance_condition','unconstrained_bias_centre']:
                    compare(p[key],stored[key])
                z=ec.coordinates_only(c['rho'],r['seed'],oc);s=cloud['selection']['selected']
                truth=z[[s['root']]+s['support']]-z[s['root']]
                close(truth,r['true_support_points']);truth_replayed+=1
                hash_matches+=ec.digest(z)==cloud['coordinates_sha256']
            else:assert r['true_support_points'] is None
            compare(evaluate(cloud['intrinsic'],cloud['observed_order'],stored,r['true_support_points']),r['evaluation'])
        phases[phase]=rows
    cal=json.loads((HERE/'frozen_calibration.json').read_text());compare(calibrate(phases['calibration']),cal)
    summary=analyze(phases['calibration'],phases['test'],cal)
    compare(summary,json.loads((HERE/'results/summary.json').read_text()))
    print(json.dumps(dict(verification='PASS_NUMERICAL_REPLAY',records=sum(map(len,phases.values())),
        truth_replayed=truth_replayed,coordinate_byte_hash_matches=int(hash_matches),
        optimizations_replayed=optimizations,maximum_interval_reoptimization_difference=max_difference,
        frozen_files=len(frozen['files']),controls=check(),decision=summary['decision'],
        limits='Archived selection/inference; fresh truth and optimizations. K is a working residual scale, not coordinate covariance.')))
if __name__=='__main__':main()
