"""Cloud-level summaries and fixed finite-budget acceptance gates."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import core


def stats(values):
    x=np.asarray([v for v in values if v is not None],float)
    if not len(x): return dict(n=0,mean=None,se=None,rms=None)
    if not np.isfinite(x).all(): raise ValueError('nonfinite metric')
    return dict(n=len(x),mean=float(x.mean()),se=float(x.std(ddof=1)/math.sqrt(len(x))) if len(x)>1 else None,
                rms=float(np.sqrt(np.mean(x*x))))


def proportion(success,total):
    if not total: return dict(success=0,total=0,fraction=None,wilson95=None)
    z=1.959963984540054; p=success/total; d=1+z*z/total
    center=(p+z*z/(2*total))/d
    half=z/d*math.sqrt(p*(1-p)/total+z*z/(4*total*total))
    return dict(success=success,total=total,fraction=p,wilson95=[center-half,center+half])


def load(directory):
    execution=json.loads((directory/'execution.json').read_text())
    records=[]
    for row in execution['records']:
        data=(directory/row['file']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=row['sha256']: raise ValueError('record hash mismatch')
        records.append(json.loads(data))
    return execution,records


def summarize(directory):
    cfg=json.loads((core.HERE/'contract.json').read_text()); gates=cfg['gates']
    execution,records=load(directory); cells=[]
    for rho in cfg['densities']:
        group=[r for r in records if r['rho']==rho]; es=[r['evaluation'] for r in group]
        charts=[e['chart'] for e in es if e.get('chart',{}).get('status')=='ok']
        cell=dict(rho=rho,clouds=len(group),mean_poisson_count=stats([r['poisson_count'] for r in group]),
                  operator_available=proportion(sum(e['status']=='ok' for e in es),len(es)),
                  chart_available=proportion(len(charts),len(es)),
                  oracle_signature=proportion(sum(e.get('oracle_signature',False) for e in es),len(es)),
                  intrinsic_signature=proportion(sum(c['signature'] for c in charts),len(es)),
                  boundary_witnesses=proportion(sum(e.get('boundary_witness_fraction',0)>0 for e in es),len(es)),
                  statuses={s:sum(e['status']==s for e in es) for s in sorted({e['status'] for e in es})})
        for key in ['time_relative_rmse','space_relative_rmse','space_spearman','operator_normalized_rmse',
                    'oracle_metric_error','product_residual','affine_transform_residual','nonlinear_flat_chart_metric_error']:
            cell[key]=stats([e.get(key) for e in es])
        for key in ['field_error','metric_error','condition','smooth_field_metric_error']:
            cell['chart_'+key]=stats([c.get(key) for c in charts])
        cell['missing_distance_fraction']=stats([e['missing_distances']/e['total_distances'] for e in es if e.get('total_distances')])
        cell['true_cap_recall']=stats([e['true_cap_recovered']/e['true_cap_events'] for e in es if e.get('true_cap_events')])
        cell['true_cap_precision']=stats([e['true_cap_recovered']/e['selected_nonreference'] for e in es if e.get('selected_nonreference')])
        cell['mean_population']=stats([sum(e['populations'])/2 for e in es if 'populations' in e])
        operator_names=sorted({name for e in es for name in e.get('operator',{})})
        cell['operator_fields']={name:dict(response=stats([e['operator'][name]['value'] for e in es if 'operator' in e]),
             target=next(e['operator'][name]['target'] for e in es if 'operator' in e)) for name in operator_names}
        cells.append(cell)
    high,low=cells[-1],cells[0]
    def le(value,limit): return value is not None and value<=limit
    def ge(value,limit): return value is not None and value>=limit
    def improves(key):
        a,b=high[key]['rms'],low[key]['rms']; return a is not None and b is not None and a<b
    p1=dict(time_accuracy=le(high['time_relative_rmse']['rms'],gates['time_relative_rmse']),
            space_accuracy_conditional=le(high['space_relative_rmse']['rms'],gates['space_relative_rmse']),
            space_ranking_conditional=ge(high['space_spearman']['mean'],gates['space_spearman_min']),
            neighborhood_availability=ge(high['operator_available']['fraction'],1-gates['maximum_failure_fraction']),
            time_improvement=improves('time_relative_rmse'),space_improvement=improves('space_relative_rmse'))
    p2=dict(operator_accuracy=le(high['operator_normalized_rmse']['rms'],gates['operator_normalized_rmse']),
            oracle_metric_accuracy=le(high['oracle_metric_error']['rms'],gates['metric_relative_rmse']),
            oracle_signature=ge(high['oracle_signature']['fraction'],gates['signature_success_fraction']),
            metric_improvement=improves('oracle_metric_error'),
            chart_availability=ge(high['chart_available']['fraction'],1-gates['maximum_failure_fraction']),
            chart_accuracy=le(high['chart_metric_error']['rms'],gates['metric_relative_rmse']),
            chart_fields=le(high['chart_field_error']['rms'],gates['chart_field_relative_rmse']),
            chart_signature=ge(high['intrinsic_signature']['fraction'],gates['signature_success_fraction']))
    algebra=all(e.get('product_residual',0)<=gates['algebra_absolute_tolerance'] and
                e.get('affine_transform_residual',0)<=gates['algebra_absolute_tolerance'] and
                e.get('operator',{}).get('constant',{}).get('value',0)==0 and
                e.get('chart',{}).get('product_residual',0)<=gates['algebra_absolute_tolerance']
                for r in records for e in [r['evaluation']])
    relabel=sum(r['evaluation'].get('relabel_pass',False) for r in records)
    expected={(rho,cfg['test_seed_base']+100*i+j) for i,rho in enumerate(cfg['densities']) for j in range(cfg['test_replicates_per_density'])}
    actual={(r['rho'],r['seed']) for r in records}
    complete=execution['mode']=='test' and execution['status']=='COMPLETE' and actual==expected and len(records)==len(expected)
    budget=execution['seconds']<=cfg['wall_budget_seconds'] and execution['peak_mib']<=cfg['memory_budget_mib']
    passed=complete and budget and algebra and relabel==3 and all(p1.values()) and all(p2.values())
    return dict(schema='x6.bk-phase12-summary/1',decision='PASS_FLAT_PILOT' if passed else 'HOLD_PHASE3',
                complete=complete,budget_pass=budget,algebra_pass=algebra,relabel_clouds_passed=relabel,
                phase1_gates=p1,phase2_gates=p2,cells=cells,seconds=execution['seconds'],peak_mib=execution['peak_mib'],
                source_commit=execution['source_commit'],curvature_estimator=False,
                caveats=['2+1 only; no asymptotic proof','distance errors conditional on successful anchor search; coverage and oracle cap recall reported',
                         'chart is an exploratory same-cloud volume estimator','signature denominator includes unavailable clouds',
                         'BD-C2 NO_GO unchanged'])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=summarize(args.directory)
    data=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output: args.output.write_text(data)
    else: print(data)

if __name__=='__main__': main()
