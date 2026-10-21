"""SPDX-License-Identifier: Apache-2.0"""
import inspect
import json
import numpy as np
from scipy.optimize._numdiff import approx_derivative
from gc_common import close,order_check,matrices
from gc_model import canonical,interval_jacobian,objective,precision,correct,predict,intervals
from gc_analyze import decide

def order_of(p):
    dt=p[None,:,0]-p[:,None,0];d=p[None,:,1:]-p[:,None,1:]
    return (dt>0)&(dt*dt>np.sum(d*d,axis=2))

def check():
    p=np.array([[0.,0.,0.],[2.,.2,.1],[-1.,.1,-.1],[.2,1.,.3],[.4,-.5,1.1],[1.,1.5,-.3]])
    r=order_of(p);q=intervals(p);M=matrices(p[1:],r);m=len(q)
    J=interval_jacobian(p)
    close(J,approx_derivative(lambda v:intervals(np.vstack((np.zeros(3),v.reshape(-1,3)))),p[1:].ravel()))
    u=np.linspace(-1,1,m);K=np.eye(m)*.2+.1*np.outer(u,u);W=precision(K,'full');target=.98*q
    f,g=objective(p,target,W)
    close(g,approx_derivative(lambda v:objective(np.vstack((np.zeros(3),v.reshape(-1,3))),target,W)[0],p[1:].ravel()).ravel())
    inv=np.linalg.solve(K,np.eye(m));close(W,inv/np.mean(np.diag(inv)))
    assert abs((q-target)@W@(q-target)-(q-target)@precision(K,'diagonal')@(q-target))>1e-5
    can=canonical(p[1:],r);close(intervals(can),q)
    boost=np.array([[np.cosh(.6),-np.sinh(.6),0],[-np.sinh(.6),np.cosh(.6),0],[0,0,1.]])
    transformed=p@boost.T+np.array([7.,-2.,4.]);transformed-=transformed[0]
    close(intervals(canonical(transformed[1:],r)),q)
    perm=np.array([0,4,2,5,1,3]);cp=canonical(p[perm][1:],r[np.ix_(perm,perm)])
    close(intervals(cp[np.argsort(perm)]),q)
    for variant in ['unweighted','diagonal','full']:
        zero=correct(can,r,q,K,variant);assert zero['status']=='ACCEPTED'
        close(intervals(np.vstack((np.zeros(3),zero['features']))),q)
        scaled=correct(can,r,target,K,variant);assert scaled['status']=='ACCEPTED'
        sq=intervals(np.vstack((np.zeros(3),scaled['features'])))
        assert np.linalg.norm(sq-target)<2e-4 and scaled['candidate_order']['passed']
        again=correct(canonical(transformed[1:],r),r,target,K,variant)
        np.testing.assert_allclose(intervals(np.vstack((np.zeros(3),again['features']))),sq,atol=2e-5,rtol=2e-5)
    bad=p.copy();bad[1,0]=0;assert not order_check(bad,r)['passed']
    close(M['fit_weight'].sum(),1.)
    for mask in M['groups'].values():close(M['fit_weight'][mask].sum(),1/3)
    assert list(inspect.signature(predict).parameters)==['intrinsic','order','frozen']
    from copy import deepcopy
    variants={v:dict(order_violations=0,fallbacks=0,simultaneous=dict(rate=1.),groups={g:dict(rmse=.98 if v=='full' else 1.) for g in M['groups']}) for v in ['baseline','unweighted','diagonal','full']}
    phases={p:dict(complete=64,variants=deepcopy(variants)) for p in ['calibration','test']}
    paired={v:dict(rmse_ratio_full_over_comparator=.98,upper_below_one=True) for v in ['baseline','unweighted','diagonal']}
    assert all(decide(phases,paired)[0].values())
    mutations=[lambda p,c:p['test'].update(complete=20),lambda p,c:p['test']['variants']['full'].update(order_violations=1),
        lambda p,c:p['test']['variants']['full'].update(fallbacks=7),lambda p,c:p['test']['variants']['full']['simultaneous'].update(rate=.9),
        lambda p,c:c['baseline'].update(rmse_ratio_full_over_comparator=1.),lambda p,c:c['baseline'].update(upper_below_one=False),
        lambda p,c:c['diagonal'].update(upper_below_one=False),lambda p,c:p['test']['variants']['full']['groups']['root'].update(rmse=1.06)]
    for mutate in mutations:
        ph,co=deepcopy(phases),deepcopy(paired);mutate(ph,co);assert not all(decide(ph,co)[0].values())
    return dict(status='PASS',groups=['interval_jacobian_finite_difference','objective_gradient_finite_difference',
        'precision_direct_solve','correlation_negative_control','canonical_interval_identity','lorentz_translation_invariance',
        'node_permutation_invariance','zero_residual_fixed_point','known_scale_correction','correction_boost_invariance',
        'strict_order_negative_control','equal_cloud_group_weights','inference_only_signature','all_eight_gate_negative_controls'])
if __name__=='__main__':print(json.dumps(check()))
