#!/usr/bin/env python3
"""Exact fork/diamond interval bookkeeping and stationary certificates."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
from math import isqrt
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reference_action',ROOT/'inputs/reference_action.py')
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
N=7;ZERO=(0,)*N
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

class Dual:
    """Exact first derivative in the four independently varied outer clocks."""
    def __init__(self,v,d=None):self.v=v;self.d=tuple(d if d is not None else (F(0),)*4)
    @staticmethod
    def coerce(x):return x if isinstance(x,Dual)else Dual(x)
    def __add__(self,o):o=self.coerce(o);return Dual(self.v+o.v,[a+b for a,b in zip(self.d,o.d)])
    __radd__=__add__
    def __neg__(self):return Dual(-self.v,[-a for a in self.d])
    def __sub__(self,o):return self+-self.coerce(o)
    def __rsub__(self,o):return self.coerce(o)+-self
    def __mul__(self,o):o=self.coerce(o);return Dual(self.v*o.v,[a*o.v+self.v*b for a,b in zip(self.d,o.d)])
    __rmul__=__mul__
    def __truediv__(self,o):o=self.coerce(o);return Dual(self.v/o.v,[(a*o.v-self.v*b)/(o.v*o.v)for a,b in zip(self.d,o.d)])
    def __rtruediv__(self,o):return self.coerce(o)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        out=Dual(1)
        for _ in range(n):out=out*self
        return out

def geometries():
    past=set(combinations(range(4),2))
    fork=frozenset(past|{(a,b)for a in range(4)for b in (4,5)})
    diamond=frozenset(set(fork)|{(a,6)for a in range(6)})
    return fork,diamond

def norm_scaled(K,j,Y,l2):return 1+l2*sum((b*(Y[j]-Y[i])**2 for (i,k),b in K.items()if k==j),F(0))/2
def inv(Y,l2=F(1)):
    a,b,c,d=Y;P=-8*a+16*b-9*c+d
    A=1+l2*(-8*a*a+16*b*b-9*c*c+d*d)/2
    return A,P

def symbolic_checks(K):
    times=[var(i)for i in range(7)];a,b,c,d,t1,t2,U=times
    sq=lambda x:mul(x,x)
    norms=[]
    for j in (4,5,6):
        p=const(1)
        for (i,k),beta in K.items():
            if k==j:p=add(p,scale(sq(add(times[j],scale(times[i],-1))),F(beta,2)))
        norms.append(p)
    P=add(scale(a,-8),scale(b,16),scale(c,-9),d)
    A=add(const(1),scale(add(scale(sq(a),-8),scale(sq(b),16),scale(sq(c),-9),sq(d)),F(1,2)))
    result=[]
    def eq(label,left,right):check(left==right,label);result.append(label)
    eq('fork norm one',norms[0],add(A,scale(mul(P,t1),-1)))
    eq('fork norm two',norms[1],add(A,scale(mul(P,t2),-1)))
    expected=add(const(1),scale(add(sq(add(U,scale(t1,-1))),sq(add(U,scale(t2,-1))),scale(sq(add(U,scale(d,-1))),16),scale(sq(add(U,scale(c,-1))),-8)),F(1,2)))
    eq('join norm with reclassified intervals',norms[2],expected)
    eq('first branch own derivative',diff(norms[0],4),scale(P,-1))
    eq('second branch own derivative',diff(norms[1],5),scale(P,-1))
    eq('join derivative in branch one',diff(norms[2],4),add(t1,scale(U,-1)))
    eq('join derivative in branch two',diff(norms[2],5),add(t2,scale(U,-1)))
    eq('join clock derivative',diff(norms[2],6),add(scale(U,10),scale(t1,-1),scale(t2,-1),scale(d,-16),scale(c,8)))
    eq('branch norm mismatch',add(norms[0],scale(norms[1],-1)),scale(mul(P,add(t1,scale(t2,-1))),-1))
    # Impose equality of incomparable scalar clocks, then the join clock equation.
    Ustar=scale(add(t1,scale(d,8),scale(c,-4)),F(1,5))
    joined=substitute(substitute(norms[2],5,t1),6,Ustar)
    h=add(t1,scale(d,-1));L=add(d,scale(c,-1))
    J=add(const(1),scale(add(sq(h),scale(mul(h,L),-2),scale(sq(L),-9)),F(4,5)))
    eq('reduced diamond compatibility',joined,J)
    return result

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    fork,diamond=geometries();Uf=frozenset(range(6));Ud=frozenset(range(7))
    Kf=ref.weights(fork,Uf);Kd=ref.weights(diamond,Ud)
    check((4,5)not in diamond and(5,4)not in diamond,'branches incomparable')
    join_coeff={i:b for (i,j),b in Kd.items()if j==6}
    check(join_coeff=={0:0,1:0,2:-8,3:16,4:1,5:1},'global join coefficients')
    syms=symbolic_checks(Kd)
    left=frozenset((0,1,2,3,4,6));right=frozenset((0,1,2,3,5,6));shared=left&right
    KL,KR,KS=[ref.weights(diamond,V)for V in (left,right,shared)]
    delta=ref.correction(Kd,KL,KR,KS)
    expected_delta={(0,6):-8,(1,6):32,(2,6):-49,(3,6):35}
    check({p:b for p,b in delta.items()if b}==expected_delta,'overlap correction table')
    grav=lambda V,K:len(V)-sum(K.values())
    gv=[grav(Ud,Kd),grav(left,KL),grav(right,KR),grav(shared,KS)]
    check(gv==[-4,5,5,4] and gv[0]-gv[1]-gv[2]+gv[3]==-10,'gravity correction')
    gluing=[]
    for slope,shift,w1,w2,r in product((F(1,3),F(1,2)),(F(-1,4),F(0)),(F(1,4),F(3,4)),(F(1,4),F(3,4)),(F(1,4),F(3,4))):
        T=tuple(shift+slope*i*i for i in range(7));ww=(F(0),)*4+(w1,w2,r)
        full=ref.action(Kd,Ud,T,ww)
        naive=ref.action(KL,left,T,ww)+ref.action(KR,right,T,ww)-ref.action(KS,shared,T,ww)
        dS=-sum((ww[j]*b*(T[j]-T[i])**2 for (i,j),b in delta.items()),F(0))/4
        check(full-naive==dS,'full overlap action')
        q,ql,qr,qs=[ref.grad(k,7,T,ww)for k in (Kd,KL,KR,KS)];dq=ref.grad(delta,7,T,ww)
        check(all(q[i]-ql[i]-qr[i]+qs[i]==dq[i]for i in range(7)),'full overlap reactions')
        gluing.append({'slope':slope,'shift':shift,'w1':w1,'w2':w2,'r':r,'delta_S':dS,'delta_q':dq})
    # Pure fork uses the old P=A=0 collar and independent incomparable clocks.
    old=(F(-5,2),F(-2),F(-4,3),F(0));fork_cases=[]
    check(inv(old)==(0,0),'inherited flat collar')
    for t1,t2,w1,w2 in product((F(1,4),F(1,2),F(3,4)),repeat=4):
        T=old+(t1,t2);ww=(F(0),)*4+(w1,w2);q=ref.grad(Kf,6,T,ww)
        check(ref.norm(Kf,4,T)==ref.norm(Kf,5,T)==q[4]==q[5]==0,'pure fork stationarity')
        fork_cases.append({'t1':t1,'t2':t2,'w1':w1,'w2':w2})
    # Construct complete-form diamond witnesses in T=L*Y coordinates.
    # L^2 is rational, Y belongs to one exact quadratic number field.
    shapes=[];family=[];excluded=[];mismatch=[];ad_count=0
    for p,X in product((F(1,4),F(1,2),F(3,4)),(F(1,2),F(1),F(2),F(3))):
        l2=5/(4*(10-p*p));hh=1-p;V=2-p+X
        rad=1/(4*l2)+2*V*V-F(9,8)*(2-p)**2+hh*hh/8
        check(rad>0,'positive radical')
        check(not(isqrt(rad.numerator)**2==rad.numerator and isqrt(rad.denominator)**2==rad.denominator),'nonsquare field')
        Z=Surd(0,1,rad);ell=Z-V;Phat=8*ell-8*X+1
        threshold_poly=2*X*X-X/2-F(7,64)-1/(4*l2)
        check(ell>0 and(Phat<0)==(threshold_poly>0),'ordered collar root and sign test')
        shapes.append({'p':p,'X':X,'L_squared':l2,'ell_over_L':ell,'P_over_L':Phat,'admissible':Phat<0})
        for sh in (F(-1,3),F(0),F(2,5)):
            d=Surd(sh,0,rad);c=d-1;b=c-X;a=b-ell;outer=(a,b,c,d)
            A,P=inv(outer,l2);tau=A/(l2*P);U=(tau+8*d-4*c)/5
            check(tau==d+hh and U-tau==F(4,5)*p,'parametric clocks')
            if Phat>=0:
                excluded.append({'p':p,'X':X,'shift_over_L':sh,'reason':'positive join would require negative branch density'});continue
            for r in (F(1,4),F(1,2),F(3,4)):
                w=-r*(U-tau)/P;check(0<w<1,'positive branch density within cap')
                Y=outer+(tau,tau,U);ww=(F(0),)*4+(w,w,r)
                check(a<b<c<d<tau<U,'causal inequalities')
                q=ref.grad(Kd,7,Y,ww)
                check(all(norm_scaled(Kd,j,Y,l2)==0 and q[j]==0 for j in (4,5,6)),'all diamond equations')
                check(q[0]==-8*w*(tau-a) and q[0]<0,'strict oldest outer reaction')
                check(sum(q)==0 and l2*sum((Y[i]*q[i]for i in range(7)),F(0))==2*w+r,'Ward and Euler balance')
                # Automatic differentiation through the original join row.
                Dy=[Dual(y,[F(i==j)for i in range(4)])for j,y in enumerate(outer)]
                Ad,Pd=inv(Dy,l2);td=Ad/(Pd*l2);Ud2=(td+8*Dy[3]-4*Dy[2])/5
                J=norm_scaled(Kd,6,Dy+[td,td,Ud2],l2)
                check(J.v==0 and J.d[0]>0,'rank-one compatibility derivative')
                check(all(q[i]==-r*J.d[i]/(2*l2)for i in range(4)),'independent conormal derivative');ad_count+=4
                for eps in (F(-1,1000),F(1,1000)):
                    YY=list(Y);YY[4]+=eps
                    c1,c2=norm_scaled(Kd,4,YY,l2),norm_scaled(Kd,5,YY,l2)
                    check(c1-c2==-l2*P*eps and c1!=c2,'branch time mismatch identity')
                    qw=ref.grad(Kd,7,YY,ww)
                    check(qw[4]-qw[5]==-r*eps/2,'branch response mismatch')
                    mismatch.append({'p':p,'X':X,'shift_over_L':sh,'r':r,'epsilon_over_L':eps,'C1_minus_C2':c1-c2})
                family.append({'p':p,'X':X,'shift_over_L':sh,'L_squared':l2,'Y_clocks':Y,'branch_density':w,'join_density':r,'q_outer_divided_by_L':q[:4],'J_derivatives_in_Y':J.d})
    # Chronology follows the partial order, not an artificial label sequence.
    neg=[]
    def reject(name,ok):check(ok,name);neg.append({'incorrect_assumption':name,'rejected':True})
    reject('two chain arms can be added without interval reclassification',any(row['delta_S']!=0 for row in gluing))
    reject('five common vertices imply zero overlap correction',len(shared)==5 and any(delta.values()))
    reject('incomparable branch clocks must be strictly ordered by label',all(z['Y_clocks'][4]==z['Y_clocks'][5]for z in family))
    reject('a pure fork forces its branch clocks equal',any(z['t1']!=z['t2']for z in fork_cases))
    TT=old+(F(1,4),F(1,2),F(3,4));ww=(F(0),)*4+(F(1,2),)*3;qq=ref.grad(Kd,7,TT,ww)
    reject('the flat fork collar can be rejoined with positive ordered matter',qq[4]>0 and qq[5]>0)
    reject('join-compatible norms alone guarantee positive weights',bool(excluded))
    reject('joint inner stationarity eliminates external reactions',all(z['q_outer_divided_by_L'][0]<0 for z in family))
    row=family[0];Y=row['Y_clocks'];w=row['branch_density'];r=row['join_density'];badw=(F(0),)*4+(w+F(1,1000),w,r);qbad=ref.grad(Kd,7,Y,badw)
    reject('branch densities remain independent after rejoining',qbad[4]!=0 and qbad[5]==0)
    # Necessary finite mismatch bounds tested without requiring a solution.
    budgets=0
    for row in family:
        Y=list(row['Y_clocks']);l2=row['L_squared'];w=row['branch_density'];r=row['join_density']
        for eps in (F(-1,1000),F(1,1000)):
            YY=list(Y);YY[4]+=eps;w1=w+F(1,2000);ww=(F(0),)*4+(w1,w,r)
            P=inv(YY[:4],l2)[1];cs=[norm_scaled(Kd,j,YY,l2)for j in (4,5)];q=ref.grad(Kd,7,YY,ww)
            check(l2*abs(P)*abs(YY[4]-YY[5])<=abs(cs[0])+abs(cs[1]),'finite clock mismatch budget')
            check(abs(P)*abs(w1-w)<=2*(abs(q[4])+abs(q[5]))+r*abs(YY[4]-YY[5]),'finite density mismatch budget');budgets+=1
    summary={'status':'PASS','symbolic_identities':len(syms),'gluing_cases':len(gluing),'gluing_reaction_components':7*len(gluing),'fork_stationary_cases':len(fork_cases),'diamond_shapes':len(shapes),'admissible_shapes':sum(x['admissible']for x in shapes),'excluded_shifted_collars':len(excluded),'diamond_stationary_cases':len(family),'automatic_boundary_derivatives':ad_count,'branch_time_perturbations':len(mismatch),'mismatch_budget_cases':budgets,'negative_controls':len(neg),'physical_gates':'HOLD','paid_compute':False,'n5_production':False,'external_replication':False}
    outputs={'intervals_and_gluing.json':{'fork_relation':sorted(fork),'diamond_relation':sorted(diamond),'join_coefficients':join_coeff,'delta_B':[[i,j,v]for(i,j),v in delta.items()if v],'gravity':[{'name':n,'F_g':v}for n,v in zip(('global','left_arm','right_arm','overlap'),gv)],'symbolic_checks':syms,'gluing_cases':gluing},'stationary_families.json':{'fork':fork_cases,'diamond_shapes':shapes,'diamond':family,'excluded':excluded},'perturbations_and_controls.json':{'branch_time_perturbations':mismatch,'finite_budget_cases':budgets,'negative_controls':neg},'verification.json':summary}
    for name,data in outputs.items():(out/name).write_text(json.dumps(enc(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main(Path(sys.argv[1])if len(sys.argv)>1 else ROOT/'results')

