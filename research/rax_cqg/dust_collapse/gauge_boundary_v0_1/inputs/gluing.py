"""Finite-poset gluing; only exact integer and rational arithmetic."""
from functools import lru_cache
from itertools import product, permutations
from fractions import Fraction as Q
from math import comb


def require(ok, message):
    if not ok:
        raise ValueError(message)


@lru_cache(None)
def pairs(code, n):
    return tuple((i, j) for i in range(n) for j in range(n) if code & (1 << (i*n+j)))


def encode(relations, n):
    return sum(1 << (i*n+j) for i, j in set(relations))


@lru_cache(None)
def valid(code, n):
    rows = [(code >> (i*n)) & ((1 << n)-1) for i in range(n)]
    return all(not rows[i] & (1 << i) and
               all(not (rows[j] & ~rows[i]) for j in range(n) if rows[i] & (1 << j))
               for i in range(n))


@lru_cache(None)
def all_posets(n):
    unordered = [(i, j) for i in range(n) for j in range(i+1, n)]
    answer = []
    for choices in product((0, 1, 2), repeat=len(unordered)):
        code = sum((1 << (i*n+j)) if v == 1 else (1 << (j*n+i)) if v == 2 else 0
                   for (i, j), v in zip(unordered, choices))
        if valid(code, n):
            answer.append(code)
    return tuple(sorted(answer))


@lru_cache(None)
def intervals(code, n):
    rel = set(pairs(code, n))
    return tuple((i, j, sum(1 << k for k in range(n) if (i, k) in rel and (k, j) in rel))
                 for i, j in pairs(code, n))


def weight(k, epsilon=None):
    if epsilon is None:
        return (-1, 9, -16, 8)[k] if k < 4 else 0
    # Scaled smeared action F_epsilon/sqrt(epsilon), for rational epsilon.
    e = Q(epsilon)
    f = sum(Q(c)*comb(k, m)*e**m*(1-e)**(k-m)
            for m, c in enumerate((1, -9, 16, -8)) if m <= k)
    return -e*f


@lru_cache(None)
def action(code, n, nodes=None, epsilon=None):
    nodes = (1 << n)-1 if nodes is None else nodes
    return nodes.bit_count() + sum(weight((inside & nodes).bit_count(), epsilon)
                                   for i, j, inside in intervals(code, n)
                                   if nodes & (1 << i) and nodes & (1 << j))


def coupling(code, n, a, b, epsilon=None):
    """Correction for *induced isolated* pieces; includes internal layer changes."""
    require(not a & b, 'Blocks must be disjoint')
    ambient = a | b
    cross = regrade = 0
    for i, j, inside in intervals(code, n):
        if not (ambient & (1 << i) and ambient & (1 << j)):
            continue
        full = weight((inside & ambient).bit_count(), epsilon)
        if bool(a & (1 << i)) != bool(a & (1 << j)):
            cross += full
        else:
            block = a if a & (1 << i) else b
            regrade += full-weight((inside & block).bit_count(), epsilon)
    return cross, regrade


def induced(code, n, nodes):
    ordered = [i for i in range(n) if nodes & (1 << i)]
    idx = {x: i for i, x in enumerate(ordered)}
    return encode([(idx[i], idx[j]) for i, j in pairs(code, n) if i in idx and j in idx], len(idx))


def relabel(code, n, permutation):
    return encode([(permutation[i], permutation[j]) for i, j in pairs(code, n)], n)


@lru_cache(None)
def all_permutations(n):
    return tuple(permutations(range(n)))


@lru_cache(None)
def canonical(code, n):
    orbit = [relabel(code, n, p) for p in all_permutations(n)]
    return min(orbit), sum(c == code for c in orbit)


def block_permutations(n, na):
    return tuple(a+tuple(x+na for x in b)
                 for a in all_permutations(na) for b in all_permutations(n-na))


def colored_canonical(code, n, na):
    orbit = [relabel(code, n, p) for p in block_permutations(n, na)]
    return min(orbit), sum(c == code for c in orbit)


def poly_add(poly, exponent, coefficient=1):
    poly[exponent] = poly.get(exponent, Q(0))+coefficient
    if not poly[exponent]:
        del poly[exponent]


def poly_readout(poly, z):
    """Exact real/imaginary rational pair at 1, -1 or i."""
    real = imag = Q(0)
    for e, c in poly.items():
        if z == '1':
            real += c
        elif z == '-1':
            real += c*((-1)**(e % 2))
        elif z == 'i':
            r, j = [(1, 0), (0, 1), (-1, 0), (0, -1)][e % 4]
            real += c*r; imag += c*j
        else:
            raise ValueError('Unsupported exact readout')
    return real, imag


def future_kernel(code, n):
    """One new maximal element: its past must be an order ideal."""
    answer = {}; extensions = []
    base = encode(pairs(code, n), n+1)
    for past in range(1 << n):
        extended = base | encode([(i, n) for i in range(n) if past & (1 << i)], n+1)
        if valid(extended, n+1):
            delta = action(extended, n+1)-action(code, n)
            poly_add(answer, delta)
            extensions.append({'past_mask': past, 'delta_F4': delta, 'full_code': extended})
    return answer, extensions


def current_data(code, n):
    covers = [(i, j) for i, j, interior in intervals(code, n) if not interior]
    divergence = [0]*n
    for i, j in covers:
        divergence[i] += 1; divergence[j] -= 1
    return covers, divergence

