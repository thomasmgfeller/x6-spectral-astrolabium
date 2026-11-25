"""Exterior clock test on the original order and a one-event extension."""
from bisect import bisect_right
from collections import Counter


def histories(start=1, prefix=()):
    """All retreat schedules in ticks 1..48 with gaps of at least 12."""
    yield prefix
    for tick in range(start, 49):
        yield from histories(tick + 12, prefix + (tick,))


def causal(p, v):
    # Double spatial coordinates permit inserting a half-station.
    return v[0] > p[0] and v[0] - p[0] >= 6 * abs(v[1] - p[1])


def count_interval(p, v, extra=()):
    # All original station columns in the diamond, plus any inserted point.
    sites = ((t, 2*j) for t in range(p[0]+1, v[0])
             for j in range(p[1]//2-5, p[1]//2+6))
    return sum(causal(p, z) and causal(z, v) for z in sites) + sum(
        causal(p, z) and causal(z, v) for z in extra)


def kernel(n):
    return (1, -9, 16, -8)[n] if n < 4 else 0


def front_test(stencil):
    # Reconstruct all short-distance coefficients by direct order comparisons.
    direct = []
    for d in range(1, 61):
        for s in range(-5, 6):
            p, v = (0, 0), (d, 2*s)
            if causal(p, v):
                b = kernel(count_interval(p, v))
                if b:
                    direct.append((d, s, b))
    assert sorted(direct) == sorted(stencil)
    counts = Counter()
    for retreats in histories():
        counts['all_schedules'] += 1
        if any(t > 36 for t in retreats):
            continue
        counts['plateau_schedules'] += 1
        j = 4 - len(retreats)  # R(0)=0
        assert j > 0
        reached = [(d, s, b) for d, s, b in direct
                   if j+s <= -bisect_right(retreats, d)]
        assert reached == [(48, -4, -8)]
    # Limiting control. A front retreating every 12 ticks has no occupied
    # receiver from even the first exterior station, for any source phase.
    for phase in range(12):
        assert all(1+s > -((phase+d)//12) for d, s, _ in direct)
    counts['null_phases_without_exterior_contact'] = 12

    # Uniform positive density 1/4 up to R(t), zero beyond; affine clock Y=h*t.
    def radius(t):
        return 32-t//24

    def clock_test(t, extra):
        j = radius(t+48)+4
        p = (t, 2*j)
        assert j > radius(t)
        active = []
        # Inserting an event cannot reactivate an old interval of size >=4.
        for d, s, _ in direct:
            v = (t+d, 2*(j+s))
            if v[1] <= 2*radius(v[0]):
                b = kernel(count_interval(p, v, extra))
                if b:
                    active.append([v[0], v[1], b, d])
        for z in extra:
            assert z[1] > 2*radius(z[0])  # inserted vacuum density
        numerator = sum(b*d for _, _, b, d in active)
        assert numerator % 4 == 0  # integer-valued for the two declared probes
        return numerator//4, active

    u, v, z = (95, 62), (143, 54), (137, 55)
    assert causal(u,z) and causal(z,v)
    before = clock_test(95, ())
    after = clock_test(95, (z,))
    later = clock_test(167, (z,))
    assert (count_interval(u,v), count_interval(u,v,(z,))) == (3,4)
    assert (before[0], after[0], later[0]) == (-96,0,-96)
    return {'schedules': dict(counts), 'old_interval_counts': [3,4],
            'extension': {'base_at_tick_95': before, 'modified_at_tick_95': after,
                          'modified_at_tick_167': later,
                          'inserted_tick_and_double_station': z}}
