"""Exact finite existence tests for N13→N14 rates on compressed marked data.

Use --discover to regenerate the sparse rational certificate (SciPy/SymPy).
Default replay, including the full enumeration and rational checks, uses the
standard library. Neither mode reads the archived N14 extension witness.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "prior"))
from local_growth import catalogue, ex

FLOOR = Q(1, 1000000)
MASKED = "six_order_mask_first"
UNMASKED = "without_pre_mask"
CANDIDATES = {
    "types": ("parent", "child"),
    "first_ancestor": ("parent", "child", "first"),
    "ordered_ancestors": ("parent", "child", "first", "reverse"),
    "marked_insertion": ("parent", "child", "last"),
    "ordered_ancestors_and_marked_insertion": ("parent", "child", "first", "reverse", "last"),
    "rooted_parent": ("rooted_parent", "child"),
    "rooted_child": ("parent", "rooted_child"),
    "rooted_parent_and_marked_insertion": ("rooted_parent", "last"),
}
ORBIT_FAMILIES = ("chain", "one")


@lru_cache(maxsize=None)
def edges(code):
    return tuple((i, j) for i in range(6) for j in range(6) if code & (1 << (6 * i + j)))


@lru_cache(maxsize=None)
def distinguished_last(code):
    # The five old interior vertices can be freely renamed in this invariant.
    return min(ex.rename(edges(code), (*p, 5)) for p in permutations(range(5)))


def features(row, admissible):
    prior, paths = catalogue(row, admissible)
    middle = {ex.encode(e["edges"]): e["middle_reverse_end_masks"][:2]
              for e in row["marked_ledger"]}
    descriptions = {}
    full = set()
    for c, ((parent, child), orbit) in paths.items():
        p = c & ex.PAIR_MASK
        first, reverse = middle[p]
        # The two archived N11 orders have trivial automorphism group.
        # Preserve the root and forget the order of the two older insertions.
        rooted = min(p, ex.rename(edges(p), (0, 1, 2, 4, 3, 5)))
        incidence = sum(i < 3 <= j for i, j in edges(c))
        values = dict(parent=parent, child=child, first=first, reverse=reverse,
                      last=distinguished_last(c), rooted_parent=rooted,
                      rooted_child=min(orbit))
        values.update({f"cap{k}": min(k, incidence) for k in (3, 4, 5)})
        descriptions[c] = values
        if all(d in paths for d in orbit):
            full.add(c)
    return prior, paths, descriptions, full


def reduce_system(prior, paths, descriptions, full, fields, masked):
    """Solve every homogeneous exchange equation by exact ratio propagation."""
    keys = {c: tuple(d[f] for f in fields) for c, d in descriptions.items()
            if c in full or not masked}
    adjacency = defaultdict(set)
    partial_keys = {key for c, key in keys.items() if c not in full}
    for c, key in keys.items():
        p = c & ex.PAIR_MASK
        for d in paths[c][1]:
            if d in keys:
                ratio = prior[p][0] / prior[d & ex.PAIR_MASK][0]
                adjacency[key].add((keys[d], ratio))
    representative, factor, blocked = {}, {}, set()
    for anchor in sorted(adjacency):
        if anchor in representative:
            continue
        stack = [anchor]
        factor[anchor] = Q(1)
        representative[anchor] = anchor
        while stack:
            key = stack.pop()
            if key in partial_keys:
                blocked.add(anchor)
            for other, ratio in sorted(adjacency[key]):
                expected = factor[key] * ratio
                if other in representative:
                    assert representative[other] == anchor
                    if factor[other] != expected:
                        blocked.add(anchor)
                else:
                    representative[other] = anchor
                    factor[other] = expected
                    stack.append(other)
    # Give every component a reproducible short identifier, the lowest path
    # code of any member. Its potential still refers to the sorted key anchor.
    component_code = {}
    for c in sorted(keys):
        component_code.setdefault(representative[keys[c]], c)
    components = {key: component_code[a] for key, a in representative.items()}
    forced = {component_code[a] for a in blocked}
    rows = {p: Counter() for p in prior}
    for c, key in keys.items():
        comp = components[key]
        if comp not in forced:
            rows[c & ex.PAIR_MASK][comp] += factor[key]
    return keys, components, factor, forced, rows


def dense_rows(rows):
    cols = sorted(set().union(*(r.keys() for r in rows.values())))
    unique = {}
    for p, raw in sorted(rows.items()):
        unique.setdefault(tuple(raw.get(j, 0) for j in cols), p)
    return cols, list(unique.values()), list(unique)


def discover(rows):
    """Use numerical optimization only to locate a verifiable rational certificate."""
    import numpy as np
    from scipy.optimize import linprog
    from sympy import Matrix

    cols, ps, raw = dense_rows(rows)
    mat = np.array(raw, dtype=float)
    nr, nc = mat.shape
    # An exact common floor for every non-forced component gives a witness
    # for the largest support compatible with homogeneous exchange equations.
    rhs = [1 - FLOOR * sum(row) for row in raw]
    fit = linprog(np.zeros(nc), A_eq=mat, b_eq=np.array(rhs, dtype=float),
                  method="highs-ds", bounds=(0, None))
    if fit.success:
        keep = np.flatnonzero(fit.x > 1e-9)
        m = Matrix([[r[j] for j in keep] for r in raw])
        weights, free = m.gauss_jordan_solve(Matrix(rhs))
        assert not free.rows and min(weights) > 0
        return {"kind": "positive_on_free_components", "floor": str(FLOOR),
                "excess": {str(cols[j]): str(x) for j, x in zip(keep, weights)}}
    # Farkas dual for unrestricted nonnegative component variables:
    # A^T y >= 0 and sum(y) = -1 contradict A theta = 1, theta >= 0.
    dual = linprog(np.ones(2 * nr), A_ub=np.hstack((-mat.T, mat.T)),
                   b_ub=np.zeros(nc), A_eq=[np.r_[np.ones(nr), -np.ones(nr)]],
                   b_eq=[-1.0], bounds=(0, None), method="highs-ds")
    if not dual.success:
        raise ValueError("Neither a fixed-floor point nor a Farkas vector was found.")
    y = dual.x[:nr] - dual.x[nr:]
    fractions = [Q(float(v)).limit_denominator(1000000) for v in y]
    cert = {"kind": "farkas_infeasible",
            "prefix_multipliers": {str(p): str(v) for p, v in zip(ps, fractions) if v}}
    verify_dual(rows, cert)
    return cert


def verify_dual(rows, cert):
    y = {int(k): Q(v) for k, v in cert["prefix_multipliers"].items()}
    assert y.keys() <= rows.keys() and sum(y.values()) == -1
    product = Counter()
    for p, weight in y.items():
        for comp, value in rows[p].items():
            product[comp] += weight * value
    assert all(v >= 0 for v in product.values())
    return {"dual_sum_on_target": "-1", "nonzero_dual_rows": len(y)}


def verify_point(prior, paths, full, system, cert):
    keys, components, factor, forced, rows = system
    floor = Q(cert["floor"])
    excess = {int(k): Q(v) for k, v in cert["excess"].items()}
    open_components = set(components.values()) - forced
    assert excess.keys() <= open_components and floor > 0 and all(v > 0 for v in excess.values())
    theta = {k: floor + excess.get(k, 0) for k in open_components}
    rates = {}
    for c, key in keys.items():
        comp = components[key]
        rates[c] = factor[key] * theta.get(comp, 0)
    mass = {c: prior[c & ex.PAIR_MASK][0] * rate for c, rate in rates.items()}
    sums = Counter()
    for c, weight in mass.items():
        sums[c & ex.PAIR_MASK] += weight
        assert all(weight == mass.get(d, 0) for d in paths[c][1])
    assert sums == Counter({p: mu for p, (mu, _) in prior.items()})
    assert sum(mass.values()) == 1 and all(v >= 0 for v in rates.values())
    assert all(c in full for c, v in mass.items() if v)
    positive = {c for c in full if mass.get(c, 0) > 0}
    return {"positive_complete_marked_paths": len(positive),
            "minimum_positive_conditional_rate": str(min(rates[c] for c in positive)),
            "minimum_positive_path_mass": str(min(mass[c] for c in positive)),
            "verified_exact_prefix_marginals": len(prior),
            "strict_on_complete_support": positive == full}



def free_orbit_pair(prior, paths, system, certificate):
    """Test a unit transfer of total probability between the archived A/B orbits."""
    a, b = 12586556, 545263164
    keys, components, factor, forced, rows = system
    floor = Q(certificate["floor"])
    active = [components[keys[o]] for o in (a, b)]
    assert active[0] != active[1] and not (set(active) & forced)
    assert all(row.get(active[0], 0) == row.get(active[1], 0) for row in rows.values())
    affected = sorted(p for p, row in rows.items() if row.get(active[0], 0))
    masses = []
    for orbit, component in zip((a, b), active):
        members = {c for c, key in keys.items() if components[key] == component}
        assert members == set(paths[orbit][1]) and len(members) == 3
        assert all(factor[keys[c]] == 1 and prior[c & ex.PAIR_MASK][0] == Q(1, 147)
                   for c in members)
        theta = floor + Q(certificate["excess"].get(str(component), 0))
        masses.append(theta * len(members) / 147)
    # A separate unit increase in the total mass of either orbit is realised
    # by an equal 49-unit increase of its component rate. The columns cancel.
    assert all(rows[p][active[0]] == 1 for p in affected)
    return {"end_types": [paths[a][0][1], paths[b][0][1]],
            "representative_codes": [a, b], "equal_column_positive_prefixes": affected,
            "component_rate_change_per_unit_total_orbit_mass": 49,
            "witness_orbit_masses": [str(x) for x in masses],
            "open_transfer_interval_for_strict_positivity": [str(-masses[1]), str(masses[0])]}


def evaluate(prior, paths, descriptions, full, fields, masked, certs, find, tag):
    system = reduce_system(prior, paths, descriptions, full, fields, masked)
    keys, components, _, forced, rows = system
    free = set(components.values()) - forced
    blocked_paths = sum(components[keys[c]] in forced for c in full)
    result = {"rate_keys": len(components), "exchange_components": len(set(components.values())),
              "free_exchange_components_before_normalization": len(free),
              "complete_paths_forced_zero_by_exchange": blocked_paths}
    dead = sorted(p for p, row in rows.items() if not row)
    if dead:
        p = dead[0]
        return {**result, "status": "infeasible_zero_row",
                "zero_rows": len(dead), "example_prefix_code": p,
                "positive_archived_mass_at_example": str(prior[p][0])}
    if find:
        certs[tag] = discover(rows)
    cert = certs[tag]
    if cert["kind"] == "farkas_infeasible":
        return {**result, "status": "infeasible_farkas", **verify_dual(rows, cert)}
    assert cert["kind"] == "positive_on_free_components"
    evidence = verify_point(prior, paths, full, system, cert)
    if tag.startswith("one/rooted_parent_capped_incidence_4/"):
        evidence["pure_orbit_transfer_A_to_B"] = free_orbit_pair(prior, paths, system, cert)
    status = "strict_complete_support" if evidence["strict_on_complete_support"] else "feasible_proper_support"
    return {**result, "status": status, **evidence}


def run(certificate, find=False):
    if not __debug__:
        raise RuntimeError("Python assertions must be enabled")
    base = ROOT / "prior" / "v05"
    target = ex.read_json(base / "upstream/v03/results.json")["paths_by_root"]
    good = ex.admissible_orders(ex.read_json(base / "growth.json")["sequential_admissible"])
    certs = {} if find else ex.read_json(certificate)
    out = {}
    for name in ORBIT_FAMILIES:
        prior, paths, descriptions, full = features(target[name], good)
        series = {}
        candidates = CANDIDATES.copy()
        for k in ((4, 5) if name == "chain" else (3, 4)):
            candidates[f"rooted_parent_capped_incidence_{k}"] = ("rooted_parent", "child", f"cap{k}")
        for model, fields in candidates.items():
            series[model] = {}
            for masking in (MASKED, UNMASKED):
                tag = f"{name}/{model}/{masking}"
                series[model][masking] = evaluate(prior, paths, descriptions, full, fields,
                                                  masking == MASKED, certs, find, tag)
        out[name] = {"positive_prefixes": len(prior), "complete_marked_paths": len(full),
                     "complete_mark_orbits": len({min(paths[c][1]) for c in full}),
                     "families": series}
    if find:
        ex.dump(certs, certificate)
    return {"scope": "Independent nonnegative per-marked-insertion rates, rootwise exact N13 marginal, S3 exchange, finite N14 control.", "roots": out}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path, default=ROOT / "candidates_certificate.json")
    parser.add_argument("--discover", action="store_true")
    args = parser.parse_args()
    ex.dump(run(args.certificate, args.discover), args.output)
