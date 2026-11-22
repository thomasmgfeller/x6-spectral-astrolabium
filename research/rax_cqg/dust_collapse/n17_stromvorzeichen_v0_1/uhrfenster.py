"""Rational finite-window certificate for the final upper-density-bin effect."""
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial
import json

import nachrechnen as cap

old, n16 = cap.old, cap.n16
M,H=cap.M,cap.H
C=(cap.Y16-n16.YN)/19
E=-Q(1,38)


def polynomial_product(left,right):
    out={}
    for (i,j),a in left.items():
        for (k,l),b in right.items():
            key=(i+k,j+l)
            out[key]=out.get(key,0)+a*b
    return out


def mean(poly):
    # Independent normalized uniforms x=Y15-6 and v=w15-m on [-H,H].
    return sum((a*H**(i+j)/((i+1)*(j+1)) for (i,j),a in poly.items()
                if i%2==0 and j%2==0),Q(0))


def outward(iv, digits=58):
    scale=10**digits
    return Q(iv[0]*scale//1,scale), -Q((-iv[1]*scale)//1,scale)


def phase_log_derivative(d0, a, b, t, half_width):
    # After removing a pure time carrier, J=E exp(iP). g=dP/dt.
    # P=v*d0 + [(m+v)a + tc]x + [(m+v)b + te]x².
    p={(0,1):d0,(1,0):M*a+t*C,(1,1):a,(2,0):M*b+t*E,(2,1):b}
    g={(1,0):C,(2,0):E}
    mag=sum(abs(v)*H**(i+j) for (i,j),v in p.items())
    gmax=abs(C)*H+abs(E)*H**2
    pmax=mag+half_width*gmax  # applies to every t in the final window
    assert pmax < Q(1,100)
    lower=1-pmax**2/2
    jr=ji=gr=gi=Q(0)
    poly={(0,0):Q(1)}
    for k in range(6):
        m=mean(poly)/factorial(k)
        mg=mean(polynomial_product(poly,g))/factorial(k)
        if k%4==0: jr+=m; gr+=mg
        if k%4==1: ji+=m; gi+=mg
        if k%4==2: jr-=m; gr-=mg
        if k%4==3: ji-=m; gi-=mg
        poly=polynomial_product(poly,p)
    rem=mag**6/factorial(6)
    re,im=old.box(jr,rem),old.box(ji,rem)
    gre,gim=old.box(gr,gmax*rem),old.box(gi,gmax*rem)
    # J'=i E[g exp(iP)]; d log |J|²/dt = 2 Re[J' conjugate J]/|J|².
    numerator=old.sc(2,old.sub(old.mul(gre,im),old.mul(gim,re)))
    denominator=old.add(old.square(re),old.square(im))
    at_t=old.divide(numerator,denominator)
    # Bound second derivative 2 Re[J''/J-(J'/J)^2] across all t.
    ejp=abs(mean(g))+gmax*pmax
    curvature=2*(mean(polynomial_product(g,g))/lower+(ejp/lower)**2)
    return outward(old.add(at_t,old.box(0,half_width*curvature)))


def branch_bound(name,center,old_ref,first,final):
    y=dict(center[0]); y[15]=n16.YN
    region=old.whole_cell(center,old_ref)
    base=n16.budget(first,center,region)
    # Extra cross term from varying the old outgoing clock within its window
    # while bounding the narrow hidden source-clock deviations at fixed Y15.
    extra=sum((M+H)*abs(b)*2*H*old.RADIUS/38 for i,b in first.items() if i in old.I+(3,))
    e=base['max_mittlere_phasenabweichung']+(base['max_phasenfehler']+extra)**2/2
    widths={i:H for i in old.F[1:]}
    center16=cap.slope_range(first,y,widths,n16.YN)
    move16=sum(abs(b)*(2*(abs(y[i]-n16.YN)+widths.get(i,0))*H+H**2)/38
               for i,b in first.items())
    interval16=old.add(center16,old.box(0,move16))
    interval17=cap.slope_range(final,y,{**widths,15:H},cap.Y16)
    phase=old.total([region['staubphase'],old.mul(cap.BAND,interval16),
                     old.mul(cap.BAND,interval17)])
    c=1-(phase[1]-phase[0])**2/8
    eta=H*(cap.relative_slope_span(final,y,cap.Y16)+abs(C)*H+abs(E)*H**2)
    assert c>Q(99,100) and cap.Y16>n16.YN+H
    distance=2*eta*e*(1+1/c)/((c-e)*(1-eta/c))
    # The entire new term has no input-clock contribution in the primary and
    # shielded cases. The minimal case is an old-preparation contrast.
    p16=old.add(region['p'],n16.input_correction(first,y))
    p_shift=(M+H)*H*abs(sum(b for i,b in first.items() if i in old.P))/(19*old.DELTA[0])
    p17=old.add(p16,old.box(0,p_shift))
    if name=='minimal': assert p17[0]>0
    if name=='stromerhaltend': assert p17==region['p']
    return c,distance,p17


def evaluate(name,q):
    ideal=n16.CASES[name]
    _,_,final=cap.geometry(ideal)
    first=n16.new_edges(ideal)
    assert final[15]==1
    neutral,family=n16.packet_family(q)
    ref=-n16.old_coefficient(neutral)[7]/2
    errors=[]; bounds=[]; currents={}; branches={}
    for sign,center in family.items():
        c,delta,current=branch_bound(name,center,ref,first,final)
        bounds.append(c); errors.append(delta); currents[sign]=current
        if not set(first)&set(old.F):
            y=center[0]
            d0=n16.slope(first,y)
            a=sum(b*(y[i]-n16.YN) for i,b in first.items())/19
            b=-Q(sum(first.values()),38)
            branches[sign]=d0,a,b
    err=sum(errors)
    if not branches:
        # Both first-birth and final terms depend only on common old clocks.
        assert set(first)==set(old.F)
        return dict(center_exactly_equal=True,whole_gap=old.box(0,err),
                    packet_trace_error_sum=err,input_current=currents)
    slices=16
    half_width=H/slices
    enclosures=[]
    for j in range(slices):
        t=M-H+(2*j+1)*half_width
        enclosures.append(old.sub(phase_log_derivative(*branches['positiv'],t,half_width),
                                  phase_log_derivative(*branches['negativ'],t,half_width)))
    deriv=min(lo for lo,hi in enclosures),max(hi for lo,hi in enclosures)
    if deriv[0]<=0<=deriv[1]:
        # Conservative generic bound if the sign is unresolved.
        radius=max(map(abs,deriv))
        floor=(bounds[0]*bounds[1])**2
        assert 2*H*radius<1
        width=radius*H/(4*floor*(1-2*H*radius))+err
        return dict(center_log_likelihood_slope=deriv,whole_gap=outward(old.box(0,width)),
                    packet_trace_error_sum=err,input_current=currents)
    lo=min(map(abs,deriv));hi=max(map(abs,deriv))
    floor=(bounds[0]*bounds[1])**2
    # P(upper | +)-P(upper | -): cross product of the upper and lower halves.
    # Integral of (t_high-t_low) over normalized opposite half windows = H/4.
    assert 2*H*hi<1
    low=floor*lo*H/4
    high=hi*H/(4*floor*(1-2*H*hi))
    centered=(low,high) if deriv[0]>0 else (-high,-low)
    whole=old.add(centered,old.box(0,err))
    return dict(leading_log_slope_per_clock_halfwidth_squared=-2*M*C*(branches['positiv'][1]-branches['negativ'][1])/3,
                center_log_likelihood_slope=deriv,center_gap=outward(centered),whole_gap=outward(whole),
                packet_trace_error_sum=err,center_amplitude_lower=min(bounds),input_current=currents)


def run():
    assert sha256((cap.ROOT/'uhrfenster_vertrag.json').read_bytes()).hexdigest()==(
        cap.ROOT/'uhrfenster_vertrag.sha256').read_text().split()[0]
    return {k:{s:evaluate(k,q) for s,q in [('original',old.STEP),('transfer',old.STEP/2)]}
            for k in n16.CASES}


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    print(json.dumps(run(),default=str,sort_keys=True,indent=2))
