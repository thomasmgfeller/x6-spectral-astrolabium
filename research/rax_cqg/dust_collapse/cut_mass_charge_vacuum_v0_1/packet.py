"""Same-collar charge on an explicit incoming route and coherent outer packet."""
from cmath import exp
from math import sqrt,sin
from fractions import Fraction as F
from calibrate import (P,I,FUT,OFF,M0,M1,delta,TOL,order,path_positions,
                      midpoint_cells,polynomial,avg,point,summary)

def packed(z):
    return [round(z.real,11),round(z.imag,11)]

def response(key,path,k,mass,center,n):
    rel,_=order(key)
    beta=4/sqrt(6);d=sqrt(2/(19*beta))
    u=path_positions(path,rel,k);lam=midpoint_cells([path],u)
    b={}
    for y,x in rel:
        j=sum((y,q) in rel and (q,x) in rel for q in range(15))
        b[y,x]=(1,-9,16,-8)[j] if j<4 else 0
    grav=15-sum(b.values())
    result=[0j]*4
    eta=.0001
    for sign in (-1,1):
        mid=sign/16
        for j in range(n+1):
            offset=mid-1/32+j/(16*n)
            D=4*d-offset
            T={v:(v-5)*d for v in P+FUT}
            T[3]+=offset
            T.update({v:T[3]+D*float(u[v]) for v in I})
            w={v:float(mass*lam[v])*D for v in I}
            C=[1+(beta/2)*sum(h*(T[x]-T[y])**2 for (y,z),h in b.items() if z==x) for x in range(15)]
            L=sum(C[v] for v in P)/2
            amp=exp(1j*(grav-center*L-sum(C[v] for v in FUT)/16-sum(w[v]*C[v] for v in I)/2))
            amp*=sin(L/32)/(L/32) if L else 1
            charge=beta/2*sum(w[x]*coef*(T[y]-T[x]) for (y,x),coef in b.items() if y in P and x in I)
            # Exact integration of the collective past density, Simpson in each clock lobe.
            fac=(1 if j in (0,n) else 4 if j%2 else 2)/(6*n)
            z=amp*fac
            for q,v in enumerate((z,z*charge,z*exp(1j*eta*charge),z*exp(-1j*eta*charge))):
                result[q]+=v
    den,num,plus,minus=result
    assert abs(den)>1e-4
    derivative=(plus-minus)/(2j*eta*den)
    assert abs(derivative-num/den)<1e-7
    return den,num/den

def read_independent_mean(key,route,k,mass):
    # Direct finite differences of the original dust action in unscaled clock coordinates.
    # Integrate charge with the diagonal packet weight (Simpson is exact for this quadratic).
    from calibrate import encode
    from gluing import intervals
    rel,_=order(key)
    code=encode(rel,15)
    nums=[(y,x,(1,-9,16,-8)[inn.bit_count()] if inn.bit_count()<4 else 0)
          for y,x,inn in intervals(code,15)]
    beta=4/sqrt(6);d=sqrt(2/(19*beta));eps=.125
    u=path_positions(route,rel,k);lam=midpoint_cells([route],u)
    mean=0.
    for sign in (-1,1):
        for j,factor in enumerate((1,4,1)):
            off=sign/16+(j-1)/32
            D=4*d-off
            T={v:(v-5)*d for v in P+FUT}
            T[3]+=off;T.update({v:T[3]+D*float(u[v]) for v in I})
            w={v:1/8 for v in P+FUT}
            w.update({v:float(mass*lam[v])*D for v in I})
            def S(tau):
                t={v:x+(tau if v in P else 0.) for v,x in T.items()}
                return -sum(w.values())/2-beta/4*sum(w[x]*b*(t[x]-t[y])**2 for y,x,b in nums)
            mean+=factor*(S(-eps/2)-S(eps/2))/(12*eps)
    return mean

def run(key,path):
    rel,deg=order(key)
    route=list(path)
    records={}
    gains={}
    for k in (F(1,3),F(11,24)):
        u=path_positions(route,rel,k)
        poly=polynomial(deg,u,midpoint_cells([route],u))
        gain=avg(poly)
        assert gain[0]>0
        gains[str(k)]=(1/gain[1],1/gain[0])
        vals={}
        for mass in (F(0),M0,M1):
            coherent={}
            for center in (F(1,8),F(1,4)):
                responses=[response(key,route,k,mass,float(center),n) for n in (64,128,256)]
                dev=max(abs(a-b) for a,b in zip(responses[-1],responses[-2]))
                assert dev<3e-9
                norm,q=responses[-1]
                coherent[str(center)]={"complex_charge_insertion_over_amplitude":packed(q),
                         "amplitude_with_common_packet_normalization_removed":packed(norm),
                         "128_to_256_absolute_change_below":3e-9}
            vals[str(mass)]={"known_inlet_mass":str(mass),"p_at_right_center":summary(tuple(mass*x for x in point(poly,OFF))),
                            "p_at_left_center":summary(tuple(mass*x for x in point(poly,-OFF))),
                            "auxiliary_mean_p":summary(tuple(mass*x for x in gain)),"coherent":coherent}
        direct={str(m):read_independent_mean(key,route,k,m) for m in (F(0),M0,M1)}
        gain_from_M0=float(M0)/direct[str(M0)]
        inferred=gain_from_M0*direct[str(M1)]
        assert abs(direct["0"])<1e-11 and abs(inferred-float(M1))<1e-11
        assert abs(gain_from_M0-float(sum(gains[str(k)])/2))<1e-10
        records[str(k)]={"response":vals,"gain_from_positive_standard":summary(gains[str(k)]),
                         "independent_action_difference_validation":{"gain_from_quarter":round(gain_from_M0,10),
                         "inferred_mass_at_held_out_unit_dose":round(inferred,10)}}
    intervals=[((1-TOL)*l,(1+TOL)*h) for l,h in gains.values()]
    assert max(l for l,h in intervals)>min(h for l,h in intervals)
    # Read off the timing where p vanishes analytically at the right-lobe centre.
    d=float(delta[0]);k0=(23/16-d)/(3*(4*d-1/16))
    assert 1/3<k0<11/24
    return {"end_type":key,"route":route,"profiles":records,"positive_mass_zero_charge":{
             "offset":"1/16","k_exact":"(23/16 - Delta)/(3*(4*Delta - 1/16))","k_approx":k0,"p":"0"},
             "true_dust_vacuum":{"scope":"all w=0, separate collar preparation","p":"0"},
             "matched_empty_interior":{"scope":"same positive outer packet with w_inner=0","p":"0"},
             "tag_of_known_unit_validates_same_profile_mean_gain":True,
             "common_2pct_gain_for_the_two_route_profiles":False}

