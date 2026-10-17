"""Deterministic controls, permitted before the frozen target experiment."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
import sys
from pathlib import Path
import numpy as np
from core import coefficients, flat_probability, de_sitter_slope, overlap_weights, chain_sums, taylor_sums
from quadrature import pair_probability, volume
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'lorentz_curvature'))
from geometry import flat_points, relation


def execute():
    expected = [(Q(2,315), -Q(2,105), Q(1,90)),
                (Q(4,315), -Q(2,45), Q(1,42)),
                (Q(28,1485), -Q(4,55), Q(1,27))]
    for k, (a, b, ds) in zip(range(2,5), expected):
        assert coefficients(4,k)[2:] == (a,b)
        assert de_sitter_slope(k) == ds
    a2,b2 = coefficients(4,2)[2:]; a3,b3 = coefficients(4,3)[2:]
    assert a2*b3-a3*b2 == -Q(4,99225)
    for d in range(2,11):
        assert coefficients(d,1)[2:] == (0,0)
    assert np.allclose([flat_probability(4,k) for k in range(2,5)], [1/10,1/350,1/29400], rtol=0, atol=1e-17)
    # Exact covariance identity in a non-continuum model, independent of RSS.
    # iid uniform draws from a three-atom total order; coincident atoms are incomparable.
    covariance_checks = 0
    for n in [4,6]:
        rows = []
        for labels in product(range(3), repeat=n):
            rows.append([Q(sum(len(set(labels[i] for i in s)) == k for s in combinations(range(n),k)), comb(n,k)) for k in [2,3]])
        means = [sum(r[j] for r in rows)/len(rows) for j in range(2)]
        for i,k in enumerate([2,3]):
            for j,ell in enumerate([2,3]):
                covariance = sum((r[i]-means[i])*(r[j]-means[j]) for r in rows)/len(rows)
                weights = overlap_weights(n,k,ell)
                assert sum(weights) == 1
                predicted = Q(0)
                for s in range(1,min(k,ell)+1):
                    m = k+ell-s
                    joint = 0
                    for labels in product(range(3), repeat=m):
                        first = labels[:k]
                        second = labels[:s]+labels[k:]
                        joint += len(set(first)) == k and len(set(second)) == ell
                    predicted += weights[s]*(Q(joint,3**m)-means[i]*means[j])
                assert covariance == predicted
                covariance_checks += 1
    rng = np.random.Generator(np.random.PCG64(481516))
    checks = 0
    for case in range(12):
        x = flat_points(rng,9)
        x = x[np.argsort(x[:,0])]
        c = relation(x) if case < 10 else (np.triu(np.ones((9,9),bool),1) if case==10 else np.zeros((9,9),bool))
        w = rng.uniform(.2,2,(3,9))
        sums = chain_sums(c,w)
        counts = chain_sums(c)
        tay = taylor_sums(c,x[:,0])
        for j,k in enumerate(range(2,5)):
            subsets = [s for s in combinations(range(9),k) if all(c[s[a],s[b]] for a in range(k) for b in range(a+1,k))]
            ref = np.array([sum(np.prod(row[list(s)]) for s in subsets) for row in w])
            tref = sum(2*np.sum(x[list(s),0]**2)+8*np.sum(x[list(s),0])**2-k/6 for s in subsets)
            assert counts[j] == len(subsets)
            assert np.allclose(sums[:,j],ref,rtol=1e-12,atol=1e-12)
            assert abs(tay[j]-tref) < 1e-11
            checks += 1
        assert np.array_equal(chain_sums(c.T),counts)
    for order in [12,20,32]:
        assert abs(volume(0,order)-np.pi/24) < 1e-14
        assert abs(pair_probability(0,order)-.1) < 1e-14
    for args in [(1,2),(4,0),(4.0,2)]:
        try: coefficients(*args)
        except ValueError: pass
        else: raise AssertionError('invalid coefficients accepted')
    print({'status':'PASS_DETERMINISTIC_CONTROLS','exact_covariance_checks':covariance_checks,
           'brute_force_chain_checks':checks,'flat_quadrature_orders':[12,20,32]})


if __name__ == '__main__': execute()
