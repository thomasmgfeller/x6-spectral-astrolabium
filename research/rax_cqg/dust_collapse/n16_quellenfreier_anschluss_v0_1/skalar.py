"""Exact conditional N15/N16 scalar boundary test in the inherited H3 frame."""
from fractions import Fraction as Q
from itertools import combinations, product
import json


P = (0, 1, 2, 3)
I = (4, 5, 6, 11, 12, 13, 14)
F = (7, 8, 9, 10)
LAYERS = (1, -9, 16, -8)


def zeros(n, m):
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return list(zip(*a))


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in transpose(b)] for row in a]


def block(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def det_inverse(a):
    """Gauss-Jordan with row pivots. All calls require a nonsingular matrix."""
    n = len(a)
    mat = [list(row) + unit for row, unit in zip(a, eye(n))]
    det = Q(1)
    for k in range(n):
        pivot_row = next((j for j in range(k, n) if mat[j][k]), None)
        if pivot_row is None:
            raise ValueError("Singular matrix")
        if pivot_row != k:
            mat[k], mat[pivot_row] = mat[pivot_row], mat[k]
            det = -det
        pivot = mat[k][k]
        det *= pivot
        mat[k] = [x/pivot for x in mat[k]]
        for j in range(n):
            if j != k and mat[j][k]:
                scale = mat[j][k]
                mat[j] = [x-scale*y for x, y in zip(mat[j], mat[k])]
    return det, [row[n:] for row in mat]


def geometry(ideal):
    old = set(combinations(P, 2)) | set(combinations(F, 2))
    old.update(product(P, I+F))
    old.update(product(I, F))
    code = 375841
    old.update(edge for bit, edge in enumerate(combinations(I, 2)) if code & (1 << bit))
    if ideal is not None:
        assert all(i in ideal for i, j in old if j in ideal)
    relation = old | ({(j, 15) for j in ideal} if ideal is not None else set())
    n = 15 if ideal is None else 16
    pairs = {}
    for i, j in relation:
        depth = sum((i, v) in relation and (v, j) in relation for v in range(n))
        if depth < len(LAYERS):
            pairs[i, j] = LAYERS[depth]
    return n, pairs


def framed_hessian(n, pairs):
    # beta/2 q^T H q = -beta/4 sum_ij b_ij (q_i-q_j)^2.
    h = zeros(n, n)
    for (i, j), weight in pairs.items():
        w = Q(weight, 2)
        h[i][j] += w
        h[j][i] += w
        h[i][i] -= w
        h[j][j] -= w
    frame = zeros(n, n)
    am = (-128, 241, 119, -232)
    ap = am[::-1]
    bm = (-46, -32, -16, 0)
    bp = tuple(-v for v in bm[::-1])
    for j in range(3):
        frame[j+1][j] = frame[7+j][3+j] = Q(1)
    for j, point in enumerate(I):
        frame[point][6+j] = Q(1)
    for j in range(4):
        frame[P[j]][13] = bm[j]
        frame[F[j]][14] = bp[j]
    if n == 16:
        frame[15][15] = Q(1)
    g = multiply(multiply(transpose(frame), h), frame)
    for j in range(3):
        g[13][j] -= am[j+1]
        g[j][13] -= am[j+1]
        g[14][3+j] += ap[j]
        g[3+j][14] += ap[j]
    g[13][13] -= sum(x*y for x, y in zip(am, bm))
    g[14][14] += sum(x*y for x, y in zip(ap, bp))
    return g


def summarize(ideal):
    n, pairs = geometry(ideal)
    g = framed_hessian(n, pairs)
    interior = list(range(6, 15))
    outside = list(range(6)) + ([15] if n == 16 else [])
    hidden_det, hidden_inverse = det_inverse(block(g, interior, interior))
    links = block(g, outside, interior)
    schur_term = multiply(multiply(links, hidden_inverse), transpose(links))
    k = [[g[i][j]-schur_term[r][s] for s, j in enumerate(outside)]
         for r, i in enumerate(outside)]
    xin, yout = range(3), range(3, 6)
    a, b = block(k, xin, xin), block(k, xin, yout)
    b_det, b_inv = det_inverse(b)
    a2 = multiply(a, a)
    t = [[v + (i == j) for j, v in enumerate(row)] for i, row in enumerate(a2)]
    _, t_inv = det_inverse(t)
    # Re(precision)/beta after integration with exp(-beta*x^T*x/2).
    precision = multiply(multiply(transpose(b), t_inv), b)
    minors = [det_inverse(block(precision, range(d), range(d)))[0] for d in (1, 2, 3)]
    assert all(v > 0 for v in minors)
    out = {"active_new_edges": {str(i): w for (i, j), w in sorted(pairs.items()) if j == 15},
           "hidden_det": str(hidden_det), "mixed_det": str(b_det),
           "real_precision_over_beta_leading_minors": list(map(str, minors))}
    if n == 16:
        c = block(k, xin, [6])
        # beta(B*y+c*q_n)^T (I+A^2)^-1 (B*y+c*q_n) in |psi|^2.
        out["translation_B_inverse_c"] = [str(z[0]) for z in multiply(b_inv, c)]
    return out


def run():
    cases = {"N15": None, "J_P_6": P+(6,), "J_all": tuple(range(15)),
             "J_P_6_11_12_13": P+(6, 11, 12, 13)}
    report = {name: summarize(ideal) for name, ideal in cases.items()}
    assert report["J_P_6"]["active_new_edges"] == {"1": -8, "2": 16, "3": -9, "6": 1}
    assert report["J_all"]["active_new_edges"] == {"7": -8, "8": 16, "9": -9, "10": 1}
    assert set(map(int, report["J_P_6_11_12_13"]["active_new_edges"])).isdisjoint(P)
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
