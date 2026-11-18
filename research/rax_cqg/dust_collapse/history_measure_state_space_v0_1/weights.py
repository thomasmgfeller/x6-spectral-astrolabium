"""Reconstruct the one-edge N11 conditional weights and test the free S3 direction."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "v05"
sys.path.insert(0, str(SOURCE))
import exchange

A, B = 12586556, 545263164


def edges(code):
    return frozenset((i, j) for i in range(6) for j in range(6)
                     if code & (1 << (6*i+j)))


def orbit_codes(code):
    return sorted({exchange.rename(edges(code), perm) for perm in exchange.MARK_PERMS})


def direct_geometry(code):
    """Count open intervals on the full history using independent consecutive labels."""
    past, inner, future = range(4), range(4, 10), range(10, 14)
    relation = set(combinations(past, 2)) | set(combinations(future, 2))
    relation.update((i, j) for i in past for j in [*inner, *future])
    relation.update((i, j) for i in inner for j in future)
    relation.update((4+i, 4+j) for i, j in edges(code))
    intervals = Counter(sum((i, k) in relation and (k, j) in relation for k in range(14))
                        for i, j in relation)
    f4 = 14 - sum(coef * intervals[n] for n, coef in enumerate((1, -9, 16, -8)))
    automorphisms = sum(exchange.rename(edges(code), perm) == code for perm in permutations(range(6)))
    return {"F4": f4, "interior_relations": len(edges(code)), "interior_automorphisms": automorphisms,
            "open_intervals_by_size": {str(k): v for k, v in sorted(intervals.items())}}


def projections(masses, labels):
    """Project orbit masses onto labelled pairs after every permutation and onto endpoints."""
    pairs = [Counter() for perm in exchange.MARK_PERMS]
    ends = Counter()
    for orbit, mass in masses.items():
        codes = orbit_codes(orbit)
        ends[labels[orbit]] += mass
        for i, perm in enumerate(exchange.MARK_PERMS):
            for code in codes:
                prefix = exchange.rename(edges(code), perm) & exchange.PAIR_MASK
                pairs[i][prefix] += mass / len(codes)
    return pairs, ends


def run():
    if not __debug__:
        raise RuntimeError("Python assertions must be enabled")
    growth = exchange.read_json(SOURCE / "growth.json")
    prior = exchange.read_json(SOURCE / "upstream/v03/results.json")["paths_by_root"]["one"]
    published = exchange.read_json(SOURCE / "exchange.json")["one"]
    certificate = exchange.read_json(SOURCE / "exchange_certificate.json")["one"]
    labels = exchange.admissible_orders(growth["sequential_admissible"])
    target, columns, sizes, _ = exchange.build(prior, labels)
    uniform, fraction, _ = exchange.residual_target(target, columns, sizes)
    residual = {int(key): Q(value) for key, value in certificate["residual_orbit_masses"].items()}
    base = {key: fraction*u + (1-fraction)*residual.get(key, 0) for key, u in uniform.items()}
    assert len(base) == 191 and min(base.values()) > 0 and sum(base.values()) == 1
    assert labels[A] == 1790 and labels[B] == 5374
    assert base[A] == base[B] == Q(1,882)
    old_pairs = {exchange.encode(row["edges"]):Q(row["conditional_weights"]["symmetric_completion"])
                 for row in prior["marked_ledger"]}
    base_pairs, ends = projections(base, labels)
    assert all(pair == Counter(old_pairs) for pair in base_pairs)
    assert ends == {int(k):Q(v) for k,v in published["witness_N14_end_weights"].items()}
    assert ends[labels[A]] == base[A] and ends[labels[B]] == base[B]

    # An identical column in each labelled cut proves equality for the full line,
    # not only for the particular positive values tested below.
    p_a, _ = projections({A: Q(1)}, labels)
    p_b, _ = projections({B: Q(1)}, labels)
    assert sizes[A] == sizes[B] == 3
    assert p_a == p_b and all(col == p_a[0] for col in p_a)
    geometry = {str(labels[k]): direct_geometry(k) for k in (A,B)}
    for k, row in geometry.items():
        assert row["F4"] == growth["audit"][k]["F4"] and row["interior_automorphisms"] == 2
    f_a, f_b = (geometry[str(labels[k])]["F4"] for k in (A,B))
    initial_mean = sum(mass*growth["audit"][str(end)]["F4"] for end, mass in ends.items())

    shift = base[A]/2
    checks = {}
    for t in (-base[B], Q(0), shift, base[A]):
        test = base.copy()
        test[A] -= t
        test[B] += t
        pair_laws, end_law = projections(test, labels)
        assert all(pair == Counter(old_pairs) for pair in pair_laws)
        assert sum(end_law.values()) == 1 and min(test.values()) >= 0
        mean = sum(mass*growth["audit"][str(end)]["F4"] for end, mass in end_law.items())
        assert mean == initial_mean + t*(f_b-f_a)
        checks[str(t)] = {"orbit_A":str(test[A]), "orbit_B":str(test[B]),
                          "all_orbit_masses_strictly_positive": min(test.values()) > 0,
                          "F4_coefficient_average": str(mean)}
    assert initial_mean == Q(7741,441) and shift == Q(1,1764)
    return {"condition":"one-edge N11 root; real nonnegative path coefficients, normalized per root",
            "source_v05_commit":"8fe1fd9bef3e793ffae8fa7cefe66aea4af87d98",
            "fully_admissible_orbits":len(base), "positive_marked_pairs":sum(v > 0 for v in old_pairs.values()),
            "marked_pair_entries_checked_including_zeros":len(old_pairs),
            "A":{"orbit":A,"end":labels[A],"codes":orbit_codes(A)},
            "B":{"orbit":B,"end":labels[B],"codes":orbit_codes(B)},
            "common_unit_column_in_each_of_six_marked_cuts":{str(i):str(m) for i,m in sorted(p_a[0].items())},
            "geometry":geometry, "base_mass_per_selected_orbit":str(base[A]),
            "transfer_convention":"t from A to B",
            "closed_nonnegative_interval":[str(-base[B]),str(base[A])],
            "strict_positivity":"open interior of the closed nonnegative interval",
            "baseline_conditional_F4_coefficient_average":str(initial_mean),
            "conditional_average_slope":f_b-f_a,
            "example_shift":str(shift), "conditional_average_change":str(shift*(f_b-f_a)),
            "two_root_coefficient_average_change_at_equal_root_coefficients":str(shift*(f_b-f_a)/2),
            "transfer_checks":checks}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    out = parser.parse_args().output
    out.write_text(json.dumps(run(),sort_keys=True,indent=2)+"\n")
