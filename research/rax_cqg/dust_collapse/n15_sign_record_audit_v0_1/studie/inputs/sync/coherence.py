"""Rigorous phase-range bound for a single dust carrier and a finite diagnostic tube."""
from fractions import Fraction as Q
from itertools import product
import support
import tube


def bounds(x):
    return (x,x)


def add(a,b):
    return (a[0]+b[0],a[1]+b[1])


def sub(a,b):
    return (a[0]-b[1],a[1]-b[0])


def mul(a,b):
    vals = [x*y for x,y in product(a,b)]
    return min(vals),max(vals)


def sq(a):
    return (0 if a[0]<=0<=a[1] else min(x*x for x in a),max(x*x for x in a))


def center(a):
    return (a[0]+a[1])/2


def phase_box(rel, tile, rho, mass, profile):
    d = sub(mul(bounds(4),support.DELTA),tile)
    e = mul(tile,(1/support.DELTA[1],1/support.DELTA[0]))
    clocks = {v:bounds(Q(v-5)) for v in support.PAST+support.FUTURE}
    clocks[3] = add(clocks[3],e)
    weights = {v:bounds(Q(1,8)) for v in support.FUTURE}
    for v in support.PAST:
        weights[v] = (rho-Q(1,32),rho+Q(1,32))
    for v in support.I:
        c = Q(profile["clock_center"][str(v)])
        r = Q(profile["clock_halfwidth"])
        # Both partial derivatives of -2+4u+(1-u)e are positive here.
        clocks[v] = (Q(-2)+4*(c-r)+(1-(c-r))*e[0],
                     Q(-2)+4*(c+r)+(1-(c+r))*e[1])
        f = tuple(map(Q,profile["dwell_affine_ranges_per_vertex"][str(v)]))
        weights[v] = mul(mul(mul(bounds(mass),d),f),(Q(99,100),Q(101,100)))
    # Expand the quadratic action in the clocks. Collect the first-order
    # terms before applying interval bounds, including the shared past density.
    n = 15
    t = [center(clocks[v]) for v in range(n)]
    dt = [sub(clocks[v],bounds(t[v])) for v in range(n)]
    w = [center(weights[v]) for v in range(n)]
    dw = [sub(weights[v],bounds(w[v])) for v in range(n)]
    C = [Q(1)]*n
    grad = [Q(0)]*n
    clock_correction = [bounds(Q(0)) for _ in range(n)]
    quadratic = bounds(Q(0))
    for y,x in sorted(rel):
        inside = sum((y,v) in rel and (v,x) in rel for v in range(n))
        if inside >= 4:
            continue
        b = Q((1,-9,16,-8)[inside],19)
        diff = t[x]-t[y]
        dd = sub(dt[x],dt[y])
        C[x] += b*diff**2
        grad[x] += 2*b*w[x]*diff
        grad[y] -= 2*b*w[x]*diff
        second = mul(bounds(b),sq(dd))
        quadratic = add(quadratic,mul(bounds(w[x]),second))
        corr = add(mul(bounds(2*b*diff),dd),second)
        clock_correction[x] = add(clock_correction[x],corr)
    total = add(bounds(sum(a*b for a,b in zip(w,C))),quadratic)
    for v in range(n):
        total = add(total,mul(bounds(grad[v]),dt[v]))
        total = add(total,mul(dw[v],clock_correction[v]))
        if v not in support.PAST:
            total = add(total,mul(dw[v],bounds(C[v])))
    total = add(total,mul(dw[0],bounds(sum(C[v] for v in support.PAST))))
    return mul(bounds(Q(-1,2)),total)


def run():
    profile = tube.run()
    _,rel = support.geometry(profile['carrier'])
    rows = {}
    tiles = 8
    for M,rho in product(support.MASSES,(Q(1,8),Q(1,4))):
        phases = []
        for a,b in support.WINDOWS:
            step = (b-a)/tiles
            for i in range(tiles):
                phases.append(phase_box(rel,(a+i*step,a+(i+1)*step),rho,M,profile))
        l = min(p[0] for p in phases)
        r = max(p[1] for p in phases)
        # Exact conservative bound cos(x) >= 1-x^2/2, then clip at zero.
        lower = max(Q(0),1-(r-l)**2/8)
        rows[f"{M};{rho}"] = {"phase_rad_exact":list(map(str,(l,r))),
                              "phase_rad_display":[float(l),float(r)],
                              "conditional_modulus_lower_exact":str(lower),
                              "conditional_modulus_lower_display":float(lower)}
    return {"unit":"absolute value of conditional dust amplitude divided by auxiliary tube measure; one fixed geometry, common gravitational phase and scalar factor removed",
            "tiles_per_lobe":tiles,"rows":rows}


if __name__=="__main__":
    import json
    print(json.dumps(run(),indent=2))
