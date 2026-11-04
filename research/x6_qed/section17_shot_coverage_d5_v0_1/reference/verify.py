"""Independent half-path joins and explicit matching enumeration for verification."""
from functools import lru_cache
from itertools import combinations, product


class ExhaustiveCheck:
    def __init__(self, adj):
        self.adj = adj
        self.halves = []
        self.closed_neighbours = []
        for u, row in enumerate(adj):
            walks = [((u,),0)]
            for v, a in row:
                if v < 0:
                    continue
                walks.append(((u,v),a))
                for w,b in adj[v]:
                    if w >= 0 and w != u:
                        walks.append(((u,v,w), a^b))
            by_tip = {}
            for path, bit in walks:
                by_tip.setdefault(path[-1], []).append((path,bit))
            self.halves.append(by_tip)
            self.closed_neighbours.append({u} | {v for v,_ in row if v>=0})

    @lru_cache(None)
    def pair_paths(self, u, v):
        paths = set()
        if v < 0:
            for last, halves in self.halves[u].items():
                end_masks = [m for w,m in self.adj[last] if w < 0]
                for path, mask in halves:
                    if len(path) <= 2:
                        for end in end_masks:
                            paths.add((frozenset(path[1:]),mask ^ end))
        else:
            left, right = self.halves[u], self.halves[v]
            for tip in left.keys() & right.keys():
                for (p,a),(q,b) in product(left[tip],right[tip]):
                    if set(p) & set(q) == {tip}:
                        paths.add((frozenset((set(p)|set(q))-{u,v}),a^b))
        return paths

    def analyse(self, active):
        groups = [{v} for v in active]
        for u,v in combinations(active,2):
            if self.closed_neighbours[u] & self.closed_neighbours[v]:
                left = next(g for g in groups if u in g)
                right = next(g for g in groups if v in g)
                if left is not right:
                    groups.remove(right)
                    left.update(right)
        all_active = set(active)
        result = []
        for g in groups:
            possible = set()
            pairs = list(combinations(sorted(g),2))
            for pair_count in range(len(g)//2 + 1):
                for selected in combinations(pairs, pair_count):
                    covered = {v for pair in selected for v in pair}
                    if len(covered) != 2*pair_count:
                        continue
                    assignment = list(selected) + [(u,-1) for u in sorted(g-covered)]
                    supports = [{b for internal,b in self.pair_paths(u,v) if all_active.isdisjoint(internal)}
                                for u,v in assignment]
                    for bits in product(*supports):
                        possible.add(sum(bits)%2)
            result.append((tuple(sorted(g)),sum(1 << b for b in possible)))
        return sorted(result)
