"""Independent finite enumeration and transport checks for availability audit."""
import itertools
import numpy as np
from availability import chain_stats, diagnose, diagnose_side, THRESHOLDS


def check(core):
    rng = np.random.default_rng(9637821)
    checked = 0
    for n in range(3, 23):
        for _ in range(5):
            r = np.triu(rng.random((n, n)) < .24, 1)
            for k in range(n):
                r |= r[:, k, None] & r[None, k, :]
            g = core.Poset(r, rng.random(n))
            w = np.array([[g.interval(a, b) if r[a, b] else -1 for b in range(n)] for a in range(n)])
            result = chain_stats(w, list(range(n)))
            scores = [min(w[a, b], w[b, c], w[a, c]) for a, b, c in itertools.combinations(range(n), 3)
                      if r[a, b] and r[b, c] and r[a, c]]
            assert result['maximum_bottleneck'] == max(scores, default=-1)
            for k in THRESHOLDS:
                assert result['triples'][str(k)] == sum(v >= k for v in scores)
            # Separate recursive exhaustive path enumeration on small graphs.
            def height(a):
                return 1 + max((height(b) for b in range(a + 1, n) if w[a, b] >= 8), default=0)
            assert result['threshold8_height'] == max(map(height, range(n)))
            checked += 1
    # A linear order has a future triple at k=8 exactly once N(s,T)>=27.
    for interior in (26, 27, 28):
        n = interior + 3
        g = core.Poset(np.triu(np.ones((n, n), bool), 1), np.arange(n, dtype=float))
        row = diagnose_side(g, [1], [0, n - 1], 'future')
        assert row['minimum_boundary_interval'] == interior
        assert bool(row['all']['triples']['8']) == (interior >= 27)
    return dict(brute_force_orders=checked, packing_bound_controls=3, status='PASS')


def transport(core, g, s, boundary, original, seed):
    p = np.random.default_rng(seed ^ 38123).permutation(g.size)
    inv = np.argsort(p)
    h = core.Poset(g.r[np.ix_(p, p)], g.marks[p])
    mapped = {**s, 'root': int(inv[s['root']]),
              'support': [int(inv[a]) for a in s['support']],
              'temporal': [int(inv[a]) for a in s['temporal']]}
    relabeled = diagnose(h, mapped, [int(inv[a]) for a in boundary])
    for views in relabeled.get('views', {}).values():
        for row in views.values():
            row['eligible_events'] = [int(p[a]) for a in row['eligible_events']]
            for name in ('all', 'capped40'):
                if row[name]['witness']:
                    row[name]['witness']['events'] = [int(p[a]) for a in row[name]['witness']['events']]
    assert relabeled == original
    reverse = diagnose(core.Poset(g.r.T, g.marks), s, boundary[::-1])
    for name, views in original['views'].items():
        for side, other in (('past', 'future'), ('future', 'past')):
            a, b = views[side], reverse['views'][name][other]
            for key in ('common_count', 'eligible_events', 'maximum_support_minimum',
                        'minimum_boundary_interval', 'packing_impossible'):
                assert a[key] == b[key]
            for cap in ('all', 'capped40'):
                for key in ('candidates', 'triples', 'maximum_bottleneck', 'threshold8_height'):
                    assert a[cap][key] == b[cap][key]
                # Several maximal witnesses may tie; the invariant is the maximum.
    return dict(relabeling='PASS', time_reversal='PASS')
