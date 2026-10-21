"""Frozen descriptive analysis; independent clouds are the sampling units."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from moment_common import HERE,config
from moments import NAMES


def load(directory):
    execution=json.loads((directory/'execution.json').read_text());rows=[]
    assert len({r['file'] for r in execution['records']})==len(execution['records'])
    for r in execution['records']:
        data=(directory/r['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==r['sha256']
        rows.append(json.loads(data))
    return execution,rows


def stats(values):
    a=np.array(values,float)
    return dict(n=len(a),mean=float(a.mean()) if len(a) else None,
                se=float(a.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None)


def summarize(directory):
    contract,_=config();execution,rows=load(directory);mode=execution['mode']
    expected=[(rho,s) for i,rho in enumerate(contract['densities']) for s in
              (contract['development_seeds'] if mode=='development' else [contract['test_seed_base']+100*i+j for j in range(contract['test_replicates_per_density'])])]
    complete=execution['status']=='COMPLETE' and [(r['rho'],r['seed']) for r in rows]==expected
    budget=execution['seconds']<=contract['wall_budget_seconds'] and execution['peak_mib']<=contract['memory_budget_mib']
    algebra=execution['controls']['status']=='PASS_SOFTWARE_CONTROLS' and all(a.get('raw_identity_pass',a['status']!='ok') for r in rows for a in r['arms'].values())
    cells=[]
    for rho in contract['densities']:
        group=[r for r in rows if r['rho']==rho];arms={}
        for arm in contract['arms']:
            ds=[r['arms'][arm]['diagnosis'] for r in group if r['arms'][arm]['status']=='ok']
            variants={}
            for name in NAMES:
                sq=[d['variants'][name]['error']**2 for d in ds]
                variants[name]=dict(rms=float(np.sqrt(np.mean(sq))) if sq else None,
                    signatures=sum(d['variants'][name]['lorentz_signature'] for d in ds),
                    paired_squared_error_reduction=stats([d['variants']['raw']['error']**2-d['variants'][name]['error']**2 for d in ds]))
            arms[arm]=dict(available=len(ds),total=len(group),availability=len(ds)/len(group) if group else 0,
                variants=variants,
                corrected_to_raw_rms=variants['TSD']['rms']/variants['raw']['rms'] if ds and variants['raw']['rms'] else None,
                shapley={f:stats([d['shapley_squared_error_reduction'][f] for d in ds]) for f in contract['factors']},
                moments={k:stats([d['decomposition'][k] for d in ds]) for k in ['temporal_error_squared','shell_error_squared','cross_term']},
                temporal_ratio=stats([np.mean(d['temporal_proper_time_ratios']) for d in ds]),
                shell_mean_ratio=stats([np.mean([v['mean'] for v in d['shell_proper_time_ratios']]) for d in ds]),
                shell_within_side_sd_ratio=stats([np.mean([v['sd'] for v in d['shell_proper_time_ratios']]) for d in ds]),
                endpoint_rapidity=stats([np.mean(d['endpoint_rapidities']) for d in ds]),
                reference_rapidity=stats([np.mean(d['reference_rapidities']) for d in ds]),
                mean_side_population=stats([np.mean(d['populations']) for d in ds]))
        cells.append(dict(rho=rho,arms=arms))
    primary=next(c for c in cells if c['rho']==contract['primary_density'])
    passed=complete and budget and algebra and all(a['availability']>=contract['availability_min'] and
        a['corrected_to_raw_rms'] is not None and a['corrected_to_raw_rms']<=contract['corrected_to_raw_rms_max'] for a in primary['arms'].values())
    return dict(schema='x6.bk-moment-summary/1',mode=mode,complete=complete,budget_pass=budget,algebra_pass=algebra,
                clouds=len(rows),cells=cells,decision=('MOMENT_CONTROLS_INFORMATIVE' if passed else 'MOMENT_DIAGNOSIS_MIXED') if mode=='test' else 'DEVELOPMENT_ONLY',
                phase3='HOLD_PHASE3',note='Oracle diagnostics only; paired errors use identical available clouds within each arm. Standard errors use cloud means; no convergence claim.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args()
    summary=summarize(a.directory);(a.directory/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
