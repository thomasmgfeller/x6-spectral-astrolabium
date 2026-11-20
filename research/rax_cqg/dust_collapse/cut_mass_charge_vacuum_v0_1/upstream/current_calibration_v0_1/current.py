"""A conserved marked-edge current; no dynamics or 4D reconstruction is assumed."""
from fractions import Fraction


class Current:
    def __init__(self, nodes, relations, transfers, sources):
        self.nodes = set(nodes)
        if not set(sources) <= self.nodes:
            raise ValueError('source declared at unknown event')
        self.relations = set(relations)
        self.transfers = {e: Fraction(v) for e, v in transfers.items()}
        self.sources = {x: Fraction(sources.get(x, 0)) for x in self.nodes}
        if any(x not in self.nodes or y not in self.nodes or x == y for x, y in self.relations):
            raise ValueError('invalid causal relation')
        if any(e not in self.relations or f < 0 for e, f in self.transfers.items()):
            raise ValueError('transfer must be nonnegative on a declared future relation')
        # Topological elimination checks the declared order generators, not an embedding.
        left = set(self.nodes)
        while left:
            ready = {y for y in left if not any(b == y and a in left for a, b in self.relations)}
            if not ready:
                raise ValueError('causal cycle')
            left -= ready
        if any(self.divergence(x) != self.sources[x] for x in self.nodes):
            raise ValueError('undeclared mass source or sink')

    def divergence(self, x):
        return sum(f for (a, b), f in self.transfers.items() if a == x) - sum(
            f for (a, b), f in self.transfers.items() if b == x)

    def is_past_set(self, past):
        past = set(past)
        return past <= self.nodes and all(y not in past or x in past for x, y in self.relations)

    def cut_mass(self, past):
        past = set(past)
        if not self.is_past_set(past):
            raise ValueError('cut must be a down-set')
        return sum(f for (x, y), f in self.transfers.items() if x in past and y not in past)

    def outward(self, region):
        region = set(region)
        if not region <= self.nodes:
            raise ValueError('unknown event in region')
        return sum(f * (int(x in region) - int(y in region))
                   for (x, y), f in self.transfers.items())

    def weak_pairing(self, phi):
        return sum(f * (Fraction(phi[y]) - Fraction(phi[x]))
                   for (x, y), f in self.transfers.items())

    def coarse_grain(self, blocks):
        if set(blocks) != self.nodes:
            raise ValueError('partition must cover all nodes')
        rel = {(blocks[x], blocks[y]) for x, y in self.relations if blocks[x] != blocks[y]}
        trans = {}
        for (x, y), f in self.transfers.items():
            a, b = blocks[x], blocks[y]
            if a != b:
                trans[a, b] = trans.get((a, b), Fraction(0)) + f
        src = {a: sum(self.sources[x] for x in self.nodes if blocks[x] == a) for a in set(blocks.values())}
        return Current(set(blocks.values()), rel, trans, src)
