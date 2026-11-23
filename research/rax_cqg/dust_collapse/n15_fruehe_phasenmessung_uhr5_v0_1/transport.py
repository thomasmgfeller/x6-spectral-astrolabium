"""Persistence of a measured clock-packet subspace through the next contraction."""
import argparse
from fractions import Fraction as F
import json
import numpy as np
from modelltest import ROOT,EDGES,E,K,H,DX,I,INNER_MEANS,clocks,dwell,require,run as prefix_bounds
from messung import study,local,D,X0,SPLIT,nodes


def centre_phase(z,t,d):
    u=INNER_MEANS.copy();u[0]+=z;u[1]+=t+d
    y=clocks(E,u);f=dwell(u)
    return sum(f[j]*(-F(1,2)-sum(F(b,38)*(y[j]-y[i])**2 for (i,end),b in EDGES.items() if end==j))
               for j in (4,5,6))


def algebra():
    # Multidegree <=3 in each variable. Four values on each axis prove the cubic identity.
    pts=(F(-1,31),F(0),F(1,113),F(2,47))
    for z in pts:
        for t in pts:
            for d in pts:
                diff=centre_phase(z,t,d)-centre_phase(z,t,-d)-centre_phase(0,t,d)+centre_phase(0,t,-d)
                require(diff==-F(15,2432)*d*z*(660*z-389),'Phasendrift')
    def drift(z):return -F(15,2432)*z*(660*z-389)/(72*K**2)
    lo,hi=drift(-F(1,64)),drift(F(1,64))
    require(lo<0<hi and max(-lo,hi)<F(1,25000),'Driftintervall')
    v=F(prefix_bounds()['visibility_lower'])
    kmin,kmax=(1-4*H)/304,(1+4*H)/304
    a=kmin*(DX-H)
    b=F(1,25000)+kmax*(DX+H)
    gap=v*(1-b*b/2)*(a-a**3/6)
    require(gap>F(14,10**7),'Bitabstand')
    return {'polynomial_checks':64,'drift_interval':list(map(str,[lo,hi])),
            'early_gap_lower_for_shared_spectator_weights':I.of(gap).rounded(13)[0]}


def wave_tests():
    q,w=nodes('gauss',14);ww=w[:,None]*w[None,:]
    z4=q[:,None]
    error=diff_error=0.;cases=0
    for t in (-float(H),.3*float(H),float(H)):
        def cal(z):
            am,gm,*_=local('gauss',-1,z,t,0);ap,gp,*_=local('gauss',1,z,t,0)
            return ap*am.conjugate()/np.abs(ap*am)*np.exp(1j*(gp-gm)*X0)
        fixed,adapted=cal(0.),cal(z4)
        for u12 in (.625-1/1024,.625+1/1024):
            x=(u12-.375)/2*(1+.01*q[None,:])
            y4=-1.75+3.75*(.125+z4/64)
            y12=-1.75+3.75*u12
            left=[1+.8*z4+.5j*x,.37+np.exp(.4j*z4)*(x+.2)]
            for x12 in (.125,.1255):
                advance=4*x12*(u12-.25-t)/171
                for pulse in (-1,0,1):
                    right=[]
                    for arm in (-1,1):
                        y5=-1.75+3.75*(.25+t+arm*SPLIT)
                        y6=-1.75+3.75*.375+pulse/(8*np.sqrt(D))
                        y11=-1.75+3.75*.5
                        c=-.5
                        for b,yi in ((-8,y4),(16,y5),(-9,y6),(1,y11)):
                            c=c-(b/38)*(y12-yi)**2
                        right.append(np.exp(1j*D*x12*c))
                    def push(v):return np.array([np.sum(ww*r*h) for h,r in zip(v,right)])
                    def mix(v,p):return [-1j*np.conj(p)*v[1],1j*p*v[0]]
                    after=np.asarray(mix(push(left),fixed*np.exp(1j*advance)))
                    error=max(error,float(np.max(abs(push(mix(left,fixed))-after))))
                    diff_error=max(diff_error,float(np.max(abs(push(mix(left,adapted))-after))))
                    cases+=1
    require(error<5e-14 and diff_error>1e-8,'Verklebung')
    return {'test_waves_and_continuations':cases,'fixed_mixer_max_residual':error,
            'adapted_vs_fixed_witness':diff_error}


def run():
    early={}
    for method,n in (('gauss',20),('cc',21)):
        row=study(method,n,0,fixed=True)['1.0']
        early[method]={k:row[k] for k in ('early_plus_low','early_plus_high','B_high_minus_low')}
    require(abs(early['gauss']['early_plus_high']-early['cc']['early_plus_high'])<1e-13,'Quadratur')
    return {'algebra':algebra(),'measurements':early,'transport':wave_tests()}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args();res=run()
    if args.json: print(json.dumps(res,indent=2,default=float))
    else:
        ref=json.loads((ROOT/'transport.json').read_text())
        require(res['algebra']==ref['algebra'],'Algebra')
        for method,row in res['measurements'].items():
            for k,v in row.items():require(abs(v-ref['measurements'][method][k])<2e-13,'Archiv')
        print('PASS · Übertragung der Ergebnisräume bis hinter 12')
