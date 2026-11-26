"""Enumerate every induced two-event interval refinement and test its field equations."""
from fractions import Fraction as F
from itertools import combinations, product

LAYERS = (1,-9,16,-8)


def powerset(nodes):
    items=sorted(nodes)
    for k in range(len(items)+1):
        for group in combinations(items,k):
            yield set(group)


def closure(edges):
    rel=set(edges)
    while True:
        nxt=rel | {(i,k) for i,j in rel for a,k in rel if a==j}
        if nxt==rel:
            return rel
        rel=nxt


def orders(old):
    nodes={i for edge in old for i in edge}
    before=lambda i:{p for p,q in old if q==i}
    after=lambda i:{q for p,q in old if p==i}
    mandatory_past=before(16)|{16}
    mandatory_future=after(18)|{18}
    records=[]
    for extra_p in powerset(before(18)-mandatory_past):
        past=mandatory_past|extra_p
        if not all(i in past for i,j in old if j in past):
            continue
        for extra_f in powerset(after(16)-mandatory_future):
            future=mandatory_future|extra_f
            if all(j in future for i,j in old if i in future):
                records.append((past,future))
    out={}
    for (p1,f1),(p2,f2) in product(records,repeat=2):
        links={(16,19),(19,18),(16,20),(20,18)}
        for n,p,f in [(19,p1,f1),(20,p2,f2)]:
            links.update((i,n) for i in p)
            links.update((n,i) for i in f)
        rel=closure(old|links)
        if {(i,j) for i,j in rel if i in nodes and j in nodes}!=old:
            continue
        if (19,20) in rel or (20,19) in rel or any(i==j for i,j in rel):
            continue
        key=(17 in p1,17 in p2)
        assert key not in out
        out[key]=rel
    assert set(out)==set(product([False,True],repeat=2))
    # Second construction uses only the four generating edges and the optional ones.
    for (a,b),rel in out.items():
        links={(16,19),(19,18),(16,20),(20,18)}
        if a: links.add((17,19))
        if b: links.add((17,20))
        assert closure(old|links)==rel
    return out


def coefficients(rel):
    nodes={i for edge in rel for i in edge}
    result={}
    for i,j in rel:
        n=sum((i,k) in rel and (k,j) in rel for k in nodes)
        if n<len(LAYERS):
            result[i,j]=LAYERS[n]
    return result


def audit_action(rel, routes, a, b):
    """Check six reduced gradients against exact finite differences of the full action."""
    c=coefficients(rel)
    n=range(21)
    # Independently construct coefficients from matrix multiplication of the order matrix.
    intervals={(i,j):sum(int((i,k) in rel)*int((k,j) in rel) for k in n) for i,j in rel}
    assert c=={e:LAYERS[k] for e,k in intervals.items() if k<len(LAYERS)}
    inc=lambda j:{i:k for (i,m),k in c.items() if m==j}
    out=lambda i:{j:k for (m,j),k in c.items() if m==i}
    assert out(20)==out(19)=={18:1,7:-9,8:16,9:-8}
    assert out(15)=={16:1,18:-8,19:-9,20:-9}
    assert inc(16)=={0:-8,1:16,2:-9,15:1}
    assert inc(19)==({1:-8,2:16,15:-9,16:1}|({17:1} if a else {}))
    assert inc(18)=={15:-8,16:16,17:(1,-9,16)[a+b],19:1,20:1}
    def action(Y,W,traces,k,mu,J):
        total=19*sum(W)+sum(h*W[j]*(Y[j]-Y[i])**2 for (i,j),h in c.items())-J*W[16]
        for track,hist in zip(routes,traces,strict=True):
            last=0
            for j,inertia,probe in track:
                delta=Y[probe[1]]-Y[probe[0]] if probe else 0
                total+=k*W[inertia]*(hist[j]-hist[last]-delta)**2
                if probe: total+=mu*W[j]*delta**2
                last=j
        return total
    ys={0:-5,1:-4,2:-3,3:F(-11,6),7:2,8:3,9:4,10:5,
        15:F(-5,2),16:F(1,17),17:F(-9,2),18:F(1,9),19:F(1,11),20:F(1,10)}
    for j in n:
        if j not in ys: ys[j]=F(sum(k==j for i,k in rel),11)-1
    y=[F(ys[j]) for j in n]
    w=[F(j+1,40) if j not in (15,17,20) else F(0) for j in n]
    s,t,h,r,v,z=(y[j] for j in (16,15,17,18,19,20))
    k=F(1,79);mu=-k;J=F(1,43)
    velocities=(F(2,13),F(-3,17),F(5,19))
    flow=k*velocities[0];load=k*sum(x*x for x in velocities)
    traces=[]
    for track,impulse in zip(routes,velocities,strict=True):
        hist={0:F(0)}
        last=0
        for j,inertia,probe in track:
            delta=y[probe[1]]-y[probe[0]] if probe else 0
            hist[j]=hist[last]+delta+impulse/w[inertia]
            last=j
        traces.append(hist)
    bare=lambda j:19+sum(q*(y[j]-y[i])**2 for i,q in inc(j).items())
    collar=lambda clock:sum(c[20,j]*w[j]*(y[j]-clock) for j in (7,8,9))
    GS=(1+mu)*w[16]*(s-t)-8*w[18]*(r-t)-9*w[19]*(v-t)-flow
    GN=w[18]*(r-v)+collar(v)-w[19]*sum(q*(v-y[i]) for i,q in inc(19).items())
    exact={('y',15):GS, ('y',20):w[18]*(r-z)+collar(z), ('y',19):GN,
           ('w',19):35+32*v+8*v*v-9*(v-t)**2+(v-s)**2+a*(v-h)**2,
           ('w',16):-(s*s+6*s+6)+(1+mu)*(s-t)**2+load/w[16]**2-J,
           ('w',18):19-8*(r-t)**2+(16+mu)*(r-s)**2+((1,-9,16)[a+b]+mu)*(r-h)**2+(r-v)**2+(r-z)**2+load/w[18]**2}
    assert exact['w',19]==bare(19)
    step=F(1,100000)
    for (kind,j),expected in exact.items():
        yp,ym,wp,wm=y.copy(),y.copy(),w.copy(),w.copy()
        plus,minus=(yp,ym) if kind=='y' else (wp,wm)
        plus[j]+=step;minus[j]-=step
        diff=(action(yp,wp,traces,k,mu,J)-action(ym,wm,traces,k,mu,J))/(2*step)
        assert diff == (-2*expected if kind=='y' else expected)
    return len(exact)
