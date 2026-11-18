"""Exact N13→N14 composition test for a growth rate per marked insertion.

A forward ordered path c with labelled prefix p and unmarked types (i,j)
gets coefficient mu(p)*q(i,j). Rates may differ between the two N11 roots.
A second test imposes the six-order eligibility mask before assigning rates.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "v05"))
import exchange as ex


def catalogue(row, end_labels):
    paths, prefixes = {}, {}
    for entry in row["marked_ledger"]:
        mu = Q(entry["conditional_weights"]["symmetric_completion"])
        if not mu:
            continue
        edges = frozenset(map(tuple, entry["edges"]))
        prefix = ex.encode(edges)
        old_type = entry["middle_reverse_end_masks"][2]
        prefixes[prefix] = (mu, old_type)
        for child in ex.extend(edges, 5):
            code = ex.encode(child)
            if code in end_labels:
                images = tuple(sorted({ex.rename(child, p) for p in ex.MARK_PERMS}))
                assert code not in paths and code & ex.PAIR_MASK == prefix
                paths[code] = ((old_type, end_labels[code]), images)
    assert sum(m for m, _ in prefixes.values()) == 1
    return prefixes, paths


def relations(prefixes, paths, masked):
    # For two relabellings c,d the equality of path coefficients is
    # q(key[d]) = mu(prefix[c])/mu(prefix[d]) * q(key[c]).
    adj = defaultdict(dict)
    forced = {}
    choices = {p:Counter() for p in prefixes}
    full_examples, partial_examples = {}, {}
    for code, (key, orbit) in sorted(paths.items()):
        missing = next((d for d in orbit if d not in paths), None)
        if missing is None:
            full_examples.setdefault(key, code)
        else:
            partial_examples.setdefault(key, code)
            if masked:
                continue
            forced.setdefault(key, (code, missing))
        p = code & ex.PAIR_MASK
        choices[p][key] += 1
        for d in orbit:
            if d in paths:
                other = paths[d][0]
                ratio = prefixes[p][0] / prefixes[d & ex.PAIR_MASK][0]
                adj[key].setdefault((other, ratio), (code, d))
    assert all(choices.values())
    mixed = sorted(full_examples.keys() & partial_examples.keys())
    k = mixed[0]
    return adj, forced, choices, {
        "count":len(mixed), "example_type_pair":list(k),
        "full_ordered_code":full_examples[k], "partial_ordered_code":partial_examples[k],
    }


def components(adj, forced):
    # Seed a positive unit coefficient at each component anchor. All other
    # values are then fixed rational multiples. A forced zero or inconsistent
    # cycle forces the entire component, including its seed, to zero.
    group, tests = {}, []
    for anchor in sorted(adj):
        if anchor in group:
            continue
        potentials = {anchor:Q(1)}
        stack = [anchor]
        clash = None
        while stack:
            a = stack.pop()
            for (b, ratio), codes in sorted(adj[a].items()):
                value = potentials[a] * ratio
                if b not in potentials:
                    potentials[b] = value
                    stack.append(b)
                elif potentials[b] != value and clash is None:
                    clash = {"relabelled_codes":list(codes),
                             "relative_value_from_tree":str(potentials[b]),
                             "relative_value_from_edge":str(value)}
        touched = sorted(potentials.keys() & forced.keys())
        blocked = bool(touched) or clash is not None
        index = len(tests)
        group.update(dict.fromkeys(potentials, index))
        tests.append({"anchor_type_pair":list(anchor), "blocked":blocked,
                      "support_zero_codes":list(forced[touched[0]]) if touched else None,
                      "cycle_conflict":clash})
    return group, tests


def evaluate(prefixes, paths, masked):
    adj, forced, choices, mixed = relations(prefixes, paths, masked)
    group, tests = components(adj, forced)
    def blocked(key):
        return tests[group[key]]["blocked"]
    impossible = [p for p, row in choices.items() if all(blocked(k) for k in row)]
    assert impossible
    p = min(impossible)
    mu, old_type = prefixes[p]
    rows = choices[p]
    direct = None
    for key in sorted(adj):
        for (other, ratio), (c, d) in sorted(adj[key].items()):
            if key == other and ratio > 1 and all(i in paths for i in paths[c][1]):
                direct = {"type_pair":list(key), "relabelled_codes":[c,d],
                          "positive_prefix_masses":[str(prefixes[i & ex.PAIR_MASK][0]) for i in (c,d)],
                          "required_rate_multiple":str(ratio)}
                break
        if direct:
            break
    assert direct
    evidence = []
    for k, count in sorted(rows.items()):
        test = tests[group[k]]
        assert test["cycle_conflict"] or test["support_zero_codes"]
        evidence.append({"end_type": k[1], "number_marked_insertions":count,
                         **{name: test[name] for name in ("anchor_type_pair", "cycle_conflict", "support_zero_codes")}})
    return {"candidate_result":"infeasible",
            "number_distinct_rate_parameters":len(group),
            "number_forced_zero_by_homogeneous_equations":sum(map(blocked,group)),
            "number_positive_prefixes_with_all_rates_zero":len(impossible),
            "mixed_support_type_pairs":mixed,
            "single_rate_cycle_forcing_zero":direct,
            "central_pair_components":[{"parent_type":i,"end_type":j,"forced_zero":blocked((i,j))}
                      for i,j in sorted(group) if j in (1790,5374)],
            "contradiction":{"labelled_N13_code":p,"N13_type":old_type,"required_mass":str(mu),
                             "sum_of_all_proposed_child_masses":"0",
                             "eligible_labelled_insertions":sum(rows.values()),
                             "forced_zero_rate_witnesses":evidence}}


def run():
    if not __debug__:
        raise RuntimeError("Python assertions must be enabled")
    source = ROOT / "v05"
    catalogue14 = ex.read_json(source/"growth.json")
    good = ex.admissible_orders(catalogue14["sequential_admissible"])
    old = ex.read_json(source/"upstream/v03/results.json")["paths_by_root"]
    rows = {}
    for r, row in sorted(old.items()):
        prefixes, paths = catalogue(row, good)
        rows[r] = {"number_positive_marked_prefixes":len(prefixes),
                   "unfiltered":evaluate(prefixes, paths, False),
                   "six_order_mask_first":evaluate(prefixes, paths, True)}
    return {"scope":"Same rate per marked insertion at fixed unmarked parent and child; independent rate set per N11 root; preserve published marked S2 marginal and invariance under all S3 mark permutations.",
            "roots":rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    path = parser.parse_args().output
    path.write_text(json.dumps(run(),sort_keys=True,indent=2) + "\n")
