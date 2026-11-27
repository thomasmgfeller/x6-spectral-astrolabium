"""Exact checks of the N22 action inputs for the two PR419 geometric alternatives."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json

PAIR_SHA = 'c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f'
WITNESS_SHA = '967a350d6f7887f445027b08c070830c6a2a5e2bddeec9ca295df6a253858ce2'
COORDS_SHA = 'a8bdf817687174d3c47d6ebf105974b41008a9037555e66da62a581c9f9601f4'
RADIUS_STEP = Q(1,100000)
DEVICES = frozenset({(15,16),(16,18),(17,18),(18,7)})
EARLY, LATE = {0,1,2,3}, {7,8,9,10}
SPHERES = (Q(1),Q(357,200))


def checked(path, sha):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == sha, path
    return json.loads(raw)


def point(value):
    return Q(value),Q(value)


def add(x,y):
    return x[0]+y[0],x[1]+y[1]


def mul(x,y):
    corners=[i*j for i in x for j in y]
    return min(corners),max(corners)


def square_difference(x,y):
    lo,hi = x[0]-y[1], x[1]-y[0]
    return 0 if lo <= 0 <= hi else min(lo**2,hi**2),max(lo**2,hi**2)


def field_action(y,w,k):
    """Scale of the archived field stationarity equations for zero source and zero post-kicks."""
    total=mul(point(19),(sum(v[0] for v in w),sum(v[1] for v in w)))
    for (i,j),value in sorted(k.items()):
        total=add(total,mul(point(value),mul(w[j],square_difference(y[j],y[i]))))
    return total


def outward(bound, digits=10):
    a,b=bound
    d=10**digits
    low=(a*d).__floor__(); high=(b*d).__ceil__()
    def to_string(n):
        sign='-' if n<0 else ''
        n=abs(n)
        return f'{sign}{n//d}.{n%d:0{digits}d}'
    return to_string(low),to_string(high)


def radius_neighborhood(clocks,w,coords,r,z):
    # In the given flat control, time is the normalized clock and c=1.
    # Enclose simultaneously every r' in [r-eps,r+eps] with fixed centre/speed.
    def radius(t):
        return r-(t-Q(1,2))/8
    sides = []
    radial = []
    for xyz,clock,weight in zip(coords,clocks,w):
        d2=sum((x-c)**2 for x,c in zip(xyz,(0,0,z)))
        rlo,rhi=radius(clock[1])-RADIUS_STEP,radius(clock[0])+RADIUS_STEP
        assert 0<rlo<=rhi
        if weight[0]>0:
            sides.append(rlo**2-d2)
            radial.append((d2/rhi**2,d2/rlo**2))
        else:
            assert weight==(0,0)
            sides.append(d2-rhi**2)
    radial.sort()
    profile_gaps=[b[0]-a[1] for a,b in zip(radial,radial[1:])]
    ray_margin=[]
    for i in (3,4,5):
        ta,tb=clocks[i],clocks[11]
        for t in (Q(15,32),Q(17,32)):
            assert ta[1]<tb[0]<=tb[1]<t
            alpha=( (t-ta[1])/(tb[1]-ta[0]), (t-ta[0])/(tb[0]-ta[1]) )
            maximum=0
            for a,b,c in zip(coords[i],coords[11],(0,0,z)):
                maximum+=max((a+u*(b-a)-c)**2 for u in alpha)
            ray_margin.append((radius(t)-RADIUS_STEP)**2-maximum)
    # For each geometry, |p(t)-C|-R(t) is convex on the entire time window.
    assert len(radial)==19 and min(*sides,*profile_gaps,*ray_margin)>0
    return [str(r-RADIUS_STEP),str(r+RADIUS_STEP)]


def run(pair, witness, coord_data):
    coords=[tuple(map(Q,row)) for row in coord_data]
    rel=set(map(tuple,pair['relation']))
    assert len(rel)==152
    layers={(i,j):sum((i,h) in rel and (h,j) in rel for h in range(22)) for i,j in rel}
    hist=[sum(min(n,4)==i for n in layers.values()) for i in range(5)]
    base={edge:(1,-9,16,-8,0)[min(4,n)] for edge,n in layers.items()}
    k={edge:Q(value)-Q(edge in DEVICES,10**11) for edge,value in base.items()}
    assert len(DEVICES & rel)==4
    f4=22-sum(base.values())
    assert hist==[32,22,21,22,55] and f4==28
    anc={n:sorted(i for i,j in rel if j==n) for n in (18,19)}
    outside={17,20}|LATE
    proposed_inside=set(anc[18]) | set(anc[19]) | {18,19}
    assert proposed_inside & outside=={17,20}
    assert tuple(map(Q,witness['beide_radien']))==SPHERES
    assert {(r['praeparation'], Q(r['radius_bei_halb'])) for r in witness['faelle']}=={
        (p,r) for p in ('heavy','light') for r in SPHERES}
    out={}
    for prep in ('heavy','light'):
        row=pair[prep]
        y=[tuple(map(Q,b)) for b in row['clock_box']]
        w=[tuple(map(Q,b)) for b in row['weight_box']]
        clock=[tuple(map(Q,b)) for b in row['normalized_clocks']]
        assert len(y)==len(w)==len(clock)==22 and all(w[i][0]>0 for i in LATE)
        assert all(Q(1,2)<clock[j][0]<=clock[j][1]<=Q(17,32) for j in (17,18,19,20))
        assert all(clock[j][0]>Q(17,32) for j in LATE)
        assert {j for j,(lo,hi) in enumerate(w) if lo==hi==0}=={15,17,20}
        assert sum(lo>0 for lo,hi in w)==19
        ids={id_ for id_ in range(22) if w[id_][0]>0}
        certified=sorted((Q(v['radius_bei_halb']),Q(v['kleinste_quadratische_seitenmarge']),
                          Q(v['kleinste_quadratische_bahnmarge_an_fensterenden']))
                         for v in witness['faelle'] if v['praeparation']==prep)
        assert all(gap>0 and g_ray>0 for _,gap,g_ray in certified)
        assert [r for r,_,_ in certified]==list(SPHERES)
        # Rectangular enclosures may overestimate individual values. A shared field
        # realization produces the very same polynomial, so its *paired* contrast
        # cancels algebraically, independently of these enclosure widths.
        bounds=field_action(y,w,k)
        # Cross-check the polynomial at the rational midpoint using its derivative
        # with respect to the receiver weights (linearity in each weight).
        my=[sum(z)/2 for z in y]; mw=[sum(z)/2 for z in w]
        val=field_action([point(z) for z in my],[point(z) for z in mw],k)
        independently=sum(mw[j]*(19+sum(c*(my[j]-my[i])**2 for (i,b),c in k.items() if b==j)) for j in range(22))
        assert val==point(independently) and bounds[0]<=independently<=bounds[1]
        out[prep]={'F_feld_huelle_dezimal_nach_aussen':outward(bounds),'positive_ereignisse':len(ids),
                   'radiusumgebungen_mit_gleichen_seitendaten':[
                       radius_neighborhood(clock,w,coords,r,z) for r,z in zip(SPHERES,(Q(-1),Q(-9,4)))],
                   'kragengewichte_spaet_positiv':True,'zeitbereich_17_18_19_20':outward((
                       min(clock[i][0] for i in (17,18,19,20)),max(clock[i][1] for i in (17,18,19,20)))),
                   'innerhalb_einer_praeparation_gepaarte_differenz_F_feld':'0'}
    heavy,light=[tuple(map(Q,out[n]['F_feld_huelle_dezimal_nach_aussen'])) for n in ('heavy','light')]
    assert heavy[1]<light[0] or light[1]<heavy[0]
    assert all(pair[x] is None for x in ('physical_radius_heavy','physical_radius_light','external_mass_standard'))
    return {'N':22,'order_id':pair['order_id'],'relationen':len(rel),'schichten_0_1_2_3_ab4':hist,
            'F4_ungeschmiert':f4,'vorgaenger':anc,'register_ueberschneidung':sorted(proposed_inside&outside),
            'zwei_kinematische_radien':list(map(str,SPHERES)),'praeparationen':out,
            'zusaetzliche_radiusabhaengige_randwirkung':'NICHT_FESTGELEGT',
            'physische_verschraenkung_oder_QFI':'NICHT_FESTGELEGT'}


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Python ohne -O starten')
    cli=argparse.ArgumentParser()
    cli.add_argument('vergleichspaar',type=Path)
    cli.add_argument('gegenzeuge',type=Path)
    cli.add_argument('koordinaten',type=Path,nargs='?')
    args=cli.parse_args()
    pos=args.koordinaten or args.vergleichspaar.with_name('Ortskoordinaten.json')
    print(json.dumps(run(checked(args.vergleichspaar,PAIR_SHA),checked(args.gegenzeuge,WITNESS_SHA),checked(pos,COORDS_SHA)),
                     indent=2,ensure_ascii=False))
