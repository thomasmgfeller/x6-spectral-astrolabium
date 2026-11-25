"""Certified phase-to-density readouts for the second PR 369 packet pair."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'basis'))
from versuch import (I,S,D,H,EPS,NOISE,ETA,Q0,INNER,PAST,FUTURE,ORDER,EDGES,
                     HIDDEN,STEP,W0,box_data,box,decimals,coeffs)
from ordnung import source_parts

ZERO=(0,0,0,0,0,0)
V=dict(zip(PAST,(F(76,64),F(47,64),F(24,64),F(8,64))))
C={7:-127,8:240,9:-120}
LIMIT=F(2047,2048)

def setting(i,s,j=None,t=0):
    key=list(ZERO)
    key[i]=s
    if j is not None:
        key[j]=t
    return tuple(key)

def stencils():
    # All quantities are relative phases. Phi(0)=0 exactly.
    mass={}
    for s in (-1,1):
        mass[setting(4,s)]=s/(2*H)
        mass[setting(0,s)]=-19/H**2
        mass[setting(1,s)]=285/H**2
        for t in (-1,1):
            mass[setting(0,s,1,t)]=-F(190,9)*s*t/(4*H**2)
            mass[setting(2,s,3,t)]=19*s*t/(4*H**2)
    local={setting(5,s):F(19,8)/H**2 for s in (-1,1)}
    return {'summe':mass,'dichte12':local}

def source_vector(mode):
    a,b,u,v,_,_=mode
    return {**{j:u+v*V[j] for j in PAST},11:a,13:b}

def state(arm,side):
    y,c,d,f,x=box_data(arm)
    q=sum(c[j]*d[j] for j in HIDDEN)
    shape={j:Q0*d[j]/q for j in HIDDEN}
    x={j:t+side*EPS*shape.get(j,0) for j,t in x.items()}
    w={j:D*x[j] for j in INNER}
    w.update({j:box(W0-ETA,W0+ETA) for j in FUTURE})
    return y,w,shape

def phase(data,mode):
    y,w,_=data
    c0=coeffs(y)
    coeff=dict(c0)
    v=source_vector(mode)
    # The local copy of clock 4 is changed only on crossing edge (4,12).
    for (i,j),b in EDGES.items():
        delta=(v.get(j,0)-v.get(i,0)-(mode[5] if (i,j)==(4,12) else 0))*STEP
        coeff[j]-=F(b,38)*delta*(2*(y[j]-y[i])+delta)
    phase=sum(w[j]*coeff[j] for j in w)
    phase+=mode[4]*H*sum(c*w[j] for j,c in C.items())/D
    inlet=sum(coeff[j] for j in PAST)
    assert inlet.absmax()<32*S  # real and positive sinc(inlet/32)
    return phase,inlet

def bound_arm(cells,mode):
    # For fixed future z, each factor is the integral over its own past.
    # The two clock-5 components have equal weight. Taking the product Zs Z0*
    # produces four equally weighted lobe pairs before the final z integral.
    on=[phase(cell,mode) for cell in cells]
    off=[phase(cell,ZERO) for cell in cells]
    lobes=[p-r for p,_ in on for r,_ in off]
    mean=sum(lobes)/4
    radius=max(F((z-mean).absmax(),S) for z in lobes)
    assert radius<1
    coslower=1-radius**2/2
    err=radius**3/(6*coslower)
    inlet=on[0][1]-off[0][1]
    for rho in (F(1,8),F(1,4)):
        assert (mean+rho*inlet).absmax()+I.of(err).hi<I.of(1).lo
    return err,radius,coslower

def check_stencil():
    # Complete fine action on each unit density, independently by past-distance
    # counting and rational source strength. Here D=1; rescaling restores x=w/D.
    y={j:F(k*k-3*k+9,67) for k,j in enumerate(ORDER)}
    def coeff(j,mode,forget=False):
        v=source_vector(mode)
        jpos=ORDER.index(j)
        total=F(-1,2)
        for k,i in enumerate(ORDER[:jpos]):
            n=jpos-k-1
            if n>=4:continue
            shift=v.get(j,0)-(0 if forget and i==11 else v.get(i,0))
            if i==4 and jpos>ORDER.index(11):shift-=mode[5]
            total-=F((1,-9,16,-8)[n],38)*(y[j]-y[i]+H*shift)**2
        return total+mode[4]*H*C.get(j,0)
    for name,table in stencils().items():
        for j in ORDER:
            got=sum(a*(coeff(j,k)-coeff(j,ZERO)) for k,a in table.items())
            assert got==int(j in INNER if name=='summe' else j==12),(name,j,got)
    mass=stencils()['summe']
    lost={12:1,13:1,14:16,7:-8}
    for j in ORDER:
        bad=sum(a*(coeff(j,k,True)-coeff(j,ZERO,True)) for k,a in mass.items())
        assert int(j in INNER)-bad==lost.get(j,0)
    for j in ORDER:
        corr=sum(s*t*coeff(j,setting(0,s,1,t)) for s,t in product((-1,1),repeat=2))/(4*H**2)
        bad=sum(s*t*coeff(j,setting(0,s,1,t),True) for s,t in product((-1,1),repeat=2))/(4*H**2)
        assert corr==F(-9,19)*int(j==13) and bad==0
    assert (STEP/F(15,4)+F(1,2**22)).hi<I.of(F(7,128)).lo
    cross=[(i,j) for i,j in EDGES if i==4 and ORDER.index(j)>ORDER.index(11)]
    assert cross==[(4,12)] and EDGES[4,12]==-8
    v,h=source_parts(EDGES)
    assert all(v[j]+h[j]==int(j in INNER) for j in ORDER)

def run():
    check_stencil()
    rows={}
    for side,label in [(-1,'niedrig'),(1,'hoch')]:
        cells=[state(arm,side) for arm in (-1,1)]
        # Mean of every jitter is zero and the unshifted midpoint widths
        # telescope. Equal lobe volumes. Only the nonlinear Q0/q remains.
        shapes=[cell[2] for cell in cells]
        expected={'summe':I.of(LIMIT)+side*EPS*sum(sum(a.values()) for a in shapes)/2,
                  'dichte12':I.of(W0)+side*EPS*sum(a[12] for a in shapes)/2}
        row={}
        for name,table in stencils().items():
            error=F(0); maxradius=F(0); mincoherence=F(1)
            for mode,weight in table.items():
                err,r,coh=bound_arm(cells,mode)
                error+=abs(weight)*err
                maxradius=max(maxradius,r);mincoherence=min(mincoherence,coh)
            result=expected[name]+box(-error,error)
            cut=LIMIT if name=='summe' else W0
            margin=side*(result-cut)
            assert margin.lo>0,(name,label,decimals(result),float(error))
            weights=sum(map(abs,table.values()))
            row[name]={'mean':decimals(expected[name]),'readout':decimals(result),
                       'phase_bias_bound':decimals(I.of(error))[1],
                       'max_phase_spread_rad':decimals(I.of(maxradius))[1],
                       'margin_at_threshold':decimals(margin)[0],
                       'phase_error_tolerance_rad':decimals(margin/weights,15)[0],
                       'sum_abs_stencil_weights':str(weights),
                       'coherence_after_inlet_factor_lower':decimals(I.of(mincoherence))[0]}
        rows[label]=row
    return rows


def binary_test():
    from intervalle import C as Complex, cis, sinc
    # Remove the class-dependent global phase, which is common to both
    # settings. The unshifted bulk integrand is then the neutral one.
    amps=[]
    for lobe in (-1,1):
        y,c,d,_,x=box_data(lobe)
        full=coeffs(y)
        q=sum(c[j]*d[j] for j in HIDDEN)
        separation=EPS*D*Q0*d[12]/q
        w={j:D*x[j] for j in INNER}
        w.update({j:box(W0-ETA,W0+ETA) for j in FUTURE})
        neutral=sum(w[j]*full[j] for j in w)
        delta=F(-8,38)*STEP*(2*(y[12]-y[4])-STEP)
        odd=separation*delta
        base=cis(neutral)
        active=base*cis(w[12]*delta)
        amps.append((base,active*cis(-odd),active*cis(odd),active*Complex(0,2*odd*sinc(odd))))
    a,lo,hi,db=[(left+right).scale(F(1,2)) for left,right in zip(*amps)]
    def norm(z):
        return (z.conj()*z).re
    nlo=norm(a)+norm(lo)
    nhi=norm(a)+norm(hi)
    assert min(nlo.lo,nhi.lo)>0
    diff=((a.conj()*db).im-(a.conj()*lo).im/nlo*((hi+lo).conj()*db).re)/nhi
    assert diff.hi<0
    return {'P_plus_high_minus_low':decimals(diff),
            'equal_prior_accuracy_percent_fixed_reversed_assignment':decimals(50*(1-diff),10),
            'fully_dephased_P_plus':'1/2'}

def support_control():
    rows={}
    for arm in (-1,1):
        y,c,d,_,_=box_data(arm)
        q=sum(c[j]*d[j] for j in HIDDEN)
        for sign in (-1,1):
            t=sign*STEP
            # Of the three hidden coefficients only c12 contains Y4.
            dc=F(-8,38)*t*(2*(y[12]-y[4])-t)
            assert q.hi<0 and (q+dc).hi<0
            signed=-EPS*Q0*dc/(q*(q+dc))
            distance=signed if signed.lo>0 else -signed
            gap=distance-2*NOISE
            assert gap.lo>0
            rows[f'{arm},{sign}']={'absolute_shift_x12':decimals(distance),
                                   'clear_gap_x12':decimals(gap)}
    return rows


def results():
    return {'phase_readouts':run(),'single_output':binary_test(),'shifted_selection':support_control()}

if __name__=='__main__':
    print(json.dumps(results(),indent=2,sort_keys=True))
