"""Existence bounds for coupled solutions and both mass diagnostics."""
from fractions import Fraction as F
from intervall import I,inverse_seed
from modell import FREE,POS,ZERO,DEVICE,WINDOW,evaluate

def put(y,w,z):
    Y=y.copy();W=w.copy()
    for i,v in zip(FREE,z[:len(FREE)],strict=True):Y[i]=v
    for i,v in zip(POS,z[len(FREE):],strict=True):W[i]=v
    return Y,W

def product(row,col):return sum((k*col[j] for j,k in row),I())

def certify(pair,side,rel,edges,seed):
    d=pair[side];y,w=([I(*v) for v in d[key]]+[I()] for key in ['clock_box','weight_box'])
    center=[I(v) for v in seed['clock']+seed['weight']]
    radii=[F(1,10**9)]*len(FREE)+[F(1,10**11 if side=='heavy' else 10**12)]*len(POS)
    outer=[v+I(-r,r) for v,r in zip(center,radii)]
    f,J,_=evaluate(*put(y,w,center),edges,I())
    pre=inverse_seed(J)
    _,large,_=evaluate(*put(y,w,outer),edges,I())
    eta=[];q=[]
    for i,row in enumerate(pre):
        norm=sum((int(i==j)-product(row,col)).mag()*r for j,(col,r) in enumerate(zip(zip(*large),radii)))/radii[i]
        q.append(norm);eta.append(norm+product(row,f).mag()/radii[i])
    assert max(eta)<1 and max(q)<1
    Y,W=put(y,w,[v+I(-r*b,r*b) for v,r,b in zip(center,radii,eta)])
    resid,_,G=evaluate(Y,W,edges,I())
    assert len(resid)==26 and all(v.l<=0<=v.h for v in resid)
    assert all(Y[i].h<Y[j].l for i,j in rel)
    assert all(W[j].l>0 and W[j].h<1 for j in range(23) if j not in ZERO)
    assert all(W[j].l==W[j].h==0 for j in ZERO)
    assert all((Y[j]-Y[i]).mag()<8 for i,j in DEVICE+((15,18),))
    duration=Y[7]-Y[3];x=[(v-Y[3])/duration for v in Y]
    inside=[j for j,v in enumerate(x) if WINDOW[0]<=v.l<=v.h<=WINDOW[1]]
    assert inside==[j for j,v in enumerate(x) if v.h>=WINDOW[0] and v.l<=WINDOW[1]]
    assert inside==[17,20,22]
    mass_q=-4*sum(G[:4],I())/F(pair['reference_Q'])
    mass_b=4*sum((W[j] for j in POS),I())/duration/F(pair['reference_B'])
    nominal=F(pair['nominal_'+side])
    assert min(mass_q.l,mass_b.l)>nominal*F(102,100)
    lower_positive=min((max(WINDOW[0]-v.h,v.l-WINDOW[1],F(0)),j) for j,v in enumerate(x) if j not in ZERO)
    return dict(y=[v.data() for v in Y],w=[v.data() for v in W],x=[v.data() for v in x],
                image_norm_upper=str(F(-(-max(eta)*10**9//1),10**9)),
                contraction_upper=str(F(-(-max(q)*10**9//1),10**9)),
                min_order_gap=str(min(Y[j].l-Y[i].h for i,j in rel)),min_interior_weight=str(min(W[i].l for i in POS)),
                window=inside,positive_in_window=[],contacts=[],mass_q=mass_q.data(),mass_b=mass_b.data(),
                nearest_positive=[lower_positive[1],str(lower_positive[0])])
