"""Certified two-mode transfer and end intensity bounds on the published N15 chain."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from registertest import (cell,amplitudes,CENTER,R,H,D,K,EPS,Q0,I,S,ORDER,
                          EDGES,C,decimals)
from versuch import NOISE
from intervalle import cis,sinc
A=F(8,38)
Z0=F(-7,4)+K*F(5,8)

def upper(z):
    return F(I.of(z).hi,S)

def radius(z):
    return F(z.hi-z.lo,2*S)

def middle(z):
    return F(z.hi+z.lo,2*S)

def hull(terms):
    return I(min(v.lo for v in terms),max(v.hi for v in terms))

def above(x,digits=22):
    return decimals(I.of(x),digits)[1]

def verify_kernel():
    assert [(i,j,b) for (i,j),b in EDGES.items() if i==4 and ORDER.index(j)>ORDER.index(11)]==[(4,12,-8)]
    incoming={i:b for (i,j),b in EDGES.items() if j==12}
    assert incoming=={4:-8,5:16,6:-9,11:1} and sum(incoming.values())==0
    left=ORDER[:ORDER.index(11)+1]
    right=ORDER[ORDER.index(11)+1:]
    count=0
    for off in (F(-2,7),F(0),F(3,8)):
        y={j:F(k,5)+off*(j%3)/23 for k,j in enumerate(ORDER)}
        for j in right:
            for t in (F(-1,32),F(1,32),F(1,7)):
                k=ORDER.index(j)
                def direct(passed):
                    prev={**y,4:passed}
                    return -F(1,2)-sum(F(b,38)*(y[j]-prev[ORDER[k-m]])**2
                                        for m,b in enumerate((1,-9,16,-8),1))
                delta=direct(y[4]+t)-direct(y[4])
                want=A*t*(t-2*(y[12]-y[4])) if j==12 else 0
                assert delta==want
                count+=1
    assert left[-4:]==(4,5,6,11)
    return count

def port_bounds(c,r,t,wrange,zradius):
    wc=middle(wrange)
    t=I.of(t)
    reference=A*wc*t*(t-2*(Z0-c))
    # For every true input displacement v in [-r,r], subtract a single
    # constant packet-to-packet phase before bounding the wave difference.
    err=upper(A*t*(radius(wrange)*(-(t-2*(Z0-c)))+2*upper(wrange)*(zradius+r)))
    assert err>0 and (t-2*(Z0-c)).hi<0
    maxgap=abs(Z0-c)+zradius+upper(t)
    wiggle=A*upper(wrange)*r*(2*maxgap+r)
    cosine=1-wiggle**2/2
    assert cosine>F(999,1000)
    trace=err/cosine
    ratio=err/(2*cosine-err)
    return {'w_range':decimals(wrange),'reference_phase_rad':decimals(reference,15),
            'uniform_wave_error':above(err),'trace_distance_upper':above(trace),
            'optimal_input_window_accuracy_percent_upper':above(50*(1+trace),13),
            'sigma_min_over_max_upper':above(ratio),
            'squared_singular_ratio_upper':above(ratio*ratio,36)}

def birth():
    data=[cell(lobe,-R,R) for lobe in (-1,1)]
    rows={}
    for name,c,r,t in [('breit',CENTER,R,H/D.sqrt()),('benachbart',CENTER-R/2,R/2,R)]:
        row={}
        for side,label in ((-1,'niedrige_dichte'),(1,'hohe_dichte')):
            w=hull([D*(v[3][12]+side*EPS*Q0/v[7]) for v in data])
            row[label]=port_bounds(c,r,t,w,R)
        row['geoeffnete_dichte_und_uhr']=port_bounds(c,r,t,I(0,S),K/64)
        rows[name]=row
    return rows

def masked_end(mode,parts,wide):
    packets=[]
    for side in (-1,1):
        acc=[C(0) for _ in range(3)]
        if wide:
            shift=I.of(0) if side<0 else H/D.sqrt()
            origin=-R+shift
            length=2*R
        else:
            origin=-R if side<0 else F(0)
            length=R
        assert upper(I.of(origin+length)) < K/64 and I.of(origin).lo > -I.of(K/64).lo
        for lobe in (-1,1):
            for k in range(parts):
                v=cell(lobe,origin+length*k/parts,origin+length*(k+1)/parts)
                # True input clocks in each half, never substitute another
                # Y4 at the cut. Complete neutral phase and class phase.
                y,n,f,x,_,_,q,qs,_=v
                assert y[4].lo>y[3].hi and y[5].lo>y[4].hi
                den=q if mode=='gemeinsam' else qs
                for sign in (-1,1):
                    for j in f:
                        packet=x[j]+(sign*EPS*Q0*n[j]/den if j in (12,13,14) else 0)
                        assert (packet-F(99,100)*f[j]).lo>0 and (F(101,100)*f[j]-packet).lo>0
                        if j==12:
                            assert min((sign*(packet-F(1,8))).lo,(sign*(packet-f[j])).lo)>0
                vals=amplitudes(v,mode,I.of(0))
                acc=[a+b for a,b in zip(acc,vals)]
        packets.append([a.scale(F(1,2*parts)) for a in acc])
    lo0,hi0,da=packets[0]
    lo1,hi1,db=packets[1]
    def norm(a):return (a.conj()*a).re
    nlo,nhi=norm(lo0)+norm(lo1),norm(hi0)+norm(hi1)
    assert min(nlo.lo,nhi.lo)>0
    # P(label -i | common end success) = 1/2 + Im(L*H)/N.
    delta_j=(da.conj()*hi1+lo0.conj()*db).im
    delta_n=((hi0+lo0).conj()*da+(hi1+lo1).conj()*db).re
    delta=(delta_j-(lo0.conj()*lo1).im/nlo*delta_n)/nhi
    if mode=='gemeinsam': assert delta.lo==delta.hi==0
    else: assert delta.hi<0
    return {'delta_conditional_minus_i_label':decimals(delta,18),
            'accuracy_percent_common_success_equal_conditional_priors':decimals(50*(1-delta),14),
            'positive_denominator_lower':decimals(I(min(nlo.lo,nhi.lo),min(nlo.lo,nhi.lo)),7)[0]}

def selection_marker():
    # Alternative q(y): separate a change of the prepared density window from
    # true state transfer. At fixed remaining clocks both interval widths agree.
    out={}
    for name,start,end,step in [('breit',-R,R,H/D.sqrt()),('benachbart',-R,F(0),I.of(R))]:
        tv=[]
        for lobe in (-1,1):
            y,_,_,_,_,_,q,_,_=cell(lobe,start,end)
            dc=-A*step*(2*(y[12]-y[4])-step)
            diff=-EPS*Q0*dc/(q*(q+dc))
            gap=diff if diff.lo>0 else -diff
            tv.append(gap/(2*NOISE))
        distance=hull(tv)
        assert distance.lo>0 and distance.hi<S
        out[name]={'conditional_uniform_density_TV':decimals(distance,13),
                   'equal_prior_classical_input_window_accuracy_percent_paired_clocks':decimals(50*(1+distance),10)}
    return out


def equal_phase_rate():
    # Full, unshifted histories. Two genuine widely separated Y4 packets with
    # the same real input phase. Integrate the early common density analytically;
    # its factor cancels in the intensity ratio.
    ph=[]
    t=H/D.sqrt()
    for shift in (I.of(0),t):
        for lobe in (-1,1):
            y,d,f,x,w,neutral,q,qs,diff=cell(lobe,shift-R,shift+R)
            odd=D*EPS*Q0*diff/qs
            ph.append((neutral,odd))
    # Remove exactly the class-wide constant phases. Two independent inner
    # histories share z in the norm. Rectangles over both z's also enclose it.
    delta=I.of(0)
    lower=I.of(0)
    for a,oa in ph:
        for b,ob in ph:
            ds=a-b;dg=oa-ob
            delta-=2*ds*sinc(ds)*dg*sinc(dg)/16
            lower+=cis(ds-dg).re/16
    assert lower.lo>0 and delta.lo>0
    return {'relative_intensity_high_minus_low':decimals(delta/lower,17),
            'absolute_difference_per_common_squared_mass':decimals(delta,17)}

def run():
    return {'equal_phase_wide':equal_phase_rate(),'rational_action_checks':verify_kernel(),'birth':birth(),
            'phase_preparation':{name:{mode:masked_end(mode,parts,wide) for mode in ('gemeinsam','festes_profil')}
                                 for name,parts,wide in [('benachbart',32,False),('breit',4,True)]},
            'conditional_preparation_control':selection_marker()}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
