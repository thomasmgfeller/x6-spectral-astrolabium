"""Prespecified paired selection and operator gates; truth read only after seal.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
import math
from collections import Counter
import numpy as np
from eb_common import HERE, read, save, frozen

def fields(points,c):
    x=np.array(points)[4:]-np.array(points)[4]; out=[]
    for spec in c['fields']:
        k=np.array(spec['k']); phase=spec['phase']; fun=np.cos if spec['kind']=='cos' else np.sin
        out.append((fun(x@k+phase)-fun(phase),(k[0]**2-k[1]**2-k[2]**2)*fun(phase)))
    return out

def main():
    frozen(); c=read(HERE/'contract.json'); rows=[]; status={a:Counter() for a in ['legacy','candidate']}
    for index in range(c['clouds']):
        path=HERE/f'results/cloud-{index:02d}.json.gz'; r=read(path)
        row=dict(index=index,selection={a:v['status']=='SELECTED' for a,v in r['selection']['arms'].items()},
            primary={},errors={},noise={},variance={},predicted_variance={},selector_seconds=r['selection']['selector_seconds'])
        if r['replicates']:
            truth=read(HERE/f'results/truth/cloud-{index:02d}.json')
            assert truth['inference_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
            for arm,tr in truth['arms'].items():
                ff=fields(tr['points'],c); reps=[v['arms'][arm]['measurement']['four'] for v in r['replicates']]
                p=reps[0]; row['primary'][arm]=dict(status=p['status'],qualified=p.get('qualified',False))
                status[arm].update(v['status'] for v in reps)
                if p['status']=='WEIGHTS_VALID':
                    w=np.array(p['weights']); row['errors'][arm]=[float(w@y-target) for y,target in ff]
                    row['noise'][arm]=float(c['field_noise_sigma']**2*(w@w))
                    cov=np.array(p['weight_covariance'])
                    row['predicted_variance'][arm]=float(np.mean([y@cov@y for y,_ in ff]))
                if all(v['status']=='WEIGHTS_VALID' for v in reps[1:]):
                    values=np.array([[np.array(v['weights'])@y for y,_ in ff] for v in reps[1:]])
                    row['variance'][arm]=float(np.mean(np.var(values,axis=0,ddof=1)))
        rows.append(row)
    selected={a:sum(r['selection'][a] for r in rows) for a in status}
    gains=[r['index'] for r in rows if r['selection']['candidate'] and not r['selection']['legacy']]
    losses=[r['index'] for r in rows if r['selection']['legacy'] and not r['selection']['candidate']]
    n=len(gains)+len(losses)
    # Exact one-sided conditional binomial tail under equal discordant probabilities.
    pvalue=sum(math.comb(n,k) for k in range(len(gains),n+1))/2**n if n else 1.
    common=[r for r in rows if all(a in r['errors'] for a in status)]
    groups=[r for r in rows if all(a in r['variance'] for a in status)]
    summaries={}
    for a in status:
        own=[r for r in rows if a in r['errors']]
        qualified=[r for r in own if r['primary'][a]['qualified']]
        calibrated=[r for r in rows if a in r['variance'] and a in r['predicted_variance']]
        def rmse(rr):return float(np.sqrt(np.mean([e*e for r in rr for e in r['errors'][a]]))) if rr else None
        empirical=float(np.mean([r['variance'][a] for r in calibrated])) if calibrated else None
        predicted=float(np.mean([r['predicted_variance'][a] for r in calibrated])) if calibrated else None
        times=[r['selector_seconds'][a] for r in rows]
        summaries[a]=dict(selected=selected[a],qualified_primary=len(qualified),computable_primary=len(own),
            all_available_rmse=rmse(own),qualified_subset_rmse=rmse(qualified),paired_primary_count=len(common),paired_rmse=rmse(common),
            paired_noise=float(np.mean([r['noise'][a] for r in common])) if common else None,
            paired_repeat_groups=len(groups),paired_repeat_variance=float(np.mean([r['variance'][a] for r in groups])) if groups else None,
            calibration_groups=len(calibrated),empirical_variance=empirical,predicted_variance=predicted,
            calibration_ratio=empirical/predicted if predicted and predicted>0 else None,
            selector_seconds=dict(median=float(np.median(times)),maximum=max(times)))
    old,new=summaries['legacy'],summaries['candidate']
    def ratio(key):return new[key]/old[key] if old[key] is not None and old[key]>0 and new[key] is not None else None
    ratios={key:ratio(key) for key in ['paired_rmse','paired_noise','paired_repeat_variance']}
    completed=all(read(HERE/f'results/worker-{i}.json')['status']=='COMPLETE' for i in range(c['workers']))
    sg=c['selection_gates']; og=c['operator_gates']
    selection_gates=dict(all_attempts_completed=completed and len(rows)==c['clouds'],
        availability=selected['candidate']>=sg['minimum_selected'],no_legacy_losses=len(losses)==0,
        minimum_gains=len(gains)>=sg['minimum_gains'],paired_exact_tail=pvalue<=sg['maximum_one_sided_p'],
        selector_cost=new['selector_seconds']['median']<=sg['maximum_median_seconds'] and new['selector_seconds']['maximum']<=sg['maximum_seconds'])
    def within(key,limit):return ratios[key] is not None and ratios[key]<=limit
    operator_gates=dict(qualified_primary=new['qualified_primary']>=og['minimum_qualified_primary'],
        common_primary=len(common)>=og['minimum_common_primary'],accuracy=within('paired_rmse',og['maximum_rmse_ratio']),
        field_noise=within('paired_noise',og['maximum_noise_ratio']),
        complete_repeat_groups=len(groups)>=og['minimum_paired_repeat_groups'],repeat_variance=within('paired_repeat_variance',og['maximum_repeat_variance_ratio']),
        calibration_groups=new['calibration_groups']>=og['minimum_calibration_groups'],
        covariance_calibration=new['calibration_ratio'] is not None and og['calibration_ratio_range'][0]<=new['calibration_ratio']<=og['calibration_ratio_range'][1])
    out=dict(selection_status='SELECTION_PILOT_SUPPORTED' if all(selection_gates.values()) else 'SELECTION_HOLD',
        operator_status='OPERATOR_PILOT_SUPPORTED' if all(selection_gates.values()) and all(operator_gates.values()) else 'OPERATOR_HOLD',
        selection_gates=selection_gates,operator_gates=operator_gates,summaries=summaries,ratios=ratios,
        gain_indices=gains,loss_indices=losses,one_sided_paired_exact_p=pvalue,paired_primary_indices=[r['index'] for r in common],
        paired_repeat_indices=[r['index'] for r in groups],status_counts={a:dict(v) for a,v in status.items()},records=rows,holds=c['holds'],
        scope='Fresh independent A configurations; paired old/new selectors on identical A and B draws. Point-estimate pilot gates, no population qualification. Own-sample and qualified-subset errors are descriptive and selection-biased. No covariance coverage claim.')
    save(HERE/'analysis.json',out); print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))

if __name__=='__main__':main()
