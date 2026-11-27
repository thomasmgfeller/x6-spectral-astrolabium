"""Certify clock windows for one material-side measurement, with exact fractions."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WINDOW = Q(15, 32), Q(17, 32)
HALF = Q(1, 2)
SPEED = Q(1, 8)
GRID = 10**10
SPHERES = ((Q(-1), Q(1)), (Q(-5, 2), Q(2)))


def point(x):
    return x, x


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sub(a, b):
    return a[0]-b[1], a[1]-b[0]


def product(a, b):
    values = [u*v for u in a for v in b]
    return min(values), max(values)


def sq(a):
    values = [u*u for u in a]
    return (0 if a[0]<=0<=a[1] else min(values)), max(values)


def bounds_sum(terms):
    lo, hi = 0, 0
    for l,h in terms:
        lo, hi = lo+l, hi+h
    return lo,hi


def polynomial(coords, clocks, start, center_z, radius):
    # z = x - 1/2.  Distance² minus radius² is a*z² + b*z + c.
    j = 11
    dt = sub(clocks[j], clocks[start])
    assert dt[0]>0 and clocks[j][1]<WINDOW[0]
    vel = [product(point(v-u), (1/dt[1], 1/dt[0]))
           for u,v in zip(coords[start],coords[j])]
    assert bounds_sum(sq(v) for v in vel)[1]<1
    d = [add(point(p-c),product(v,sub(point(HALF),clocks[start])))
         for p,c,v in zip(coords[start], (0,0,center_z), vel)]
    a = sub(bounds_sum(sq(v) for v in vel),point(SPEED**2))
    b = product(point(2), add(bounds_sum(product(u,v) for u,v in zip(d,vel)),
                              point(radius*SPEED)))
    c = sub(bounds_sum(sq(u) for u in d), point(radius**2))
    return a,b,c


def evaluate(poly, x):
    a,b,c = poly
    z = sub(x,point(HALF))
    return add(product(add(product(a,z),b),z),c)


def derivative(poly, x):
    a,b,_ = poly
    return add(product(product(point(2),a),sub(x,point(HALF))),b)


def enclosing_grid_cell(poly):
    lo = int(WINDOW[0]*GRID)
    hi = int(WINDOW[1]*GRID)
    assert evaluate(poly,point(Q(lo,GRID)))[1]<0
    assert evaluate(poly,point(Q(hi,GRID)))[0]>0
    assert derivative(poly,WINDOW)[0]>0
    while hi-lo>1:
        m = (lo+hi)//2
        a,b = evaluate(poly,point(Q(m,GRID)))
        if b<0:
            lo=m
        elif a>0:
            hi=m
        else:
            raise RuntimeError("Grid evaluation unresolved. Refine the clock enclosure.")
    return Q(lo,GRID),Q(hi,GRID)


def on_window(poly, x, increasing):
    if increasing:
        assert derivative(poly,x)[0]>0
        return evaluate(poly,point(x[0]))[0],evaluate(poly,point(x[1]))[1]
    h=(x[1]-x[0])/64
    boxes=[evaluate(poly,(x[0]+i*h,x[0]+(i+1)*h)) for i in range(64)]
    return min(b[0] for b in boxes),max(b[1] for b in boxes)


def outward(a, digits=9):
    scale=10**digits
    def dec(integer):
        sign='-' if integer<0 else ''
        whole, frac=divmod(abs(integer),scale)
        return f'{sign}{whole}.{frac:0{digits}d}'
    return [dec(a[0]*scale//1),dec(-((-a[1]*scale)//1))]


def main():
    pins={'Vergleichspaar.json':'c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f',
          'Ortskoordinaten.json':'a8bdf817687174d3c47d6ebf105974b41008a9037555e66da62a581c9f9601f4'}
    for file,digest in pins.items():
        assert sha256((ROOT/'input'/file).read_bytes()).hexdigest()==digest
    inp=json.loads((ROOT/'input/Vergleichspaar.json').read_text())
    p=[list(map(Q,line)) for line in json.loads((ROOT/'input/Ortskoordinaten.json').read_text())]
    radii=[Q(1),Q(2)]
    stable=(Q(31,64),WINDOW[1])
    symmetric=(Q(1,2)-Q(1979,100000),Q(1,2)+Q(1979,100000))
    assert WINDOW[0]<symmetric[0] and symmetric[1]<WINDOW[1]
    records=[]
    groups={}
    all_polys={}
    for start in (3,4,5):
        roots=[]
        for side in ('heavy','light'):
            clocks=[tuple(map(Q,row)) for row in inp[side]['normalized_clocks']]
            assert [start,11] in inp['relation']
            pair=[polynomial(p,clocks,start,*s) for s in SPHERES]
            all_polys[start,side]=pair
            small=on_window(pair[0],WINDOW,False)
            large=on_window(pair[1],WINDOW,True)
            assert small[1]<0 and large[0]<0<large[1]
            bracket=enclosing_grid_cell(pair[1])
            roots.append(bracket)
            records.append(dict(start=start,through=11,preparation=side,
                small_squared_gap_full_window=outward(small),
                large_squared_gap_full_window=outward(large),
                large_squared_gap_derivative=outward(derivative(pair[1],WINDOW)),
                switch_clock_closed_enclosure=outward(bracket,10)))
        groups[start]=max(v[0] for v in roots),max(v[1] for v in roots)
    best=5
    assert all(groups[best][1]<groups[i][0] for i in (3,4))
    minimum_clearance=[]
    symmetric_lower=[]
    for side in ('heavy','light'):
        pair=all_polys[best,side]
        margins=[]
        radius_upper=[r-SPEED*(stable[0]-HALF) for r in radii]
        for j,poly in enumerate(pair):
            l,h=on_window(poly,stable,j==1)
            # Margins eps with dist <= R-eps or dist >= R+eps. R>eps.
            R=radius_upper[j]
            d=Q(1,10**6)
            def pass_margin(n):
                eps=n*d
                if j==0:return eps<1 and h < -2*R*eps+eps**2
                return l>2*R*eps+eps**2
            lo,hi=0,10**6
            assert pass_margin(lo)
            while hi-lo>1:
                m=(lo+hi)//2
                if pass_margin(m):lo=m
                else:hi=m
            margins.append(str(lo*d))
        minimum_clearance.append(margins)
        gl=on_window(pair[1],symmetric,True)[0]
        assert gl>0 and on_window(pair[0],symmetric,False)[1]<0
        symmetric_lower.append(gl)
    return dict(window=[str(q) for q in WINDOW],gap="distance_squared_minus_radius_squared",
                records=records,selected_start=best,through=11,readout="inside_small_outside_large",
                common_robust_suffix=[str(v) for v in stable],
                radial_clearances_suffix_heavy_light_small_large=minimum_clearance,
                symmetric_test_at_halfwidth="1979/100000",
                symmetric_large_squared_gap_lower_bound=outward(point(min(symmetric_lower)))[0],
                candidates="The three previously discriminating witness lines only",
                clocks="closed input intervals, all combinations",
                measured_physical_radius=None,physical_pilot_count=8,physical_P3_status="NOT_RUN")


if __name__=='__main__':
    if not __debug__:raise RuntimeError("Run without -O")
    parser=argparse.ArgumentParser()
    parser.add_argument('--ausgabe',action='store_true')
    args=parser.parse_args()
    ans=json.dumps(main(),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    path=ROOT/'Ergebnis.json'
    if args.ausgabe:path.write_text(ans)
    else:assert path.read_bytes()==ans.encode('utf-8')
    print(ans)
