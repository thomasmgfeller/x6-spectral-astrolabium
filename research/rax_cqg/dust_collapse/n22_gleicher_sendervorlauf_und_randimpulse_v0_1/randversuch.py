"""Stationary N22 mixed and fixed collar problems, with validated local enclosures."""
from fractions import Fraction as F
from decimal import Decimal as D
from quelle import box,hull,SCALE
from algebra import inv,mid
from feldroehre import POS,absmax
from leseregel import digits,decode,ERROR,REFERENCE

PAST=(0,1,2,15)
FIELDS=(0,1,2,3,7,8,9,10)
SOURCES=(F(-1,10**6),F(0),F(1,10**6))

def build(central,collar):
    y,w=([box(F(s)) for s in central[k]] for k in ('y','w'))
    for j in FIELDS:
        y[j],w[j]=[hull(*map(F,p)) for p in collar[str(j)]]
    return y,w

def evaluate(y,w,J,c,free,axes,cast):
    n=len(y)
    zero=cast(0)
    d=[cast(19) for _ in y]
    g=[zero]*n
    cross=[[zero]*n for _ in y]
    hess=[[zero]*n for _ in y]
    for i,j,k in c:
        p=k*(y[j]-y[i]);t=k*w[j]
        d[j]+=p*(y[j]-y[i]);flow=p*w[j]
        g[i]+=flow;g[j]-=flow
        cross[i][j]+=p;cross[j][j]-=p
        hess[i][j]+=t;hess[j][i]+=t;hess[i][i]-=t;hess[j][j]-=t
    d[16]-=J
    value=[d[j] for j in POS]+[g[i] for i in free]
    jac=[[-2*cross[i][j] for i in axes]+[zero]*len(POS) for j in POS]
    jac.extend([[hess[i][j] for j in axes]+[cross[i][j] for j in POS] for i in free])
    return value,jac,g

def put(y,w,axes,x):
    yy,ww=y.copy(),w.copy()
    for j,v in zip(axes,x):yy[j]=v
    for j,v in zip(POS,x[len(axes):],strict=True):ww[j]=v
    return yy,ww

def predict(y,w,J,coeff,free,axes):
    y=list(map(mid,y));w=list(map(mid,w))
    c=[(i,j,mid(k)) for (i,j),k in coeff.items()]
    x=[y[i] for i in axes]+[w[j] for j in POS]
    for _ in range(4):
        v,jac,_=evaluate(*put(y,w,axes,x),mid(J),c,free,axes,D)
        pre=inv(jac)
        x=[u-sum(a*b for a,b in zip(row,v)) for u,row in zip(x,pre)]
    return [F(u).limit_denominator(10**20) for u in x]

def dot(row,v):
    return sum((a*v[j] for j,a in row),box(0))

def certificate(start,collar,J,coeff,rel,free,target=None,spread=F(0)):
    mixed=target is not None
    axes=tuple(8 if mixed and j==15 else j for j in free)
    y,w=build(start,collar)
    if mixed:y[15]=box(target)
    x=predict(y,w,J,coeff,free,axes)
    cy,cw=put(y,w,axes,list(map(box,x)))
    c=[(i,j,box(k)) for (i,j),k in coeff.items()]
    jbox=box(J)
    _,jac,_=evaluate(cy,cw,jbox,c,free,axes,box)
    C=[[(j,box(a)) for j,a in enumerate(row) if a] for row in inv(jac)]
    # Affine prediction over the target interval using a rational enclosure
    # of an approximate slope. The derivative of the residual is checked below.
    ext_axes=axes+(15,) if mixed else axes
    _,ext,_=evaluate(cy,cw,jbox,c,free,ext_axes,box)
    if spread:
        assert mixed
        fpar=[row[len(axes)] for row in ext]
        slope=[box(-mid(dot(row,fpar))) for row in C]
    else:slope=[box(0)]*len(x)
    par=hull(-spread,spread)
    ry,rw=cy.copy(),cw.copy()
    if mixed:ry[15]=box(target)+hull(-spread,spread)
    jrange=jbox
    line=[box(u)+par*s for u,s in zip(x,slope)]
    basey,basew=put(ry,rw,axes,line)
    v,_,_=evaluate(cy,cw,jbox,c,free,axes,box)
    _,jacline,_=evaluate(basey,basew,jrange,c,free,ext_axes,box)
    # Sensitivity of the residual along the entire affine line by the mean value theorem.
    line_deriv=[]
    for i,row in enumerate(jacline):
        axial=row[:len(axes)]+row[len(ext_axes):]
        extra=row[len(axes)] if spread else box(0)
        line_deriv.append(sum((a*b for a,b in zip(axial,slope,strict=True)),extra))
    radii=[F(1,10**8)]*len(axes)+[F(1,10**9)]*len(POS)
    wide=[v+hull(-r,r) for v,r in zip(line,radii)]
    by,bw=put(ry,rw,axes,wide)
    _,jac,_=evaluate(by,bw,jrange,c,free,axes,box)
    cols=list(zip(*jac))
    norms=[];betas=[]
    for i,row in enumerate(C):
        betas.append(absmax(dot(row,v)+par*dot(row,line_deriv))/radii[i])
        norms.append(sum(absmax(box(int(i==j))-dot(row,col))*r for j,(r,col) in enumerate(zip(radii,cols)))/radii[i])
    q=max(norms); eta=max(a+b for a,b in zip(betas,norms))
    if q>=1 or eta>=1:raise ValueError(f'no contraction q={float(q)}, eta={float(eta)}')
    # Each solution lies in this sharper componentwise image.
    loc=[v+hull(-r*(a+b),r*(a+b)) for v,r,a,b in zip(line,radii,betas,norms)]
    ly,lw=put(ry,rw,axes,loc)
    assert all(ly[i].hi<ly[j].lo for i,j in rel)
    assert all(0<lw[j].lo<=lw[j].hi<SCALE for j in POS) and all(lw[j].lo==lw[j].hi==0 for j in (15,17,20))
    steps=[ly[j]-ly[i] for i,j in ((15,16),(15,18),(17,18),(18,7))]
    assert all(absmax(s)<8 for s in steps)
    _,_,curr=evaluate(ly,lw,jrange,c,free,axes,box)
    assert all(curr[i].contains_zero() for i in free)
    assert all((ly[j].data(),lw[j].data())==(cy[j].data(),cw[j].data()) for j in (0,1,2))
    ab=ly[21].data()
    l,h=map(F,ab)
    ds=list(digits(l-ERROR,h+ERROR))
    decisions=sorted({decode(n,b) for n in ds for b in range(REFERENCE-1,REFERENCE+2)})
    up=lambda v:str(F(-(-v*10**12//1),10**12))
    return {'clock':{str(j):ly[j].data() for j in (0,1,2,3,7,8,15,16,19,20,21)},
            'early_currents':{str(j):curr[j].data() for j in (0,1,2,3)},
            'receiver_codes':[min(ds),max(ds)],'decisions':decisions,'upper_image':up(eta),'upper_contraction':up(q),
            'weights_past':{str(j):lw[j].data() for j in PAST},
            'equations':len(axes)+len(POS),'relations':len(rel),'positive_weights':len(POS)}, (cy,cw,x,axes,ly,lw)
