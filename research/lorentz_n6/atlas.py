"""Exact, bounded n<=6 atlas; separate from the scheduled small-order agent."""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from agent.lorentz_spectral import charpoly, spectral_key, validate_order


class Budget:
    def __init__(self, seconds=180):
        self.end = time.monotonic() + seconds

    def check(self):
        if time.monotonic() > self.end:
            raise TimeoutError("atlas budget exhausted; no complete atlas produced")


def canonical(c):
    """Exact canonical word within invariantly ordered (in,out)-degree cells.

    An isomorphism preserves cells. Enumerating every permutation inside each
    cell is therefore sufficient; no graph hash decides isomorphism.
    """
    n = len(c)
    groups = defaultdict(list)
    for i in range(n):
        groups[(sum(c[j][i] for j in range(n)), sum(c[i]))].append(i)
    choices = [itertools.permutations(groups[k]) for k in sorted(groups)]
    return min(tuple(int(c[i][j]) for i in p for j in p)
               for parts in itertools.product(*choices)
               for p in [tuple(itertools.chain.from_iterable(parts))])


def enumerate_orders(n, budget):
    if type(n) is not int or not 1 <= n <= 6:
        raise ValueError("standalone enumeration restricted to n=1..6")
    edges = list(itertools.combinations(range(n), 2))
    representatives, multiplicities = {}, defaultdict(int)
    accepted = 0
    for mask in range(1 << len(edges)):
        budget.check()
        rows = [0] * n
        for k, (i, j) in enumerate(edges):
            if mask & (1 << k):
                rows[i] |= 1 << j
        if any(rows[j] & ~rows[i] for i in range(n) for j in range(i+1, n)
               if rows[i] & (1 << j)):
            continue
        c = [[int(bool(rows[i] & (1 << j))) for j in range(n)] for i in range(n)]
        key = canonical(c)
        representatives.setdefault(key, c)
        multiplicities[key] += 1
        accepted += 1
    return representatives, multiplicities, accepted


def quill(c, vertex, direction):
    c = validate_order(c)
    n = len(c)
    if not 0 <= vertex < n or direction not in ("future", "past"):
        raise ValueError("invalid quill anchor or direction")
    q = np.zeros((n+1, n+1), dtype=np.int64)
    q[:n, :n] = c
    if direction == "future":
        q[:n, n] = c[:, vertex]
        q[vertex, n] = 1
    else:
        q[n, :n] = c[vertex, :]
        q[n, vertex] = 1
    return validate_order(q)


def pair_spectra(c, budget):
    c = np.array(c, dtype=object)
    squared = c @ c  # Integer chain counts, NOT Boolean transitive closure.
    return (charpoly(c+c.T, budget), charpoly(squared+squared.T, budget))


def freeze(value):
    return tuple(freeze(v) for v in value) if isinstance(value, (list, tuple)) else value


def partition(records, key):
    groups = defaultdict(list)
    for r in records:
        groups[freeze(key(r))].append(r["id"])
    collisions = sorted(v for v in groups.values() if len(v) > 1)
    return {"classes": len(groups), "collision_groups": collisions,
            "unresolved_pairs": sum(len(v)*(len(v)-1)//2 for v in collisions),
            "excess_orders": sum(len(v)-1 for v in collisions)}


def build(n=6, seconds=180):
    budget = Budget(seconds)
    representatives, multiplicities, accepted = enumerate_orders(n, budget)
    records = []
    for index, (key, data) in enumerate(sorted(representatives.items())):
        c = np.array(data, dtype=np.int64)
        incoming, outgoing = c.sum(axis=0), c.sum(axis=1)
        minimal = np.flatnonzero(incoming == 0).tolist()
        maximal = np.flatnonzero(outgoing == 0).tolist()
        responses = []
        for direction, vertices in [("future", maximal), ("past", minimal)]:
            for v in vertices:
                q = quill(c, v, direction)
                responses.append({"anchor": v, "direction": direction,
                                  "causal_matrix": q.tolist(),
                                  "polynomials_S_S2": pair_spectra(q, budget)})
        records.append({"id": f"n{n}-{index:04d}", "causal_matrix": data,
                        "canonical_word": "".join(map(str, key)),
                        "natural_label_multiplicity": multiplicities[key],
                        "polynomials_S_A_K": spectral_key(c, budget),
                        "polynomials_S_S2": pair_spectra(c, budget),
                        "minimal_maximal_isolated": [len(minimal), len(maximal),
                            int(np.sum((incoming == 0) & (outgoing == 0)))],
                        "quills": responses})
    base = lambda r: (r["polynomials_S_S2"], r["minimal_maximal_isolated"])
    future = lambda r: sorted(freeze(q["polynomials_S_S2"]) for q in r["quills"]
                              if q["direction"] == "future")
    summary = {
        "three_spectra": partition(records, lambda r: r["polynomials_S_A_K"]),
        "three_spectra_endpoints": partition(records, lambda r: (
            r["polynomials_S_A_K"], r["minimal_maximal_isolated"][:2])),
        "paper_quill_baseline": partition(records, base),
        "paper_maximal_quills": partition(records, lambda r: (base(r), future(r))),
    }
    if n == 6:
        observed = [len(records), summary["three_spectra"]["classes"],
                    summary["three_spectra_endpoints"]["classes"],
                    summary["paper_quill_baseline"]["unresolved_pairs"],
                    summary["paper_maximal_quills"]["unresolved_pairs"]]
        if observed != [318, 286, 314, 33, 0]:
            raise AssertionError(f"literature mismatch: {observed}")
    paths = [Path(__file__), ROOT/"agent/lorentz_spectral.py"]
    return {"schema": "x6.lorentz.exact-atlas/1", "n": n,
            "status": "GENERATED_REQUIRES_INDEPENDENT_CHECK",
            "evidence": "FINITE_EXACT_REPLICATION_NOT_GENERAL_THEOREM",
            "source": "https://doi.org/10.1088/1361-6382/abc3f8",
            "source_locations": "C columns Tables 1,2; maximal-quill stage Table 4",
            "binary_relations_examined": 2**(n*(n-1)//2),
            "naturally_labeled_orders": accepted, "nonisomorphic_orders": len(records),
            "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in paths},
            "summary": summary, "records": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=180)
    args = parser.parse_args()
    result = build(seconds=args.seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":"))+"\n")
    print(json.dumps({k: result[k] for k in ("nonisomorphic_orders", "naturally_labeled_orders", "summary")}))
