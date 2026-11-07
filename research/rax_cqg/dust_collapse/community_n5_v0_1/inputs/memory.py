"""Exact full-past growth representation, not a physical growth law."""
from fractions import Fraction as Q
from functools import lru_cache

B=(1,-9,16,-8)
def bits(mask):return [i for i in range(mask.bit_length()) if mask>>i&1]
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
@lru_cache(None)
def ideals(pred):
    return tuple(s for s in range(1<<len(pred)) if all(not pred[i]&~s for i in bits(s)))
@lru_cache(None)
def natural_orders(n):
    if n==0:return ((),)
    return tuple(p+(s,) for p in natural_orders(n-1) for s in ideals(p))
@lru_cache(None)
def extensions(pred):
    n=len(pred)
    @lru_cache(None)
    def f(chosen):
        if chosen==(1<<n)-1:return 1
        return sum(f(chosen|(1<<i)) for i in range(n) if not chosen>>i&1 and not pred[i]&~chosen)
    return f(0)
def with_anchor(pred,close=False):
    out=(0,)+tuple((s<<1)|1 for s in pred)
    return out+((1<<len(out))-1,) if close else out
def relabel(pred,order):
    pos={old:new for new,old in enumerate(order)}
    return tuple(sum(1<<pos[j] for j in bits(pred[i])) for i in order)
def code(pred):
    n=len(pred);return sum(1<<(i*n+j) for j,s in enumerate(pred) for i in bits(s))
def from_code(value,n):return tuple(sum(1<<i for i in range(n) if value>>(i*n+j)&1) for j in range(n))
def intervals(pred):
    for x,px in enumerate(pred):
        for y in bits(px):
            k=sum(bool(px>>z&1 and pred[z]>>y&1) for z in range(len(pred)))
            yield y,x,k
def gravity(pred):return len(pred)-sum(B[k] for _,_,k in intervals(pred) if k<4)
def matter(pred,T,w):
    return -sum(w,Q(0))/2-sum((w[x]*B[k]*(T[x]-T[y])**2/4 for y,x,k in intervals(pred) if k<4),Q(0))
def signature(pred,past,T):
    """Sufficient for this proposed next past ideal, not a universal small state."""
    require(past in ideals(pred),'Past must be an ideal')
    rows=[[Q(0),Q(0),Q(0)] for _ in range(4)]
    for y in bits(past):
        k=sum(bool(past>>z&1 and pred[z]>>y&1) for z in range(len(pred)))
        if k<4:
            for j in range(3):rows[k][j]+=T[y]**j
    return rows
def increment(pred,past,T,t,w):
    rows=signature(pred,past,T)
    g=1-sum(B[k]*rows[k][0] for k in range(4))
    s=-w/2-w/4*sum(B[k]*(rows[k][0]*t*t-2*rows[k][1]*t+rows[k][2]) for k in range(4))
    return g,s
def norm_factor(pred):
    e=extensions(pred)
    return sum((Q(e,extensions(pred+(s,)))**2 for s in ideals(pred)),Q(0))
def pullback(horizon,terminal):
    weights={(horizon,p):terminal(p) for p in natural_orders(horizon)}
    for n in range(horizon-1,-1,-1):
        for p in natural_orders(n):
            e=extensions(p)
            weights[n,p]=sum((Q(e,extensions(p+(s,)))**2*weights[n+1,p+(s,)] for s in ideals(p)),Q(0))
    return weights
