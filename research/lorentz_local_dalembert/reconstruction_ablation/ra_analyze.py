"""SPDX-License-Identifier: Apache-2.0
Paired retrospective decomposition, including signed interactions.
"""
import numpy as np
from ra_common import cfg,close

ARMS=['original','metadata','projected','projected_metadata','oracle']


def component_stats(z,names):
    z=np.asarray(z);n=len(z);mu=z.mean(axis=0);c=z-mu
    second=np.einsum('nfi,nfj->fij',z,z)/n
    covariance=np.einsum('nfi,nfj->fij',c,c)/n
    close(second,covariance+mu[:,:,None]*mu[:,None,:])
    aggregate=second.mean(axis=0)
    direct=float(np.mean(z.sum(axis=2)**2));close(aggregate.sum(),direct)
    return dict(names=names,mean_per_field=mu.tolist(),covariance_per_field=covariance.tolist(),
        second_moment_per_field=second.tolist(),aggregate_second_moment=aggregate.tolist(),
        squared_terms={name:float(aggregate[i,i]) for i,name in enumerate(names)},
        signed_cross_terms={names[i]+' x '+names[j]:float(2*aggregate[i,j]) for i in range(len(names)) for j in range(i+1,len(names))},
        mse_sum=float(aggregate.sum()),direct_mse=direct,identity_residual=float(aggregate.sum()-direct))


def analyze(records,execution):
    output={}
    for phase_index,phase in enumerate(cfg()['phases']):
        all_rows=[r for r in records if r['phase']==phase]
        good=[r for r in all_rows if r['status']=='COMPLETE'];n=len(good)
        assert n>1
        errors=np.array([[f['errors'] for f in r['fields']] for r in good])
        components=np.array([[f['taylor'] for f in r['fields']] for r in good])
        d=errors[:,:,4]
        losses=np.mean(errors*errors,axis=1)
        rng=np.random.default_rng(cfg()['bootstrap_seed']+phase_index)
        samples=rng.integers(0,n,size=(cfg()['bootstrap_replicates'],n))
        boots=losses[samples].mean(axis=1)
        primary={};metadata={}
        for label,i,mi in [('original',0,1),('projected',2,3)]:
            r=errors[:,:,i]-d;c=errors[:,:,mi]-errors[:,:,i]
            stats=component_stats(np.stack((d,r),axis=2),['discretization','reconstruction'])
            close(stats['direct_mse'],np.mean(errors[:,:,i]**2))
            ratio=float(np.sqrt(losses[:,4].mean()/losses[:,i].mean()))
            interval=np.quantile(np.sqrt(boots[:,4]/boots[:,i]),[.025,.975]).tolist()
            stats.update(oracle_to_actual_rmse_ratio=ratio,paired_cloud_bootstrap_95=interval,
                descriptive_geometric_leverage=ratio<cfg()['oracle_rmse_ratio_screen'] and interval[1]<1,
                reconstruction_rms=float(np.sqrt(np.mean(r*r))),
                cross_fraction_of_actual_mse=sum(stats['signed_cross_terms'].values())/stats['direct_mse'])
            primary[label]=stats
            v=component_stats(np.stack((d,r,c),axis=2),['discretization','reconstruction','metadata_increment'])
            close(v['direct_mse'],np.mean(errors[:,:,mi]**2));metadata[ARMS[mi]]=v
        arm_summary={}
        for i,label in enumerate(ARMS):
            arm_summary[label]=dict(rmse=float(np.sqrt(losses[:,i].mean())),
                per_field_rmse=np.sqrt(np.mean(errors[:,:,i]**2,axis=0)).tolist(),
                mean_error_per_field=errors[:,:,i].mean(axis=0).tolist(),
                paired_cloud_bootstrap_rmse_95=np.sqrt(np.quantile(boots[:,i],[.025,.975])).tolist(),
                mean_hypothetical_iid_variance=float(np.mean([r['hypothetical_iid_variance'][i] for r in good])))
        moment=np.array([r['physical_moment_residuals'] for r in good])
        output[phase]=dict(scheduled=len(all_rows),paired_complete=n,
            original_complete=sum(r['input_status']=='COMPLETE' for r in all_rows),
            unavailable=[dict(index=r['index'],seed=r['seed'],status=r['status'],reason=r.get('reason',r.get('oracle',{}).get('reason'))) for r in all_rows if r['status']!='COMPLETE'],
            arms=arm_summary,primary=primary,metadata=metadata,
            taylor={label:component_stats(components[:,:,i,:],['linear','quadratic','higher_order']) for i,label in enumerate(ARMS)},
            max_physical_linear_moment_error={label:float(np.max(np.abs(moment[:,i,:3]))) for i,label in enumerate(ARMS)},
            max_physical_quadratic_moment_error={label:float(np.max(np.abs(moment[:,i,3:]))) for i,label in enumerate(ARMS)},
            oracle_condition_range=[min(r['oracle']['condition'] for r in good),max(r['oracle']['condition'] for r in good)])
    complete=all(v['scheduled']==cfg()['expected_clouds_per_phase'] and v['paired_complete']==v['original_complete'] for v in output.values())
    budget=execution['status']=='COMPLETE' and execution['seconds']<=cfg()['wall_budget_seconds'] and execution['peak_mib']<=cfg()['memory_budget_mib']
    return dict(schema='x6.reconstruction-ablation-results/1',
        decision='DECOMPOSITION_VERIFIED' if complete and budget else 'DECOMPOSITION_HOLD',
        execution_within_budget=budget,primary_phase=cfg()['primary_phase'],phases=output,
        holds=cfg()['unchanged'],
        limits=['Retrospective reused clouds; bootstrap intervals are descriptive and not simultaneous.',
                'Oracle uses hidden true geometry; it is not an available estimator or universal lower bound.',
                'Fixed supports and one density: no support-selection ablation or asymptotic convergence proof.',
                'Signed interactions prevent an independent positive-percentage allocation.',
                'Noise-free diagnostic; hypothetical IID variances are reported separately without new noise experiments.'])
