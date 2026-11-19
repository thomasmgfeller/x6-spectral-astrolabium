"""Exact three-time cut laws, compared against independent enumeration of all clock bins."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import prod
import json
from ideals import cut_cell, frontier, ideals, intersect, minkowski_order, volume

CUTS = (Q(1,2),Q(7,12),Q(2,3))
BIN_WEIGHTS = (6,1,1,4)


def cube(predecessors):
    options = ideals(predecessors)
    n = len(predecessors)
    total = 12**n
    joint = Counter()
    indices = range(n)
    # Independent construction from maximum clock over each principal past.
    ancestry = [[j for j in indices if i==j or mask & (1<<j)] for i,mask in enumerate(predecessors)]
    for bins in product(range(4),repeat=n):
        release = [max(bins[j] for j in anc) for anc in ancestry]
        key = tuple(sum(1<<i for i,k in enumerate(release) if k<=s) for s in range(3))
        joint[key] += prod(BIN_WEIGHTS[k] for k in bins)

    cells = [{a:cut_cell(predecessors,a,t,Q(0),Q(1)) for a in options} for t in CUTS]
    mass = [{a:volume(c) for a,c in layer.items()} for layer in cells]
    assert all(sum(layer.values())==1 for layer in mass)
    def transition(i,j):
        return {(a,b):volume(intersect(cells[i][a],cells[j][b]))/mass[i][a]
                for a in options for b in options}
    k01,k12,k02 = transition(0,1),transition(1,2),transition(0,2)
    for a,b,c in product(options,repeat=3):
        assert mass[0][a]*k01[a,b]*k12[b,c] == Q(joint[a,b,c],total)
    for a,c in product(options,repeat=2):
        assert sum(k01[a,b]*k12[b,c] for b in options)==k02[a,c]
    for kernel in (k01,k12,k02):
        assert all(sum(kernel[a,b] for b in options)==1 for a in options)
    # Removing the censoring of the minimal complement overcounts cut boxes.
    naive_total = sum(CUTS[0]**a.bit_count() for a in options)
    assert naive_total>1
    return {"ideals":len(options),"three_time_ideal_triples_tested":len(options)**3,
            "clock_bin_assignments":4**n,"positive_triples":len(joint),
            "empty_frontier_size":len(frontier(0,predecessors)),
            "no_release_from_0_to_quarter_given_empty":str(k01[0,0]),
            "mass_sum_ignoring_frontier_at_zero":str(naive_total)}


def compute():
    events,example = minkowski_order()
    result = {name:cube(p) for name,p in (("C0",(0,1,3)),("C1",(0,0,1)),("flat_1plus3",example))}
    p0,p1 = (Q(result[k]["no_release_from_0_to_quarter_given_empty"]) for k in ("C0","C1"))
    assert p0==Q(5,6) and p1==Q(25,36)
    return {"cases":result,"empty_prefix_gap":str(p0-p1),
            "common_probability_minimax_error":str((p0-p1)/2),
            "flat_events_txyz":events}


if __name__=='__main__':
    print(json.dumps(compute(),indent=2))
