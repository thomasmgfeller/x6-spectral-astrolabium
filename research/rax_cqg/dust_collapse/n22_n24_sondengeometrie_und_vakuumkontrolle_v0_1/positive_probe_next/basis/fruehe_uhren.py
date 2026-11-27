"""Project D16 and D19 jointly onto the clock boxes when their rows are intact."""
from fractions import Fraction as Q
from intervall import I, S, Empty, Singular, point
from filter import intersect,hull,Z
EPS=Q(1,10**11)

def match(m,j,row):
    return {i:k for i,k,c in m.inc[j]}==row

def first_projection(m,y):
    if not match(m,16,{0:-8,1:16,2:-9,15:1-EPS}) or not match(m,19,{1:-8,2:16,15:-9,16:1}):
        return None
    early=[(-8,y[0]),(16,y[1]),(-9,y[2])]
    offset=19+sum((k*(-1-v).sq() for k,v in early),Z)
    slope=2*sum((k*(-1-v) for k,v in early),Z)
    pending=[y[16]];kept=[]
    while pending:
        a=pending.pop()
        try:
            x=a+1
            u=(a-(-(offset+x*(slope-x))/point(1-EPS)).sqrt()).cut(y[15])
            if u.h<=y[2].l:continue
            inp=[(-8,y[1]),(16,y[2]),(-9,u),(1,a)]
            h=sum((k*v for k,v in inp),Z)
            d=19+sum((k*(-1-v).sq() for k,v in inp),Z)
            residual=d-2*h*(y[19]+1)
            if residual.l>0 or residual.h<0:continue
            p=(-1+d/(2*h)).cut(y[19]).cut(I(a.l,y[7].h))
        except Empty:continue
        except Singular:
            if a.h-a.l<=S//4096:
                # Retain all values when the rational formula cannot decide.
                kept.append((a,y[15],y[19],h))
                continue
        else:
            if a.h-a.l<=S//4096:
                kept.append((a,u,p,h))
                continue
        pending.extend(a.halves())
    if not kept:raise Empty("D16 und D19 gemeinsam")
    for j,vals in zip((16,15,19),zip(*kept)):
        intersect(y,j,hull(vals))
    return hull([t[3] for t in kept])

def sharpen(m,y,w):
    h=first_projection(m,y)
    if h is None or h.l<=0:return
    inc18={1:-8,2:16,15:-9,16:1-EPS,17:1-EPS,20:1}
    actual={i:k for i,k,_ in m.inc[18]}
    if actual!=inc18 and actual!={**inc18,22:1}:return
    out18={7:1-EPS,8:-9,9:16,10:-8}
    if {j:k for j,k,_ in m.out[18]}!=out18:return
    def force(x):
        return (sum((point(k)*w[j]*y[j] for j,k in out18.items()),Z)
                -x*sum((point(k)*w[j] for j,k in out18.items()),Z))
    if force(y[18]).h>=0:return
    greatest=y[7]-y[0]
    assert greatest.h<8*S and y[22].l>y[0].l and y[22].h<y[7].h
    slack=point(16*EPS)
    upper=y[19]+h/2+slack+slack.sq()/(2*h)
    y[18]=I(max(y[18].l,(y[19]-point(128*EPS)/(2*h)).l),min(y[18].h,upper.h))
    w[18]=I(max(w[18].l,(-force(y[18])/(h+slack)).l),w[18].h)
    twin={7:-9,8:16,9:-8,18:1,21:1}
    if {j:k for j,k,_ in m.out[20]}!=twin or {j:k for j,k,_ in m.out[17]}!={**twin,18:1-EPS}:return
    base=-9*w[7]+16*w[8]-8*w[9]
    total=base+w[18]+w[21]
    if total.l<=0:return
    diff=point(EPS)*w[18]*(y[18]-y[17])/total
    intersect(y,17,y[20]-diff);intersect(y,20,y[17]+diff)
