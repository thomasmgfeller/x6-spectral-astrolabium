"""Independent combinatorial construction and exact finite differences."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from random import Random
import subprocess
from eingaben import MATERIAL, DEVICE, EARLY, LATE, SCALE


def combinatorics(d):
    old=set(d['order'])
    nodes=tuple(range(19))
    past=[sum(1<<i for i in nodes if (i,j) in old) for j in nodes]
    # An ideal is any bit-vector that contains all predecessors of each member.
    ideals=[0]
    for mask in range(1,1<<19):
        hi=mask.bit_length()-1
        # Labels need not be topological. Check each set without such an assumption.
        if not past[hi]&~mask and all(not(past[i]&~mask) for i in nodes[:hi] if (mask>>i)&1):
            ideals.append(mask)
    full=(1<<19)-1
    single=[]
    for p in ideals:
        for middle in ideals:
            if p&~middle:continue
            f=full^middle
            if p and f and all((p & ~past[i])==0 for i in nodes if f & (1<<i)):
                single.append((p,f))
    kept=set();reasons=Counter()
    for p,f in single:
        for q,g in single:
            if p&g or q&f or not(p&q&MATERIAL and f&g&MATERIAL):continue
            if p&LATE or q&LATE or f&EARLY or g&EARLY:why='collar_time'
            elif not p&DEVICE:why='native_density'
            elif not g&~LATE:why='collar_vacuum'
            else:
                why='field_system';kept.add((p,f,q,g))
            reasons[why]+=1
    assert set(d['rows'])==kept
    assert sum(reasons.values())==d['old']['common_anchors_total']
    return dict(reasons)


def fraction_checks(d,indices):
    old=set(d['order']);nodes=range(21)
    k=F(1,79);mu=-k;J=F(1,43);vel=[F(-2,11),F(3,13),F(5,17)]
    h=F(1,2048)
    # Deliberately distinct off-shell fields and nonzero device impulses.
    y=[F(5*j-31,37) for j in nodes]
    w=[F(j+3,31) if j not in (15,17,20) else F(0) for j in nodes]
    probes=[]
    segments=[]
    for track,v in zip(d['routes'],vel):
        for j,inertia,edge in track:
            gap=y[edge[1]]-y[edge[0]] if edge else 0
            segments.append((j,inertia,edge,gap+v/w[inertia]))
            if edge:
                a,b=edge
                probes.append((a,b,j,v))
    dy=[F(0) for _ in nodes]
    dw=[F(0) for _ in nodes];dw[16]=-J
    for j,inertia,edge,inc in segments:
        gap=y[edge[1]]-y[edge[0]] if edge else 0
        dw[inertia]+=k*(inc-gap)**2
        if edge:dw[j]+=mu*gap**2
    for a,b,j,v in probes:
        val=mu*w[j]*(y[b]-y[a])-k*v
        dy[a]+=val;dy[b]-=val
    checked=0
    for idx in indices:
        row=d['rows'][idx]
        rel=set(old)
        for j,p,f in ((19,*row[:2]),(20,*row[2:])):
            rel.update((i,j) for i in range(19) if p & 1<<i)
            rel.update((j,i) for i in range(19) if f & 1<<i)
        assert all((i,z) in rel for i,j in rel for q,z in rel if j==q)
        counts={(i,j):sum((i,t) in rel and (t,j) in rel for t in nodes) for i,j in rel}
        edges=[(i,j,(1,-9,16,-8)[n]) for (i,j),n in counts.items() if n<4]
        def action(Y,W):
            v=19*sum(W)-J*W[16]
            for i,j,c in edges:v+=c*W[j]*(Y[j]-Y[i])**2
            for j,inertia,probe,inc in segments:
                gap=Y[probe[1]]-Y[probe[0]] if probe else 0
                v+=k*W[inertia]*(inc-gap)**2
                if probe:v+=mu*W[j]*gap**2
            return v
        for j in (4,5,6,11,12,13,14,15,16,17,18,19,20):
            lo=y[:];hi=y[:];lo[j]-=h;hi[j]+=h
            G=sum(c*w[z]*(y[z]-y[j]) for i,z,c in edges if i==j)
            G-=w[j]*sum(c*(y[j]-y[i]) for i,z,c in edges if z==j)
            assert -(action(hi,w)-action(lo,w))/(4*h)==G+dy[j]
            checked+=1
            if j in (15,17,20):continue
            lo=w[:];hi=w[:];lo[j]-=h;hi[j]+=h
            D=19+sum(c*(y[j]-y[i])**2 for i,z,c in edges if z==j)
            assert (action(y,hi)-action(y,lo))/(2*h)==D+dw[j]
            checked+=1
    return {'orders':len(indices),'exact_field_derivatives':checked}


def kernel_controls(d,binary):
    f=['P',str(len(d['order']))]+['%d %d'%tuple(e) for e in d['order']]
    f+=[' '.join(map(str,d['reference'][j])) for j in range(19)]
    rng=Random(1729)
    tests=[(0,0,0,0),(-1,1,-1,1),(0,1,1,SCALE),(5,30,1,1),(-15*SCALE,12*SCALE,1,1)]
    for _ in range(300):
        a,b=sorted(rng.randrange(-20*SCALE,20*SCALE) for _ in range(2))
        c,e=sorted(rng.randrange(-20*SCALE,20*SCALE) for _ in range(2))
        tests.append((a,b,c,e))
    f+=['I '+' '.join(map(str,r)) for r in tests]
    out=subprocess.run([binary],input='\n'.join(f)+'\n',text=True,capture_output=True,check=True).stdout.splitlines()
    assert out[0]=='parent accepted' and len(out)==1+len(tests)
    for line,t in zip(out[1:],tests):
        a,b,c,e=[F(x,SCALE) for x in t]
        vals=[F(int(x),SCALE) for x in line.split()]
        def encloses(j,items):assert all(vals[2*j]<=s<=vals[2*j+1] for s in items)
        encloses(0,[x*y for x,y in product((a,b),(c,e))])
        squares=[a*a,b*b]+([F(0)] if a<=0<=b else [])
        encloses(1,squares); encloses(2,[a/-9,b/-9]);encloses(3,[abs(a),abs(b)]+([F(0)] if a<=0<=b else []))
        if c<=0<=e:encloses(4,[-10,10])
        else:
            corners=[x/y for x,y in product((a,b),(c,e))]
            lo=max(-10,min(corners));hi=min(10,max(corners))
            if lo<=hi:encloses(4,[lo,hi])
            else:
                assert vals[8]>vals[9] or vals[9]-vals[8]<=F(1,SCALE)
    return {'stationary_N19_sweep_orders':2,'rational_kernel_boxes':len(tests)}


def density_only(d):
    """Independent one-equation certificate for undisturbed ancestors of event 19.

    For device-null ancestors the only bound used is positive causal separation.
    Products below use Fraction endpoints rather than the C++ interval engine.
    """
    old=set(d['order'])
    groups=Counter(row[0] for row in d['rows'])
    clock={i:tuple(F(v,SCALE) for v in bounds[:2]) for i,bounds in {**d['collar'],**d['native']}.items()}
    low,high=[F(v,SCALE) for v in d['window']]
    result=[];by_sign=Counter();single=0
    for mask,count in sorted(groups.items()):
        past=[i for i in range(19) if mask & (1<<i)]
        if 16 in past or 18 in past:continue
        coefficients={}
        for i in past:
            length=sum((i,j) in old for j in past)
            if length<4:coefficients[i]=(1,-9,16,-8)[length]
        minimum=maximum=None
        for part in range(16):
            a=low+part*(high-low)/16;b=a+(high-low)/16
            left=right=F(19)
            for i,c in coefficients.items():
                if i in (15,17):
                    oldest=max(clock[k][0] for k in past if (k,i) in old)
                    lo,hi=F(0),max(F(0),b-oldest)**2
                else:
                    first,last=clock[i]
                    lo=max(F(0),a-last)**2;hi=max(F(0),b-first)**2
                left+=min(c*lo,c*hi);right+=max(c*lo,c*hi)
            minimum=left if minimum is None else min(minimum,left)
            maximum=right if maximum is None else max(maximum,right)
        sign='negative' if maximum<0 else 'positive' if minimum>0 else 'open'
        by_sign[sign]+=count
        result.append({'past':past,'orders':count,'D19':[str(minimum),str(maximum)],'sign':sign})
        if past==[0,17]:
            assert count==1205 and 19-8*(low+5)**2<F(-18287,100)
            single=count
    assert single
    return {'counts':dict(by_sign),'checked_pasts':len(result),'certificates':result,'two_ancestor_example':single}
