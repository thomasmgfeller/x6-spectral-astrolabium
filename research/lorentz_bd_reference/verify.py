"""Algebraic controls, separate geometry predicate and deterministic evidence replay."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import binom
from core import contract, counts, weights, operator, curvature, sprinkle, seed, geometry, physical_volume, truth, forward_grid, reference
from analyze import group_result, gate
from continuum import mean_curvature
from run import frozen

def independent_counts(x):
    # Unsquared Euclidean norm and full rows; independent of sorted upper loop.
    result=[]
    for p in x:
        d=x-p
        result.append(np.count_nonzero(d[:,0]>np.linalg.norm(d[:,1:],axis=1)))
    return np.asarray(result,dtype=np.int64)

def selftest():
    from fractions import Fraction as Q
    np.testing.assert_array_equal(weights(np.arange(8),1.),[1,-9,16,-8,0,0,0,0])
    # Exact finite thinning expectation, independently summed via binomial PMF.
    for eps in [.025,.17,.6,1.]:
        for n in [0,1,2,3,4,11,50]:
            want=sum(c*binom.pmf(k,n,eps) for k,c in enumerate([1,-9,16,-8]))
            np.testing.assert_allclose(weights(np.array([n]),eps)[0],want,rtol=2e-13,atol=1e-13)
    # Poisson transform: E f(N,eps)=exp(-eps*v) P(eps*v).
    from scipy.stats import poisson
    for mu,eps in [(2.3,.17),(30.,.05),(100.,.2)]:
        n=np.arange(1000); xi=mu*eps
        got=np.dot(poisson.pmf(n,mu),weights(n,eps))
        want=np.exp(-xi)*(1-9*xi+8*xi**2-4*xi**3/3)
        np.testing.assert_allclose(got,want,atol=1e-12)
    x=np.array([[-.4,0,0,0],[-.2,0,0,0],[0,0,0,0],[.2,0,0,0]])
    np.testing.assert_array_equal(counts(x),[3,2,1,0])
    ns=counts(x); assert ns.sum()==6
    assert not np.isclose(operator(ns,100,.17),operator(ns+1,100,.17)), 'off-by-one negative control not detected'
    phi=np.array([.3,-.6,2,4.])
    assert np.isclose(operator(ns,100,.17,3*phi,6),3*operator(ns,100,.17,phi,2))
    assert np.isclose(operator(ns,1600,.17),4*operator(ns,100,.17))
    rng=np.random.default_rng(seed('selftest-only'))
    for h in [0.,.19,.37]:
        for i in range(12):
            x,_=sprinkle(rng,1400,h)
            np.testing.assert_array_equal(counts(x),independent_counts(x))
    # Spatial and temporal distribution of a separately generated large cloud.
    # Draw several clouds under the point guard rather than condition N.
    h=.37; clouds=[sprinkle(rng,30000,h)[0] for _ in range(16)]
    x=np.concatenate(clouds); eta=x[:,0]
    density=lambda t: (4*np.pi/3)*(.5-abs(t))**3/(1-h*t)**4
    v=geometry.oracle(h)['volume']
    mean=sum(quad(lambda t:t*density(t),a,b)[0] for a,b in [(-.5,0),(0,.5)])/v
    second=sum(quad(lambda t:t*t*density(t),a,b)[0] for a,b in [(-.5,0),(0,.5)])/v
    assert abs(eta.mean()-mean)<6*np.sqrt((second-mean*mean)/len(x))
    radial=(np.linalg.norm(x[:,1:],axis=1)/(.5-abs(eta)))**3
    assert abs(radial.mean()-.5)<6/np.sqrt(12*len(x))
    np.testing.assert_allclose(physical_volume(0),np.pi/24,atol=1e-14)
    p,q=forward_grid(); assert p[0]==.1 and q[0]==0
    # Check interpolation against exact rational enclosures at off-grid h.
    for hq in [Q(7,100),Q(19,100),Q(37,100)]:
        a,b=reference.probability(hq)
        from core import invert
        assert abs(float(invert(float((a+b)/2)))-truth(float(hq)))<1e-6
    for h in [0.,.37]:
        a=mean_curvature(h,1234,.17,48); b=mean_curvature(h,1234,.17,80)
        assert abs(a-b)<1e-7
    return dict(status='PASS',controls=['epsilon=1 layers','binomial thinning','Poisson transform','linearity','density scaling',
        'off-by-one rejection','36 independent causal predicates','volume-weighted time and radial sampling','C2 inversion','continuum quadrature'])

def verify_archive(folder, replay):
    for name,digest in json.loads((folder/'hashes.json').read_text()).items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest,name
    execution=json.loads((folder/'execution.json').read_text()); frozen(execution['source_ref'])
    assert execution['status']=='COMPLETE'
    c=contract(); selection=json.loads((folder/'selection.json').read_text())
    for row in selection['development']:
        a=np.load(folder/row['file']); mse=np.mean(a['bd'].reshape(-1,c['group_size'],4).mean(axis=1)**2,axis=0)
        np.testing.assert_array_equal(mse,row['group_mse'])
        assert int(np.argmin(mse))==selection['selected'][str(row['flat_expected_count'])]
    checked=0; independent=0
    for file in sorted(folder.glob('*.npz')):
        a=np.load(file); split,lam,hs=file.stem.split('-'); lam=int(lam); h=float(hs); rho=lam/(np.pi/24)
        for i in range(len(a['n'])):
            ns=a['interval_counts'][a['offsets'][i]:a['offsets'][i+1]]
            assert len(ns)==a['n'][i] and int(ns.sum())==a['c2'][i]
            assert hashlib.sha256(ns.tobytes()).hexdigest()==a['interval_hash'][i]
            np.testing.assert_array_equal([curvature(ns,rho,e) for e in c['epsilon_candidates']],a['bd'][i])
            if replay:
                rng=np.random.default_rng(seed(f'{split}/{lam}/{h:.8f}/{i}'))
                x,_=sprinkle(rng,rho,h)
                assert hashlib.sha256(x.tobytes()).hexdigest()==a['coordinate_hash'][i]
                np.testing.assert_array_equal(counts(x),ns)
                if i%64==0:
                    np.testing.assert_array_equal(independent_counts(x),ns); independent+=1
            checked+=1
    summary=json.loads((folder/'summary.json').read_text())
    for r in summary['rows']:
        a=np.load(folder/r['file']); j=selection['selected'][str(r['flat_expected_count'])]
        assert group_result(a['n'],a['c2'],a['bd'][:,j],r['h'])==r['metrics']
    assert gate(summary['rows'],all(r['poisson_control'] and r['continuum_control'] for r in summary['rows']))==summary['decision']
    return dict(status='PASS_FULL_REPLAY' if replay else 'PASS_ARCHIVE',clouds=checked,independent_predicate_clouds=independent,decision=summary['decision'])

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--archive',type=Path); p.add_argument('--replay',action='store_true'); args=p.parse_args()
    result={'selftest':selftest()}
    if args.archive: result['archive']=verify_archive(args.archive,args.replay)
    print(json.dumps(result,indent=2))
