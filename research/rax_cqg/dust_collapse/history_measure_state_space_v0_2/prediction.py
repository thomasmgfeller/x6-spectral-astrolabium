"""Coarsest prefix partitions for the distribution of the next unmarked endpoint.

All probabilities refer to positive control weights conditional on one root.
Equivalence concerns complete distributions, before any clock or detector.
"""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys

PRIOR = Path(__file__).resolve().parent / "prior"
sys.path.insert(0, str(PRIOR))
from local_growth import catalogue, ex
from weights import edges


def ordered_blocks(keys, signatures):
    groups = defaultdict(list)
    for key in sorted(keys):
        groups[signatures[key]].append(key)
    return sorted(groups.values())


def probabilities(prefixes, paths, sizes, law):
    rows = {p: Counter() for p in prefixes}
    for code, ((_, end), orbit) in paths.items():
        p = code & ex.PAIR_MASK
        k = min(orbit)
        if k in sizes:
            rows[p][end] += law[k] / sizes[k] / prefixes[p][0]
    assert all(sum(row.values()) == 1 for row in rows.values())
    return rows


def signature_blocks(rows):
    return ordered_blocks(rows,{p:tuple(sorted(row.items())) for p,row in rows.items()})


def minimum_partition(root,law,rows,prefixes,paths,sizes,target,columns):
    # Strict positivity gives each prefix precisely its enumerated support.
    support = ordered_blocks(rows,{p:tuple(sorted(row)) for p,row in rows.items()})
    if root == "chain":
        src = Path(__file__).with_name("prediction_minimum_certificate.json")
        cert = ex.read_json(src)
        floor = Q(cert["floor"])
        extra = {int(k):Q(v) for k,v in cert["residual_above_floor"].items()}
        assert extra.keys() <= law.keys() and min(extra.values())>0 and floor>0
        witness = {k:floor+extra.get(k,0) for k in law}
        assert ex.marginal(columns,witness)==Counter(target)
        assert sum(witness.values())==1
        alternate = probabilities(prefixes, paths, sizes, witness)
    else:
        alternate = rows
    assert signature_blocks(alternate)==support
    return support


def witnesses(rows, prefixes, blocks):
    """Pick an exact largest within-parent discrepancy; fix ties by prefix code."""
    candidates = [(p,q) for p,q in combinations(sorted(rows),2) if prefixes[p][1]==prefixes[q][1]]
    def tv(p,q):
        ends = rows[p].keys() | rows[q].keys()
        return sum(abs(rows[p][e]-rows[q][e]) for e in ends) / 2
    p,q = max(candidates,key=lambda pair:tv(*pair))
    separated_ends = sorted(rows[p].keys() | rows[q].keys())
    e = max(separated_ends,key=lambda end:abs(rows[p][end]-rows[q][end]))
    by_type = defaultdict(set)
    for i,block in enumerate(blocks):
        for prefix in block:
            by_type[prefixes[prefix][1]].add(i)
    return {
        "unmarked_prefix_types":len(by_type),
        "number_of_predictive_classes_per_prefix_type":{str(k):len(v) for k,v in sorted(by_type.items())},
        "worst_same_parent_TV_for_archived_law":{
            "N13_type":prefixes[p][1], "prefix_codes":[p,q], "TV":str(tv(p,q)),
            "largest_single_endpoint_difference_at":e, "probabilities":[str(rows[x][e]) for x in (p,q)]}}


def run():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    source = PRIOR / "v05"
    labels = ex.admissible_orders(ex.read_json(source/"growth.json")["sequential_admissible"])
    roots = ex.read_json(source/"upstream/v03/results.json")["paths_by_root"]
    cert = ex.read_json(source/"exchange_certificate.json")
    out = {}
    for root, data in sorted(roots.items()):
        prefixes, paths = catalogue(data, labels)
        target, columns, sizes, _ = ex.build(data, labels)
        uni, cap, _ = ex.residual_target(target,columns,sizes)
        residual = cert[root]["residual_orbit_masses"]
        law = {k:cap*v + (1-cap)*Q(residual.get(str(k),0)) for k,v in uni.items()}
        assert min(law.values()) > 0 and ex.marginal(columns,law)==Counter(target)
        rows = probabilities(prefixes,paths,sizes,law)
        fixed = signature_blocks(rows)
        # Any S3-invariant lift assigns swapped prefixes equal endpoint rows.
        # This one strictly positive lift already separates all remaining pairs.
        swap = {p:ex.rename(edges(p),(0,1,2,4,3)) for p in prefixes}
        structural = ordered_blocks(rows,{p:min(p,swap[p]) for p in prefixes})
        assert all(swap[swap[p]]==p and prefixes[p]==prefixes[swap[p]] for p in prefixes)
        assert fixed==structural
        universal = structural
        minimal = minimum_partition(root,law,rows,prefixes,paths,sizes,target,columns)
        out[root] = {
            "positive_ordered_prefixes":len(prefixes), "pair_orbits":len(target),
            "positive_triple_orbits":len(sizes),
            "number_fixed_law_classes":len(fixed), "number_universal_classes":len(universal),
            "minimum_classes_over_strictly_positive_laws":len(minimal),
            "minimum_partition":minimal,
            "number_classes_crossing_parent_types":sum(len({prefixes[p][1] for p in g})>1 for g in universal),
            "fixed_law_blocks":fixed, "universal_blocks":universal,
            "fixed_law_distributions_by_representative":{
                str(g[0]):{str(e):str(v) for e,v in sorted(rows[g[0]].items())} for g in fixed},
            **witnesses(rows,prefixes,universal)}
    return out


if __name__ == "__main__":
    p = ArgumentParser(description=__doc__)
    p.add_argument("output", type=Path)
    ex.dump(run(),p.parse_args().output)
