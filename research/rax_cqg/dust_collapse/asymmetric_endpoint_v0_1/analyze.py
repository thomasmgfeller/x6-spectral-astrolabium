#!/usr/bin/env python3
"""Exact terminal-clock certificates for two causal arms; no production sum."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reference_action',ROOT/'inputs/reference_action.py')
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
def check(ok,msg):
    if not ok:raise ValueError(msg)
def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

def geometry(p,q):
    left=tuple(range(4,4+p));right=tuple(range(4+p,4+p+q));j=4+p+q
    rel=set(combinations(range(4),2))
    rel.update((a,v)for a in range(4)for v in left+right+(j,))
    rel.update(combinations(left,2));rel.update(combinations(right,2))
    rel.update((a,j)for a in left+right)
    V=frozenset(range(j+1));R=frozenset(rel)
    check(all((a,c)in R for a,b in R for bb,c in R if b==bb),'transitive closure')
    return left,right,j,V,R,ref.weights(R,V)

def gaps_to_times(gaps):
    # g0=U-last, g1=last-previous, ..., glength=first-d, H=1.
    p=len(gaps)-1
    check(sum(gaps)==1 and min(gaps)>0,'normalized strict gaps')
    return tuple(1-sum(gaps[:p-i])for i in range(p))
def profile(p,peak,eps=F(1,100)):
    g=[eps]*(p+1);g[peak]=1-p*eps;return tuple(g)
def arm_score(g):return sum((ref.B[k]*sum(g[:k+1])for k in range(min(len(g)-1,4))),F(0))
def score(K,j,T):return sum((b*(T[j]-T[i])for(i,k),b in K.items()if k==j),F(0))
def shared_score(p,q,outer,U):
    return sum((ref.B[k]*(U-outer[3-i])for i in range(4)for k in [p+q+i]if k<4),F(0))
def chronological(R,T):return all(T[i]<T[j]for i,j in R)

# Sparse rational polynomials for the primary eight-event order.
N=8;Z=(0,)*N
def const(c):return {Z:F(c)}if c else {}
def var(i):e=list(Z);e[i]=1;return {tuple(e):F(1)}
def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items()if c}
def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            ef=tuple(a+b for a,b in zip(e,f));out[ef]=out.get(ef,F(0))+c*d
    return {e:c for e,c in out.items()if c}
def scale(p,c):return {e:c*v for e,v in p.items()if c*v}
def diff(p,i):
    out={}
    for e,c in p.items():
        if e[i]:f=list(e);f[i]-=1;out[tuple(f)]=c*e[i]
    return out

def symbolic_primary(K):
    T=[var(i)for i in range(8)];a,b,c,d,e,f,g,U=T
    delta=lambda a,b:add(a,scale(b,-1))
    sq=lambda p:mul(p,p)
    C=const(1)
    for(i,j),beta in K.items():
        if j==7:C=add(C,scale(sq(delta(U,T[i])),F(beta,2)))
    expected=add(const(1),scale(add(scale(sq(delta(U,d)),-8),scale(sq(delta(U,e)),-9),sq(delta(U,f)),sq(delta(U,g))),F(1,2)))
    D=add(scale(delta(U,e),15),delta(f,e),delta(g,d),scale(delta(e,d),7))
    x,y,z,alpha=delta(e,d),delta(f,e),delta(U,f),delta(g,d)
    H=delta(U,d)
    checks=[]
    def eq(name,l,r):check(l==r,name);checks.append(name)
    eq('original endpoint norm',C,expected)
    eq('negative norm derivative certificate',scale(diff(C,7),-1),D)
    eq('positive edge gap decomposition',D,add(scale(x,7),scale(y,16),scale(z,15),alpha))
    eq('strict lower margin',add(D,scale(H,-7)),add(scale(y,9),scale(z,8),alpha))
    eq('strict upper margin',add(scale(H,17),scale(D,-1)),add(scale(x,9),z,delta(U,g)))
    return checks

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    left,right,j,V,R,K=geometry(2,1)
    coeff={i:b for(i,k),b in K.items()if k==j}
    check(coeff=={0:0,1:0,2:0,3:-8,4:-9,5:1,6:1},'asymmetric endpoint intervals')
    syms=symbolic_primary(K)
    rows=[];samples=0;derivatives=0;primary_bounds=[];all_witnesses=[]
    excluded_positive={(1,2),(2,1),(2,2)}
    excluded_negative={(1,3),(3,1),(3,3)}
    for p,q in product(range(1,5),repeat=2):
        l,r,terminal,V,R,K=geometry(p,q);local=[]
        for ip,iq,c in product(range(p+1),range(q+1),(F(-1,10),F(-1),F(-2))):
            gl,gr=profile(p,ip),profile(q,iq)
            T=(c-2,c-1,c,F(0))+gaps_to_times(gl)+gaps_to_times(gr)+(F(1),)
            check(chronological(R,T),'strict causal clocks')
            S=score(K,terminal,T)
            check(S==arm_score(gl)+arm_score(gr)+shared_score(p,q,T[:4],T[-1]),'global versus arm formula')
            ww=(F(0),)*4+(F(1,2),)*(p+q+1);grad=ref.grad(K,len(T),T,ww)
            check(grad[-1]==-S/4,'original endpoint variation')
            h=F(1,1000);Tp=list(T);Tm=list(T);Tp[-1]+=h;Tm[-1]-=h
            check((ref.action(K,V,Tp,ww)-ref.action(K,V,Tm,ww))/(2*h)==grad[-1],'independent action derivative');derivatives+=1
            if(p,q)in excluded_positive:check(S<0,'positive endpoint exclusion')
            if(p,q)in excluded_negative:check(S>0,'negative endpoint exclusion')
            local.append({'T':T,'S':S,'left_peak':ip,'right_peak':iq});samples+=1
            if(p,q)==(2,1):
                for density,shift in product((F(1,4),F(1,2),F(3,4)),(F(-1,3),F(0),F(2,5))):
                    TT=tuple(x+shift for x in T);ww=(F(0),)*4+(F(1,2),)*3+(density,)
                    qq=ref.grad(K,len(T),TT,ww)[-1];H=TT[-1]-TT[3]
                    D=2*qq/density
                    check(7*H<D<17*H,'strict normalized endpoint bounds')
                    primary_bounds.append({'density':density,'shift':shift,'left_peak':ip,'right_peak':iq,'q_endpoint':qq,'duration':H,'normalized_2q_over_rH':D/H})
        if(p,q)in excluded_positive:status='EXCLUDED_Q_POSITIVE';witness=None
        elif(p,q)in excluded_negative:status='EXCLUDED_Q_NEGATIVE';witness=None
        else:
            lo=next(x for x in local if x['S']<0);hi=next(x for x in local if x['S']>0)
            lam=hi['S']/(hi['S']-lo['S']);T=tuple(lam*x+(1-lam)*y for x,y in zip(lo['T'],hi['T']))
            check(0<lam<1 and chronological(R,T) and score(K,terminal,T)==0,'exact convex clock witness')
            normj=ref.norm(K,terminal,T)
            witness={'T':T,'interpolation_lambda':lam,'endpoint_S':F(0),'endpoint_norm':normj,'full_stationarity_claimed':False}
            all_witnesses.append({'p':p,'q':q,**witness});status='CLOCK_ONLY_FEASIBLE'
        rows.append({'p':p,'q':q,'status':status,'sample_count':len(local),'minimum_S':min(x['S']for x in local),'maximum_S':max(x['S']for x in local),'clock_only_witness':witness})
    # Sharp infimum/supremum approached within the strict order domain.
    l,r,j,V,R,K=geometry(2,1);sharp=[]
    for eps,which in product((F(1,10),F(1,100),F(1,1000)),('lower','upper')):
        if which=='lower':x,y,z,alpha=1-2*eps,eps,eps,eps;expected=7+18*eps
        else:x,y,z,alpha=eps,1-2*eps,eps,1-eps;expected=17-11*eps
        T=(F(-3),F(-2),F(-1),F(0),x,x+y,alpha,F(1))
        check(chronological(R,T) and -score(K,j,T)==expected,'sharp bound witness')
        sharp.append({'epsilon':eps,'approaches':which,'T':T,'normalized_2q_over_rH':expected})
    # Arms of length >=4 share the same active suffix coefficient formula.
    suffix=[]
    for p in (4,5,6,7):
        for peak in range(p+1):
            gl=profile(p,peak);expected=-gl[1]+8*gl[2]-8*gl[3]
            check(arm_score(gl)==expected,'four-suffix identity')
            suffix.append({'length':p,'peak':peak,'score':expected})
    neg=[]
    def reject(label,condition):check(condition,label);neg.append({'incorrect_assumption':label,'rejected':True})
    # Naively copy the old diamond's four active coefficients into the new order.
    T=(F(-3),F(-2),F(-1),F(0),F(1,3),F(2,3),F(1,2),F(1))
    old_like=-8*(T[-1]-T[2])+16*(T[-1]-T[3])+(T[-1]-T[5])+(T[-1]-T[6])
    reject('inserted arm event leaves endpoint coefficients unchanged',score(K,j,T)!=old_like)
    reject('every asymmetric arm pair is excluded',any(x['p']!=x['q']for x in all_witnesses))
    reject('only asymmetric pairs are excluded',any(x['p']==x['q']and x['status'].startswith('EXCLUDED')for x in rows))
    reject('zero endpoint clock derivative proves full stationarity',any(x['endpoint_norm']!=0 for x in all_witnesses))
    ww=(F(0),)*4+(F(0),F(1,2),F(1,2),F(1,2))
    qzero=ref.grad(K,8,T,ww)[-1]
    reject('zero density removes an inserted event from causal intervals',qzero>0 and coeff[4]==-9)
    tiny=(F(0),)*4+(F(1,2),)*3+(F(1,10**12),);qtiny=ref.grad(K,8,T,tiny)[-1]
    reject('small absolute residual removes the normalized obstruction',0<qtiny<F(1,10**9) and 2*qtiny/tiny[-1]>7)
    reject('positive density is unnecessary for the strict bound',ref.grad(K,8,T,(F(0),)*4+(F(1,2),)*3+(F(0),))[-1]==0)
    summary={'status':'PASS','symbolic_primary_identities':len(syms),'arm_length_cases':len(rows),'excluded_cases':sum(x['status'].startswith('EXCLUDED')for x in rows),'clock_only_feasible_cases':len(all_witnesses),'strict_profile_cases':samples,'independent_endpoint_derivatives':derivatives,'primary_bound_cases':len(primary_bounds),'sharp_limit_witnesses':len(sharp),'long_arm_suffix_checks':len(suffix),'negative_controls':len(neg),'full_asymmetric_stationary_solution_derived':False,'physical_gates':'HOLD','paid_compute':False,'n5_production':False,'external_replication':False}
    outputs={'endpoint_certificates.json':{'primary_relation':sorted(geometry(2,1)[4]),'endpoint_coefficients':coeff,'symbolic_checks':syms,'primary_bound_cases':primary_bounds,'sharp_limits':sharp},'arm_length_screen.json':{'row_column_lengths':[1,2,3,'4_or_more'],'tested_representatives':[1,2,3,4],'cases':rows,'long_arm_suffix_checks':suffix,'interpretation':'CLOCK_ONLY_FEASIBLE is not full stationarity'},'controls_and_norm_checks.json':{'negative_controls':neg,'clock_only_witness_norms':[{'p':x['p'],'q':x['q'],'C_endpoint':x['endpoint_norm']}for x in all_witnesses],'boundary_conditions':'exclusions require a free positive terminal endpoint with no outgoing contribution'},'verification.json':summary}
    for name,data in outputs.items():(out/name).write_text(json.dumps(enc(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main(Path(sys.argv[1])if len(sys.argv)>1 else ROOT/'results')
