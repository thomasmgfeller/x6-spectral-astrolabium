"""Finite antichains and mod-two homology of unions of anchored shadows."""
from itertools import combinations
from collections import Counter

def all_antichains(nodes, relation):
    family = {frozenset()}
    for v in sorted(nodes):
        family |= {a | {v} for a in family if all(
            (u,v) not in relation and (v,u) not in relation for u in a)}
    return family

def rank(columns):
    pivots = {}
    for column in columns:
        while column:
            i = column.bit_length()-1
            if i not in pivots:
                pivots[i] = column
                break
            column ^= pivots[i]
    return len(pivots)

def boundary_rank(high, low):
    index = {face:i for i,face in enumerate(low)}
    return rank(sum(1 << index[facet] for facet in combinations(cell,len(cell)-1))
                for cell in high)

def betti2(facets):
    # All faces up to dimension 3 suffice for H2.
    def cells(n):
        return sorted({c for f in facets for c in combinations(sorted(f),n)})
    edges, triangles, tetrahedra = map(cells,(2,3,4))
    return len(triangles)-boundary_rank(triangles,edges)-boundary_rank(tetrahedra,triangles)

def enumerate_shadows(nodes, relation, pair):
    family = all_antichains(nodes,relation)
    maximal = {a for a in family if all(a|{v} not in family for v in nodes-a)}
    assert len(maximal)==37 and len(family)==337
    assert all((0,j) in relation and (j,21) in relation for j in pair)
    assert all(((i,17) in relation)==((i,20) in relation) and
               ((17,i) in relation)==((20,i) in relation) for i in nodes)
    slices = sorted((a for a in maximal if {17,19}<=a), key=lambda a:(len(a),sorted(a)))
    assert len(slices)==6 and all(set(pair)<=a for a in slices)
    rows=[]
    for a in sorted(family-{frozenset()},key=lambda a:(len(a),sorted(a))):
        shadows = {frozenset(u for u in a if (u,v) in relation) for v in nodes-a}
        shadows |= {frozenset(u for u in a if (v,u) in relation) for v in nodes-a}
        while True:
            expanded = shadows | {x&y for x in shadows for y in shadows}
            if expanded==shadows: break
            shadows = expanded
        proper = sorted((s for s in shadows if 1<len(s)<len(a)),key=lambda s:(len(s),sorted(s)))
        counts = Counter()
        for n in range(len(proper)+1):
            for group in combinations(proper,n):
                counts[betti2(group+tuple((v,) for v in a))] += 1
        rows.append(dict(cut=sorted(a),maximal=a in maximal,proper=[sorted(s) for s in proper],
                         families=sum(counts.values()),max_betti2=max(counts)))
    test = tuple(combinations(range(4),3))
    assert betti2(test)==1 and betti2([range(4)])==0
    assert betti2(test+tuple(tuple(v+4 for v in f) for f in test))==2
    return dict(nonempty_antichains=len(rows),maximal=len(maximal),contact_slices=[sorted(a) for a in slices],
                proper_families=sum(q['families'] for q in rows),max_betti2=max(q['max_betti2'] for q in rows),rows=rows)
