"""Independent interval counting, action polarisation and exact propagator checks."""
from fractions import Fraction as F
from itertools import combinations
from zipfile import ZipFile
import json
from ordnung import ROOT, load_background, operators, select
from puls import block, run


def direct_matrix(bg):
    past = {j: {i for i, k in bg.relation if k == j} for j in bg.nodes}
    future = {j: {k for i, k in bg.relation if i == j} for j in bg.nodes}
    coeff = {0: 1, 1: -9, 2: 16, 3: -8}
    return [[-1 if i == j else coeff.get(len(future[i] & past[j]), 0) if i in past[j] else 0
             for i in bg.nodes] for j in bg.nodes]


def action(b, phi):
    """Sum the published Gamma product identity at unit volume and zero mass."""
    total = 0
    for i, row in enumerate(b):
        square = sum(v * x*x for v, x in zip(row, phi))
        linear = sum(v * x for v, x in zip(row, phi))
        total += square - 2 * phi[i] * linear + phi[i]**2 * sum(row)
    return -F(total, 4)


def polarise(b):
    n = len(b)
    basis = [[int(i == j) for j in range(n)] for i in range(n)]
    halfdiag = [action(b, v) for v in basis]
    return [[action(b, [a + c for a, c in zip(basis[i], basis[j])]) - halfdiag[i] - halfdiag[j]
             for j in range(n)] for i in range(n)]


def det(matrix):
    """Bareiss elimination with exact integer divisions and row pivoting."""
    a = [row.copy() for row in matrix]
    sign, previous = 1, 1
    for k in range(len(a) - 1):
        p = next((j for j in range(k, len(a)) if a[j][k]), None)
        if p is None:
            return 0
        if p != k:
            a[k], a[p] = a[p], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                value = a[i][j] * pivot - a[i][k] * a[k][j]
                a[i][j], rem = divmod(value, previous)
                assert rem == 0
        previous = pivot
    return sign * a[-1][-1]


def mixed_checks(bg, b, data):
    """Verify off/on dust finite differences at exact rational test coordinates."""
    contract = json.loads((ROOT / 'basis/action_contract.json').read_bytes())
    assert contract['parameters']['direct_dust_scalar_coupling'] == 0
    with ZipFile(ROOT / 'basis/N19.zip') as archive:
        fixed = json.loads(archive.read('Paar.json'))['fixed_rounded']
    y = {int(k): sum(map(F, pair))/2 for k, pair in fixed['Y'].items()}
    w = {int(k): sum(map(F, pair))/2 for k, pair in fixed['w'].items()}
    sender, _ = select(bg)
    phi = [F(data['action']['all_arms']['on'][k]) for k in bg.nodes]
    zero = [F(0)] * len(bg.nodes)

    def total(clocks, weights, field, strength):
        dust = 19*sum(weights.values()) + sum(weights[j]*b[j][i]*(clocks[j]-clocks[i])**2
                                               for i, j in bg.relation)
        return dust + action(b, field) - strength*field[sender]

    step = F(1, 10**8)
    count = 0
    for i in bg.inner:
        for coordinate in (['clock', 'weight'] if w[i] else ['clock']):
            left, right = y.copy(), w.copy()
            if coordinate == 'clock':
                left[i] += step
            else:
                right[i] += step
            diff_on = total(left, right, phi, 1) - total(y, w, phi, 1)
            diff_off = total(left, right, zero, 0) - total(y, w, zero, 0)
            assert diff_on == diff_off
            count += 1
    return count


def audit():
    bg = load_background()
    sender, receiver = select(bg)
    b = direct_matrix(bg)
    h = polarise(b)
    assert (b, h) == operators(bg)
    data = run()
    inner = bg.inner
    signed = [[int(2 * v) for v in row] for row in block(h, inner, inner)]
    assert all(2*h[i][j] == signed[k][l] for k,i in enumerate(inner) for l,j in enumerate(inner))
    determinant = det(signed)
    assert determinant
    topology = sorted(bg.nodes, key=lambda j: sum(k == j for _, k in bg.relation))
    for c, source in enumerate(inner):
        predicted = {i: 0 for i in bg.nodes}
        for j in topology:
            if j in inner:
                predicted[j] = sum(b[j][i] * predicted[i] for i in bg.nodes if (i, j) in bg.relation) - int(j == source)
        for r, node in enumerate(inner):
            # (H^-1)_{r,c}=2 cofactor_{c,r}(2H)/det(2H).
            minor = [[v for j, v in enumerate(row) if j != r]
                     for i, row in enumerate(signed) if i != c]
            val = F(2 * (-1)**(c+r) * det(minor), determinant)
            assert str(val) == data['action']['all_inner_sources'][source]['response'][node]
            assert str(predicted[node]) == data['bd_probe']['all_inner_sources'][source]['response'][node]
    # A covariant matrix and a unique solution imply a covariant full field.
    swaps = 0
    for a, c in combinations(bg.nodes, 2):
        perm = {i: (c if i == a else a if i == c else i) for i in bg.nodes}
        renamed = bg.renamed(perm)
        assert select(renamed) == (perm[sender], perm[receiver])
        b2, h2 = operators(renamed)
        for src, mat, tag in [(b, b2, 'bd_probe'), (h, h2, 'action')]:
            assert all(mat[perm[i]][perm[j]] == src[i][j] for i in bg.nodes for j in bg.nodes)
            for key, loc, strength in [('off', sender, 0), ('on', sender, 1),
                                       ('negative', sender, -1), ('reverse', receiver, 1)]:
                vals = data[tag]['all_arms'][key]
                field = {perm[i]: F(v) for i, v in vals.items()}
                for i in renamed.inner:
                    assert sum(mat[i][j] * field[j] for j in renamed.nodes) == strength * int(i == perm[loc])
        swaps += 1
    # Read two equal rows directly from the polarised action, without row reduction.
    h_node, = [i for i in bg.nodes if bg.weights[i] == (0, 0)
               and (i, receiver) in bg.relation and (i, sender) not in bg.relation
               and (sender, i) not in bg.relation]
    support = sorted({sender} | {j for i, j in bg.relation if i == sender})
    assert [h[sender][j] for j in support] == [h[h_node][j] for j in support]
    assert data['retarded_action_fixed']['augmented_rank'] == data['retarded_action_fixed']['rank'] + 1
    assert data['retarded_action_free_future']['augmented_rank'] == data['retarded_action_free_future']['rank'] + 1
    assert data['action']['receiver'] == {'off': '0', 'on': '1/5', 'negative': '-1/5'}
    assert data['bd_probe']['receiver'] == {'off': '0', 'on': '-1', 'negative': '1'}
    assert data['action']['reverse_at_sender'] == '1/5' and data['bd_probe']['reverse_at_sender'] == '0'
    assert not data['action']['retarded_inner_sources'] and data['bd_probe']['retarded_inner_sources'] == inner
    return {'det_2H_inner': str(determinant), 'inner_inverse_entries_per_operator': len(inner)**2,
            'polarised_hessian_entries': len(bg.nodes)**2, 'all_transpositions': swaps,
            'dust_finite_differences_off_on': mixed_checks(bg, b, data),
            'identical_rows_on_sender_future': [sender, h_node],
            'columns': support, 'coefficients': list(map(str, [h[sender][j] for j in support]))}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
