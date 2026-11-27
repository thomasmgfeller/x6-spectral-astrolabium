"""Exact rational inequalities on archived clock boxes, with c = 1."""
from fractions import Fraction as F
from itertools import combinations
HALF = F(1,2)
SPEED = F(1,8)
BALLS = [((F(0),F(0),F(-1)), F(1)), ((F(0),F(0),F(-5,2)), F(2))]
def sub(a,b): return tuple(x-y for x,y in zip(a,b,strict=True))
def dot(a,b): return sum(x*y for x,y in zip(a,b,strict=True))
def norm2(a): return dot(a,a)
def diff(a,b): return a[0]-b[1],a[1]-b[0]
def square(a):
    p,q=a
    return (0 if p<=0<=q else min(p*p,q*q), max(p*p,q*q))
def dist2(p,q): return norm2(sub(p,q))
def mul(a,b):
    v=[i*j for i in a for j in b]
    return min(v),max(v)
def inside_clock(clock,weights):
    window={i for i,(lo,hi) in enumerate(clock) if F(15,32)<=lo<=hi<=F(17,32)}
    assert all(hi<F(15,32) or lo>F(17,32) for i,(lo,hi) in enumerate(clock) if i not in window)
    assert window=={17,18,19,20}
    positive={j for j,(lo,hi) in enumerate(weights) if lo>0}
    assert all(weights[j]==(0,0) for j in set(range(len(clock)))-positive)
    assert positive&window=={18,19}
    return positive

def causal(p,x,rel):
    margins=[]
    for i,j in combinations(range(len(p)),2):
        t=diff(x[j],x[i])
        s=dist2(p[i],p[j]); lo,hi=square(t)
        if (i,j) in rel or (j,i) in rel:
            assert (i,j) not in rel or t[0]>0
            assert (j,i) not in rel or t[1]<0
            margins.append(lo-s)
        else: margins.append(s-hi)
    assert len(margins)==231 and min(margins)>0
    return min(margins)

def balls(p,x,positive):
    results=[]
    for center,r0 in BALLS:
        radial=[]; gaps=[]; sites=[]
        for i,t in enumerate(x):
            rlo,rhi=[r0-SPEED*(v-HALF) for v in reversed(t)]
            assert 0<rlo<=rhi
            d2=dist2(p[i],center)
            s=(d2/rhi**2,d2/rlo**2)
            assert (s[1]<1 if i in positive else s[0]>1)
            gaps.append(rlo*rlo-d2 if i in positive else d2-rhi*rhi)
            if i in positive: radial.append(s)
            sites.append(s)
        # Distinct advected radial coordinates permit a single smooth radial density
        # for this sphere and this preparation across all 19 positive events.
        radial.sort()
        sep=min(b[0]-a[1] for a,b in zip(radial,radial[1:]))
        assert sep>0 and len(radial)==19
        results.append(dict(R=r0,area_in_pi=4*r0*r0,
                            squared_margin=min(gaps),site_gap=sep,material_coordinates_squared=sites))
    return results

def probes(p,x,rel,extend=True):
    rows=[]
    for i,j in sorted(rel):
        if extend and x[j][1]>=HALF:continue
        if not extend and not x[i][1]<HALF<x[j][0]:continue
        dt=diff(x[j],x[i])
        assert dt[0]>0
        num=HALF-x[i][1],HALF-x[i][0]
        alpha=(num[0]/dt[1],num[1]/dt[0])
        if not extend: assert 0<alpha[0]<=alpha[1]<1
        pt=[]
        for b,a in zip(p[j],p[i]):
            l,h=mul(alpha,(b-a,b-a));pt.append((a+l,a+h))
        signs=[]
        for center,r in BALLS:
            ds=[square((a-c,b-c)) for (a,b),c in zip(pt,center)]
            s=(sum(t[0] for t in ds),sum(t[1] for t in ds))
            sign='innen' if s[1]<r*r else ('aussen' if s[0]>r*r else 'offen')
            signs.append(dict(tag=sign,d2=s))
        rows.append(dict(von=i,durch=j,alpha=alpha,point_box=pt,balls=signs))
    return rows

def extended_order(p, clocks, relation, probe):
    """Causal past and future of probe 22, certified on its position and time boxes."""
    point=probe['point_box']
    past=[];future=[];unrelated=[]
    for k,(v,t) in enumerate(zip(p,clocks,strict=True)):
        terms=[square((lo-c,hi-c)) for (lo,hi),c in zip(point,v)]
        spatial=sum(a for a,b in terms),sum(b for a,b in terms)
        time=square((HALF-t[1],HALF-t[0]))
        if spatial[1]<time[0]:
            assert t[1]<HALF or t[0]>HALF
            (past if t[1]<HALF else future).append(k)
        else:
            assert spatial[0]>time[1], (probe['von'],k)
            unrelated.append(k)
    new=relation|{(k,22) for k in past}|{(22,k) for k in future}
    assert all((i,k) in new for i,j in new for l,k in new if j==l)
    assert probe['von'] in past and probe['durch'] in past
    return dict(past=past,future=future,incomparable=unrelated,relations=len(new))

def contact_test(p,x,rel,positive):
    # Rotate one short vector around the unaltered point 17. Its radius is
    # identical at both endpoints, so the 17--20 invariant interval is fixed.
    a=sub(p[19],p[17]); scale=F(1,10000)
    b=tuple(v*scale for v in a); other=b[1:]+b[:1]
    assert norm2(b)==norm2(other)
    ta=diff(x[19],x[17]); tb=diff(x[20],x[17])
    assert norm2(b)>square(tb)[1]
    # Whole orientation sphere. Euclidean displacements bounded by U, with
    # U chosen rationally above sqrt(norm2(b)).
    U=F(1,40000);assert norm2(b)<U**2
    for j in range(len(p)):
        if j in (17,20):continue
        dt=square(diff(x[20],x[j])); s=dist2(p[17],p[j])
        if (20,j) in rel or (j,20) in rel:
            h=dt[0]-s-U**2; assert h>0 and h*h>4*s*U**2
        else:
            h=s-dt[1]-U**2; assert h>0 and h*h>4*dt[1]*U**2
    for center,r in BALLS:
        rmax=r-SPEED*(x[20][0]-HALF)
        assert dist2(p[17],center)>(rmax+U)**2
    cases=[]
    for name,q in [('parallel',b),('gedreht',other)]:
        new=list(p);new[20]=tuple(v+w for v,w in zip(p[17],q))
        margin=causal(new,x,rel);balls(new,x,positive)
        # det = |a×q|² - |t_a q - t_b a|², with metric (-,+,+,+).
        base=norm2(a)*norm2(q)-dot(a,q)**2
        terms=[square(diff(mul(ta,(u,u)),mul(tb,(v,v)))) for u,v in zip(q,a)]
        det=base-sum(z[1] for z in terms),base-sum(z[0] for z in terms)
        assert det[1]<0 if name=='parallel' else det[0]>0
        cases.append(dict(lage=name,det=det,squared_causal_margin=margin))
    return cases
