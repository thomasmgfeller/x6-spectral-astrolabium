"""Exact checks for the 2+4+2 BDG benchmark. Python 3.10+, standard library."""
from collections import Counter, defaultdict
from itertools import product
from math import cos, pi, comb
from cmath import exp

weights = (-1, 9, -16, 8, 0)
vectors = [tuple(k) for k in product((1, 2, 3), repeat=4)
           if (1 in k or 3 in k) and (2 in k or 3 in k)]
assert len(vectors) == 79

def interval_score(left, right):
    relations = {(i, 6+j) for i in range(2) for j in range(2)}
    for m, (l, r) in enumerate(zip(left, right), start=2):
        for i in range(2):
            if l & (1 << i):
                relations.add((i, m))
            if r & (1 << i):
                relations.add((m, 6+i))
    counts = Counter(sum((x, z) in relations and (z, y) in relations
                         for z in range(8)) for x, y in relations)
    return 8 + sum(w * counts[i] for i, w in enumerate(weights))

def matrix_score(left, right):
    adjacent = sum(v.bit_count() for v in left+right)
    outer = [sum(bool(u & (1 << i)) and bool(v & (1 << j))
                 for u, v in zip(left, right))
             for i in range(2) for j in range(2)]
    return 8 - adjacent + sum(weights[k] for k in outer)

groups = defaultdict(Counter)
full_scores = defaultdict(Counter)
for left, right in product(vectors, repeat=2):
    score = matrix_score(left, right)
    assert score == interval_score(left, right)
    degree = sum(bool(x & 1) for x in left)
    for key in (0, degree):
        groups[key][score % 5] += 1
        full_scores[key][score] += 1

phase = 4*pi/5
z = exp(1j*phase)
for key, h in sorted(groups.items()):
    row = [h[i] for i in range(5)]
    amplitude = sum(c*z**i for i, c in enumerate(row))
    print(f'd={key} h={row} count={sum(row)} |Z|={abs(amplitude):.8f} '
          f'coherence={abs(amplitude)/sum(row):.8f}')
assert sum(groups[0].values()) == 79**2 == 6241
assert all(sum(groups[k][j] for k in range(1, 5)) == groups[0][j]
           for j in range(5))

# Bilayer: enumerate all 4 x 4 matrices at the same diagnostic phase.
m = 16
free = Counter()
degree2 = Counter()
mod5 = Counter()
for edges in range(2**m):
    k = edges.bit_count()
    free[k] += 1
    if (edges & 15).bit_count() == 2:
        degree2[k] += 1
    if k % 5 == 0:
        mod5[k] += 1
assert all(free[k] == comb(m, k) for k in range(m+1))
assert all(degree2[k] == (comb(4, 2)*comb(12, k-2) if 0 <= k-2 <= 12 else 0)
           for k in range(m+1))
def amp(h):
    return abs(sum(c*z**(8-k) for k,c in h.items()))
q = 2*abs(cos(phase/2))
assert abs(amp(free) - q**16) < 1e-9
assert abs(amp(degree2) - 6*q**12) < 1e-9
assert abs(amp(mod5)-sum(mod5.values())) < 1e-9
print('4+4 bilayer: free, degree 2, residue 0',
      [(sum(h.values()), round(amp(h),8)) for h in (free, degree2, mod5)])

for coupling in (2.3, 2.4, 2.6):
    print(f'g={coupling:.1f}', [round(abs(sum(c*exp(1j*coupling*s) for s,c
           in full_scores[key].items())) / sum(full_scores[key].values()), 8)
           for key in range(5)])

# Exact transfer for three layers, using the five coefficients of Z[z]/(z^5-1).
from itertools import combinations_with_replacement
from math import factorial, prod

def cycle_product(a, b):
    c = [0] * 5
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[(i+j) % 5] += x*y
    return c

def transfer(a, m, t):
    result = [[0]*5 for _ in range(m+1)]
    n = a + m + t
    for types in combinations_with_replacement(range(1, 1 << a), m):
        rows = [sum(1 << j for j,v in enumerate(types) if v & (1 << i))
                for i in range(a)]
        if not all(rows):
            continue
        multiplicity = factorial(m) // prod(factorial(k) for k in Counter(types).values())
        exponent = n - sum(r.bit_count() for r in rows)
        degree = rows[0].bit_count()
        bins = [[0]*5 for _ in range(1 << m)]
        for u in range(1, 1 << m):
            sizes = [(r & u).bit_count() for r in rows]
            f = -u.bit_count() + sum(weights[j] for j in sizes if j < 4)
            bins[u][f % 5] = 1
        # After the subset zeta transform, bins[d] counts all nonempty u inside d.
        for j in range(m):
            bit = 1 << j
            for d in range(1 << m):
                if d & bit:
                    for k, x in enumerate(bins[d ^ bit]):
                        bins[d][k] += x
        totals = [0]*5
        for d, base in enumerate(bins):
            power = base
            for _ in range(t-1):
                power = cycle_product(power, base)
            sign = (-1)**(m-d.bit_count())
            for k, x in enumerate(power):
                totals[(k+exponent) % 5] += sign*x
        for key in (0, degree):
            for k,x in enumerate(totals):
                result[key][k] += multiplicity*x
    assert all(min(row) >= 0 for row in result)
    assert all(result[0][k] == sum(row[k] for row in result[1:]) for k in range(5))
    return result

def halves(a, m):
    return sum((-1)**i * comb(a,i) * (2**(a-i)-1)**m for i in range(a+1))

assert transfer(2, 4, 2) == [[h[j] for j in range(5)] for _,h in sorted(groups.items())]
larger = transfer(3, 6, 3)
assert sum(larger[0]) == halves(3, 6)**2
for k,h in enumerate(larger):
    amplitude = abs(sum(x*z**j for j,x in enumerate(h)))
    print(f'3+6+3 d={k} h={h} count={sum(h)} |Z|={amplitude:.6f} R={amplitude/sum(h):.9f}')
