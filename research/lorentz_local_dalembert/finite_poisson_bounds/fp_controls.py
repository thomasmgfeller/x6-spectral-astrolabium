"""Nonexperimental checks of bounds, probability inversion and exact algebra.
SPDX-License-Identifier: Apache-2.0
"""
import math
import numpy as np
from scipy.stats import poisson
from fp_common import HERE,F,count_box,cube_bounds,confidence_bound,read,save
from fp_bound import Bound

def controls():
    results=[]
    def check(name,passed,detail):
        assert passed,name
        results.append(dict(name=name,passed=bool(passed),detail=detail))
    for x in [F(0),F(1),F(2),F(1,10**40),F(10**30,7)]:
        lo,hi=cube_bounds(x);assert lo**3<=x<=hi**3
    check('directed_cube_enclosures',True,5)
    check('zero_count_exact_tail_interval',count_box(0)==(F(0),F(12)),['0','12'])
    # Enumeration is a numerical sanity check, not the coverage proof.
    worst=0.
    for mu in [.1,1,8,32,128,1000]:
        stop=int(poisson.ppf(1-1e-14,mu));miss=poisson.sf(stop,mu)
        for n in range(stop+1):
            lo,hi=count_box(n)
            if not float(lo)<=mu<=float(hi):miss+=poisson.pmf(n,mu)
        assert miss<=2*math.exp(-12)+1e-12
        worst=max(worst,float(miss))
    check('marginal_tail_enumeration',True,dict(maximum_failure=worst,union_single=2*math.exp(-12)))
    check('family_union_bound',confidence_bound(1736)<F(1,20),str(confidence_bound(1736)))
    # Synthetic exact-geometry fixture; no real source outcomes are inspected.
    rng=np.random.default_rng(782101)
    anchors=np.array([[0,0,0],[-3,0,0],[-5,1,0],[-7,.2,1.]])
    support=np.column_stack((np.r_[-2.,2.,rng.uniform(-2,-1,5),rng.uniform(1,2,5)],rng.uniform(-.4,.4,(12,2))))
    z=np.vstack((anchors,[-1.,.1,.2],support))
    nodes=list(range(len(z)));pairs=[[i,j] for i in nodes for j in nodes if i<j and (i<4 or j<4)]
    p=dict(landmarks=[0,1,2,3],root=4,support=list(range(5,len(z))),pairs=pairs,scale=.2)
    from fp_common import interval
    zz=[[F(f'{v:.12f}') for v in row] for row in z]
    q=[interval(zz,a,b) for a,b in pairs]
    box=[(v-F(1,10**5),v+F(1,10**5)) for v in q]
    bound=Bound(p,list(range(len(pairs))),z,box)
    finite=bound.evaluate(20)
    check('finite_radius_contraction',finite['status']=='FINITE_BOUND' and finite.get('ten_percent_certified',False),finite)
    from fp_common import normup
    # Check actual finite perturbation in q, recomputing the original intrinsic solve.
    import sys
    from inference import four_geometry
    qq=np.array(list(map(float,q)));pert=qq+np.linspace(-1,1,len(q))*1e-5/2**20
    def weights(qvalues):
        h,v,_,tm=four_geometry(qvalues,p);v=v[5:];t,x,y=v.T
        D=np.array([t,x,y,t*t,x*x,y*y,t*x,t*y,x*y]);H=np.eye(len(v))+np.ones((len(v),len(v)))
        K=np.block([[H,D.T],[D,np.zeros((9,9))]])
        sol=np.linalg.solve(K,np.r_[np.zeros(len(v)),tm@qvalues]);a=sol[:len(v)]
        return np.r_[-a.sum(),a]/p['scale']**2
    actual=float(np.linalg.norm(weights(pert)-weights(qq)))
    check('finite_difference_below_certificate',actual<=float(finite['absolute_error_upper']),dict(actual=actual,upper=finite['absolute_error_upper']))
    # Deliberately enormous uncertainty must not be declared certified.
    huge=Bound(p,list(range(len(pairs))),z,[(v-1000,v+1000) for v in q],pivots=bound.pivots).evaluate(0)
    check('uncertain_rank_abstains',huge['status']=='NO_CONTRACTION_CERTIFICATE',huge['status'])
    return dict(status='PASS',checks=results,scope='Synthetic numerical sanity checks plus exact algebra; statistical coverage is proved analytically.')

if __name__=='__main__':
    result=controls();save(HERE/'controls.json',result);print('PASS',len(result['checks']),'controls')
