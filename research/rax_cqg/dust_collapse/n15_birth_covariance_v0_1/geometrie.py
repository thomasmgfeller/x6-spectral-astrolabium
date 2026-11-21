"""Finite labelled inputs, path profiles, exact action and charge certificates."""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb

import numpy as np
import density_translation_375841 as intervals

LAYERS = (1, -9, 16, -8)


def linear_extensions(nodes, edges):
    """Generate topological orders, independent of the two-chain description."""
    if not nodes:
        yield ()
        return
    for v in nodes:
        if all(b != v or a not in nodes for a, b in edges):
            for tail in linear_extensions(tuple(n for n in nodes if n != v), edges):
                yield (v,) + tail


def pair_code(order, edges):
    return sum(1 << i for i, edge in enumerate(combinations(order, 2)) if edge in edges)


@dataclass(frozen=True)
class Input:
    past: tuple
    inside: tuple
    future: tuple
    axes: tuple
    relation: frozenset

    def transport(self, mapping):
        def move(row):
            return tuple(mapping[v] for v in row)
        return Input(move(self.past), tuple(sorted(move(self.inside))), move(self.future),
                     move(self.axes), frozenset(move(edge) for edge in self.relation))


class Geometry:
    def __init__(self, data):
        self.data = data
        self.b = np.zeros((15, 15), dtype=int)
        for a, b in data.relation:
            size = sum((a, v) in data.relation and (v, b) in data.relation for v in range(15))
            self.b[a, b] = LAYERS[size] if size < len(LAYERS) else 0
        self.gravity = int(15 - self.b.sum())
        self.hessian2 = self.b + self.b.T - np.diag(self.b.sum(axis=0) + self.b.sum(axis=1))
        self.inner_edges = {(a,b) for a,b in data.relation if a in data.inside and b in data.inside}
        self.paths = self.maximal_paths()
        height = max(map(len, self.paths))
        self.centers = {v: Q(max(path.index(v)+1 for path in self.paths if v in path), height+1)
                        for v in data.inside}

    def maximal_paths(self):
        covers = {(a,b) for a,b in self.inner_edges
                  if not any((a,v) in self.inner_edges and (v,b) in self.inner_edges
                             for v in self.data.inside)}
        def expand(prefix):
            more = sorted(b for a,b in covers if a == prefix[-1])
            if not more:
                yield prefix
            for b in more:
                yield from expand(prefix + (b,))
        return sorted(p for v in self.data.inside if all(b != v for _,b in covers)
                      for p in expand((v,)))

    def endpoint_weight(self, edge_law, chain_law):
        # Lookup by the whole orbit, without assuming that the integer encoding
        # of this presentation is the archive key (or that the key is minimal).
        codes = {str(pair_code(row, self.inner_edges))
                 for row in linear_extensions(self.data.inside, self.inner_edges)}
        matched = codes & (edge_law.keys() | chain_law.keys())
        if len(codes) != 35 or matched != {'375841'}:
            raise ValueError(f"Unexpected archive-key match: {matched}")
        key, = matched
        return (Q(edge_law.get(key, 0)) + Q(chain_law.get(key, 0))) / 2

    def charge(self, radius, axes=None):
        """Rational interval extension over e,u,xi; rows kept in native input IDs."""
        box, add, sub = intervals.box, intervals.plus, intervals.minus
        mul, scale, sq, total = intervals.times, intervals.scale, intervals.square, intervals.add_all
        past, inner = self.data.past, self.data.inside
        e = box(Q(-1,4), radius)
        u = {v:box(self.centers[v], radius) for v in inner}
        dwell = {v:box(0) for v in inner}
        for path in self.paths:
            cuts = [box(0)] + [scale(Q(1,2),add(u[a],u[b])) for a,b in zip(path,path[1:])] + [box(1)]
            for v,lo,hi in zip(path,cuts,cuts[1:]):
                assert lo[1] < hi[0]
                dwell[v] = add(dwell[v],scale(Q(1,len(self.paths)),sub(hi,lo)))
        y = {v:box(j-5) for j,v in enumerate(past)}
        y[past[-1]] = add(y[past[-1]],e)
        duration = sub(box(4), e)
        y.update({v:add(add(box(-2),e),mul(duration,u[v])) for v in inner})
        row, derivative = {}, {}
        for v in inner:
            row[v] = add(box(1),scale(Q(1,19),total(
                scale(int(self.b[a,v]),sq(sub(y[v],y[a]))) for a in y if (a,v) in self.data.relation)))
            derivative[v] = mul(scale(Q(1,19),duration),total(
                scale(int(self.b[a,v]),sub(y[a],y[v])) for a in past))
        a,b,c = axes if axes is not None else self.data.axes
        shift = dict.fromkeys(inner,box(0))
        for target,left,right in ((a,b,c),(b,c,a),(c,a,b)):
            shift[target] = scale(Q(7600,8_000_000),sub(row[left],row[right]))
        if not radius:
            assert sum(shift[v][0] for v in inner) == 0
            assert sum(row[v][0]*shift[v][0] for v in inner) == 0
        result = []
        for direction in (-1,1):
            density = {}
            for v in inner:
                diff = add(scale(direction,shift[v]),box(0,radius))
                assert max(map(abs,diff)) < dwell[v][0]/100
                density[v] = add(dwell[v],diff)
                assert 0 < density[v][0] and Q(1,4)*Q(13,50)*duration[1]*density[v][1] < 1
            result.append(total(mul(density[v],derivative[v]) for v in inner))
        return tuple(result)


def enumerate_orders(ref):
    inner = ref.data.inside
    generated = list(linear_extensions(inner, ref.inner_edges))
    # Independent exhaustive check using every one of the 7! permutations.
    a,b = sorted(ref.paths,key=len)
    assert len(a) == 3 and len(b) == 4
    assert set(a).isdisjoint(b) and set(a+b) == set(inner)
    shuffle = {o for o in permutations(inner)
               if tuple(v for v in o if v in a) == a and tuple(v for v in o if v in b) == b}
    assert set(generated) == shuffle and len(generated) == len(shuffle) == comb(7,3)
    return generated


def exact_transport(ref, new, labels):
    """Finite coefficient certificate for equality of the full integrands."""
    d, t = ref.data, new.data
    pull = [labels[v] for v in range(15)]
    assert sorted(pull) == list(range(15))
    assert all((labels[a],labels[b]) in t.relation for a,b in d.relation)
    assert len(t.relation) == len(d.relation)
    ix = np.ix_(pull, pull)
    assert np.array_equal(new.b[ix],ref.b) and np.array_equal(new.hessian2[ix],ref.hessian2)
    assert new.gravity == ref.gravity
    assert all(new.centers[labels[v]] == ref.centers[v] for v in d.inside)
    assert {tuple(labels[v] for v in p) for p in ref.paths} == set(new.paths)
    assert tuple(labels[v] for v in d.axes) == t.axes
    assert tuple(labels[v] for v in d.past) == t.past
    assert tuple(labels[v] for v in d.future) == t.future
    assert not new.b[np.ix_(t.past,t.future)].any()
    # Rows, paths, ordered cofactor axes, and product boxes now fix C, k, f,
    # d, both selector domains, and the regulated scalar action at every point.
