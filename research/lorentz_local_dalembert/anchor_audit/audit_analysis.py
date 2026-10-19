"""Frozen cloud-level descriptive analysis; coverage never grants phase 3."""
import argparse
import hashlib
import json
from pathlib import Path
from scipy.stats import binomtest
from common import config
import analyze as legacy_analysis

stats = legacy_analysis.stats
proportion = legacy_analysis.proportion


def load(directory):
    execution = json.loads((directory/'execution.json').read_text()); rows = []
    for record in execution['records']:
        data = (directory/record['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != record['sha256']: raise ValueError('Record hash mismatch')
        rows.append(json.loads(data))
    return execution, rows


def ratio(e,a,b): return e[a]/e[b] if e.get(b) else None


def summarize(directory):
    audit,cfg = config(); execution,records = load(directory); cells = []
    for rho in audit['densities']:
        rows = [r for r in records if r['rho']==rho]; methods = {}
        for name in audit['methods']:
            es = [r['evaluations'][name] for r in rows]
            charts = [e['chart'] for e in es if e.get('chart',{}).get('status')=='ok']
            cell = dict(available=proportion(sum(e['status']=='ok' for e in es),len(es)),
                        signature=proportion(sum(e.get('oracle_signature',False) for e in es),len(es)),
                        chart_available=proportion(len(charts),len(es)),
                        chart_signature=proportion(sum(c['signature'] for c in charts),len(es)),
                        boundary_witness=proportion(sum(e.get('boundary_witness_fraction',0)>0 for e in es),len(es)))
            for key in ['time_relative_rmse','space_relative_rmse','space_spearman','operator_normalized_rmse','oracle_metric_error']:
                cell[key] = stats([e.get(key) for e in es])
            for key in ['metric_error','field_error','condition']:
                cell['chart_'+key] = stats([c.get(key) for c in charts])
            for key,a,b in [('cap_recall','true_cap_recovered','true_cap_events'),('cap_precision','true_cap_recovered','selected_nonreference'),('missing_fraction','missing_distances','total_distances')]:
                cell[key] = stats([ratio(e,a,b) for e in es])
            cell['population'] = stats([sum(e['populations'])/2 for e in es if 'populations' in e])
            cell['method_seconds'] = stats([r['method_seconds'][name] for r in rows])
            methods[name] = cell
        pairs = [(r['evaluations']['legacy64'],r['evaluations']['balanced64']) for r in rows]
        gained = sum(a['status']!='ok' and b['status']=='ok' for a,b in pairs)
        lost = sum(a['status']=='ok' and b['status']!='ok' for a,b in pairs)
        recall_differences = []
        for a,b in pairs:
            x,y = ratio(a,'true_cap_recovered','true_cap_events'),ratio(b,'true_cap_recovered','true_cap_events')
            if x is not None and y is not None: recall_differences.append(y-x)
        common = [(a,b) for a,b in pairs if a['status']==b['status']=='ok']
        paired = dict(gained=gained,lost=lost,availability_gain=(gained-lost)/len(rows) if rows else None,
                      mcnemar_exact_two_sided_p=float(binomtest(gained,gained+lost,.5).pvalue) if gained+lost else 1.,
                      recall_change=stats(recall_differences),
                      common_available=len(common),
                      common_legacy_metric_error=stats([a['oracle_metric_error'] for a,b in common]),
                      common_balanced_metric_error=stats([b['oracle_metric_error'] for a,b in common]),
                      rescued_distances=sum(r['rescued_distances'] for r in rows),
                      originally_missing_distances=sum(r['legacy_missing_distances'] for r in rows))
        cells.append(dict(rho=rho,clouds=len(rows),methods=methods,paired=paired))
    high = cells[-1]; primary = audit['primary']; candidate = high['methods']['balanced64']
    def ge(a,b): return a is not None and a>=b
    gates = dict(availability_gain=ge(high['paired']['availability_gain'],primary['availability_gain_min']),
                 candidate_availability=ge(candidate['available']['fraction'],primary['balanced64_availability_min']),
                 cap_recall_gain=ge(high['paired']['recall_change']['mean'],primary['cap_recall_gain_min']))
    expected = {(rho,audit['test_seed_base']+100*i+j) for i,rho in enumerate(audit['densities']) for j in range(audit['test_replicates_per_density'])}
    actual = {(r['rho'],r['seed']) for r in records}
    complete = execution['mode']=='test' and execution['status']=='COMPLETE' and actual==expected and len(records)==len(expected)
    budget = execution['seconds']<=audit['wall_budget_seconds'] and execution['peak_mib']<=audit['memory_budget_mib']
    algebra = all(e.get('product_residual',0)<=cfg['gates']['algebra_absolute_tolerance'] and
                  e.get('affine_transform_residual',0)<=cfg['gates']['algebra_absolute_tolerance'] and
                  e.get('chart',{}).get('product_residual',0)<=cfg['gates']['algebra_absolute_tolerance'] and
                  e.get('operator',{}).get('constant',{}).get('value',0)==0
                  for r in records for e in r['evaluations'].values())
    relabels = sum(r['relabel_pass'] is True for r in records)
    decision = 'ANCHOR_COVERAGE_IMPROVED' if complete and budget and algebra and relabels==3 and all(gates.values()) else 'ANCHOR_SEARCH_HOLD'
    return dict(schema='x6.bk-anchor-audit-summary/1',decision=decision,phase3='HOLD_PHASE3',
                complete=complete,budget_pass=budget,algebra_pass=algebra,relabel_clouds_passed=relabels,
                primary_gates=gates,original_metric_limit=cfg['gates']['metric_relative_rmse'],
                high_density_metric_limit_met={name:(cell['oracle_metric_error']['rms'] is not None and cell['oracle_metric_error']['rms']<=cfg['gates']['metric_relative_rmse']) for name,cell in high['methods'].items()},
                cells=cells,source_commit=execution['source_commit'],seconds=execution['seconds'],peak_mib=execution['peak_mib'],
                caveats=['Paired cloud-level descriptive audit, not a convergence proof or external replication',
                         'Conditional metric RMS uses different available clouds; common subset also reported',
                         'Oracle cap retains noisy discrete shells and times; not an intrinsic method or lower bound',
                         'Known density, marked posets and 2+1 flat spacetime only; BD-C2 NO_GO unchanged'])


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('directory',type=Path)
    parser.add_argument('--output',type=Path); args=parser.parse_args()
    data=json.dumps(summarize(args.directory),indent=2,allow_nan=False)+'\n'
    if args.output: args.output.write_text(data)
    else: print(data)
