"""3+1 chain geometry, exact Poisson atoms, and guarded count reconstruction."""
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.stats import chi2
import exact_start as exact

PAIRS=list(combinations(range(7),2))
INDEX={p:k for k,p in enumerate(PAIRS)}
PRED=[k for k,p in enumerate(PAIRS) if p != (5,6)]
B=np.array([[int(a<=i and j<=b) for i,j in PAIRS] for a,b in PAIRS],dtype=np.int64)


def base(epsilon,sign):
    return [exact.point(-8,0,0,0), exact.point(-6,1,0,0),
            exact.point(-4,0,1,0), exact.point(-2,0,0,0),
            exact.point(0,0,0,F(epsilon)),
            exact.point(1,F(1,4),F(1,4),F(1,4)),
            exact.point(2,-F(1,4),F(1,4),sign*F(1,4))]


def exact_geometry(points):
    n=len(points)
    ss=[[exact.interval(a,b) for b in points] for a in points]
    if not all(points[i][0]<points[j][0] and ss[i][j]<0 for i,j in PAIRS):
        raise ValueError('not a strict timelike chain; no replacement permitted')
    # V(i,j) = pi/24 * W(i,j); rational W eliminates integration error.
    w=lambda i,j:ss[i][j]**2 if i<j else F(0)
    atoms=[w(i,j)-w(i+1,j)-w(i,j-1)+w(i+1,j-1) for i,j in PAIRS]
    assert all(x>=0 for x in atoms)
    assert sum(atoms)==w(0,6)
    for k,(a,b) in enumerate(PAIRS):
        assert sum(atoms[l] for l in range(21) if B[k,l])==w(a,b)
        for m,(c,d) in enumerate(PAIRS):
            assert sum(atoms[l] for l in range(21) if B[k,l] and B[m,l])==w(max(a,c),min(b,d))
    return {'points':[[str(x) for x in p] for p in points],
            'signed_intervals':[str(ss[i][j]) for i,j in PAIRS],
            'volume_ratios':[str(w(i,j)/w(0,6)) for i,j in PAIRS],
            'atom_ratios':[str(x/w(0,6)) for x in atoms],
            'outer_W':str(w(0,6)), 'tau_squared':str(-ss[5][6]),
            'exact_covariance_identities':441}


def arrays(g):
    return {k:np.array([float(F(x)) for x in g[k]])
            for k in ('signed_intervals','volume_ratios','atom_ratios')}


def build_system(s):
    # s: observations x 21. No access to entry INDEX[(5,6)].
    n=len(s); G=np.zeros((n,4,4)); d=np.zeros((n,4))
    for i in range(1,5):
        for j in range(1,5):
            sij=0 if i==j else s[:,INDEX[tuple(sorted((i,j)))]]
            G[:,i-1,j-1]=(s[:,INDEX[(0,i)]]+s[:,INDEX[(0,j)]]-sij)/2
        d[:,i-1]=(s[:,INDEX[(0,5)]]-s[:,INDEX[(i,5)]]
                    -s[:,INDEX[(0,6)]]+s[:,INDEX[(i,6)]])/2
    return G,d


def reconstruct(counts, rho, exact_s=None):
    s=-np.sqrt(24*counts/(np.pi*rho))
    G,d=build_system(s)
    if exact_s is not None:
        G[:]=build_system(exact_s[None,:])[0][0]
    eig,Q=np.linalg.eigh(G)
    eigmin=np.min(abs(eig),axis=1); eigmax=np.max(abs(eig),axis=1)
    structural=(np.sum(eig<0,axis=1)==1)&(eigmin>eigmax*1e-12)
    # Do not invert rejected matrices.
    tau2=np.full(len(counts),np.nan)
    idx=np.where(structural)[0]
    projected=np.einsum('nij,ni->nj',Q[idx],d[idx])
    tau2[idx]=-np.sum(projected**2/eig[idx],axis=1)
    positive=structural & np.isfinite(tau2)&(tau2>0)
    positive &= np.min(counts[:,PRED],axis=1)>0
    tau=np.where(positive,np.sqrt(np.maximum(tau2,0)),np.nan)
    return {'tau':tau,'tau2':tau2,'valid':positive,'G':G,'d':d,'eig':eig,'Q':Q,
            'count_eligible':np.min(counts[:,PRED],axis=1)>=16}


def poisson_box(counts,rho,alpha=.05):
    k=counts[:,PRED]; tail=alpha/(2*len(PRED))
    low=np.zeros(k.shape)
    nz=k>0
    low[nz]=chi2.ppf(tail,2*k[nz])/2
    high=chi2.ppf(1-tail,2*(k+1))/2
    return low,high,-np.sqrt(24*high/(np.pi*rho)),-np.sqrt(24*low/(np.pi*rho))


def uncertainty(counts,rho,rec):
    low,high,slo,shi=poisson_box(counts,rho)
    s=-np.sqrt(24*counts/(np.pi*rho))
    err=np.zeros_like(s); err[:,PRED]=np.maximum(abs(s[:,PRED]-slo),abs(shi-s[:,PRED]))
    E=np.zeros_like(rec['G']); ed=np.zeros_like(rec['d'])
    for i in range(1,5):
        for j in range(1,5):
            if i==j: E[:,i-1,j-1]=err[:,INDEX[(0,i)]]
            else: E[:,i-1,j-1]=(err[:,INDEX[(0,i)]]+err[:,INDEX[(0,j)]]+err[:,INDEX[tuple(sorted((i,j)))]] )/2
        ed[:,i-1]=(err[:,INDEX[(0,5)]]+err[:,INDEX[(i,5)]]+err[:,INDEX[(0,6)]]+err[:,INDEX[(i,6)]] )/2
    lo=np.zeros(len(counts)); hi=np.full(len(counts),np.inf); ratio=np.full(len(counts),np.inf)
    ix=np.where(rec['valid'])[0]
    T=rec['Q'][ix]/np.sqrt(abs(rec['eig'][ix]))[:,None,:]
    AT=abs(T)
    Eb=np.einsum('nki,nkl,nlj->nij',AT,E[ix],AT)
    e=np.linalg.norm(Eb,axis=(1,2))
    db=np.einsum('nki,nk->ni',T,rec['d'][ix])
    de=np.einsum('nki,nk->ni',AT,ed[ix])
    dn=np.linalg.norm(db,axis=1); en=np.linalg.norm(de,axis=1)
    ratio[ix]=e
    good=e<1
    ids=ix[good]
    bound=(dn[good]**2*e[good]+2*dn[good]*en[good]+en[good]**2)/(1-e[good])
    upper=rec['tau2'][ids]+bound
    feasible=upper>=0
    ids=ids[feasible]; bound=bound[feasible]
    lo[ids]=np.sqrt(np.maximum(0,rec['tau2'][ids]-bound))
    hi[ids]=np.sqrt(rec['tau2'][ids]+bound)
    cert=(lo>0)&(lo>=rec['tau']/1.1)&(hi<=rec['tau']/.9)
    return {'lo':lo,'hi':hi,'finite':np.isfinite(hi),'certificate_10pct':cert,
            'perturbation_ratio':ratio,'mean_low':low,'mean_high':high}


def sample_diamond(rng,n,left,right):
    """Uniform Minkowski 4-volume, exact inverse-CDF construction in rest frame."""
    left=np.asarray(left,float); right=np.asarray(right,float)
    dt=right[0]-left[0]; dx=right[1:]-left[1:]
    T=np.sqrt(dt*dt-dx@dx); half=T/2
    w=rng.random(n)**.25
    t=(2*rng.integers(0,2,n)-1)*half*(1-w)
    direction=rng.standard_normal((n,3)); direction/=np.linalg.norm(direction,axis=1)[:,None]
    radius=half*w*rng.random(n)**(1/3)
    x=direction*radius[:,None]
    beta=dx/dt; beta2=beta@beta; gamma=dt/T
    bx=x@beta
    tt=gamma*(t+bx)
    xx=x+(((gamma-1)/beta2*bx+gamma*t)[:,None]*beta if beta2>0 else 0)
    return np.column_stack((tt,xx))+(left+right)/2


def cloud_counts(cloud,points):
    fut=[]; past=[]
    for p in np.asarray(points,float):
        dt=cloud[:,0]-p[0]; dx=cloud[:,1:]-p[1:]
        causal=dt*dt>np.einsum('ij,ij->i',dx,dx)
        fut.append(causal&(dt>0)); past.append(causal&(dt<0))
    return np.array([np.count_nonzero(fut[i]&past[j]) for i,j in PAIRS],dtype=np.int64)
