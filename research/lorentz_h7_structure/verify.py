"""Certificate checker; imports no analysis or historical implementation.

Uses integer identities, pivoted determinant interpolation and permutation counts.
This is algorithmic cross-checking by the same authoring process, not external review.
"""
import argparse
import copy
from fractions import Fraction
import hashlib
from itertools import combinations, permutations
import json
from math import comb
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mat(rows):
    n = len(rows)
    require(all(len(row) == n and set(row) <= {'0', '1'} for row in rows), 'bad relation encoding')
    c = [[int(x) for x in row] for row in rows]
    require(all(not c[i][i] for i in range(n)), 'reflexivity')
    require(all(not(c[i][j] and c[j][k]) or c[i][k]
                for i in range(n) for j in range(n) for k in range(n)), 'transitivity')
    return c


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def det(matrix):
    a = copy.deepcopy(matrix); n = len(a); sign = previous = 1
    for k in range(n-1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k+1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]; sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*pivot-a[i][k]*a[k][j]
                require(numerator % previous == 0, 'inexact determinant step')
                a[i][j] = numerator//previous
        for i in range(k+1, n):
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def poly(a):
    n = len(a)
    values = [det([[x*int(i == j)-a[i][j] for j in range(n)] for i in range(n)]) for x in range(n+1)]
    result = [Fraction(0)]*(n+1); basis = [Fraction(1)]
    for k in range(n+1):
        for j, b in enumerate(basis):
            result[j] += values[0]*b
        values = [v-u for u, v in zip(values, values[1:])]
        next_basis = [Fraction(0)]*(len(basis)+1)
        for j, b in enumerate(basis):
            next_basis[j] -= k*b/(k+1); next_basis[j+1] += b/(k+1)
        basis = next_basis
    require(all(v.denominator == 1 for v in result), 'nonintegral polynomial')
    return list(map(int, reversed(result)))


def linear_count(c):
    # Strip uniquely determined least elements, then enumerate all residual permutations.
    a = copy.deepcopy(c)
    while len(a) > 1:
        minima = [j for j in range(len(a)) if not any(row[j] for row in a)]
        if len(minima) != 1:
            break
        i = minima[0]
        require(all(a[i][j] for j in range(len(a)) if i != j), 'unique minimum not least')
        a = [[v for j, v in enumerate(row) if j != i] for k, row in enumerate(a) if k != i]
    require(len(a) <= 8, 'permutation scope exceeded')
    relations = [(i, j) for i in range(len(a)) for j in range(len(a)) if a[i][j]]
    return sum(all(p[i] < p[j] for i, j in relations) for p in permutations(range(len(a))))


def isomorphic(a, b):
    n = len(a)
    da = [(sum(a[j][i] for j in range(n)), sum(a[i])) for i in range(n)]
    db = [(sum(b[j][i] for j in range(n)), sum(b[i])) for i in range(n)]
    return any(all(da[i] == db[p[i]] for i in range(n)) and
               all(a[i][j] == b[p[i]][p[j]] for i in range(n) for j in range(n))
               for p in permutations(range(n)))


def check_features(c, f):
    n = len(c)
    s = [[c[i][j]+c[j][i] for j in range(n)] for i in range(n)]
    a = [[c[i][j]-c[j][i] for j in range(n)] for i in range(n)]
    k = [[2*sum(c[v][i]*c[v][j]-c[i][v]*c[j][v] for v in range(n))
          for j in range(n)] for i in range(n)]
    require(f['polynomials_S_A_K'] == [poly(m) for m in [s, a, k]], 'polynomial mismatch')
    degrees = [[sum(c[j][i] for j in range(n)), sum(c[i])] for i in range(n)]
    wf = sum(c[v][i]*c[v][j] for v in range(n) for i, j in combinations(range(n), 2))
    wp = sum(c[i][v]*c[j][v] for v in range(n) for i, j in combinations(range(n), 2))
    height = 1; power = c
    while any(map(any, power)):
        height += 1; require(height <= n, 'cyclic input'); power = mm(power, c)
    reach = [[bool(i == j or s[i][j]) for j in range(n)] for i in range(n)]
    for v in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][v] and reach[v][j])
    components = sorted({tuple(j for j in range(n) if row[j]) for row in reach})
    expected = {'n': n, 'minimal_maximal': [sum(d[0] == 0 for d in degrees), sum(d[1] == 0 for d in degrees)],
                'W_future': wf, 'W_past': wp, 'degree_pairs': sorted(degrees),
                'isolated': degrees.count([0, 0]), 'component_sizes': sorted(map(len, components)),
                'shared_successors_of_unit_minima': sum(c[i][v]*c[j][v]
                    for i, j in combinations(range(n), 2) for v in range(n)
                    if degrees[i] == degrees[j] == [0, 1]),
                'relations': sum(map(sum, c)), 'height': height, 'linear_extensions': linear_count(c)}
    require({k: v for k, v in f.items() if k != 'polynomials_S_A_K'} == expected, 'structural feature mismatch')


def certificate(cert, matrices):
    c, d = matrices[cert['left']], matrices[cert['right']]; n = len(c)
    r = cert['R_equals_2Q']; p = cert['target_labels']
    require(len(r) == n and all(len(row) == n for row in r), 'R shape')
    require(all(type(v) is int for row in r for v in row), 'R integer')
    require(sorted(p) == list(range(n)), 'not a relabelling')
    require(all(sum(r[v][i]*r[v][j] for v in range(n)) == 4*int(i == j)
                for i in range(n) for j in range(n)), 'orthogonality')
    require(all(sum(row) == 2 for row in r), 'ones vector')
    require(all(sum(r[u][i]*c[u][v]*r[v][j] for u in range(n) for v in range(n)) == 4*d[p[i]][p[j]]
                for i in range(n) for j in range(n)), 'similarity')
    switched = mat(cert['switched_relation_rows'])
    require(switched == [[d[p[i]][p[j]] for j in range(n)] for i in range(n)], 'switched data')


def verify(result):
    data = json.loads((HERE/'inputs.json').read_text())
    require(result['input_sha256'] == hashlib.sha256((HERE/'inputs.json').read_bytes()).hexdigest(), 'input hash')
    originals = {}
    for path, expected in data['sources'].items():
        raw = subprocess.check_output(['git', 'show', data['base_commit']+':'+path], cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest() == expected, 'source hash')
        source = json.loads(raw)
        if path.endswith('counterexamples.json'):
            for pair in source:
                for side in ['left', 'right']:
                    record = pair[side]; originals[record['id']] = record['relation_rows']
        else:
            for r in source['records']:
                if r['id'].startswith('n8-degree-'):
                    originals[r['id']] = [''.join(map(str, row)) for row in r['causal_matrix']]
    require(originals == data['relations'], 'published input mismatch')
    matrices = {name: mat(r['relation_rows']) for name, r in result['records'].items()}
    expected_ids = set(originals)
    for k in data['connected_prefix_lengths']:
        expected_ids.update(name+'-prefix-'+str(k) for name in ['n7-0475', 'n7-0734'])
    require(set(matrices) == expected_ids, 'record coverage')
    for name, rows in originals.items():
        require(result['records'][name]['relation_rows'] == rows, 'original altered')
    require(len(result['certificates']) == 2, 'certificate count')
    for cert, fixed in zip(result['certificates'], data['certificates']):
        require(all(cert[k] == v for k, v in fixed.items()), 'certificate binding')
        x = cert['switch_set']; n = len(matrices[cert['left']])
        require(cert['R_equals_2Q'] == [[1-2*int(i == j) if i in x and j in x else 2*int(i == j)
                                       for j in range(n)] for i in range(n)], 'switch block')
        certificate(cert, matrices)
    for name, c in matrices.items():
        check_features(c, result['records'][name]['features'])
    expected_pairs = [[c['left'], c['right']] for c in data['certificates']]+[['n8-degree-a', 'n8-degree-b']]
    expected_pairs += [[name+'-prefix-'+str(k) for name in ['n7-0475', 'n7-0734']] for k in data['connected_prefix_lengths']]
    require([p['ids'] for p in result['pairs']] == expected_pairs, 'pair coverage')
    for pair in result['pairs']:
        a, b = [result['records'][name]['features'] for name in pair['ids']]
        require(all(a[key] == b[key] for key in ['n', 'polynomials_S_A_K', 'minimal_maximal', 'W_future', 'W_past']), 'H7 mismatch')
        require(pair['H7_equal'] is True and pair['same_D'] == (a['degree_pairs'] == b['degree_pairs']), 'pair metadata')
        require(pair['isolated_counts'] == [a['isolated'], b['isolated']], 'isolated metadata')
        require(pair['linear_extensions'] == [a['linear_extensions'], b['linear_extensions']], 'extension metadata')
        if pair['kind'] == 'connected_prefix':
            # A different exact number of linear extensions proves nonisomorphism.
            require(a['linear_extensions'] != b['linear_extensions'], 'nonisomorphism witness missing')
        else:
            require(not isomorphic(*(matrices[name] for name in pair['ids'])), 'pair is isomorphic')
        if pair['kind'] == 'connected_prefix':
            k = pair['k']; require(k in data['connected_prefix_lengths'], 'prefix scope')
            for seed, name in zip(['n7-0475', 'n7-0734'], pair['ids']):
                c = matrices[name]; n = len(c)
                require(all(c[i][j] == (int(i < j) if i < k else (0 if j < k else matrices[seed][i-k][j-k]))
                            for i in range(n) for j in range(n)), 'ordinal prefix')
                f = result['records'][name]['features']
                require(f['component_sizes'] == [n] and f['minimal_maximal'] == [1, 3], 'connected endpoints')
                require(f['height'] == k+3 and f['relations'] == 8+7*k+comb(k, 2), 'prefix counts')
                require(f['W_future'] == 7+sum(comb(7+j, 2) for j in range(k)), 'future lift formula')
                require(f['W_past'] == 6+8*k+7*comb(k, 2)+(comb(k, 3) if k >= 3 else 0), 'past lift formula')
    grams = []
    for name in ['n8-degree-a', 'n8-degree-b']:
        c = matrices[name]
        require(all(not c[i][j] for i in range(8) for j in range(8) if not(i < 4 <= j)), 'height two blocks')
        grams.append(poly([[sum(c[i][v]*c[j][v] for v in range(4, 8)) for j in range(4)] for i in range(4)]))
    require(grams == result['height_two_control_BBt_polynomials'] and grams[0] == grams[1], 'Gram polynomials')
    require(result['pairs'][2]['same_D'] and result['pairs'][2]['isolated_counts'] == [0, 0], 'degree control')
    return matrices


def main(path):
    result = json.loads(path.read_text()); matrices = verify(result)
    controls = []
    def reject(name, fn):
        try:
            fn()
        except ValueError:
            controls.append(name)
        else:
            raise ValueError('invalid data accepted: '+name)
    cert = result['certificates'][0]
    bad = copy.deepcopy(cert); bad['R_equals_2Q'][0][0] += 1
    reject('altered_orthogonal_matrix', lambda: certificate(bad, matrices))
    bad = copy.deepcopy(cert); bad['target_labels'][0], bad['target_labels'][1] = bad['target_labels'][1], bad['target_labels'][0]
    reject('wrong_relabelling', lambda: certificate(bad, matrices))
    wrong = copy.deepcopy(matrices); wrong[cert['right']][0][6] = 0
    reject('changed_target_relation', lambda: certificate(cert, wrong))
    f = copy.deepcopy(result['records'][cert['left']]['features']); f['polynomials_S_A_K'][0][-1] += 1
    reject('altered_polynomial', lambda: check_features(matrices[cert['left']], f))
    reject('missing_transitive_edge', lambda: mat(['010', '001', '000']))
    print(json.dumps({'status': 'PASS_EXACT_STRUCTURE_COUNTERCHECK', 'records': len(matrices),
                      'exact_polynomials_checked': 3*len(matrices)+2, 'similarity_certificates': 2,
                      'collision_pairs': len(result['pairs']), 'negative_controls_rejected': controls,
                      'scope': 'Algorithmic cross-check; general statements require the accompanying proofs; no external human review'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('results', type=Path, nargs='?', default=HERE/'results.json')
    main(parser.parse_args().results)
