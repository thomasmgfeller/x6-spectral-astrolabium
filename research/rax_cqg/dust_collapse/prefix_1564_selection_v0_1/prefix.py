"""Disintegrate the archived positive exchangeable witness on marked prefix 1564."""
import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path

BASE=Path(__file__).resolve().parent
INPUT=BASE/'inputs'
PREFIX=1564
A,B=1790,5374
PAIR_MASK=sum(1<<(6*i+j) for i in range(5) for j in range(5) if i!=j)
MARKS=tuple((0,1,2,*p) for p in permutations((3,4,5)))


def read(name):
    return json.loads((INPUT/name).read_text())


def edges(code):
    return [(i,j) for i in range(6) for j in range(6) if code & (1<<(6*i+j))]


def encode(rels, perm):
    return sum(1<<(6*perm[i]+perm[j]) for i,j in rels)


def canonical(rels,n):
    pairs=list(combinations(range(n),2))
    candidates=[]
    for perm in permutations(range(n)):
        renamed=[(perm[i],perm[j]) for i,j in rels]
        if all(i<j for i,j in renamed):
            candidates.append(sum(1<<pairs.index(edge) for edge in renamed))
    return min(candidates)


def row():
    data=read('exchange.json')['one']
    target={int(k):F(v) for k,v in data['target_pair_marginal'].items()}
    ordered={}
    for code,weight in target.items():
        variants={code,encode(edges(code),(0,1,2,4,3,5))}
        for c in variants:
            ordered[c]=weight/len(variants)
    prior=ordered[PREFIX]
    assert prior==F(1,147)
    each=F(data['max_uniform_labelled_path_component'])/data['paths_valid_in_all_six_orders']
    residual=read('exchange_certificate.json')['one']['residual_orbit_masses']
    rest=1-F(data['max_uniform_labelled_path_component'])
    paths=[]
    for end in data['fully_admissible_end_types']:
        rels=[p for k,p in enumerate(combinations(range(6),2)) if end&(1<<k)]
        for c in {encode(rels,perm) for perm in permutations(range(6))}:
            if (c&PAIR_MASK)!=PREFIX:
                continue
            orbit={encode(edges(c),p) for p in MARKS}
            if all((x&PAIR_MASK) in ordered for x in orbit):
                mass=each+rest*F(residual.get(str(min(orbit)),0))/len(orbit)
                paths.append((int(end),c,mass/prior))
    paths.sort()
    by_type=Counter()
    for end,_,r in paths:
        by_type[end]+=r
    assert sum(by_type.values())==1 and len(paths)==16 and len(by_type)==10
    assert by_type[A]==by_type[B]==F(1,18)
    assert canonical(edges(PREFIX),5)==62
    assert {c for end,c,_ in paths if end in (A,B)}=={25769807420,545263164}
    # delta in conditional coefficients per unit t on the original orbit mass.
    scale=1/(3*prior)
    assert scale==49
    assert by_type[A]-scale*F(1,1764)==F(1,36)
    assert by_type[B]+scale*F(1,1764)==F(1,12)
    archives=read('weights.json')
    assert F(archives['base_mass_per_selected_orbit'])==F(1,882)
    for branch,end in [('A',A),('B',B)]:
        c,= [child for j,child,_ in paths if j==end]
        assert c in archives[branch]['codes']
        assert len(archives[branch]['codes'])==3
    examples=read('memory.json')['roots']['one']
    for value in (F(-1,1764),F(0),F(1,1764)):
        saved=examples[str(value)]['example']
        assert saved['prefix_code']==PREFIX and F(saved['prefix_coefficient'])==prior
        assert [F(v) for v in saved['individual_transition_coefficients']]==[
            by_type[A]-scale*value,by_type[B]+scale*value]
    return paths,by_type
