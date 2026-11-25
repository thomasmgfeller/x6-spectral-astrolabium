"""Certified directed sums for spatially assigned cut charges and lateral currents."""
from fractions import Fraction as F
from functools import lru_cache
from decimal import Decimal, localcontext

SCALE = 10**30
ONE = (SCALE, SCALE)
ZERO = (0, 0)


def enclose(x):
    return x.numerator*SCALE//x.denominator, -((-x.numerator*SCALE)//x.denominator)


def add(a,b):
    return a[0]+b[0], a[1]+b[1]


def times(k,a):
    p, q = k*a[0], k*a[1]
    return min(p,q), max(p,q)


def mul(a,b):
    corners = [x*y for x in a for y in b]
    return min(corners)//SCALE, -((-max(corners))//SCALE)


def divide(a,b):
    assert b[0] > 0
    return mul(a, (SCALE*SCALE//b[1], -((-SCALE*SCALE)//b[0])))


def total(items):
    lo = hi = 0
    for a,b in items:
        lo += a
        hi += b
    return lo,hi


def overlap(a,b):
    return max(a[0],b[0]) <= min(a[1],b[1])


def display(a):
    with localcontext() as ctx:
        ctx.prec = 65
        return [format(Decimal(x)/Decimal(SCALE),'f') for x in a]


def flux_test(stencil, r, root):
    q = (enclose(root[0])[0], enclose(root[1])[1])

    @lru_cache(None)
    def qt(n):
        if n == 0:
            return ONE
        half = qt(n//2)
        square = mul(half,half)
        return mul(square,q) if n%2 else square

    @lru_cache(None)
    def rx(j):
        return enclose(r**j)

    def field(n,j):
        # Units of the first-slice density at j=2547.
        return mul(qt(n),rx(j-2547))

    def coefficients(route):
        # A unit cell centred at 0. Its right face separates stations 0 and 1.
        charge, lateral, activity = [], [], []
        for d, s, b in stencil:
            dest = 0 if route == 'receiver' else s
            charge.extend(times(-b*d, mul(qt(l),rx(dest))) for l in range(1,d+1))
            for x in range(min(0,-s)+1,max(0,-s)+1):
                clock = qt(d) if route == 'receiver' else ONE
                unit = mul(clock,rx(x+s))
                lateral.append(times(-b*d*(1 if s>0 else -1),unit))
                activity.append(times(abs(b)*d,unit))
        return total(charge), total(lateral), total(activity)

    # Second implementation: enumerate edges touching an actual local window.
    # Evaluate their receiver fields individually before routing them.
    def local_edges(route,n,j):
        cut, side = [], []
        for d,s,b in stencil:
            for tick in range(n-d,n+1):
                for x in range(j-4,j+5):
                    end = x+s
                    receiver_at_crossing = route == 'receiver'
                    station = end if receiver_at_crossing else x
                    face_tick = tick if receiver_at_crossing else tick+d
                    cross_cut = tick <= n < tick+d and station == j
                    cross_face = face_tick == n and min(x,end) <= j < max(x,end)
                    if cross_cut or cross_face:
                        current = times(-b*d,field(tick+d,end))
                        if cross_cut:
                            cut.append(current)
                        if cross_face:
                            side.append(times(1 if s>0 else -1,current))
        return total(cut), total(side)

    assert -sum(b*d*d for d,_,b in stencil) == 83
    boundary = 2547
    threshold = divide(total(field(0,j) for j in range(190,195)),times(500,ONE))
    walls = []
    for n in range(7681):
        # Each decision certified with strict, disjoint enclosures.
        while field(n,boundary)[1] < threshold[0]:
            boundary -= 1
        assert field(n,boundary)[0] > threshold[1]
        assert field(n,boundary+1)[1] < threshold[0]
        walls.append(boundary)
    assert walls[0] == 2547
    retreats = [t for t in range(1,len(walls)) if walls[t] != walls[t-1]]
    assert all(walls[t-1]-walls[t] == 1 for t in retreats)
    gaps = sorted(set(b-a for a,b in zip(retreats,retreats[1:])))
    assert min(gaps) >= 12

    result = {}
    for route in ('receiver','emitter'):
        cap, flow, gross = coefficients(route)
        assert cap[0] > 0 and flow[1] < 0 and gross[0] > -flow[0]
        for n,j in ((48,2547), (1920,2448), (7680,2151)):
            local_q,local_f = local_edges(route,n,j)
            assert overlap(local_q,mul(cap,field(n,j)))
            assert overlap(local_f,mul(flow,field(n,j)))
        # Check a per-vertex continuity equation, independent of boundary selection.
        cq,cf = local_edges(route,50,2547)
        pq,_ = local_edges(route,49,2547)
        _,lf = local_edges(route,50,2546)
        assert overlap(add(cq,cf),add(pq,lf))

        def swept_flux(old,new,t):
            crossing = mul(flow,field(t,old))
            if old == new:
                return crossing
            assert new == old-1
            return add(crossing,mul(cap,field(t,old)))

        def inventory(t,k):
            return mul(cap,total(field(t,j) for j in range(2101,k+1)))

        rows = []
        for moving in (False,True):
            track = walls if moving else [2547]*len(walls)
            through = ZERO
            abs_ticks = ZERO
            left = ZERO
            start = inventory(0,track[0])
            for t in range(1,len(track)):
                f = swept_flux(track[t-1],track[t],t)
                assert f[0] > 0 or f[1] < 0
                through = add(through,f)
                abs_ticks = add(abs_ticks,f if f[0]>0 else times(-1,f))
                left = add(left,mul(flow,field(t,2100)))
                if t%1920 == 0:
                    # Independent inventory change on a finite strip with both faces.
                    balance = add(left,add(start,times(-1,inventory(t,track[t]))))
                    assert overlap(through,balance)
                    rows.append({'ticks_elapsed':t,'wall':'fixed_initial_level' if moving else 'relative_level',
                                 'last_inner_station':track[t],
                                 'net_outward_in_initial_cell_charges':display(divide(through,cap)),
                                 'sum_of_absolute_tick_fluxes_in_initial_cell_charges':display(divide(abs_ticks,cap)),
                                 'independent_balance_in_initial_cell_charges':display(divide(balance,cap))})
        result[route] = {'cut_charge_per_density':display(cap),
                         'outward_flux_per_density':display(flow),
                         'unsigned_edge_flux_per_density_at_fixed_face':display(gross),
                         'fixed_face_flux_per_local_cell_charge':display(divide(flow,cap)),
                         'balance_checks':rows}
    rr, ee = result.values()
    for a,b in zip(rr['balance_checks'],ee['balance_checks']):
        for key in ('net_outward_in_initial_cell_charges','sum_of_absolute_tick_fluxes_in_initial_cell_charges'):
            assert overlap(tuple(map(F,a[key])),tuple(map(F,b[key])))
    return {'first_tick':38400,'last_tick':46080,
            'wall_on_five_slices':walls[::1920],'retreat_count':len(retreats),
            'retreat_gaps_in_ticks':gaps,'allocation':result}
