"""Cloud-block analysis of frozen methods; transfer fields are the primary endpoint."""
import hashlib
import json
import numpy as np
from mb_common import HERE, contract, write_json
from mb_model import ARMS


def load_rows():
    rows, executions = [], []
    for shard in [0,1]:
        folder = HERE/f'test-{shard}'
        e = json.loads((folder/'execution.json').read_text())
        executions.append(e)
        for item in e['records']:
            raw = (folder/item['file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==item['sha256']
            rows.append(json.loads(raw))
    return executions, sorted(rows,key=lambda r:r['seed'])


def moment_stats(errors):
    e = np.asarray(errors)
    return dict(rmse=float(np.sqrt(np.mean(e*e))),bias=float(e.mean()),
                centered_rms=float(np.sqrt(np.mean((e-e.mean())**2))))


def analyze(save=True):
    cfg = contract()
    raw = (HERE/'frozen_model.json').read_bytes()
    frozen = json.loads(raw)
    executions, rows = load_rows()
    assert all(e['calibration_sha256']==hashlib.sha256(raw).hexdigest() for e in executions)
    expected = list(range(cfg['test_seeds'][0],cfg['test_seeds'][1]+1))
    assert [r['seed'] for r in rows]==expected
    good = [r for r in rows if r['evaluation']['status']=='COMPLETE']
    assert good, 'No complete clouds: execution HOLD'
    clean = np.array([[np.array(f['clean'])-f['truth'] for f in r['evaluation']['fields']] for r in good])
    obs = np.array([[np.array(f['observed'])-f['truth'] for f in r['evaluation']['fields']] for r in good])
    prior = np.array([[f['prior_error'] for f in r['evaluation']['fields']] for r in good])
    noise = np.array([r['metadata_inference']['conditional_field_covariance'] for r in good])
    second = np.asarray(frozen['residual_second_moment'])
    rv = np.diagonal(noise+second,axis1=1,axis2=2)
    p = cfg['prior_sigma']**2
    gain = p/(p+rv)
    posterior = prior[:,:,None]+gain[:,None,:]*(obs-prior[:,:,None])
    post_var = p*rv/(p+rv)
    covered = np.abs(posterior)<=1.959963984540054*np.sqrt(post_var[:,None,:])
    ntrain = len(cfg['training_fields'])
    transfer = np.arange(ntrain,clean.shape[1])
    rng = np.random.default_rng(cfg['bootstrap_seed'])
    indices = rng.integers(0,len(good),size=(cfg['bootstrap_draws'],len(good)))
    out = dict(decision='METADATA_HOLD',scope=cfg['scope'],total=len(rows),complete=len(good),
               calibration_sha256=hashlib.sha256(raw).hexdigest(),groups={},comparisons={},
               execution=[{k:e[k] for k in ['shard','source_commit','status','seconds','peak_mib']} for e in executions])
    for group, ids in [('seen',np.arange(ntrain)),('transfer',transfer)]:
        stats = {}
        for j,name in enumerate(ARMS):
            c, o, po = clean[:,ids,j], obs[:,ids,j], posterior[:,ids,j]
            hits = covered[:,ids,j]
            coverage_draws = hits.mean(axis=1)[indices].mean(axis=1)
            stats[name] = dict(clean=moment_stats(c),observed=moment_stats(o),posterior=moment_stats(po),
                nominal_coverage=float(hits.mean()),coverage_hits=int(hits.sum()),
                field_responses=int(hits.size),independent_clouds=len(good),
                coverage_cloud_bootstrap_95=np.quantile(coverage_draws,[.025,.975]).tolist(),
                mean_noise_variance=float(noise[:,j,j].mean()),
                mean_gain=float(gain[:,j].mean()),mean_nees=float(np.mean(po**2/post_var[:,None,j])))
        out['groups'][group]=stats
    out['per_field']={f['name']:{name:dict(clean=moment_stats(clean[:,i,j]),
        posterior=moment_stats(posterior[:,i,j]),nominal_coverage=float(covered[:,i,j].mean()))
        for j,name in enumerate(ARMS)} for i,f in enumerate(good[0]['evaluation']['fields'])}
    for a,b in [('metadata','original'),('projected_metadata','projected'),
                ('metadata','constant_ablation'),('projected_metadata','projected_constant_ablation'),
                ('projected','original'),('projected_metadata','metadata')]:
        aa,bb=ARMS.index(a),ARMS.index(b)
        mse_a=np.mean(clean[:,transfer,aa]**2,axis=1)
        mse_b=np.mean(clean[:,transfer,bb]**2,axis=1)
        draws=np.sqrt(mse_a[indices].mean(axis=1)/mse_b[indices].mean(axis=1))
        ratios=[out['per_field'][f['name']][a]['clean']['rmse']/out['per_field'][f['name']][b]['clean']['rmse']
                for f in cfg['transfer_fields']]
        out['comparisons'][a+'_vs_'+b]=dict(clean_rmse_ratio=float(np.sqrt(mse_a.mean()/mse_b.mean())),
            paired_cloud_bootstrap_95=np.quantile(draws,[.025,.975]).tolist(),
            maximum_per_transfer_field_ratio=max(ratios),
            posterior_rmse_ratio=out['groups']['transfer'][a]['posterior']['rmse']/out['groups']['transfer'][b]['posterior']['rmse'])
    strata=np.searchsorted(frozen['noise_strata_edges'],noise[:,0,0],side='right')
    out['noise_strata'] = []
    for k in range(3):
        take=np.flatnonzero(strata==k)
        out['noise_strata'].append(dict(stratum=k,n_clouds=len(take),arms={name:dict(
            clean=moment_stats(clean[take][:,transfer,j]),
            nominal_coverage=float(covered[take][:,transfer,j].mean())) for j,name in enumerate(ARMS)} if len(take) else {}))
    out['diagnostics']={name:dict(ood_clouds=sum(r['metadata_inference']['diagnostics'][name]['ood'] for r in good),
        clipped_clouds=sum(r['metadata_inference']['diagnostics'][name]['clipped'] for r in good),
        null_unavailable=sum(not r['metadata_inference']['diagnostics'][name]['null_available'] for r in good),
        maximum_noise_ratio=max(r['metadata_inference']['diagnostics'][name]['noise_ratio'] for r in good))
        for name in ['metadata','projected_metadata','constant_ablation','projected_constant_ablation']}
    out['relations']=dict(before_failed=sum(not r['intrinsic']['before']['passed'] for r in good),
                         after_failed=sum(not r['intrinsic']['projection']['after']['passed'] for r in good),
                         pairs=sum(r['intrinsic']['before']['pairs'] for r in good))
    out['all_clouds_with_prior_fallback_rmse']={}
    completed={r['seed']:i for i,r in enumerate(good)}
    for j,name in enumerate(ARMS):
        errors=[]
        for r in rows:
            if r['seed'] in completed:
                errors.extend(posterior[completed[r['seed']],transfer,j])
            else:
                errors.extend(float(np.random.default_rng(np.random.SeedSequence([r['seed'],702302,int(i)])).normal(
                    scale=cfg['prior_sigma'])) for i in transfer)
        out['all_clouds_with_prior_fallback_rmse'][name]=float(np.sqrt(np.mean(np.array(errors)**2)))
    gates=dict(execution_complete=all(e['status']=='COMPLETE' for e in executions),
        budgets=all(e['seconds']<=cfg['wall_budget_seconds_per_shard'] and e['peak_mib']<=cfg['memory_budget_mib_per_shard'] for e in executions),
        availability=len(good)>=cfg['minimum_test_complete'],
        accepted_relations_exact=out['relations']['after_failed']==0,
        noise_cap=all(v['maximum_noise_ratio']<=cfg['maximum_noise_variance_ratio']+1e-7 for v in out['diagnostics'].values()))
    for a,b,ablation in [('metadata','original','constant_ablation'),('projected_metadata','projected','projected_constant_ablation')]:
        cmp=out['comparisons'][a+'_vs_'+b]
        gates[a+'_improvement']=cmp['clean_rmse_ratio']<=cfg['required_clean_rmse_ratio']
        gates[a+'_bootstrap']=cmp['paired_cloud_bootstrap_95'][1]<1
        gates[a+'_field_guard']=cmp['maximum_per_transfer_field_ratio']<=cfg['maximum_per_transfer_field_ratio']
        gates[a+'_posterior_guard']=cmp['posterior_rmse_ratio']<=cfg['maximum_posterior_rmse_ratio']
        gates[a+'_coverage']=out['groups']['transfer'][a]['nominal_coverage']>=cfg['minimum_nominal_coverage']
        gates[a+'_ablation']=out['comparisons'][a+'_vs_'+ablation]['clean_rmse_ratio']<=1
    out['gates']=gates
    if all(gates.values()):
        out['decision']='METADATA_PILOT_SUPPORTED'
    if save:
        write_json(HERE/'summary.json',out)
    return out


if __name__=='__main__':
    out=analyze()
    print(json.dumps({k:out[k] for k in ['decision','complete','comparisons','diagnostics','gates']},indent=2))
