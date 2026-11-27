"""Certify a full-rank midpoint secant matrix on an explicit rational box."""
from fractions import Fraction as F
from math import lcm
from decimal import Decimal as D
from algebra import inv
from feldroehre import POS
from impulsfelder import fields
from zukunftsbasis import FUTURE,name
from paarstudie import upper

ALL=[(k,j) for k in ('y','w') for j in range(22)]
UNIT=10**28

def domain(witnesses,free):
    active={('y',j) for j in free}|{('w',j) for j in POS}|set(FUTURE)
    out={}
    for t,j in ALL:
        axis=t,j
        lo=min(F(s[t][j][0]) for s in witnesses)
        hi=max(F(s[t][j][1]) for s in witnesses)
        if axis in active:
            pad=max((hi-lo)/50,F(1,10**9 if t=='y' else 10**11))
            lo-=pad;hi+=pad
        # Represent every endpoint on the same fixed grid, outward.
        out[axis]=(int(lo*UNIT//1),int(-(-hi*UNIT//1)))
    return out

def augmented(y,w,c,free,axes,cast,extra=()):
    _,A,_=fields(y,w,cast(0),c,free,list(axes)+list(extra),[cast(0)]*5,cast)
    for i,row in enumerate(A):row.insert(len(axes),cast(-int(i==POS.index(16))))
    assert len(A)==30 and len(A[0])==30+len(extra)
    return A

def majorant(A,changes,rads):
    # A and every derivative matrix are exact; C is an integer approximation
    # of the inverse on scale UNIT. Summation precedes interval bounding.
    n=len(A)
    C=[[int((a*D(UNIT)).to_integral_value()) for a in row] for row in inv([r[:n] for r in A])]
    divisor=1
    for row in A:
        for a in row:divisor=lcm(divisor,a.denominator)
    B=[[int(a*divisor) for a in row] for row in A]
    rem=[[abs(int(i==j)*UNIT*divisor-sum(u*v for u,v in zip(row,col))) for j,col in enumerate(zip(*B))] for i,row in enumerate(C)]
    M=[[F(x,UNIT*divisor) for x in row] for row in rem]
    for axis,cols in changes.items():
        if rads[axis]==0:continue
        shift=F(rads[axis],2*UNIT)
        for j,(den,terms) in cols.items():
            fac=shift/(UNIT*den)
            for i,crow in enumerate(C):
                M[i][j]+=abs(sum(crow[k]*num for k,num in terms))*fac
    return M

def norm_proof(M):
    # The rounded integer vector is a candidate positive diagonal rescaling.
    # The final weighted infinity norm uses exact fractions.
    n=len(M);scale=10**20
    A=[[int(-(-a*scale//1)) for a in row] for row in M]
    weights=[scale]*n
    for _ in range(65):
        v=[sum(a*b for a,b in zip(row,weights)) for row in A]
        rate=max(F(t,scale*u) for t,u in zip(v,weights))
        if rate<F(9,10):
            return rate,weights
        # Applying I + M avoids cyclic weight oscillations.
        added=[t+scale*u for t,u in zip(v,weights)]
        top=max(added)
        weights=[max(1,(t*scale+top-1)//top) for t in added]
    if rate<1:return rate,weights
    return None,None

def solve_triple(domain_,free,coeff,fixed,clock_bound=False):
    axes=[('y',i) for i in free]+[('w',i) for i in POS]+[a for a in FUTURE if a not in fixed]
    c=[(i,j,F(k)) for (i,j),k in sorted(coeff.items())]
    mid={a:F(l+h,2*UNIT) for a,(l,h) in domain_.items()}
    rads={a:h-l for a,(l,h) in domain_.items()}
    y,w=([mid[k,j] for j in range(22)] for k in ('y','w'))
    extra=fixed if clock_bound else ()
    A=augmented(y,w,c,free,axes,F,extra)
    # The full Jacobian is affine. Compute its exact directional coefficients.
    changes={}
    for axis,r in rads.items():
        if r==0:continue
        k,j=axis
        yy,ww=y.copy(),w.copy()
        (yy if k=='y' else ww)[j]+=1
        variation=augmented(yy,ww,c,free,axes,F,extra)
        cols={}
        for col in range(len(A[0])):
            entries=[(i,variation[i][col]-A[i][col]) for i in range(30) if variation[i][col]!=A[i][col]]
            if entries:
                den=lcm(*(a.denominator for _,a in entries))
                cols[col]=den,[(i,int(a*den)) for i,a in entries]
        changes[axis]=cols
    combined=majorant(A,changes,rads)
    M=[row[:30] for row in combined]
    q,weights=norm_proof(M)
    result=dict(fixed=[name(a) for a in fixed],certified=q is not None,
                upper_norm=upper(q) if q is not None else None,weights=weights)
    if clock_bound and q is not None:
        assert tuple(fixed)==FUTURE[:3]
        b=[sum(row[30:]) for row in combined]
        # If |delta clocks| <= 1, a positive rational supersolution bounds
        # every component of the unknown vector, including its last entry J.
        A0=[[int(i==j)-a for j,a in enumerate(row)] for i,row in enumerate(M)]
        approx=[F(sum((c*(D(t.numerator)/D(t.denominator)) for c,t in zip(row,b)),D(0))).limit_denominator(10**18)
                for row in inv(A0)]
        gap=max([F(0)]+[(v+sum(a*t for a,t in zip(row,approx))-u)/wt
                        for v,row,u,wt in zip(b,M,approx,weights)])
        shift=gap/(1-q)+F(1,10**30)
        guard=[v+shift*wt for v,wt in zip(approx,weights)]
        assert all(v>=0 for v in guard)
        assert all(v+sum(a*t for a,t in zip(row,guard))<=u for v,row,u in zip(b,M,guard))
        bound=F(upper(guard[-1]))
        result['clock_bound']=dict(source_per_max_clock_gap=str(bound),
                                  minimum_adjacent_gap=str(F(1,10**6)/bound),
                                  supersolution=[str(t) for t in guard])
    return result

def audit_identity(row1,row2,coeff,free):
    # Independent scalar edge sums for the exact finite difference in all 30
    # equations and all field coordinates (not limited to shared coordinates).
    axes=ALL
    c=[(i,j,F(k)) for (i,j),k in coeff.items()]
    def state(row):
        return [[sum(map(F,ab))/2 for ab in row[k]] for k in ('y','w')]
    ya,wa=state(row1);yb,wb=state(row2)
    ja,jb=F(row1['source']),F(row2['source'])
    def f(y,w,J):
        density=[19-int(i==16)*J+sum(k*(y[b]-y[a])**2 for a,b,k in c if b==i) for i in POS]
        flow=[sum(k*w[b]*(y[b]-y[a])*(int(i==a)-int(i==b)) for a,b,k in c if i in (a,b)) for i in list(free)+list(range(4))]
        return density+flow[:len(free)]+[y[15]]+flow[len(free):]
    mid=lambda l,r:[(a+b)/2 for a,b in zip(l,r)]
    _,A,_=fields(mid(ya,yb),mid(wa,wb),(ja+jb)/2,c,free,axes,[F(0)]*5,F)
    delta=[b-a for a,b in zip(ya+wa,yb+wb)]
    for i,(l,r,v) in enumerate(zip(f(ya,wa,ja),f(yb,wb,jb),A)):
        assert r-l==sum(k*t for k,t in zip(v,delta))-int(i==POS.index(16))*(jb-ja)
    return len(A)
