"""Exact and numerical controls; no target outcomes tune acceptance gates."""
from fractions import Fraction as F
from decimal import Decimal
import math,random,json
from pathlib import Path
import numpy as np
import joint
from intervals import I,precision

def main():
    precision(60);checks=0
    def contains(z,f):
        nonlocal checks
        assert F(z.lo)<=f<=F(z.hi);checks+=1
    rng=random.Random(2026102706)
    for _ in range(200):
        a=F(rng.randint(-10000,10000),rng.randint(1,1000));b=F(rng.randint(1,10000),rng.randint(1,1000))
        x=I(a.numerator)/a.denominator;y=I(b.numerator)/b.denominator
        for z,f in [(x,a),(y,b),(x+y,a+b),(x-y,a-b),(x*y,a*b),(x/y,a/b),(-x,-a),(x.square(),a*a)]:contains(z,f)
        root=y.sqrt(); assert F(root.lo)**2<=b<=F(root.hi)**2;checks+=1
    contains(I(0).sqrt(),F(0));contains(I(-1,1).square(),F(0))
    e_lower=sum((F(24)**k/math.factorial(k) for k in range(101)),F(0))
    assert e_lower>20*2**30;checks+=1
    assert np.array_equal(joint.C@joint.TINV,np.eye(20,dtype=np.int64));checks+=1
    gs=json.loads((Path(__file__).resolve().parents[1]/'poisson_v0_2/geometries.json').read_text())
    for g in gs:
        ratios=[F(x) for x in g['atom_ratios']]
        cells=[ratios[k] for k in joint.KEEP]+[sum(ratios[k] for k in joint.MERGED)]
        for j,k in enumerate(joint.baseline.PRED):
            assert sum(int(joint.C[j,b])*cells[b] for b in range(20))==F(g['volume_ratios'][k]);checks+=1
    # Perfect-square interval counts yield a known exact rational q.
    g=gs[0];scale=160000
    signed=[F(x) for x in g['signed_intervals']]
    full=np.array([int((scale*s)**2) for s in signed],dtype=np.int64)
    assert all(F(int(full[k]))==(scale*s)**2 for k,s in enumerate(signed))
    y=joint.cells_from_counts(full)
    rigorous=joint.evaluate(y,True)
    target=scale*F(g['tau_squared'])
    assert F(Decimal(rigorous['qhat_lower']))<=target<=F(Decimal(rigorous['qhat_upper']));checks+=1
    assert rigorous['certified'];checks+=1
    # Separate finite-difference check of the joint first derivative.
    y=np.rint(joint.means_from_geometry(g)*268435456).astype(np.int64)
    analytic=np.array(joint.evaluate(y,diagnostics=True)['gradient'])
    def qpoint(v):
        obs=joint.C@v;s=np.zeros((1,21));s[0,joint.baseline.PRED]=-np.sqrt(obs)
        G,d=joint.baseline.build_system(s)
        return -d[0]@np.linalg.solve(G[0],d[0])
    numeric=[]
    for b in range(20):
        h=max(1.,abs(y[b])*1e-5);v=y.astype(float);v[b]+=h
        u=y.astype(float);u[b]-=h
        numeric.append((qpoint(v)-qpoint(u))/(2*h))
    relative=np.linalg.norm(analytic-numeric)/np.linalg.norm(analytic)
    assert relative<1e-5,relative;checks+=1
    return {'status':'PASS_CONTROLS','checks':checks,'interval_precision':60,
            'derivative_relative_norm_difference':float(relative),
            'exact_alpha_bound_lt_0_05':True,'alpha_upper_numeric':2**30*math.exp(-24)}

if __name__=='__main__':print(json.dumps(main(),indent=2))
