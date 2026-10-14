"""Independent standard-library verifier; imports NO atlas/agent algorithms.

Enumeration: adjoining a maximal point with every order ideal as its past.
Isomorphism: directed backtracking bijections, not canonical words.
Polynomials: Bareiss determinants + rational Newton interpolation, not traces.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def ideals_orders(n):
    if n == 0:
        yield []
        return
    for c in ideals_orders(n-1):
        for mask in range(1 << (n-1)):
            if any((mask >> j) & 1 and c[i][j] and not (mask >> i) & 1
                   for i in range(n-1) for j in range(n-1)):
                continue
            yield [row + [(mask >> i) & 1] for i, row in enumerate(c)] + [[0]*n]


def degrees(c):
    return [(sum(c[j][i] for j in range(len(c))), sum(c[i])) for i in range(len(c))]


def isomorphic(a, b):
    if len(a) != len(b):
        return False
    da, db = degrees(a), degrees(b)
    if sorted(da) != sorted(db):
        return False
    candidates = {i: [j for j in range(len(b)) if da[i] == db[j]] for i in range(len(a))}
    order = sorted(candidates, key=lambda i: len(candidates[i]))
    assigned, used = {}, set()

    def walk(k):
        if k == len(order):
            return True
        i = order[k]
        for j in candidates[i]:
            if j in used or any(a[i][u] != b[j][v] or a[u][i] != b[v][j]
                                for u, v in assigned.items()):
                continue
            assigned[i] = j
            used.add(j)
            if walk(k+1):
                return True
            del assigned[i]
            used.remove(j)
        return False
    return walk(0)


def determinant(matrix):
    a = [list(row) for row in matrix]
    sign, previous, n = 1, 1, len(a)
    for k in range(n-1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k+1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*pivot - a[i][k]*a[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division not exact")
                a[i][j] = numerator // previous
        for i in range(k+1, n):
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def polynomial(a):
    n = len(a)
    differences = [determinant([[int(i == j)*x-a[i][j] for j in range(n)]
                               for i in range(n)]) for x in range(n+1)]
    coefficients, basis = [Fraction(0)]*(n+1), [Fraction(1)]
    for k in range(n+1):
        for j, b in enumerate(basis):
            coefficients[j] += differences[0]*b
        differences = [v-u for u, v in zip(differences, differences[1:])]
        next_basis = [Fraction(0)]*(len(basis)+1)
        for j, b in enumerate(basis):
            next_basis[j] -= k*b/(k+1)
            next_basis[j+1] += b/(k+1)
        basis = next_basis
    if any(x.denominator != 1 for x in coefficients):
        raise ArithmeticError("noninteger interpolated polynomial")
    return [int(x) for x in reversed(coefficients)]


def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))]
            for i in range(len(a))]


def operators(c):
    n = len(c)
    s = [[c[i][j]+c[j][i] for j in range(n)] for i in range(n)]
    a = [[c[i][j]-c[j][i] for j in range(n)] for i in range(n)]
    sa, ass = multiply(s, a), multiply(a, s)
    k = [[sa[i][j]-ass[i][j] for j in range(n)] for i in range(n)]
    c2 = multiply(c, c)
    s2 = [[c2[i][j]+c2[j][i] for j in range(n)] for i in range(n)]
    return s, a, k, s2


def closure_quill(c, anchor, direction):
    n = len(c)
    q = [row+[0] for row in c] + [[0]*(n+1)]
    if direction == "future":
        q[anchor][n] = 1
    elif direction == "past":
        q[n][anchor] = 1
    else:
        raise ValueError("invalid direction")
    for k in range(n+1):
        for i in range(n+1):
            for j in range(n+1):
                q[i][j] = int(q[i][j] or (q[i][k] and q[k][j]))
    return q


def verify(doc):
    if doc["schema"] != "x6.lorentz.exact-atlas/1" or doc["n"] != 6:
        raise ValueError("verifier certifies only n=6 schema/1")
    records = doc["records"]
    if len(records) != 318 or len({r["id"] for r in records}) != 318:
        raise ValueError("incomplete/duplicate representative list")
    buckets = defaultdict(list)
    for r in records:
        c = r["causal_matrix"]
        if len(c) != 6 or any(len(row) != 6 for row in c):
            raise ValueError("invalid matrix shape")
        if any(type(v) is not int or v not in (0, 1) for row in c for v in row):
            raise ValueError("invalid relation entries")
        if any(c[i][i] for i in range(6)) or any(c[i][j] and c[j][k] and not c[i][k]
               for i in range(6) for j in range(6) for k in range(6)):
            raise ValueError("invalid strict partial order")
        signature = tuple(sorted(degrees(c)))
        if any(isomorphic(c, other["causal_matrix"]) for other in buckets[signature]):
            raise ValueError("duplicate isomorphism class")
        buckets[signature].append(r)
    counts = Counter()
    for c in ideals_orders(6):
        matches = [r for r in buckets[tuple(sorted(degrees(c)))] if isomorphic(c, r["causal_matrix"])]
        if len(matches) != 1:
            raise ValueError("enumeration not covered exactly once")
        counts[matches[0]["id"]] += 1
    checked_polynomials = 0
    groups = {k: defaultdict(list) for k in doc["summary"]}
    token = lambda x: json.dumps(x, separators=(",", ":"))
    for r in records:
        if counts[r["id"]] != r["natural_label_multiplicity"]:
            raise ValueError("enumeration multiplicity mismatch")
        c = r["causal_matrix"]
        s, a, k, s2 = operators(c)
        three = [polynomial(m) for m in (s, a, k)]
        pair = [three[0], polynomial(s2)]
        checked_polynomials += 4
        if three != r["polynomials_S_A_K"] or pair != r["polynomials_S_S2"]:
            raise ValueError("polynomial mismatch")
        ds = degrees(c)
        ends = [sum(x == 0 for x, y in ds), sum(y == 0 for x, y in ds), sum(x == y == 0 for x, y in ds)]
        if ends != r["minimal_maximal_isolated"]:
            raise ValueError("endpoint mismatch")
        expected = {(i, d) for i, (x, y) in enumerate(ds)
                    for d, valid in [("future", y == 0), ("past", x == 0)] if valid}
        actual = [(q["anchor"], q["direction"]) for q in r["quills"]]
        if len(actual) != len(expected) or set(actual) != expected:
            raise ValueError("missing or duplicate quill")
        future = []
        for q in r["quills"]:
            cq = closure_quill(c, q["anchor"], q["direction"])
            if cq != q["causal_matrix"]:
                raise ValueError("quill closure mismatch")
            sq, _, _, s2q = operators(cq)
            qp = [polynomial(sq), polynomial(s2q)]
            checked_polynomials += 2
            if qp != q["polynomials_S_S2"]:
                raise ValueError("quill polynomial mismatch")
            if q["direction"] == "future":
                future.append(qp)
        keys = [three, [three, ends[:2]], [pair, ends], [[pair, ends], sorted(future)]]
        for name, key in zip(("three_spectra", "three_spectra_endpoints", "paper_quill_baseline", "paper_maximal_quills"), keys):
            groups[name][token(key)].append(r["id"])
    for name, bucket in groups.items():
        collisions = sorted(v for v in bucket.values() if len(v) > 1)
        observed = {"classes": len(bucket), "collision_groups": collisions,
                    "unresolved_pairs": sum(len(v)*(len(v)-1)//2 for v in collisions),
                    "excess_orders": sum(len(v)-1 for v in collisions)}
        if observed != doc["summary"][name]:
            raise ValueError("summary or collision-membership mismatch")
    if (doc["binary_relations_examined"] != 32768 or
        doc["naturally_labeled_orders"] != sum(counts.values()) or doc["nonisomorphic_orders"] != 318):
        raise ValueError("enumeration totals mismatch")
    return {"status": "PASS", "scope": "INDEPENDENT_ALGORITHM_CHECK_NOT_EXTERNAL_REVIEW",
            "representatives_checked": 318, "natural_orders_checked": sum(counts.values()),
            "exact_polynomials_checked": checked_polynomials,
            "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(json.loads(args.atlas.read_text()))
    result["atlas_sha256"] = hashlib.sha256(args.atlas.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))
