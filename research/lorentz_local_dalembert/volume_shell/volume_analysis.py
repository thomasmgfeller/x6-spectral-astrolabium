"""Frozen paired analysis with an explicit affine-response guard."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from volume_common import config
from moment_analysis import stats


def load(directory):
    e=json.loads((directory/'execution.json').read_text());rows=[]
    assert len({r['file'] for r in e['records']})==len(e['records'])
    for r in e['records']:
        data=(directory/r['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==r['sha256']
        rows.append(json.loads(data))
    return e,rows


def rms(values):
    return float(np.sqrt(np.mean(np.array(values,float)**2))) if values else None


def summarize(directory):
    contract,_=config();e,rows=load(directory);mode=e['mode']
    expected=[(rho,seed) for i,rho in enumerate(contract['densities']) for seed in
              (contract['development_seeds'] if mode=='development' else [contract['test_seed_base']+100*i+j for j in range(contract['test_replicates_per_density'])])]
    complete=e['status']=='COMPLETE' and [(r['rho'],r['seed']) for r in rows]==expected
    budget=e['seconds']<=contract['wall_budget_seconds'] and e['peak_mib']<=contract['memory_budget_mib']
    algebra=e['controls']['status']=='PASS_SOFTWARE_CONTROLS' and all(
        r['relabel_pass'] is not False and (r['selection']['status']!='ok' or r['oracle_moment_identity_pass']) and
        all(a['status']!='ok' or a['evaluation']['algebra_pass'] for a in r['arms'].values()) for r in rows)
    cells=[]
    for rho in contract['densities']:
        group=[r for r in rows if r['rho']==rho];arms={}
        for method in contract['methods']:
            available=[r for r in group if r['arms'][method]['status']=='ok'];ev=[r['arms'][method]['evaluation'] for r in available]
            common=[r for r in available if r['arms']['raw']['status']=='ok']
            raw=[r['arms']['raw']['evaluation'] for r in common];new=[r['arms'][method]['evaluation'] for r in common]
            paired={}
            for key in ['metric_error','affine_drift']:
                a=rms([v[key] for v in raw]);b=rms([v[key] for v in new])
                paired[key]=dict(raw_rms=a,candidate_rms=b,ratio=b/a if a else None,
                                 squared_reduction=stats([u[key]**2-v[key]**2 for u,v in zip(raw,new)]))
            fields={}
            if ev:
                for field in ev[0]['fields']:
                    fields[field]=dict(target=ev[0]['fields'][field]['target'],
                                       response=stats([v['fields'][field]['value'] for v in ev]),
                                       error_rms=rms([v['fields'][field]['value']-v['fields'][field]['target'] for v in ev]))
            quality=[r['arms'][method]['shell_time_quality'] for r in available if 'shell_time_quality' in r['arms'][method]]
            arms[method]=dict(available=len(ev),total=len(group),availability=len(ev)/len(group) if group else 0,
                metric_rms=rms([v['metric_error'] for v in ev]),affine_drift_rms=rms([v['affine_drift'] for v in ev]),
                dimensional_affine_norm_rms=rms([v['dimensional_affine_norm'] for v in ev]),
                lorentz_signatures=sum(v['lorentz_signature'] for v in ev),paired_count=len(common),paired=paired,fields=fields,
                shell_time_quality={k:stats([q[k] for q in quality]) for k in ['mean_ratio','relative_mse','minimum_count','mean_count']} if quality else None)
        cells.append(dict(rho=rho,arms=arms))
    a=next(c for c in cells if c['rho']==contract['primary_density'])['arms'][contract['primary_method']]
    mr=a['paired']['metric_error']['ratio'];ar=a['paired']['affine_drift']['ratio']
    gates=dict(availability=a['availability']>=contract['minimum_availability'],
               paired_metric=mr is not None and mr<=contract['maximum_paired_metric_rms_ratio'],
               paired_affine_drift=ar is not None and ar<=contract['maximum_paired_affine_drift_rms_ratio'])
    passed=complete and budget and algebra and all(gates.values())
    return dict(schema='x6.bk-volume-shell-summary/1',mode=mode,complete=complete,budget_pass=budget,algebra_pass=algebra,
                clouds=len(rows),cells=cells,primary_gates=gates,
                decision=('INTRINSIC_SHELL_WEIGHTING_IMPROVED' if passed else 'SHELL_WEIGHTING_HOLD') if mode=='test' else 'DEVELOPMENT_ONLY',
                phase3='HOLD_PHASE3',note='Primary candidate fixed before data. Cloud-level uncertainty; descriptive improvement is not flat/curvature qualification. Oracle arms are diagnostic only.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();s=summarize(a.directory)
    (a.directory/'summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
