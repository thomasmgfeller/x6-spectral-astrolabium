"""Post-seal evaluation of availability, accuracy and computational/noise cost.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,gzip,hashlib,json
from collections import Counter
from pathlib import Path
import numpy as np
from fit import SOURCE
from inference import ETA,design,solve
from run import encode,frozen,save

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['archive','fresh']);a=ap.parse_args()
    frozen();c=json.loads((HERE/'contract.json').read_text());root=HERE/('archive' if a.mode=='archive' else 'results')
    rows=[];times=[];all_fit=[];all_old=[]
    for index in range(c['clouds']):
        path=root/f'cloud-{index:02d}.json.gz'
        if not path.exists():rows.append(dict(index=index,status='NOT_COMPLETED'));continue
        raw=path.read_bytes();r=json.loads(gzip.decompress(raw));e=dict(index=index,status=r['selection']['status'])
        if not r['replicates']:rows.append(e);continue
        truth=json.loads((root/f'truth/cloud-{index:02d}.json').read_text())
        assert truth['inference_sha256']==hashlib.sha256(raw).hexdigest()
        p=r['selection']['fourth']['packet'];points=np.array(truth['points']);x=points[4:]-points[4];scale=p['scale']
        oracle,*_=solve(design(x[1:]/scale),np.array([0,0,0,-2,2,2,0,0,0.]),scale)
        reps=r['replicates'];primary=reps[0];f=primary['fit'];old=primary['baseline']['four'];three=primary['baseline']['baseline']
        e.update(fit_status=f['status'],four_status=old['status'],fit_qualified=f.get('qualified',False),four_qualified=old.get('qualified',False),fit_reason=f.get('reason'),fit_seconds=f['seconds'])
        weights={'oracle':oracle}
        for arm,v in [('fit',f),('four',old),('three',three)]:
            if v['status']=='WEIGHTS_VALID':weights[arm]=np.array(v['weights'])
        e['fields']=[]
        for spec in c['fields']:
            k=np.array(spec['k']);phase=spec['phase'];u=x@k;fun=np.cos if spec['kind']=='cos' else np.sin
            y=fun(u+phase)-fun(phase);linear=(-np.sin(phase) if spec['kind']=='cos' else np.cos(phase))*u
            target=(k[0]**2-k[1]**2-k[2]**2)*fun(phase)
            field=dict(name=spec['name'],errors={arm:float(w@y-target) for arm,w in weights.items()},linear={arm:float(w@linear) for arm,w in weights.items()})
            if len(reps)>1 and all(rr['fit']['qualified'] and rr['baseline']['four']['status']=='WEIGHTS_VALID' for rr in reps[1:]):
                field['repeat_variance']={arm:float(np.var([np.array((rr['fit'] if arm=='fit' else rr['baseline']['four'])['weights'])@y for rr in reps[1:]],ddof=1)) for arm in ['fit','four']}
            e['fields'].append(field)
        e['noise_variance']={arm:float(c['field_noise_sigma']**2*(w@w)) for arm,w in weights.items()}
        e['interval_mse']={}
        ii,jj=np.triu_indices(len(points),1);true_s2=np.sum((points[jj]-points[ii])**2*ETA,axis=1)/scale**2
        for arm,v in [('fit',f),('four',old)]:
            if v['status']=='WEIGHTS_VALID':
                z=np.array(v['coordinates']);s2=np.sum((z[jj]-z[ii])**2*ETA,axis=1)
                e['interval_mse'][arm]=float(np.mean((s2-true_s2)**2))
        for rr in reps:
            times.append(rr['fit']['seconds']);all_fit.append(rr['fit']['status']);all_old.append(rr['baseline']['four']['status'])
        rows.append(e)
    common=[r for r in rows if r.get('fit_status')=='WEIGHTS_VALID' and r.get('four_status')=='WEIGHTS_VALID']
    def stats(pop):
        if not pop:return None
        rmse={arm:float(np.sqrt(np.mean([f['errors'][arm]**2 for r in pop for f in r['fields']]))) for arm in ['fit','four','oracle']}
        linear={arm:float(np.sqrt(np.mean([f['linear'][arm]**2 for r in pop for f in r['fields']]))) for arm in ['fit','four']}
        noise={arm:float(np.mean([r['noise_variance'][arm] for r in pop])) for arm in ['fit','four']}
        intervals={arm:float(np.sqrt(np.mean([r['interval_mse'][arm] for r in pop]))) for arm in ['fit','four']}
        return dict(clouds=len(pop),rmse=rmse,rmse_ratio=rmse['fit']/rmse['four'],linear_rmse=linear,linear_ratio=linear['fit']/linear['four'],mean_noise_variance=noise,noise_ratio=noise['fit']/noise['four'],normalized_signed_interval_rmse=intervals)
    primary=stats(common);qualified_common=stats([r for r in common if r['four_qualified']])
    complete=[r for r in rows if r.get('fields') and 'repeat_variance' in r['fields'][0]]
    repeat=None
    if complete:
        v={arm:float(np.mean([f['repeat_variance'][arm] for r in complete for f in r['fields']])) for arm in ['fit','four']}
        repeat=dict(clouds=len(complete),variance=v,ratio=v['fit']/v['four'],scope='Conditional on selected A, complete B1-B8 paired groups only; descriptive, no candidate coverage calibration.')
    boot=None
    if len(common)>=2:
        rng=np.random.default_rng(c['bootstrap_seed']);sq=np.array([[np.mean([f['errors'][arm]**2 for f in r['fields']]) for arm in ['four','fit']] for r in common])
        ix=rng.integers(0,len(common),(c['bootstrap_draws'],len(common)));means=sq[ix].mean(axis=1)
        boot=np.quantile(np.sqrt(means[:,1]/means[:,0]),[.025,.975]).tolist()
    qualified=sum(r.get('fit_qualified',False) for r in rows);g=c['primary_gates']
    gates=dict(all_scheduled_recorded=all(r['status']!='NOT_COMPLETED' for r in rows),qualified_availability=qualified>=g['minimum_qualified_primary_clouds'],common_availability=len(common)>=g['minimum_common_primary_weight_cases'],rmse=primary is not None and primary['rmse_ratio']<=g['maximum_rmse_ratio_fit_to_four'],linear_response=primary is not None and primary['linear_ratio']<=g['maximum_linear_response_rmse_ratio'],noise_cost=primary is not None and primary['noise_ratio']<=g['maximum_mean_iid_noise_variance_ratio'],fit_cost=bool(times) and np.median(times)<=g['maximum_median_fit_seconds'] and max(times)<=g['maximum_fit_seconds'],repeat_variance=repeat is not None and repeat['clouds']>=g['minimum_complete_repeat_groups'] and repeat['ratio']<=g['maximum_repeat_response_variance_ratio'])
    out=dict(status=('DEVELOPMENT_CANDIDATE_SUPPORTED' if all(gates.values()) else 'HOLD') if a.mode=='fresh' else 'ARCHIVE_DESCRIPTIVE_ONLY',mode=a.mode,scheduled=c['clouds'],selection_statuses=dict(Counter(r['status'] for r in rows)),qualified_primary=dict(fit=qualified,four=sum(r.get('four_qualified',False) for r in rows)),all_replicates=dict(fit=dict(Counter(all_fit)),four=dict(Counter(all_old))),raw_common=primary,both_qualified_common=qualified_common,rmse_ratio_cloud_bootstrap_95=boot,repeat=repeat,fit_seconds=dict(median=float(np.median(times)),maximum=max(times),total=sum(times)) if times else None,gates=gates if a.mode=='fresh' else None,records=rows,holds=c['holds'],note='Order is fitted input, not independent accuracy evidence. Four analytic fields and B repeats do not multiply independent A selections. Common-set accuracy is conditional; failures are retained in coverage.')
    save(HERE/f'analysis-{a.mode}.json',out)
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))

if __name__=='__main__':main()
