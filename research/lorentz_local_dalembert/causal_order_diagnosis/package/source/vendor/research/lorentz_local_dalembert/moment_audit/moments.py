"""Explicit coordinate-assisted interventions on fixed memberships, never inference."""
import math
import numpy as np
ETA = np.diag([-1.,1.,1.])
NAMES = ['raw','T','S','TS','D','TD','SD','TSD']


def proper(v):
    v = np.asarray(v, float)
    q2 = -np.einsum('...i,ij,...j->...',v,ETA,v)
    if not np.all(np.isfinite(v)) or np.any(q2 <= 0):
        raise ValueError('strict finite timelike vectors required')
    return np.sqrt(q2)


def future_unit(v):
    return np.sign(v[...,0])[...,None]*v/proper(v)[...,None]


def boost(a,u):
    """Lorentz map taking future unit a to u, identity on their orthogonal plane."""
    return np.eye(3)+np.outer(u+a,(u+a)@ETA)/(1-u@ETA@a)-2*np.outer(u,a@ETA)


def shapley(errors_squared):
    e = np.asarray(errors_squared)
    if e.shape != (8,): raise ValueError('eight factorial values required')
    out=[]
    for bit in [1,2,4]:
        value=0.
        for mask in range(8):
            if not mask & bit:
                k=mask.bit_count()
                value += math.factorial(k)*math.factorial(2-k)/6*(e[mask]-e[mask|bit])
        out.append(float(value))
    np.testing.assert_allclose(sum(out), e[0]-e[7], rtol=1e-10, atol=1e-10)
    return out


def diagnose(temporal, shells, references, tn, tm, c):
    v=np.asarray(temporal,float); sides=[np.asarray(w,float) for w in shells]
    refs=np.asarray(references,float)
    if v.shape != (2,3) or refs.shape != (2,3) or len(sides)!=2 or min(map(len,sides))==0:
        raise ValueError('two endpoints, two nonempty shells and two references required')
    if tn<=0 or tm<=0 or c<=0: raise ValueError('positive scales required')
    if v[0,0]>=0 or v[1,0]<=0: raise ValueError('past/future endpoint order required')
    for w,r in zip(sides,refs):
        if w.ndim!=2 or w.shape[1]!=3 or np.any(w[:,0]*r[0]<=0):
            raise ValueError('shell orientation mismatch')
    qv=proper(v); qw=[proper(w) for w in sides]; axes=future_unit(refs)
    ends=future_unit(v); u=ends.sum(axis=0); u=u/proper(u)
    rotations=[boost(a,u) for a in axes]
    out={}; pieces=[]
    for mask,name in enumerate(NAMES):
        vv=v.copy(); ww=[w.copy() for w in sides]
        if mask & 1: vv*= (tn/qv)[:,None]
        if mask & 2: ww=[w*(tm/q)[:,None] for w,q in zip(ww,qw)]
        if mask & 4:
            vv=np.sign(v[:,0])[:,None]*proper(vv)[:,None]*u
            ww=[w@b.T for w,b in zip(ww,rotations)]
        t=-(c+3)/(2*tn**2)*(vv.T@vv)
        s=c/(2*tm**2)*sum(w.T@w/len(w) for w in ww)
        metric=t+s; error=float(np.linalg.norm(metric-ETA)/np.sqrt(3))
        eig=np.linalg.eigvalsh(metric); tol=1e-10*max(1.,max(abs(eig)))
        out[name]=dict(metric=metric,error=error,
                       lorentz_signature=bool(sum(eig < -tol)==1 and sum(eig>tol)==2))
        if mask==0: pieces=[t,s]
    ti=-(c+3)*np.outer(u,u); si=ETA-ti
    dt=pieces[0]-ti; ds=pieces[1]-si
    decomposition=dict(temporal=pieces[0],shell=pieces[1],temporal_ideal=ti,shell_ideal=si,
                       temporal_error_squared=float(np.sum(dt*dt)/3),
                       shell_error_squared=float(np.sum(ds*ds)/3),
                       cross_term=float(2*np.sum(dt*ds)/3))
    np.testing.assert_allclose(sum(decomposition[k] for k in ['temporal_error_squared','shell_error_squared','cross_term']),out['raw']['error']**2,atol=1e-9,rtol=1e-10)
    rapidity=lambda a: np.arccosh(np.maximum(1.,-a@ETA@u))
    return dict(variants=out,observer=u,decomposition=decomposition,
                shapley_squared_error_reduction=dict(zip(['T','S','D'],shapley([out[n]['error']**2 for n in NAMES]))),
                temporal_proper_time_ratios=qv/tn,
                shell_proper_time_ratios=[dict(mean=float(np.mean(q/tm)),sd=float(np.std(q/tm)),minimum=float(min(q/tm)),maximum=float(max(q/tm))) for q in qw],
                endpoint_rapidities=rapidity(ends),reference_rapidities=rapidity(axes),
                populations=[len(w) for w in sides])
