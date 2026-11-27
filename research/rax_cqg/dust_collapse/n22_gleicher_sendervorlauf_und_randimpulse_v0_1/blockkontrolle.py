"""Exact edge-dependency and interval isolation of the sender/receiver subsystem."""
from fractions import Fraction as F
from quelle import box,hull
from algebra import inv
from feldroehre import POS,absmax
from randversuch import evaluate,dot

BLOCK=tuple(range(15,22))
DENSITY=(16,18,19,21)

def isolate(state,source,coeff,free):
    cy,cw,x,axes,ly,lw=state
    assert tuple(free)==axes
    incident={i for (i,j),k in coeff.items() if k and j in BLOCK}
    incident.update(j for (i,j),k in coeff.items() if k and i in BLOCK)
    boundary=sorted(incident-set(BLOCK))
    assert boundary==[0,1,2,7,8,9,10]
    assert tuple(j for j in POS if j in BLOCK)==DENSITY
    c=[(i,j,box(k)) for (i,j),k in coeff.items() if i in BLOCK or j in BLOCK]
    pos_cols=[POS.index(j)+len(BLOCK) for j in DENSITY]
    col_ids=list(range(len(BLOCK)))+pos_cols
    row_ids=[POS.index(j) for j in DENSITY]+list(range(len(POS),len(POS)+len(BLOCK)))
    def reduced(y,w):
        val,A,_=evaluate(y,w,box(source),c,BLOCK,BLOCK,box)
        return [val[i] for i in row_ids],[[A[i][j] for j in col_ids] for i in row_ids]
    v,jac=reduced(cy,cw)
    C=[[(i,box(e)) for i,e in enumerate(row) if e] for row in inv(jac)]
    radii=[F(1,10**7)]*len(BLOCK)+[F(1,10**8)]*len(DENSITY)
    yy,ww=cy.copy(),cw.copy()
    for k,j in enumerate(BLOCK):yy[j]+=hull(-radii[k],radii[k])
    for k,j in enumerate(DENSITY):
        radius=radii[k+len(BLOCK)]
        ww[j]+=hull(-radius,radius)
    assert all(yy[j].lo<=ly[j].lo<=ly[j].hi<=yy[j].hi for j in BLOCK)
    assert all(ww[j].lo<=lw[j].lo<=lw[j].hi<=ww[j].hi for j in DENSITY)
    _,wide=reduced(yy,ww)
    betas=[];norms=[]
    for i,row in enumerate(C):
        betas.append(absmax(dot(row,v))/radii[i])
        norms.append(sum(absmax(int(i==j)-dot(row,col))*r for j,(r,col) in enumerate(zip(radii,zip(*wide))))/radii[i])
    eta=max(a+b for a,b in zip(betas,norms))
    assert max(norms)<1 and eta<1
    err=radii[0]*(betas[0]+norms[0])
    clock=cy[15]+hull(-err,err)
    return dict(read_boundary=boundary,clocks=list(BLOCK),densities=list(DENSITY),clock15=clock.data(),
                upper_image=str(F(-(-eta*10**12//1),10**12)))

def check_jac(state,source,coeff,free):
    # Independently form residuals by summing each variable's contributions to
    # the action, then take an exact symmetric difference of quadratic polynomials.
    cy,cw,x,axes,_,_=state
    def center(b):return sum(map(F,b.data()))/2
    y=list(map(center,cy));w=list(map(center,cw))
    c=[(i,j,k) for (i,j),k in coeff.items()]
    _,A,_=evaluate(y,w,source,c,free,axes,F)
    def reference(y,w):
        density=[19-source*(j==16)+sum(k*(y[b]-y[a])**2 for a,b,k in c if b==j) for j in POS]
        clock=[sum(k*w[b]*(y[b]-y[a])*(int(a==j)-int(b==j)) for a,b,k in c if a==j or b==j) for j in free]
        return density+clock
    h=F(1,1000)
    for ix,(isclock,j) in enumerate([(True,j) for j in axes]+[(False,j) for j in POS]):
        yl,yh=y.copy(),y.copy();wl,wh=w.copy(),w.copy()
        l,r=(yl,yh) if isclock else (wl,wh)
        l[j]-=h;r[j]+=h
        v0,v1=reference(yl,wl),reference(yh,wh)
        assert all((b-a)/(2*h)==row[ix] for a,b,row in zip(v0,v1,A))
    return len(A)*len(A[0])
