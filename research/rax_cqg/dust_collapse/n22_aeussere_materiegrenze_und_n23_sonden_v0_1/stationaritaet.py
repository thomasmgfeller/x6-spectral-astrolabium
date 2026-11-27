"""Necessary stationary equations for the unforced inserted event."""
from fractions import Fraction as F
from geometrie import mul,diff,square

def add(a,b): return a[0]+b[0],a[1]+b[1]
def const(a): return F(a),F(a)
def scale(a,s): return mul(a,const(s))
def ratio(a,b):
    assert b[0]*b[1]>0
    return mul(a,(1/b[1],1/b[0]))
def kernel(rel):
    return {(i,j):(1,-9,16,-8,0)[min(4,sum((i,k) in rel and (k,j) in rel for k in range(23)))] for i,j in rel}
def terms(c,j):
    return {i:k for (i,t),k in c.items() if t==j and k}
def density(inc,y,z):
    d=const(19)
    for j,k in inc.items():d=add(d,scale(square(diff(z,y[j])),k))
    return d
def derivative(inc,y,z):
    d=const(0)
    for j,k in inc.items():d=add(d,scale(diff(z,y[j]),2*k))
    return d

def check(rel,ext,y,w):
    relation=rel|{(i,22) for i in ext['past']}|{(22,j) for j in ext['future']}
    coeff=kernel(relation)
    assert set(ext['future'])=={7,8,9,10}
    corrections=((15,16),(16,18),(17,18),(18,7))
    assert not any(j in {4,5,6,11,22} or i==22 for i,j in corrections)
    # Below only the positive ancestors and the original collar are used.
    fixed={j:y[j] for j in [0,1,2,3,7,8,9,10]}
    raw=terms(coeff,4)
    assert raw==terms(coeff,5)==terms(coeff,6)=={0:-8,1:16,2:-9,3:1}
    slope=derivative(raw,fixed,const(0))
    assert sum(raw.values())==0 and slope[1]<0
    first=ratio(scale(density(raw,fixed,const(0)),-1),slope)
    assert first[0]>fixed[3][1]
    fixed.update({i:first for i in [4,5,6]})
    # Convex quadratic negative at the latest parent; its only causal zero
    # is bracketed by two rational endpoints with certified opposite signs.
    inc=terms(coeff,11)
    assert inc=={2:-8,3:16,4:1,5:1} and sum(inc.values())>0
    assert density(inc,fixed,first)[1]<0
    mid=sum(y[11])/2
    bracket=mid-F(1,10**6),mid+F(1,10**6)
    assert bracket[0]>first[1]
    assert density(inc,fixed,const(bracket[0]))[1]<0
    assert density(inc,fixed,const(bracket[1]))[0]>0
    fixed[11]=bracket
    def time(x):
        return add(scale(fixed[3],1-x),scale(fixed[7],x))
    edges=terms(coeff,22)
    if 6 in ext['past']:
        assert edges=={4:-9,5:-9,6:1,11:1}
        assert terms(coeff,12)==edges
    else: assert edges=={3:-8,4:-9,5:-9,11:1}
    zl=time(F(15,32));zr=time(F(17,32))
    left=density(edges,fixed,zl)
    slope_window=derivative(edges,fixed,(zl[0],zr[1]))
    assert left[1]<F('-1.31') and slope_window[1]<0
    entire=(density(edges,fixed,zr)[0],left[1])
    def zero_clock(z):
        result=const(0)
        for j in ext['future']:
            result=add(result,scale(mul(w[j],diff(fixed[j],z)),coeff[22,j]))
        return result
    assert [coeff[22,j] for j in range(7,11)]==[1,-9,16,-8]
    edge_values=[zero_clock(time(i)) for i in (0,1)]
    assert all(a[1]<0 for a in edge_values)
    return dict(incoming=edges,event_4_5_6=first,early_slope=slope,event_11=bracket,
                D22_window=entire,D22_center=density(edges,fixed,time(F(1,2))),
                D22_derivative_window=slope_window,
                empty_G22_on_0_to_1=(min(a[0] for a in edge_values),max(a[1] for a in edge_values)),
                empty_G22_center=zero_clock(time(F(1,2))),status='EXCLUDED_FREE_PROBE')
