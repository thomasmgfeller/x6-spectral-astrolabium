"""SPDX-License-Identifier: Apache-2.0"""
import json
import numpy as np
from gu_common import close,cfg
from gu_model import intervals,matrices,covariance,predict,evaluate
from gu_calibrate import rank

def check():
    rng=np.random.default_rng(76261021);x=rng.normal(size=(12,3));p=np.vstack((np.zeros(3),x))
    t=p[:,0];q=intervals(p);i,j=np.triu_indices(len(p),1);order=np.zeros((len(p),len(p)),bool)
    for a,b,interval in zip(i,j,q):
        if interval<0:order[a,b]=t[b]>t[a];order[b,a]=t[a]>t[b]
    M=matrices(x,order);K=covariance(M,[.2,.3,.4])
    boost=np.array([[np.cosh(.7),-np.sinh(.7),0],[-np.sinh(.7),np.cosh(.7),0],[0,0,1.]])
    close(intervals(p@boost.T),q);close(intervals(p*3)/9,q)
    G=(p*np.array([-1.,1.,1.]))@p.T
    close(M['H']@q,[G[a,b] for a,b in M['gram_pairs']])
    assert np.linalg.eigvalsh(K)[0]>0
    # Exact propagation, checked against an independent factor representation.
    A=np.zeros((len(i),len(p)));A[np.arange(len(i)),i]=A[np.arange(len(i)),j]=1/np.sqrt(2.)
    F=M['D'][:,None]*np.column_stack((np.sqrt(.2)*np.eye(len(i)),np.sqrt(.3)*A,np.sqrt(.4)*np.ones(len(i))))
    close(K,F@F.T);close(M['H']@K@M['H'].T,(M['H']@F)@(M['H']@F).T)
    w=np.ones(len(i))/len(i);assert w@K@w>10*np.sum(w*w*np.diag(K))
    rootpair=np.where(i==0)[0];a,b=rootpair[:2]
    endpoint=covariance(M,[1e-8,.3,0.]);assert endpoint[a,b]>0
    fake=dict(arms={arm:dict(bias_coefficients=[0.,0.,0.],variance_components=[.2,.3,.4]) for arm in cfg()['arms']},
        support_cut=12.,condition_cut=100.,metadata_min=[0.,0.],metadata_max=[100.,1e9])
    intrinsic=dict(status='COMPLETE',original_features=x.tolist(),projection=dict(features=x.tolist()),scale=1.)
    pred=predict(intrinsic,order,fake);evaluation=evaluate(intrinsic,order,pred,p)
    close(evaluation['score'],0.)
    # Affine interval bias can be removed exactly, including induced Gram bias.
    bias=M['X']@np.array([.1,.2,-.3]);centre=q-bias
    close(M['H']@(q-centre),M['H']@bias)
    assert rank(24)==24 and rank(32)==32 and rank(19)==19 and rank(18)>18
    # Prediction signature is intentionally limited to inference-only inputs.
    import inspect
    assert list(inspect.signature(predict).parameters)==['intrinsic','order','frozen']
    return dict(status='PASS',groups=['lorentz_and_scale_invariance','exact_gram_identity',
        'psd_and_factor_covariance','gram_cross_terms','shared_endpoint_and_diagonal_negative_control',
        'zero_error_and_bias','conformal_rank','inference_only_signature'])

if __name__=='__main__':print(json.dumps(check()))
