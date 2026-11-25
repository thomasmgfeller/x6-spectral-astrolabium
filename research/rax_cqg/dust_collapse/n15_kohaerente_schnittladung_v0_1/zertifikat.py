"""Rational complex-current bounds on the published stationary branch and finite packet."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from intervall import Box, box, SCALE
from pruefung import I,P,FUT
from randdichte import construct
from paketbreite import ideals,coeffs,slopes

MID=F(1,6)
WIDTH=F(1,2**22)
PAST_DENSITY=F(1,8)


def lower(b):
    return F(b.lo,SCALE)


def upper(b):
    return F(b.hi,SCALE)


def mag(b):
    return max(-lower(b),upper(b))


def add_term(poly,variables,coefficient):
    key=tuple(sorted(variables))
    poly[key]=poly.get(key,box(0))+coefficient


def coord(j):
    return I.index(j)


def saddle_phase(edges,y,w):
    # The seven inner C_j vanish exactly. Retain the original action at both collars.
    return -sum(w[j]*(19+sum(b*(y[i]-y[j]).square() for (i,v),b in edges.items() if v==j))
                for j in P+FUT)/38


def expansion(edges,y,w,hy,hw):
    poly={}
    for (i,j),b in edges.items():
        # dy_i-dy_j in the normalized [-1,1] coordinates.
        d=[(coord(v),sgn*hy) for v,sgn in ((i,1),(j,-1)) if v in I]
        for a,u in d:
            if j in I:
                add_term(poly,(coord(j)+7,a),-F(b,19)*hw[j]*(y[i]-y[j])*u)
            for c,v in d:
                add_term(poly,(a,c),-F(b,38)*w[j]*u*v)
                if j in I:
                    add_term(poly,(coord(j)+7,a,c),-F(b,38)*hw[j]*u*v)
    return poly


def charge_poly(edges,region,y,w,hy,hw,subtract_start):
    c=coeffs(edges,region,subtract_start)
    ay,aw=slopes(c,y,w)
    poly={}
    for j in I:
        add_term(poly,(coord(j),),ay[j]*hy)
        add_term(poly,(coord(j)+7,),aw[j]*hw[j])
    for (i,j),b in c.items():
        if j in I and b:
            for v,sign in ((i,1),(j,-1)):
                if v in I:
                    add_term(poly,(coord(j)+7,coord(v)),sign*b*hw[j]*hy)
    return poly


def l1(poly):
    return sum(map(mag,poly.values()))


def first_moment(poly,phase):
    # Only equal odd-coordinate masks can give a nonzero product expectation.
    def odd(key):
        return tuple(sorted(k for k,n in Counter(key).items() if n%2))
    buckets={}
    for key,v in phase.items():
        buckets.setdefault(odd(key),[]).append((key,v))
    left=right=F(0)
    for k,val in poly.items():
        for q,v in buckets.get(odd(k),()):
            den=1
            for count in Counter(k+q).values():
                assert count%2==0
                den*=count+1
            products=[x*y for x in (val.lo,val.hi) for y in (v.lo,v.hi)]
            left+=F(min(products),den*SCALE**2)
            right+=F(max(products),den*SCALE**2)
    return left,right


def label(region):
    return ','.join(map(str,sorted(region-set(P)))) or 'Eingang'


def pulse_coeff(edges,region,w,hw):
    # G(t)=S(Y+t1_A)=S(Y)-t q_A/19+t^2 K_A on an ideal.
    return -sum(b*(w[j]+Box(-hw[j].hi,hw[j].hi) if j in I else w[j])
                for (i,j),b in edges.items() if i in region and j not in region)/38


def one_tile(e,level,origin,pulse):
    rel,edges,y,w,center=construct(e,True)
    w.update(dict.fromkeys(P,box(PAST_DENSITY)))
    hy=(4-e)*F(1,64*2**level)
    hw={j:w[j]*F(1,100*2**level) for j in I}
    phase=expansion(edges,y,w,hy,hw)
    bs=l1(phase)
    phi=mag(saddle_phase(edges,y,w)-box(origin))
    cos_rotation=1-(phi+bs)**2/2
    assert cos_rotation>0
    # A pulse shifts an entire ideal, so an ordered edge changes by at most one pulse.
    for i,j in rel:
        jitter=(hy.hi if i in I else 0)+(hy.hi if j in I else 0)
        assert F(y[j].lo-y[i].hi-jitter,SCALE)>pulse
    inlet=charge_poly(edges,set(P),y,w,hy,hw,False)
    positive=lower(center)-l1(inlet)
    assert positive>0
    # q_P is positive and its conditional expectation is the stationary charge.
    inlet_floor=lower(center)*cos_rotation
    rows={}
    for region in ideals(rel):
        diff=charge_poly(edges,region,y,w,hy,hw,True)
        m=first_moment(diff,phase)
        x=l1(diff)
        m_abs=max(-m[0],m[1])
        abs_bound=m_abs+x*bs**2/2
        # Im[exp(i(S0-origin)) E(X exp(i dS))] with E(X)=0.
        err=x*(bs**3/6 + phi*bs**2/2)+m_abs*phi**2/2
        projected=(m[0]-err,m[1]+err)
        q_range=upper(center)+l1(charge_poly(edges,region,y,w,hy,hw,False))
        kmax=mag(pulse_coeff(edges,region,w,hw))
        # Symmetric derivative from the two arms, in units of the raw charge.
        pulse_bias=q_range*pulse**2*(kmax+(q_range/19)**2/6)
        rows[label(region)]=(abs_bound,projected,pulse_bias,q_range,kmax)
    return rows,(inlet_floor,upper(center),cos_rotation,bs,phi,positive)


def run():
    _,edges,y,w,_=construct(box(MID),True)
    w.update(dict.fromkeys(P,box(PAST_DENSITY)))
    mid=saddle_phase(edges,y,w)
    origin=(lower(mid)+upper(mid))/2
    n=8
    pulse=F(1,64)
    result={}
    for level in range(4):
        tiles=[one_tile(Box.hull(MID-WIDTH+2*WIDTH*F(k,n),MID-WIDTH+2*WIDTH*F(k+1,n)),
                        level,origin,pulse) for k in range(n)]
        lower_inlet=min(t[1][0] for t in tiles)
        upper_inlet=max(t[1][1] for t in tiles)
        lower_z=min(t[1][2] for t in tiles)
        rows={}
        for key in tiles[0][0]:
            vals=[t[0][key] for t in tiles]
            absolute=max(v[0] for v in vals)
            lo=min(v[1][0] for v in vals)
            hi=max(v[1][1] for v in vals)
            nonzero=max(0,lo,-hi)/upper_inlet
            rows[key]={'relative_upper':str(absolute/lower_inlet),'relative_lower':str(nonzero),
                       'projected_difference':[str(lo),str(hi)]}
        # Each finite probe differs from its own derivative by at most this amount per unit measure.
        qmax=max(v[3] for t in tiles for v in t[0].values())
        eps=max(v[2] for t in tiles for v in t[0].values())
        peak=max(F(v['relative_upper']) for v in rows.values())
        finite_bound=(peak*lower_inlet+2*eps)/(lower_inlet-eps)
        read_error=F(2,10**6)
        combined_bias=eps+19*read_error/pulse
        observed_bound=(peak*lower_inlet+2*combined_bias)/(lower_inlet-combined_bias)
        assert combined_bias<lower_inlet and observed_bound<F(1,50)
        result[str(level)]={'cuts':rows,'cut_count':len(rows),'current_ratio_error_max':str(peak),
            'finite_pulse_ratio_error_max':str(finite_bound),'pulse_step_Y':str(pulse),
            'complex_arm_read_error':str(read_error),'finite_with_read_error':str(observed_bound),
            'single_arm_pair_derivative_bias':str(eps),'q_abs_max':str(qmax),
            'rotated_inlet_real_lower':str(lower_inlet),'amplitude_modulus_lower':str(lower_z),
            'max_abs_inner_phase_deviation':str(max(t[1][3] for t in tiles)),
            'max_abs_center_phase_rotation':str(max(t[1][4] for t in tiles))}
    return {'rotation_rad':str(origin),'tiles':n,'levels':result}


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
