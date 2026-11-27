"""Validated fixed-point solutions at one pair of fixed future coordinates."""
from fractions import Fraction as F
from decimal import Decimal as D
from quelle import box,hull,SCALE
from algebra import mid,inv
from feldroehre import POS,absmax
from randversuch import build,dot
from impulsfelder import fields
from impulsabgleich import coords,setcoords
from leseregel import digits,decode,ERROR,REFERENCE
from zukunftsbasis import FUTURE,name

def upper(x,scale=10**12):
    return str(F(-(-x*scale//1),scale))

def coefficients(coeff,cast):
    return [(i,j,cast(k)) for (i,j),k in sorted(coeff.items())]

def certify(seed,collar,source,coeff,free,rel,goals,fixed):
    inner=[('y',i) for i in free]+[('w',i) for i in POS]
    extra=[a for a in FUTURE if a not in fixed]
    axes=inner+extra
    by,bw=build(seed,collar)
    y,w=list(map(mid,by)),list(map(mid,bw))
    x=coords(y,w,axes)
    dec=coefficients(coeff,mid)
    for _ in range(6):
        v,A,_=fields(*setcoords(y,w,axes,x),mid(source),dec,free,axes,list(map(mid,goals)),D)
        C=inv(A)
        x=[a-sum(k*t for k,t in zip(row,v)) for a,row in zip(x,C)]
    x=[box(F(a).limit_denominator(10**21)) for a in x]
    cy,cw=setcoords(by,bw,axes,x)
    c=coefficients(coeff,box)
    val,amat,_=fields(cy,cw,box(source),c,free,axes,list(map(box,goals)),box)
    pre=[[(j,box(k)) for j,k in enumerate(row) if k] for row in inv(amat)]
    rs=[F(1,10**10 if t=='y' else 10**11) for t,j in axes]
    yy,ww=setcoords(by,bw,axes,[a+hull(-r,r) for a,r in zip(x,rs)])
    _,jac,_=fields(yy,ww,box(source),c,free,axes,list(map(box,goals)),box)
    image=[];norm=[]
    for i,row in enumerate(pre):
        norm.append(sum(absmax(int(i==j)-dot(row,col))*r for j,(r,col) in enumerate(zip(rs,zip(*jac))))/rs[i])
        image.append(absmax(dot(row,val))/rs[i]+norm[-1])
    assert max(image)<1 and max(norm)<1
    ly,lw=setcoords(by,bw,axes,[v+hull(-r*q,r*q) for v,r,q in zip(x,rs,image)])
    assert all(ly[i].hi<ly[j].lo for i,j in rel)
    assert all(0<lw[j].lo<=lw[j].hi<SCALE for j in set(range(22))-{15,17,20})
    assert all(lw[j].lo==lw[j].hi==0 for j in (15,17,20))
    assert all(absmax(ly[j]-ly[i])<8 for i,j in ((15,16),(15,18),(17,18),(18,7)))
    residual,_,_=fields(ly,lw,box(source),c,free,axes,list(map(box,goals)),box)
    assert len(residual)==30 and all(v.contains_zero() for v in residual)
    assert all(a.data()==b.data() for a,b in zip(coords(ly,lw,fixed),coords(by,bw,fixed)))
    lo,hi=map(F,ly[21].data()); ds=list(digits(lo-ERROR,hi+ERROR))
    labels=sorted({decode(d,r) for d in ds for r in range(REFERENCE-1,REFERENCE+2)})
    return dict(fixed=[name(a) for a in fixed],source=str(source),upper_image=upper(max(image)),
                upper_contraction=upper(max(norm)),codes=[min(ds),max(ds)],labels=labels,
                y=[a.data() for a in ly],w=[a.data() for a in lw])
