"""Clock-ideal amplitudes by positive rectangles and exact reference count laws."""
from itertools import combinations
from math import comb
from fractions import Fraction as Q
import numpy as np
from clock import INNER, CUTS, ideals, layout, packet


def rectangles(mask, n, m, threshold, lib):
    rows = []
    for _,d,frontier in ideals(mask):
        limits = {j:(-1.5,threshold) for j in d}
        limits.update({j:(threshold,1.5) for j in frontier})
        rows.append(packet(mask,n,m,(),lib,bounds=limits)[:,0])
    return np.array(rows).T


def exact_count(mask):
    """Count directly by low raw marks, independently of the rectangles."""
    coeff,_ = layout(mask)
    cases = ideals(mask)
    hist = np.zeros((7,7),dtype=int)
    for low_size in range(7):
        for subset in combinations(INNER,low_size):
            low = set(subset)
            d = {j for j in low if all(i in low for i in INNER if (i,j) in coeff)}
            matching = [members for _,members,frontier in cases if members<=low and not frontier&low]
            assert matching == [d]
            hist[len(d),low_size] += 1
    assert np.array_equal(hist.sum(axis=0),[comb(6,k) for k in range(7)])
    out = {}
    for t in CUTS:
        p = (Q(t)+Q(3,2))/3
        masses = [sum(int(n)*p**k*(1-p)**(6-k) for k,n in enumerate(row)) for row in hist]
        assert sum(masses)==1
        out[str(t)] = [str(mass) for mass in masses]
    return hist.tolist(),out


def reference_transport(mask):
    """Exact tower on ideal states only, under independent uniform raw marks."""
    from itertools import product
    from sympy import Matrix, Rational, zeros
    thresholds = (Q(0),Q(1,4),Q(3,8))
    cases = ideals(mask)
    index = {code:i for i,(code,_,_) in enumerate(cases)}
    pred = {j:{i for i in INNER if (i,j) in layout(mask)[0]} for j in INNER}
    def code(low):
        return sum(1<<k for k,j in enumerate(INNER) if j in low and pred[j]<=low)
    def kernel(s,t):
        p,q = ((v+Q(3,2))/3 for v in (s,t))
        weights = (p,q-p,1-q)
        joint = zeros(len(cases))
        for region in product(range(3),repeat=6):
            a=code({j for j,k in zip(INNER,region) if k==0})
            b=code({j for j,k in zip(INNER,region) if k<2})
            prob=weights[0]**region.count(0)*weights[1]**region.count(1)*weights[2]**region.count(2)
            joint[index[a],index[b]] += Rational(prob)
        marginal = joint*Matrix.ones(len(cases),1)
        for i,(_,d,f) in enumerate(cases):
            assert marginal[i] == p**len(d)*(1-p)**len(f)
        return Matrix(len(cases),len(cases),lambda i,j:joint[i,j]/marginal[i])
    a,b,c=thresholds
    direct=kernel(a,c)
    assert direct==kernel(a,b)*kernel(b,c)
    return {'thresholds':list(map(str,thresholds)), 'ideal_states':len(cases),
            'total_matrix_entries_checked':len(cases)**2,'maximum_exact_difference':'0'}
