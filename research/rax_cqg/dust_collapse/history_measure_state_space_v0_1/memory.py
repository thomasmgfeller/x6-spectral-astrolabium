"""Construct normalized transitions for complete marked S3 paths and test every cut."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import json
from pathlib import Path

from local_growth import catalogue, ex
from weights import A, B, edges

ROOT = Path(__file__).resolve().parent
H = Q(1, 1764)


def rate_checks(orbit_mass, orbit_size, paths, prior, renamed, example_codes):
    # Complete forward histories outside the six-order support have zero mass.
    joint = {code:orbit_mass[min(orbit)]/orbit_size[min(orbit)]
             for code, (_, orbit) in paths.items() if min(orbit) in orbit_mass}
    assert len(joint) == sum(orbit_size.values()) and sum(joint.values()) == 1
    assert min(joint.values()) > 0
    positive = {k for k,v in prior.items() if v}
    transition = {code:m/prior[code & ex.PAIR_MASK] for code,m in joint.items()}
    rows = {p:Q(0) for p in positive}
    for code, rate in transition.items():
        rows[code & ex.PAIR_MASK] += rate
    assert all(v == 1 for v in rows.values())
    for permuted in renamed:
        projected, row_sum = Counter(), Counter()
        for code, translated in permuted.items():
            p = translated & ex.PAIR_MASK
            q = transition[translated]
            assert prior[p] * q == joint[code]
            projected[p] += joint[code]
            row_sum[p] += q
        assert projected == Counter(prior)
        assert row_sum == Counter(dict.fromkeys(positive, Q(1)))
    result = {"positive_marked_transitions":len(transition),
              "normalized_positive_prefix_rows_per_permutation":len(rows),
              "reconstructed_N13_entries_per_permutation":len(prior),
              "permutations_verified":len(renamed),
              "zero_weight_children_of_positive_prefixes":len(paths)-len(joint),
              "minimum_positive_conditional_transition":str(min(transition.values()))}
    if example_codes:
        prefix = example_codes[0] & ex.PAIR_MASK
        assert all(c & ex.PAIR_MASK == prefix for c in example_codes)
        result["example"] = {
            "prefix_code":prefix, "prefix_coefficient":str(prior[prefix]),
            "end_types":[1790,5374], "child_codes":example_codes,
            "individual_transition_coefficients":[str(transition[c]) for c in example_codes],
            "total_all_outgoing_coefficients":str(rows[prefix])}
    return result


def run():
    if not __debug__:
        raise RuntimeError("Python assertions must be enabled")
    source = ROOT/"v05"
    growth = ex.read_json(source/"growth.json")
    good = ex.admissible_orders(growth["sequential_admissible"])
    roots = ex.read_json(source/"upstream/v03/results.json")["paths_by_root"]
    cert = ex.read_json(source/"exchange_certificate.json")
    results = {}
    for name, row in sorted(roots.items()):
        target, columns, sizes, counts = ex.build(row,good)
        uniform, cap, _ = ex.residual_target(target,columns,sizes)
        residual = cert[name]["residual_orbit_masses"]
        base = {orbit:cap*u+(1-cap)*Q(residual.get(str(orbit),0))
                for orbit,u in uniform.items()}
        _, paths = catalogue(row,good)
        codes = sorted(code for code, (_, orbit) in paths.items() if min(orbit) in base)
        assert len(codes) == counts["paths_valid_in_all_six_orders"]
        diagrams = {k:edges(k) for k in codes}
        renamed = [{c:ex.rename(e,p) for c,e in diagrams.items()} for p in ex.MARK_PERMS]
        assert all(set(perm.values()) == set(codes) for perm in renamed)
        prior = {ex.encode(v["edges"]):Q(v["conditional_weights"]["symmetric_completion"])
                 for v in row["marked_ledger"]}
        examples = []
        if name=="one":
            for orbit in (A,B):
                selected = [c for c in codes if c & ex.PAIR_MASK == 1564 and min(paths[c][1]) == orbit]
                assert len(selected)==1
                examples.extend(selected)
            assert [good[c] for c in examples] == [1790,5374]
        series = {}
        for shift in ((-H,Q(0),H) if name=="one" else (Q(0),)):
            mass = base.copy()
            if name=="one":
                mass[A] -= shift
                mass[B] += shift
            series[str(shift)] = rate_checks(mass, sizes, paths, prior, renamed, examples)
        results[name] = series
    return {"meaning":"Disintegration of constructed nonnegative control coefficients; no transition law independent of the input lift is used.",
            "roots":results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    output = parser.parse_args().output
    output.write_text(json.dumps(run(),sort_keys=True,indent=2)+"\n")
