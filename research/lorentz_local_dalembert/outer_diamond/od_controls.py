"""Independent geometry/count oracles and inference transport controls."""
import copy
import hashlib
import itertools
import numpy as np
from od_common import core, config, digest
from od_simulation import uniform_diamond, shell, extent, relation, VOLUME
from od_order import PhysicalPoset, chain_witness
from im_controls import check as inherited_check
import intrinsic


def check():
    inherited = inherited_check()
    c, _, _ = config()
    rng = np.random.default_rng(583921)
    sample = rng.integers(0, 256, size=(127, 139), dtype=np.uint8)
    for array in (sample, sample.T, sample[::2, ::3], sample.astype(float)):
        assert digest(array) == hashlib.sha256(array.tobytes()).hexdigest()
    z = np.vstack(([[-.5, 0, 0], [.5, 0, 0]], uniform_diamond(58, 2, rng)))
    r = relation(z, 7)
    scalar = np.array([[b[0] > a[0] and (b[0]-a[0])**2 > (b[1]-a[1])**2+(b[2]-a[2])**2
                        for b in z] for a in z], dtype=np.uint8)
    np.testing.assert_array_equal(r, scalar)
    g = PhysicalPoset(r, rng.random(len(z)), [0, 1])
    checked = excluded = 0
    for a, b in itertools.product(range(len(z)), repeat=2):
        if r[a, b]:
            wanted = sum(bool(scalar[a, k] and scalar[k, b]) for k in range(2, len(z)))
            assert g.interval(a, b) == wanted
            excluded += sum(bool(scalar[a, k] and scalar[k, b]) for k in (0, 1))
            checked += 1
    assert excluded > 0
    orders = 0
    for n in range(3, 23):
        for repetition in range(3):
            r = np.triu(rng.random((n, n)) < .35, 1)
            for k in range(n):
                r |= r[:, k, None] & r[None, k, :]
            h = core.Poset(r, rng.random(n))
            for threshold in (0, 1, 2, 8):
                expected = any(r[a, b] and r[b, d] and min(h.interval(a, b), h.interval(b, d), h.interval(a, d)) >= threshold
                               for a, b, d in itertools.combinations(range(n), 3))
                witness = chain_witness(h, list(rng.permutation(n)), threshold)
                assert (witness is not None) == expected
            orders += 1
    z = uniform_diamond(60000, 1, rng)
    assert np.all(extent(z) < 1)
    np.testing.assert_allclose((z*z).mean(axis=0), [1/40, 3/80, 3/80], atol=.001, rtol=0)
    counts = []
    for seed in range(500):
        z, marks, colours, meta = shell(100, seed, 1, 1, 1.25, c)
        counts.append(len(z))
        assert len(z) == len(marks) == len(colours)
    mean = 100 * VOLUME * (1.25**3 - 1)
    assert abs(np.mean(counts)-mean) < 5*np.sqrt(mean/500)
    assert abs(np.var(counts, ddof=1)/mean-1) < .25
    return dict(status='PASS', inherited=inherited, scalar_relation_pairs=len(g.r)**2,
                direct_intervals=checked, artificial_interiors_excluded=excluded,
                brute_force_orders=orders, uniform_moments=True, shell_count_replicates=len(counts),
                streaming_hash_oracles=4)


def transport(g, s, rho, probes, colours, c, expected, seed):
    if s['status'] != 'ok':
        return dict(status='PASS', applicable=False)
    permutation = np.random.default_rng(seed ^ 0x15B29).permutation(g.size)
    inverse = np.argsort(permutation)
    renamed = copy.deepcopy(s)
    renamed['root'] = int(inverse[s['root']])
    for key in ['support', 'temporal']:
        renamed[key] = [int(inverse[x]) for x in s[key]]
    mapped_probes = [int(inverse[x]) for x in probes]
    gp = PhysicalPoset(g.r[np.ix_(permutation, permutation)], g.marks[permutation], mapped_probes)
    actual = intrinsic.infer(gp, renamed, rho, mapped_probes, colours[permutation], c)
    del gp
    gr = PhysicalPoset(g.r.T, g.marks, probes)
    reverse = intrinsic.infer(gr, s, rho, probes, colours, c)
    del gr
    for row, unmap, reversed_time in [(actual, lambda a: int(permutation[a]), False), (reverse, lambda a: a, True)]:
        a, b = expected['frame'], row['frame']
        assert a['status'] == b['status']
        assert a.get('eligible_triples') == b.get('eligible_triples')
        if a['status'] == 'ok':
            assert a['landmarks'] == [unmap(x) for x in b['landmarks']]
            assert (a['side'] != b['side']) == reversed_time
            for key in ['gram', 'vectors', 'feature_gram', 'lorentz_feature_gram', 'eigenvalues', 'condition']:
                np.testing.assert_allclose(a[key], b[key], **c['calibration_replay_tolerance'])
            assert a['guard']['checks'] == b['guard']['checks']
        for name in ['intrinsic_raw', 'intrinsic_guarded']:
            assert expected[name]['adopted'] == row[name]['adopted']
            assert expected[name]['fallback_reasons'] == row[name]['fallback_reasons']
            np.testing.assert_allclose(expected[name]['weights'], row[name]['weights'], **c['calibration_replay_tolerance'])
    return dict(status='PASS', applicable=True, relabel=True, time_reversal=True)
