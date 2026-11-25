"""Two-way light calibration and transport of positive, comoving material probes."""
from fractions import Fraction as F
from math import sqrt, isqrt
from hashlib import sha256
from itertools import permutations
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys

MASS=(F(1,4),F(1),F(4))
TARGET=F(1,9200); BAND=(TARGET*F(199,200),TARGET*F(201,200))
STAMP=F(2,10**6); TICK=F(1,10**7); LAG=TICK
E0=STAMP+TICK/2; ERR=2*E0
FACTORS=(F('.96'),F('.985'),F(1),F('1.015'),F('1.04'),F('1.09'))
IDS=('L','H','V','B','S','K')
def root(x,n):
    scale=10**18; q=x.numerator*scale**n//x.denominator
    if n==2:k=isqrt(q)
    else:
        lo,hi=0,1
        while hi**n<=q:hi*=2
        while lo+1<hi:
            mid=(lo+hi)//2
            if mid**n<=q:lo=mid
            else:hi=mid
        k=lo
    a=F(k,scale)
    return a,a if a**n==x else a+F(1,scale)

def locate(bits):
    if len(bits)!=641 or not any(bits):return None
    j=max(i for i,b in enumerate(bits) if b)
    if j==640 or not all(bits[:j+1]):return None
    return j

def material_profile(m):
    # The exact LTB mass derivative has the sign of m*(1−(a/10)^2) inside.
    return [m>0 and F(13*i,640)<10 for i in range(641)]

def travel_bounds(a,theta):
    # Enclose EVERY ideal initial round trip, including the allowed delay.
    upper=2*(a+3*E0)*theta+LAG
    tmax=upper+E0
    assert tmax<F(3,1000) and F(225,1000)*E0<F(145,1000)*tmax
    scale=1-F(145,1000)*tmax
    # Metric dominates scale² times Euclidean initial metric globally.
    half=theta/2
    lower=4*a*(half-half**3/6)*scale
    return lower,upper

def echo_bounds(a,theta):
    lo,hi=travel_bounds(a,theta)
    # Instrument duration is difference of integer clock ticks.
    return -(-(lo-ERR)//TICK), (hi+ERR)//TICK

def decode(ticks,ratio,uncertainty):
    measured=ticks*TICK
    dtlo,dthi=measured-ERR,measured+ERR
    rlo=ratio*(10-uncertainty)-3*(E0+dthi)
    rhi=ratio*(10+uncertainty)+3*E0
    assert dtlo>LAG and rlo>7
    return (dtlo-LAG)/(2*rhi),dthi/(2*rlo)

def contained(v):
    return BAND[0]<=v[0]<=v[1]<=BAND[1]

def select(observations,ratio,uncertainty):
    if len({i for i,n in observations})!=len(observations):return 'UNGÜLTIG'
    certified=[i for i,n in observations if contained(decode(n,ratio,uncertainty))]
    if len(certified)==1:return certified[0]
    return 'KEINER' if not certified else 'MEHRDEUTIG'

def rates(phi,state,a0,m):
    # Affine-independent null ray parametrized by polar angle.
    t,offset,mu=state
    a=a0+offset
    if a<=10:q=m*(5-3*(a/10)**2)/2000;qp=-3*m*a/100000
    else:q=m/a**3;qp=-3*q/a
    s=sqrt(2*q);sp=qp/s; f=1-1.5*t*s
    R=a*f**(2/3)
    L=f**(2/3)-a*t*sp*f**(-1/3)
    rt=-a*s*f**(-1/3)
    lt=-(s+a*sp)*f**(-1/3)-a*t*s*sp/2*f**(-4/3)
    v=sqrt(1-mu*mu)
    return R/v,R*mu/(v*L),v*(1+R*(rt/R-lt/L)*mu)

def shoot(a,m,theta,start,steps):
    def integrate(mu):
        state=(start,0.,mu);h=theta/steps
        def inc(y,k,s):return tuple(v+s*t for v,t in zip(y,k))
        for n in range(steps):
            t=n*h
            k1=rates(t,state,a,m);k2=rates(t+h/2,inc(state,k1,h/2),a,m)
            k3=rates(t+h/2,inc(state,k2,h/2),a,m);k4=rates(t+h,inc(state,k3,h),a,m)
            state=tuple(v+h*(a1+2*a2+2*a3+a4)/6 for v,a1,a2,a3,a4 in zip(state,k1,k2,k3,k4))
        return state
    lo,hi=-2*theta,0.
    assert integrate(lo)[1]<0<integrate(hi)[1]
    for _ in range(39):
        mid=(lo+hi)/2
        if integrate(mid)[1]>0:hi=mid
        else:lo=mid
    result=integrate((lo+hi)/2)
    assert abs(result[1])<2e-15
    return result[0]

def measured_echo(a,m,t):
    out=[]
    for steps in (4,8):
        first=shoot(float(a),float(m),float(t),0.,steps)
        second=shoot(float(a),float(m),float(t),first,steps)
        out.append(second)
    assert abs(out[1]-out[0])<1e-13
    lower,upper=travel_bounds(a,t)
    assert float(lower)<=out[1]<=float(upper)
    rounded=round(out[1]/float(TICK))
    assert abs(out[1]/float(TICK)-rounded)<.49999
    return rounded

def late_radius(a,m,t):
    ma=m*(5*(a/10)**3-3*(a/10)**5)/2
    s=root(2*ma/a**3,2);sqrt5=root(F(5),2)
    factors=[1-F(3,2)*(5*t5/6+t)*sv for t5 in sqrt5 for sv in s]
    assert min(factors)>0
    return root(a**3*min(factors)**2,3)[0],root(a**3*max(factors)**2,3)[1]

def late(m,a,angle):
    out=[]
    for hard in (True,False):
        emit=STAMP if hard else -STAMP
        dt=F(1,1000)-2*emit
        lo,hi=late_radius(a,m,emit)
        assert lo-3*dt>7
        if hi*angle[1]<=dt:out.append('JA')
        elif (lo-3*dt)*angle[0]>dt:out.append('NEIN')
        else:out.append('UNBESTIMMT')
    return out

def archived_geometry():
    spec=spec_from_file_location('ltb_control',Path(__file__).resolve().parent/'basis/ltb.py')
    module=module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module

def reader(frame,uncertainty):
    if set(frame)!={'probe','initial_positive','final_positive','echo_ticks'}:
        raise ValueError('Unbekannte Datenfelder')
    i=locate([x=='1' for x in frame['initial_positive']])
    if i is None or locate([x=='1' for x in frame['final_positive']])!=i:return 'KEINE_MATERIALKLAMMER'
    return select(frame['echo_ticks'],F(13*i,6400),uncertainty)

def run():
    result={};raw=[];frames=[]
    model=archived_geometry()
    assert locate(material_profile(0)) is None
    for m in MASS:
        j=locate(material_profile(m));assert j==492
        a=F(13*j,640);ratio=a/10
        # Codes preassigned independently of the geometric distances.
        codes=sorted(IDS,key=lambda x:sha256(('Kennung|'+x).encode()).digest())
        obs=[];bounds={}
        for code,factor in zip(codes,FACTORS):
            rec=measured_echo(a,m,factor*TARGET)
            ticks=echo_bounds(a,factor*TARGET)
            assert ticks[0]<=rec<=ticks[1]
            obs.append((code,rec));bounds[code]=ticks
        early=[];late_sign=[]
        for aj in model.GRID:
            radii=[]
            for t,signs in ((0.,early),(model.END/2,late_sign)):
                rad,rho,jac,_=model.evolve(float(aj),t,float(m))
                assert jac>0
                signs.append(rho>0)
                radii.append(rad)
            if aj==a:
                lo,hi=late_radius(a,m,F(0))
                assert abs(radii[1]-float((lo+hi)/2))<1e-12
        assert early==late_sign==material_profile(m)
        def binary(bits):return ''.join('1' if v else '0' for v in bits)
        frame={'probe':str(len(frames)+1),'initial_positive':binary(early),
               'final_positive':binary(late_sign),'echo_ticks':sorted(obs)}
        frames.append(frame)
        actual=codes[2]
        eligible={}
        for err in (F(0),F('.01'),F('.1')):
            always=[];sometimes=[]
            for code,(lo,hi) in bounds.items():
                accepted=[n for n in range(lo,hi+1) if contained(decode(n,ratio,err))]
                if accepted:sometimes.append(code)
                if len(accepted)==hi-lo+1:always.append(code)
            winner=reader(frame,err)
            assert winner==select(obs,ratio,err)
            assert all(select(list(p),ratio,err)==winner for p in permutations(obs))
            eligible[str(err)]={'nominal':winner,'all_ticks':always,'some_ticks':sometimes}
        assert eligible['0']['all_ticks']==eligible['0']['some_ticks']==[actual]
        obs_dict=dict(obs)
        # All-error enclosure for the selected marker, independent of nominal outcomes at T*.
        l,h=bounds[actual]
        angle=(decode(l,ratio,0)[0],decode(h,ratio,0)[1])
        assert contained(angle) and angle[0]<=TARGET<=angle[1]
        assert select([],ratio,0)=='KEINER'
        assert select([(actual,obs_dict[actual]),('X',obs_dict[actual])],ratio,0)=='MEHRDEUTIG'
        assert select([(actual,obs_dict[actual])]*2,ratio,0)=='UNGÜLTIG'
        assert select([(codes[0],obs_dict[codes[0]])],ratio,0)=='KEINER'
        # A measured interval strictly straddling a tolerance boundary cannot qualify.
        n=next(n for n in range(obs_dict[actual]-500,obs_dict[actual]) if decode(n,ratio,0)[0]<BAND[0]<decode(n,ratio,0)[1])
        assert select([('X',n)],ratio,0)=='KEINER'
        dmin,dmax=l*TICK,h*TICK
        rcap_l=((dmin-ERR-LAG)/(2*BAND[0])-3*E0)/ratio-10
        rcap_u=10-((dmax+ERR)/(2*BAND[1])+3*(E0+dmax+ERR))/ratio
        rcap=min(rcap_l,rcap_u)
        assert F(0)<rcap<F('.01')
        low_echo,high_echo=travel_bounds(a,TARGET)
        # Feasible electronics setting: true emission at zero, start stamp −2 μs,
        # end stamp +2 μs, rounded to the nearest tick. Bound all resulting ticks.
        high_counts=(-(-(low_echo+2*STAMP-TICK/2)//TICK),(high_echo+2*STAMP+TICK/2)//TICK)
        assert all(not contained(decode(n,ratio,F('.01'))) for n in range(high_counts[0],high_counts[1]+1))
        # Test a continuous interval of hidden angles, without requiring exact tuning.
        # Both forward echo bounds are increasing; the extreme durations suffice.
        alternate=(F(9999,10000)*TARGET,F(10001,10000)*TARGET)
        altlo=echo_bounds(a,alternate[0])[0];althi=echo_bounds(a,alternate[1])[1]
        assert contained((decode(altlo,ratio,0)[0],decode(althi,ratio,0)[1]))
        raw.append({'M_for_scoring':str(m),'positive_station':j,'radial_scale_ratio':str(ratio),
                    'readings':dict(obs),'hidden_angle_factors':dict(zip(codes,map(str,FACTORS))),
                    'outer_tick_bounds':bounds})
        result[str(m)]={'selected':actual,'calibrations':eligible,'angle_over_target':list(map(str,(v/TARGET for v in angle))),
                        'radius_standard_certified_halfwidth':str(rcap),'failed_ticks_at_opposite_stamp_offsets':high_counts,
                        'late_inner':late(m,a,angle),'late_support':late(m,F(10),angle),
                        'hidden_angle_check_inner':late(m,a,(TARGET,TARGET)),'hidden_angle_check_support':late(m,F(10),(TARGET,TARGET))}
    return result,raw,frames
if __name__=='__main__':
    for m,d in run()[0].items():
        print(m,d['calibrations'],[float(F(v)) for v in d['angle_over_target']],d['late_inner'],d['late_support'])
