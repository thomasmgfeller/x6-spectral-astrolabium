"""Independent field construction, exact four-history comparisons and a numerical full-box control."""
from fractions import Fraction as Q
from itertools import combinations, product
import cmath
import json
import math

import auswerten as study
from auswerten import iv, witness, support, MASS, COUPLING, ETA, CODE, ROOT

INNER = support.I
DIN = Q(1023,1024)


def geometry():
    # Construct the order from bits and enumerate maximal internal chains as sets.
    nodes=tuple(INNER)
    internal={pair for bit,pair in enumerate(combinations(nodes,2)) if CODE & (1<<bit)}
    relation=(internal | set(combinations(support.PAST,2)) | set(combinations(support.FUTURE,2))
              | set(product(support.PAST,INNER+support.FUTURE)) | set(product(INNER,support.FUTURE)))
    chains=[]
    for size in range(1,len(nodes)+1):
        for group in combinations(nodes,size):
            if all(edge in internal for edge in combinations(group,2)):
                chains.append(group)
    paths=[p for p in chains if not any(set(p)<set(q) for q in chains)]
    height=max(map(len,paths))
    centres={}
    for j in nodes:
        rank=max(c.index(j)+1 for c in paths if j in c)
        centres[j]=Q(1,2) if all(len(c)==1 for c in paths if j in c) else Q(rank,height+1)
    terms=[]
    for a,b in relation:
        k=sum((a,j) in relation and (j,b) in relation for j in range(15))
        if k<4:
            terms.append((a,b,(1,-9,16,-8)[k]))
    assert set(terms)==set(study.EDGES)
    return sorted(paths),centres,sorted(terms)


PATHS,CENTRES,TERMS=geometry()


def shares_of(u):
    zero=0*next(iter(u.values()))
    f={v:zero for v in INNER}
    for path in PATHS:
        mids=[zero]+[(u[a]+u[b])/2 for a,b in zip(path,path[1:])]+[1+zero]
        for v,a,b in zip(path,mids,mids[1:]):
            f[v]+=(b-a)/len(PATHS)
    return f


def history(rho,coords,side):
    mask,index,sign=coords
    u={v:c+DIN*(1 if mask & (1<<i) else -1)/64 for i,(v,c) in enumerate(CENTRES.items())}
    f=shares_of(u)
    assert sum(f.values())==1 and min(f.values())>0
    left,right=support.WINDOWS[index//2]
    offset=(left+right+(1 if index%2 else -1)*DIN*(right-left))/2
    e=tuple(sorted(offset/d for d in support.DELTA))
    d=tuple(4*a-offset for a in support.DELTA)
    y={v:iv.bounds(Q(v-5)) for v in support.PAST+support.FUTURE}
    y[3]=iv.add(y[3],e)
    for v in INNER:
        y[v]=iv.add(iv.bounds(-2+4*u[v]),iv.mul(e,iv.bounds(1-u[v])))
    w={v:iv.bounds(rho+sign*DIN/32) for v in support.PAST}
    w.update({v:iv.bounds(Q(1,8)) for v in support.FUTURE})
    marker=MASS*(1+side*DIN*ETA)
    for v in INNER:
        w[v]=iv.mul(d,iv.bounds(marker*f[v]))
    assert all(0<l<=r<1 for l,r in w.values())
    assert all(y[a][1]<y[b][0] for a,b in study.ORDER)
    totals={v:iv.bounds(Q(1)) for v in range(15)}
    for a,b,k in TERMS:
        totals[b]=iv.add(totals[b],iv.mul(iv.bounds(Q(k,19)),iv.sq(iv.sub(y[b],y[a]))))
    summed=iv.bounds(Q(0))
    for v in range(15):
        summed=iv.add(summed,iv.mul(w[v],totals[v]))
    return study.quant(iv.mul(iv.bounds(Q(-1,2)),summed)),marker,(offset,w[0][0])


def direct_arms(inputs):
    def arm(sign):
        return sum(float(weight)*cmath.exp(1j*float(iv.center(phase)+sign*COUPLING*x/2))
                   for weight,phase,x in inputs)
    plus,minus=arm(1),arm(-1)
    return (abs(cmath.phase(plus*minus.conjugate())/float(COUPLING*MASS)-1),
            (abs(plus)**2+abs(minus)**2)/2)


def phasor_product(inputs):
    re,im=iv.bounds(Q(0)),iv.bounds(Q(0))
    for w1,p1,x1 in inputs:
        for w2,p2,x2 in inputs:
            angle=iv.add(iv.sub(p1,p2),iv.bounds(COUPLING*((x1+x2)/2-MASS)))
            re=iv.add(re,iv.mul(iv.bounds(w1*w2),study.trig(angle)))
            im=iv.add(im,iv.mul(iv.bounds(w1*w2),study.trig(angle,True)))
    assert re[0]>0
    absolute_im=(0 if im[0]<=0<=im[1] else min(map(abs,im)),max(map(abs,im)))
    z=study.ratio(absolute_im,re)
    assert z[1]<1 and COUPLING*MASS+z[1]<3
    lo=sum((-1)**i*z[0]**(2*i+1)/(2*i+1) for i in range(8))
    hi=sum((-1)**i*z[1]**(2*i+1)/(2*i+1) for i in range(7))
    return study.quant((lo/study.B,hi/study.B),10**10)


def four_histories(rho,coords):
    data=[]
    for (s,c) in zip((1,-1),coords):
        old=history(rho,c,s)
        assert max(old[0][0],witness.history(CODE,rho,s,c)[0])<=min(old[0][1],witness.history(CODE,rho,s,c)[1])
        central=history(rho,c,0)
        assert old[2]==central[2]
        data.extend([old,central])
    assert data[0][2]!=data[2][2]
    marg=(Q(7,11),Q(4,11))
    pairs={str(r):direct_arms([(r/(1+r),*data[0][:2]),(1/(1+r),*data[2][:2])])[0]
           for r in (Q(1),Q(7,4),Q(4,7),Q(4))}
    output={}
    for label,(alpha,beta) in [('A',(DIN,DIN)),('B',(Q(1,1024),Q(1,512)))]:
        w=[marg[0]*alpha,marg[0]*(1-alpha),marg[1]*beta,marg[1]*(1-beta)]
        assert min(w)>0 and (sum(w[:2]),sum(w[2:]))==marg
        mix=[(weight,*row[:2]) for weight,row in zip(w,data)]
        bounds=phasor_product(mix)
        direct,power=direct_arms(mix)
        assert float(bounds[0])<=direct<=float(bounds[1]) and power>0
        state='PASS' if bounds[1]<=Q(1,50) else 'FAIL' if bounds[0]>Q(1,50) else 'HOLD'
        output[label]=dict(weights=w,relative_abs_error=bounds,gate=state)
    return output,pairs


def radical_inverse(k,base):
    factor=1/base
    value=0.0
    while k:
        k,rem=divmod(k,base)
        value+=factor*rem
        factor/=base
    return value


def full_box_check(n=4096):
    # Integrate the uniform jitter variables analytically, and check the full integrand by
    # a deterministic Halton rule in the other nine variables. No quadrature error claim.
    delta=(3/722)**0.25
    primes=(2,3,5,7,11,13,17,19,23)
    geom=[(a,b,c/19) for a,b,c in TERMS]
    norms=[0.0,0.0]
    values={rho:[0j,0j,0j] for rho in study.RHO}
    for k in range(1,n+1):
        q=[radical_inverse(k,p) for p in primes]
        u={v:float(CENTRES[v])+(q[i]-0.5)/32 for i,v in enumerate(INNER)}
        f=shares_of(u)
        for i,(l,r) in enumerate(support.WINDOWS):
            offset=float(l)+float(r-l)*q[7]
            d=4*delta-offset
            y={v:v-5 for v in support.PAST+support.FUTURE}
            y[3]+=offset/delta
            y.update({v:y[3]+d*u[v]/delta for v in INNER})
            c=[1.0]*15
            for a,b,weight in geom:
                c[b]+=weight*(y[b]-y[a])**2
            ws={v:4*d*f[v] for v in INNER}
            derivative={v:-0.5*c[v]*ws[v]*0.01 for v in INNER}
            jac=d**14*math.prod(f.values())
            norms[i]+=jac
            for rho in study.RHO:
                inlet=float(rho)+(q[8]-0.5)/16
                baseline=-0.5*(sum(c[v] for v in support.PAST)*inlet
                              +sum(c[v] for v in support.FUTURE)/8
                              +sum(c[v]*ws[v] for v in INNER))
                for arm,sign in enumerate((1,-1,0)):
                    phase=baseline+sign
                    args=[derivative[v]+sign*.01*f[v] for v in INNER]
                    product_sinc=math.prod(math.sin(x)/x if x else 1.0 for x in args)
                    values[rho][arm]+=jac*cmath.exp(1j*phase)*product_sinc
    return {rho:(abs(cmath.phase(arms[0]*arms[1].conjugate())/2-1),
                 abs(arms[2])/sum(norms)) for rho,arms in values.items()},norms[0]/sum(norms)
