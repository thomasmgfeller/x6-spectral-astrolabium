"""Prespecified feasibility and weight-mass gates; no polynomial fit scoring."""
import argparse
import json
from pathlib import Path
from feas_common import config
from volume_analysis import load,rms
from moment_analysis import stats
from feasibility import validate_record

def summarize(directory):
    contract,_=config();e,rows=load(directory);mode=e['mode']
    expected=[(rho,seed) for i,rho in enumerate(contract['densities']) for seed in
              (contract['development_seeds'] if mode=='development' else [contract['test_seed_base']+100*i+j for j in range(contract['test_replicates_per_density'])])]
    complete=e['status']=='COMPLETE' and [(r['rho'],r['seed']) for r in rows]==expected
    budget=e['seconds']<=contract['wall_budget_seconds'] and e['peak_mib']<=contract['memory_budget_mib']
    valid=all(validate_record(r,contract) for r in rows)
    algebra=e['controls']['status']=='PASS_SOFTWARE_CONTROLS' and all(
        (r['cloud_controls'] is None or r['cloud_controls']['status']=='PASS') and all(
            v['status']!='FEASIBLE' or v['reconstructed']['algebra_pass'] for s in r['supports'].values() for v in s.get('policies',{}).values()) for r in rows)
    cells=[];unresolved=0
    for rho in contract['densities']:
        group=[r for r in rows if r['rho']==rho];supports={}
        for name in contract['supports']:
            usable=[r['supports'][name] for r in group if r['supports'][name]['status']=='ok'];policies={}
            for policy in contract['policies']:
                values=[s['policies'][policy] for s in usable];feasible=[v for v in values if v['status']=='FEASIBLE']
                counts={status:sum(v['status']==status for v in values) for status in ['FEASIBLE','INFEASIBLE','UNRESOLVED']}
                unresolved+=counts['UNRESOLVED'];bounded=sum(v['mass_ratio']<=contract['maximum_mass_ratio'] for v in feasible)
                policies[policy]=dict(counts=counts,unavailable=len(group)-len(usable),total=len(group),
                    feasible_fraction=len(feasible)/len(group) if group else 0,
                    bounded_mass_count=bounded,bounded_mass_fraction=bounded/len(group) if group else 0,
                    minimum_mass=stats([v['minimum_mass'] for v in feasible]),mass_ratio=stats([v['mass_ratio'] for v in feasible]),
                    maximum_mass_ratio=max((v['mass_ratio'] for v in feasible),default=None),
                    full_rank_count=sum(v['rank']==9 for v in values))
            supports[name]=dict(available=len(usable),total=len(group),policies=policies,
                baseline_metric_rms=rms([u['baseline_evaluation']['metric_error'] for u in usable]),
                baseline_affine_rms=rms([u['baseline_evaluation']['affine_drift'] for u in usable]),
                baseline_mass=stats([u['baseline_mass'] for u in usable]),
                support_count=stats([u['support_count'] for u in usable]),
                maximum_scaled_distance=stats([u['maximum_scaled_distance'] for u in usable]))
        transitions={}
        comparisons=[('caps','fixed_time','caps','free_time'),('caps','fixed_time','caps','unrestricted'),
                     ('caps','fixed_time','full_shells','fixed_time')]
        for fs,fp,ts,tp in comparisons:
            table={}
            for r in group:
                a=r['supports'][fs].get('policies',{}).get(fp,{}).get('status','UNAVAILABLE')
                b=r['supports'][ts].get('policies',{}).get(tp,{}).get('status','UNAVAILABLE')
                key=a+' -> '+b;table[key]=table.get(key,0)+1
            transitions[fs+'/'+fp+' to '+ts+'/'+tp]=table
        cells.append(dict(rho=rho,supports=supports,paired_transitions=transitions))
    primary=next(c for c in cells if c['rho']==contract['primary_density'])['supports'][contract['primary_support']]['policies'][contract['primary_policy']]
    gates=dict(feasible_fraction=primary['feasible_fraction']>=contract['minimum_feasible_fraction'],
               bounded_mass_fraction=primary['bounded_mass_fraction']>=contract['minimum_bounded_mass_fraction'],
               all_available_resolved=unresolved==0)
    passed=complete and budget and valid and algebra and all(gates.values())
    return dict(schema='x6.bk-moment-feasibility-summary/1',mode=mode,complete=complete,budget_pass=budget,
        certificates_pass=valid,algebra_pass=algebra,clouds=len(rows),cells=cells,primary_gates=gates,
        decision=('CAP_MOMENT_FEASIBILITY_SUPPORTED' if passed else 'CAP_MOMENT_FEASIBILITY_HOLD') if mode=='test' else 'DEVELOPMENT_ONLY',
        phase3='HOLD_PHASE3',note='Coordinate-assisted feasibility only. Fitted moments are constraints, not independent metric validation. Nonunique witnesses are not preferred operators.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();s=summarize(a.directory)
    (a.directory/'summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
