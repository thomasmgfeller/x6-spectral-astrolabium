"""Run the frozen synthetic control experiment and assigned-PDF GUM study."""
import hashlib,json,platform,sys
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import binom
from scipy.optimize import brentq
from model import coherence,scaled_kvf
from gum import evaluate,interval


def save(path,obj):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')


def run():
    contract=json.loads(Path('CONTRACT.json').read_text())
    for line in Path('FREEZE.sha256').read_text().splitlines():
        sha,name=line.split(None,1)
        if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=sha:
            raise ValueError('freeze mismatch '+name)
    cert=json.loads(Path('records/certificate.json').read_text())
    n,k=cert['decision']['pairs'],cert['decision']['threshold']
    p0,p1=float(cert['decision']['p0_lower']),float(cert['decision']['p1_upper'])
    rhos=[[coherence(m,r) for r in [1,2,3]] for m in [0,.5]]
    Path('raw').mkdir(exist_ok=True)
    records=[]
    for i,mass in enumerate([0.,.5]):
        arrays=[]
        rng=np.random.default_rng(contract['raw_seeds'][i])
        for j,rho in enumerate(rhos[i]):
            # Equivalent construction from independent field and detector-noise Gaussians.
            field=rng.standard_normal((n,2))@np.linalg.cholesky([[1.,rho],[rho,1.]]).T
            noise=np.sqrt(.05)*rng.standard_normal((n,2))
            xy=field+noise
            np.save(f'raw/M{i}_R{j+1}.npy',xy,allow_pickle=False)
            arrays.append(xy)
        same=int(np.count_nonzero(arrays[2][:,0]*arrays[2][:,1]>=0))
        record={'model':f'M{i}','nominal_coherence':rhos[i],
                'scaled_physical_kvf':[scaled_kvf(mass,r) for r in [1,2,3]],
                'same_sign_count_R3':same,'decision':'M0' if same>k else 'M1',
                'gum':evaluate(arrays,contract['gum_seeds'][i])}
        records.append(record)
        save(f'records/M{i}.json',record)
        print(f'M{i}: {same}/{n}, decision {record["decision"]}',flush=True)
    # Fresh independent replications at certified worst-case sign probabilities.
    trials=contract['endpoint_campaign_trials']
    rng=np.random.default_rng(contract['endpoint_campaign_seed'])
    counts0=rng.binomial(n,p0,size=trials)
    counts1=rng.binomial(n,p1,size=trials)
    np.save('raw/endpoint_counts_M0.npy',counts0,allow_pickle=False)
    np.save('raw/endpoint_counts_M1.npy',counts1,allow_pickle=False)
    errors0=int(np.count_nonzero(counts0<=k));errors1=int(np.count_nonzero(counts1>k))
    campaign={'trials_each':trials,'seed':contract['endpoint_campaign_seed'],
              'p0':p0,'p1':p1,'errors_M0':errors0,'errors_M1':errors1,
              'error_M0_99pct_interval':interval(errors0,trials),
              'error_M1_99pct_interval':interval(errors1,trials),
              'binomial_tail_M0':float(binom.cdf(k,n,p0)),
              'binomial_tail_M1':float(binom.sf(k,n,p1)),
              'scope':'synthetic Bernoulli endpoint campaign; Hoeffding bounds carry the conditional guarantee'}
    save('records/campaign.json',campaign)
    aliases=[]
    for j,r in enumerate([1,2,3]):
        delta=rhos[0][j]-rhos[1][j]
        noise0=np.diag([.1,.1]);noise1=np.array([[.1,delta],[delta,.1]])
        t0=np.array([[1,rhos[0][j]],[rhos[0][j],1]])+noise0
        t1=np.array([[1,rhos[1][j]],[rhos[1][j],1]])+noise1
        assert np.allclose(t0,t1,rtol=0,atol=2e-16)
        assert np.linalg.eigvalsh(noise1).min()>0
        aliases.append({'distance':r,'noise_covariance_M1':delta,
                        'minimum_noise_eigenvalue':float(np.linalg.eigvalsh(noise1).min()),
                        'same_observation_covariance':t0.tolist()})
    width_alias=brentq(lambda w:coherence(0,3,w)-rhos[1][2],.5,1)
    controls={'noise_alias':aliases,
              'noise_alias_scope':'setting-dependent correlated noise outside the frozen calibration bounds can make all three raw Gaussian pair laws identical',
              'single_setting_width_alias_massless_width':width_alias,
              'width_alias_scope':'matches massive nominal coherence only at R3; outside [0.98,1.02]',
              'identical_model_probability_gap':0.,
              'identical_model_status':'HOLD_IDENTIFIABILITY',
              'field_status':evaluate([],[],mode='FIELD'),
              'response_channel_status':'UNMEASURED; equal-time-centre commutator is zero by symmetry in both models'}
    save('records/controls.json',controls)
    save('records/environment.json',{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()})
    save('records/summary.json',{'status':'CONDITIONAL_SYNTHETIC_CONTROL_COMPLETE',
         'physical_release':'HOLD_FIELD_TRANSFER','quantum_gravity_evidence':False,
         'selected_distance':3,'pairs_per_setting':n,'settings':3,
         'total_pairs_per_model':3*n,'threshold':k,'decisions':[r['decision'] for r in records],
         'nominal_coherences':rhos,'certificate':'records/certificate.json',
         'joint_assigned_pdf_coverage_checks':[r['gum']['joint_region']['validation_interval_contains_target'] for r in records]})
    print(json.dumps(campaign,indent=2),flush=True)


if __name__=='__main__':run()
