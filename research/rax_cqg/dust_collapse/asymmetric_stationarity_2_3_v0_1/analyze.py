#!/usr/bin/env python3
"""Exact full-system certificate for the fixed (2,3) two-arm order.

Only Python's standard library; no production histories or numerical root search.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import importlib.util, json, sys
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('reference_action', ROOT/'inputs/reference_action.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)

def check(ok, message):
    if not ok: raise ValueError(message)

def enc(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)): return [enc(v) for v in x]
    return x

def geometry():
    V=frozenset(range(10)); left=(4,5); right=(6,7,8); j=9
    R=set(combinations(range(4),2))
    R.update((a,x) for a in range(4) for x in range(4,10))
    R.update(combinations(left,2)); R.update(combinations(right,2))
    R.update((x,j) for x in left+right)
    R=frozenset(R)
    check(all((a,c) in R for a,b in R for bb,c in R if b==bb),'transitive order')
    return V,R,ref.weights(R,V)

def explicit(T,W):
    a,b,c,d,e,f,g,h,i,U=T; we,wf,wg,wh,wi,r=W[4:]
    P=-8*a+16*b-9*c+d; A=1+(-8*a*a+16*b*b-9*c*c+d*d)/2
    Pe=-8*b+16*c-9*d+e; Pg=-8*b+16*c-9*d+g
    Ae=1+(-8*b*b+16*c*c-9*d*d+e*e)/2
    Ag=1+(-8*b*b+16*c*c-9*d*d+g*g)/2
    Q=-8*c+16*d-9*g+h; B=1+(-8*c*c+16*d*d-9*g*g+h*h)/2
    L=9*e-f-16*g+9*h-i
    M=-9*e*e+f*f+16*g*g-9*h*h+i*i
    norms=[A-P*e,Ae-Pe*f,A-P*g,Ag-Pg*h,B-Q*i,1+U*L+M/2]
    q=[(we*P+wf*(f-e)-9*r*(U-e))/2,
       (wf*Pe+r*(U-f))/2,
       (wg*P+wh*(h-g)-9*wi*(i-g)+16*r*(U-g))/2,
       (wh*Pg+wi*(i-h)-9*r*(U-h))/2,
       (wi*Q+r*(U-i))/2,-r*L/2]
    return norms,q

# Sparse multivariate polynomials over Q: no symbolic dependency or float tolerance.
N=16; ZERO=(0,)*N
def const(c): return {ZERO:F(c)} if c else {}
def var(i):
    e=list(ZERO);e[i]=1;return {tuple(e):F(1)}
def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}
def scale(p,k):return {e:k*c for e,c in p.items() if k*c}
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            ef=tuple(x+y for x,y in zip(e,f));out[ef]=out.get(ef,F(0))+c*d
    return {e:c for e,c in out.items() if c}
def sq(p):return mul(p,p)
def diff(p,i):
    out={}
    for e,c in p.items():
        if e[i]:f=list(e);f[i]-=1;out[tuple(f)]=e[i]*c
    return out

def symbolic(K):
    T=[var(k) for k in range(10)]; W=[const(0)]*4+[var(k) for k in range(10,16)]
    a,b,c,d,e,f,g,h,i,U=T; we,wf,wg,wh,wi,r=W[4:]
    C=[]
    for x in range(4,10):
        C.append(add(const(1),*[scale(sq(sub(T[x],T[y])),F(beta,2)) for (y,xx),beta in K.items() if xx==x]))
    action=scale(add(*[mul(w,c) for w,c in zip(W[4:],C)]),F(-1,2))
    P=add(scale(a,-8),scale(b,16),scale(c,-9),d)
    A=add(const(1),scale(add(scale(sq(a),-8),scale(sq(b),16),scale(sq(c),-9),sq(d)),F(1,2)))
    def second(x,y):
        Px=add(scale(b,-8),scale(c,16),scale(d,-9),x)
        Ax=add(const(1),scale(add(scale(sq(b),-8),scale(sq(c),16),scale(sq(d),-9),sq(x)),F(1,2)))
        return sub(Ax,mul(Px,y)),Px
    Cf,Pe=second(e,f);Ch,Pg=second(g,h)
    Q=add(scale(c,-8),scale(d,16),scale(g,-9),h)
    B=add(const(1),scale(add(scale(sq(c),-8),scale(sq(d),16),scale(sq(g),-9),sq(h)),F(1,2)))
    L=add(scale(e,9),scale(f,-1),scale(g,-16),scale(h,9),scale(i,-1))
    M=add(scale(sq(e),-9),sq(f),scale(sq(g),16),scale(sq(h),-9),sq(i))
    expectedC=[sub(A,mul(P,e)),Cf,sub(A,mul(P,g)),Ch,sub(B,mul(Q,i)),add(const(1),mul(U,L),scale(M,F(1,2)))]
    expected2q=[add(mul(we,P),mul(wf,sub(f,e)),scale(mul(r,sub(U,e)),-9)),
                add(mul(wf,Pe),mul(r,sub(U,f))),
                add(mul(wg,P),mul(wh,sub(h,g)),scale(mul(wi,sub(i,g)),-9),scale(mul(r,sub(U,g)),16)),
                add(mul(wh,Pg),mul(wi,sub(i,h)),scale(mul(r,sub(U,h)),-9)),
                add(mul(wi,Q),mul(r,sub(U,i))),scale(mul(r,L),-1)]
    checks=[]
    def eq(name,left,right):check(left==right,name);checks.append(name)
    for k in range(6):
        eq('norm_'+str(k),C[k],expectedC[k])
        eq('clock_derivative_'+str(k),scale(diff(action,k+4),2),expected2q[k])
        eq('density_derivative_'+str(k),scale(diff(action,k+10),-2),C[k])
    eq('first_norm_difference',sub(C[0],C[2]),mul(P,sub(g,e)))
    # Abstract gap variables; substitute the terminal clock equation explicitly.
    t,v,w,gamma,s,base,last=[var(k) for k in range(7)]
    egap=sub(scale(add(t,w),F(1,8)),v)
    ee=add(base,egap); ff=add(ee,t);gg=base;hh=add(base,v);ii=add(hh,w)
    M0=add(scale(sq(ee),-9),sq(ff),scale(sq(gg),16),scale(sq(hh),-9),sq(ii))
    reduced=add(scale(sq(t),F(9,8)),scale(sq(w),F(7,8)),scale(mul(v,w),4),scale(sq(v),-16))
    eq('terminal_second_moment_reduction',M0,reduced)
    tsame=sub(scale(v,8),w)
    same=add(sq(tsame),scale(sq(v),-9),sq(add(v,w)))
    eq('equal_first_clocks_square_certificate',scale(same,F(1,2)),add(sq(sub(w,scale(v,F(7,2)))),scale(sq(v),F(63,4))))
    cf=add(scale(sq(gamma),F(-1,2)),mul(t,gamma))
    ch=add(scale(sq(sub(gamma,s)),F(-1,2)),mul(v,sub(gamma,s)))
    eq('second_norm_difference',sub(cf,ch),add(mul(gamma,sub(t,add(v,s))),mul(s,add(v,scale(s,F(1,2))))))
    eq('positive_quadratic_remainder',sub(add(scale(sq(t),9),scale(sq(w),7)),scale(sq(add(t,w)),F(7,2))),add(scale(sq(sub(t,w)),F(7,2)),scale(sq(t),2)))
    eq('clock_elimination',sub(mul(t,last),scale(mul(gamma,add(last,t)),9)),sub(mul(last,sub(t,scale(gamma,9))),scale(mul(gamma,t),9)))
    eq('half_ratio_margin',sub(scale(add(v,scale(s,F(1,2))),2),sub(add(v,s),t)),add(v,t))
    eq('unit_ratio_margin',sub(add(v,scale(s,F(1,2))),sub(add(v,s),t)),sub(t,scale(s,F(1,2))))
    return checks

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    V,R,K=geometry();checks=symbolic(K)
    check({y:b for (y,x),b in K.items() if x==9}=={0:0,1:0,2:0,3:0,4:-9,5:1,6:16,7:-9,8:1},'terminal coefficients')
    samples=clock_diffs=density_diffs=0
    snapshots=[]; gaps=(F(1,10),F(1,3),F(1)); shifts=(F(-2,3),F(0),F(3,5))
    profiles=[(x,y) for x in ((F(1,5),F(1,3)),(F(1,2),F(1,4))) for y in ((F(1,7),F(1,4),F(1,2)),(F(1,3),F(1,5),F(1,8)),(F(2,5),F(1,3),F(1,6)))]
    densities=[(F(1,4),)*6,(F(1,2),)*6,tuple(F(k,7) for k in range(1,7))]
    for L,M,N,(ll,rr),W0,shift in product(gaps,gaps,gaps,profiles,densities,shifts):
        e=ll[0];f=sum(ll);g=rr[0];h=sum(rr[:2]);i=sum(rr);U=max(f,i)+F(2,3)
        T=tuple(x+shift for x in (-(L+M+N),-(L+M),-L,F(0),e,f,g,h,i,U));W=(F(0),)*4+W0
        check(all(T[x]<T[y] for x,y in R),'causal clocks')
        cs,qs=explicit(T,W);originalq=ref.grad(K,10,T,W)
        eps=F(1,1000)
        for z in range(4,10):
            check(cs[z-4]==ref.norm(K,z,T) and qs[z-4]==originalq[z],'explicit full system')
            plus=list(T);minus=list(T);plus[z]+=eps;minus[z]-=eps
            dq=(ref.action(K,V,plus,W)-ref.action(K,V,minus,W))/(2*eps)
            check(dq==qs[z-4],'clock central derivative');clock_diffs+=1
            wp=list(W);wm=list(W);wp[z]+=eps;wm[z]-=eps
            dw=(ref.action(K,V,T,wp)-ref.action(K,V,T,wm))/(2*eps)
            check(dw==-cs[z-4]/2,'density central derivative');density_diffs+=1
        check(sum(originalq)==0,'global clock shift identity')
        samples+=1
        if len(snapshots)<3:snapshots.append({'T':T,'W':W,'norms':cs,'clock_gradient':qs})
    # Nonvacuous conditional certificate witnesses, not full stationary solutions.
    witnesses=[]
    for v,shift in product((F(1,3),F(1),F(2)),shifts):
        s=v/100;t=v/10;w=8*(v-s)-t
        gamma=s*(v+s/2)/(v+s-t)
        u=9*gamma*t/(t-9*gamma)
        e=v;g=e+s;f=e+t;h=g+v;i=h+w;U=f+u;K0=e+gamma
        T=tuple(x+shift for x in (-21*K0/8,-15*K0/8,-K0,F(0),e,f,g,h,i,U))
        r=F(1,10000);wf=9*r*(U-e)/t;W=(F(0),)*4+(F(1,2),wf,F(1,2),F(1,2),F(1,2),r)
        cs,qs=explicit(T,W)
        check(all(T[x]<T[y] for x,y in R) and all(0<x<1 for x in W[4:]),'conditional witness domain')
        check(-8*T[0]+16*T[1]-9*T[2]+T[3]==0,'P zero witness')
        check(qs[0]==qs[1]==qs[5]==0 and cs[0]==cs[2] and cs[1]==cs[3],'nonvacuous conditional constraints')
        check(t>9*gamma and gamma>s and v>8*s,'exceptional branch inequalities')
        check(cs[5]>1+F(87,32)*v*v,'uniform positive norm margin')
        witnesses.append({'T':T,'W':W,'P':F(0),'left_clock_and_endpoint_clock_zero':True,'second_norms_equal':True,'norms':cs,'terminal_lower_bound':1+F(87,32)*v*v,'full_stationarity':False})
    equal=[]
    for v,ratio,shift in product(gaps,(F(1),F(2),F(7)),shifts):
        w=ratio*v;t=8*v-w;e=g=v;f=e+t;h=g+v;i=h+w;U=max(f,i)+v
        T=tuple(x+shift for x in (F(-3),F(-2),F(-1),F(0),e,f,g,h,i,U));W=(F(0),)*4+(F(1,2),)*6
        cs,qs=explicit(T,W)
        check(qs[-1]==0 and cs[-1]==1+(w-F(7,2)*v)**2+F(63,4)*v*v,'equal first clocks norm')
        equal.append({'v':v,'w':w,'shift':shift,'endpoint_norm':cs[-1]})
    # The previous published clock-only witness must be retained, not promoted.
    oldT=tuple(map(F,('-21/10','-11/10','-1/10','0','1/100','1/50','1/100','1/50','9/100','1')))
    oldW=(F(0),)*4+(F(1,2),)*6;oldC,oldq=explicit(oldT,oldW)
    negative=[]
    def reject(name,condition):check(condition,name);negative.append({'incorrect_claim':name,'rejected':True})
    reject('terminal clock alone proves stationarity',oldq[-1]==0 and oldC[-1]==F(2507,2500))
    reject('exceptional collar may be dropped',len(witnesses)>0 and witnesses[0]['P']==0)
    reject('equal second norms mean zero second norms',witnesses[0]['norms'][1]==witnesses[0]['norms'][3]!=0)
    reject('clock-feasible branches must have equal first clocks',witnesses[0]['T'][4]!=witnesses[0]['T'][6])
    zeroW=list(oldW);zeroW[-1]=F(0)
    reject('zero density deletes its free density equation',explicit(oldT,zeroW)[0][-1]==oldC[-1]!=0)
    wrong=dict(K);wrong[(4,9)]=1
    reject('old link coefficient survives global interval recount',ref.norm(wrong,9,oldT)!=oldC[-1])
    # Swapping the complete arms is an isomorphism, not a numerical relabelling order.
    perm={0:0,1:1,2:2,3:3,4:7,5:8,6:4,7:5,8:6,9:9}
    RR=frozenset((perm[x],perm[y]) for x,y in R);KK=ref.weights(RR,V)
    TT=[F(0)]*10;WW=[F(0)]*10
    for x in V:TT[perm[x]]=oldT[x];WW[perm[x]]=oldW[x]
    check(ref.action(KK,V,TT,WW)==ref.action(K,V,oldT,oldW),'arm-exchange action')
    oq=ref.grad(K,10,oldT,oldW);nq=ref.grad(KK,10,TT,WW)
    for x in V:check(nq[perm[x]]==oq[x] and ref.norm(KK,perm[x],TT)==ref.norm(K,x,oldT),'arm-exchange equations')
    summary={'status':'PASS','symbolic_identities':len(checks),'strict_profiles':samples,'independent_clock_derivatives':clock_diffs,'independent_density_derivatives':density_diffs,'exceptional_conditional_witnesses':len(witnesses),'equal_first_clock_controls':len(equal),'negative_controls':len(negative),'arm_exchange_components':10,'excluded_full_stationarity_classes':[[2,3],[3,2]],'bound':'C_j > 1 + 87*v^2/32 under the stated necessary subset; conservative, not sharp','physical_gates':'HOLD','paid_compute':False,'n5_production':False,'external_replication':False}
    outputs={'full_system.json':{'labels':['a','b','c','d','e','f','g','h','i','j'],'relation':sorted(R),'global_coefficients':[[x,y,b] for (x,y),b in K.items()],'symbolic_checks':checks,'sample_equations':snapshots},'exclusion_certificates.json':{'P_nonzero':'first norms force e=g; Cj=1+(w-7v/2)^2+63v^2/4','P_zero':'gamma>0; t>9gamma; if s>0, norm equality forces gamma>s and v>8s; hence t+w>7v','norm_lower_bound':'1+87v^2/32','not_sharp':True,'equal_first_clock_controls':equal},'conditional_controls.json':{'interpretation':'These are exact partial-constraint witnesses, not full stationary solutions','exceptional_witnesses':witnesses,'inherited_clock_only_witness':{'T':oldT,'norms':oldC,'clock_gradient':oldq},'negative_controls':negative},'verification.json':summary}
    for name,data in outputs.items():(out/name).write_text(json.dumps(enc(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'results')
