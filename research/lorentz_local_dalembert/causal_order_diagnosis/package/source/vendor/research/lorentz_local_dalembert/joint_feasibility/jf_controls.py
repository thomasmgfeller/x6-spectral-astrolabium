"""Direct interval oracles, boundary rejections and inference transport."""
import copy
import inspect
import itertools
import numpy as np
from jf_common import core, PhysicalPoset, config
from joint import Counts, select, certificate, design_check, frames
from intrinsic import ETA, normalize, noise_guard
from od_controls import check as inherited_check


def check():
    inherited = inherited_check()
    c, oc, guards, cfg = config()
    n = 22
    relation = np.triu(np.ones((n, n), dtype=np.uint8), 1)
    colours = np.arange(n, dtype=np.uint8) % 2
    probes = [3, 18]
    g = PhysicalPoset(relation, np.random.default_rng(516420).random(n), probes)
    counts = Counts(g, colours, 1000, guards)
    direct = 0
    for a in range(n):
        for b in range(a+1, n):
            ids = [i for i in range(n) if i not in probes and relation[a, i] and relation[i, b]]
            wanted = (len(ids), sum(colours[i] == 0 for i in ids), sum(colours[i] == 1 for i in ids))
            assert counts.values(a, b) == wanted
            assert counts.values(b, a) == wanted
            assert counts.good(a, b) == (wanted[0] >= 16 and min(wanted[1:]) >= 4)
            direct += 1
    assert normalize(np.eye(3), 100) is None
    assert normalize(np.diag([-101., 1., 1.]), 100) is None
    assert normalize(np.diag([-100., 1., 1.]), 100) is not None
    rng = np.random.default_rng(516421)
    z = rng.normal(size=(20, 3))
    assert design_check(z, 1., c)['passed']
    assert not design_check(np.tile([1., 0., 0.], (20, 1)), 1., c)['passed']
    h = ETA.copy(); v = z.T; t = np.eye(3)
    def guard(full=16, halves=(4, 12), gram=None):
        hd = [(h if gram is None else gram, v), (h, v)]
        return noise_guard(h, v, t, hd, [full], [[halves[0]], [halves[1]]], 1., guards)
    assert guard()['passed']
    assert not guard(full=15)['passed']
    assert not guard(halves=(3, 13))['passed']
    assert not guard(gram=np.eye(3))['passed']
    assert not guard(gram=2*ETA)['passed']
    # Small exhaustive chain oracle covers the new mixed-frame enumerator.
    # Toy thresholds are local to this software check, never to real inference.
    toy_guards = {**guards, 'guard_min_interval': 1, 'guard_min_half_interval': 0}
    toy = core.Poset(np.triu(np.ones((20, 20), dtype=np.uint8), 1), rng.random(20))
    toy_counts = Counts(toy, np.arange(20, dtype=np.uint8) % 2, 1000, toy_guards)
    _, funnel = frames(toy, toy_counts, 10, [8, 12], [], c, toy_guards)
    eligible = [a for a in range(20) if all((toy.r[a, b] or toy.r[b, a]) and toy_counts.good(a, b) for b in [8, 10, 12]) and (a < 8 or a > 12)]
    expected = [q for q in itertools.combinations(eligible, 3) if all(toy_counts.good(a, b) for a, b in itertools.combinations(q, 2))]
    assert len(expected) == funnel['count_qualified_triples'] > 0
    mixed = sum(q[0] < 8 and q[-1] > 12 for q in expected)
    assert mixed == funnel['families']['mixed']['count'] > 0
    assert 'audit' not in inspect.signature(select).parameters
    # No simulator/evaluation import or coordinate input in the inference module.
    import joint
    source = inspect.getsource(joint)
    assert 'import experiment' not in source and 'import od_simulation' not in source
    return dict(status='PASS', inherited=inherited, direct_intervals=direct,
                count_boundary_rejections=2, signature_condition_cases=3,
                gram_rejections=2, rank_cases=2, audit_input_separated=True,
                exhaustive_chain_triples=len(expected), mixed_chain_triples=mixed)


def witness_check(g, selected, colours, audit_colours, rho, guards, c):
    if selected is None:
        return dict(status='PASS', applicable=False)
    out = dict(status='PASS', applicable=True, checked_intervals=0)
    for label, colour in [('selection', colours), ('audit', audit_colours)]:
        actual = certificate(g, Counts(g, colour, rho, guards), selected['root'], selected['temporal'],
                             selected['landmarks'], selected['support'], guards)
        physical = np.ones(g.size, bool)
        # A physical endpoint can never appear in its own strict interval;
        # PhysicalPoset masks artificial probes from every interior bitset.
        if hasattr(g, 'probes_for_check'):
            physical[g.probes_for_check] = False
        for pair, full, h0, h1 in zip(actual['interval_pairs'], actual['interval_counts'], *actual['half_interval_counts']):
            a, b = pair
            if g.r[b, a]:
                a, b = b, a
            interior = g.r[a].astype(bool) & g.r[:, b].astype(bool) & physical
            assert int(interior.sum()) == full
            assert int(np.sum(interior & (colour == 0))) == h0
            assert int(np.sum(interior & (colour == 1))) == h1
            out['checked_intervals'] += 1
        out[label+'_guard'] = actual['guard']['passed']
    assert out['selection_guard']
    dc = design_check(selected['certificate']['features'], selected['scale'], c)
    assert dc['passed']
    return out


def transport(g, root, chain, inner, probes, colours, rho, c, guards, scale, expected, seed):
    rng = np.random.default_rng(seed ^ 516422)
    permutation = rng.permutation(g.size); inv = np.argsort(permutation)
    gp = PhysicalPoset(g.r[np.ix_(permutation, permutation)], g.marks[permutation], inv[probes])
    renamed = select(gp, int(inv[root]), [int(inv[b]) for b in chain], inv[inner].tolist(),
                     inv[probes].tolist(), colours[permutation], rho, c, guards, scale)
    del gp
    gr = PhysicalPoset(g.r.T, g.marks, probes)
    reversed_ = select(gr, root, list(reversed(chain)), inner, probes, colours, rho, c, guards, scale)
    del gr
    for row, unmap, reverse in [(renamed, lambda a: int(permutation[a]), False), (reversed_, lambda a: a, True)]:
        assert row['status'] == expected['status']
        for a, b in zip(expected['shells'], row['shells']):
            assert a['status'] == b['status']
            if 'frames' in a:
                for key in ['count_qualified_triples', 'signature_condition', 'stable_gram']:
                    assert a['frames'][key] == b['frames'][key]
        if expected['selected'] is not None:
            a, b = expected['selected'], row['selected']
            assert a['support'] == [unmap(x) for x in b['support']]
            assert a['landmarks'] == [unmap(x) for x in b['landmarks']]
            assert a['lower_count'] == b['lower_count']
            assert a['certificate']['guard']['checks'] == b['certificate']['guard']['checks']
            for key in ['gram', 'vectors', 'condition']:
                np.testing.assert_allclose(a['certificate'][key], b['certificate'][key], **c['replay_tolerance'])
    return dict(status='PASS', relabelling=True, time_reversal=True,
                selected_witness=expected['selected'] is not None)
