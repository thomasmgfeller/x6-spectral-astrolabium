"""Marked one-node extensions and exact PR 295 scalar screen."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"reference"))
import geometry as scalar
from geometry import P,F

INNER=(4,5,6,11)
PAIRS=tuple(combinations(INNER,2))
BASE=("chain","one")


def transitive(edges):
    return all((a,d) in edges for a,b in edges for c,d in edges if b==c)


@lru_cache(None)
def canonical(edges):
    """Least forward-edge bit mask over all topological labellings."""
    ids=[]
    for perm in permutations(INNER):
        labels=dict(zip(INNER,perm))
        rel={(labels[i],labels[j]) for i,j in edges}
        if all(a<b for a,b in rel):
            ids.append(sum(1<<i for i,e in enumerate(PAIRS) if e in rel))
    return min(ids)


def bits_to_edges(mask):
    return tuple(e for i,e in enumerate(PAIRS) if mask & (1<<i))


def enumerate_extensions():
    families={}
    for parent in BASE:
        old=set(map(tuple,scalar.CONTRACT["interior"][parent]))
        members=[]
        for pattern in product((-1,0,1),repeat=3):
            rel=old|{(i,11) if s<0 else (11,i) for i,s in zip(INNER[:3],pattern) if s}
            if transitive(rel):
                assert {(a,b) for a,b in rel if 11 not in (a,b)}==old
                members.append({"relations_to_new":list(pattern),"mask":canonical(frozenset(rel))})
        families[parent]=members
    # Independent enumeration of ALL posets on four labelled vertices, followed
    # by deletion of the marked node and selection of the exact two parent orders.
    allpairs=tuple((a,b) for a in INNER for b in INNER if a!=b)
    hist={p:Counter() for p in BASE};count=0
    parentsets={p:set(map(tuple,scalar.CONTRACT["interior"][p])) for p in BASE}
    for mask in range(1<<12):
        rel={e for i,e in enumerate(allpairs) if mask & (1<<i)}
        if not transitive(rel): continue
        count+=1
        restricted={e for e in rel if 11 not in e}
        for p in BASE:
            if restricted==parentsets[p]: hist[p][canonical(frozenset(rel))]+=1
    assert count==219
    for p in BASE:
        assert hist[p]==Counter(m["mask"] for m in families[p])
    return families


def name(mask):
    return f"poset{mask:02d}_lift"


def screen():
    scalar.mp.mp.dps=55
    families=enumerate_extensions(); states={}; audit={}
    for p in BASE:
        audit[p],states[p]=scalar.kernel(p)
    masks=sorted({entry["mask"] for rows in families.values() for entry in rows})
    for mask in masks:
        nm=name(mask)
        # Add the explicit four-point relation under a fresh runtime key. The
        # inherited rigging reads the same list and preserves all collar labels.
        scalar.CONTRACT["interior"][nm.removesuffix("_lift")]=bits_to_edges(mask)
        info,state=scalar.kernel(nm)
        audit[nm]=dict(info,canonical_mask=mask,inner_relations=bits_to_edges(mask))
        if state is not None: states[nm]=state
    return families,audit,states
