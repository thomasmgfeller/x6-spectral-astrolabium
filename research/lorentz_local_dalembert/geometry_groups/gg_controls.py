"""SPDX-License-Identifier: Apache-2.0"""
import inspect
import json
import numpy as np
from gg_common import cfg,close
from gg_model import matrices,basis,covariance,intervals,predict,evaluate,fit_one
from gg_calibrate import rank
from gg_analyze import shape,paired_comparison
from gu_controls import check as inherited_check

def check():
    inherited=inherited_check();rng=np.random.default_rng(77261022)
    x=rng.normal(size=(16,3));p=np.vstack((np.zeros(3),x));n=len(p)
    i,j=np.triu_indices(n,1);q=intervals(p);order=np.zeros((n,n),bool)
    for a,b,s in zip(i,j,q):
        if s<0:order[a,b]=p[b,0]>p[a,0];order[b,a]=p[a,0]>p[b,0]
    M=matrices(x,order);masks=list(M['groups'].values())
    assert np.all(np.sum(masks,axis=0)==1);assert all(mask.any() for mask in masks)
    B,names,floors=basis(M,'grouped');assert len(B)==10 and floors==[0,1,2]
    coeff=np.arange(1,11)*.001;K=covariance(M,coeff,'grouped');assert np.linalg.eigvalsh(K)[0]>0
    A=np.zeros((len(i),n));A[np.arange(len(i)),i]=A[np.arange(len(i)),j]=1/np.sqrt(2.)
    factors=[np.diag(mask.astype(float)) for mask in masks]+[A]+[mask[:,None]*A for mask in masks[1:]]
    factors += [mask[:,None].astype(float) for mask in masks]+[(M['q']/M['D'])[:,None]]
    F=M['D'][:,None]*np.column_stack([np.sqrt(c)*f for c,f in zip(coeff,factors)])
    close(K,F@F.T);close(M['H']@K@M['H'].T,(M['H']@F)@(M['H']@F).T)
    # Opposite interval signs induce negative covariance in the scale component.
    negative=np.where(q<0)[0][0];positive=np.where(q>0)[0][0]
    assert B[-1][negative,positive]<0
    # Group-specific root covariance is not block-diagonal overall.
    root=np.where(masks[0])[0][0]
    adjacent=[k for k in range(len(i)) if masks[1][k] and len(set((i[root],j[root]))&set((i[k],j[k])))>0]
    assert adjacent and B[3][root,adjacent[0]]>0
    close(sum(M['fit_weight']),1.)
    for mask in masks:close(sum(M['fit_weight'][mask]),1/3)
    # Group labels use the observed order, never signs of reconstructed intervals.
    distorted=matrices(x*np.array([.01,10.,10.]),order)
    for name in M['groups']:assert np.array_equal(M['groups'][name],distorted['groups'][name])
    boost=np.array([[np.cosh(.4),-np.sinh(.4),0],[-np.sinh(.4),np.cosh(.4),0],[0,0,1.]])
    transformed=matrices(x@boost.T,order);close(covariance(transformed,coeff,'grouped'),K)
    # Bias shrinkage selects zero when all development errors are exactly zero.
    data=[]
    for k in range(8):
        xx=x*(1+.02*k);data.append((xx,order,intervals(np.vstack((np.zeros(3),xx)))))
    fit=fit_one(data,'grouped');assert fit['bias_shrinkage']==0;close(fit['bias_coefficients'],0.)
    fake=dict(models={which:{arm:dict(bias_coefficients=[0.]*(3 if which=='pooled' else 6),bias_shrinkage=0.,
        variance_components=[.1]*len(basis(M,which)[0])) for arm in cfg()['arms']} for which in cfg()['models']},
        support_cut=16,condition_cut=100,metadata_min=[0,0],metadata_max=[100,1e9])
    intrinsic=dict(status='COMPLETE',original_features=x.tolist(),projection=dict(features=x.tolist()),scale=1.)
    pred=predict(intrinsic,order,fake);result=evaluate(intrinsic,order,pred,p)
    for which in cfg()['models']:close(result['models'][which]['score'],0.)
    assert rank(64)==62 and rank(48)==47
    assert list(inspect.signature(predict).parameters)==['intrinsic','order','frozen']
    balanced=np.tile([-1.,1.],32)
    assert shape(balanced)['passed'] and not shape(.1*balanced)['passed']
    assert not shape(balanced+2.)['passed'] and not shape(balanced[:20])['passed']
    fixtures=[]
    for sign in balanced:
        fixtures.append(dict(evaluation=dict(status='COMPLETE',models={which:dict(arms={
            arm:dict(standardized_blocks={g:float(sign*(2 if which=='pooled' else 1)) for g in cfg()['focus_groups']})
            for arm in cfg()['arms']}) for which in cfg()['models']})))
    paired=paired_comparison(fixtures);assert paired['improvement_screen_passed']
    close(paired['difference_grouped_minus_pooled'],-np.log(4.))
    for row in fixtures:
        row['evaluation']['models']['pooled'],row['evaluation']['models']['grouped']=row['evaluation']['models']['grouped'],row['evaluation']['models']['pooled']
    assert not paired_comparison(fixtures)['improvement_screen_passed']
    return dict(status='PASS',inherited=inherited,groups=['exhaustive_disjoint_groups','ten_component_psd_factorization',
        'gram_covariance_cross_terms','signed_scale_negative_covariance','cross_group_endpoint_dependence',
        'cloud_and_group_balancing','observed_order_classification','lorentz_invariant_covariance',
        'leave_one_cloud_out_zero_bias','zero_error_prediction','conformal_rank','inference_only_boundary',
        'shape_screen_negative_controls','paired_improvement_direction_and_negative_control'])

if __name__=='__main__':print(json.dumps(check()))
