"""Separate algebraic checks. Does not import the primary graph implementation."""
from itertools import product


def insist(ok, message):
    if not ok:
        raise ValueError(message)


def construct(name):
    if name == 'star-k1-6':
        return [[int(i != j and (i == 0 or j == 0)) for j in range(7)] for i in range(7)]
    if name == 'cycle-4':
        return [[int((i - j) % 4 in (1, 3)) for j in range(4)] for i in range(4)]
    vertices = list(product(range(4), repeat=2))
    insist(name in ('rook-4x4', 'shrikhande'), 'unknown construction')
    steps = {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}
    return [[int(x != y and ((x[0] == y[0] or x[1] == y[1]) if name == 'rook-4x4'
             else ((x[0]-y[0]) % 4, (x[1]-y[1]) % 4) in steps))
             for y in vertices] for x in vertices]


def determinant(matrix):
    """Fraction-free Bareiss elimination with row pivoting."""
    a = [r[:] for r in matrix]
    n, sign, previous = len(a), 1, 1
    if not n:
        return 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if a[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * p - a[i][k] * a[k][j]
                insist(numerator % previous == 0, 'Bareiss exact division')
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = p
    return sign * a[-1][-1]


def polynomial(coefficients, x):
    value = 0
    for c in coefficients:
        value = value * x + c
    return value


def certify(name, a, row):
    n = len(a)
    insist(a == construct(name), 'input differs from independent construction')
    chi = row['adjacency_characteristic']
    insist(len(chi) == n + 1 and chi[0] == 1, 'characteristic degree')
    # n+1 distinct exact evaluation points certify a degree-n polynomial identity.
    for x in range(n + 1):
        lhs = determinant([[x * int(i == j) - a[i][j] for j in range(n)] for i in range(n)])
        insist(lhs == polynomial(chi, x), 'independent characteristic identity')
        expected = (x**5 * (x*x-6) if name == 'star-k1-6' else
                    x*x*(x*x-4) if name == 'cycle-4' else
                    (x-6)*(x-2)**6*(x+2)**9)
        insist(lhs == expected, 'closed-form characteristic reference')
    # K4 count via traces of cubes of induced neighbour matrices: each K4 is
    # counted at 4 vertices, with 6 oriented triangles in each neighbourhood.
    total = 0
    for v in range(n):
        neighbours = [i for i in range(n) if a[v][i]]
        total += sum(a[i][j]*a[j][k]*a[k][i]
                     for i in neighbours for j in neighbours for k in neighbours)
    insist(total % 24 == 0 and total // 24 == row['k4_count'], 'independent K4 count')
    degrees = list(map(sum, a)); m = sum(degrees) // 2
    if n == 16:
        insist(degrees == [6]*16, 'regularity')
        insist(all(sum(a[i][k]*a[k][j] for k in range(n)) == 4*int(i == j)+2
                    for i in range(n) for j in range(n)), 'A squared = 4I + 2J')
    z = row['ihara_reciprocal_ascending']
    insist(len(z) <= 2*m + 1 and z[0] == 1, 'Ihara degree/constant')
    # Bass identity, independently at enough points to certify the whole
    # polynomial. For the tree multiply by (1-u^2), avoiding a division.
    bound = max(2*m, 2*n) if m < n else 2*m
    for u in range(bound + 1):
        b = [[int(i == j)*(1+u*u*(degrees[i]-1))-u*a[i][j]
              for j in range(n)] for i in range(n)]
        p = polynomial(list(reversed(z)), u)
        d = determinant(b)
        if m >= n:
            insist(p == (1-u*u)**(m-n)*d, 'independent Ihara-Bass identity')
        else:
            insist(p*(1-u*u)**(n-m) == d, 'independent tree Bass identity')
    return {'characteristic_points': n+1, 'bass_points': bound+1,
            'k4_via_neighbour_triangle_traces': total//24,
            'closed_form_spectrum': 'PASS', 'independent_construction': 'PASS'}


def primitive_orbits(a, length):
    """Tiny star/C4 check only: rotations identified, reversal distinct."""
    insist(len(a) <= 7 and 1 <= length <= 8, 'bounded cycle enumeration')
    found = set()
    def visit(path):
        if len(path) == length:
            if not a[path[-1]][path[0]]:
                return
            if any(path[(i-1) % length] == path[(i+1) % length] for i in range(length)):
                return
            if any(length % d == 0 and path == path[:d]*(length//d) for d in range(1, length)):
                return
            found.add(min(tuple(path[k:]+path[:k]) for k in range(length)))
            return
        for v, edge in enumerate(a[path[-1]]):
            if edge and (len(path) < 2 or v != path[-2]):
                visit(path+[v])
    for start in range(len(a)):
        visit([start])
    return len(found)
