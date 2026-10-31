#!/usr/bin/env python3
"""Exact smoothed-kernel envelopes and inherited finite-time budgets.

No new random cloud, fit or network request. Explicit exceptions work under -O.
The general arguments and scope are in PROOF.md.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import sys

ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise ValueError(message)

def verify_sources():
    meta=json.loads((ROOT/'evidence/SOURCES.json').read_text())
    for item in meta['sources']:
        b=(ROOT/'evidence'/item['file']).read_bytes()
        require(hashlib.sha256(b).hexdigest()==item['sha256'],'source SHA256: '+item['file'])
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['git_blob'],'source Git blob')
    return len(meta['sources'])

verify_sources()
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('baseline_v027',ROOT/'evidence/reproduce_v027.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

COEFFS={0:list(map(F,[1,-9,16,-8])),21:[F(197,8),F(-3033,8),F(2363,2),F(-1331),F(504)]}
DIAGONAL={0:F(-1),21:F(-71,8)}

def weight(c,e,n,absolute=False):
    return sum(((abs(v) if absolute else v)*comb(n,k)*e**k*(1-e)**(n-k)
                for k,v in enumerate(c) if k<=n),F(0))

def polynomial_weight(c,e,n):
    require(0<e<1,'polynomial form needs 0<epsilon<1')
    # Build falling-factorial polynomials by convolution, then use Horner.
    polynomial=[F(0)]*len(c); falling=[F(1)]
    for k,ck in enumerate(c):
        scale=ck*(e/(1-e))**k/factorial(k)
        for j,a in enumerate(falling): polynomial[j]+=scale*a
        nxt=[F(0)]*(len(falling)+1)
        for j,a in enumerate(falling): nxt[j]-=k*a;nxt[j+1]+=a
        falling=nxt
    value=F(0)
    for a in reversed(polynomial):value=value*n+a
    return (1-e)**n*value

def certify(c,e):
    require(0<e<1 and any(c),'nontrivial finite smoothed kernel')
    d=len(c)-1; probs=[F(1)]+[F(0)]*d
    best=F(0); indices=[]; values=[]
    for n in range(10000):
        recursive=sum((ck*pk for ck,pk in zip(c,probs)),F(0))
        direct=weight(c,e,n); polynomial=polynomial_weight(c,e,n)
        require(recursive==direct==polynomial,'weight representations differ')
        values.append(direct)
        if abs(direct)>best:best=abs(direct);indices=[n]
        elif abs(direct)==best:indices.append(n)
        tail=sum((abs(ck)*pk for ck,pk in zip(c,probs)),F(0))
        if n>=d and e*(n+1)>=d and tail<best:
            ratios=[(1-e)*F(n+1,n+1-k) for k in range(d+1)]
            require(max(ratios)<=1,'tail terms are not monotone')
            # Directly check several post-cutoff weights as an implementation audit.
            for m in [n+1,n+2,n+17,2*n+1]:
                require(abs(weight(c,e,m))<=weight(c,e,m,True)<=tail,'tail audit')
            return dict(epsilon=str(e),rho_floor_multiple=str(F(1,16)/e),
                        maximum=str(best),maximum_decimal=base.decimal_out(best),
                        maximizers=indices,weights_at_maximizers=[str(values[j]) for j in indices],
                        cutoff=n,tail_upper=str(tail),tail_upper_decimal=base.decimal_out(tail,upper=True),
                        max_tail_ratio=str(max(ratios)),checked_integer_weights=n+1)
        probs=[(1-e)*probs[k]+(e*probs[k-1] if k else 0) for k in range(d+1)]
    raise ValueError('certificate cutoff budget exceeded')

def semigroup_audit():
    count=0
    for c,e,p,n in itertools.product(COEFFS.values(),[F(1,16),F(1,32),F(1,64)],
                                    [F(1),F(1,2),F(2,3),F(3,7)],list(range(25))+[48,101]):
        nested=sum((comb(n,m)*p**m*(1-p)**(n-m)*weight(c,e,m) for m in range(n+1)),F(0))
        require(nested==weight(c,p*e,n),'binomial composition identity')
        count+=1
    return count

def graph_audit(certificates):
    maxima={int(item['theta']):F(item['maximum']) for item in certificates if item['epsilon']=='1/16'}
    counts=0; frozen_count=0
    for n in range(1,6):
        for order in base.orders(n):
            intervals=[[sum(order[i][h] and order[h][j] for h in range(n)) for j in range(n)] for i in range(n)]
            for theta,e in itertools.product(COEFFS,[F(1,16),F(1,32),F(1,64)]):
                c=COEFFS[theta];cap=e*maxima[theta]/7
                k=[[e*weight(c,e,intervals[i][j])/7 if order[i][j] else F(0) for j in range(n)] for i in range(n)]
                envelope=[[cap if order[i][j] else F(0) for j in range(n)] for i in range(n)]
                r=base.forward(k)
                require(r==base.inverse_dense(k)==base.path_sums(k),'response methods differ')
                major=base.forward(envelope)
                for i in range(n):
                    require(sum(map(abs,r[i]),F(0))<=sum(major[i],F(0)),'refined graph envelope')
                cut=n//2; frozen=[[F(0)]*n if i<cut else row[:] for i,row in enumerate(k)]
                fr=base.forward(frozen)
                require(fr==base.inverse_dense(frozen)==base.path_sums(frozen),'history response differs')
                for i in range(cut,n):
                    require(sum(map(abs,fr[i]),F(0))<=sum(major[i],F(0)),'frozen graph envelope')
                counts+=1;frozen_count+=1
    return dict(operator_cases=counts,frozen_history_cases=frozen_count)

def rounded_interval(lo,hi,places=30):
    require(lo<=hi,'reversed interval');scale=10**places
    lower=F(lo.numerator*scale//lo.denominator,scale)
    upper=F(-((-hi.numerator*scale)//hi.denominator),scale)
    require(lower<=lo<=hi<=upper,'outward rounding')
    return dict(lower_fraction=str(lower),upper_fraction=str(upper),
                lower_decimal=base.decimal_out(lower,places),upper_decimal=base.decimal_out(upper,places,True))

def interval_value(c,d,precision):
    al,au=base.a_bounds(precision);T=F(9,4);H=F(4)
    wl,wu=[F(3,2)*a*c/(1-a*d) for a in [al,au]]
    fl,_,_=base.series_bounds(wl*T**4,0,F(1,10**45))
    _,fu,_=base.series_bounds(wu*T**4,0,F(1,10**45))
    hl=hu=F(0)
    for j in range(4):
        sl,_,_=base.series_bounds(wl*T**4,j,F(1,10**45))
        _,su,_=base.series_bounds(wu*T**4,j,F(1,10**45))
        pref=H**(4-j)*T**j/factorial(4-j)
        hl+=wl*pref*sl;hu+=wu*pref*su
    ba=(1+100*(fl-1),1+100*(fu-1))
    bj=(1+100*(fl-1+hl),1+100*(fu-1+hu))
    return dict(F=(fl,fu),history_H=(hl,hu),B_active=ba,B_joint=bj,
                eta_active=(F(1,1000)/ba[1],F(1,1000)/ba[0]),
                eta_joint=(F(1,1000)/bj[1],F(1,1000)/bj[0]))

def budget_audit(certificates):
    rows=[];raw={}
    for theta in COEFFS:
        variants=[('v027_raw_coefficients',max(map(abs,COEFFS[theta]))),('c0_method_floor',abs(COEFFS[theta][0]))]
        variants += [('smoothed_'+c['epsilon'],F(c['maximum'])) for c in certificates if c['theta']==theta]
        for label,C in variants:
            runs=[interval_value(C,DIAGONAL[theta],p) for p in [40,60,80]]
            for key in runs[0]:
                require(max(r[key][0] for r in runs)<=min(r[key][1] for r in runs),'precision intervals fail overlap')
            raw[theta,label]=runs[-1]
            rows.append(dict(theta=theta,kind=label,C=str(C),precision_checks=[40,60,80],
                             **{key:rounded_interval(*value) for key,value in runs[-1].items()}))
    old=json.loads((ROOT/'evidence/RESULTS_v027.json').read_text())
    for oldrow in old['bounds']:
        if oldrow['T']!='9/4':continue
        ours=raw[oldrow['theta'],'v027_raw_coefficients']
        for oldkey,newkey in [('F','F'),('history_H','history_H'),('B_delta_0_01','B_active'),('joint_B_delta_0_01','B_joint')]:
            lo,hi=ours[newkey];a=F(oldrow[oldkey]['lower_fraction']);b=F(oldrow[oldkey]['upper_fraction'])
            require(max(lo,a)<=min(hi,b),'inherited budget mismatch')
    ratios=[]
    for theta in COEFFS:
        prior=raw[theta,'v027_raw_coefficients'];updated=raw[theta,'smoothed_1/16']
        ratios.append(dict(theta=theta,**{key:rounded_interval(prior[key][0]/updated[key][1],prior[key][1]/updated[key][0])
                                         for key in ['B_active','B_joint']}))
    return rows,ratios

def negative_controls(certificates):
    rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label)
        else:raise ValueError('negative control escaped: '+label)
    c=COEFFS[21];s=F(next(v['maximum'] for v in certificates if v['theta']==21 and v['epsilon']=='1/16'))
    reject('c0_is_not_the_global_maximum',lambda:require(abs(weight(c,F(1,16),5))<=abs(c[0]),'c0 misses negative maximum'))
    reject('refined_envelope_not_valid_below_density_floor',lambda:require(abs(weight(c,F(1),3))<=s,'rho=q violates refined cap'))
    p=F(1,2);e=F(1,16);n=7
    nested=sum((comb(n,m)*p**m*(1-p)**(n-m)*weight(c,e,m) for m in range(n+1)),F(0))
    reject('wrong_thinning_parameter',lambda:require(nested==weight(c,e/p,n),'use product, not quotient'))
    early=max(abs(weight(c,F(1,64),n)) for n in range(51))
    reject('finite_scan_misses_late_peak',lambda:require(abs(weight(c,F(1,64),101))<=early,'late peak'))
    reject('density_alone_does_not_zero_the_entry_envelope',lambda:require(abs(weight(c,F(1,10**6),0))<=F(1,1000),'c0 persists'))
    reject('tail_cut_before_monotonicity_threshold',lambda:require(F(1,16)*(5+1)>=len(c)-1,'tail not monotone'))
    return rejected

def main():
    certificates=[dict(theta=theta,**certify(c,F(1,den))) for theta,c in COEFFS.items() for den in [16,32,64]]
    for theta in COEFFS:
        seq=[F(c['maximum']) for c in certificates if c['theta']==theta]
        require(seq[0]>=seq[1]>=seq[2]>=abs(COEFFS[theta][0]),'sup norm contraction')
    rows,ratios=budget_audit(certificates)
    result=dict(version='0.28',date='2026-11-01',base_commit='63c8be4df882316a7629907a5da3ee012e47e309',
                sources_verified=verify_sources(),certificates=certificates,
                total_integer_weights=sum(c['checked_integer_weights'] for c in certificates),
                semigroup_checks=semigroup_audit(),graph_checks=graph_audit(certificates),
                budgets=rows,improvement_ratios=ratios,negative_controls=negative_controls(certificates),
                scope=dict(q='3/(16*pi)',rho_floor='3/pi',T='9/4',H='4',delta='1/100',output_budget='1/1000'),
                method='HOLD',g1='HOLD',new_random_clouds=0,
                interpretation='smaller sufficient upper bounds, not measured error reduction')
    b=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode();out=ROOT/'results/RESULTS.json'
    if '--check' in sys.argv:
        require(out.read_bytes()==b,'byte replay mismatch');print('PASS: v0.28 exact byte-for-byte replay')
    else:
        out.write_bytes(b)
        print(json.dumps({k:result[k] for k in ['sources_verified','total_integer_weights','semigroup_checks','graph_checks','negative_controls','method','g1']},indent=2))

if __name__=='__main__':main()
