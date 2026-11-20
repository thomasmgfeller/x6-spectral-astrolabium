"""Calibrated tagged-flow controls and a charge window on the finite joint fields."""
from cmath import exp
from fractions import Fraction as F
from itertools import combinations
from math import sin, sqrt
from charge import P,I,FUT,ROOT,order,catalogue,row,delta,beta
import json

def tag_calibration():
    checked=0
    for mask in catalogue():
        rel,_=order(mask)
        nodes=(P[-1],)+I+(FUT[0],)
        covers=[(u,v) for u,v in rel if u in nodes and v in nodes and
                not any((u,z) in rel and (z,v) in rel for z in nodes)]
        forward={nodes[0]:1}
        back={nodes[-1]:1}
        for v in nodes[1:]: forward[v]=sum(forward[u] for u,z in covers if z==v)
        for u in reversed(nodes[:-1]): back[u]=sum(back[v] for z,v in covers if z==u)
        f={(u,v):F(forward[u]*back[v],forward[nodes[-1]]) for u,v in covers}
        T={v:F(pos,13) for pos,v in enumerate(nodes)}
        a=F(3,17)
        for mass in (F(0),F(1),F(1,4),F(4)):
            def phase(tau):
                return sum(mass*q*(T[v]+tau*(v in P)-T[u]-tau*(u in P)) for (u,v),q in f.items())
            assert phase(0)==mass*(T[nodes[-1]]-T[nodes[0]])
            assert (phase(-a/2)-phase(a/2))/a==mass
            checked+=1
    return {"calibration_controls":["0","1"],"validation_masses":["1/4","4"],"orders":1048,
            "exact_source_readings":checked,"reference_gain":"1","reference_offset":"0",
            "gain_for_coupled_P3_mass":None}

def selected_band(p0,c,lo,hi):
    if not lo<hi: raise ValueError("unordered limits")
    atom=lo<=p0<hi
    if c==0: return atom,(0.,1.) if atom else (0.,0.)
    l,r=sorted(((lo-p0)/c,(hi-p0)/c))
    a,b=max(0.,l),min(1.,r)
    return atom,(a,b) if b>a else (0.,0.)

def phase_integral(a,b,D):
    halfphase=D*(b-a)/4
    sinc=1 if halfphase==0 else sin(halfphase)/halfphase
    return (b-a)*exp(-1j*D*(a+b)/4)*sinc

def conditional_amplitude(p0,c,D,lo,hi):
    atom,(a,b)=selected_band(p0,c,lo,hi)
    return (atom+phase_integral(a,b,D))/2

def as_complex(z):
    return [format(float(x),".12g") for x in (z.real,z.imag)]

def test_selector():
    for c in (-7.,0.,7.):
        for D in (-3.,0.,4.):
            for p0 in (-1.,0.,.5,1.,2.):
                edges=(-20.,0.,.5,1.,20.)
                values=[conditional_amplitude(p0,c,D,l,h) for l,h in zip(edges,edges[1:])]
                assert abs(sum(values)-(1+phase_integral(0,1,D))/2)<1e-12
                for l,h in zip(edges,edges[1:]):
                    atom,(a,b)=selected_band(p0,c,l,h)
                    if b>a:
                        assert l<=p0+c*(a+b)/2<h
                    assert atom==(l<=p0<h)

def witness():
    # Deterministic choice: first canonical end type with a d=3 vertex, then the first such vertex.
    typ=next(mask for mask in catalogue() if 3 in order(mask)[1])
    rel,deg=order(typ)
    ix=deg.index(3);v=I[ix]
    Dlt=sqrt(2/(19*(4/sqrt(6))));B=4/sqrt(6)
    off=-1/16
    T={i:(i-5)*Dlt for i in P+FUT}
    T[3]+=off
    T[v]=1.5*Dlt
    for k,u in enumerate(I):
        if k<ix: T[u]=T[3]+(T[v]-T[3])*(k+1)/(ix+1)
        if k>ix: T[u]=T[v]+(T[7]-T[v])*(k-ix)/(len(I)-ix)
    assert all(T[u]<T[z] for u,z in rel)
    b={(u,z):((1,-9,16,-8)[n] if n<4 else 0) for u,z in rel
       for n in [sum((u,k) in rel and (k,z) in rel for k in range(15))]}
    c=B/2*sum(b[u,v]*(T[u]-T[v]) for u in P)
    assert abs(c-B/2*(28*Dlt-8*off))<1e-12 and c>4.04
    def D(z):return 1+B/2*sum(coef*(T[z]-T[u])**2 for (u,y),coef in b.items() if y==z)
    # Scalar field fixed at zero; actual gravity and fixed collar density phases included.
    F4=15-sum(b.values())
    S0=F4-sum(D(z)/16 for z in P+FUT)
    out={}
    bands=[(.2475,.2525),(3.96,4.04)]
    edges=[-20.,*(x for band in bands for x in band),20.]
    partition=sum(conditional_amplitude(0,c,D(v),l,h) for l,h in zip(edges,edges[1:]))
    assert abs(partition-(1+phase_integral(0,1,D(v)))/2)<1e-13
    for m,(lo,hi) in zip(("1/4","4"),bands):
        atom,(a,z)=selected_band(0,c,lo,hi)
        assert not atom and 0<a<z<1
        joint=(.5**6)*exp(1j*S0)*conditional_amplitude(0,c,D(v),lo,hi)
        n=128
        # Independent composite Simpson integration of the original single-history phase.
        f=lambda u:exp(1j*(S0-D(v)*u/2))
        step=(z-a)/n
        num=(f(a)+f(z)+sum((4 if k%2 else 2)*f(a+k*step) for k in range(1,n)))*step/(3*128)
        assert abs(num-joint)<1e-13
        out[m]={"window":[lo,hi],"selected_density_interval":[round(a,12),round(z,12)],
                "reference_measure_given_clocks_including_stratum":round((z-a)/128,15),
                "complex_amplitude_given_clocks_including_stratum":as_complex(joint)}
    return {"N15_end_type":typ,"active_inner_event":v,"other_six_inner_densities":"on their null atoms",
            "boundary_density":"1/8 on both collars","source_charge_per_unit_density":round(c,12),
            "causally_increasing_clocks":True,"scalar_field":"fixed to zero","F4":F4,"bands":out,
            "independent_integration":"128-panel composite Simpson within 1e-13 absolute",
            "scope":"Conditional density contraction including all seven density measures on the specified stratum; clocks fixed; no coherent integration over histories or clocks."}
