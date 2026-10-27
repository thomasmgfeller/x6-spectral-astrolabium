"""Run the frozen 4D Poisson campaign; all unavailable outcomes retained."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,platform,time
import numpy as np
import scipy
from scipy.stats import beta,poisson,kstest,chi2
import model as m

ROOT=Path(__file__).resolve().parent

def tail(k,mu):
    return np.minimum(1,2*np.minimum(poisson.cdf(k,mu),poisson.sf(k-1,mu)))

def cp_lower(k,n,alpha):
    return 0. if k==0 else float(beta.ppf(alpha,k,n-k+1))

def score(rec,true_tau):
    err=np.abs(rec['tau']/true_tau-1)
    good=rec['valid']&rec['count_eligible']&(err<=.1)
    vals=err[np.isfinite(err)]
    return good,{'valid':int(rec['valid'].sum()),'count_eligible':int(rec['count_eligible'].sum()),
                 'success_10pct':int(good.sum()),
                 'conditional_relative_rmse':float(np.sqrt(np.mean(vals**2))) if len(vals) else None,
                 'conditional_median_relative_abs_error':float(np.median(vals)) if len(vals) else None}

def controls(protocol,geos):
    rng=np.random.Generator(np.random.PCG64(protocol['sampler_check_seed']))
    pts=m.sample_diamond(rng,protocol['sampler_check']['points'],[-1,0,0,0],[1,0,0,0])
    r=np.linalg.norm(pts[:,1:],axis=1); t=pts[:,0]
    u=1-(1-abs(t))**4; v=(r/(1-abs(t)))**3; z=(pts[:,3]/r+1)/2
    tests={name:float(kstest(values,'uniform').pvalue) for name,values in zip(protocol['sampler_check']['tests'],[u,v,z])}
    inside=bool(np.all(abs(t)+r<1+1e-13))
    direct=[]; raw=[]; ctrl=protocol['direct_cloud_check']
    for gi,g in enumerate(geos[:4]):
        a=m.arrays(g); points=np.array([[float(F(x)) for x in p] for p in g['points']])
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([protocol['direct_cloud_seed'],gi])))
        samples=[]
        for repeat in range(ctrl['replicates']):
            n=rng.poisson(ctrl['outer_expected_count'])
            cloud=m.sample_diamond(rng,n,points[0],points[-1])
            c=m.cloud_counts(cloud,points)
            assert c[m.INDEX[(0,6)]]==n
            samples.append(c)
        samples=np.array(samples); raw.append(samples)
        mu=ctrl['outer_expected_count']*a['volume_ratios']
        pv=tail(samples.sum(axis=0),ctrl['replicates']*mu)
        direct.append({'geometry':g['id'],'min_marginal_p':float(pv.min()),
                       'simulated_points':int(samples[:,m.INDEX[(0,6)]].sum())})
    np.savez_compressed(ROOT/'direct_cloud_counts.npz',counts=np.array(raw))
    # Full input mask blindness: target-target count must never alter either result.
    a=m.arrays(geos[0]); rho=65536/(np.pi/24*float(F(geos[0]['outer_W'])))
    c=np.maximum(1,np.rint(65536*a['volume_ratios'])).astype(np.int64)[None,:]
    rr=m.reconstruct(c,rho); uu=m.uncertainty(c,rho,rr)
    changed=c.copy(); changed[:,m.INDEX[(5,6)]]+=10000000
    rr2=m.reconstruct(changed,rho); uu2=m.uncertainty(changed,rho,rr2)
    blind=all(np.array_equal(rr[k],rr2[k],equal_nan=True) for k in ['tau','tau2','valid','G','d'])
    blind &= all(np.array_equal(uu[k],uu2[k],equal_nan=True) for k in ['lo','hi','certificate_10pct'])
    exact_errors=[]
    for g in geos:
        a=m.arrays(g); G,d=m.build_system(a['signed_intervals'][None,:]); q=-d[0]@np.linalg.solve(G[0],d[0])
        exact_errors.append(abs(q/float(F(g['tau_squared']))-1))
    assert max(exact_errors)<1e-9
    assert blind
    sample_pass=inside and min(tests.values())>=protocol['sampler_check']['family_alpha']/3
    direct_pass=min(d['min_marginal_p'] for d in direct)>=ctrl['family_alpha']/(4*21)
    return {'sampler_p_values':tests,'sampler_inside':inside,'sampler_gate_pass':sample_pass,
            'direct_cloud_checks':direct,'direct_cloud_gate_pass':direct_pass,
            'withheld_target_count_blindness':blind,'exact_input_max_relative_tau_squared_error':max(exact_errors),
            'exact_covariance_identities':len(geos)*441}

def main():
    start=time.monotonic(); freeze=json.loads((ROOT/'FREEZE.json').read_text())
    for name,h in freeze['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
    p=json.loads((ROOT/'PROTOCOL.json').read_text()); geos=json.loads((ROOT/'geometries.json').read_text())
    checks=controls(p,geos)
    assert checks['sampler_gate_pass'] and checks['direct_cloud_gate_pass']
    print('Independent direct-cloud and sampler controls passed.',flush=True)
    reps=p['replicates_per_geometry_per_density']; records=[]; allcounts=[]; alliid=[]; allmetrics=[]; allbounds=[]
    minp=1.; covstats=[]; margtests=0
    for level,budget in enumerate(p['outer_expected_counts']):
        for gi,g in enumerate(geos):
            a=m.arrays(g); rho=budget/(np.pi/24*float(F(g['outer_W'])))
            rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi,0])))
            atoms=rng.poisson(budget*a['atom_ratios'],size=(reps,21))
            counts=atoms@m.B.T
            rngi=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi,1])))
            iid=rngi.poisson(budget*a['volume_ratios'],size=(reps,21))
            rec=m.reconstruct(counts,rho); oracle=m.reconstruct(counts,rho,a['signed_intervals']); wrong=m.reconstruct(iid,rho)
            true_tau=np.sqrt(float(F(g['tau_squared'])))
            good,sc=score(rec,true_tau); ogood,osc=score(oracle,true_tau); igood,isc=score(wrong,true_tau)
            unc=m.uncertainty(counts,rho,rec)
            means=budget*a['volume_ratios']
            mean_cover=np.all((means[m.PRED]>=unc['mean_low'])&(means[m.PRED]<=unc['mean_high']),axis=1)
            tau_cover=(unc['lo']<=true_tau)&(unc['hi']>=true_tau)
            # The mathematically sufficient bound must cover on every simultaneous-box event.
            assert np.all(tau_cover[mean_cover])
            cert=unc['certificate_10pct']
            assert not np.any(cert&mean_cover&(~(np.abs(rec['tau']/true_tau-1)<=.100000001)))
            pv=tail(counts.sum(axis=0),reps*means); minp=min(minp,float(pv.min())); margtests+=21
            j=m.INDEX[(5,6)]; direct=(24*counts[:,j]/(np.pi*rho))**.25
            direct_good=(counts[:,j]>=16)&(np.abs(direct/true_tau-1)<=.1)
            covpair=[m.INDEX[(0,3)],m.INDEX[(0,6)]]
            sx=(counts[:,covpair]-means[covpair])/np.sqrt(means[covpair])
            si=(iid[:,covpair]-means[covpair])/np.sqrt(means[covpair])
            covstats.append({'primary_standardized_product_sum':float(np.prod(sx,axis=1).sum()),
                             'iid_standardized_product_sum':float(np.prod(si,axis=1).sum()),
                             'expected_product':float(np.sqrt(means[covpair[0]]/means[covpair[1]])),
                             'product_variance':float(1+means[covpair[0]]/means[covpair[1]]+1/means[covpair[1]]),
                             'replicates':reps})
            record={'geometry':g['id'],'family':g['family'],'kind':g['kind'],'epsilon':g['epsilon'],
                    'level':level,'outer_expected_count':budget,'rho':rho,'replicates':reps,
                    'smallest_expected_input_count':float(means[m.PRED].min()),
                    'true_tau':true_tau,'primary':sc,'oracle_anchor_diagnostic':osc,'iid_negative_control':isc,
                    'direct_count_success_10pct':int(direct_good.sum()),
                    'simultaneous_mean_box_coverage':int(mean_cover.sum()),
                    'tau_interval_coverage':int(tau_cover.sum()),'finite_tau_intervals':int(unc['finite'].sum()),
                    'certificate_10pct':int(cert.sum()),
                    'primary_success_cp_lower':cp_lower(int(good.sum()),reps,.05/len(geos)),
                    'certificate_cp_lower':cp_lower(int(cert.sum()),reps,.05/len(geos))}
            records.append(record); allcounts.append(counts); alliid.append(iid)
            allmetrics.append(np.column_stack([rec['tau'],rec['valid'],rec['count_eligible'],good,oracle['tau'],wrong['tau'],direct]))
            allbounds.append(np.column_stack([unc['lo'],unc['hi'],cert,mean_cover,tau_cover,unc['perturbation_ratio']]))
        current=[r for r in records if r['level']==level]
        print(json.dumps({'budget':budget,'success':sum(r['primary']['success_10pct'] for r in current),
                          'total':reps*len(geos),'finite_intervals':sum(r['finite_tau_intervals'] for r in current),
                          'certificates':sum(r['certificate_10pct'] for r in current)}),flush=True)
    checks['marginal_count_checks']={'tests':margtests,'min_p':minp,'threshold':p['marginal_count_check']['family_alpha']/margtests,
                                     'pass':minp>=p['marginal_count_check']['family_alpha']/margtests}
    N=sum(x['replicates'] for x in covstats)
    expected=sum(x['expected_product']*x['replicates'] for x in covstats)/N
    actual=sum(x['primary_standardized_product_sum'] for x in covstats)/N
    negative=sum(x['iid_standardized_product_sum'] for x in covstats)/N
    se=np.sqrt(sum(x['product_variance']*x['replicates'] for x in covstats))/N
    checks['nested_count_covariance']={'theory_standardized_product':expected,'observed':actual,
                                      'standard_error_known_model':se,'z_diagnostic':(actual-expected)/se,
                                      'independent_marginals_observed':negative,'independent_marginals_theory':0}
    primary=[r for r in records if r['level']==p['primary_density_index']]
    report={'version':'0.2','date':'2026-10-27','scope':p['scope'],
            'accuracy_gate_pass':all(r['primary_success_cp_lower']>=.9 for r in primary),
            'uncertainty_gate_pass':all(r['certificate_cp_lower']>=.9 for r in primary),
            'primary_count_vectors':N,'geometries':len(geos),'direct_cloud_replicates':1024,
            'controls':checks,'records':records,'runtime_seconds':time.monotonic()-start,
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'source_freeze_sha256':hashlib.sha256((ROOT/'FREEZE.json').read_bytes()).hexdigest()}
    np.savez_compressed(ROOT/'campaign_arrays.npz',counts=np.array(allcounts),iid_negative=np.array(alliid),
                        metrics=np.array(allmetrics),bounds=np.array(allbounds))
    (ROOT/'RESULTS.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ['accuracy_gate_pass','uncertainty_gate_pass','primary_count_vectors','runtime_seconds']}),flush=True)

if __name__=='__main__':main()
