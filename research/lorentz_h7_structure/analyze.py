"""Exact post-hoc structural analysis. Standard library, no network or floats."""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def polynomial(a):
    n = len(a)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coeff = [1]
    for k in range(1, n+1):
        b = multiply(a, b)
        trace = sum(b[i][i] for i in range(n))
        require(trace % k == 0, 'nonintegral recurrence')
        coeff.append(-trace//k)
        for i in range(n):
            b[i][i] += coeff[-1]
    require(not any(map(any, b)), 'Cayley-Hamilton residual')
    return coeff


def operators(c):
    n = len(c)
    s = [[c[i][j]+c[j][i] for j in range(n)] for i in range(n)]
    a = [[c[i][j]-c[j][i] for j in range(n)] for i in range(n)]
    sa, ass = multiply(s, a), multiply(a, s)
    return [s, a, [[sa[i][j]-ass[i][j] for j in range(n)] for i in range(n)]]


def features(c):
    n = len(c)
    require(all(c[i][i] == 0 for i in range(n)), 'reflexive relation')
    require(all(not(c[i][j] and c[j][k]) or c[i][k]
                for i in range(n) for j in range(n) for k in range(n)), 'nontransitive relation')
    past = [sum(col) for col in zip(*c)]
    future = list(map(sum, c))
    predecessors = [sum(c[j][i] << j for j in range(n)) for i in range(n)]
    @lru_cache(None)
    def extensions(mask):
        if mask == (1 << n)-1:
            return 1
        return sum(extensions(mask | (1 << i)) for i in range(n)
                   if not(mask >> i & 1) and not(predecessors[i] & ~mask))
    @lru_cache(None)
    def height_at(i):
        return 1+max((height_at(j) for j in range(n) if c[i][j]), default=0)
    unseen = set(range(n)); components = []
    while unseen:
        active = {min(unseen)}; component = set()
        while active:
            v = active.pop(); component.add(v); unseen.discard(v)
            active.update(j for j in unseen if c[v][j] or c[j][v])
        components.append(len(component))
    return {'n': n, 'polynomials_S_A_K': [polynomial(a) for a in operators(c)],
            'minimal_maximal': [past.count(0), future.count(0)],
            'W_future': sum(d*(d-1)//2 for d in future),
            'W_past': sum(d*(d-1)//2 for d in past),
            'degree_pairs': sorted([a, b] for a, b in zip(past, future)),
            'isolated': sum(a == b == 0 for a, b in zip(past, future)),
            'shared_successors_of_unit_minima': sum(sum(c[i][v]*c[j][v] for v in range(n))
                for i in range(n) for j in range(i+1, n)
                if past[i] == past[j] == 0 and future[i] == future[j] == 1),
            'component_sizes': sorted(components), 'relations': sum(future),
            'height': max(map(height_at, range(n))), 'linear_extensions': extensions(0)}


def lift(c, k):
    n = len(c)
    return [[int(i < j) if i < k else (0 if j < k else c[i-k][j-k])
             for j in range(n+k)] for i in range(n+k)]


def run():
    data = json.loads((HERE/'inputs.json').read_text())
    matrices = {name: [[int(x) for x in row] for row in rows]
                for name, rows in data['relations'].items()}
    certificates = []
    for cert in data['certificates']:
        c = matrices[cert['left']]; n = len(c); x = cert['switch_set']
        r = [[1-2*int(i == j) if i in x and j in x else 2*int(i == j)
              for j in range(n)] for i in range(n)]
        raw = multiply(multiply(transpose(r), c), r)
        require(all(v in (0, 4) for row in raw for v in row), 'switch is not binary')
        switched = [[v//4 for v in row] for row in raw]
        target = matrices[cert['right']]; p = cert['target_labels']
        require(switched == [[target[p[i]][p[j]] for j in range(n)] for i in range(n)], 'certificate mismatch')
        certificates.append({**cert, 'R_equals_2Q': r,
                             'switched_relation_rows': [''.join(map(str, row)) for row in switched]})
    pairs = [{'ids': [c['left'], c['right']], 'kind': 'minimal_seed'} for c in data['certificates']]
    pairs.append({'ids': ['n8-degree-a', 'n8-degree-b'], 'kind': 'known_degree_control'})
    for k in data['connected_prefix_lengths']:
        names = []
        for seed in ['n7-0475', 'n7-0734']:
            name = seed+'-prefix-'+str(k); matrices[name] = lift(matrices[seed], k); names.append(name)
        pairs.append({'ids': names, 'kind': 'connected_prefix', 'k': k})
    records = {name: {'relation_rows': [''.join(map(str, row)) for row in c], 'features': features(c)}
               for name, c in matrices.items()}
    primary = ['n', 'polynomials_S_A_K', 'minimal_maximal', 'W_future', 'W_past']
    for pair in pairs:
        a, b = [records[name]['features'] for name in pair['ids']]
        require(all(a[key] == b[key] for key in primary), 'H7 differs')
        pair.update(H7_equal=True, same_D=a['degree_pairs'] == b['degree_pairs'],
                    isolated_counts=[a['isolated'], b['isolated']],
                    linear_extensions=[a['linear_extensions'], b['linear_extensions']])
    controls = [matrices[name] for name in ['n8-degree-a', 'n8-degree-b']]
    gram = [polynomial(multiply([row[4:] for row in c[:4]], transpose([row[4:] for row in c[:4]]))) for c in controls]
    return {'schema': 'x6.h7-structure-results/1', 'status': 'EXACT_RESULTS_REQUIRE_COUNTERCHECK',
            'discovery_status': 'POST_HOC_EXPLANATION_NOT_PREREGISTERED',
            'input_sha256': hashlib.sha256((HERE/'inputs.json').read_bytes()).hexdigest(),
            'certificates': certificates, 'records': records, 'pairs': pairs,
            'height_two_control_BBt_polynomials': gram}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); result = run()
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'records': len(result['records']), 'pairs': len(result['pairs'])}))
