"""SPDX-License-Identifier: Apache-2.0
Batch invariant geometry correction. No true coordinates or field observations.
"""
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
from gc_common import cfg,matrices,covariance,intervals,order_check,constraints

ETA=np.array([-1.,1.,1.])

def canonical(features,order):
    """Fix the Lorentz gauge using the root Gram matrix; retain time orientation."""
    x=np.asarray(features);G=(x*ETA)@x.T
    values,vectors=np.linalg.eigh(G)
    scale=max(1.,float(np.max(abs(values))))
    if not(values[0]<-1e-10*scale and values[-2]>1e-10*scale):
        raise ValueError('degenerate root Gram signature')
    z=np.column_stack((vectors[:,0]*np.sqrt(-values[0]),
        vectors[:,-2]*np.sqrt(values[-2]),vectors[:,-1]*np.sqrt(values[-1])))
    p=np.vstack((np.zeros(3),z));r=np.asarray(order,bool);i,j=np.where(r)
    if len(i)==0:raise ValueError('no causal direction for time orientation')
    if np.sum(p[j,0]-p[i,0])<0:p[:,0]*=-1
    if not order_check(p,r)['passed']:raise ValueError('canonical order mismatch')
    np.testing.assert_allclose(intervals(p),intervals(np.vstack((np.zeros(3),x))),atol=1e-8,rtol=1e-8)
    return p

def interval_jacobian(points):
    p=np.asarray(points);i,j=np.triu_indices(len(p),1)
    d=2*(p[i]-p[j])*ETA;J=np.zeros((len(i),len(p),3));k=np.arange(len(i))
    J[k,i]=d;J[k,j]=-d
    return J[:,1:,:].reshape(len(i),-1)

def precision(K,variant):
    if variant=='unweighted':return np.eye(len(K))
    if variant=='diagonal':W=np.diag(1/np.diag(K))
    elif variant=='full':W=cho_solve(cho_factor(K,lower=True),np.eye(len(K)))
    else:raise ValueError(variant)
    W=(W+W.T)/2
    return W/np.mean(np.diag(W))

def objective(points,target,W):
    e=intervals(points)-target;v=W@e
    return .5*float(e@v)/len(e),interval_jacobian(points).T@v/len(e)

def correct(initial,order,target,K,variant):
    """Fixed local constrained solve; all unsuccessful outcomes return baseline."""
    c=cfg();initial=np.asarray(initial);v0=initial[1:].ravel();radius=c['maximum_relative_shift']*np.linalg.norm(v0)
    W=precision(K,variant);f0=objective(initial,target,W)[0]
    fzero,_,_=constraints(initial,np.asarray(order,bool),0.)
    minimum=float(np.min(fzero(v0)))
    if minimum<=0:raise ValueError('initial embedding must be strictly feasible')
    margin=min(c['maximum_margin'],.5*minimum)
    fun,jac,unpack=constraints(initial,np.asarray(order,bool),margin)
    trust=lambda v:radius**2-float((v-v0)@(v-v0))
    tgrad=lambda v:-2*(v-v0)
    result=minimize(lambda v:objective(unpack(v),target,W),v0,jac=True,method='SLSQP',
        constraints=[dict(type='ineq',fun=fun,jac=jac),dict(type='ineq',fun=trust,jac=tgrad)],
        options=dict(ftol=c['solver_ftol'],maxiter=c['solver_maxiter']))
    candidate=unpack(result.x);finite=bool(np.isfinite(candidate).all())
    after=order_check(candidate,order) if finite else dict(passed=False)
    relative=float(np.linalg.norm(result.x-v0)/np.linalg.norm(v0)) if finite else None
    slack=float(np.min(fun(result.x))) if finite else None
    f1=objective(candidate,target,W)[0] if finite else None
    accept=bool(result.success and finite and after['passed'] and slack>=-c['feasibility_tolerance']
        and relative<=c['maximum_relative_shift']+1e-8 and f1<=f0+1e-12)
    return dict(status='ACCEPTED' if accept else 'FALLBACK',
        features=(candidate if accept else initial)[1:].tolist(),solver_success=bool(result.success),
        solver_status=int(result.status),iterations=int(result.nit),objective_before=f0,
        objective_candidate=f1,relative_shift=relative,minimum_constraint_slack=slack,
        margin=margin,candidate_order=after)

def predict(intrinsic,order,frozen):
    if intrinsic['status']!='COMPLETE':return dict(status=intrinsic['status'])
    features=np.asarray(intrinsic['projection']['features']);M=matrices(features,order)
    params=frozen['models']['grouped']['projected']
    bias=params['bias_shrinkage']*(M['group_X']@params['bias_coefficients']);target=M['q']-bias
    K=covariance(M,params['variance_components'],'grouped');condition=float(np.linalg.cond(K))
    baseline=np.vstack((np.zeros(3),features));assert order_check(baseline,order)['passed']
    variants={'baseline':dict(status='BASELINE',features=features.tolist())}
    reason=None
    try:
        initial=canonical(features,order)
        if condition>cfg()['maximum_covariance_condition']:raise ValueError('covariance condition limit')
    except (ValueError,AssertionError,np.linalg.LinAlgError) as exc:
        reason=str(exc)
    for variant in cfg()['variants'][1:]:
        if reason is not None:variants[variant]=dict(status='FALLBACK',reason=reason,features=features.tolist())
        else:variants[variant]=correct(initial,order,target,K,variant)
    sd=np.sqrt(np.diag(K));gsd=np.sqrt(np.einsum('ij,ij->i',M['H']@K,M['H']))
    blocks={name:dict(sd=float(np.sqrt(w@K@w))) for name,w in M['blocks'].items()}
    for v in variants.values():
        p=np.vstack((np.zeros(3),v['features']));q=intervals(p)
        v.update(interval_centre=q.tolist(),gram_centre=(M['H']@q).tolist(),
            blocks={name:float(w@q) for name,w in M['blocks'].items()},order=order_check(p,order))
    return dict(status='COMPLETE',variants=variants,scale=intrinsic['scale'],support_count=len(features),
        covariance_condition=condition,interval_sd=sd.tolist(),gram_sd=gsd.tolist(),blocks=blocks,
        unconstrained_bias_centre=target.tolist(),group_weights=M['fit_weight'].tolist())

def evaluate(intrinsic,order,prediction,true_points):
    if prediction['status']!='COMPLETE':return dict(status=prediction['status'])
    M=matrices(intrinsic['projection']['features'],order)
    truth=intervals(np.asarray(true_points)/prediction['scale']);variants={}
    for name,v in prediction['variants'].items():
        e=np.asarray(v['interval_centre'])-truth;iz=e/prediction['interval_sd']
        gz=(np.asarray(v['gram_centre'])-M['H']@truth)/prediction['gram_sd']
        bz={k:float((v['blocks'][k]-w@truth)/prediction['blocks'][k]['sd']) for k,w in M['blocks'].items()}
        family=dict(interval=float(np.max(abs(iz))),gram=float(np.max(abs(gz))),block=max(abs(b) for b in bz.values()))
        variants[name]=dict(score=max(family.values()),family_scores=family,
            group_balanced_mse=float(M['fit_weight']@(e*e)),interval_mse=float(np.mean(e*e)),
            groups={g:dict(n=int(mask.sum()),mse=float(np.mean(e[mask]**2))) for g,mask in M['groups'].items() if mask.any()},
            standardized_blocks=bz)
    e=np.asarray(prediction['unconstrained_bias_centre'])-truth
    return dict(status='COMPLETE',variants=variants,true_intervals=truth.tolist(),
        unconstrained_bias_group_balanced_mse=float(M['fit_weight']@(e*e)))
