"""Enumerate and screen one further labelled insertion on the v0.4 support."""
import argparse
from collections import Counter
from contextlib import contextmanager
from functools import cache
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream"
sys.path.insert(0, str(UPSTREAM / "v03"))
import orders
from orders import bit_edges, geometry, label, transitive


def layout(key):
    """Preserve the boundary labels and the lowest naturally labelled orbit mask."""
    n, mask = key
    if n != 6:
        return orders.layout(key)
    inner = (*orders.NODES, 13)
    past, future = geometry.P, geometry.F
    edges = set(combinations(past, 2)) | set(combinations(future, 2))
    edges.update(product(past, inner + future))
    edges.update(product(inner, future))
    edges.update((inner[i], inner[j]) for i, j in bit_edges(n, mask))
    assert transitive(edges)
    coefficients = {}
    for i, j in sorted(edges):
        count = sum((i, k) in edges and (k, j) in edges for k in (*past, *inner, *future))
        coefficients[i, j] = (1, -9, 16, -8)[count] if count <= 3 else 0
    return inner, coefficients, 14 - sum(coefficients.values())


@contextmanager
def scalar_layouts():
    with patch.object(geometry, "order", layout):
        yield


@cache
def positions(n):
    return {pair: 1 << i for i, pair in enumerate(combinations(range(n), 2))}


def natural_masks(n, edges):
    """Generate masks of all order-preserving bijections to natural labels."""
    bits = positions(n)
    for image in permutations(range(n)):
        if all(image[i] < image[j] for i, j in edges):
            yield sum(bits[image[i], image[j]] for i, j in edges)


@cache
def natural_orbits(n):
    """Group all transitive upper triangular masks. The smallest mask names the orbit."""
    lookup, automorphisms = {}, {}
    for mask in range(1 << len(positions(n))):
        if mask in lookup:
            continue
        edges = bit_edges(n, mask)
        if transitive(edges):
            images = Counter(natural_masks(n, edges))
            assert min(images) == mask and len(set(images.values())) == 1
            automorphisms[mask] = images[mask]
            lookup.update(dict.fromkeys(images, mask))
    return lookup, automorphisms


def daughter_counts_n14(parent_mask):
    """Count labelled last-event patterns for a single fixed labelled representative."""
    return Counter(min(natural_masks(6, e)) for e in orders.extend(bit_edges(5, parent_mask), 5))


def deletion_counts(end, five_lookup):
    """Independently count which parent shapes are recovered by deleting each event."""
    edges = bit_edges(6, end)
    counts = Counter()
    for v in range(6):
        bits = positions(5)
        mask = sum(bits[i - (i > v), j - (j > v)] for i, j in edges if i != v and j != v)
        counts[five_lookup[mask]] += 1
    assert sum(counts.values()) == 6
    return counts


def independent_ranks(key):
    """Check the domain using ranks before integration, without Schur complements."""
    inner, coefficients, _ = layout(key)
    n = len(inner)
    # Rows map (outer x[3], y[3], inner q[n], past t, future t) to event values.
    section = geometry.s.zeros(n + 8)
    for j in range(3):
        section[j + 1, j] = section[j + 7, j + 3] = 1
    for j, node in enumerate(inner):
        section[node, 6 + j] = 1
    section[:4, -2] = geometry.BM
    section[7:11, -1] = geometry.BP
    # Twice the pulled-back Hessian, built directly from edge differences.
    G = geometry.s.zeros(n + 8)
    for (a, b), coefficient in coefficients.items():
        if coefficient:
            d = section[a, :] - section[b, :]
            G -= coefficient * (d.T * d)
    for j in range(3):
        G[-2, j] -= 2 * geometry.AM[j + 1]
        G[j, -2] -= 2 * geometry.AM[j + 1]
        G[-1, j + 3] += 2 * geometry.AP[j]
        G[j + 3, -1] += 2 * geometry.AP[j]
    G[-2, -2] -= 2 * geometry.AM.dot(geometry.BM)
    G[-1, -1] += 2 * geometry.AP.dot(geometry.BP)

    def rank(matrix):
        return matrix.to_DM().rank()

    pure = n - rank(G[:, 6:6+n])
    integrated = list(range(6, n + 8))
    free = n + 2 - rank(G[:, integrated])
    # On eliminating the regular integration pivots the bordered mixed block
    # reduces to the inherited mixed Legendre block plus free zero rows/columns.
    Hxy = G[[0, 1, 2, *integrated], [3, 4, 5, *integrated]]
    defect = Hxy.rows - rank(Hxy) - free
    assert free >= pure >= 0 and defect >= 0
    return {"pure_bulk_nullity": pure, "full_free_nullity": free,
            "bordered_mixed_rank": Hxy.rows - free - defect,
            "reduced_mixed_defect": defect}


def run():
    full = json.loads((UPSTREAM / "results.json").read_text())
    prev = json.loads((UPSTREAM / "v03/results.json").read_text())
    parents = sorted(int(k.split("_")[1]) for k in full["full_N13"])
    assert len(parents) == len(set(parents)) == 23
    five, aut5 = natural_orbits(5)
    six, aut6 = natural_orbits(6)
    assert all(orders.orbit_table(5)[bit_edges(5, mask)] == canon for mask, canon in five.items())
    forward = {p: daughter_counts_n14(p) for p in parents}
    ends = sorted(set.union(*(set(rows) for rows in forward.values())))

    # Each labelled insertion can equally be counted by deleting a distinguished vertex
    # from a six-type and relabelling its restriction. Count every six-type, also the
    # ones no selected parent reaches. This cross-check tests zero counts too.
    for end, aut in aut6.items():
        deleted = deletion_counts(end, five)
        assert all(forward[p][end] * aut == deleted[p] * aut5[p] for p in parents)

    audit = {}
    geometry.mp.mp.dps = 65
    with scalar_layouts():
        for end in ends:
            row, state = geometry.kernel((6, end))
            assert (state is not None) == (row["status"] == "ADMISSIBLE")
            checks = independent_ranks((6, end))
            assert checks["pure_bulk_nullity"] == len(row["pure_bulk_null_vectors"])
            assert checks["full_free_nullity"] == row["free_directions"]
            assert checks["reduced_mixed_defect"] == row["legendre_size"] - row["legendre_rank"]
            assert (not checks["pure_bulk_nullity"] and not checks["reduced_mixed_defect"]) == (state is not None)
            row["independent_integer_rank_check"] = checks
            audit[end] = row
    admissible = sorted(m for m in ends if audit[m]["status"] == "ADMISSIBLE")
    by_root = {}
    all_parents = set()
    for root, rows in prev["paths_by_root"].items():
        old = Counter(path["middle_reverse_end_masks"][2] for path in rows["marked_ledger"]
                      if Fraction(path["conditional_weights"]["sequential"]) > 0)
        assert sum(old.values()) == rows["sequential_paths"] and set(old) <= set(parents)
        all_parents.update(old)
        raw = Counter()
        for p, mu in old.items():
            raw.update({c: mu * mult for c, mult in forward[p].items()})
        surviving = {m: raw[m] for m in admissible if raw[m]}
        by_root[root] = {"N13_prefix_marked_paths": dict(sorted(old.items())),
                         "all_end_marked_paths": dict(sorted(raw.items())),
                         "admissible_end_marked_paths": surviving,
                         "marked_paths_before_final_screen": sum(raw.values()),
                         "marked_paths_after_final_screen": sum(surviving.values())}
    assert all_parents == set(parents)
    census = {"all_N14_natural_masks": len(six), "all_N14_unlabelled_types": len(aut6),
              "all_N14_labelled_orders": sum(factorial(6) // a for a in aut6.values()),
              "N13_parents": len(parents), "N14_raw_end_types": len(ends),
              "N14_sequential_admissible_types": len(admissible),
              "parent_child_pairs_before_screen": sum(len(rows) for rows in forward.values()),
              "parent_child_pairs_after_screen": sum(sum(c in admissible for c in rows) for rows in forward.values()),
              "marked_paths_before_final_screen": sum(r["marked_paths_before_final_screen"] for r in by_root.values()),
              "marked_paths_after_final_screen": sum(r["marked_paths_after_final_screen"] for r in by_root.values())}
    assert set(admissible) == {c for row in by_root.values() for c in map(int, row["admissible_end_marked_paths"])}
    return {"base_commit": "71d8e32186a81e6f3ef571450397eafe357dc174", "counts": census,
            "parents": {p:dict(sorted(rows.items())) for p, rows in forward.items()},
            "sequential_admissible": admissible, "audit": audit, "by_root": by_root}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError("Use Python with assertions enabled")
    result = run()
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result["counts"]))
