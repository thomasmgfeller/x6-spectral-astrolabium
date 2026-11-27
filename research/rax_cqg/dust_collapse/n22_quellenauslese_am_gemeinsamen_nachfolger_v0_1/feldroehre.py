"""Uniform contraction on a drift interval around one affine stationary-state predictor."""
from fractions import Fraction as F
from quelle import box,hull,Box,SCALE
from algebra import inv
from ableitung import Jet,prepare
from leserbasis import LIMIT

COLLAR=(0,1,2,3,7,8,9,10)
POS=(4,5,6,11,12,13,14,16,18,19,21)
def absmax(b):return F(max(abs(b.lo),abs(b.hi)),SCALE)

def intersect(a,b):
    return Box(max(a.lo,b.lo),min(a.hi,b.hi))

def solution_line(data):
    center=data['0']
    slopes={}
    for key in ('y','w'):
        lo,hi=data[str(-LIMIT)][key],data[str(LIMIT)][key]
        slopes[key]=[(F(v)-F(u))/(2*LIMIT) for u,v in zip(lo,hi,strict=True)]
    return {k:[(F(c),s) for c,s in zip(center[k],slopes[k],strict=True)] for k in slopes}

def states(line,drift,collar):
    ys,ws=([Jet(box(c)+drift*s,s) for c,s in line[k]] for k in ('y','w'))
    for j in COLLAR:
        ys[j],ws[j]=collar[0][j],collar[1][j]
    return ys,ws

def field(y,w,source,coeff):
    D=[Jet(19) for _ in y]
    G=[Jet(0) for _ in y]
    for (i,j),k in coeff.items():
        gap=y[j]-y[i]
        v=k*gap
        D[j]+=v*gap
        flow=v*w[j]
        G[i]+=flow
        G[j]-=flow
    D[16]-=source
    return D,G

def jacobian(y,w,coeff,free):
    n=len(y)
    cross=[[box(0) for _ in y] for _ in y]
    hessian=[[box(0) for _ in y] for _ in y]
    for (i,j),k in coeff.items():
        p=k*(y[j]-y[i]);v=k*w[j]
        cross[i][j]+=p
        cross[j][j]-=p
        hessian[i][j]+=v
        hessian[j][i]+=v
        hessian[i][i]-=v
        hessian[j][j]-=v
    return [[-2*cross[i][j] for i in free]+[box(0)]*len(POS) for j in POS]+[
        [hessian[i][j] for j in free]+[cross[i][j] for j in POS] for i in free]

def preconditioner(x,y,coeff,free):
    C=inv(jacobian([k.v for k in x],[k.v for k in y],coeff,free))
    return [[(i,box(c)) for i,c in enumerate(row) if c] for row in C]

def project(row,v):
    return sum((c*v[k] for k,c in row),box(0))

def up(v,scale=10**12):return str(F(-(-v*scale//1),scale))

def certify(env,left,right):
    y,w,rel,coeff,free,J,line,functions,C=env
    m=(left+right)/2
    spread=hull(left-m,right-m)
    cm=prepare(y,w,m,m,J,functions)
    cb=prepare(y,w,left,right,J,functions) if left!=right else cm
    for j in (0,1,2):
        for part,expected in zip(cb,[(F(-5),F(-4),F(-3))[j],F(1,8)]):
            value=part[j]
            assert value.v.lo==value.v.hi==expected*SCALE and value.d.lo==value.d.hi==0
    for b,c in zip(cb,cm):
        for j in COLLAR:
            b[j]=Jet(intersect(b[j].v,c[j].v+spread*b[j].d),b[j].d)
    ym,wm=states(line,box(m),cm)
    yb,wb=states(line,hull(left,right),cb)
    D,G=field(ym,wm,J,coeff)
    mid=[D[j].v for j in POS]+[G[j].v for j in free]
    D,G=field(yb,wb,J,coeff)
    deriv=[D[j].d for j in POS]+[G[j].d for j in free]
    # Weighted sup-norm on errors about X_0+s*drift.
    radii=[F(1,10**8) if j in (15,21) else F(1,10**7) for j in free]+[F(1,10**8)]*len(POS)
    yy=[b.v for b in yb];ww=[b.v for b in wb]
    for i,j in enumerate(free):
        yy[j]+=hull(-radii[i],radii[i])
    for i,j in enumerate(POS):
        ww[j]+=hull(-radii[len(free)+i],radii[len(free)+i])
    jac=jacobian(yy,ww,coeff,free)
    cols=list(zip(*jac))
    betas=[];norms=[]
    for i,row in enumerate(C):
        p=project(row,mid)+spread*project(row,deriv)
        betas.append(absmax(p)/radii[i])
        norm=sum(absmax(int(i==j)-project(row,col))*radii[j] for j,col in enumerate(cols))
        norms.append(norm/radii[i])
    q=max(norms)
    eta=max(a+b for a,b in zip(betas,norms))
    if eta>=1:
        return None
    assert q<1 and all(yy[i].hi<yy[j].lo for i,j in rel)
    assert all(ww[j].lo>0 and ww[j].hi<SCALE for j in POS)
    assert all(ww[j].lo==ww[j].hi==0 for j in set(free)-set(POS))
    pointer=(yy[16]-yy[15],yy[18]-yy[15],yy[18]-yy[17],yy[7]-yy[18])
    assert all(absmax(v)<8 for v in pointer)
    terminal=2*yy[21]-(-8*yy[2]+16*yy[15]-9*yy[16]+yy[17]+yy[19]+yy[20])
    assert terminal.contains_zero()
    def component(j):
        k=free.index(j)
        err=radii[k]*(betas[k]+norms[k])
        return (yb[j].v+hull(-err,err)).data()
    assert (15,16) in rel and (16,21) in rel
    return dict(drift=[str(left),str(right)],receiver=component(21),antecedent=component(15),
                upper_contraction=up(q),upper_image=up(eta),equations=len(radii),
                relations=len(rel),positive_weights=len(POS))

def environment(y,w,rel,coeff,free,source,line,fun):
    assert tuple(j for j in free if j not in (15,17,20))==POS
    ref=prepare(y,w,F(0),F(0),source,fun)
    sy,sw=states(line,box(0),ref)
    return (y,w,rel,coeff,free,source,line,fun,preconditioner(sy,sw,coeff,free))
