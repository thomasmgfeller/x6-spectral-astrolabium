"""Coordinate-blind event counts with labelled, non-counting boundary probes."""
import numpy as np
from od_common import core


class PhysicalPoset(core.Poset):
    def __init__(self, relation, marks, probes):
        super().__init__(relation, marks)
        mask = (1 << self.size) - 1
        for a in probes:
            mask &= ~(1 << int(a))
        # Query endpoints can be probes, but interiors/candidate sets are events.
        self.succ = [bits & mask for bits in self.succ]
        self.pred = [bits & mask for bits in self.pred]


def root_counts(g, s, colours):
    if s['status'] != 'ok':
        return None
    bits = [int.from_bytes(np.packbits(colours == i, bitorder='little').tobytes(), 'little') for i in (0, 1)]
    out = []
    for b in s['support']:
        a, d = (s['root'], b) if g.r[s['root'], b] else (b, s['root'])
        assert g.r[a, d]
        interior = g.succ[a] & g.pred[d]
        out.append(dict(point=b, count=interior.bit_count(), halves=[(interior & q).bit_count() for q in bits]))
    return out


def chain_witness(g, eligible, threshold=8):
    """Exhaustive existence search over middle vertices, with an explicit witness."""
    mask = sum(1 << int(a) for a in eligible)
    for b in eligible:
        before = g.pred[b] & mask
        after = g.succ[b] & mask
        if not before or not after:
            continue
        a = next((a for a in core.indices(before) if g.interval(a, b) >= threshold), None)
        if a is None:
            continue
        d = next((d for d in core.indices(after) if g.interval(b, d) >= threshold), None)
        if d is not None:
            counts = [g.interval(a, b), g.interval(b, d), g.interval(a, d)]
            assert min(counts) >= threshold
            return dict(events=[a, b, d], intervals=counts)
    return None


def coverage(g, s, c):
    if s['status'] != 'ok':
        return dict(status=s['status'])
    out = {}
    points = [s['root']] + s['support']
    for name, cones in [('past', g.pred), ('future', g.succ)]:
        common = (1 << g.size) - 1
        for b in points:
            common &= cones[b]
        eligible = []
        for a in core.indices(common):
            counts = [(g.succ[a] & g.pred[b]).bit_count() if g.r[a, b]
                      else (g.succ[b] & g.pred[a]).bit_count() for b in points]
            if min(counts) >= c['landmark_min_interval']:
                eligible.append(a)
        eligible.sort(key=lambda a: g.marks[a])
        out[name] = dict(common=common.bit_count(), eligible=len(eligible),
                         witness=chain_witness(g, eligible, c['landmark_min_interval']))
    return dict(status='ok', sides=out)
