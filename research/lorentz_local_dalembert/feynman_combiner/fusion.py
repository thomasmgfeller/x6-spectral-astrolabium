"""Linear reference only. Inputs must share an identified coordinate frame.
R is the JOINT error covariance, never merely the spread between reconstructions.
"""
import numpy as np


def covariance(a):
    a = np.asarray(a,float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.isfinite(a).all():
        raise ValueError('finite square covariance required')
    if not np.allclose(a,a.T,atol=1e-12,rtol=1e-12):
        raise ValueError('asymmetric covariance')
    if np.linalg.eigvalsh(a).min() < -1e-10*max(1.,np.linalg.norm(a,2)):
        raise ValueError('indefinite covariance')
    return (a+a.T)/2


def combine(z, joint_covariance, weights):
    z = np.asarray(z,float); w = np.asarray(weights,float)
    if z.ndim != 2 or w.shape != (len(z),) or not np.isfinite(z).all() or not np.isfinite(w).all():
        raise ValueError('finite reconstructions and weights required')
    if not np.isclose(w.sum(),1.,atol=1e-12,rtol=0):
        raise ValueError('weights must sum to one')
    r = covariance(joint_covariance)
    a = np.kron(w.reshape(1,-1),np.eye(z.shape[1]))
    if r.shape != (z.size,z.size): raise ValueError('joint covariance dimension')
    return w@z, covariance(a@r@a.T), a


def blue_weights(r):
    """Scalar-channel BLUE; fail on singular covariance rather than add fake noise."""
    r = covariance(r)
    np.linalg.cholesky(r)
    v = np.linalg.solve(r,np.ones(len(r)))
    return v/v.sum()


def update(prediction, p, measurement, r, h, cross):
    """cross = Cov(true_state - prediction, measurement_error), explicit even if zero."""
    x,z,h = np.asarray(prediction,float),np.asarray(measurement,float),np.asarray(h,float)
    p,r,c = covariance(p),covariance(r),np.asarray(cross,float)
    covariance(np.block([[p,c],[c.T,r]]))
    innovation = z-h@x
    s = covariance(h@p@h.T+r+h@c+c.T@h.T)
    np.linalg.cholesky(s)
    b = p@h.T+c
    gain = np.linalg.solve(s,b.T).T
    posterior = x+gain@innovation
    post_cov = covariance(p-gain@b.T)
    return dict(prediction=x, measurement=z, innovation=innovation, innovation_covariance=s,
                gain=gain, posterior=posterior, posterior_covariance=post_cov,
                nis=float(innovation@np.linalg.solve(s,innovation)))


def causal_check(points, relation, tolerance=1e-10):
    """Flat 2+1, c=1, strict future order; checks false and missing relations.
    Offline geometric consistency, NOT an online no-future-data guarantee.
    No projection or repair is performed.
    """
    points = np.asarray(points,float); relation = np.asarray(relation,bool)
    if points.ndim!=2 or points.shape[1]!=3 or relation.shape!=(len(points),len(points)) or not np.isfinite(points).all():
        raise ValueError('invalid embedding or relation')
    dt = points[None,:,0]-points[:,None,0]
    dr = np.linalg.norm(points[None,:,1:]-points[:,None,1:],axis=2)
    margin = dt-dr
    predicted = (dt>tolerance)&(margin>=-tolerance)
    np.fill_diagonal(predicted,False)
    return dict(missing=int(np.sum(relation&~predicted)),extra=int(np.sum(predicted&~relation)),
                passed=bool(np.array_equal(relation,predicted)))
