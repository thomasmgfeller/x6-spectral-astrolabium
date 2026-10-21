"""SPDX-License-Identifier: Apache-2.0"""
import json
import numpy as np
from ca_common import HERE,cfg,load_results,write
from gu_analyze import stats

def summarize(rows):
    good=[r for r in rows if r['evaluation']['status']=='COMPLETE'];variants={}
    for name in cfg()['references']+cfg()['candidates']:
        a=[r['evaluation']['variants'][name] for r in good]
        variants[name]=dict(rmse=float(np.sqrt(np.mean([x['mse'] for x in a]))),
            mse_change=float(np.mean([x['mse_change'] for x in a])),cross_term=float(np.mean([x['cross_term'] for x in a])),
            step_squared=float(np.mean([x['step_squared'] for x in a])),
            groups={g:dict(rmse=float(np.sqrt(np.mean([x['groups'][g]['mse'] for x in a if g in x['groups']]))),
                cross_term=float(np.mean([x['groups'][g]['cross_term'] for x in a if g in x['groups']])),
                step_squared=float(np.mean([x['groups'][g]['step_squared'] for x in a if g in x['groups']]))) for g in ['root','support_spacelike','support_causal']},
            fallbacks=sum(x['fallback'] for x in a),order_violations=sum(not x['order']['passed'] for x in a),
            covariance_condition=stats([x['covariance_condition'] for x in a]),
            scale_step_amplitude=stats([x['scale_step_amplitude'] for x in a]),
            scale_step_energy_fraction=stats([x['scale_step_energy_fraction'] for x in a]))
    for x in variants.values():
        x['ratio_to_baseline']=x['rmse']/variants['baseline']['rmse'];x['ratio_to_diagonal']=x['rmse']/variants['diagonal']['rmse']
        x['ratio_to_full']=x['rmse']/variants['full']['rmse']
    return dict(attempts=len(rows),complete=len(good),abstentions=len(rows)-len(good),variants=variants,
        spectral={b:stats([r['evaluation']['spectral'][b]['mean_standardized_square'] for r in good]) for b in ['lowest_quarter','middle_half','highest_quarter']},
        correlation_condition=stats([r['evaluation']['correlation_condition'] for r in good]),
        signed_scale_precision_attenuation=stats([r['evaluation']['signed_scale_precision_attenuation'] for r in good]),
        maximum_rank_one_identity_error=max(r['evaluation']['rank_one_identity_error'] for r in good))

def select(blocks,pooled):
    c=cfg();eligibility={}
    for name in c['candidates']:
        gates={}
        for phase,p in blocks.items():
            v=p['variants'][name];base=p['variants']['baseline']
            gates[phase]=dict(minimum_complete=p['complete']>=c['minimum_complete_per_historical_block'],
                practical_improvement=v['ratio_to_baseline']<=c['maximum_rmse_ratio_to_baseline'],
                no_worse_than_diagonal=v['ratio_to_diagonal']<=c['maximum_rmse_ratio_to_diagonal'],
                group_noninferiority=all(v['groups'][g]['rmse']/base['groups'][g]['rmse']<=c['maximum_group_rmse_ratio'] for g in base['groups']),
                exact_order=v['order_violations']==0,acceptable_fallbacks=v['fallbacks']/p['complete']<=c['maximum_fallback_rate'])
        eligibility[name]=dict(passed=all(all(g.values()) for g in gates.values()),gates=gates)
    eligible=[n for n in c['candidates'] if eligibility[n]['passed']]
    def lowest(names):
        best=min(pooled['variants'][n]['rmse'] for n in names)
        return next(n for n in names if pooled['variants'][n]['rmse']<=best+1e-12)
    return dict(eligibility=eligibility,eligible=eligible,selected=lowest(eligible) if eligible else None,
        lowest_descriptive_rmse=lowest(c['candidates']),
        decision='PROCEED_TO_FRESH_CONFIRMATION' if eligible else 'STOP_CORRELATION_CORRECTION_SCREEN')

def analyze(rows):
    blocks={phase:summarize([r for r in rows if r['historical_phase']==phase]) for phase in ['calibration','test']}
    pooled=summarize(rows);selection=select(blocks,pooled)
    return dict(execution='DIAGNOSTIC_COMPLETE',decision=selection['decision'],selection=selection,
        historical_blocks=blocks,pooled_development=pooled,new_simulations=0,
        holds=['HOLD_BATCH_CORRECTION','HOLD_EMBEDDING_COVARIANCE','HOLD_KALMAN','HOLD_PHASE3','METADATA_HOLD'],
        interpretation='All PR78 observations, including its old test set, are reused development data. Ablations are descriptive and not independent validation. No candidate is released by this screen.')
def main():
    executions,rows=load_results();assert len(rows)==cfg()['historical_attempts'] and all(e['status']=='COMPLETE' for e in executions)
    s=analyze(rows);write(HERE/'results/summary.json',s)
    print(json.dumps(dict(decision=s['decision'],selection=s['selection'],pooled_ratios={n:v['ratio_to_baseline'] for n,v in s['pooled_development']['variants'].items()})))
if __name__=='__main__':main()
