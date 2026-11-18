"""Exact marginal test for three exchangeable insertion marks on the N14 support."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'upstream' / 'v03'))
from orders import bit_edges, extend


def encode(edges):
    """Directed pair (i,j) occupies bit 6*i+j. Root labels 0,1,2 stay fixed."""
    return sum(1 << (6*i+j) for i, j in edges)


def rename(edges, perm):
    return encode((perm[i], perm[j]) for i, j in edges)


def read_json(path):
    return json.loads(path.read_text())


def dump(data, path):
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + '\n')


def admissible_orders(masks):
    all_perms = list(permutations(range(6)))
    return {rename(edges, p): mask for mask in masks for edges in [bit_edges(6, mask)] for p in all_perms}


MARK_PERMS = [(0, 1, 2, *t) for t in permutations((3, 4, 5))]
PAIR_MASK = encode((i, j) for i in range(5) for j in range(5) if i != j)


def build(row, admissible):
    pair_group, target = {}, Counter()
    archived = {}
    forward = {}
    for entry in row['marked_ledger']:
        edges = frozenset(map(tuple, entry['edges']))
        key = encode(edges)
        swap = rename(edges, (0,1,2,4,3))
        pair_group[key] = min(key, swap)
        law = entry['conditional_weights']
        mass = Q(law['symmetric_completion'])
        archived[key] = (swap, mass)
        if mass:
            target[pair_group[key]] += mass
        if Q(law['sequential']) > 0:
            for child in extend(edges, 5):
                code = encode(child)
                if code in admissible:
                    assert code not in forward
                    forward[code] = child
    assert sum(target.values()) == 1
    assert all(archived[swap] == (key,mass) for key,(swap,mass) in archived.items())
    seen = set()
    columns = {}
    sizes = {}
    order_counts = Counter()
    for code, edges in sorted(forward.items()):
        if code in seen:
            continue
        renamed = [rename(edges, p) for p in MARK_PERMS]
        orbit = set(renamed)
        seen.update(orbit)
        number_good = sum(c in forward for c in renamed)
        order_counts[number_good] += len(orbit.intersection(forward))
        if number_good == 6:
            counts = Counter(pair_group[c & PAIR_MASK] for c in orbit)
            assert counts.keys() <= target.keys()
            columns[min(orbit)] = {p:Q(n, len(orbit)) for p,n in counts.items()}
            sizes[min(orbit)] = len(orbit)
    assert sum(order_counts.values()) == len(forward)
    assert sum(sizes.values()) == order_counts[6]
    return dict(target), columns, sizes, {
        'forward_paths':len(forward),
        'forward_paths_by_number_of_valid_orders':dict(sorted(order_counts.items())),
        'paths_valid_in_all_six_orders':order_counts[6],
        'fully_admissible_orbits':len(columns),
        'fully_admissible_end_types':sorted({admissible[orbit] for orbit in columns}),
        'ordered_positive_pair_paths':row['reverse_also_admissible_paths'],
        'unordered_positive_pair_classes':len(target),
    }


def marginal(columns, masses):
    out = Counter()
    for orbit, mass in masses.items():
        for pair, coefficient in columns[orbit].items():
            out[pair] += mass * coefficient
    return out


def residual_target(target, columns, sizes):
    # A uniform probability on the labelled full-support paths gives orbit
    # masses proportional to orbit sizes, including paths with stabilizers.
    total = sum(sizes.values())
    uniform = {k:Q(n,total) for k,n in sizes.items()}
    b = marginal(columns,uniform)
    assert set(b) == set(target) and sum(b.values()) == 1
    # If p = lambda*b + (1-lambda)*r, positivity of r bounds lambda.
    cap = min(target[i] / b[i] for i in target)
    assert 0 < cap < 1
    residual = {k:(v-cap*b[k])/(1-cap) for k,v in target.items()}
    return uniform, cap, residual


def discover(target, columns):
    """Find a sparse solution. Reconstruct its weights exactly on that support."""
    import numpy as np
    from scipy.optimize import linprog
    from sympy import Matrix
    pids, cids = sorted(target), sorted(columns)
    A = [[columns[k].get(p,0) for k in cids] for p in pids]
    b = [target[p] for p in pids]
    fit = linprog(np.zeros(len(cids)), A_eq=np.array(A,dtype=float),
                  b_eq=np.array(b,dtype=float), bounds=(0,None), method='highs-ds',
                  options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
    if not fit.success:
        raise ArithmeticError(fit.message)
    support = np.flatnonzero(fit.x > 1e-10)
    selected = Matrix([[row[j] for j in support] for row in A])
    weights, free = selected.gauss_jordan_solve(Matrix(b))
    if free.rows:
        raise ArithmeticError('The reported support is not a vertex.')
    return {'residual_orbit_masses':{str(cids[j]):str(w) for j,w in zip(support,weights) if w}}


def verify(target, columns, sizes, certificate, labels):
    uniform, cap, residual = residual_target(target,columns,sizes)
    masses = {int(i):Q(x) for i,x in certificate['residual_orbit_masses'].items()}
    assert masses.keys() <= columns.keys() and all(x > 0 for x in masses.values())
    assert sum(masses.values()) == 1
    assert marginal(columns,masses) == Counter(residual)
    mixed = {k:cap*u+(1-cap)*masses.get(k,0) for k,u in uniform.items()}
    assert min(mixed.values()) > 0 and sum(mixed.values()) == 1
    assert marginal(columns,mixed) == Counter(target)
    endpoints = Counter()
    for orbit, mass in mixed.items():
        endpoints[labels[orbit]] += mass
    assert sum(endpoints.values()) == 1 and all(x > 0 for x in endpoints.values())
    limiting = [str(i) for i,v in sorted(residual.items()) if not v]
    assert limiting
    # There are at most len(target) independent marginal equalities. Their
    # sum is normalization. A strictly positive feasible point permits small
    # displacements in both directions along every null vector.
    return {
        'minimum_total_variation_to_archived_pair_law':'0',
        'exact_strictly_positive_extension_exists':True,
        'max_uniform_labelled_path_component':str(cap),
        'limiting_pair_classes':limiting,
        'nonzero_orbits_in_residual':len(masses),
        'witness_N14_end_weights':{str(k):str(v) for k,v in sorted(endpoints.items())},
        'lower_bound_affine_dimension':len(columns)-len(target),
        'uniform_path_law_pair_marginal_TV':str(sum(abs(x-target[k]) for k,x in marginal(columns,uniform).items())/2),
        'target_pair_marginal':{str(i):str(x) for i,x in sorted(target.items())},
    }


def run(growth, cert, out, find=False):
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    growth_data = read_json(growth)
    good = admissible_orders(growth_data['sequential_admissible'])
    prior = read_json(ROOT/'upstream'/'v03'/'results.json')
    certificates = {} if find else read_json(cert)
    result = {}
    for root,row in sorted(prior['paths_by_root'].items()):
        target, columns, sizes, counts = build(row, good)
        assert counts['forward_paths'] == sum(growth_data['by_root'][root]['admissible_end_marked_paths'].values())
        if find:
            _, _, residual = residual_target(target,columns,sizes)
            certificates[root] = discover(residual,columns)
        result[root] = {**counts, **verify(target,columns,sizes,certificates[root],good)}
    if find:
        dump(certificates,cert)
    dump(result,out)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--growth',type=Path,default=ROOT/'growth.json')
    p.add_argument('--certificate',type=Path,default=ROOT/'exchange_certificate.json')
    p.add_argument('--output',type=Path,default=ROOT/'exchange.json')
    p.add_argument('--discover',action='store_true',help='Find a new LP certificate (requires SciPy).')
    args = p.parse_args()
    run(args.growth,args.certificate,args.output,args.discover)
