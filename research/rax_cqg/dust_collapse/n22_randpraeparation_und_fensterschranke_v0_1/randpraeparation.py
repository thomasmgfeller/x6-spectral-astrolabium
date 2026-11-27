"""Outward enclosures for jointly prepared collar clocks and weights."""
from fractions import Fraction as F
from itertools import product

LABELS = (0,1,2,3,7,8,9,10)
S = 10**9


def response(y,w,alpha):
    from quelle import box
    from gemischt import COEFF,CLOCK,WEIGHT,FUT,PAST
    from zustand import gradients,check
    from algebra import solve_box

    t,h=y[18],y[17]
    gap=t-h
    assert gap.lo>0
    other=sum((c*(t-y[i]) for (i,j),c in COEFF.items() if j==18 and i!=17),box(0))
    root=(gap*gap-2*alpha*other).sqrt()
    slope={i:box(0) for i in y}
    slope[18]=box(1)
    slope[17]=1+2*other/(gap+root)
    moved=y.copy()
    for j in (17,18):
        moved[j]=y[j]+alpha*slope[j]
    assert (moved[17]-(t+alpha-root)).contains_zero()
    # For fixed weights, old gradient minus new gradient is alpha times rhs.
    rhs={i:box(0) for i in y}
    for (i,j),c in COEFF.items():
        term=c*w[j]*(slope[i]-slope[j])
        rhs[i]+=term
        rhs[j]-=term
    coords=[('w',j) for j in WEIGHT+FUT]+[('M',j) for j in FUT]
    matrix=[]
    for i in CLOCK+PAST:
        incoming=sum((c*(moved[i]-moved[j]) for (j,k),c in COEFF.items() if k==i),box(0))
        row=[]
        for kind,j in coords:
            c=COEFF.get((i,j),0)
            if kind=='M':
                value=box(c)
            elif j in FUT:
                value=-c*moved[i]
            else:
                value=c*(moved[j]-moved[i])-(incoming if j==i else 0)
            row.append(value)
        matrix.append(row)
    unit=lambda key:[box(int(z==key)) for z in coords]
    matrix.extend([unit(('w',16)),[a-y[7]*b for a,b in zip(unit(('M',7)),unit(('w',7)))]])
    unit_response=solve_box(matrix,[rhs[i] for i in CLOCK+PAST]+[box(0),box(0)])
    dw=dict(zip(coords,(alpha*v for v in unit_response)))
    weights=w.copy()
    for j in WEIGHT+FUT:
        weights[j]=w[j]+dw['w',j]
    for j in FUT:
        # Equivalent to (w[j]*y[j]+dM[j])/(w[j]+dw[j]), retaining the shared clock.
        moved[j]=y[j]+(dw['M',j]-y[j]*dw['w',j])/weights[j]
    assert (moved[7]-y[7]).contains_zero() and (weights[16]-w[16]).contains_zero()
    moved[7],weights[16]=y[7],w[16]
    check(moved,weights)
    old,_=gradients(y,w); updated,_=gradients(moved,weights)
    assert all((old[i]-updated[i]).contains_zero() for i in PAST)
    return moved,weights


def signed_rhs_audit():
    # An independent exact evaluation including a zero shift and both signs.
    from gemischt import COEFF
    labels=range(19)
    y=[F((i+1)**2,30) for i in labels]
    w=[F(i+2,31) for i in labels]
    sigma=[F(0) for i in labels]
    sigma[17],sigma[18]=F(4,7),F(1)
    def gradient(i,z):
        return sum(c*w[b]*(z[b]-z[a])*(int(i==a)-int(i==b)) for (a,b),c in COEFF.items())
    for alpha in (F(0),F(-7,11),F(3,5)):
        shifted=[v+alpha*d for v,d in zip(y,sigma)]
        for i in labels:
            expected=sum(c*w[b]*(sigma[a]-sigma[b])*(int(i==a)-int(i==b))
                         for (a,b),c in COEFF.items())
            assert gradient(i,y)-gradient(i,shifted)==alpha*expected
    return len(y)*3


def tick_row(state,j):
    vals=[F(s)*S for k in ('y','w') for s in state[k][j].data()]
    return [v//1 if i%2==0 else -(-v//1) for i,v in enumerate(vals)]


def hull_rows(cells):
    return {j:[(min if col%2==0 else max)(cs[j][col] for cs in cells) for col in range(4)]
            for j in LABELS}


def compute(previous,early,partitions):
    from modell import setup
    from empfangsbit import K0,STEP,V
    from staubgeraet import solve,verify
    from referenzwechsel import displaced
    from quelle import box,hull
    from driftfamilie import LABELS as sources,LIMIT
    y,w=setup(previous,early)
    vel=(hull(-112*V,112*V),)*3
    q=(hull(-1,1),)*3
    all_cells=[]
    endpoints=[-LIMIT+2*LIMIT*j/partitions for j in range(partitions+1)]
    assert endpoints[0]==-LIMIT and endpoints[-1]==LIMIT and len(set(endpoints))==partitions+1
    def collar(yy,ww,J,vs):
        state=solve(yy,ww,J,vs,K0,box(-K0),'positive_bridge')
        verify(state,J,vs,K0,box(-K0),'positive_bridge',q)
        return {j:tick_row(state,j) for j in LABELS}
    for left,right in zip(endpoints,endpoints[1:]):
        yy,ww=response(y,w,hull(6*STEP+left,6*STEP+right))
        for source in sources:
            all_cells.append(dict(drift=[str(left),str(right)],source=str(source),collar=collar(yy,ww,source,vel)))
    checks=0
    # Exact prepared point enclosures via the original unmodified drift solver.
    # At a shared endpoint the point enclosure must fit both adjacent cells.
    probe_drifts=sorted({-LIMIT,F(0),LIMIT,-6*STEP})
    for drift in probe_drifts:
        yy,ww=displaced(y,w,box(6*STEP+drift))
        for J in sources:
            groups=[r for r in all_cells if r['source']==str(J) and F(r['drift'][0])<=drift<=F(r['drift'][1])]
            assert groups
            for signs in [(0,0,0),*product((-1,1),repeat=3)]:
                ref=collar(yy,ww,J,tuple(box(112*V*sign) for sign in signs))
                for group in groups:
                    for j in LABELS:
                        a=group['collar'][j];b=ref[j]
                        for k in (0,2):
                            assert a[k]<=b[k]<=b[k+1]<=a[k+1]
                            checks+=1
    return dict(cells=all_cells,collar=hull_rows([r['collar'] for r in all_cells]),
                partitions=partitions,point_checks=checks,rhs_checks=signed_rhs_audit())
