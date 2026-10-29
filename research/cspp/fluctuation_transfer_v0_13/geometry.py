"""Safe box enclosures for overlaps of arbitrary 4D Alexandrov intervals.

Exact rational geometric decisions. Unresolved boundary boxes contribute
[0, volume]; no sampled-point estimate is used as a certificate.
"""
from fractions import Fraction as F
from flint import arb
from kernel import require,ball


def before(a,b):return b[0]>a[0] and (b[0]-a[0])**2>sum((x-y)**2 for x,y in zip(a[1:],b[1:]))

def distance_range(point,box):
    low=F(0);high=F(0)
    for c,(a,b) in zip(point,box):
        low+=(a-c)**2 if c<a else (c-b)**2 if c>b else 0
        high+=max((a-c)**2,(b-c)**2)
    return low,high

def classify(interval,box):
    a,b=interval;tl,tu=box[0];da,Da=distance_range(a[1:],box[1:]);db,Db=distance_range(b[1:],box[1:])
    if tu<=a[0] or tl>=b[0]:return -1
    if (tu-a[0])**2<=da or (b[0]-tl)**2<=db:return -1
    if tl>a[0] and tu<b[0] and (tl-a[0])**2>Da and (b[0]-tu)**2>Db:return 1
    return 0

def overlap(intervals,depth=12):
    require(intervals and isinstance(depth,int) and depth>=0,'interval inventory and depth')
    intervals=[(tuple(map(F,a)),tuple(map(F,b))) for a,b in intervals]
    require(all(len(a)==len(b)==4 and before(a,b) for a,b in intervals),'strict timelike endpoints')
    lo=max(a[0] for a,b in intervals);hi=min(b[0] for a,b in intervals)
    if hi<=lo:return arb(0),{'inside_boxes':0,'unresolved_boxes':0}
    box=[(lo,hi)]
    for k in range(1,4):
        l=max(max(a[k]-(b[0]-a[0]),b[k]-(b[0]-a[0])) for a,b in intervals)
        u=min(min(a[k]+(b[0]-a[0]),b[k]+(b[0]-a[0])) for a,b in intervals)
        if u<=l:return arb(0),{'inside_boxes':0,'unresolved_boxes':0}
        box.append((l,u))
    lower=F(0);unknown=F(0);inside=boundary=0;stack=[(box,0)]
    while stack:
        b,level=stack.pop();states=[classify(i,b) for i in intervals]
        if -1 in states:continue
        volume=F(1)
        for l,u in b:volume*=u-l
        if all(s==1 for s in states):lower+=volume;inside+=1;continue
        if level==depth:unknown+=volume;boundary+=1;continue
        k=max(range(4),key=lambda j:b[j][1]-b[j][0]);l,u=b[k];m=(l+u)/2
        left=list(b);right=list(b);left[k]=(l,m);right[k]=(m,u)
        stack.extend([(left,level+1),(right,level+1)])
    return ball(lower).union(ball(lower+unknown)),{'inside_boxes':inside,'unresolved_boxes':boundary}
