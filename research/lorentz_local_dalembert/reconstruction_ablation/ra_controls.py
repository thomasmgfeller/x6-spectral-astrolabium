"""SPDX-License-Identifier: Apache-2.0
Analytic fixtures independent of the archived target geometries.
"""
import json
import numpy as np
from ra_common import close,ec,design,TARGET
from ra_core import reference,taylor_parts
from ra_analyze import component_stats


def check():
    x=np.random.default_rng(70421000).normal(size=(40,3))*.1
    ref=reference(x,.1);assert ref['status']=='COMPLETE'
    b=np.asarray(ref['full_coefficients']);close(design(x)@b[1:],TARGET);close(b.sum(),0)
    close(reference(x,.3)['full_coefficients'],b)
    rapidity=.4;ch=np.cosh(rapidity);sh=np.sinh(rapidity)
    boost=np.array([[ch,-sh,0],[-sh,ch,0],[0,0,1.]])
    theta=.7;rot=np.array([[1.,0,0],[0,np.cos(theta),-np.sin(theta)],[0,np.sin(theta),np.cos(theta)]])
    close(reference(x@boost.T@rot.T,.1)['full_coefficients'],b)
    distorted=x.copy();distorted[:,0]+=0.01*(x[:,1]/.1)**2
    bad=reference(distorted,.1);assert bad['status']=='COMPLETE'
    altered=np.asarray(bad['full_coefficients'])
    detected=[]
    for spec in ec.cfg()['fields']:
        pure=taylor_parts(x,spec,np.vstack((b,b)))
        close(pure['taylor'][0][:2],0);close(pure['errors'][0],pure['errors'][1])
        changed=taylor_parts(x,spec,np.vstack((altered,b)))
        detected.append(abs(changed['errors'][0]-changed['errors'][1]))
    assert max(detected)>1e-4
    e=np.array([[[1.,-2.]],[[2.,-1.]]]);s=component_stats(e,['d','r'])
    close(s['direct_mse'],1);close(s['signed_cross_terms']['d x r'],-4)
    degenerate=reference(np.tile([.1,.2,.3],(12,1)),.1)
    assert degenerate['status']=='ORACLE_UNAVAILABLE'
    return dict(status='PASS',groups=['polynomials_and_independent_svd','scale_invariance','lorentz_invariance',
        'exact_taylor_and_zero_reconstruction','controlled_geometry_distortion','signed_cross_term','rank_rejection'])


if __name__=='__main__':print(json.dumps(check()))
