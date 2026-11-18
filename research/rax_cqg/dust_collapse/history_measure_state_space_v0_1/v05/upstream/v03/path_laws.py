"""Exact rational weights for ordered, endpoint-uniform-path and exchangeable insertions."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import permutations
from orders import extend, orbit_table, restrict, swapped, ROOTS


def tv(a, b):
    return sum(abs(a.get(k, 0)-b.get(k, 0)) for k in a.keys() | b.keys()) / 2


def group(law, project):
    total = defaultdict(Q)
    for end, mass in law.items():
        total[project(end)] += mass
    return dict(total)


def summarize_paths(root, ends, states):
    active = {e for e,(a,b,c) in ends.items() if (4,a) in states and (5,c) in states}
    both = {e for e in active if swapped(e) in active}
    parents = tuple(e for e in extend(ROOTS[root],3) if (4,orbit_table(4)[e]) in states)
    n = len(parents)
    assert n == 7
    parent_id = {e:i for i,e in enumerate(parents)}
    def cell(e):
        return (parent_id[restrict(e,4)],parent_id[restrict(swapped(e),4)])
    first_totals = Counter(restrict(e,4) for e in active)
    assert set(first_totals) == set(parents)
    step = {e:Q(1,n*first_totals[restrict(e,4)]) for e in active}
    joint = {e:Q(1,len(active)) for e in active}
    cells = Counter(cell(e) for e in both)
    used = Counter()
    num_match = 0
    for perm in permutations(range(n)):
        pairs = list(enumerate(perm))
        if all(k in cells for k in pairs):
            used.update(pairs)
            num_match += 1
    assert num_match and used.keys() == cells.keys()
    symmetric = {e:Q(used[cell(e)],num_match*n*cells[cell(e)]) for e in both}
    assert all(symmetric[e] == symmetric[swapped(e)] > 0 for e in both)
    assert all(group(symmetric,lambda e:restrict(e,4))[p] == Q(1,n) for p in parents)
    assert group(step,lambda e:restrict(e,4)) == group(symmetric,lambda e:restrict(e,4))
    laws = {"sequential":step, "uniform_complete_paths":joint, "symmetric_completion":symmetric}
    by_law = {}
    for name,d in laws.items():
        assert sum(d.values()) == 1
        flipped = {swapped(e):v for e,v in d.items()}
        marginal = group(d,lambda e:ends[e][2])
        by_law[name] = {
            "swap_path_TV":str(tv(d,flipped)),
            "probability_weight_on_no_reverse":str(sum(v for e,v in d.items() if swapped(e) not in active)),
            "endpoint_weights":{str(k):str(v) for k,v in sorted(marginal.items())},
            "first_marginal_TV_to_v02":str(tv(group(d,lambda e:restrict(e,4)),{p:Q(1,n) for p in parents})),
        }
    def end_law(d):
        return group(d,lambda e:ends[e][2])
    # The end is isomorphic after swapping the temporary marks. A path law
    # and its own relabelling therefore always have identical endpoint weights.
    for e,(_,_,g) in ends.items():
        assert ends[swapped(e)][2] == g
    raw = {v[2] for v in ends.values()}
    end_good = {g for g in raw if (5,g) in states}
    sequential_good = set(end_law(step))
    both_good = set(end_law(symmetric))
    counts = Counter(((4,a) in states,(4,b) in states,(5,c) in states) for a,b,c in ends.values())
    def path_repr(e):
        return [list(pair) for pair in sorted(e)]
    failures = sorted(active-both, key=lambda e:tuple(sorted(e)))
    return {
        "paths":len(ends),"endpoint_types":len(raw),"admissible_end_types":len(end_good),
        "sequential_paths":len(active),"sequential_end_types":len(sequential_good),
        "reverse_also_admissible_paths":len(both),"bidirectional_end_types":len(both_good),
        "forward_only":len(active-both),"end_ok_but_no_admissible_path_types":sorted(end_good-sequential_good),
        "status_counts":{"".join("1" if flag else "0" for flag in k):n for k,n in sorted(counts.items())},
        "matching_count":num_match,"matching_cells":len(cells),"used_cells":len(used),
        "endpoint_TV_step_vs_complete":str(tv(end_law(step),end_law(joint))),
        "endpoint_TV_step_vs_symmetric":str(tv(end_law(step),end_law(symmetric))),
        "witness_forward_only":{"edges":path_repr(failures[0]),"middle_reverse_end_masks":list(ends[failures[0]])},
        "laws":by_law,
        "marked_ledger":[{"edges":path_repr(e),"middle_reverse_end_masks":list(ends[e]),
                          "conditional_weights":{name:str(d.get(e,0)) for name,d in laws.items()}}
                         for e in sorted(ends,key=lambda e:tuple(sorted(e)))],
    }
