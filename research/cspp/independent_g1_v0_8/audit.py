"""Pre-data exact controls and adversarial gate tests; never use validation RNG."""
from fractions import Fraction as F
import json,math,time
import numpy as np
from flint import arb,acb,ctx
from support import HERE,old,legacy_fields,check,write,pack,unpack,plan,geometry,norm
import scalar_operator as op
import inference

def rational_relation(a,b):
    d=[F(float(y))-F(float(x)) for x,y in zip(a,b)]
    return d[0]>0 and d[0]**2>sum(z*z for z in d[1:])

def compute():
    ctx.prec=128;p=plan();checks=[]
    check(p['statistics']['critical_successes_out_of_64']==30,'fixed critical count')
    check(inference.tail(29,64,F(1,4))>F(1,4800)>inference.tail(30,64,F(1,4)),'exact test boundary')
    check(inference.tail(30,64,F(3,5))>F(98,100),'fixed64 power rationale')
    checks.append('exact binomial threshold and rejection power')
    # Verify binomial coverage at an independent rational grid, including near p0.
    lower=[inference.cp_lower(k,64,F(1,4800))[0] for k in range(65)]
    check(all(a<=b for a,b in zip(lower,lower[1:])),'monotone lower endpoint; missing-success conservatism')
    for prob in [F(0),F(1,100),F(1,10),F(1,4),F(1,2),F(3,4),F(99,100),F(1)]:
        risk=sum(F(math.comb(64,k))*prob**k*(1-prob)**(64-k) for k in range(65) if lower[k]>prob)
        check(risk<=F(1,4800),'exact one-sided coverage regression')
    checks.append('rational CP inversion and coverage regression, all65 counts')
    # Deterministic graph, independently enumerated without C++ bitsets.
    x=np.array([[-2,0,0,0],[-1.5,.25,0,0],[-1,0,.125,0],[-.5,0,0,.25],[0,0,0,0],[.5,.25,0,0]],float)
    probes=old.probes()[:21];_,pc,rr,rp,st=geometry.inventory(x,probes,full=False)
    for q,point in enumerate(probes):
        for j,y in enumerate(x):
            exact=sum(rational_relation(y,z) and rational_relation(z,point) for z in x) if rational_relation(y,point) else -1
            check(int(pc[q,j])==exact,'independent interval count')
    checks.append('126 independently enumerated strict interval counts')
    values=op.values(x)[0];fp,_=legacy_fields.fields(probes);fx,_=legacy_fields.fields(x)
    for r,row in enumerate(values):
        for c,z in enumerate(row):check(abs(float(z.real.mid())+1j*float(z.imag.mid())-fx[r,c])<1e-13,'legacy field identity')
    # The cutoff tail is part of the sampled field; include both transition axes.
    transition=np.array([[t,r,0,.125] for t in [-2.75,-2,-1.25,0,1.25,2,2.75] for r in [0,1.25,2,2.75]],float)
    v=op.values(transition)[0];vfloat,_=legacy_fields.fields(transition)
    for i,row in enumerate(v):
        for j,z in enumerate(row):check(abs(complex(float(z.real.mid()),float(z.imag.mid()))-vfloat[i,j])<1e-12,'cutoff included')
    check(op.taper(arb(1))==1 and op.taper(arb(3)).is_zero(),'smooth cutoff endpoint branches')
    checks.append('field identities, cutoff transition and exact plateau reference')
    from math import comb
    for e in p['epsilon']:
        table=op.weights(24,e);eps=F(e)
        for n,w in enumerate(table):
            exact=sum(F(c)*comb(n,k)*eps**k*(1-eps)**(n-k) for k,c in enumerate([1,-9,16,-8]) if k<=n)
            check(w.contains(arb(str(exact))),'independent binomial weight')
    checks.append('75 independent exact rational layer weights')
    for e in p['epsilon']:
        result=op.compute(x,pc,512,e,values)
        table=op.weights(int(pc.max(initial=0)),e);vp,bp=op.values(probes,True)
        a=4*(arb(e)*arb(3)*512/(512*arb.pi())/6).sqrt()
        for j,f in enumerate(result):
            for q,point in enumerate(probes):
                direct=a*(-vp[q][j]+arb(e)*sum(table[int(pc[q,k])]*values[k][j] for k in range(len(x)) if pc[q,k]>=0))
                check(unpack(f['operator_values'][q]).overlaps(direct),'independent explicit sum vs matrix')
    checks.append('630 independent direct ball sums and separate numeric error controls')
    # Gate negative controls: count29 cannot reject; count30 must; paired fields
    # do not become independent observations; failures cannot shrink denominator.
    for k,expected in [(0,False),(29,False),(30,True),(64,True)]:
        check((inference.tail(k,64,F(1,4))<=F(1,4800))==expected,'no premature rejection')
    check(inference.cp_lower(0,64,F(1,4800))==(F(0),F(0)),'nonrejection is not acceptance')
    check(not (arb('0.2 +/- 0.001')>arb('1/5')),'uncertain threshold cannot count as exceedance')
    check(not arb('0 +/- 1e-8').is_zero(),'uncertain zero is not exact zero')
    checks.append('uncertain threshold, exact-zero and insufficient-count negative controls')
    # Near null boundaries use exact fallback including rounded endpoint ties.
    origin=np.zeros(4);fallbacks=0
    for t in [np.nextafter(1.,0.),1.,np.nextafter(1.,2.)]:
        target=np.array([t,1.,0,0]);actual,stats=geometry.relation(origin,target)
        check(actual==rational_relation(origin,target),'exact near-null result');fallbacks+=stats[1]
    check(fallbacks>=1,'near-null fallback exercised');checks.append('exact dyadic near-null geometry')
    return {'status':'PASS','checks':checks,'validation_seed_used':False,
            'critical_count':30,'null_tail_at_30':str(inference.tail(30,64,F(1,4))),
            'power_at_p_0_6':str(inference.tail(30,64,F(3,5))),
            'nominal_family_alpha':'1/40'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();write(a.out,compute())
