"""Minimal parallel interpolation between the existing send and receive events."""
from fractions import Fraction as F


def diamond_extension(order, nodes):
    sender, receiver, positive, empty = 16, 18, 19, 20
    assert (sender, receiver) in order
    assert not {i for i in nodes if (sender, i) in order and (i, receiver) in order}
    lower = {sender} | {p for p in nodes if (p, sender) in order}
    upper = {receiver} | {q for q in nodes if (receiver, q) in order}
    ext = order | {(p, n) for p in lower for n in (positive, empty)}
    ext |= {(n, q) for q in upper for n in (positive, empty)}
    assert {(p, q) for p, q in ext if p in nodes and q in nodes} == order
    assert all(p != q for p, q in ext)
    assert all((p, r) in ext for p, q in ext for j, r in ext if q == j)
    assert (positive, empty) not in ext and (empty, positive) not in ext
    def edges(target):
        all_nodes = nodes | {positive, empty}
        coeff = (1, -9, 16, -8)
        counts = {p:sum((p, j) in ext and (j, target) in ext for j in all_nodes)
                  for p in all_nodes if (p, target) in ext}
        return {p: coeff[n] if n < 4 else 0 for p,n in counts.items()}
    return ext, edges(positive)


def density_gradient(Y, coefficients):
    from quelle import box, hull
    from speichermodell import square
    ymin = F(Y[16].data()[0])
    ymax = F(Y[18].data()[1])
    new_clock = hull(ymin, ymax)
    contributions = [c*square(new_clock-Y[p]) for p,c in coefficients.items() if c]
    interval = sum(contributions, box(19))
    return interval.data()


def predecessor_families(order, nodes):
    from itertools import combinations
    lower = {16} | {i for i in nodes if (i,16) in order}
    upper = {i for i in nodes if (i,18) in order}
    free = sorted(upper - lower)
    def ideal(s):
        return all(v not in s or u in s for u,v in order)
    possibilities = {frozenset(lower | set(extra)) for k in range(len(free)+1)
                     for extra in combinations(free,k) if ideal(lower | set(extra))}
    other = {frozenset(lower)}
    while True:
        larger = other | {s | {v} for s in other for v in free if v not in s and ideal(s | {v})}
        if larger == other:
            break
        other = larger
    assert other == possibilities
    result = []
    for s in sorted(possibilities, key=lambda subset:(len(subset), sorted(subset))):
        # Construct a witness extension with exactly this past at 19.
        ext, _ = diamond_extension(order, nodes)
        ext |= {(u,19) for u in s}
        assert all((p,r) in ext for p,q in ext for j,r in ext if q==j)
        assert not ((19,20) in ext or (20,19) in ext)
        assert {u for u,v in ext if v==19} == s
        weights = (1,-9,16,-8)
        coeff = {i:next((w for k,w in enumerate(weights) if k==sum((i,j) in order for j in s)),0)
                 for i in s}
        result.append((sorted(s),coeff))
    return result


def receiver_bound(state, coeff, velocity, k):
    """Use the receiver's own stationarity equation before interval evaluation."""
    from quelle import box, hull
    from speichermodell import square
    from gemischt import COEFF
    Y, W = state['y'], state['w']
    r, s, h = Y[18], Y[16], Y[17]
    assert coeff == {i:c for (i,j),c in COEFF.items() if j==18}
    # Both clocks sampled on arrival at 18 have mismatch -k. All three pointers
    # have conserved discrete momentum k*v and use W[18] for inertia at 18.
    endpoint = k*(square(r-s) + square(r-h)) - k*sum((square(v) for v in velocity),box(0))/square(W[18])
    full = hull(F(s.data()[0]),F(r.data()[1]))
    slope = sum((2*c*(full-Y[i]) for i,c in coeff.items() if c),box(0))
    direct = sum((c*square(r-Y[i]) for i,c in coeff.items() if c),box(19))
    assert max(endpoint.lo,direct.lo) <= min(endpoint.hi,direct.hi)
    return {'receiver_gradient':endpoint.data(), 'slope':slope.data()}
