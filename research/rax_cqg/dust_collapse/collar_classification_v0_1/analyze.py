#!/usr/bin/env python3
"""Exact collar classification controls; standard library, no production integral."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from math import isqrt
import importlib.util, json, sys

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('inherited',ROOT/'inputs/two_block_analyze.py')
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
def check(ok,msg):
    if not ok:raise ValueError(msg)

class Surd:
    """a+b sqrt(d), d a positive nonsquare rational; exact signs."""
    def __init__(self,a=0,b=0,d=305):self.a,self.b,self.d=F(a),F(b),F(d)
    def coerce(self,o):
        if isinstance(o,Surd):
            if o.d==self.d:return o
            if not o.b:return Surd(o.a,0,self.d)
            raise ValueError('different quadratic fields')
        return Surd(o,0,self.d)
    def __add__(self,o):o=self.coerce(o);return Surd(self.a+o.a,self.b+o.b,self.d)
    __radd__=__add__
    def __neg__(self):return Surd(-self.a,-self.b,self.d)
    def __sub__(self,o):return self+-self.coerce(o)
    def __rsub__(self,o):return self.coerce(o)+-self
    def __mul__(self,o):o=self.coerce(o);return Surd(self.a*o.a+self.d*self.b*o.b,self.a*o.b+self.b*o.a,self.d)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.coerce(o);z=o.a*o.a-self.d*o.b*o.b
        if not z:raise ZeroDivisionError()
        return self*Surd(o.a/z,-o.b/z,self.d)
    def __rtruediv__(self,o):return self.coerce(o)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        z=Surd(1,0,self.d)
        for _ in range(n):z=z*self
        return z
    def __eq__(self,o):o=self.coerce(o);return self.a==o.a and self.b==o.b
    def sign(self):
        sa=(self.a>0)-(self.a<0);sb=(self.b>0)-(self.b<0)
        if not sb:return sa
        if not sa or sa==sb:return sb
        delta=self.a*self.a-self.d*self.b*self.b
        return sa*((delta>0)-(delta<0))
    def __lt__(self,o):return (self-o).sign()<0
    def __le__(self,o):return (self-o).sign()<=0
    def __gt__(self,o):return (self-o).sign()>0
    def __ge__(self,o):return (self-o).sign()>=0
    def __abs__(self):return self if self.sign()>=0 else -self
    def __bool__(self):return bool(self.a or self.b)

def enc(x):
    if isinstance(x,Surd):return {'a':str(x.a),'b':str(x.b),'sqrt_d':str(x.d)}
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

# Independent symbolic coefficient comparison in six formal clock variables.
N=6;ZERO=(0,)*N
def const(v):return {ZERO:F(v)} if v else {}
def var(i):e=list(ZERO);e[i]=1;return {tuple(e):F(1)}
def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items()if c}
def scale(p,k):return {e:c*k for e,c in p.items()if c*k}
def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            ef=tuple(a+b for a,b in zip(e,f));out[ef]=out.get(ef,F(0))+c*d
    return {e:c for e,c in out.items()if c}
def diff(p,i):
    out={}
    for e,c in p.items():
        if e[i]:f=list(e);f[i]-=1;out[tuple(f)]=e[i]*c
    return out
def substitute(p,i,value):
    out={}
    for e,c in p.items():
        f=list(e);power=f[i];f[i]=0;term={tuple(f):c}
        for _ in range(power):term=mul(term,value)
        out=add(out,term)
    return out

def invariants(T):
    a,b,c,d=T;P=-8*a+16*b-9*c+d
    ts=8*b-16*c+9*d
    A=1+(-8*a*a+16*b*b-9*c*c+d*d)/2
    D=1+(-8*b*b+16*c*c-9*d*d)/2
    E=D+ts*ts/2;H=A-P*ts
    x=c-b;s=b-2*c+d
    dE=(0,16*x+72*s,-16*x-144*s,72*s)
    dH=(8*(ts-a),16*(b-ts)-8*P,-9*(c-ts)+16*P,d-ts-9*P)
    return P,ts,E,H,dE,dH

def symbolic_checks():
    a,b,c,d,t,u=[var(i)for i in range(6)]
    sq=lambda p:mul(p,p)
    P=add(scale(a,-8),scale(b,16),scale(c,-9),d)
    ts=add(scale(b,8),scale(c,-16),scale(d,9))
    A=add(const(1),scale(add(scale(sq(a),-8),scale(sq(b),16),scale(sq(c),-9),sq(d)),F(1,2)))
    D=add(const(1),scale(add(scale(sq(b),-8),scale(sq(c),16),scale(sq(d),-9)),F(1,2)))
    cf=add(A,scale(mul(P,t),-1))
    cg=add(D,scale(sq(t),F(1,2)),scale(mul(add(t,scale(ts,-1)),u),-1))
    direct=[]
    for i in (4,5):
        times=[a,b,c,d,t,u];row=const(1)
        for j in range(i):
            k=i-j-1
            if k<4:row=add(row,scale(sq(add(times[i],scale(times[j],-1))),F(ref.B[k],2)))
        direct.append(row)
    checks=[]
    def eq(name,l,r):check(l==r,name);checks.append(name)
    eq('C_f from original interval coefficients',direct[0],cf)
    eq('C_g from original interval coefficients',direct[1],cg)
    eq('C_g derivative in u',diff(cg,5),scale(add(t,scale(ts,-1)),-1))
    E=add(D,scale(sq(ts),F(1,2)));H=add(A,scale(mul(P,ts),-1))
    eq('C_g at forced t_star',substitute(cg,4,ts),E)
    eq('C_f at forced t_star',substitute(cf,4,ts),H)
    x=add(c,scale(b,-1));s=add(b,scale(c,-2),d)
    eq('E in chronological gaps',E,add(const(1),scale(sq(x),-8),scale(sq(s),36)))
    eta=add(t,scale(ts,-1));g=add(u,scale(t,-1))
    eq('exact E residual identity',add(cg,mul(eta,g),scale(sq(eta),F(1,2))),E)
    eq('exact F residual identity',add(cf,mul(P,eta)),H)
    dE=[{},add(scale(x,16),scale(s,72)),add(scale(x,-16),scale(s,-144)),scale(s,72)]
    dH=[scale(add(ts,scale(a,-1)),8),add(scale(add(b,scale(ts,-1)),16),scale(P,-8)),add(scale(add(c,scale(ts,-1)),-9),scale(P,16)),add(d,scale(ts,-1),scale(P,-9))]
    for i in range(4):
        eq('E boundary derivative '+str(i),diff(E,i),dE[i])
        eq('F boundary derivative '+str(i),diff(H,i),dH[i])
    return checks

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    syms=symbolic_checks()
    U=frozenset(range(6));K=ref.weights(frozenset(combinations(range(6),2)),U)
    slopes=[F(1,2),F(3,5),F(5,8),F(2,3),F(7,10),F(3,4),F(1)]
    shifts=[F(-1,3),F(0),F(2,5)];dens=[F(1,4),F(1,2),F(3,4)]
    collars=[];cases=[];rejected=[];h=F(1,1024);derivative_count=0
    for m in slopes:
        dx=(3*m-2)/(2-9*m*m);x=F(1,2)+dx;s=F(1,6)+m*dx
        check(x>0 and s>0 and 8*x*x-36*s*s==1,'rational conic')
        rad=(71*x*x+414*x*s+559*s*s)/8
        check(rad>0 and isqrt(rad.numerator)**2!=rad.numerator or rad>0 and isqrt(rad.denominator)**2!=rad.denominator,'nonsquare radicand')
        Z=Surd(0,1,rad);z=Z-2*x-9*s
        check(z>0,'ordered older collar')
        sign_poly=39*x*x+46*x*s-569*s*s
        for shift in shifts:
            d=Surd(shift,0,rad);b=d-2*x-s;c=d-x-s;a=b-z;outer=(a,b,c,d)
            P,ts,E,H,dE,dH=invariants(outer)
            check(E==H==0 and ts>d,'parametric collar equations')
            check((P<0)==(sign_poly<0),'chronology discriminant')
            check(dH[0]>0 and dE[1]>0 and dE[0]==0,'rank-two boundary Jacobian')
            for i in range(4):
                Tp=list(outer);Tm=list(outer);Tp[i]+=h;Tm[i]-=h
                ip,im=invariants(Tp),invariants(Tm)
                check((ip[2]-im[2])/(2*h)==dE[i] and (ip[3]-im[3])/(2*h)==dH[i],'independent boundary derivative')
                derivative_count+=2
            row={'slope':m,'shift':shift,'x':x,'s':s,'z':z,'P':P,'t_star':ts,'admissible':P<0,'jacobian_rank':2}
            collars.append(row)
            if P>=0:rejected.append({'slope':m,'shift':shift,'reason':'u<=t for every positive w/v'});continue
            for w,v in product(dens,repeat=2):
                t=ts;u=t-w*P/v;T=outer+(t,u);ww=(F(0),)*4+(w,v)
                check(all(T[i]<T[i+1]for i in range(5)),'ordered six clocks')
                q=ref.grad(K,6,T,ww)
                check(ref.norm(K,4,T)==ref.norm(K,5,T)==q[4]==q[5]==0,'full joint equations')
                expected=[-w*f/2-v*e/2 for e,f in zip(dE,dH)]
                check(q[:4]==expected,'conormal outer reactions')
                check(q[0]==-4*w*(t-a) and q[0]<0,'strict outer reaction')
                check(sum(q)==0 and sum((T[i]*q[i]for i in range(6)),F(0))==w+v,'outer Ward and Euler identities')
                check(ref.rank([list(dE),list(dH)])==2,'independent row reduction')
                cases.append({'slope':m,'shift':shift,'w':w,'v':v,'T':T,'q_outer':q[:4]})
    # Independent coordinate perturbations of the previous exact witness.
    R=Surd(0,1,305);base=(-R/6,Surd(F(-5,2)),Surd(-2),Surd(F(-4,3)))
    epsilons=[F(-1,1000),F(-1,10000),F(-1,100000),F(1,100000),F(1,10000),F(1,1000)]
    perturb=[]
    for i,eps in product(range(4),epsilons):
        T=list(base);T[i]+=eps;P,ts,E,H,_,_=invariants(T)
        check(all(T[j]<T[j+1]for j in range(3))and ts>T[3] and P<0,'perturbations retain strict open inequalities')
        if i==0:check(E==0 and H==4*R*eps/3-4*eps*eps and H!=0,'a perturbation cannot be absorbed')
        else:
            coeff={1:(20,28),2:(-32,136),3:(12,36)}[i]
            check(E==coeff[0]*eps+coeff[1]*eps*eps and E!=0,'later perturbation cannot be absorbed')
        perturb.append({'clock':i,'epsilon':eps,'E':E,'F':H,'inner_readjustment_possible':False})
    # Budgets for approximate solutions, without any collar retuning.
    budgets=[];identity_count=0
    for z,x,y in product((F(1,4),F(1,2),F(3,4)),repeat=3):
        outer=(-x-y-z,-x-y,-y,F(0));P,ts,E,H,_,_=invariants(outer)
        for t,g,w,v in product((F(1,8),F(1,2)),(F(1,4),F(1)),(F(1,4),F(3,4)),(F(1,4),F(3,4))):
            u=t+g;T=outer+(t,u);ww=(F(0),)*4+(w,v)
            cf,cg=ref.norm(K,4,T),ref.norm(K,5,T);qu=ref.grad(K,6,T,ww)[5];eta=t-ts
            check(qu==v*eta/2 and E==cg+eta*g+eta*eta/2 and H==cf+P*eta,'off-surface residual identities')
            vmin=F(1,4);G=F(1)
            BE=abs(cg)+2*G*abs(qu)/vmin+2*qu*qu/(vmin*vmin)
            BF=abs(cf)+2*abs(P)*abs(qu)/vmin
            check(abs(E)<=BE and abs(H)<=BF,'finite residual bounds')
            identity_count+=3
            budgets.append({'outer':outer,'t':t,'gap':g,'w':w,'v':v,'E':E,'F':H,'C_f':cf,'C_g':cg,'q_u':qu,'E_bound':BE,'F_bound':BF})
    # Tangential data are correlated; translation is not arbitrary coordinate noise.
    tangent=[]
    for row in cases:
        T=row['T'];outer=T[:4];P,ts,E,H,_,_=invariants(outer)
        shift=F(1,1000);T2=tuple(v+shift for v in T);P2,t2,E2,H2,_,_=invariants(T2[:4])
        check(P2==P and E2==E and H2==H and t2-ts==shift,'translation preserves admissibility')
        tangent.append({'slope':row['slope'],'w':row['w'],'v':row['v'],'shift':shift})
    neg=[]
    def reject(label,condition):check(condition,label);neg.append({'incorrect_assumption':label,'rejected':True})
    reject('E=F=0 alone guarantees chronological positive future',bool(rejected))
    reject('all nearby independent collars have a readjusted solution',len(perturb)==24 and all(not x['inner_readjustment_possible']for x in perturb))
    reject('every perturbation destroys the solution',len(tangent)>0)
    reject('joint inner stationarity removes all outer forces',all(x['q_outer'][0]<0 for x in cases))
    # Clock gradients alone become small as the free density approaches zero.
    bad=(-F(5,2),F(-2),-F(4,3),F(0),F(1,4),F(1,2));ww=(F(0),)*4+(F(1,10**12),F(1,10**12))
    qq=ref.grad(K,6,bad,ww)
    reject('small weighted clock residuals certify density normalization',abs(qq[4])<F(1,10**9) and abs(qq[5])<F(1,10**9) and ref.norm(K,5,bad)!=0)
    reject('the conormal reaction has only one independent direction',all(x['jacobian_rank']==2 for x in collars))
    summary={'status':'PASS','symbolic_polynomial_identities':len(syms),'parametric_collars':len(collars),'admissible_collars':sum(x['admissible']for x in collars),'excluded_chronology_collars':len(rejected),'joint_stationary_cases':len(cases),'boundary_derivatives':derivative_count,'independent_perturbations':len(perturb),'budget_cases':len(budgets),'off_surface_identities':identity_count,'tangent_translations':len(tangent),'negative_controls':len(neg),'physical_gates':'HOLD','paid_compute':False,'n5_production':False,'external_replication':False}
    outputs={'classification.json':{'symbolic_checks':syms,'collars':collars,'stationary_cases':cases,'excluded':rejected},'perturbation_certificates.json':{'independent':perturb,'tangent_translation_count':len(tangent),'negative_controls':neg},'residual_budgets.json':{'v_min':F(1,4),'gap_cap':F(1),'cases':budgets},'verification.json':summary}
    for name,data in outputs.items():(out/name).write_text(json.dumps(enc(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main(Path(sys.argv[1])if len(sys.argv)>1 else ROOT/'results')
