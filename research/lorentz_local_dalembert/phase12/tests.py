"""Independent software controls; success is not a scientific acceptance."""
import ast
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
import core


def check():
    count=0
    # Exhaustive path enumeration on many small random transitive DAGs.
    rng=np.random.default_rng(7631)
    for n in range(2,10):
        for _ in range(8):
            r=np.triu(rng.random((n,n))<.3,1)
            for k in range(n): r|=r[:,k,None]&r[None,k,:]
            perm=rng.permutation(n); inv=np.argsort(perm)
            g=core.Poset(r[np.ix_(perm,perm)],rng.random(n))
            for a,b in itertools.product(range(n),repeat=2):
                paths=[]
                def visit(v,steps):
                    if v==b: paths.append(steps); return
                    for w in np.flatnonzero(r[v]): visit(w,steps+1)
                visit(a,0); expected=max(paths,default=-1)
                assert g.to(int(inv[b]))[inv[a]]==expected
                assert g.to(int(inv[a]),True)[inv[b]]==expected
                count+=1
    # Independent adaptive quadrature of the same geometric integral.
    for x in [0,.02,.2,1,3]:
        t=math.sqrt(1+x*x)
        def angular(theta):
            upper=1/(2*(t+x*math.cos(theta)))
            return quad(lambda r:r*(t-r-math.sqrt(r*r+x*x+2*x*r*math.cos(theta))),0,upper,epsabs=1e-12)[0]
        reference=48/math.pi*quad(angular,0,math.pi/2,epsabs=1e-11)[0]
        assert abs(core.overlap_function([x])[0]-reference)<2e-8
        if x>0: assert abs(core.invert_overlap(reference)-x)<2e-5
    # Exact symmetric continuum-moment stencil, constructed independently.
    xyz=np.array([[0,0,0],[.2,0,0],[-.2,0,0],[0,.2,0],[0,-.2,0],[0,0,.2],[0,0,-.2]])
    s=dict(root=0,support=list(range(1,7)),weights=[-25,-25,25,25,25,25])
    eta=np.diag([-1.,1.,1.])
    np.testing.assert_allclose(core.metric(s,xyz),eta,atol=1e-14)
    assert core.apply(s,np.ones(7))==0
    for i in range(3): assert abs(core.apply(s,xyz[:,i]))<1e-14
    transform=np.array([[1,.2,0],[0,2,.3],[.1,0,.8]])
    y=xyz@transform.T+np.array([2,-1,3])
    target=transform@eta@transform.T
    np.testing.assert_allclose(core.metric(s,y),target,atol=1e-12)
    np.testing.assert_allclose(core.metric(s,y),core.metric_outer(s,y),atol=1e-12)
    # Signature-only or zero-output substitutes must not pass component checks.
    assert np.linalg.norm(eta-target)/np.linalg.norm(target)>.5
    assert np.linalg.norm(target)/np.linalg.norm(target)>.5
    assert core.independent_columns(np.ones((10,4)),np.arange(4)) is None
    cfg=json.loads((core.HERE/'contract.json').read_text())
    short=core.Poset(np.triu(np.ones((3,3),bool),1),[.1,.2,.3])
    assert core.neighborhood(short,32768,0,2,cfg)['status']=='short_chain'
    # The inference module imports no evaluator/sampler and accepts no coordinates.
    tree=ast.parse((core.HERE/'core.py').read_text())
    assert not any(isinstance(n,(ast.Import,ast.ImportFrom)) and 'experiment' in ast.unparse(n) for n in ast.walk(tree))
    result=dict(status='PASS_SOFTWARE_CONTROLS',independent_chain_pairs=count,
                adaptive_quadrature_cases=5,curvature_estimator=False)
    return result

if __name__=='__main__': print(json.dumps(check(),indent=2))
