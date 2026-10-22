"""Frozen post-seal calculations. All primary rules reside in contract.json.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,gzip,hashlib,json
from collections import Counter
from pathlib import Path
import numpy as np
from models import PRIOR
from run import save
from runner import verify_freeze

HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['development','conditional']);a=ap.parse_args();verify_freeze()
    c=json.loads((HERE/'contract.json').read_text());rows=[];all_status={};timings={};groups={}
    arms=['old_poisson','full_gls']+(['no_support_order','diagonal_gls'] if a.mode=='development' else [])
    for arm in ['four']+arms:all_status[arm]=Counter();timings[arm]=[];groups[arm]=[]
    for index in c['selected_indices']:
        raw=(HERE/f'{a.mode}/cloud-{index:02d}.json.gz').read_bytes();r=json.loads(gzip.decompress(raw));truth=json.loads((HERE/f'{a.mode}/truth/cloud-{index:02d}.json').read_text());assert truth['inference_sha256']==hashlib.sha256(raw).hexdigest()
        pts=np.array(truth['points']);x=pts[4:]-pts[4];fields=[]
        for spec in c['fields']:
            k=np.array(spec['k']);phase=spec['phase'];fun=np.cos if spec['kind']=='cos' else np.sin
            fields.append((fun(x@k+phase)-fun(phase),(k[0]**2-k[1]**2-k[2]**2)*fun(phase)))
        reps=r['replicates'];primary=reps[0]['arms'];entry=dict(index=index,primary={arm:dict(status=v['status'],qualified=v.get('qualified',False)) for arm,v in primary.items()},errors={},noise={},variance={})
        for arm,v in primary.items():
            if v['status']=='WEIGHTS_VALID':
                w=np.array(v['weights']);entry['errors'][arm]=[float(w@y-target) for y,target in fields];entry['noise'][arm]=float(c['field_noise_sigma']**2*(w@w))
        for arm in primary:
            for rep in reps:
                v=rep['arms'][arm];all_status[arm][v['status']]+=1
                if 'seconds' in v:timings[arm].append(v['seconds'])
            if all(rr['arms'][arm]['status']=='WEIGHTS_VALID' for rr in reps[1:]):
                vals=np.array([[np.array(rr['arms'][arm]['weights'])@y for y,_ in fields] for rr in reps[1:]])
                entry['variance'][arm]=float(np.mean(np.var(vals,axis=0,ddof=1)))
        rows.append(entry)
    summaries={}
    for arm in arms:
        common=[r for r in rows if arm in r['errors'] and 'four' in r['errors']]
        vr=[r for r in rows if all(k in r['variance'] for k in set(['four','old_poisson',arm]))]
        rmse={k:float(np.sqrt(np.mean([e**2 for r in common for e in r['errors'][k]]))) for k in ['four',arm]} if common else None
        noise={k:float(np.mean([r['noise'][k] for r in common])) for k in ['four',arm]} if common else None
        var={k:float(np.mean([r['variance'][k] for r in vr])) for k in set(['four','old_poisson',arm])} if vr else None
        t=timings[arm]
        summaries[arm]=dict(qualified_primary=sum(r['primary'][arm]['qualified'] for r in rows),common_primary=len(common),rmse=rmse,rmse_ratio_to_four=rmse[arm]/rmse['four'] if rmse else None,noise=noise,noise_ratio_to_four=noise[arm]/noise['four'] if noise else None,complete_repeat_groups=len(vr),repeat_group_indices=[r['index'] for r in vr],variance=var,variance_ratio_to_four=var[arm]/var['four'] if var else None,variance_ratio_to_old_poisson=var[arm]/var['old_poisson'] if var else None,fit_seconds=dict(median=float(np.median(t)),maximum=max(t)) if t else None)
    s=summaries['full_gls'];g=c['conditional_gates'];gates={}
    if a.mode=='conditional':
        gates=dict(all_19_configurations_completed=len(rows)==19,qualified_primary=s['qualified_primary']>=g['minimum_qualified_primary'],common_primary=s['common_primary']>=g['minimum_common_primary'],rmse=s['rmse_ratio_to_four'] is not None and s['rmse_ratio_to_four']<=g['maximum_rmse_ratio_to_four'],field_noise=s['noise_ratio_to_four'] is not None and s['noise_ratio_to_four']<=g['maximum_noise_variance_ratio_to_four'],repeat_groups=s['complete_repeat_groups']>=g['minimum_complete_repeat_groups'],repeat_variance_vs_four=s['variance_ratio_to_four'] is not None and s['variance_ratio_to_four']<=g['maximum_repeat_variance_ratio_to_four'],repeat_variance_vs_old=s['variance_ratio_to_old_poisson'] is not None and s['variance_ratio_to_old_poisson']<=g['maximum_repeat_variance_ratio_to_old_poisson'],cost=s['fit_seconds']['median']<=g['maximum_median_fit_seconds'] and s['fit_seconds']['maximum']<=g['maximum_fit_seconds'])
    out=dict(status=('CONDITIONAL_DEVELOPMENT_SUPPORTED' if all(gates.values()) else 'HOLD') if gates else 'POSTHOC_DIAGNOSTIC',mode=a.mode,configurations=len(rows),summaries=summaries,status_counts={a:dict(v) for a,v in all_status.items()},gates=gates,records=rows,holds=c['holds'],scope='Same 19 previously selected A configurations. Fresh conditional B draws do not establish new-A selection or global pipeline qualification. Order is fitted input, not independent validation.')
    save(HERE/f'analysis-{a.mode}.json',out);print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))

if __name__=='__main__':main()
