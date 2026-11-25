"""Independent root count and finite differences using the published matter_action implementation."""
from fractions import Fraction as F
from itertools import product
from math import gcd,lcm
import dynamik as dy
from gluing import encode


def primitive(p):
    while p and not p[-1]:p.pop()
    if not p:return []
    g=gcd(*p)
    return [k//g for k in p]


def sturm(p,a,b):
    def sign(poly,q):
        u,v=q.numerator,q.denominator
        val=poly[-1];den=v
        for x in reversed(poly[:-1]):
            val=val*u+x*den;den*=v
        return (val>0)-(val<0)
    chain=[primitive(p[:]),primitive([j*k for j,k in enumerate(p) if j])]
    while True:
        v=chain[-1];w=chain[-2][:]
        while len(w)>=len(v):
            d=len(w)-len(v);a1=w[-1]*(1 if v[-1]>0 else -1)
            w=[k*abs(v[-1]) for k in w]
            for j,x in enumerate(v):w[j+d]-=a1*x
            w=primitive(w)
        if not w:break
        chain.append([-k for k in w])
    def changes(x):
        s=[sign(row,x) for row in chain]
        s=[v for v in s if v]
        return sum(p!=q for p,q in zip(s,s[1:]))
    return changes(a)-changes(b)


def relation(a,b):
    return a!=b and b[0]-a[0]>=12*abs(b[1]-a[1])


def full_interval(dt,k):
    a,b=(0,6),(dt,6+k)
    items=[a]+[(t,x) for t in range(1,dt) for x in range(13)
               if relation(a,(t,x)) and relation((t,x),b)]+[b]
    return items


def original_action_probe(dt,k,expected):
    points=full_interval(dt,k);n=len(points)
    rel=[(i,j) for i,p in enumerate(points) for j,q in enumerate(points) if relation(p,q)]
    code=encode(rel,n);w=[F(j+1,3*n) for j in range(n)]
    eta=F(1,8);answer=0
    for a,b in product((1,-1),repeat=2):
        y=[F(t) for t,x in points];y[0]+=a*eta;y[-1]+=b*eta
        assert all(y[i]<y[j] for i,j in rel)
        answer+=a*b*dy.variation.matter_action(code,n,y,w)
    assert answer/(2*eta**2)==expected*w[-1]


def run(rows):
    # Count intermediate events explicitly using order comparisons rather than the column-length formula.
    kernel={}
    for k in range(-5,6):
        for dt in range(max(1,12*abs(k)),12*abs(k)+6):
            count=len(full_interval(dt,k))-2
            b=dy.variation.kernel(count)
            if b:kernel[dt,k]=b
    assert {(d,k):b for d,k,b in dy.STENCIL}==kernel
    for (dt,k),val in kernel.items():
        original_action_probe(dt,k,val)
    for dt,k in [(5,0),(14,1),(49,-4),(60,5)]:
        original_action_probe(dt,k,0)
    results={}
    for radius,roots in rows.items():
        r=F(radius)
        coeff=[sum(b*t*r**k for (t,k),b in kernel.items() if t==j) for j in range(49)]
        coeff[0]=-sum(b*t for (t,k),b in kernel.items())
        data=[F(v) for v in coeff];den=lcm(*(k.denominator for k in data))
        p=[int(v*den) for v in data]
        num=sturm(p,F(1,2),F(2))
        assert num==len(roots)
        for a,b in roots:assert sturm(p,F(a),F(b))==1
        results[radius]=num
    return {'sturm_counts':results,'original_action_pairs':len(kernel)+4}
