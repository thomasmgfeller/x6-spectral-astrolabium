"""Krawczyk/contractive enclosures of prepared N22 states at fixed late fields."""
from decimal import Decimal
from fractions import Fraction as F
from algebra import mid,inv
from feldroehre import POS,absmax
from impulsfelder import fields
from impulsabgleich import setcoords,coords
from paarstudie import upper
from quelle import box,hull,SCALE
from randversuch import dot
from anfangsbasis import QSTAR,PAST,LATE


def solve(y_ref,w_ref,free,order,coeff,spec,b_star):
    mode=spec['mode']
    axes=[('y',i) for i in free]+[('w',i) for i in POS]
    base_y=y_ref.copy()
    base_w=w_ref.copy()
    if mode=='QB':
        axes += [('y',0),('y',1)]
        # The third early clock is an explicitly prescribed Dirichlet value.
        base_y[2]=F(spec['y'][2])
        y0,w0=([F(v) for v in spec[key]] for key in ('y','w'))
        qt=QSTAR*F(spec['q_ratio'])
        bt=b_star*F(spec['b_ratio'])
    else:
        base_y[spec['index']]+=F(spec['shift'])
        y0,w0=base_y,base_w
    duration=y_ref[7]-y_ref[3]
    def make(convert,cast):
        edges=[(i,j,convert(F(k))) for (i,j),k in sorted(coeff.items())]
        dy=convert(duration)
        goals=[convert(0)]*5
        def evaluate(y,w):
            vals,A,g=fields(y,w,convert(0),edges,free,axes,goals,cast)
            if mode=='QB':
                # The last five original rows are Y15 and the four early impulses.
                q=sum((-g[i] for i in PAST),convert(0))
                dq=[-sum(col,convert(0)) for col in zip(*A[-4:])]
                vals=vals[:-5]+[q-convert(qt),sum((w[j] for j in POS),convert(0))-convert(bt)*dy]
                A=A[:-5]+[dq,[convert(int(k=='w' and j in POS)) for k,j in axes]]
            else:
                vals,A=vals[:-5],A[:-5]
            return vals,A,g
        return evaluate
    decimal=make(mid,Decimal)
    ydec,wdec=list(map(mid,base_y)),list(map(mid,base_w))
    x=list(map(mid,coords(y0,w0,axes)))
    for _ in range(8):
        vals,A,_=decimal(*setcoords(ydec,wdec,axes,x))
        x=[v-sum(k*b for k,b in zip(row,vals)) for v,row in zip(x,inv(A))]
    center=[box(F(v).limit_denominator(10**21)) for v in x]
    Y,W=list(map(box,base_y)),list(map(box,base_w))
    evaluate=make(box,box)
    vals,A,_=evaluate(*setcoords(Y,W,axes,center))
    C=[[(j,box(k)) for j,k in enumerate(row) if k] for row in inv(A)]
    radii=[F(1,10**11 if k=='y' else 10**12) for k,j in axes]
    outer=[v+hull(-r,r) for v,r in zip(center,radii)]
    _,Aj,_=evaluate(*setcoords(Y,W,axes,outer))
    eta=[];contraction=[]
    for i,row in enumerate(C):
        q=sum(absmax(int(i==j)-dot(row,col))*r for j,(r,col) in enumerate(zip(radii,zip(*Aj))))/radii[i]
        contraction.append(q)
        eta.append(q+absmax(dot(row,vals))/radii[i])
    assert max(eta)<1 and max(contraction)<1,(spec['name'],float(max(eta)))
    inner=[v+hull(-r*e,r*e) for v,r,e in zip(center,radii,eta)]
    y,w=setcoords(Y,W,axes,inner)
    vals,_,g=evaluate(y,w)
    assert len(vals)==len(axes) and all(v.contains_zero() for v in vals)
    assert all(y[i].hi<y[j].lo for i,j in order)
    zero={15,17,20}
    assert all(w[j].lo==w[j].hi==0 for j in zero)
    assert all(0<w[j].lo<=w[j].hi<SCALE for j in set(range(22))-zero)
    assert all(absmax(y[j]-y[i])<8 for i,j in ((15,16),(15,18),(17,18),(18,7)))
    assert all(y[j].data()==Y[j].data() and w[j].data()==W[j].data() for j in LATE)
    assert all(w[j].data()==W[j].data() for j in PAST)
    q=-sum((g[i] for i in PAST),box(0))
    crossed=-sum((box(F(k))*w[j]*(y[j]-y[i]) for (i,j),k in coeff.items()
                  if i in PAST and j not in PAST),box(0))
    assert (q-crossed).contains_zero()
    # B is evaluated from density regardless of any target used to select the state.
    B=sum((w[j] for j in POS),box(0))*box(1/duration)
    if mode=='QB':
        assert (q-box(qt)).contains_zero() and (B-box(bt)).contains_zero()
    xnorm=[(v-box(y_ref[3]))*box(1/duration) for v in y]
    half=F(1,2);h=F(1,32)
    data=[tuple(map(F,a.data())) for a in xnorm]
    inside=[j for j,(l,u) in enumerate(data) if half-h<=l<=u<=half+h]
    assert inside==[j for j,(l,u) in enumerate(data) if l<=half+h and u>=half-h]
    positive=[j for j in inside if j not in zero];empty=sorted(set(inside)&zero)
    from itertools import combinations
    width=max((n for n in range(1,len(positive)+1) if any(all((a,b) not in order and (b,a) not in order for a,b in combinations(group,2)) for group in combinations(positive,n))),default=0)
    pairs=[]
    for a in positive:
        for b in empty:
            if (a,b) in order or (b,a) in order:continue
            before=sorted(i for i in range(22) if i not in zero and (i,a) in order and (i,b) in order)
            after=sorted(i for i in range(22) if i not in zero and (a,i) in order and (b,i) in order)
            if before and after:pairs.append(dict(pair=[a,b],past=before,future=after))
    return dict(name=spec['name'],mode=mode,Q=q.data(),B=B.data(),cut=crossed.data(),
                target_Q=str(qt) if mode=='QB' else None,target_B=str(bt) if mode=='QB' else None,
                y=[v.data() for v in y],w=[v.data() for v in w],normalized=[z.data() for z in xnorm],
                positive=positive,empty=empty,antichain=width,contacts=pairs,dimension=len(axes),
                contraction_upper=upper(max(contraction)),image_upper=upper(max(eta)))
