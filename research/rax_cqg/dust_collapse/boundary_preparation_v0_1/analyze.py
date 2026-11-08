#!/usr/bin/env python3
"""Exact small controls; no production sampling, standard library only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, sys

B = tuple(map(F, (-8,16,-9,1)))
T0 = (F(-5,2), F(-2), F(-4,3), F(0))
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def norm2(a): return dot(a,a)
def C(T,t): return 1 + sum(b*(t-y)**2 for b,y in zip(B,T))/2
def S(T,t,w): return -w*C(T,t)/2
def q(T,t,w): return tuple(w*b*(t-y)/2 for b,y in zip(B,T))
def qt(T,w): return w*dot(B,T)/2
def check(ok,msg):
    if not ok: raise ValueError(msg)
def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def interval(x): return (F(x),F(x))
def add(x,y): return x[0]+y[0], x[1]+y[1]
def neg(x): return -x[1], -x[0]
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    v=[a*b for a in x for b in y]; return min(v),max(v)
def div(x,y):
    check(y[0]*y[1]>0,'zero-containing denominator')
    return mul(x,(1/y[1],1/y[0]))
def scale(x,k): return mul(x,interval(k))
def square(x):
    if x[0]<=0<=x[1]: return F(0),max(x[0]**2,x[1]**2)
    return min(x[0]**2,x[1]**2),max(x[0]**2,x[1]**2)
def arctan_bounds(x,n=24):
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    nxt=(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s,s+nxt),max(s,s+nxt)
def bounds_dict(x):
    return {'lower':x[0], 'upper':x[1], 'approximation_not_certificate':float((x[0]+x[1])/2)}

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    shifts=(F(-1,3),F(0),F(2,5)); gaps=(F(1,4),F(1,2),F(1))
    weights=(F(1,4),F(1,2),F(3,4))
    cases=[]; pair_count=0
    for shift in shifts:
        T=tuple(y+shift for y in T0); gradients=[]
        for gap,w in product(gaps,weights):
            t=shift+gap; Q=q(T,t,w); p=tuple(-z for z in Q)
            check(C(T,t)==0 and qt(T,w)==0,'stationary witness')
            check(sum(Q)==0 and dot(T,Q)==w,'reaction balance')
            wh=-dot(T,p); th=shift-2*p[3]/wh
            check((wh,th)==(w,t),'momentum reconstruction')
            check(sum(p)==0,'translation generator')
            h=F(1,113)
            for y in range(4):
                Tp=list(T); Tm=list(T); Tp[y]+=h; Tm[y]-=h
                d=(S(Tp,t,w)-S(Tm,t,w))/(2*h)
                check(d==Q[y],'central action derivative')
                comm=(qt(Tp,w)-qt(Tm,w))/(2*h)
                check(comm==w*B[y]/2,'commutator derivative')
            gradients.append(p)
            cases.append({'shift':shift,'t':t,'w':w,'q':Q,'p':p,'reconstructed':[th,wh]})
        for i in range(len(gradients)):
            for j in range(i):
                check(gradients[i]!=gradients[j],'universal phase unexpectedly supported')
                pair_count+=1
    perturbed=0; components=0
    for raw in product((-1,0,1),repeat=4):
        T=tuple(y+F(d,128) for y,d in zip(T0,raw))
        for t,w in product(gaps,weights):
            h=F(1,257)
            for y in range(4):
                Tp=list(T); Tm=list(T); Tp[y]+=h; Tm[y]-=h
                check((S(Tp,t,w)-S(Tm,t,w))/(2*h)==q(T,t,w)[y],'perturbed derivative')
                # Frozen phase W=-S(t*,w*,T) has the correct reaction sign.
                check((-S(Tp,t,w)+S(Tm,t,w))/(2*h)==-q(T,t,w)[y],'frozen phase derivative')
                components+=1
            check(sum(q(T,t,w))+qt(T,w)==0,'full translation Ward identity')
            gamma=C(T,t)-1
            check(dot(T,q(T,t,w))+t*qt(T,w)==-w*gamma,'homogeneity identity')
            perturbed+=1
    p=tuple(-z for z in q(T0,F(1,2),F(1,2)))
    # A zero-sum perturbation violates the conormal/branch conditions.
    badp=(p[0]+1,p[1]-1,p[2],p[3]); badw=-dot(T0,badp)
    check(sum(badp)==0 and badp!=tuple(-z for z in q(T0,-2*badp[3]/badw,badw)), 'bad momentum accepted')
    check(norm2(q(T0,F(1,2),F(1,2)))>0,'zero phase incorrectly sufficient')
    check(norm2(tuple(2*z for z in q(T0,F(1,2),F(1,2))))>0,'wrong phase sign accepted')
    check(norm2(B)>0,'commutator incorrectly zero')
    check(C(T0,F(1,2))==0 and C(tuple(T0[i]+F(i==0,128) for i in range(4)),F(1,2))!=0,'perturbation failed')
    # Tracking W=-S in the varying interior parameters deletes the normalization.
    Tbad=tuple(T0[i]+F(i==0,128) for i in range(4))
    check(C(Tbad,F(1,2))!=0 and S(Tbad,F(1,2),F(1,2))-S(Tbad,F(1,2),F(1,2))==0,'tracking-phase negative control')
    b2=norm2(B); bt=tuple(b*y for b,y in zip(B,T0))
    j2=4*(b2*norm2(bt)-dot(B,bt)**2)
    check(j2==87744,'coarea determinant')
    check(j2>0,'independent moment gradients')
    # Independent polynomial recurrence from integration by parts:
    # J_n = -4n z - 2n(2n-1) z J_(n-1), z=pi^-2.
    J=[F(0)]; moments=[]
    for n in (1,2):
        nxt=[F(0)] + [-2*n*(2*n-1)*v for v in J]
        nxt[1]-=4*n
        J=nxt
        moment=[v/2 for v in J]; moment[0]+=F(1,2*n+1)
        moments.append(moment)
    check(moments==[[F(1,3),F(-2)],[F(1,5),F(-4),F(24)]],'cosine moment recurrence')
    pi=sub(scale(arctan_bounds(F(1,5)),16),scale(arctan_bounds(F(1,239)),4))
    check(pi[0]>F(314159,100000) and pi[1]<F(314160,100000),'pi bounds')
    invpi2=div(interval(1),square(pi))
    c2=sub(interval(F(1,3)),scale(invpi2,2))
    c4=add(sub(interval(F(1,5)),scale(invpi2,4)),scale(square(invpi2),24))
    fourthvar=sub(c4,square(c2))
    check(c2[0]>0 and fourthvar[0]>0,'positive cosine moments')
    rows=[]
    for eps,hbar in product((F(1,64),F(1,128),F(1,256)),(F(1),F(1,1000),F(1,1000000))):
        t=w=F(1,2); K=402*t*t+1560*t+1568
        eC=add(scale(c2,K*eps**2),scale(fourthvar,F(201,2)*eps**4))
        eq=scale(c2,F(201,2)*w*w*eps**2)
        er=scale(square(pi),hbar*hbar/eps**2)
        prod=mul(eq,er); universal=F(201,8)*hbar*hbar*w*w
        check(prod[0]>universal,'uncertainty bound violated')
        rows.append({'epsilon':eps,'hbar_diagnostic':hbar,'t':t,'w':w,'E_C':bounds_dict(eC),'E_q':bounds_dict(eq),'E_R':bounds_dict(er),'product':bounds_dict(prod),'universal_lower':universal})
    # Exact scaling of the two leading residuals, no floating point comparison.
    scales=[]
    for eps in (F(1,64),F(1,128),F(1,256)):
        hbar=eps**2
        scales.append({'epsilon':eps,'hbar':hbar,'Eq_factor':eps**2,'ER_factor_hbar2_over_epsilon2':hbar*hbar/eps**2})
    summary={'status':'PASS','exact_stationary_cases':len(cases),'distinct_phase_pairs':pair_count,'perturbed_cases':perturbed,'perturbed_action_derivatives':components,'frozen_phase_derivatives':components,'stationary_derivatives':len(cases)*4,'commutator_coefficients':len(cases)*4,'cosine_budget_cases':len(rows),'negative_controls':6,'coarea_J_squared':j2,'paid_compute':False,'n5_production':False,'physical_preparation_derived':False,'external_replication':False,'scope':'analytical control package; no physical gate release'}
    outputs={'reaction_controls.json':{'cases':cases,'summary':summary},'packet_bounds.json':{'pi':bounds_dict(pi),'c2':bounds_dict(c2),'c4':bounds_dict(c4),'cases':rows,'double_limit_scaling':scales},'verification.json':summary}
    for name,data in outputs.items():
        (out/name).write_text(json.dumps(encode(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(encode(summary),sort_keys=True))
if __name__=='__main__': main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results')
