"""Exact finite simple undirected graphs; Python standard library, Apache-2.0."""
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ValueError(message)


def adjacency(graph):
    require(type(graph) is dict and set(graph) == {'id', 'n', 'edges'}, 'graph fields')
    n = graph['n']
    require(type(n) is int and 1 <= n <= 16, 'bounded integer vertex count')
    require(type(graph['id']) is str, 'graph id')
    edges = graph['edges']
    require(type(edges) is list and len(edges) <= n * (n - 1) // 2, 'edge list')
    a = [[0] * n for _ in range(n)]
    previous = None
    for edge in edges:
        require(type(edge) is list and len(edge) == 2, 'edge pair')
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < v < n,
                'strict endpoints: no aliases, loops or negative indices')
        require(previous is None or previous < edge, 'sorted distinct edges')
        previous = edge
        a[u][v] = a[v][u] = 1
    return a


def characteristic(a):
    """Faddeev-LeVerrier with exact divisions; descending monic coefficients."""
    n = len(a)
    rows = [[(k, v) for k, v in enumerate(row) if v] for row in a]
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n + 1):
        ab = [[sum(v * b[r][j] for r, v in rows[i]) for j in range(n)]
              for i in range(n)]
        trace = sum(ab[i][i] for i in range(n))
        require(trace % k == 0, 'nonintegral characteristic coefficient')
        c = -trace // k
        coefficients.append(c)
        for i in range(n):
            ab[i][i] += c
        b = ab
    require(all(v == 0 for row in b for v in row), 'Cayley-Hamilton residual')
    return coefficients


def nonbacktracking(a):
    arcs = [(i, j) for i, row in enumerate(a) for j, v in enumerate(row) if v]
    return arcs, [[int(v == x and u != y) for x, y in arcs] for u, v in arcs]


def k4_cliques(a):
    return [list(c) for c in combinations(range(len(a)), 4)
            if all(a[u][v] for u, v in combinations(c, 2))]


def summarize(a):
    arcs, t = nonbacktracking(a)
    # det(I-uT) has ascending coefficients equal to descending chi_T.
    z = characteristic(t)
    while len(z) > 1 and z[-1] == 0:
        z.pop()
    return {'n': len(a), 'm': len(arcs) // 2,
            'degrees': sorted(map(sum, a)), 'adjacency_characteristic': characteristic(a),
            'ihara_reciprocal_ascending': z, 'k4_count': len(k4_cliques(a))}


def relabel(a, order):
    require(sorted(order) == list(range(len(a))), 'permutation')
    return [[a[i][j] for j in order] for i in order]
