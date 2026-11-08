#!/usr/bin/env python3
"""Exact finite block bookkeeping and Q(sqrt(305)) stationary witnesses."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
from math import isqrt
import json,sys

def check(ok,msg):
    if not ok:raise ValueError(msg)

class Q:
    def __init__(self,a=0,b=0):self.a,self.b=F(a),F(b)
    @staticmethod
    def asq(x):return x if isinstance(x,Q)else Q(x)
    def __add__(self,o):o=Q.asq(o);return Q(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,o):return self+-Q.asq(o)
    def __rsub__(self,o):return Q.asq(o)+-self
    def __mul__(self,o):o=Q.asq(o);return Q(self.a*o.a+305*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=Q.asq(o);d=o.a*o.a-305*o.b*o.b
        if not d:raise ZeroDivisionError()
        return self*Q(o.a/d,-o.b/d)
    def __rtruediv__(self,o):return Q.asq(o)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        r=Q(1)
        for _ in range(n):r=r*self
        return r
    def __eq__(self,o):o=Q.asq(o);return self.a==o.a and self.b==o.b
    def sign(self):
        if self.b==0:return (self.a>0)-(self.a<0)
        if self.a==0:return (self.b>0)-(self.b<0)
        sa=(self.a>0)-(self.a<0);sb=(self.b>0)-(self.b<0)
        if sa==sb:return sa
        d=self.a*self.a-305*self.b*self.b
        return sa*((d>0)-(d<0))
    def __lt__(self,o):return (self-o).sign()<0
    def __le__(self,o):return (self-o).sign()<=0
    def __gt__(self,o):return (self-o).sign()>0
    def __ge__(self,o):return (self-o).sign()>=0
    def __bool__(self):return self.a!=0 or self.b!=0

def enc(x):
    if isinstance(x,Q):return {'rational':str(x.a),'sqrt305':str(x.b)}
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:enc(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v)for v in x]
    return x
B=(1,-9,16,-8)
def weights(rel,V):
    return {(y,x):B[k] if k<4 else 0 for y,x in sorted(rel) if y in V and x in V
            for k in [sum((y,z)in rel and (z,x)in rel for z in V)]}
def action(K,V,T,w):return -sum((w[x]for x in V),F(0))/2-sum((w[x]*b*(T[x]-T[y])**2 for (y,x),b in K.items()),F(0))/4
def grad(K,n,T,w):
    q=[F(0)for _ in range(n)]
    for (y,x),b in K.items():
        j=w[x]*b*(T[x]-T[y])/2;q[y]+=j;q[x]-=j
    return q

def norm(K,x,T):return 1+sum((b*(T[x]-T[y])**2 for (y,xx),b in K.items()if xx==x),F(0))/2

def natural_orders(n):
    pairs=list(combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        rel=frozenset(p for j,p in enumerate(pairs)if mask>>j&1)
        if all((a,c)in rel for a,b in rel for bb,c in rel if b==bb):yield rel

def correction(K,KL,KR,KD):return {p:K[p]-KL.get(p,0)-KR.get(p,0)+KD.get(p,0)for p in K}
def rank(M):
    a=[list(row)for row in M];r=0
    for c in range(len(a[0])):
        z=next((j for j in range(r,len(a))if a[j][c]),None)
        if z is None:continue
        a[r],a[z]=a[z],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for j in range(len(a)):
            if j!=r:
                v=a[j][c];a[j]=[x-v*y for x,y in zip(a[j],a[r])]
        r+=1
        if r==len(a):break
    return r

def pmul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def padd(*rows):return [sum((r[i]if i<len(r)else F(0)for r in rows),F(0))for i in range(max(map(len,rows)))]
def pscale(a,k):return [k*x for x in a]
def peval(p,x):return sum((a*x**i for i,a in enumerate(p)),F(0))

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    counts={'orders':0,'covers':0,'matter_action_cases':0,'response_components':0,'gravity_identities':0,'nonzero_corrections':0,'reclassification_covers':0}
    first_reclassification=None;by_n={}
    for n in range(1,5):
        U=frozenset(range(n));posets=list(natural_orders(n));by_n[str(n)]=len(posets);counts['orders']+=len(posets)
        for rel in posets:
            allsets=[frozenset(i for i in U if m>>i&1)for m in range(1<<n)]
            cache={V:weights(rel,V)for V in allsets};K=cache[U]
            fields=[(tuple(F((i+1)**2,7)for i in U),tuple(F(i+1,n+2)for i in U)),(tuple(F(i+1,3)for i in U),tuple(F(0)if i%2 else F(2,3)for i in U))]
            for labels in product(range(3),repeat=n):
                L=frozenset(i for i in U if labels[i]!=1);R=frozenset(i for i in U if labels[i]!=0);D=L&R
                if not L or not R:continue
                KL,KR,KD=(cache[V]for V in (L,R,D));delta=correction(K,KL,KR,KD)
                counts['covers']+=1
                counts['nonzero_corrections']+=any(delta.values())
                reclass=[p for p in K if delta[p] and ((p[0]in L and p[1]in L)or(p[0]in R and p[1]in R))]
                if reclass:
                    counts['reclassification_covers']+=1
                    if first_reclassification is None:first_reclassification={'n':n,'relation':sorted(rel),'L':sorted(L),'R':sorted(R),'D':sorted(D),'delta_B':[[y,x,v]for (y,x),v in delta.items()if v]}
                Fg=lambda V:len(V)-sum(cache[V].values())
                check(Fg(U)-Fg(L)-Fg(R)+Fg(D)==-sum(delta.values()),'gravity gluing')
                counts['gravity_identities']+=1
                for T,w in fields:
                    residual=action(K,U,T,w)-action(KL,L,T,w)-action(KR,R,T,w)+action(KD,D,T,w)
                    deltaS=-sum((w[x]*v*(T[x]-T[y])**2 for (y,x),v in delta.items()),F(0))/4
                    check(residual==deltaS,'matter inclusion-exclusion')
                    q,ql,qr,qd=(grad(kk,n,T,w)for kk in (K,KL,KR,KD));dc=grad(delta,n,T,w)
                    for i in U:check(q[i]-ql[i]-qr[i]+qd[i]==dc[i],'interface response correction');counts['response_components']+=1
                    counts['matter_action_cases']+=1
    check(by_n=={'1':1,'2':2,'3':7,'4':40},'natural-order enumeration')
    chain_rows=[]
    for n in range(6,11):
        U=frozenset(range(n));rel=frozenset(combinations(range(n),2));K=weights(rel,U)
        for j in range(3,n-1):
            for m in range(1,min(5,j+1)+1):
                L=frozenset(range(j+1));R=frozenset(range(j-m+1,n));D=L&R
                dB=correction(K,weights(rel,L),weights(rel,R),weights(rel,D))
                exact=not any(dB.values())
                check(exact==(m>=4),'four-element chain memory')
                if m<4:check(dB[(j-m,j+1)]==B[m],'missing active cross interval')
                chain_rows.append({'n':n,'cut':j,'overlap':m,'exact_without_correction':exact,'nonzero_delta_pairs':sum(v!=0 for v in dB.values())})
    # The four-record result is not universal for non-chain orders.
    star=frozenset((y,5)for y in range(5));U=frozenset(range(6));L=frozenset(range(5));R=frozenset(range(1,6));D=L&R
    star_delta=correction(weights(star,U),weights(star,L),weights(star,R),weights(star,D))
    check(star_delta[(0,5)]==1,'non-chain width counterexample')
    # Original fixed collar: one future positive element is impossible.
    old=(F(-5,2),F(-2),F(-4,3),F(0));rel6=frozenset(combinations(range(6),2));K6=weights(rel6,U)
    frozen=[]
    for t,g,w,v in product((F(1,16),F(1,8),F(1,4)),(F(1,16),F(1,4),F(1)),(F(1,4),F(1,2),F(3,4)),(F(1,4),F(1,2),F(3,4))):
        u=t+g;T=old+(t,u);ww=(F(0),)*4+(w,v);q=grad(K6,6,T,ww)
        check(norm(K6,4,T)==0,'inherited first normalization')
        check(q[4]==v*(u-t)/2 and q[4]>0,'frozen-collar one-future exclusion')
        frozen.append({'t':t,'u':u,'w':w,'v':v,'interface_residual':q[4]})
    # Two future positive elements: a concave positive norm polynomial.
    tpoly=[F(0),F(1)];upoly=[F(-32,3),F(9)]
    H=padd(pscale(pmul(tpoly,tpoly),F(1,2)),pscale(pmul(tpoly,upoly),F(-1)),pscale(upoly,F(16,3)),[F(-7,9)])
    check(H==[F(-173,3),F(176,3),F(-17,2)],'two-future norm polynomial')
    endpoints=[peval(H,F(4,3)),peval(H,F(16,3))]
    check(endpoints==[F(49,9),F(121,9)]and H[2]<0,'concavity positivity certificate')
    # Retuned collar: exact two-free-element stationary family, with old units.
    r=Q(0,1);kappa=(70-4*r)/3;check(kappa>0,'positive kappa')
    family=[];hessian_cases=0;derivatives=0
    def setup(c,w,v):
        return tuple(x+c for x in (-r/6,Q(F(-5,2)),Q(-2),Q(F(-4,3))))+(Q(c),Q(c)+kappa*w/v),(Q(0),)*4+(Q(w),Q(v))
    def bulkgrad(T,ww):
        qs=grad(K6,6,T,ww)
        return [qs[4],qs[5],-norm(K6,4,T)/2,-norm(K6,5,T)/2]
    for c,w,v in product((F(-1,3),F(0),F(2,5)),(F(1,4),F(1,2),F(3,4)),(F(1,4),F(1,2),F(3,4))):
        T,ww=setup(c,w,v);q=grad(K6,6,T,ww)
        check(all(T[i]<T[i+1]for i in range(5)),'new chronological collar')
        check(norm(K6,4,T)==norm(K6,5,T)==0,'joint normalization')
        check(q[4]==q[5]==0,'joint clock stationarity')
        check(sum(q)==0 and sum((x*y for x,y in zip(T,q)),Q(0))==w+v,'outer reaction balance')
        left=frozenset(range(5));KL=weights(rel6,left);ql=grad(KL,6,T,ww)
        check(ql[4]==-w*kappa/2 and q[4]-ql[4]==w*kappa/2,'momentum matching with nonzero reactions')
        h=F(1,1024)
        Hnum=[]
        for i in range(4):
            Tp=list(T);Tm=list(T);wp=list(ww);wm=list(ww)
            if i<2:Tp[4+i]+=h;Tm[4+i]-=h
            else:wp[2+i]+=h;wm[2+i]-=h
            der=(action(K6,U,Tp,wp)-action(K6,U,Tm,wm))/(2*h)
            check(der==bulkgrad(T,ww)[i],'independent action derivative');derivatives+=1
            gp,gm=bulkgrad(Tp,wp),bulkgrad(Tm,wm)
            Hnum.append([(a-b)/(2*h)for a,b in zip(gp,gm)])
        u=T[5]-c
        Hexpected=[[-Q(v)/2,Q(v)/2,-kappa/2,u/2],[Q(v)/2,Q(0),Q(0),Q(0)],[-kappa/2,Q(0),Q(0),Q(0)],[u/2,Q(0),Q(0),Q(0)]]
        check(Hnum==Hexpected and rank(Hnum)==2,'rank-two stationary Hessian');hessian_cases+=1
        # Verify the complete normal form away from the stationary point.
        for dt,du in ((F(1,2000),F(-1,3000)),(F(-1,2000),F(1,3000))):
            P=list(T);P[4]+=dt;P[5]+=du;tt=P[4]-c;uu=P[5]-c
            expected=tt*(v*uu-w*kappa)/2-v*tt*tt/4
            check(action(K6,U,P,ww)==expected,'exact coupled normal form')
        family.append({'shift':c,'T':T,'w':w,'v':v,'past_reactions':q[:4],'left_interface_reaction':ql[4],'future_interface_reaction':q[4]-ql[4],'hessian_rank':2})
    # Concrete negative controls.
    neg=[]
    def reject(name,test):check(test,name);neg.append({'incorrect_assumption':name,'rejected':True})
    TT=old+(F(1,2),F(1));ww=(F(0),)*4+(F(1,2),F(1,2));L=frozenset(range(5));R=frozenset((4,5));D=L&R
    naive=action(weights(rel6,L),L,TT,ww)+action(weights(rel6,R),R,TT,ww)-action(weights(rel6,D),D,TT,ww)
    reject('single interface point suffices without cross terms',naive!=action(K6,U,TT,ww))
    reject('three common chain records always suffice',any(z['overlap']==3 and not z['exact_without_correction']for z in chain_rows))
    reject('four common records suffice on every causal set',star_delta[(0,5)]!=0)
    reject('internal interval reclassification can be discarded',first_reclassification is not None)
    reject('fixed-collar exclusion rules out every collar',len(family)>0 and all(z['hessian_rank']==2 for z in family))
    reject('each block must be separately stationary at a glued interface',family[0]['left_interface_reaction']!=0 and family[0]['left_interface_reaction']+family[0]['future_interface_reaction']==0)
    reject('joint inner stationarity closes the outer reaction',any(family[0]['past_reactions']))
    Tnew,wnew=setup(F(0),F(1,2),F(1,2));Tbad=list(Tnew);Tbad[0]+=F(1,1000)
    reject('the retuned boundary data need no preparation',norm(K6,4,Tbad)!=0)
    # An appended future zero-density row has zero matter response.
    wzero=(F(0),)*4+(F(1,2),F(0));qzero=grad(K6,6,TT,wzero)
    check(qzero[4]==0 and action(K6,U,TT,wzero)==action(weights(rel6,L),L,TT,wzero),'appended zero-density control')
    den=10**12;lower=F(isqrt(305*den*den),den);upper=lower+F(1,den)
    check(lower*lower<305<upper*upper,'sqrt enclosure')
    k_bounds=[(70-4*upper)/3,(70-4*lower)/3]
    summary={'status':'PASS',**counts,'natural_orders_by_n':by_n,'chain_overlap_cases':len(chain_rows),'frozen_one_future_cases':len(frozen),'new_collar_family_cases':len(family),'independent_bulk_derivatives':derivatives,'hessian_cases':hessian_cases,'hessian_components':hessian_cases*16,'negative_controls':len(neg),'physical_gates':'HOLD','paid_compute':False,'n5_production':False,'physical_vacuum_exterior_derived':False,'external_replication':False}
    outputs={
      'gluing_and_memory.json':{'summary':counts,'first_reclassification':first_reclassification,'chain_overlap':chain_rows,'nonchain_counterexample':{'relation':sorted(star),'overlap':4,'missing_pair':[0,5],'delta_B':1}},
      'frozen_collar_exclusions.json':{'one_future':frozen,'two_future':{'H_coefficients':H,'necessary_t_interval':[F(4,3),F(16,3)],'endpoint_values':endpoints,'concave':True}},
      'retuned_stationary_family.json':{'kappa':kappa,'sqrt305_bounds':[lower,upper],'kappa_bounds':k_bounds,'cases':family,'negative_controls':neg},
      'verification.json':summary}
    for name,data in outputs.items():(out/name).write_text(json.dumps(enc(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(enc(summary),sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1])if len(sys.argv)>1 else Path(__file__).parent/'results')
