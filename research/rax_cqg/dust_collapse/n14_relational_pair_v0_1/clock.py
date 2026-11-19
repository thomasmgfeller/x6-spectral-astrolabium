"""N14 packet contractions with independent Gauss panels for the two minimal clocks.

Adapted from history_measure_state_space_v0_1/response.py. The root axes now have
their own nodes and weights, and right before summation the first-release classes
are separated. The other four clocks retain their full uniform measure.
"""
import ctypes as ct
from itertools import combinations, product
from pathlib import Path
import subprocess
import numpy as np

BASE = Path(__file__).resolve().parent
INNER = (4, 5, 6, 11, 12, 13)
PAST, FUTURE = (0, 1, 2, 3), (7, 8, 9, 10)
BETA = 4 / np.sqrt(6)
STEP = np.sqrt(2 / (19*BETA))
RHO = np.array([1/8, 1/4])
MASKS = (1790, 5374)
CUTS = (0., .25)


def native(tmp):
    target = Path(tmp)/'tail.so'
    subprocess.run(['cc','-O3','-std=c99','-ffp-contract=off','-fPIC','-shared',
                    str(BASE/'inputs/contraction.c'),'-lm','-o',str(target)], check=True)
    lib = ct.CDLL(str(target))
    real = np.ctypeslib.ndpointer(dtype='float64', flags='C_CONTIGUOUS')
    complex_ = np.ctypeslib.ndpointer(dtype='complex128', flags='C_CONTIGUOUS')
    lib.tail.argtypes = [ct.c_int,ct.c_int,real,complex_,complex_,real,complex_,complex_]
    lib.tail.restype = None
    return lib


def layout(mask):
    pairs = set(combinations(PAST, 2)) | set(combinations(FUTURE, 2))
    pairs.update(product(PAST, INNER + FUTURE))
    pairs.update(product(INNER, FUTURE))
    pairs.update(ij for k,ij in enumerate(combinations(INNER, 2)) if mask & (1 << k))
    minima = [j for j in INNER if not any((i,j) in pairs for i in INNER)]
    assert minima == [4,5]
    coeff = {}
    for i,j in sorted(pairs):
        length = sum((i,k) in pairs and (k,j) in pairs for k in range(14))
        coeff[i,j] = (1,-9,16,-8)[length] if length < 4 else 0
    gravity = 14 - sum(coeff.values())
    assert gravity == {1790:52, 5374:-32}[mask]
    return coeff, gravity


def panel_rule(n, cuts):
    """Split the normalized clock measure dT/3. Keep exactly n nodes per axis."""
    limits = np.array([-1.5, *cuts, 1.5])
    widths = np.diff(limits)
    if n < len(widths):
        raise ValueError('Too few nodes for the chosen cut partition')
    quota = (n-len(widths))*widths/3
    orders = 1 + np.floor(quota).astype(int)
    for j in np.argsort(-(quota-np.floor(quota)), kind='stable')[:n-orders.sum()]:
        orders[j] += 1
    nodes, weights = [], []
    for j,m in enumerate(orders):
        x,w = np.polynomial.legendre.leggauss(m)
        nodes.extend((limits[j]+limits[j+1]+x*widths[j])/2)
        weights.extend(w*widths[j]/6)
    return np.array(nodes), np.array(weights)


def density(c):
    return (1 + np.exp(-.25j*c)*np.sinc(c/(4*np.pi)))/2


def samples(mask, n, times, cuts, lib, bounds=None):
    coeff, gravity = layout(mask)
    axes = {j:panel_rule(n, cuts if j in (4,5) else ()) for j in INNER}
    if bounds:
        assert not cuts
        for j,(left,right) in bounds.items():
            x,w = axes[j]
            axes[j] = (left+right)/2+(right-left)*x/3, w*(right-left)/3
    fixed = {i:(i-5)*STEP for i in PAST+FUTURE}
    fixed[3] = times
    def collar(j):
        return 1+BETA/2*sum(v*(fixed[j]-fixed[i])**2 for (i,k),v in coeff.items()
                            if k==j and i in fixed)
    past = sum(collar(j) for j in PAST)
    overall = np.exp(1j*(gravity-sum(collar(j) for j in FUTURE)/16))
    base, unary, edge = {}, {}, {}
    for j,(x,w) in axes.items():
        base[j] = 1+BETA/2*sum(coeff[i,j]*(x-(times[:,None] if i==3 else fixed[i]))**2 for i in PAST)
        unary[j] = w*np.exp(-1j*BETA/32*sum(coeff[j,i]*(fixed[i]-x)**2 for i in FUTURE))
        for i in INNER:
            if coeff.get((i,j),0):
                edge[i,j] = BETA/2*coeff[i,j]*(axes[i][0][:,None]-x[None,:])**2

    # C tail reads (child, parent) axes, while prefix algebra uses (parent, child).
    def pack_tail(child, parents):
        table = np.ascontiguousarray([edge[i,child].T for i in parents])
        phase = np.exp(-.5j*table)
        def integrate(c):
            output = np.empty((n,)*len(parents), dtype=complex)
            lib.tail(n,len(parents),c,np.exp(-.5j*c),unary[child],table,phase,output)
            return output
        return integrate

    twins = (11,12) if mask == 1790 else (6,11)
    equal_twins = all(np.array_equal(left,right) for left,right in zip(axes[twins[0]],axes[twins[1]]))
    if mask == 1790:
        left_tail = pack_tail(11,[5,6])
        if not equal_twins:
            right_tail = pack_tail(12,[5,6])
    else:
        joint_tail = pack_tail(12,[5,6,11])

    roots4, roots5 = (unary[j]*density(base[j]) for j in (4,5))
    labels = np.searchsorted(cuts, axes[4][0])
    groups = np.zeros((len(times),len(cuts)+1), dtype=complex)
    for a in range(n):
        leaf13 = (unary[13]*density(base[13]+edge[4,13][a])).sum(axis=1)
        sibling = unary[6]*density(base[6][:,None,:]+edge[4,6][a]+edge[5,6])
        middle = np.empty_like(roots5)
        if mask == 1790:
            for k,c in enumerate(base[11]):
                left = left_tail(c+edge[4,11][a])
                right = left if equal_twins else right_tail(base[12][k]+edge[4,12][a])
                middle[k] = (sibling[k]*left*right).sum(axis=1)
        else:
            assert not coeff[3,12]
            joint = joint_tail(base[12][0]+edge[4,12][a])
            second = sibling if equal_twins else unary[11]*density(base[11][:,None,:]+edge[4,11][a]+edge[5,11])
            for b in range(n):
                f = sibling[:,b,:]
                middle[:,b] = ((f@joint[b])*second[:,b,:]).sum(axis=1)
        conditional = (roots4[:,a]*leaf13)[:,None]*roots5*middle
        first = np.minimum(labels[a],labels)
        for group in range(labels[a]+1):
            groups[:,group] += conditional[:,first==group].sum(axis=1)
    return past, overall[:,None]*groups


def cartesian(mask, n, times, cuts, lib=None, ideal_cut=None, bounds=None):
    """Independent full six-clock action; class assignment uses the released ideal."""
    coeff, gravity = layout(mask)
    fixed = {i:(i-5)*STEP for i in PAST+FUTURE}
    coord = dict(fixed)
    weights = 1.
    for pos,j in enumerate(INNER):
        x,w = panel_rule(n, cuts if j in (4,5) else ())
        if bounds and j in bounds:
            left,right = bounds[j]
            x,w = (left+right)/2+(right-left)*x/3, w*(right-left)/3
        shape = [1]*6
        shape[pos] = n
        coord[j] = x.reshape(shape)
        weights = weights*w.reshape(shape)
    release = {j:np.maximum.reduce(np.broadcast_arrays(coord[j], *[coord[i] for i in INNER if (i,j) in coeff]))
               for j in INNER}
    earliest = np.minimum.reduce(np.broadcast_arrays(*(release.values())))
    labels = np.searchsorted(cuts, earliest)
    if ideal_cut is None:
        classes = [labels==k for k in range(len(cuts)+1)]
    else:
        masks = sum((1 << k)*(release[j]<=ideal_cut) for k,j in enumerate(INNER))
        classes = [masks==code for code,_,_ in ideals(mask)]
    phases, rows = [], []
    def arg(j):
        return 1+BETA/2*sum(v*(coord[j]-coord[i])**2 for (i,k),v in coeff.items() if k==j and v)
    for t in times:
        coord[3] = t
        phases.append(sum(arg(j) for j in PAST))
        val = weights*np.exp(1j*(gravity-sum(arg(j) for j in FUTURE)/16))
        for j in INNER:
            val *= density(arg(j))
        rows.append([val[group].sum() for group in classes])
    return np.array(phases), np.array(rows)


def ideals(mask):
    coeff,_ = layout(mask)
    result = []
    parents = {j:{i for i in INNER if (i,j) in coeff} for j in INNER}
    for code in range(1<<len(INNER)):
        d = {j for k,j in enumerate(INNER) if code & (1<<k)}
        if all(parents[j]<=d for j in d):
            frontier = {j for j in INNER if j not in d and parents[j]<=d}
            result.append((code,d,frontier))
    return result


def packet(mask, n, m, cuts, lib, solver=samples, **kwargs):
    z,w = np.polynomial.legendre.leggauss(m)
    times = np.concatenate([-2*STEP+side/16+z/32 for side in (-1,1)])
    assert max(times)<0 and (7-5)*STEP>.25
    past, amp = solver(mask,n,times,cuts,lib,**kwargs)
    outer = (np.tile(w/2,2) * np.sinc(past/(64*np.pi))
             * np.exp(-.5j*RHO[:,None]*past))/np.sqrt(2*32*48)
    return outer@amp
