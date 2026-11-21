"""Verify two positive-volume cells with the same future response on type 375841.

Use Python 3 (no optional packages): python3 -B density_translation_375841.py.
All tests of inequalities or equalities use exact rational numbers.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import json

PAST = (0, 1, 2, 3)
INNER = (4, 5, 6, 11, 12, 13, 14)
FUTURE = (7, 8, 9, 10)
ORDER = 375841
CENTER = dict(zip(INNER, (Q(n, 5) for n in (1, 2, 1, 2, 3, 4, 3))))
RADIUS = Q(1, 10**7)  # applies separately to e, seven u, and seven normalized shifts xi
COFACTOR_SCALE = Q(7600, 8 * 10**6)


def box(a, r=0):
    return Q(a) - r, Q(a) + r


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def minus(a, b):
    return a[0] - b[1], a[1] - b[0]


def times(a, b):
    v = [i * j for i, j in product(a, b)]
    return min(v), max(v)


def scale(x, a):
    return times(box(x), a)


def square(a):
    return 0 if a[0] <= 0 <= a[1] else min(t*t for t in a), max(t*t for t in a)


def add_all(values):
    result = box(0)
    for value in values:
        result = plus(result, value)
    return result


def local_geometry():
    rel = set(combinations(PAST, 2)) | set(combinations(FUTURE, 2))
    rel |= set(product(PAST, INNER + FUTURE)) | set(product(INNER, FUTURE))
    rel |= {edge for bit, edge in enumerate(combinations(INNER, 2)) if ORDER & (1 << bit)}
    assert all((a, d) in rel for a, b in rel for c, d in rel if b == c)
    nodes = (3,) + INNER + (7,)
    covers = {(a, b) for a, b in rel if a in nodes and b in nodes
              and not any((a, c) in rel and (c, b) in rel for c in nodes)}

    def walk(vs):
        if vs[-1] == 7:
            yield vs[1:-1]
        else:
            for a, b in sorted(covers):
                if a == vs[-1]:
                    yield from walk(vs + (b,))

    paths = tuple(walk((3,)))
    assert all(CENTER[v] == Q(max(path.index(v)+1 for path in paths if v in path),
                              max(map(len, paths))+1) for v in INNER)
    coef = {}
    for y,x in rel:
        count = sum((y,v) in rel and (v,x) in rel for v in range(15))
        coef[y,x] = (1,-9,16,-8)[count] if count < 4 else 0
    return rel, paths, coef


def enclose(radius):
    rel, paths, coef = local_geometry()
    e = box(Q(-1,4), radius)
    u = {v:box(CENTER[v], radius) for v in INNER}
    assert all(u[a][1] < u[b][0] for a,b in rel if a in INNER and b in INNER)
    f = {v:box(0) for v in INNER}
    for path in paths:
        cuts = [box(0)] + [scale(Q(1,2),plus(u[a],u[b])) for a,b in zip(path,path[1:])] + [box(1)]
        for v, a, b in zip(path, cuts, cuts[1:]):
            assert a[1] < b[0]
            f[v] = plus(f[v],scale(Q(1,len(paths)),minus(b,a)))
    y = {i:box(i-5) for i in PAST}
    y[3] = plus(y[3],e)
    dur = minus(box(4),e)  # D/Delta
    y.update({v:plus(plus(box(-2),e),times(dur,u[v])) for v in INNER})
    C = {v:plus(box(1),scale(Q(1,19),add_all(
        scale(coef[i,v],square(minus(y[i],y[v]))) for i in y if (i,v) in rel)))
         for v in INNER}
    charge = {v:times(scale(Q(1,19),dur),add_all(
        scale(coef[i,v],minus(y[i],y[v])) for i in PAST)) for v in INNER}
    # The cross product (1,1,1) x C with reversed orientation. Identically
    # sum(d)=0 and C.d=0, pointwise for any real values of the C_v.
    d = {v:box(0) for v in INNER}
    for v, i, j in ((5,12,13),(12,13,5),(13,5,12)):
        d[v] = scale(COFACTOR_SCALE,minus(C[i],C[j]))
    if radius == 0:
        assert [d[j][0] for j in (5,12,13)] == [Q(x,10**6) for x in (268,537,-805)]
        assert sum(d[v][0] for v in INNER) == sum(C[v][0]*d[v][0] for v in INNER) == 0
    D0, D1 = Q(1,4),Q(13,50)  # enclosing Delta, not the duration D
    assert D0**4 < Q(3,722) < D1**4
    delta = times(e,(D0,D1))
    assert Q(-3,32) < delta[0] <= delta[1] < Q(-1,32)
    assert radius < Q(1,64)
    answers = {}
    for t in [-1,1]:
        x = {}
        for v in INNER:
            perturb = plus(scale(t,d[v]),box(0,radius))
            assert max(map(abs,perturb)) < f[v][0]/100
            x[v] = plus(f[v],perturb)
            # w=M*D*x=M*Delta*(4-e)*x. Both open 1% bands remain physical.
            assert 0 < x[v][0] and Q(1,4)*D1*dur[1]*Q(101,100)*f[v][1] < 1
        p = add_all(times(x[v],charge[v]) for v in INNER)
        goal = {1:Q(-1004581,190000000), -1:Q(1429581,190000000)}[t]
        assert p[0] <= goal <= p[1]
        if t == 1:
            assert Q(-54,10000) < p[0] <= p[1] < Q(-51,10000)
        else:
            assert Q(74,10000) < p[0] <= p[1] < Q(77,10000)
        if radius==0: assert p == box(goal)
        answers['negative' if t==1 else 'positive'] = list(map(str,p))
    return answers


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    print(json.dumps({'centre_p_over_M':enclose(Q(0)), 'box_halfwidth':str(RADIUS),
                      'box_p_over_M':enclose(RADIUS)}, indent=2))
