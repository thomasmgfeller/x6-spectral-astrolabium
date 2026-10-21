"""SPDX-License-Identifier: Apache-2.0"""
import json
import subprocess
from gu_common import HERE,ROOT,BASE,cfg,ec,model,sha,encode,source_check,load_phase,compare,close
from gu_model import fit,predict,evaluate
from gu_calibrate import calibrate
from gu_analyze import analyze
from gu_controls import check

def gitfile(commit,path):return subprocess.check_output(['git','show',commit+':'+str(path.relative_to(ROOT))],cwd=ROOT)
def main():
    frozen=source_check();source=frozen['commit']
    subprocess.run(['git','merge-base','--is-ancestor',source,'HEAD'],cwd=ROOT,check=True)
    for name,h in frozen['files'].items():assert sha(gitfile(source,ROOT/name))==h,name
    compare(fit(),model());schedule=json.loads((HERE/'seed_schedule.json').read_text())
    old=json.loads((BASE/'error_calibration/seed_schedule.json').read_text())
    excluded=set(old['excluded_prior_seeds'])|{r['geometry_seed'] for phase in ['calibration','test'] for r in old[phase]}
    assert excluded==set(schedule['excluded_prior_seeds'])
    assert schedule['eligible_population']==2**32-len(excluded)
    phases={};coordinate_hash_matches=0;truth_replayed=0
    _,oc,_,_=ec.config()
    for phase in ['calibration','test']:
        executions,rows=load_phase(phase)
        assert len(rows)==cfg()['clouds_per_phase']
        assert [(r['index'],r['seed']) for r in rows]==[(r['index'],r['geometry_seed']) for r in schedule[phase]]
        assert all(r['seed'] not in excluded for r in rows)
        for e in executions:
            assert e['status']=='COMPLETE' and e['source_commit']==source
            assert e['seconds']<=cfg()['wall_seconds_per_worker'] and e['peak_mib']<=cfg()['memory_mib_per_worker']
            assert e['assigned_indices']==list(range(e['worker'],cfg()['clouds_per_phase'],cfg()['workers']))
            if phase=='calibration':assert e['execution_commit']==source
            else:
                subprocess.run(['git','merge-base','--is-ancestor',e['execution_commit'],'HEAD'],cwd=ROOT,check=True)
                assert gitfile(e['execution_commit'],HERE/'frozen_calibration.json')==(HERE/'frozen_calibration.json').read_bytes()
                assert gitfile(e['execution_commit'],HERE/'source_freeze.json')==(HERE/'source_freeze.json').read_bytes()
        for r in rows:
            row=r['cloud'];p=predict(row['intrinsic'],row['observed_order'],model())
            assert sha(encode(r['prediction']).encode())==r['prediction_seal']
            compare(p,r['prediction'])
            if p['status']=='COMPLETE':
                z=ec.coordinates_only(cfg()['rho'],r['seed'],oc);s=row['selection']['selected']
                truth=z[[s['root']]+s['support']]-z[s['root']]
                close(truth,r['true_support_points']);truth_replayed+=1
                coordinate_hash_matches+=ec.digest(z)==row['coordinates_sha256']
            else:assert r['true_support_points'] is None
            compare(evaluate(row['intrinsic'],row['observed_order'],r['prediction'],r['true_support_points']),r['evaluation'])
        phases[phase]=rows
    cal=json.loads((HERE/'frozen_calibration.json').read_text());compare(calibrate(phases['calibration']),cal)
    summary=analyze(phases['calibration'],phases['test'],cal)
    compare(summary,json.loads((HERE/'results/summary.json').read_text()))
    print(json.dumps(dict(verification='PASS_NUMERICAL_REPLAY',records=sum(map(len,phases.values())),
        truth_replayed=truth_replayed,coordinate_byte_hash_matches=int(coordinate_hash_matches),
        frozen_files=len(frozen['files']),controls=check(),decision=summary['decision'],
        limits='Replay regenerates truth but reuses archived order/selection/inference. Floating-point byte hashes are diagnostic only.')))

if __name__=='__main__':main()
