"""Exact producer: maximal extensions, canonical forms, trace recurrence.

Python standard library only. The counterchecker does not import this module.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import permutations, product, combinations
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(rows):
    return [[(row >> j) & 1 for j in range(len(rows))] for row in rows]


def degrees(rows):
    n = len(rows)
    return [(sum((rows[j] >> i) & 1 for j in range(n)), rows[i].bit_count()) for i in range(n)]


def code(rows):
    n = len(rows)
    return sum(row << (n*i) for i, row in enumerate(rows))


def relabel(rows, permutation):
    return tuple(sum(((rows[i] >> j) & 1) << k for k, j in enumerate(permutation)) for i in permutation)


def canonical(rows):
    classes = defaultdict(list)
    for i, pair in enumerate(degrees(rows)):
        classes[pair].append(i)
    blocks = [list(permutations(classes[key])) for key in sorted(classes)]
    best, best_rows, hits = None, None, 0
    for choice in product(*blocks):
        perm = tuple(i for part in choice for i in part)
        transformed = relabel(rows, perm)
        word = code(transformed)
        if best is None or word < best:
            best, best_rows, hits = word, transformed, 1
        elif word == best:
            hits += 1
    return best, best_rows, hits


def enumerate_levels(maximum=7):
    require(type(maximum) is int and 1 <= maximum <= 7, 'maximum must be 1..7')
    levels, previous, counts = {}, {0: ()}, {}
    for n in range(1, maximum+1):
        current, extensions = {}, 0
        for rows in previous.values():
            past = [sum(((rows[j] >> i) & 1) << j for j in range(n-1)) for i in range(n-1)]
            for ideal in range(1 << (n-1)):
                if any((ideal >> i) & 1 and past[i] & ~ideal for i in range(n-1)):
                    continue
                candidate = tuple(rows[i] | (((ideal >> i) & 1) << (n-1)) for i in range(n-1)) + (0,)
                word, representative, _ = canonical(candidate)
                current[word] = representative
                extensions += 1
        levels[n] = [current[word] for word in sorted(current)]
        counts[n] = extensions
        previous = current
        print(json.dumps({'phase':'maximal_extensions','n':n,'classes':len(current),'ideal_extensions':extensions}), flush=True)
    return levels, counts


def linear_extensions(rows):
    n = len(rows)
    past = [sum(((rows[j] >> i) & 1) << j for j in range(n)) for i in range(n)]
    @lru_cache(None)
    def visit(done):
        if done == (1 << n)-1:
            return 1
        return sum(visit(done | (1 << i)) for i in range(n)
                   if not (done >> i) & 1 and not past[i] & ~done)
    return visit(0)


def multiply(a, b):
    columns = list(zip(*b))
    return [[sum(x*y for x, y in zip(row, col)) for col in columns] for row in a]


def polynomial(a):
    n = len(a)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    result = [1]
    for k in range(1, n+1):
        b = multiply(a, b)
        trace = sum(b[i][i] for i in range(n))
        require(trace % k == 0, 'nonintegral trace recurrence')
        coefficient = -(trace // k)
        result.append(coefficient)
        for i in range(n):
            b[i][i] += coefficient
    require(not any(x for row in b for x in row), 'Cayley-Hamilton residual')
    return result


def feature(rows):
    n, c = len(rows), matrix(rows)
    s = [[c[i][j]+c[j][i] for j in range(n)] for i in range(n)]
    a = [[c[i][j]-c[j][i] for j in range(n)] for i in range(n)]
    sa, ass = multiply(s, a), multiply(a, s)
    k = [[sa[i][j]-ass[i][j] for j in range(n)] for i in range(n)]
    ds = degrees(rows)
    depth = [1]*n
    for j in sorted(range(n), key=lambda v: ds[v][0]):
        depth[j] = 1+max((depth[i] for i in range(n) if c[i][j]), default=0)
    return {'n':n, 'polynomials_S_A_K':[polynomial(m) for m in (s,a,k)],
            'minimal_maximal':[sum(x == 0 for x,y in ds),sum(y == 0 for x,y in ds)],
            'degree_pairs':[list(pair) for pair in sorted(ds)],
            'W_future':sum(y*(y-1)//2 for x,y in ds), 'W_past':sum(x*(x-1)//2 for x,y in ds),
            'relations':sum(row.bit_count() for row in rows),'height':max(depth)}


def signature(f, mode):
    result = [f['n'], f['polynomials_S_A_K'], f['minimal_maximal']]
    if mode == 'F0_W_future':
        result.append(f['W_future'])
    elif mode == 'F0_W_both':
        result.extend([f['W_future'], f['W_past']])
    elif mode == 'F0_D':
        result.append(f['degree_pairs'])
    elif mode != 'F0':
        raise ValueError('unknown signature')
    return json.dumps(result, separators=(',',':'))


def grouping(records):
    results = {}
    for mode in ['F0','F0_W_future','F0_W_both','F0_D']:
        groups = defaultdict(list)
        for row in records:
            groups[signature(row['features'],mode)].append(row['id'])
        collisions = sorted(sorted(g) for g in groups.values() if len(g)>1)
        results[mode] = {'classes':len(groups),'collision_groups':collisions,
                         'collision_pairs':sum(len(g)*(len(g)-1)//2 for g in collisions)}
    return results


def produce(maximum=7):
    levels, counts = enumerate_levels(maximum)
    records, summaries = [], {}
    for n, orders in levels.items():
        group = []
        for index, rows in enumerate(orders):
            word, _, automorphisms = canonical(rows)
            extensions = linear_extensions(rows)
            require(extensions % automorphisms == 0,'natural multiplicity division')
            group.append({'id':f'n{n}-{index:04d}','n':n,'canonical_code':word,
                          'relation_rows':[''.join(str((row >> j)&1) for j in range(n)) for row in rows],
                          'automorphisms':automorphisms,'linear_extensions':extensions,
                          'natural_label_multiplicity':extensions//automorphisms,'features':feature(rows)})
        summaries[str(n)] = {'orders':len(group),'ideal_extensions':counts[n],
                             'naturally_labelled_orders':sum(r['natural_label_multiplicity'] for r in group),
                             'height_counts':{str(h):sum(r['features']['height']==h for r in group) for h in range(1,n+1)},
                             'groups':grouping(group)}
        records.extend(group)
        print(json.dumps({'phase':'exact_features','n':n,'records':len(group)}),flush=True)
    witnesses=[]
    lookup={r['id']:r for r in records}
    for n, summary in summaries.items():
        for group in summary['groups']['F0_W_both']['collision_groups']:
            for left, right in combinations(group,2):
                l,r=lookup[left],lookup[right]
                rows=tuple(sum((ch=='1') << j for j,ch in enumerate(row)) for row in l['relation_rows'])
                transposed=tuple(sum(((rows[j] >> i)&1) << j for j in range(int(n))) for i in range(int(n)))
                witnesses.append({'ids':[left,right],'n':int(n),'left':l,'right':r,
                                  'same_D':l['features']['degree_pairs']==r['features']['degree_pairs'],
                                  'dual_isomorphic':canonical(transposed)[0]==r['canonical_code'],
                                  'isomorphic':False})
    return {'schema':'x6.lorentz-n7-atlas/1','maximum_n':maximum,
            'records':records,'by_n':summaries,
            'n7_height_le_2':grouping([r for r in records if r['n']==7 and r['features']['height']<=2]) if maximum==7 else None,
            'hypothesis_status':'REFUTED_BY_COUNTEREXAMPLE' if witnesses else 'SUPPORTED_FINITE_N_LE_'+str(maximum),
            'primary_counterexamples':witnesses}
