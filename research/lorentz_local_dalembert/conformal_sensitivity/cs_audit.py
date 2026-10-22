"""Independent rational controls for intervals, linear inclusion and sensitivity.
SPDX-License-Identifier: Apache-2.0
"""
from cs_run import *
from cs_exact import E
import random

def arithmetic_controls():
    rng=random.Random(97123);checks=0
    for _ in range(200):
        aa=sorted(F(rng.randint(-100,100),rng.randint(1,97)) for _ in range(2))
        bb=sorted(F(rng.randint(-100,100),rng.randint(1,97)) for _ in range(2))
        a,b=I(*aa),I(*bb)
        for x in [aa[0],sum(aa)/2,aa[1]]:
          for y in [bb[0],sum(bb)/2,bb[1]]:
            for interval,value in [(a+b,x+y),(a-b,x-y),(a*b,x*y)]:assert interval.contains(value);checks+=1
            if not b.lo<=0<=b.hi:assert (a/b).contains(x/y);checks+=1
    rejected=False
    try:I(-1,1).inv()
    except AssertionError:rejected=True
    assert rejected
    return checks

def linear_controls():
    A=[[I(F(19,10),F(21,10)),I(F(1,10))],[I(F(1,10)),I(F(29,10),F(31,10))]]
    b=[I(F(9,10),F(11,10)),I(F(19,10),F(21,10))]
    # Independent exact inverse of midpoint [2,.1;.1,3].
    det=F(599,100);Q=[[I(F(3)/det),I(-F(1,10)/det)],[I(-F(1,10)/det),I(F(2)/det)]]
    enclosure,_=verified_solve(A,b,Q);checks=0
    for a in [F(19,10),F(2),F(21,10)]:
      for d in [F(29,10),F(3),F(31,10)]:
       for v in [F(9,10),F(11,10)]:
        for u in [F(19,10),F(21,10)]:
            determinant=a*d-F(1,100)
            exact=[(d*v-F(1,10)*u)/determinant,(a*u-F(1,10)*v)/determinant]
            assert all(i.contains(x) for i,x in zip(enclosure,exact));checks+=1
    rejected=False
    try:verified_solve(A,b,[[I(0),I(0)],[I(0),I(0)]])
    except AssertionError:rejected=True
    assert rejected
    return checks

def audit():
    w,z0=inputs();z=boosted(z0);scale=F(w['scale']);base=exact_weights(z,scale);normbase=sqrt_bounds(sum(v*v for v in base))
    cells=read(HERE/'cells.json');summary=read(HERE/'summary.json');c=read(HERE/'contract.json')
    assert cells[0]['lo']==c['parameter_interval'][0] and cells[-1]['hi']==c['parameter_interval'][1]
    assert all(a['hi']==b['lo'] for a,b in zip(cells,cells[1:]))
    assert len(cells)==summary['covering_partition_cells']
    assert all(F(row['inverse_residual_upper'])<1 for row in cells)
    point_checks=0
    for index in [0,len(cells)//2,len(cells)-1]:
      row=cells[index]
      for k in [F(row['lo']),(F(row['lo'])+F(row['hi']))/2,F(row['hi'])]:
        M,S=design(z,E(k,1));A=[[v.v for v in r] for r in S];Ap=[[v.d for v in r] for r in S]
        lam=solve(A,[0,0,0,-2,2,2,0,0,0]);lp=solve(A,[-v for v in matvec(Ap,lam)])
        ww=weights_from(M,[E(v,d) for v,d in zip(lam,lp)],scale)
        zz,_=flow(z,k);assert [v.v for v in ww]==exact_weights(zz,scale)
        distance=sqrt_bounds(sum((v.v-b)**2 for v,b in zip(ww,base)))[1]/normbase[0]
        speed=sqrt_bounds(sum(v.d*v.d for v in ww))[1]/normbase[0]
        assert distance<=F(row['base_relative_gap_upper']) and speed<=F(row['relative_speed_upper']);point_checks+=1
    # Independent centered differences of exactly solved weights, not AD.
    h=F(1,10**6);plus=exact_weights(flow(z,h)[0],scale);minus=exact_weights(flow(z,-h)[0],scale)
    derivative=list(map(F,read(HERE/'local.json')['derivative']))
    diff=[(a-b)/(2*h)-d for a,b,d in zip(plus,minus,derivative)]
    error=sqrt_bounds(sum(v*v for v in diff))[1]/sqrt_bounds(sum(v*v for v in derivative))[0]
    assert error<F(1,10**8)
    return dict(status='PASS',rational_arithmetic_checks=arithmetic_controls(),cramer_linear_system_checks=linear_controls(),
      bad_preconditioner_and_zero_divisor_rejected=True,continuous_partition_no_gaps=True,
      exact_point_weight_and_derivative_checks=point_checks,independent_centered_difference_relative_error_upper=outward(error)[1],
      interpretation='Point checks and finite differences are controls; the continuum proof uses validated interval inclusion.')
if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
