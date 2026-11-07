"""A declared regulated matter-action candidate, not qualified CST dust physics."""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
from gluing import intervals, pairs, valid, action as gravity_action


def kernel(k):
    return (1,-9,16,-8)[k] if k<4 else 0


def edges(code,n,nodes=None):
    nodes=(1<<n)-1 if nodes is None else nodes
    return [(y,x,kernel((inside&nodes).bit_count())) for y,x,inside in intervals(code,n)
            if nodes&(1<<y) and nodes&(1<<x)]


def gamma(code,n,T,nodes=None):
    result=[Q(0)]*n
    for y,x,b in edges(code,n,nodes):
        result[x]+=Q(b,2)*(T[x]-T[y])**2
    return result


def gamma_from_operator(code,n,T):
    """Independent product-identity form including the potential subtraction."""
    B=[[Q(-int(i==j)) for j in range(n)] for i in range(n)]
    for y,x,b in edges(code,n):B[x][y]=Q(b)
    return [sum(B[x][y]*(T[y]**2-2*T[x]*T[y]+T[x]**2) for y in range(n))/2
            for x in range(n)]


def matter_action(code,n,T,w,nodes=None):
    nodes=(1<<n)-1 if nodes is None else nodes
    g=gamma(code,n,T,nodes)
    return -sum(w[i]*(g[i]+1) for i in range(n) if nodes&(1<<i))/2


def current_and_gradient(code,n,T,w):
    current=[];grad=[Q(0)]*n
    for y,x,b in edges(code,n):
        j=Q(b,2)*w[x]*(T[x]-T[y]);current.append((y,x,j))
        grad[y]+=j;grad[x]-=j
    return current,grad


def laplacian(code,n,w):
    L=[[Q(0) for _ in range(n)] for _ in range(n)]
    for y,x,b in edges(code,n):
        a=Q(b,2)*w[x]
        L[x][x]+=a;L[y][y]+=a;L[x][y]-=a;L[y][x]-=a
    return L


def matter_coupling(code,n,T,w,a,b):
    """Cross-pair and internal interval regrading terms, isolated-block convention."""
    cross=regrade=Q(0);ambient=a|b
    for y,x,inside in intervals(code,n):
        if not ambient&(1<<x) or not ambient&(1<<y):continue
        factor=-w[x]*(T[x]-T[y])**2/4
        full=kernel((inside&ambient).bit_count())
        if bool(a&(1<<x)) != bool(a&(1<<y)):
            cross+=factor*full
        else:
            block=a if a&(1<<x) else b
            regrade+=factor*(full-kernel((inside&block).bit_count()))
    return cross,regrade


def finite_geometry_response(code,other,n,T,w,kappa=Q(1)):
    left={(y,x):b for y,x,b in edges(code,n)}
    right={(y,x):b for y,x,b in edges(other,n)}
    matter=-sum(w[x]*(right.get((y,x),0)-left.get((y,x),0))*(T[x]-T[y])**2
                for y,x in set(left)|set(right))/4
    grav=kappa*(gravity_action(other,n)-gravity_action(code,n))
    return grav,matter


def interval_carrier(code,n):
    """One fixed initial/final element; exact special case of the declared carrier."""
    if n<2 or not valid(code,n):return False
    rel=set(pairs(code,n))
    return all((0,x) in rel and (x,n-1) in rel for x in range(1,n-1)) and (0,n-1) in rel

