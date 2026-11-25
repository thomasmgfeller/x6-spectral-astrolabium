"""Independent Gauss sums of the complex charge, clock faces and finite-pulse arms."""
from decimal import Decimal as D, localcontext
from itertools import product
from pathlib import Path
import json
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from pruefung import I,P,FUT,support,variation,encode
from paketbreite import ideals

REL=support.geometry(1767356)[1]
EDGES=[(a,b,k) for a,b,k in variation.edges(encode(REL,15),15) if k]
REGIONS=ideals(REL)
U=[a for a,b,c in EDGES]; V=[b for a,b,c in EDGES]
B=np.array([c for a,b,c in EDGES])
REGMAT=np.array([[c if a in reg and b not in reg else 0 for reg in REGIONS] for a,b,c in EDGES])
H=1/64


def fields(e):
    # Reconstruct from original, unshifted edge polynomials at 60 decimal digits.
    with localcontext() as ctx:
        ctx.prec=60
        yd={i:D(i-5) for i in P+FUT}
        yd[3]+=D(str(e))
        wd={i:D(1)/(8 if i in P else 64) for i in P+FUT}
        for j in I:
            row=[(i,c) for i,k,c in EDGES if k==j]
            a=sum(c for i,c in row)
            h=sum(c*yd[i] for i,c in row)
            z=19+sum(c*yd[i]**2 for i,c in row)
            yd[j]=(z/(2*h) if a==0 else (h+(1 if j==11 else -1)*(h*h-a*z).sqrt())/a)
        for j in reversed(I):
            h=sum(c*(yd[i]-yd[j]) for i,k,c in EDGES if k==j)
            wd[j]=-sum(c*wd[k]*(yd[k]-yd[j]) for i,k,c in EDGES if i==j)/h
        for j in I:
            norm=19+sum(c*(yd[i]-yd[j])**2 for i,k,c in EDGES if k==j)
            grad=wd[j]*sum(c*(yd[i]-yd[j]) for i,k,c in EDGES if k==j)
            grad+=sum(c*wd[k]*(yd[k]-yd[j]) for i,k,c in EDGES if i==j)
            assert max(abs(norm),abs(grad)) < D('1e-52')
        return np.array([float(yd[i]) for i in range(15)]),np.array([float(wd[i]) for i in range(15)])


def tensor(order,dim):
    x,b=leggauss(order)
    ids=np.array(list(product(range(order),repeat=dim)))
    return x[ids],np.prod(b[ids]/2,axis=1)


def density_factors(beta):
    # Closed uniform density integrals. Stable small-argument series also for I0-1.
    assert np.max(np.abs(beta))<.01
    s=beta**2
    minus=s*(-1/6+s*(1/120+s*(-1/5040+s/362880)))
    i0m1=np.expm1(np.log1p(minus).sum(axis=1))
    langevin=beta*(1/3+s*(1/45+s*(2/945+s/4725)))
    return i0m1,langevin


def evaluate(y,w,hw,yoff,need_charge=False,pulse=False):
    dy=yoff[:,U]-yoff[:,V]
    y0diff=y[U]-y[V]
    deltas=B*(2*y0diff*dy+dy**2)
    # The clock-linear term vanishes only for inner translations at the central saddle.
    theta=-(deltas if pulse else B*dy**2) @ w[V]/38
    beta=np.stack([-hw[j]*deltas[:,np.array(V)==j].sum(axis=1)/38 for j in I],axis=1)
    i0m1,lv=density_factors(beta)
    cos_m1=-2*np.sin(theta/2)**2
    sin_t=np.sin(theta)
    amp_m1=(i0m1+(1+i0m1)*cos_m1)+1j*((1+i0m1)*sin_t)
    if not need_charge:
        # Density-integrated exp(i*s)-1-i*s, used on clock faces. Its subtraction
        # integrates to zero in the upper-minus-lower face difference at stationarity.
        sin_remainder=theta**3*(-1/6+theta**2*(1/120-theta**2/5040))
        face=(i0m1+(1+i0m1)*cos_m1)+1j*(sin_remainder+i0m1*sin_t)
        return amp_m1,face
    all_d=y0diff+dy
    charged=(all_d*w[V])@REGMAT
    density_moment=np.zeros_like(charged)
    for n,j in enumerate(I):
        mask=np.array(V)==j
        density_moment+=((all_d[:,mask]@REGMAT[mask])*hw[j])*lv[:,n,None]
    insertion=(1+amp_m1[:,None])*(charged+1j*density_moment)
    # Conditional E[q_A-q_P]=0. Subtract this analytic zero to retain the small signal.
    delta_charge=charged-charged[:,[0]]
    delta_density=density_moment-density_moment[:,[0]]
    residual=delta_charge*amp_m1[:,None]+1j*delta_density*(1+amp_m1[:,None])
    return amp_m1,insertion,residual


def quadrature(level,order,with_pulses=True):
    grid,wt=tensor(order,7)
    fg,fw=tensor(order,6)
    ex,ew=leggauss(order)
    phase_z=0j; b_p=0j; jac_sum=0.
    vol=np.zeros(15,dtype=complex); ward=vol.copy(); probed=vol.copy()
    for v,weight in zip(ex,ew):
        e=1/6+v/2**22
        y,w=fields(e)
        hy=(4-e)/(64*2**level)
        hw=w/(100*2**level)
        jac=(2*hy)**7*np.prod(2*hw[list(I)])*weight/2
        jac_sum+=jac
        phase0=-np.sum(w)/2-np.sum(B*w[V]*(y[U]-y[V])**2)/38
        scale=jac*np.exp(1j*phase0)
        yoff=np.zeros((len(grid),15));yoff[:,I]=hy*grid
        amplitude,charge,delta=evaluate(y,w,hw,yoff,True)
        phase_z+=scale*(1+wt@amplitude)
        b_p+=scale*(wt@charge[:,0])
        vol+=scale*(wt@delta)
        face_terms={}
        for j in I:
            other=[i for i in I if i!=j]
            d=np.zeros((len(fg),15));d[:,other]=hy*fg
            d[:,j]=hy
            plus=evaluate(y,w,hw,d)[1]
            d[:,j]=-hy
            minus=evaluate(y,w,hw,d)[1]
            face_terms[j]=19j*(fw@(plus-minus))/(2*hy)
        ward+=scale*np.array([sum(face_terms[j] for j in region if j in I) for region in REGIONS])
        if with_pulses:
            for k,region in enumerate(REGIONS):
                d=yoff.copy()
                d[:,sorted(region)]-=H
                am=evaluate(y,w,hw,d,pulse=True)[0]
                d[:,sorted(region)]+=2*H
                ap=evaluate(y,w,hw,d,pulse=True)[0]
                probed[k]+=scale*19*(wt@(am-ap))/(2j*H)
    assert min(jac_sum,abs(phase_z),abs(b_p))>0
    def pair(z):
        return [float(z.real),float(z.imag)]
    rows={}
    for k,region in enumerate(REGIONS):
        rows[','.join(map(str,sorted(region-set(P)))) or 'Eingang']={
            'volume_relative':pair(vol[k]/b_p),'face_relative':pair(ward[k]/b_p),
            'finite_relative':pair((probed[k]-probed[0])/probed[0]) if with_pulses else None}
    return {'order':order,'coherent_inlet':pair(b_p/phase_z),'modulus_Z_per_measure':abs(phase_z)/jac_sum,
            'max_volume_face_gap':float(np.max(np.abs(vol-ward))/abs(b_p)),
            'max_relative_volume':float(np.max(np.abs(vol))/abs(b_p)),
            'max_relative_finite':float(np.max(np.abs(probed-probed[0]))/abs(probed[0])) if with_pulses else None,
            'cuts':rows}


def run():
    runs={}
    for level in range(4):
        # Independent face and volume integral; use orders 3 and 4 and a finite-pulse replay at order 3.
        runs[str(level)]=[quadrature(level,3),quadrature(level,4,False)]
    return runs


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
