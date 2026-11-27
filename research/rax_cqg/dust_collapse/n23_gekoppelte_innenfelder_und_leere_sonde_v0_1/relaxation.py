"""Linear necessary inequalities with exact coefficients for a window solution."""
from fractions import Fraction as F

NODES=(0,1,2,15,16,17,18,19,20,21,22)
def plus(a,b,s=1):
    out=a.copy()
    for k,v in b.items():out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}

def scaled(a,s):return {k:v*s for k,v in a.items()}
def variable(i):return {(i,):F(1)}
def sq(i,j):
    return {(i,i):F(1),tuple(sorted((i,j))):F(-2),(j,j):F(1)}

PAST_WITH_WEIGHT_EQUATIONS=(0,1,2,15,16)
LATE_WEIGHTS={7:F('0.0039318085937'),8:F('0.0037570718357'),9:F('0.0037144907026'),10:F('0.0039062499995')}
def mon(i,j):return tuple(sorted((i,j)))

def basebox(pair,past,edges):
    # Rational outer hull common to both preparations. Verify its premises.
    bounds={0:(F('-5.00001'),F('-4.99999')),1:(F('-4.00001'),F('-3.99999')),
            2:(F('-3.001'),F('-2.99999'))}
    for side in ('heavy','light'):
        y=pair[side]['clock_box']
        for j in bounds:assert bounds[j][0]<=F(y[j][0])<=F(y[j][1])<=bounds[j][1]
        assert F(y[7][0])==F(y[7][1])==2
        for k in (F(15,32),F(17,32)):
            assert all(F('-.04')<(1-k)*F(z)+2*k<F('.21') for z in y[3])
    for j in (15,16,17,18,19,20):bounds[j]=(bounds[0][0],F(2))
    bounds[15]=bounds[16]=bounds[19]=(bounds[2][0],F(2))
    bounds[18]=(F('-.04'),F(2));bounds[22]=(F('-.04'),F('.21'))
    for j in set(past)&{17,20}:bounds[j]=(bounds[0][0],F('-1.15'))
    if len(set(past)&{17,20})==1:
        other=next(iter({17,20}-set(past)))
        bounds[other]=(F('-.041'),F('.211'))
    terms={i:k for (i,j),k in edges.items() if j==21}
    total=sum(terms.values())
    assert total and all(i in bounds for i in terms)
    upper=sum(max(k/total*b for b in bounds[i]) for i,k in terms.items())
    bounds[21]=(F('3.26') if set(past)&{17,20} else F('-.04'),upper)
    if tuple(past)==PAST_WITH_WEIGHT_EQUATIONS:
        for q in (16,18,19,21):bounds[100+q]=(F(0),F(16))
        for side in ('heavy','light'):
            amp=16 if side=='light' else 1
            for j in LATE_WEIGHTS:
                assert all(abs(amp*F(v)-LATE_WEIGHTS[j])<F(1,10**12) for v in pair[side]['weight_box'][j])
                assert all(abs(F(v)-(j-5))<F(1,10**8) for v in pair[side]['clock_box'][j])
    return bounds

def inequalities(past,rel,edges,bounds):
    rows=[]
    def le(a,b):rows.append((a,F(b)))
    def eq(a,b):le(a,b);le(scaled(a,-1),-b)
    if not set(past)&{17,20}:
        # The two untouched old empty clocks have the same outgoing functional
        # as 22; only 17 carries the strictly nonzero device correction.
        eq(plus(variable(20),variable(22),-1),0)
    if len(set(past)&{17,20})==1:
        v=next(iter({17,20}-set(past)));delta=plus(variable(v),variable(22),-1)
        le(delta,F('0.000001'));le(scaled(delta,-1),F('0.000001'))
    if {17,20}<=set(past):
        delta=plus(variable(17),variable(20),-1)
        le(delta,F('0.000001'));le(scaled(delta,-1),F('0.000001'))
    for i,j in sorted(rel):
        if i in bounds and j in bounds:le(plus(variable(i),variable(j),-1),0)
    pairs=set()
    for j in (16,18,19,21):
        d={};g={}
        for (i,t),k in edges.items():
            if t!=j:continue
            assert i in bounds
            pairs.add((i,j))
            d=plus(d,sq(i,j),k)
            g=plus(g,plus(variable(j),variable(i),-1),k)
        eq(d,-19)
        if j==21:eq(g,0)
        if j==18:le(g, -3 if set(past)&{17,20} else 0)
    if tuple(past)==PAST_WITH_WEIGHT_EQUATIONS:
        err=F(1,10**7)
        for t in range(15,23):
            a={};constant=0;rounding=0
            for (i,j),c in edges.items():
                if t!=i and t!=j:continue
                if t==j:c=-c
                if j in (7,8,9,10):
                    assert t==i
                    constant+=c*LATE_WEIGHTS[j]*(j-5)
                    a=plus(a,variable(i),-c*LATE_WEIGHTS[j])
                    ymax=max(abs(v) for v in bounds[i])
                    rounding+=abs(c)*(F(1,10**12)*(j-5+ymax)+F(1,10**8)*(LATE_WEIGHTS[j]+F(1,10**12)))
                elif j in (16,18,19,21):
                    a=plus(a,{mon(100+j,j):1,mon(100+j,i):-1},c)
                else:assert j in (15,17,20,22)
            assert rounding<err
            le(a,err-constant);le(scaled(a,-1),err+constant)
        for j in (16,18,19,21):
            for i,k in sorted(rel):
                if i in NODES and k in NODES:
                    le({mon(100+j,i):1,mon(100+j,k):-1},0)
    # Each quadratic monomial is lifted once. Use interval products,
    # McCormick envelopes, square tangents, and directed squared-gap bounds.
    monomials=sorted({key for row,b in rows for key in row if len(key)==2})
    boxes={(i,):v for i,v in bounds.items()}
    for i,j in monomials:
        l,h=bounds[i];r,s=bounds[j];z={(i,j):F(1)}
        if i==j:
            seg=[l*l,h*h]
            boxes[i,i]=(0 if l<=0<=h else min(seg),max(seg))
        else:
            seg=[v*w for v in (l,h) for w in (r,s)];boxes[i,j]=(min(seg),max(seg))
        for u,v,sign in [(l,r,1),(h,s,1),(l,s,-1),(h,r,-1)]:
            a=plus(scaled(variable(j),u),scaled(variable(i),v))
            le(scaled(plus(a,z,-1),sign),sign*u*v)
        if i==j:
            for u in [(l+h)/2, F(0)]:le(plus(scaled(variable(i),2*u),z,-1),u*u)
    for i,j in sorted(pairs):
        u=plus(variable(j),variable(i),-1);z=sq(i,j)
        l=max(0,bounds[j][0]-bounds[i][1]);h=bounds[j][1]-bounds[i][0]
        if h<l:le({},-1);continue
        le(plus(z,u,-(l+h)),-l*h)
        for v in (l,(l+h)/2,h):le(plus(scaled(u,2*v),z,-1),v*v)
    return boxes,rows
