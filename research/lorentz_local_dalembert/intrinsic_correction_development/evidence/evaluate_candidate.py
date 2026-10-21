"""Truth is consumed only after inference.json has been sealed."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent


def main():
    raw = (HERE/'inference.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==json.loads((HERE/'inference_seal.json').read_text())['sha256']
    inference = json.loads(raw)
    truth = json.loads((HERE/'evaluation_inputs.json').read_text())
    lookup = {(r['phase'],r['index']):r for r in truth['records']}
    fields = truth['fields']
    results=[]
    for row in inference['records']:
        reference=lookup[row['phase'],row['index']]
        out={k:row[k] for k in ['phase','index','seed','status']}
        if reference['status']!='COMPLETE':
            results.append(out);continue
        x=np.array(reference['true_points'])
        corr=row['correction']; accepted=corr['status']=='ACCEPTED'
        arms={name:np.array(reference['saved_'+name]) for name in ['original','projected','oracle']}
        arms['candidate_policy']=np.array(corr['weights']) if accepted else arms['projected']
        rows=[]
        for j,f in enumerate(fields):
            k=np.array(f['k']);phase=f['phase'];u=x@k
            func=np.cos if f['kind']=='cos' else np.sin
            root=func(phase);linear=(-np.sin(phase) if f['kind']=='cos' else np.cos(phase))*u
            contrast=func(phase+u)-root
            exact=(k[0]**2-k[1]**2-k[2]**2)*root
            errors={a:float(w@contrast-exact) for a,w in arms.items()}
            for a,index in [('original',0),('projected',2),('oracle',4)]:
                np.testing.assert_allclose(errors[a],reference['saved_fields'][j]['errors'][index],rtol=1e-7,atol=1e-8)
            rows.append(dict(name=f['name'],errors=errors,linear_response={a:float(w@linear) for a,w in arms.items()}))
        out.update(accepted=accepted,correction_status=corr['status'],fields=rows,
                   iid_noise_variance={a:float(1e-6*(w@w)) for a,w in arms.items()},
                   physical_linear_moment_norm={a:float(np.linalg.norm(x.T@w)) for a,w in arms.items()})
        results.append(out)
    summary={}
    for phase in ['calibration','test']:
        total=[r for r in results if r['phase']==phase]
        available=[r for r in total if 'fields' in r]
        accepted=[r for r in available if r['accepted']]
        group={}
        for name,population in [('all_previously_complete_with_fallback',available),('accepted_common_cases',accepted)]:
            if not population:
                group[name]=None;continue
            fs=[f for r in population for f in r['fields']]
            rmse={a:math.sqrt(np.mean([f['errors'][a]**2 for f in fs])) for a in arms}
            linear={a:math.sqrt(np.mean([f['linear_response'][a]**2 for f in fs])) for a in arms}
            noise={a:float(np.mean([r['iid_noise_variance'][a] for r in population])) for a in arms}
            group[name]=dict(clouds=len(population),rmse=rmse,linear_response_rmse=linear,mean_iid_noise_variance=noise,
                             rmse_ratio=rmse['candidate_policy']/rmse['original'],
                             linear_ratio=linear['candidate_policy']/linear['original'],
                             noise_ratio=noise['candidate_policy']/noise['original'])
        metric=group['all_previously_complete_with_fallback']
        gates=dict(availability=len(accepted)==len(available),rmse=metric['rmse_ratio']<=.9,
                   linear_response=metric['linear_ratio']<=.9,noise_cost=metric['noise_ratio']<=1.25)
        summary[phase]=dict(scheduled=len(total),previously_complete=len(available),accepted=len(accepted),
                            old_unavailable=len(total)-len(available),groups=group,gates=gates,
                            development_gate='PASS' if all(gates.values()) else 'HOLD')
    result=dict(status='EVALUATED',interpretation='Retrospective development; no independent statistical confirmation',
                phases=summary,records=results,new_cloud_confirmation='NOT_RUN',
                inference_sha256=hashlib.sha256(raw).hexdigest())
    (HERE/'evaluation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
