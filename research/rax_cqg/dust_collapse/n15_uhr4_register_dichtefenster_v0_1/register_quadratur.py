"""Numerical sequential full phases, rebuilding the three late density centers in each arm."""
from pathlib import Path
from itertools import product
import cmath
import math
import sys

ORDER=(0,1,2,3,4,5,6,11,12,13,14,7,8,9,10)
D=3.75*(3/722)**.25
CENTER=-1.75+3.75/8
R=3.75/2**22
EPS=2**-14

def nodes(n,dim):
    for k in range(1,n+1):
        point=[]
        for p in (2,3,5,7,11,13,17)[:dim]:
            u=0.;place=1./p;i=k
            while i:
                i,m=divmod(i,p);u+=place*m;place/=p
            point.append(2*u-1)
        yield point
        yield [-z for z in point]

def sinc(x):
    return math.sin(x)/x if x else 1.

def swap(x,lo,hi,t):
    # Half-open intervals give an involution also at shared boundaries.
    if lo<=x<hi: return x+t
    if lo+t<=x<hi+t: return x-t
    return x

def coeff(y,passed):
    memory=[];out=[]
    for j,clock in zip(ORDER,y):
        v=-.5
        for b,(_,old) in zip((1,-9,16,-8),reversed(memory)):
            v-=b*(clock-old)**2/38
        out.append(v)
        memory=(memory+[(j,clock)])[-4:]
        if j==11:
            assert [i for i,_ in memory]==[4,5,6,11]
            memory[0]=(4,passed)
    return out

def evaluate(mode,tiny,nz,nu):
    spec=R if tiny else 1/32/math.sqrt(D)
    lo=CENTER-R;hi=CENTER if tiny else CENTER+R
    pulses=(0,1) if tiny else (0,1,-1)
    totals={(rho,side):{p:[0j,0.] for p in pulses} for rho,side in product((.125,.25),(-1,1))}
    for z in nodes(nz,7):
        wf=[.125+v/2**20 for v in z[3:]]
        amps={key:dict.fromkeys(pulses,0j) for key in totals}
        for uv,lobe in product(nodes(nu,6),(-1,1)):
            g=iter(uv)
            u=[j/8+(next(g)/2**22 if j!=3 else 0) for j in range(1,8)]
            u[0]=((hi+lo)/2+uv[0]*(hi-lo)/2+1.75)/3.75
            u[1]+=lobe/1000
            y=[-5.,-4.,-3.,-1.75]+[-1.75+3.75*a for a in u]+[2.,3+z[0]/2**20,4+z[1]/2**20,5+z[2]/2**20]
            y4=y[4]
            faces=[0]+[(a+b)/2 for a,b in zip(u,u[1:])]+[1.]
            f=[b-a for a,b in zip(faces,faces[1:])];f[3]=255/2048
            # Solve the pulse-null equations for the hidden density triple.
            a,b,c=y[8:11]
            n13=-(-9)*(a-c)/(16*(b-c))
            n=(1.,n13,(-9+16*n13)/8)
            for p in pulses:
                actual=swap(y4,lo,hi,p*spec) if p else y4
                if p: assert abs(swap(actual,lo,hi,p*spec)-y4)<2e-15
                assert abs(actual-(y4+p*spec))<2e-15
                read_y={'gemeinsam':actual,'wirkungsquelle':y4,'festes_profil':CENTER}[mode]
                assignment=coeff(y,read_y)
                q=sum(v*w for v,w in zip(n,assignment[8:11]))
                dynamic=coeff(y,actual)
                past=sum(dynamic[:4])
                scale=sinc(past/32)*math.prod(sinc(D*b/2**20) for b in dynamic[4:11])
                for rho,side in amps:
                    x=f.copy()
                    for j,v in enumerate(n,4): x[j]+=side*EPS*(-1.25)*v/q
                    phase=rho*past+D*sum(i*j for i,j in zip(x,dynamic[4:11]))+sum(i*j for i,j in zip(wf,dynamic[11:]))
                    amps[rho,side][p]+=scale*cmath.exp(1j*phase)/(4*nu)
        for key,zp in amps.items():
            a=zp[0]
            for p,b in zp.items():
                real=(abs(a+b)**2-abs(a-b)**2)/4
                imag=(abs(a-1j*b)**2-abs(a+1j*b)**2)/4
                totals[key][p][0]+=complex(real,imag)/(2*nz)
                totals[key][p][1]+=(abs(a)**2+abs(b)**2)/(2*nz)
    rows={}
    for rho in (.125,.25):
        prob=[];density=[]
        for s in (-1,1):
            z=totals[rho,s]
            b,k=z[1]
            prob.append(.5+b.imag/k)
            if not tiny:
                density.append(19/8*32**2*(cmath.phase(z[1][0])+cmath.phase(z[-1][0])))
        rows[str(rho)]={'P_plus_niedrig_hoch':prob,'differenz':prob[1]-prob[0],'dichte_niedrig_hoch':density}
    return rows


def check(cert):
    results={}
    for nz,nu in ((3,4),(5,10)):
        grid={}
        for scale,tiny in [('breites_uhrfenster',False),('beide_pakethaelften',True)]:
            grid[scale]={}
            for mode,entry in cert['zwei_arme'][scale].items():
                rows=evaluate(mode,tiny,nz,nu)
                pl,ph=map(float,entry['P_plus_hoch_minus_niedrig'])
                for row in rows.values():
                    # Direct floating subtraction at 1e-11 may cost a few ulps.
                    assert pl-2e-15<=row['differenz']<=ph+2e-15
                    for lab,v in zip(('niedrig','hoch'),row['dichte_niedrig_hoch']):
                        a,b=map(float,cert['drei_stellungen'][mode][lab]['anzeige'])
                        assert a<=v<=b
                grid[scale][mode]=rows
        results[f'{2*nz}x{2*nu}']=grid
    return results
