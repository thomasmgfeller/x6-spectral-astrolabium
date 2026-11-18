"""Gaussian quadrature of the unchanged clock action by exact factor elimination."""
from functools import cache
from itertools import permutations, product
import numpy as np
from orders import geometry, layout
from clocks import BETA, STEP, RHO, quadrature, density_factor


@cache
def scheme(key):
    inner, coeff, _ = layout(key)
    scopes = [frozenset((j, *(i for (i, k), b in coeff.items() if k == j and i in inner and b))) for j in inner]
    best = None
    for ordering in permutations(inner):
        active = list(scopes)
        widths = []
        for var in ordering:
            involved = [s for s in active if var in s]
            joint = frozenset().union(*involved)
            widths.append(len(joint))
            active = [s for s in active if var not in s] + [joint - {var}]
        score = (max(widths), sum(10**w for w in widths), ordering)
        if best is None or score < best:
            best = score
    return best[0], best[2]


def align(data, scope, joint):
    return np.reshape(data, [data.shape[scope.index(v)] if v in scope else 1 for v in joint])


def clock_value(key, t, n):
    inner, coeff, gravity = layout(key)
    p, f = geometry.P, geometry.F
    x, w = quadrature(n)
    grid = 1.5*x
    fixed = {i: (i-5)*STEP for i in (*p, *f)}
    fixed[3] = t
    def fixed_c(j):
        return 1 + BETA/2 * sum(b*(fixed[j]-fixed[i])**2 for (i,k),b in coeff.items() if k==j and i in fixed)
    past = sum(fixed_c(j) for j in p)
    overall = np.exp(1j*(gravity - sum(fixed_c(j) for j in f)/16))
    tensors = []
    for j in inner:
        scope = tuple(sorted([j] + [i for (i,k),b in coeff.items() if k==j and i in inner and b]))
        times = {i: align(grid, (i,), scope) for i in scope}
        c = 1
        for (i,k),b in coeff.items():
            if k==j and b:
                other = fixed[i] if i in fixed else times[i]
                c = c + BETA*b/2*(times[j]-other)**2
        unary = w * np.exp(-1j*BETA/32 * sum(coeff[j,k]*(fixed[k]-grid)**2 for k in f))
        tensors.append((scope, density_factor(c) * align(unary, (j,), scope)))
    for v in scheme(key)[1]:
        touching = [(s,a) for s,a in tensors if v in s]
        tensors = [(s,a) for s,a in tensors if v not in s]
        joint = tuple(sorted(set().union(*(s for s,a in touching))))
        merged = 1
        for s, a in touching:
            merged = merged * align(a, s, joint)
        tensors.append((tuple(i for i in joint if i != v), merged.sum(axis=joint.index(v))))
    return past, overall * np.prod([value for scope,value in tensors])


def cartesian(key, t, n):
    inner, coeff, gravity = layout(key)
    x, w = quadrature(n)
    times = {i:(i-5)*STEP for i in (*geometry.P, *geometry.F)}
    times[3] = t
    total = 0j
    for indices in product(range(n), repeat=len(inner)):
        times.update({j:1.5*x[k] for j,k in zip(inner,indices)})
        c = {j:1 + BETA/2*sum(b*(times[j]-times[i])**2 for (i,k),b in coeff.items() if k==j)
             for j in (*inner,*geometry.F)}
        total += np.prod(w[list(indices)]) * np.prod([density_factor(c[j]) for j in inner]) * np.exp(-1j*sum(c[j] for j in geometry.F)/16)
    return np.exp(1j*gravity)*total


def packet(key, n, m):
    x, w = quadrature(m)
    norm = np.sqrt(1/48/32)
    lobes, comp = [], []
    for sign in (-1, 1):
        rows = [clock_value(key, -2*STEP+sign/16+v/32, n) for v in x]
        phase, amp = np.array([z[0] for z in rows]), np.array([z[1] for z in rows])
        lobes.append([norm*((w*np.sinc(phase/(64*np.pi))*np.exp(-0.5j*r*phase))@amp) for r in RHO])
        comp.append(norm*(w@amp))
    return np.array(lobes).T, sum(comp)/np.sqrt(2), clock_value(key,-2*STEP,n)


def encode(value):
    lobes, comp, (b, fixed) = value
    def pair(v):
        return [float(v.real),float(v.imag)]
    return {"lobes":[[pair(v) for v in row] for row in lobes], "compensated":pair(comp), "B":float(b), "fixed":pair(fixed)}


def decode(row):
    return (np.array([[complex(*v) for v in l] for l in row['lobes']]),
            complex(*row['compensated']), (row['B'],complex(*row['fixed'])))


def integrate(key):
    low = clock_value(key,-2*STEP+1/16,4)[1]
    err = abs(low-cartesian(key,-2*STEP+1/16,4))
    assert err < 1e-13
    rows, old = [], None
    for n,m in ((32,6),(48,8),(64,10),(80,12)):
        vals = packet(key,n,m)
        flat = np.r_[vals[0].ravel(),vals[1],vals[2][1]]
        rows.append({"grid":[n,m],"amplitudes":encode(vals)})
        if old is not None:
            change = float(max(abs(flat-old)))
            rows[-1]["grid_change"] = change
            if change < 3e-10:
                return {"width":scheme(key)[0],"direct_check":float(err),"grids":rows}
        old = flat
    raise ArithmeticError(f"clock quadrature unresolved for {key}")
