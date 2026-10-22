"""Independent dual identities, exact nonlinear points and rejection controls.
SPDX-License-Identifier: Apache-2.0
"""
from cb_run import *
from cs_exact import E

def contains(bounds,values):
    assert len(bounds)==len(values)
    assert all(F(a)<=v<=F(b) for (a,b),v in zip(bounds,values))

def audit():
    cert=read(HERE/'certificate.json');summary=read(HERE/'summary.json')
    c=read(HERE/'contract.json');w,z0=inputs();z=boosted(z0);scale=F(w['scale'])
    h=F(c['enclosing_poisson_budget'])/constant(w);M,S=matrices(z)
    b=list(map(F,[0,0,0,-2,2,2,0,0,0]));lam0=solve(S,b)
    Q=[[F(v) for v in row] for row in cert['inverse']]
    assert mm(Q,S)==[[F(int(i==j)) for j in range(9)] for i in range(9)]
    count=0
    for node in range(16):
        analytic,residual=derivatives(z,M,Q,lam0,node)
        for axis in range(3):
            dual=[[E(v,int(i==node+5 and k==axis)) for k,v in enumerate(row)] for i,row in enumerate(z)]
            _,Sd=matrices(dual);Sp=[[v.d for v in row] for row in Sd]
            assert analytic[axis]==mm(Q,Sp)
            assert residual[axis]==matvec(mm(Q,Sp),lam0)
            count+=1
    directions=[]
    for node in range(16):
        for axis in range(3):
            for sign in [-1,1]:
                d=[[F(0)]*3 for _ in range(16)];d[node][axis]=F(sign);directions.append(d)
        for sign in [-1,1]:
            d=[[F(0)]*3 for _ in range(16)];d[node]=[F(0),F(sign*3,5),F(sign*4,5)];directions.append(d)
    for seed in range(8):
        raw=[[((j*13+k*7+seed*5)%17)-8 for k in range(3)] for j in range(16)]
        denom=sum(abs(v) for row in raw for v in row)
        directions.append([[F(v,denom) for v in row] for row in raw])
    assert len(directions)==136
    max_gap=F(0);base=exact_weights(z,scale);norm=sqrt_bounds(sum(v*v for v in base))[0]
    for d in directions:
        # Axis and 3-4-5 cases have exact block budget 1; coordinated L1 <=1.
        if sum(v!=0 for row in d for v in row)<=2:
            budget=sum(abs(row[0])+sqrt_bounds(row[1]**2+row[2]**2)[0] for row in d)
        else:budget=sum(abs(v) for row in d for v in row)
        assert budget<=1
        zz=[row[:] for row in z]
        for j,row in enumerate(d):zz[j+5]=[v+h*a for v,a in zip(z[j+5],row)]
        mm0,ss=matrices(zz);lam=solve(ss,b);weights=exact_weights(zz,scale)
        contains(cert['multiplier_intervals'],lam);contains(cert['weight_intervals'],weights)
        K=[[F(v) for v in row] for row in cert['preconditioned_derivative_upper']]
        actual=mm(Q,ss)
        for i in range(9):
            for j in range(9):assert abs(actual[i][j]-int(i==j))<=h*K[i][j]
        residual=matvec(Q,[a-bb for a,bb in zip(matvec(ss,lam0),b)])
        assert all(abs(v)<=F(r) for v,r in zip(residual,cert['centered_residual_upper']))
        max_gap=max(max_gap,sqrt_bounds(sum((a-bb)**2 for a,bb in zip(weights,base)))[1]/norm)
    try:contains([['0','0']],[F(1)])
    except AssertionError:pass
    else:raise AssertionError('invalid enclosure accepted')
    try:verified_solve([[I(0)]],[I(1)],[[I(1)]])
    except AssertionError:pass
    else:raise AssertionError('singular system accepted')
    assert F(summary['symmetric_relative_gap_upper'])<F(1,5)
    return dict(status='PASS',exact_dual_derivative_checks=count,exact_nonlinear_points=len(directions),
       all_multiplier_weight_and_residual_enclosures=True,negative_controls=2,
       maximum_sample_base_relative_gap_upper=outward(max_gap)[1],
       scope='Arithmetic audit in a superset of admissible configurations; samples are not a proof of the uniform bound. The mean-value and contraction argument supplies that proof.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
