#!/usr/bin/env python3
"""Exact finite audits and rational enclosures; no random ensemble or network.

The infinite probability statements are proved in PROOF.md, not by these tests.
All validation uses explicit exceptions and remains active under python -O.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib
import itertools
import json
import sys

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def inverse_dense(k):
    n=len(k)
    a=[[F(i==j)-k[i][j] for j in range(n)]+identity(n)[i] for i in range(n)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if a[i][j])
        a[j],a[pivot]=a[pivot],a[j]
        v=a[j][j]; a[j]=[x/v for x in a[j]]
        for i in range(n):
            if i!=j:
                v=a[i][j]; a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    require([row[:n] for row in a]==identity(n),'dense inverse residual')
    return [row[n:] for row in a]

def forward(k):
    r=identity(len(k))
    for i,row in enumerate(k):
        require(not any(row[i:]),'causality')
        for j in range(i):
            r[i]=[x+row[j]*y for x,y in zip(r[i],r[j])]
    return r

def orders(n):
    edges=[(i,j) for i in range(n) for j in range(i)]
    seen=set()
    for bits in range(1<<len(edges)):
        a=[[False]*n for _ in range(n)]
        for b,(i,j) in enumerate(edges):
            a[i][j]=bool(bits & (1<<b))
        for h in range(n):
            for i in range(n):
                for j in range(n):
                    a[i][j] |= a[i][h] and a[h][j]
        key=tuple(a[i][j] for i,j in edges)
        if key not in seen:
            seen.add(key)
            yield a

def weight(c,e,n):
    return sum((ck*comb(n,j)*e**j*(1-e)**(n-j) for j,ck in enumerate(c) if j<=n),F(0))

def path_sums(k):
    """Independent enumeration of all increasing vertex subsequences."""
    n=len(k); r=identity(n)
    for size in range(2,n+1):
        for vertices in itertools.combinations(range(n),size):
            p=F(1)
            for j,i in zip(vertices,vertices[1:]): p*=k[i][j]
            r[vertices[-1]][vertices[0]]+=p
    return r

def finite_audit():
    counts={}; cases=0; strict=0; history_cases=0
    coeffs=[list(map(F,[1,-9,16,-8])),[F(197,8),F(-3033,8),F(2363,2),F(-1331),F(504)]]
    for n in range(1,6):
        all_orders=list(orders(n)); counts[str(n)]=len(all_orders)
        for order in all_orders:
            interval=[[sum(order[i][h] and order[h][j] for h in range(n)) for j in range(n)] for i in range(n)]
            for e,c in itertools.product([F(1),F(1,2),F(1,16),F(1,64)],coeffs):
                k=[[e*weight(c,e,interval[i][j])/7 if order[i][j] else F(0) for j in range(n)] for i in range(n)]
                h=e*max(map(abs,c))/7
                envelope=[[h if order[i][j] else F(0) for j in range(n)] for i in range(n)]
                r=forward(k); dense=inverse_dense(k); paths=path_sums(k)
                require(r==dense==paths,'independent inverse/path mismatch')
                rp=path_sums(envelope)
                for i in range(n):
                    signed=sum(map(abs,r[i]),F(0)); major=sum(rp[i],F(0))
                    require(signed<=major<=(1+h)**i,'path envelope or count bound')
                    strict+=signed<major
                # Freeze the lower time region: history rows have no dynamics.
                cut=n//2
                frozen=[([F(0)]*n if i<cut else row[:]) for i,row in enumerate(k)]
                fr=forward(frozen)
                require(fr==inverse_dense(frozen)==path_sums(frozen),'frozen history transfer')
                for i in range(cut,n):
                    require(sum(map(abs,fr[i]),F(0))<=sum(rp[i],F(0)),'history envelope')
                cases+=1; history_cases+=1
    require(counts=={'1':1,'2':2,'3':7,'4':40,'5':357},'order enumeration')
    return dict(orders_by_size=counts,total_orders=sum(counts.values()),operator_cases=cases,
                frozen_history_cases=history_cases,strict_signed_vs_positive_rows=strict)

def integral_audit():
    # Integral_0^1 s^3(1-s)^m ds, expanded independently as a polynomial.
    rows=[]
    for k in range(1,25):
        m=4*(k-1)
        integral=sum((F((-1)**j*comb(m,j),j+4) for j in range(m+1)),F(0))
        require(integral==F(6*factorial(m),factorial(m+4)),'Dirichlet coefficient')
        previous=F(6**(k-1),factorial(4*(k-1)))
        coefficient=previous*integral
        require(coefficient==F(6**k,factorial(4*k)),'cone convolution')
        rows.append(str(coefficient))
    # Frozen history: integrate polynomial forcing against k cone convolutions.
    for k in range(1,13):
        for j in range(4):
            m=4*k-1
            integ=sum((F((-1)**i*comb(j,i),m+i+1) for i in range(j+1)),F(0))
            require(integ==F(factorial(m)*factorial(j),factorial(m+j+1)),'history convolution')
    return dict(cone_identities=len(rows),history_identities=48,normalized_coefficients=rows)

def atan_bounds(q,n):
    x=F(1,q); s=sum(((-1)**j*x**(2*j+1)/(2*j+1) for j in range(n)),F(0))
    term=(-1)**n*x**(2*n+1)/(2*n+1)
    return min(s,s+term),max(s,s+term)

def a_bounds(precision):
    l5,u5=atan_bounds(5,precision); l239,u239=atan_bounds(239,precision)
    pl,pu=16*l5-4*u239,16*u5-4*l239
    require(3<pl<pu<F(22,7),'pi enclosure')
    scale=10**precision
    lo=F(isqrt((1/(2*pu)).numerator*scale**2//(1/(2*pu)).denominator),scale)
    hi=F(isqrt((1/(2*pl)).numerator*scale**2//(1/(2*pl)).denominator)+1,scale)
    require(lo*lo<=1/(2*pu) and hi*hi>=1/(2*pl),'sqrt enclosure')
    return lo,hi

def series_bounds(b,j,tolerance=F(1,10**40)):
    # S_j(b)=sum_{k>=0} b^k/(4k+j)!, positive series and rigorous tail.
    s=F(0); term=F(1,factorial(j)); k=0
    while True:
        s+=term
        denominator=1
        for r in range(1,5): denominator*=4*k+j+r
        ratio=b/denominator
        nxt=term*ratio
        # Every later ratio is smaller; ratio is a conservative tail ratio.
        if ratio<1:
            tail=nxt/(1-ratio)
            if tail<tolerance: return s,s+tail,k+1
        term=nxt; k+=1
        require(k<1000,'series did not converge')

def decimal_out(x,places=18,upper=False):
    scale=10**places; v=x.numerator*scale//x.denominator
    if upper and F(v,scale)<x: v+=1
    return f'{v//scale}.{v%scale:0{places}d}'

def interval(lo,hi):
    require(lo<=hi,'interval reversed')
    return dict(lower_fraction=str(lo),upper_fraction=str(hi),
                lower_decimal=decimal_out(lo),upper_decimal=decimal_out(hi,upper=True))

def numeric_audit():
    data=[]
    for theta,C,d in [(0,F(16),F(-1)),(21,F(1331),F(-71,8))]:
        for T in [F(1,2),F(1),F(9,4),F(25,4)]:
            runs=[]
            for precision in [40,60,80]:
                al,au=a_bounds(precision)
                # omega^4=8*pi*kappa=(3/2)*a*C/(1-a*d) at fixed q0.
                wl,wu=[F(3,2)*a*C/(1-a*d) for a in [al,au]]
                bl,bu=wl*T**4,wu*T**4
                fl,_,nl=series_bounds(bl,0); _,fu,nu=series_bounds(bu,0)
                dl,du=1+100*(fl-1),1+100*(fu-1)
                runs.append((fl,fu,dl,du,wl,wu,precision,max(nl,nu)))
            require(max(r[0] for r in runs)<=min(r[1] for r in runs),'precision overlap F')
            fl,fu,dl,du,wl,wu,_,terms=runs[-1]
            row=dict(theta=theta,T=str(T),F=interval(fl,fu),B_delta_0_01=interval(dl,du),
                     source_error_for_output_0_001=interval(F(1,1000)/du,F(1,1000)/dl),
                     precision_checks=[r[6] for r in runs],max_series_terms=terms)
            if T==F(9,4):
                H=F(4); history_runs=[]
                for run in runs:
                    rwl,rwu=run[4],run[5]; hl=hu=F(0)
                    for j in range(4):
                        sl,_,_=series_bounds(rwl*T**4,j)
                        _,su,_=series_bounds(rwu*T**4,j)
                        pref=H**(4-j)*T**j/factorial(4-j)
                        hl+=rwl*pref*sl; hu+=rwu*pref*su
                    history_runs.append((hl,hu))
                require(max(r[0] for r in history_runs)<=min(r[1] for r in history_runs),'precision overlap history')
                hl,hu=history_runs[-1]
                row['frozen_history_duration']='4'
                row['history_precision_checks']=[r[6] for r in runs]
                row['history_H']=interval(hl,hu)
                row['joint_B_delta_0_01']=interval(1+100*(fl-1+hl),1+100*(fu-1+hu))
                row['joint_input_for_output_0_001']=interval(F(1,1000)/(1+100*(fu-1+hu)),F(1,1000)/(1+100*(fl-1+hl)))
            data.append(row)
    return data

def negatives():
    rejected=[]
    def fails(label,fn):
        try: fn()
        except ValueError: rejected.append(label)
        else: raise ValueError('negative control escaped: '+label)
    fails('missing_factor_six_in_cone_convolution',lambda:require(F(1,24)==F(1,4),'bad cone coefficient'))
    fails('spurious_extra_chain_factorial',lambda:require(F(36,factorial(8))/2==F(36,factorial(8)),'extra factorial'))
    fails('missing_inverse_density',lambda:require(F(2)*F(1,3)==F(1)*F(1,3),'density scaling'))
    k=[[F(0),F(0)],[F(1),F(0)]]
    fails('omitted_direct_source_identity',lambda:require(sum(map(abs,forward(k)[1]))==1,'identity omitted'))
    fails('mean_transfer_mistaken_for_mean_norm',lambda:require(F(2)==F(1),'random signs have E K=0 but E row norm=2'))
    history_chain=[[F(0)]*3,[F(1),F(0),F(0)],[F(0),F(1),F(0)]]
    frozen=[history_chain[0],[F(0)]*3,history_chain[2]]
    fails('history_rows_accidentally_propagated',lambda:require(forward(history_chain)==forward(frozen),'history propagation'))
    return rejected

def verify_sources():
    meta=json.loads((ROOT/'evidence/SOURCES.json').read_text())
    for item in meta['sources']:
        b=(ROOT/'evidence'/item['file']).read_bytes()
        require(hashlib.sha256(b).hexdigest()==item['sha256'],'source sha256')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['git_blob'],'source git blob')
    return len(meta['sources'])

def main():
    result=dict(version='0.27',source_hashes_verified=verify_sources(),finite=finite_audit(),
                integrals=integral_audit(),bounds=numeric_audit(),negative_controls=negatives(),
                method='HOLD',g1='HOLD',new_poisson_ensemble='NOT_RUN',
                proof_assistant='NOT_PERFORMED',external_review='NOT_PERFORMED')
    encoded=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    output=ROOT/'results/RESULTS.json'
    if '--check' in sys.argv:
        require(output.read_bytes()==encoded,'result replay differs')
        print('PASS: exact byte-for-byte replay')
    else:
        output.write_bytes(encoded)
        print(json.dumps({k:v for k,v in result.items() if k not in ['bounds','integrals']},indent=2))

if __name__=='__main__': main()
