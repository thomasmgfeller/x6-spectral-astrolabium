"""Independent lens quadrature, symbolic moments, finite controls and full replay."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse
from fractions import Fraction as Q
from math import comb,isqrt,pi
from pathlib import Path
import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss
from common import kl,reference
from moments import rest_moment,radial_moment,profile_moment,wedge_bounds,certificate
from bounds import bennett_bounds,radius,confidence,THRESHOLD
from support import HERE,contract,read,dump,sources,digest,seed,geometry,relation_hash
from analysis import planning,analyze

def interval_integral(bottom,top,r,fn,order=24):
    # Direct intersection of two Euclidean balls at each conformal time.
    x,w=leggauss(order);breaks=[bottom,(bottom+top-r)/2,(bottom+top+r)/2,top];out=0.
    for lo,hi in zip(breaks,breaks[1:]):
        times=(hi-lo)*x/2+(hi+lo)/2;a=times-bottom;b=top-times
        if r==0:vol=4*pi*np.minimum(a,b)**3/3
        else:
            lens=pi*(a+b-r)**2*(r*r+2*r*(a+b)-3*(a-b)**2)/(12*r)
            vol=np.where(r<=np.abs(a-b),4*pi*np.minimum(a,b)**3/3,lens)
        out+=(hi-lo)/2*np.dot(w,vol*fn(times))
    return out

def direct_geometry(h,order):
    x,w=leggauss(order);z=0.;first=0.;second=0.
    for lo,hi in [(-.5,0.),(0.,.5)]:
        for t,wt in zip((hi-lo)*x/2+(hi+lo)/2,(hi-lo)*w/2):
            limit=.5-abs(t)
            for r,wr in zip(limit*(x+1)/2,limit*w/2):
                density=(1-h*t)**-4;weight=96*wt*wr*r*r*density
                fn=lambda u:(1-h*u)**-4
                numerator=(interval_integral(-.5,t,r,fn)+interval_integral(t,.5,r,fn))/(pi/24)
                z+=weight;first+=weight*numerator;second+=weight*numerator*numerator
    return dict(volume=z,probability=first/z**2,wedge=second/z**3)

def symbolic_checks():
    import sympy as s
    t,x=s.symbols('t x',real=True);checks=0
    for a,b in [(a,b) for a in range(4) for b in range(3)]:
        cap=s.Rational(1,2)-t
        ball=s.integrate(x**(2*b)*(cap*cap-x*x),(x,-cap,cap))
        result=48*s.integrate(t**(2*a)*ball,(t,0,s.Rational(1,2)))
        assert Q(int(s.numer(result)),int(s.denom(result)))==rest_moment(a,b)
        checks+=1
    for t,r in [(Q(-1,5),Q(1,7)),(Q(1,8),Q(1,4))]:
        for k in range(5):
            exact=sum(v*t**a*r**(2*b) for (a,b),v in profile_moment(k).items())
            numeric=(interval_integral(-.5,float(t),float(r),lambda u:u**k)+interval_integral(float(t),.5,float(r),lambda u:u**k))/(pi/24)
            assert abs(float(exact)-numeric)<2e-14
            checks+=1
    return checks

def controls():
    mp.mp.dps=200;real=lambda q:mp.mpf(q.numerator)/q.denominator
    v=Q(1,3000)
    for e in [Q(0),Q(1,10**6),Q(3,1000),Q(1,10),Q(1)]:
        lo,hi=bennett_bounds(e,v);true=(real(v)+real(e))*mp.log(1+real(e/v))-real(e)
        assert real(lo)<=true<=real(hi)
    e=radius(v,12345);true=(real(v)+real(e))*mp.log(1+real(e/v))-real(e)
    assert true>=real(THRESHOLD)/12345
    # Exact dependent binary kernel Xi Xj, N=8, M=64 independent clouds.
    n,m=8,64;kmax=comb(n,2);weights={comb(k,2):comb(n,k) for k in range(2,n+1)}
    weights[0]=1+n
    mean=sum(Q(k*w,2**n*kmax) for k,w in weights.items())
    variance=sum(Q(w,2**n)*(Q(k,kmax)-mean)**2 for k,w in weights.items())
    assert mean==Q(1,4)
    assert variance==(2*mean*(1-mean)+4*(n-2)*(Q(1,8)-mean*mean))/(n*(n-1))
    freq={0:1}
    for _ in range(m):
        nxt={}
        for total,frequency in freq.items():
            for k,w in weights.items():nxt[total+k]=nxt.get(total+k,0)+frequency*w
        freq=nxt
    correct=radius(variance,m)
    # Deliberately false pair independence, using M*choose(N,2) observations.
    square=THRESHOLD/(2*m*kmax);den=2**48;t=square*den*den;top=isqrt(t.numerator//t.denominator)
    if Q(top*top)<t:top+=1
    wrong=Q(top,den)
    coverage=lambda e:sum((Q(f,2**(n*m)) for total,f in freq.items() if abs(Q(total,m*kmax)-mean)<=e),Q(0))
    good,bad=coverage(correct),coverage(wrong)
    assert good>=Q(19,20) and bad<Q(19,20)
    rare_zero=Q(99,100)**256
    assert rare_zero>Q(1,20) # zero observed variance is not a zero population-variance certificate
    fake=radius(Q(9,100),100000)
    assert fake<Q(1,10) # repeated identical Bernoulli cloud gives 0% coverage if falsely iid
    for args in [(-1,128,1),(1.5,128,2),(0,1,1),(0,128,0)]:
        try:confidence(*args)
        except ValueError:pass
        else:raise AssertionError('invalid input accepted')
    return dict(exact_dependent_kernel_coverage=float(good),invalid_pair_independence_coverage=float(bad),
                naive_zero_variance_failure_lower=float(rare_zero),false_independent_cloud_coverage=0.,
                high_precision_bennett_checks=6)

def selftest():
    count=symbolic_checks();control=controls();off=direct_geometry(1/3,20);lo,hi=wedge_bounds(Q(1,3))
    assert float(lo)-2e-13<=off['wedge']<=float(hi)+2e-13
    print('PASS_VARIANCE_CONTROLS',flush=True)
    return dict(status='PASS_VARIANCE_CONTROLS',independent_symbolic_and_profile_checks=count,off_grid_lens=off,**control)

def geometry_audit():
    rows=[];v=Q(certificate()['uniform_variance_upper'])
    for text in contract()['quadrature_h']:
        h=Q(text);low=direct_geometry(float(h),20);high=direct_geometry(float(h),32)
        delta=max(abs(low[k]-high[k]) for k in high)
        assert delta<2e-12
        pl,pu=reference.probability(h);wl,wu=wedge_bounds(h)
        assert float(pl)-2e-13<=high['probability']<=float(pu)+2e-13
        assert float(wl)-2e-13<=high['wedge']<=float(wu)+2e-13
        p,w=high['probability'],high['wedge'];var=(2*p*(1-p)+4*126*(w-p*p))/(128*127)
        assert var<=float(v)+2e-13
        rows.append(dict(h=text,**high,variance=var,quadrature_difference=delta,
            analytical_wedge=[str(wl),str(wu)]))
    return dict(status='PASS_SEPARATE_LENS_QUADRATURE',rows=rows,
                claim='Floating quadrature cross-check; rational series and uniform tails supply the certificate')

def compare(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:compare(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):compare(x,y)
    elif isinstance(a,float):np.testing.assert_allclose(a,b,rtol=1e-12,atol=1e-14)
    else:assert a==b

def verify(out,replay=True):
    basic=selftest();audit=geometry_audit();execution=read(out/'execution.json')
    assert sources(execution['source_ref'])==execution['source_sha256']
    hashes=read(out/'hashes.json');assert sorted(p.name for p in out.iterdir())==sorted([*hashes,'hashes.json'])
    for name,expected in hashes.items():assert digest(out/name)==expected,name
    compare(certificate(),read(out/'mathematics.json'));plan=planning();compare(plan,read(out/'planning.json'))
    rows=[];replayed=0
    if plan['fresh_gate']:
        for j,cell in enumerate(contract()['fresh_cells']):
            all_counts=[]
            for begin in range(0,cell['clouds'],contract()['storage_block']):
                raw=np.load(out/f'raw-{j}-{begin}.npz',allow_pickle=False);counts=raw['c2']
                assert counts.shape==(min(contract()['storage_block'],cell['clouds']-begin),)
                assert np.issubdtype(counts.dtype,np.integer)
                if replay:
                    for i,count in enumerate(counts):
                        rng=np.random.Generator(np.random.PCG64(seed(f'holdout/h{j}/r{begin+i}')))
                        x,_=geometry.sample(rng,128,{'h':float(Q(cell['h']))})
                        c=geometry.flat_density_twin_relation(x,float(Q(cell['h'])))
                        assert relation_hash(c).encode()==raw['relation_sha256'][i]
                        assert np.count_nonzero(c)==count;replayed+=1
                all_counts.extend(counts)
            result=analyze(np.array(all_counts,dtype=np.int64),cell);compare(result,read(out/f'groups-{j}.json.gz'));rows.extend(result['rows'])
            print('verified h='+cell['h'],flush=True)
    summary=read(out/'summary.json');compare(rows,summary['rows']);assert summary['status']==plan['status']
    assert summary['fresh_clouds']==(sum(c['clouds'] for c in contract()['fresh_cells']) if plan['fresh_gate'] else 0)
    return dict(status='PASS_FULL_VARIANCE_REPLAY' if replay else 'PASS_ARCHIVE_VARIANCE_AUDIT',source_ref=execution['source_ref'],
                fresh_clouds_replayed=replayed,controls=basic,geometry_audit=audit,primary_status=plan['status'],
                external_review=False,external_replication=False,no_unadjusted_confidence_intersection=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true');p.add_argument('--input',type=Path,default=HERE/'results');p.add_argument('--archive-only',action='store_true');p.add_argument('--report',type=Path);a=p.parse_args()
    if a.selftest:selftest()
    else:
        result=verify(a.input,not a.archive_only)
        if a.report:dump(a.report,result)
        print(result['status'],flush=True)
