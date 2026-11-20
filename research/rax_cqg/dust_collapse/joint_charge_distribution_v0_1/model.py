"""Finite catalogue, inherited scalar Gaussian Gram, and frozen dust fields."""
import json
from fractions import Fraction
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import null_space
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'inputs/sync'))
import support
from tube import template

I=np.array(support.I)
P=np.array(support.PAST)
F=np.array(support.FUTURE)
BETA=4/np.sqrt(6.)
DELTA=np.sqrt(2/(19*BETA))
def laws():
    laws=json.loads((BASE/'weights.json').read_text())['laws']
    keys=sorted(map(int,laws['1:1']))
    return keys,np.array([[float(Fraction(laws[k][str(i)])) for i in keys] for k in ('1:1','1:3')])
def combined_laws():
    base=json.loads((BASE/'weights.json').read_text())['laws']
    chain=json.loads((BASE/'chain.json').read_text())['law']
    keys=sorted(map(int,set(base['1:1'])|set(chain)))
    qs=[[float((Fraction(chain.get(str(i),0))+Fraction(base[k].get(str(i),0)))/2) for i in keys]
        for k in ('1:1','1:3')]
    assert np.max(abs(np.sum(qs,axis=1)-1))<1e-12
    return keys,np.array(qs)
def edges(code):
    _,rel=support.geometry(code)
    b=np.zeros((15,15))
    for y,x in rel:
        n=sum((y,v) in rel and (v,x) in rel for v in range(15))
        if n<4: b[y,x]=(1,-9,16,-8)[n]
    return b

def scalar(b):
    # H3 reduction in the archived frame. Orthogonal coordinates in the
    # hidden Hessian avoid choosing a non-invariant order for equivalent events.
    h=(b+b.T-np.diag(b.sum(0)+b.sum(1)))/2
    frame=np.zeros((15,15))
    frame[1:4,:3]=np.eye(3)
    frame[7:10,3:6]=np.eye(3)
    frame[I,range(6,13)]=1
    am=np.array([-128,241,119,-232])
    ap=am[::-1]
    bm=np.array([-46,-32,-16,0])
    bp=-bm[::-1]
    frame[P,-2]=bm
    frame[F,-1]=bp
    g=frame.T@h@frame
    g[-2,:3]-=am[1:]; g[:3,-2]-=am[1:]
    g[-1,3:6]+=ap[:3]; g[3:6,-1]+=ap[:3]
    g[-2,-2]-=am@bm;g[-1,-1]+=ap@bp
    v,u=np.linalg.eigh(g[6:,6:])
    regular=np.abs(v)>1e-8
    assert np.all(np.abs(v[regular])>1e-6)
    j=g[:6,6:]@u
    k=g[:6,:6]-(j[:,regular]/v[regular])@j[:,regular].T
    link=j[:,~regular].T
    if len(link):
        _,lam,L=np.linalg.svd(link,full_matrices=False)
        L=L[lam>1e-8]
    else: L=np.empty((0,6))
    lx,ly=L[:,:3],L[:,3:]
    N=null_space(lx) if len(lx) else np.eye(3)
    X=-np.linalg.pinv(lx)@ly if len(lx) else np.zeros((3,3))
    assert np.linalg.norm(lx@X+ly)<1e-7
    n=N.shape[1]
    transform=np.zeros((6,n+3))
    transform[:3,:n]=N;transform[:3,n:]=X;transform[3:,n:]=np.eye(3)
    Q=transform.T@(np.diag([1.,1.,1.,0.,0.,0.])-1j*k)@transform
    T=Q[:n,:n]
    precision=Q[n:,n:]-(Q[n:,:n]@np.linalg.solve(T,Q[:n,n:]) if n else 0)
    precision=BETA*(precision+precision.T)/2
    assert np.linalg.eigvalsh(precision.real).min()>0
    phase=np.sign(v[regular]).sum()*np.pi/4
    if n: phase-=np.arctan(np.linalg.eigvalsh(T.imag)).sum()/2
    R=precision.real.astype(np.longdouble)
    det=np.longdouble(1)
    for j in range(3):
        pivot=R[j,j]
        assert pivot>0
        det*=pivot
        R[j+1:,j+1:]-=R[j+1:,j,None]*R[None,j,j+1:]/pivot
    factor=float((det/np.pi**3)**.25)*np.exp(1j*phase)
    return precision,factor

def gram(states):
    precision=np.array([x[0] for x in states],dtype=np.clongdouble)
    amp=np.array([x[1] for x in states])
    out=np.zeros((len(states),len(states)),complex)
    for i,m in enumerate(precision):
        A=m.conj()+precision.copy()
        root=np.ones(len(states),np.clongdouble)
        for j in range(3):
            pivot=A[:,j,j]
            assert np.all(pivot.real>0)
            root*=np.sqrt(pivot)
            if j<2:
                A[:,j+1:,j+1:]-=A[:,j+1:,j,None]*A[:,None,j,j+1:]/pivot[:,None,None]
        out[i]=amp[i].conj()*amp*(2*np.pi)**1.5/root
    herm=float(np.max(abs(out-out.conj().T))); diag=abs(np.diag(out)-1)
    if herm>=2e-8 or np.max(diag)>=2e-8:
        raise ValueError((herm,[(int(i),float(diag[i])) for i in np.argsort(diag)[-8:]]))
    assert np.linalg.eigvalsh(out).min()>-1e-7
    return (out+out.conj().T)/2

def setup(code):
    _,center,r,eps,_,_=template(code)
    _,rows,rhs=support.system(code)
    f0=-np.array(rhs[-7:],float)
    A=np.array(rows,float)[-7:,:7]
    return np.array([float(center[v]) for v in I]),float(r),float(eps),f0,A,edges(code)
