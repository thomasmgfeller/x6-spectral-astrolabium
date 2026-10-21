"""SPDX-License-Identifier: Apache-2.0
Truth-side diagnostics only, called after the inference has been sealed.
"""
import math
import numpy as np
from scipy.stats import norm, chi2
from ec_common import cfg, sha


def field_values(delta,spec):
    k=np.asarray(spec['k'])
    trig=np.cos if spec['kind']=='cos' else np.sin
    root=float(trig(spec['phase']))
    contrast=trig(np.asarray(delta)@k+spec['phase'])-root
    truth=float((k[0]**2-k[1]**2-k[2]**2)*root)
    return contrast,truth


def geometry(points,estimate,order):
    """Separate Lorentz-invariant Gram, proper-time and causal-label errors."""
    p=np.asarray(points); x=np.asarray(estimate); order=np.asarray(order,bool)
    eta=np.array([-1.,1.,1.])
    true_gram=(p*eta)@p.T; estimated_gram=(x*eta)@x.T
    true_relations=[]; predicted=[]; time_errors=[]
    for i in range(len(p)):
        for j in range(len(p)):
            dt,dx,dy=(p[j]-p[i]).tolist()
            tt=dt*dt-math.fsum([dx*dx,dy*dy])
            actual=dt>0 and tt>0
            assert actual==bool(order[i,j])
            dt,dx,dy=(x[j]-x[i]).tolist()
            xx=dt*dt-math.fsum([dx*dx,dy*dy])
            inferred=dt>0 and xx>0
            true_relations.append(actual); predicted.append(inferred)
            if actual:
                time_errors.append((math.sqrt(max(0.,xx))-math.sqrt(tt))/cfg()['outer_duration'])
    a=np.array(true_relations);b=np.array(predicted)
    return dict(gram_relative_error=float(np.linalg.norm(estimated_gram-true_gram)/max(np.linalg.norm(true_gram),1e-15)),
                missing_relations=int(np.count_nonzero(a & ~b)),extra_relations=int(np.count_nonzero(b & ~a)),
                causal_pairs=int(a.sum()),ordered_pairs=len(p)*(len(p)-1),
                proper_time_errors=time_errors,
                proper_time_rmse=float(np.sqrt(np.mean(np.square(time_errors)))))


def noise_bank(full,key,field):
    c=cfg(); rng=np.random.default_rng(np.random.SeedSequence([key,field,70321021]))
    inputs=rng.normal(scale=c['field_noise_sigma'],size=(c['noise_repetitions']+1,full.shape[1]))
    outputs=inputs@full.T
    repeats=outputs[:-1]
    return dict(input_sha256=sha(inputs.astype('<f8').tobytes()),
                output_sha256=sha(outputs.astype('<f8').tobytes()),
                mean=repeats.mean(axis=0).tolist(),
                covariance=np.cov(repeats,rowvar=False,ddof=1).tolist(),
                second=(repeats.T@repeats/len(repeats)).tolist(),
                holdout=outputs[-1].tolist())


def evaluate(row,z,prepared,key):
    if prepared['status']!='COMPLETE':return dict(status=prepared['status'])
    selected=row['selection']['selected']; ids=[selected['root']]+selected['support']
    points=z[ids]-z[selected['root']]
    full=np.asarray(prepared['full_coefficients'])[:4]
    noise=cfg()['field_noise_sigma']**2*(full@full.T)
    fields=[]
    for i,spec in enumerate(cfg()['fields']):
        contrast,truth=field_values(points[1:],spec)
        clean=full[:,1:]@contrast
        independent=np.array([math.fsum(float(a)*float(b) for a,b in zip(v,contrast)) for v in full[:,1:]])
        np.testing.assert_allclose(clean,independent,atol=1e-8,rtol=1e-7)
        bank=noise_bank(full,key,i)
        fields.append(dict(name=spec['name'],truth=truth,clean=clean.tolist(),
            error=(clean-truth).tolist(),observed=(clean+bank['holdout']).tolist(),noise=bank))
    metrics={}
    for name,features in [('original',row['intrinsic']['original_features']),
                          ('projected',row['intrinsic']['projection']['features'])]:
        x=np.vstack((np.zeros(3),np.asarray(features)*prepared['scale']))
        metrics[name]=geometry(points,x,row['observed_order'])
    return dict(status='COMPLETE',true_support_points=points.tolist(),
                full_coefficients=full.tolist(),conditional_noise_covariance=noise.tolist(),
                geometry=metrics,fields=fields)


def directions():
    out=[(f'arm-{i}',np.eye(4)[i]) for i in range(4)]
    for i in range(4):
        for j in range(i+1,4):
            for sign,label in [(1,'sum'),(-1,'difference')]:
                out.append((f'{label}-{i}-{j}',(np.eye(4)[i]+sign*np.eye(4)[j])/math.sqrt(2)))
    assert len(out)==16
    return out


def noise_tests(bank,covariance):
    n=cfg()['noise_repetitions']; mean=np.asarray(bank['mean']); sample=np.asarray(bank['covariance'])
    predicted=np.asarray(covariance); out=[]
    scale=max(float(np.max(np.diag(predicted))),1e-30)
    for name,v in directions():
        variance=float(v@predicted@v); s2=max(0.,float(v@sample@v)); mu=float(v@mean)
        if variance<=1e-12*scale:
            # Algebraically duplicate arms: an explicitly recorded deterministic check.
            out.append(dict(direction=name,degenerate=True,mean=mu,variance=s2,
                            passed=abs(mu)<=1e-8 and s2<=1e-10*scale))
            continue
        z=mu/math.sqrt(variance/n); q=(n-1)*s2/variance
        out.append(dict(direction=name,degenerate=False,mean_z=z,variance_ratio=s2/variance,
            mean_p=float(2*norm.sf(abs(z))),variance_p=float(min(1.,2*min(chi2.cdf(q,n-1),chi2.sf(q,n-1))))))
    return out
