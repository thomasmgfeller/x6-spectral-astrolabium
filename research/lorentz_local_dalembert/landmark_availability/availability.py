"""Exhaustive conditional order diagnostics; no coordinates or fitted weights."""
import numpy as np

THRESHOLDS = (0, 1, 2, 4, 8, 16)


def chain_stats(weights, labels):
    w = np.asarray(weights)
    n = len(labels)
    counts = {}
    for k in THRESHOLDS:
        edges = w >= k
        counts[str(k)] = int(edges.sum(axis=0) @ edges.sum(axis=1))
    if n:
        incoming = w.max(axis=0)
        outgoing = w.max(axis=1)
        bottlenecks = np.minimum(incoming, outgoing)
        b = int(np.argmax(bottlenecks))
        maximum = float(bottlenecks[b])
    else:
        maximum = -1.
    witness = None
    if maximum >= 0:
        a, c = int(np.argmax(w[:, b])), int(np.argmax(w[b, :]))
        assert w[a, c] >= maximum
        witness = dict(events=[int(labels[i]) for i in (a, b, c)],
                       intervals=[float(w[a, b]), float(w[b, c]), float(w[a, c])])
    # Relation indegree topologically orders any finite transitive order.
    order = np.argsort((w >= 0).sum(axis=0), kind='stable')
    heights = np.ones(n, dtype=int)
    for b in order:
        pred = np.flatnonzero(w[:, b] >= 8)
        if len(pred):
            heights[b] = int(heights[pred].max()) + 1
    return dict(candidates=n, triples=counts, maximum_bottleneck=maximum,
                witness=witness, threshold8_height=int(heights.max()) if n else 0)


def candidates(g, points, boundary, side):
    cone = g.pred if side == 'past' else g.succ
    bits = (1 << g.size) - 1
    for b in points:
        bits &= cone[b]
    for b in boundary:
        bits &= ~(1 << b)
    result = []
    while bits:
        low = bits & -bits
        result.append(low.bit_length() - 1)
        bits ^= low
    return sorted(result, key=lambda a: g.marks[a])


def diagnose_side(g, points, boundary, side, measure=None):
    def count(a, b):
        if g.r[b, a]:
            a, b = b, a
        assert g.r[a, b]
        return g.interval(a, b) if measure is None else measure(a, b)
    common = candidates(g, points, boundary, side)
    minima = [min(count(a, b) for b in points) for a in common]
    eligible = [a for a, value in zip(common, minima) if value >= 8]
    w = np.full((len(eligible), len(eligible)), -1., dtype=float)
    for i, a in enumerate(eligible):
        for j, b in enumerate(eligible):
            if g.r[a, b]:
                w[i, j] = count(a, b)
    endpoint = boundary[0 if side == 'past' else 1]
    outer = min(count(endpoint, b) for b in points)
    out = dict(common_count=len(common), eligible_events=eligible,
               maximum_support_minimum=float(max(minima)) if minima else None,
               minimum_boundary_interval=float(outer),
               all=chain_stats(w, eligible), capped40=chain_stats(w[:40, :40], eligible[:40]))
    if measure is None:
        out['packing_impossible'] = bool(outer < 27 or len(common) < 19)
        if out['packing_impossible']:
            assert out['all']['triples']['8'] == 0
    return out


def diagnose(g, selection, boundary, measure=None):
    if selection['status'] != 'ok':
        return dict(status=selection['status'])
    root = selection['root']
    views = dict(full=[root] + selection['support'],
                 temporal=[root] + selection['temporal'],
                 shell=[root] + [a for a in selection['support'] if a not in selection['temporal']],
                 root=[root])
    return dict(status='ok', views={name: {
        side: diagnose_side(g, points, boundary, side, measure) for side in ('past', 'future')
    } for name, points in views.items()})
