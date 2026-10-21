"""Exact-distance motivated candidate V2; not qualified on noisy clouds.

All four external landmarks must be timelike related to each other, to the
root, and to every support. Input q is positive squared proper time.
No root-to-support distance or field value is accepted by this interface.
SPDX-License-Identifier: Apache-2.0
"""
import numpy as np
from intrinsic_correction import design


def operator(q_anchor, q_anchor_root, q_anchor_support, scale):
    qa=np.asarray(q_anchor,float)
    qr=np.asarray(q_anchor_root,float)
    qx=np.asarray(q_anchor_support,float)
    if qa.shape!=(4,4) or qr.shape!=(4,) or qx.ndim!=2 or qx.shape[0]!=4:
        raise ValueError('exactly four landmarks required')
    if not all(np.isfinite(v).all() for v in [qa,qr,qx]) or not np.isfinite(scale) or scale<=0:
        raise ValueError('finite distances and positive scale required')
    if not np.allclose(qa,qa.T,atol=1e-12,rtol=1e-12) or np.any(np.diag(qa)!=0):
        raise ValueError('symmetric zero-diagonal anchor distances required')
    if np.any(qa[np.triu_indices(4,1)]<=0) or np.any(qr<=0) or np.any(qx<=0):
        raise ValueError('this version requires strictly timelike landmark intervals')
    h=(qa[1:,1:]-qa[1:,0,None]-qa[None,0,1:])/(2*scale**2)
    ev=np.linalg.eigvalsh(h)
    if not ev[0]<0<ev[1] or np.linalg.cond(h)>1e5:
        raise ValueError('affinely independent Lorentz landmark frame required')
    z=((qx[1:]-qx[0])-(qr[1:]-qr[0])[:,None]).T/(2*scale**2)
    d=design(z)
    if np.linalg.matrix_rank(d)!=9 or np.linalg.cond(d)>1e5:
        raise ValueError('full-rank bounded-condition moment system required')
    target=np.r_[np.zeros(3),2*np.diag(h),2*h[0,1],2*h[0,2],2*h[1,2]]
    n=len(z);noise=np.eye(n)+np.ones((n,n))
    kkt=np.block([[noise,d.T],[d,np.zeros((9,9))]])
    solution=np.linalg.solve(kkt,np.r_[np.zeros(n),target])
    a=solution[:n]
    residual=max(float(np.max(abs(d@a-target))),float(np.max(abs(noise@a+d.T@solution[n:]))))
    if residual>1e-7*(1+np.max(abs(target))):
        raise ValueError('moment/KKT certificate failed')
    return dict(status='EXPERIMENTAL_WEIGHTS_ONLY',weights=(np.r_[-a.sum(),a]/scale**2).tolist(),
                intrinsic_coordinates=z.tolist(),intrinsic_metric=h.tolist(),
                design_condition=float(np.linalg.cond(d)),landmark_condition=float(np.linalg.cond(h)),
                kkt_residual=residual,noise_covariance_included=True,
                observed_order_validation='REQUIRES_EXTERNAL_COMPLETE_ORDER_CHECK',
                noisy_cloud_qualification='NOT_RUN')
