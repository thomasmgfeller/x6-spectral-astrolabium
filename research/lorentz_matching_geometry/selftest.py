"""Exhaustive tiny oracles and corruption controls, before target execution."""
from collections import Counter
from itertools import permutations
import copy
import numpy as np
from core import (Stream, decode, encode, from_joint, joint_matrix, match,
                  match_indexed, require, three_order, verify_incidence, verify_relation)
import geometry


def brute(a, b):
    for p in permutations(range(len(a))):
        for q in permutations(range(len(a[0]))):
            if all(a[i][j] == b[p[i]][q[j]] for i in range(len(a)) for j in range(len(a[0]))):
                return dict(rows=list(p), columns=list(q))
    return None


def counterexample():
    b = [[1, 1], [0, 1]]
    c = [[1, 0], [1, 1]]
    d = list(reversed(c))
    a_order, b_order = three_order(b, c), three_order(b, d)
    # Both adjacent matrices separately match; one middle permutation cannot do both.
    require(match(b, b)['status'] == match(c, d)['status'] == 'ISOMORPHIC', 'marginal matches')
    require(sum(map(sum, a_order)) != sum(map(sum, b_order)), 'nonisomorphism relation count certificate')
    require(Counter(zip(*joint_matrix(b, c))) != Counter(zip(*joint_matrix(b, d))), 'joint profiles distinguish')
    return dict(B=b, C=c, C_swapped=d, relation_a=a_order, relation_b=b_order,
                total_relations=[sum(map(sum, a_order)), sum(map(sum, b_order))])


def run():
    matrices = [[[(bits >> (2*i+j)) & 1 for j in range(2)] for i in range(2)] for bits in range(16)]
    comparisons = 0
    for a in matrices:
        for b in matrices:
            result = match_indexed(encode(a), encode(b))
            require((result['status'] == 'ISOMORPHIC') == (brute(a, b) is not None), 'exhaustive 2x2 oracle')
            comparisons += 1
    for bits in range(512):
        a = [[(bits >> (3*i+j)) & 1 for j in range(3)] for i in range(3)]
        rebuilt = decode(encode(a))
        require(Counter(zip(*rebuilt)) == Counter(zip(*a)), 'all 3x3 reconstruction')
        p, q = Stream('toy', bits).shuffle(range(3)), Stream('toy-cols', bits).shuffle(range(3))
        b = [[a[i][j] for j in q] for i in p]
        result = match(a, b)
        require(result['status'] == 'ISOMORPHIC', '3x3 renamed copy')
        verify_incidence(a, b, result['witness'])
    for b in matrices:
        for c in matrices:
            joint = joint_matrix(b, c)
            rebuilt = decode(encode(joint))
            order = from_joint(rebuilt, 2)
            original = three_order(b, c)
            # Brute force the shared middle permutation; exterior nodes stay fixed.
            found = False
            for p in permutations(range(2)):
                perm = [0, 1, 2+p[0], 2+p[1], 4, 5]
                if all(order[i][j] == original[perm[i]][perm[j]] for i in range(6) for j in range(6)):
                    verify_relation(order, original, perm)
                    found = True
            require(found, 'joint three-layer full reconstruction')
    counterexample()
    rejected = []
    def reject(name, action):
        try:
            action()
        except (ValueError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('failed negative control: '+name)
    good = encode([[1, 0], [0, 1]])
    bad = copy.deepcopy(good)
    bad['counts'].pop()
    reject('missing subset', lambda: decode(bad))
    altered = copy.deepcopy(good)
    altered['counts'][0][1] += 1
    reject('changed empty count', lambda: decode(altered))
    reject('false bijection', lambda: verify_incidence([[1, 0], [0, 1]], [[1, 0], [0, 1]],
                                                     dict(rows=[0, 1], columns=[1, 0])))
    reject('duplicate bijection', lambda: verify_relation([[0, 1], [0, 0]], [[0, 1], [0, 0]], [0, 0]))
    require(match([[1, 0], [0, 1]], [[1, 0], [0, 1]], budget=0)['status'] == 'INCONCLUSIVE', 'budget not negative')
    # Known exact chain and antichain, plus a non-topologically labelled chain.
    for c in [[[0, 1, 1], [0, 0, 1], [0, 0, 0]], [[0]*3 for _ in range(3)]]:
        f = geometry.features(c)
        p = [2, 0, 1]
        g = geometry.features([[c[i][j] for j in p] for i in p])
        require(f['intersections'] == g['intersections'], 'toy intersection invariance')
        require(np.allclose(f['B'], g['B'], rtol=1e-12, atol=1e-12), 'toy spectral invariance')
    chain = geometry.features([[0, 1, 1], [0, 0, 1], [0, 0, 0]])
    require(chain['interval_histogram'] == [2, 1, 0] and chain['height'] == 3, 'known chain intervals')
    require(np.allclose(chain['eigenvalues'], [0, 1, 3]), 'known chain spectrum')
    # Generator tests use N=4 only, outside every target size and split.
    for family in ['minkowski', 'layered', 'lattice', 'jittered_lattice']:
        record = geometry.sample(family, 4, 'toy', 0)
        geometry.features([[int(x) for x in row] for row in record['relation_rows']])
    return dict(status='PASS_TOY_ONLY', pair_oracles=comparisons, binary_3x3=512,
                three_layer_2x2_pairs=256, rejected_corruptions=rejected,
                budget_control='INCONCLUSIVE', target_generation=False)


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2))
