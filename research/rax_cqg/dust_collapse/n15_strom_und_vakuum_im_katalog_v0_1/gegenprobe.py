"""Second enumeration from the upstream edge iterator and direct polarization of the leaf proofs."""
from itertools import combinations_with_replacement, product
from fractions import Fraction as Q
from math import lcm
import json

from katalog import INNER, n15
from trennnachweis import ROOT, IDS, ACTIVE


def check_masks(expected):
    all_rows={}
    inner=set(INNER)
    boundary=set(n15.support.FUTURE)
    catalogue=n15.support.catalogue()
    assert len(catalogue)==len(set(catalogue))==1048
    for typ in catalogue:
        _,rel=n15.support.geometry(typ)
        graph=n15.variation.edges(n15.encode(rel,15),15)
        maxima={j for j in INNER if not any((j,v) in rel for v in INNER)}
        # At all vertices with no internal successor the nonzero future source has residual -1/64.
        for j in maxima:
            collar=[(v,b) for i,v,b in graph if i==j and v in boundary]
            assert sum(b for v,b in collar)==0 and sum((v-5)*b for v,b in collar)==-1
        def bitset(nodes):
            return sum(1<<INNER.index(i) for i in set(nodes)&inner) | (128 if set(nodes)&boundary else 0)
        plus={j:bitset([v for i,v,b in graph if j==i and b>0]) for j in INNER}
        minus={j:bitset([v for i,v,b in graph if j==i and b<0]) for j in INNER}
        rows=[]
        for mask in range(128):
            if bitset(maxima)&mask!=bitset(maxima):continue
            quiet=[]
            for k,i in enumerate(INNER):
                if mask&(1<<k):continue
                p=plus[i]&(mask|128);m=minus[i]&(mask|128)
                if bool(p)!=bool(m):break
                if not p:quiet.append(i)
            else:
                if quiet:rows.append({'mask':mask,'quiet':quiet})
        if rows:all_rows[str(typ)]=rows
    assert all_rows==expected


def leaf(vertices,coef,edges):
    # Use a homogeneous bilinear expression on pairs of vertices, without midpoint evaluations.
    den=lcm(6,*(v.denominator*6 for row in vertices for v in row))
    clocks=[]
    for row in vertices:
        y=[-5*den,-4*den,-3*den,-11*den//6,-11*den//6,0,0,2*den,3*den,4*den,5*den,0,0,0,0]
        for j,z in zip(IDS,row):y[j]=(-11*den+23*(den//z.denominator)*z.numerator)//6
        clocks.append(y)
    # 2*den² times the quadratic Bernstein coefficient of the separating functional.
    gd=dict(zip(IDS,coef[2:]))
    for u,v in product((0,64),repeat=2):
        weights={13:u,14:v,**dict.fromkeys(n15.support.FUTURE,1)}
        terms=[(i,j,coef[ACTIVE.index(j)]*b if j in ACTIVE else 0,
                (gd.get(i,0)-gd.get(j,0))*b*weights.get(j,0)*den)
               for i,j,b in edges if b]
        for a,c in combinations_with_replacement(clocks,2):
            bound=38*den**2*sum(coef[:2])
            for i,j,quadratic,linear in terms:
                da=a[j]-a[i];dc=c[j]-c[i]
                bound+=2*quadratic*da*dc+linear*(da+dc)
            assert bound>0


def check_tree():
    def walk(z,node,edges):
        if 'p' in node:
            leaf(z,node['p'],edges)
            return 1
        i,j=node['s']
        center=tuple((a+b)/2 for a,b in zip(z[i],z[j]))
        l,r=z.copy(),z.copy();l[i]=r[j]=center
        return walk(l,node['a'],edges)+walk(r,node['b'],edges)
    count=0
    for name,tree in json.loads((ROOT/'Trennzertifikate.json').read_text()).items():
        typ,order=name.split(':');seq=list(map(int,order.split('-')))
        _,rel=n15.support.geometry(int(typ))
        edges=n15.variation.edges(n15.encode(rel,15),15)
        z=[tuple(Q(seq.index(j)>=n) for j in IDS) for n in range(7)]
        count+=walk(z,tree,edges)
    return count
