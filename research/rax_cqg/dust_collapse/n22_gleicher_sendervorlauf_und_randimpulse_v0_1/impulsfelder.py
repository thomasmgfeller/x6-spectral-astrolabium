"""Joint residual and Jacobian for fixed early clock momenta."""
from feldroehre import POS

def fields(y,w,source,coeff,free,axes,goals,cast):
    zero=cast(0);n=len(y)
    d=[cast(19)]*n;g=[zero]*n
    cross=[[zero]*n for _ in y];hess=[[zero]*n for _ in y]
    for i,j,k in coeff:
        dy=y[j]-y[i];p=k*dy;t=k*w[j];f=w[j]*p
        d[j]+=p*dy;g[i]+=f;g[j]-=f
        cross[i][j]+=p;cross[j][j]-=p
        hess[i][i]-=t;hess[j][j]-=t;hess[i][j]+=t;hess[j][i]+=t
    d[16]-=source
    rows=[('d',j) for j in POS]+[('g',j) for j in free]+[('y',15)]+[('g',i) for i in range(4)]
    vals=[d[j] for j in POS]+[g[j] for j in free]+[y[15]-goals[0]]+[g[i]-goals[i+1] for i in range(4)]
    def entry(r,i,k,j):
        if r=='d':return -2*cross[j][i] if k=='y' else zero
        if r=='g':return hess[i][j] if k=='y' else cross[i][j]
        return cast(int(k=='y' and j==i))
    return vals,[[entry(r,i,k,j) for k,j in axes] for r,i in rows],g
