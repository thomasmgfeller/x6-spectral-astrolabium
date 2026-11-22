"""Indistinguishable exterior actions and distinguishable inner-source responses."""
from fractions import Fraction as Q
from itertools import product
from basis import A, B, E, EDGES, INNER, ORDER, action, dwells, scalar_coefficients
from stationaer import box
from intervalle import I,S

EPS=Q(1,512); RADIUS=Q(1,16384)

def clock_centre():
    u=[Q(k,8) for k in range(1,8)];u[2]+=Q(1,128);return u

def individual():
    e=Q(1,4);u=clock_centre();y={j:Q(j-5) for j in E};y[3]+=e;y.update({j:y[3]+(4-e)*v for j,v in zip(INNER,u)});c=scalar_coefficients(y);f=dwells(u)
    xn=dict.fromkeys(ORDER,Q(1,8));xn.update(zip(INNER,f));changes={12:EPS*c[13],13:-EPS*c[12]}
    arms=[{v:x+sign*changes.get(v,0) for v,x in xn.items()} for sign in (-1,1)]
    for arm in arms:
        assert all(abs(arm[k]/fj-1)<Q(1,100) for k,fj in zip(INNER,f))
    assert all(i in INNER for i,j in EDGES if j in changes)
    assert sum(c[k]*v for k,v in changes.items())==0
    # Scale out the common positive D. Identical outer fields can be overwritten freely.
    # Recover all coefficients of the outer clock polynomial (degree <=2) at several exterior densities.
    vectors=[(0,)*8]+[tuple(s*int(n==j) for n in range(8)) for j in range(8) for s in (-1,1)]+[tuple(int(n in (j,k)) for n in range(8)) for j in range(8) for k in range(j+1,8)]
    for v in vectors:
        yy=dict(y);yy.update(zip(E,v));wboundary={k:Q((k+1)**2,37) for k in E}
        assert action(yy,arms[0]|wboundary)==action(yy,arms[1]|wboundary)
    # Cross-difference of S/D under arbitrary rational Y-steps gives 9*x13 after multiplying by -19.
    t=Q(1,8);markers=[]
    for w in arms:
        mixed=0
        for a,b in product((-1,1),repeat=2):
            yy=dict(y);yy[A]+=a*t;yy[B]+=b*t;mixed+=a*b*action(yy,w)
        value=-19*mixed/(4*t*t);assert value==9*w[B];markers.append(value)
    rows=[{'x':{k:w[k] for k in INNER},'mass_density_sum':sum(w[k] for k in INNER),'mixed_marker':z} for w,z in zip(arms,markers)]
    return {'offset_over_Delta':e,'normalized_inner_clocks':u,'coefficients':{k:c[k] for k in changes},'rows':rows,'delta_sum':rows[1]['mass_density_sum']-rows[0]['mass_density_sum'],'delta_mixed_marker':markers[1]-markers[0],'exterior_polynomial_samples':len(vectors)}

def packets():
    e=box(Q(1,4)-RADIUS,Q(1,4)+RADIUS);L=4-e;u={i:box(c-RADIUS,c+RADIUS) for i,c in zip(INNER,clock_centre())}
    co={};
    for j in (12,13):
        co[j]=I.of(Q(-1,2))
        for (i,k),b in EDGES.items():
            if k==j:
                assert i in INNER
                co[j]-=Q(b,38)*L**2*(u[j]-u[i])**2
    faces=[I.of(0)]+[(u[i]+u[j])/2 for i,j in zip(INNER,INNER[1:])]+[I.of(1)]
    f={j:faces[k+1]-faces[k] for k,j in enumerate(INNER)}
    for j,k in [(12,13),(13,12)]:
        # Base jitter ±0.2%, translated tubes remain strictly within the ±1% band.
        assert EPS*co[k].absmax()<Q(8,1000)*f[j].lo
    ds=2*EPS*(co[13]-co[12]);dm=-18*EPS*co[12];assert ds.lo>0 and dm.lo>0
    assert all(c-RADIUS>Q(k,8)-Q(1,64) and c+RADIUS<Q(k,8)+Q(1,64) for k,c in enumerate(clock_centre(),1))
    from stationaer import DELTA
    o=e*DELTA;assert o.lo>Q(1,32)*S and o.hi<Q(3,32)*S
    return {'clock_halfwidth':RADIUS,'base_relative_density_halfwidth':Q(1,500),'translation_scale':EPS,
            'paired_sum_difference':ds.rounded(12),'paired_mixed_difference':dm.rounded(12),
            'half_reference_mixture_sum_difference':(ds/2).rounded(12),'half_reference_mixture_mixed_difference':(dm/2).rounded(12)}

def run():return {'point':individual(),'open_packet':packets()}
if __name__=='__main__':
    import json
    print(json.dumps(run(),default=str,indent=2,sort_keys=True))
