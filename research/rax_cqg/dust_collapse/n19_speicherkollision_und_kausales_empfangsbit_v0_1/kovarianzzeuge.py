"""Exact, source-independent moment-matched input law and optimal finite-word error."""
from collections import defaultdict
from fractions import Fraction as F
from empfangsbit import K0,V,R,receiver_bit,late_code,classify
from kollision import search


def outer(v,i,j):return v[i]*v[j]


def residual_ldl(cov):
    n=len(cov)
    L=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    D=[]
    for j in range(n):
        d=cov[j][j]-sum(L[j][k]**2*D[k] for k in range(j))
        assert d>0
        D.append(d)
        for i in range(j+1,n):
            L[i][j]=(cov[i][j]-sum(L[i][k]*D[k]*L[j][k] for k in range(j)))/d
    assert all(sum(L[i][k]*D[k]*L[j][k] for k in range(n))==cov[i][j] for i in range(n) for j in range(n))
    return list(zip(zip(*L),D))


def make_law(arms):
    n=6;lam=F(1,2000000)
    vels=[tuple(map(F,a['y'])) for a in arms]
    spikes=[tuple(F(5,2)*v for v in vel)+vel for vel in vels]
    residual=[[F(int(i==j),9)-lam*sum(outer(v,i,j) for v in spikes)
               for j in range(n)] for i in range(n)]
    pairs=[(s,lam) for s in spikes]+residual_ldl(residual)
    law=defaultdict(F)
    for x,mass in pairs:
        law[tuple(x)]+=mass/2
        law[tuple(-v for v in x)]+=mass/2
    law[(F(0),)*6]+=1-sum(law.values())
    assert all(p>0 for p in law.values()) and sum(law.values())==1
    assert all(sum(v[i]*p for v,p in law.items())==0 for i in range(n))
    assert all(sum(v[i]*v[j]*p for v,p in law.items())==F(int(i==j),9) for i in range(n) for j in range(n))
    assert max(abs(z) for v in law for z in v[3:])<64
    return law


def histogram_result(table):
    error=F(0);ambiguous=[]
    for word,weights in sorted(table.items()):
        missed=sum(weights.values())-max(weights.values())
        error+=missed
        if missed:ambiguous.append({'word':word,'joint_weights':{str(k):str(v) for k,v in weights.items()},
                                    'unavoidable_error':str(missed)})
    assert sum(sum(row.values()) for row in table.values())==1
    return {'different_words':len(table),'minimum_error':str(error),'ambiguous_words':ambiguous}


def run(previous,early):
    from quelle import box
    from proben import samples
    from staubgeraet import solve,verify
    from uhrauslese import LABELS
    from nullreferenz import digit
    _,y,w=next(r for r in samples(previous,early)[0] if r[0]=='quarter')
    route='positive_bridge'
    arms=search(y,w,route,*LABELS[:2])
    law=make_law(arms)
    tables=[defaultdict(lambda:defaultdict(F)) for _ in range(2)]
    fixed_error=F(0)
    for xy,p in law.items():
        q=tuple(box(R*(x-F(5,2)*v)) for x,v in zip(xy[:3],xy[3:]))
        assert all(abs(R*(x-F(5,2)*v))<=1 for x,v in zip(xy[:3],xy[3:]))
        vel=tuple(box(V*v) for v in xy[3:])
        for J in LABELS:
            st=solve(y,w,J,vel,K0,box(-K0),route)
            hist,_=verify(st,J,vel,K0,box(-K0),route,q)
            word=tuple(map(digit,[st['y'][7],*[h[7] for h in hist],*q]))
            assert all(type(c) is int for c in word)
            baseline=digit(y[18])
            bit=receiver_bit(digit(st['y'][18]),baseline)
            late=late_code(word[0],word[3],word[6],baseline)
            fixed_error+=p/3*(classify(bit,late)!=J)
            for table,code in zip(tables,(word,word+(bit,))):table[code][J]+=p/3
    raw,extended=map(histogram_result,tables)
    assert F(raw['minimum_error'])>=F(1,12000000) and extended['minimum_error']=='0' and fixed_error==0
    return {'point_count':len(law),'label_priors':['1/3']*3,'mean':['0']*6,'covariance_diagonal':['1/9']*6,
            'covariance_off_diagonal':'0','joint_law_product':False,'scope':'quarter, positive_bridge, weak inertia',
            'law':[{'xy':list(map(str,z)),'probability':str(p)} for z,p in law.items()],
            'late_only':raw,'late_with_bit':extended,'prespecified_bit_decoder_error':str(fixed_error)}
