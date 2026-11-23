"""Prefix bit and ordinary future amplitudes with a retained classical outcome."""
import argparse
import json
from math import pi, sqrt
import numpy as np
from numpy.polynomial.legendre import leggauss
from modelltest import ROOT, SRC, ORDER, EDGES, INNER, PAST, require

DELTA=(3/722)**.25
K=3.75
D=K*DELTA
SPLIT=1/(72*D*K*K)
WIDTH=1/16384
X0=1/8
DX=1/2048
STRENGTHS=(0.,.5,1.)


def nodes(method,n):
    if method=='gauss':
        x,w=leggauss(n)
        return x,w/2
    x=np.cos(pi*np.arange(n)/(n-1))[::-1]
    k=np.arange(n)
    m=np.zeros(n)
    m[::2]=1/(1-k[::2]**2)
    return x,np.linalg.solve(np.cos(np.outer(k,np.arccos(x))),m)


def local(method,a,z4,t,pulse):
    u=[1/8+z4/64,.25+a*SPLIT+t,.375,.5,.625,.75,.875]
    faces=[0]+[(l+r)/2 for l,r in zip(u,u[1:])]+[1]
    f=dict(zip(INNER,[r-l for l,r in zip(faces,faces[1:])]))
    y={j:float(j-5) for j in PAST}
    y[3]+=.25
    y.update({j:y[3]+K*z for j,z in zip(INNER,u)})
    end=ORDER.index(13)
    c={j:-.5 for j in ORDER[:end+1]}
    step=pulse/(8*sqrt(D))
    if method=='gauss':
        for k,j in enumerate(ORDER[:end+1]):
            for lag,b in enumerate((1,-9,16,-8),1):
                if lag<=k:
                    i=ORDER[k-lag]
                    delta=y[j]-y[i]-(step if i==6 and j in (12,13) else 0)
                    c[j]=c[j]-b*delta**2/38
    else:
        for (i,j),b in EDGES.items():
            if j in c:c[j]=c[j]-b*(y[j]-y[i])**2/38
        for j in (12,13):
            c[j]=c[j]+EDGES[6,j]*(2*(y[j]-y[6])*step-step**2)/38
    wn,ww=leggauss(10)
    def uniform(centre,hw,g):
        if method=='gauss':return np.exp(1j*centre*g)*np.sinc(hw*g/pi)
        return sum(w/2*np.exp(1j*(centre+hw*n)*g) for n,w in zip(wn,ww))
    pref=1.
    for j in (4,5,6):
        pref=pref*f[j]*uniform(D*f[j],D*f[j]/100,c[j])
    right=f[12]*uniform(D*f[12],D*f[12]/100,c[12])*np.exp(1j*D/8*c[13])
    gamma=D*c[11]
    arm_wave={mark:pref*uniform(X0+mark*DX,WIDTH,gamma) for mark in (-1,1)}
    return pref,gamma,arm_wave,right,sum(c[j] for j in PAST)


def study(method,n,pulse,fixed=False):
    q,w=nodes(method,n)
    t=WIDTH*q[None,:]
    z4=q[:,None]
    weights=w[:,None]*w[None,:]
    def integrate(x):return np.sum(weights*x)
    am,gm,lm,rm,coll=local(method,-1,z4,t,pulse)
    ap,gp,lp,rp,_=local(method,1,z4,t,pulse)
    slope=4*(.25-t)/304
    require(np.max(np.abs((gp-gm)+slope))<1e-14,'Direkte Präfixphase')
    # U(1) phase of the off-diagonal mixer. Spectator controls are shared by both arms.
    cal=(ap*am.conjugate())/np.abs(ap*am)*np.exp(-1j*slope*X0)
    if fixed:
        left,_,_,_,_=local(method,-1,0.,t,pulse)
        right,_,_,_,_=local(method,1,0.,t,pulse)
        cal=(right*left.conjugate())/np.abs(right*left)*np.exp(-1j*slope*X0)
    norm=integrate(abs(am)**2+abs(ap)**2)
    aligned=2*am.conjugate()*ap*cal.conjugate()*np.exp(-1j*slope*X0)
    early={}
    for mark in (-1,1):
        av=integrate(np.imag(aligned*np.exp(-1j*slope*mark*DX))*np.sinc(WIDTH*slope/pi))/norm
        early[mark]=(1+av)/2
    out={}
    old=json.loads((SRC/'uhr5_ausgang.json').read_text())
    for eta in STRENGTHS:
        coeff=(1+sqrt(1-eta**2))/2
        balances={}; equal_intensities={}
        for mark in (-1,1):
            z0=integrate(rm*lm[mark]);z1=integrate(rp*lp[mark])
            w0=integrate(rp*(1j*cal)*lm[mark]);w1=integrate(rm*(-1j*cal.conjugate())*lp[mark])
            def intensity(theta):
                z=z0+theta*z1; za=w0+theta*w1
                direct=coeff*abs(z)**2+(1-coeff)*abs(za)**2
                # Explicit two outcomes sqrt(E_r), retained as orthogonal records.
                alpha=(sqrt((1+eta)/2)+sqrt((1-eta)/2))/2
                beta=(sqrt((1+eta)/2)-sqrt((1-eta)/2))/2
                separate=abs(alpha*z+beta*za)**2+abs(alpha*z-beta*za)**2
                require(abs(separate-direct)<1e-20,'Nichtselektive Summe')
                return direct
            i0,i1=intensity(-1j),intensity(1j)
            balances[mark]=(i0-i1)/(i0+i1)
            equal_intensities[mark]=intensity(1)/abs(z0+z1)**2
            if eta==0:
                for rho in (.125,.25):
                    common=abs(np.exp(1j*coll*rho)*np.sinc(coll/(32*pi)))**2
                    ref=old['gauss20'][f'{pulse}|{rho}']['intensities_common_scale'][str(mark)]
                    require(np.max(abs(np.array([i0,i1])*common-ref))<2e-19,'Originalausgang')
        out[str(eta)]={'early_plus_low':.5+eta*(early[-1]-.5),'early_plus_high':.5+eta*(early[1]-.5),
                       'B_high_minus_low':balances[1]-balances[-1],
                       'equal_phase_intensity_fraction_low':equal_intensities[-1],
                       'equal_phase_intensity_fraction_high':equal_intensities[1]}
    for eta in STRENGTHS:
        row=out[str(eta)]
        row['fraction_of_initial_B_difference']=row['B_high_minus_low']/out['0.0']['B_high_minus_low']
    return out


def run():
    gauss={str(p):study('gauss',20,p) for p in (0,1,-1)}
    cc={str(p):study('cc',21,p) for p in (0,1,-1)}
    delta=0
    for p in gauss:
        for eta,fields in gauss[p].items():
            for name,v in fields.items():
                tol=2e-8 if name=='fraction_of_initial_B_difference' else 2e-13
                diff=abs(v-cc[p][eta][name])
                require(diff<tol,'Quadraturvergleich '+name)
                if name=='B_high_minus_low': delta=max(delta,diff)
    return {'gauss':gauss,'cc':cc,'max_B_quadrature_difference':delta}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args();res=run()
    if args.json: print(json.dumps(res,indent=2,default=float))
    else:
        ref=json.loads((ROOT/'messung.json').read_text())
        for method in ('gauss','cc'):
            for pulse,rows in res[method].items():
                for eta,fields in rows.items():
                    for name,v in fields.items():
                        tol=2e-8 if name=='fraction_of_initial_B_difference' else 2e-13
                        require(abs(v-ref[method][pulse][eta][name])<tol,'Archiv '+name)
        print('PASS · Frühes Bit und spätere Rückwirkung, zwei Quadraturen und beide Pulsrichtungen')
