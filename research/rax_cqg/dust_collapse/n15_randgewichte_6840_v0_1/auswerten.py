"""Exact enclosures for the two archived witnesses and the specified full-box dust reference."""
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, isqrt
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'quellen'))
import zeugen as witness
from pruefen import MASS, COUPLING, ETA, coefficients, phase_box, support, tube, coherence as iv

GRID = 10**14
CODE = 6840
RHO = (Q(1,8), Q(1,4))
ORDER = support.geometry(CODE)[1]
EDGES = coefficients(ORDER)
SETUP = tube.template(CODE)
B = COUPLING*MASS
H = B*ETA*witness.INSET
TAU = B/50


def quant(v, den=GRID):
    return Q((v[0]*den).__floor__(),den), Q((v[1]*den).__ceil__(),den)


def sqroot(lo, hi):
    assert lo >= 0
    def floor(v):
        return isqrt((v*GRID**2).__floor__())
    return Q(floor(lo),GRID), Q(floor(hi)+1,GRID)


def ratio(a,b):
    assert b[0]>0
    return iv.mul(a,(1/b[1],1/b[0]))


def trig(domain, sine=False):
    # Point Taylor polynomial with Lagrange remainder; sine and cosine are 1-Lipschitz.
    l,r = quant(domain)
    x=(l+r)/2
    exponents = range(int(sine),35,2)
    val = sum((-1)**i*x**n/factorial(n) for i,n in enumerate(exponents))
    err = abs(x)**(exponents[-1]+1)/factorial(exponents[-1]+1)+(r-l)/2
    return quant((max(-1,val-err),min(1,val+err)))


def roots(cos_phase):
    a = trig(iv.bounds(TAU-H),True)
    c = trig(iv.bounds(TAU+H),True)
    b = iv.mul(iv.bounds(-2),iv.mul(trig(iv.bounds(TAU),True),cos_phase))
    disc = iv.sub(iv.sq(b),iv.mul(iv.bounds(4),iv.mul(a,c)))
    delta = sqroot(*disc)
    denom=iv.mul(iv.bounds(2),a)
    both=[quant(ratio(v,denom),10**9) for v in (iv.sub(b,delta),iv.add(b,delta))]
    assert both[0][1]<both[1][0] and all(l>0 for l,_ in both)
    return both


def controls(r,cs):
    re=iv.add(iv.mul(iv.bounds(r*r+1),trig(iv.bounds(H))),iv.mul(iv.bounds(2*r),cs))
    im=iv.mul(iv.bounds(r*r-1),trig(iv.bounds(H),True))
    gate=iv.sub(iv.mul(re,trig(iv.bounds(TAU),True)),
                iv.mul(iv.bounds(max(map(abs,im))),trig(iv.bounds(TAU))))
    pass_gate=gate[0]>=0
    assert pass_gate or gate[1]<0
    if r==1:
        assert re[0]*re[1]>0 and im==(0,0)
        err = (Q(0),Q(0)) if re[0]>0 else (Q(31415926535,10**10)/B,Q(31415926536,10**10)/B)
    else:
        assert re[0]>0
        z = ratio((min(map(abs,im)),max(map(abs,im))),re)
        assert 0<z[0]<=z[1]<1 and B+z[1]<3
        def atan_bound(x,k):
            return sum((-1)**i*x**(2*i+1)/(2*i+1) for i in range(k))
        err=quant((atan_bound(z[0],8)/B,atan_bound(z[1],7)/B),10**10)
    assert (err[1]<=Q(1,50)) if pass_gate else (err[0]>Q(1,50))
    return dict(gate='PASS' if pass_gate else 'FAIL',relative_abs_error=err,
                corrected_product_real=quant(re),corrected_product_imag=quant(im))


def pair(rho,raw):
    coords=raw['coordinates']
    actions=[witness.history(CODE,rho,s,c) for s,c in zip((1,-1),coords)]
    theta=quant(iv.sub(*actions))
    cs=trig(theta)
    root_bounds=roots(cs)
    fixed={str(r):controls(r,cs) for r in [Q(1),Q(7,4),Q(4,7),Q(4)]}
    for r,item in fixed.items():
        r=Q(r)
        t=max(r,1/r)
        low,hi=root_bounds
        predicted=('FAIL' if low[1]<t<hi[0] else 'PASS' if (t<low[0] or t>hi[1]) else None)
        assert predicted==item['gate']
    q=fixed['7/4']['relative_abs_error']
    assert Q(raw['witness']['relative_error_lower'])<=q[0]<=q[1]<=Q(raw['witness']['relative_error_upper'])
    sh=trig(theta,True)
    cosh=trig(iv.bounds(H))
    sinh=trig(iv.bounds(H),True)
    # Normalized amplitudes at r=1. Relative weights 1/2 each.
    probs=[]
    for s in (1,-1):
        c=iv.sub(iv.mul(cs,cosh),iv.mul(iv.bounds(s),iv.mul(sh,sinh)))
        pr=iv.mul(iv.bounds(Q(1,2)),iv.add(iv.bounds(1),c))
        assert pr[0]>0
        probs.append(quant(pr))
    norm=iv.mul(iv.bounds(Q(1,2)),iv.add(*probs))
    visibility=ratio(sqroot(*iv.mul(*probs)),norm)
    return dict(coordinates=coords,dust_actions=[quant(x) for x in actions],delta_S=theta,cos_delta_S=cs,
                r_ge_one_failure_between_roots=root_bounds,ratios=fixed,
                equal_weight_mean_arm_power=quant(norm),equal_weight_visibility=quant(visibility))


def jitter_bound(tile):
    # S=S0+sum a_j q_j, X=M+sum b_j q_j, independent uniform q_j in [-1,1].
    # Use E q_i q_j = delta_ij/3. Upper bound the two conditional second moments.
    _,centers,radius,_,_,max_f=SETUP
    e=tuple(sorted([o/d for o in tile for d in support.DELTA]))
    e=(e[0],e[-1])
    d=iv.sub(iv.mul(iv.bounds(4),support.DELTA),tile)
    y={j:iv.bounds(Q(j-5)) for j in support.PAST+support.FUTURE}
    y[3]=iv.add(y[3],e)
    for j,c in centers.items():
        lo,hi=c-radius,c+radius
        y[j]=(-2+4*lo+(1-lo)*e[0],-2+4*hi+(1-hi)*e[1])
    coeff=dict.fromkeys(support.I,iv.bounds(1))
    for a,b,k in EDGES:
        if b in coeff:
            term=iv.mul(iv.bounds(Q(k,19)),iv.sq(iv.sub(y[b],y[a])))
            coeff[b]=iv.add(coeff[b],term)
    b2=sum((MASS*ETA*f)**2 for f in max_f)/3
    a2=sum((MASS*ETA*d[1]*f*max(map(abs,coeff[j]))/2)**2 for j,f in zip(support.I,max_f))/3
    t=COUPLING/2
    return t*sqroot(a2*b2,a2*b2)[1]+t*t*b2/2


def tile_mass(tile):
    # The integral of (4 Delta - offset)^14 grows in Delta throughout each window.
    a,b=tile
    return tuple(((4*d-a)**15-(4*d-b)**15)/15 for d in support.DELTA)


def projection(span, anchor):
    # cos is decreasing up to pi. Beyond 3 radians simply use the global floor -1.
    distance=max(abs(span[0]-anchor),abs(span[1]-anchor))
    return trig(iv.bounds(distance))[0] if distance<3 else Q(-1)


def full(rho):
    paths,center,radius,eta,low,hi=SETUP
    assert len(center)==7 and eta==ETA and all(x>0 for x in low)
    assert 4*(4*support.DELTA[1]-support.WINDOWS[0][0])*(1+ETA)*max(hi)<1
    # Reference axis from the exact centre in clocks/density with zero jitter.
    origin=(paths,center,radius,Q(0),low,hi)
    mid=sum(support.WINDOWS[0])/2
    anchor=iv.center(phase_box(origin,EDGES,(mid,mid),rho,{j:(c,c) for j,c in center.items()},(rho,rho)))
    profile={'clock_center':{str(j):str(c) for j,c in center.items()},'clock_halfwidth':str(radius),
             'dwell_affine_ranges_per_vertex':{str(j):(str(a),str(b)) for j,a,b in zip(support.I,low,hi)}}
    denom=iv.bounds(0)
    numerator=Q(0)
    perturb=Q(0)
    lobes=[]
    for a,b in support.WINDOWS:
        lobes.append(tile_mass((a,b)))
        for i in range(8):
            step=(b-a)/8
            tile=(a+i*step,a+(i+1)*step)
            old=iv.phase_box(ORDER,tile,rho,MASS,profile)
            new=phase_box(SETUP,EDGES,tile,rho)
            phase=(max(old[0],new[0]),min(old[1],new[1]))
            assert phase[0]<=phase[1]
            floor=projection(phase,anchor)
            mass=tile_mass(tile)
            numerator+=iv.mul(mass,iv.bounds(floor))[0]
            denom=iv.add(denom,mass)
            perturb+=mass[1]*jitter_bound(tile)
    c=numerator/denom[1] if numerator>0 else Q(0)
    eps=perturb/denom[0]
    result=dict(left_reference_weight=quant(ratio(lobes[0],denom)),amplitude_modulus_lower=quant((c,c))[0],
                arm_absolute_perturbation_upper=quant((eps,eps))[1],status='HOLD')
    if c>eps:
        rel=2*eps/(B*(c-eps))
        result.update(relative_abs_error_upper=quant((rel,rel))[1],
                      norm_arm_modulus_lower=quant((c-eps,c-eps))[0])
        if B*(1+rel)<3 and rel<=1/Q(50):
            result['status']='PASS'
    # Sufficient radius in total variation NORM of a complex effective measure.
    # Common nonzero normalization is arbitrary; support and |X-M| are kept fixed.
    c=result['amplitude_modulus_lower']
    eps=result['arm_absolute_perturbation_upper']
    kappa=COUPLING*MASS*ETA/2
    radius=(TAU*c-(2+TAU)*eps)/(TAU+(2+TAU)*kappa)
    guaranteed=Q(39,100)
    disturbed=eps+kappa*guaranteed
    assert guaranteed<radius and c-guaranteed>disturbed
    bound=2*disturbed/(B*(c-guaranteed-disturbed))
    assert bound<Q(1,50) and B*(1+bound)<3
    result['stability']=dict(complex_measure_norm_radius_lower=quant((radius,radius))[0],
                             tested_norm_radius=str(guaranteed),
                             relative_error_upper_at_tested_radius=quant((bound,bound))[1])
    return result


def verify_inputs():
    origin=json.loads((ROOT/'herkunft.json').read_text())
    for path,v in origin['files'].items():
        assert sha256((ROOT/'quellen'/path).read_bytes()).hexdigest()==v['sha256'],path
    digest,name=(ROOT/'pruefplan.sha256').read_text().split()
    assert sha256((ROOT/name).read_bytes()).hexdigest()==digest
    assert not json.loads((ROOT/'quellen/zulassung.json').read_text())['physical_pass']


def run():
    verify_inputs()
    data=json.loads((ROOT/'quellen/zeugen.json').read_text())['rows']
    return {str(rho):dict(two_histories=pair(rho,data[f'{CODE};{rho}']),raw_full_box=full(rho)) for rho in RHO}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    print(json.dumps(run(),default=str,indent=2,sort_keys=True))
