"""Audit finite echo graphs, isotropic optical caps and ideal band exposure.

Python 3.10+, standard library. All mathematical inequalities are evaluated
with rational bounds. Displayed decimal approximations are for readability.
Run by itself for the analytic checks. With the accompanying basis/ directory
the original PR 382 echo records are replayed as well. Use --json for details.
"""
from fractions import Fraction as F
from math import comb, isqrt
from itertools import product
from pathlib import Path
from hashlib import sha256
import argparse
import json
from tempfile import TemporaryDirectory
from zipfile import ZipFile

DT = F(1, 1000)
ANGLE = F(1, 9200)
WIDTH = ANGLE / 200
GRID = 10 ** 26

def sin_bounds(x):
    assert 0 <= x <= 1
    s = x - x ** 3 / 6 + x ** 5 / 120
    return (s - x ** 7 / 5040, s)

def sqrt_grid(x):
    floor = isqrt(x.numerator * GRID ** 2 // x.denominator)
    lo = F(floor, GRID)
    return (lo, lo if lo ** 2 == x else F(floor + 1, GRID))

def scaled_sine_square(interval,scale):
    return (sin_bounds(interval[0])[0] ** 2 / scale, sin_bounds(interval[1])[1] ** 2 / scale)

def display(interval):
    return {'lower':str(interval[0]),'upper':str(interval[1]),
            'approx':[float(interval[0]),float(interval[1])]}

def quotient(a,b):
    assert min(b) > 0 and min(a) >= 0
    return (a[0] / b[1], a[1] / b[0])

def const_caps():
    modes = []
    for r in (F('8.5'),F('9.9')):
        a = DT / r
        dip = scaled_sine_square((a, a), 4)
        area = scaled_sine_square((a / 2, a / 2), 1)
        gap = (area[0] ** 2, area[1] ** 2)
        assert area[0] - dip[1] <= gap[0] <= gap[1] <= area[1] - dip[0]
        modes.append((dip, area, gap))
    return {'degree1_ratio':display(quotient(modes[0][0],modes[1][0])),
            'gap_ratio':display(quotient(modes[0][2],modes[1][2])),
            'leading_ratio':str(F(99,85)**2),'bands':[
                {'degree1': display(dip), 'degree0': display(mass), 'gap': display(gap)}
                for dip,mass,gap in modes]}

def h(s):
    if s<=0:
        return F(0)
    if s>=1:
        return F(1)
    return s ** 3 * (10 - 15 * s + 6 * s * s)

def cap_for_published_metric(which,steps=1024):
    # d(x) and the polynomial radial profile are from the N15 comparison study.
    lo5, hi5 = sqrt_grid(F(5))
    def at_time(t):
        def field(root5):
            dx = t / (5 * root5 / 3)
            return F(199, 5000) * h(F(1, 2) + dx) + F(161, 625) * h(64 * dx + int(which == 'A'))
        d_lo, d_hi = (field(hi5), field(lo5))
        return (sqrt_grid(1 / (100 * (1 - d_lo)))[0], sqrt_grid(1 / (100 * (1 - d_hi)))[1])
    # Monotone endpoint sums bound the null angular excursion on the wall.
    vals = [at_time(DT * i / steps) for i in range(steps + 1)]
    lower = sum((a for a, b in vals[:-1]), F(0)) * DT / steps
    upper = sum((b for a, b in vals[1:]), F(0)) * DT / steps
    # Bulk shortcut gain. Along any connecting path r in [10−DT/2,10+DT/2].
    # 1-f=(u²-1)²(81u²+8)/8, u=r/10. Bound |f'| via this identity.
    u = 1 + DT / 20
    eps = u * u - 1
    fp = (4 * u * eps * (81 * u * u + 8) + 162 * u * eps ** 2) / 8
    assert fp < F('.01')
    lower_r = 10 - DT / 2
    lip = 1 / (lower_r ** 2 * F('.8')) + F('.3') * fp / (20 * lower_r * F('.5'))
    assert lip < F(1, 40)
    # Integral L|r−10|−w_min r'²/2 <= L² DT³/(6 w_min) by Cauchy-Schwarz.
    upper += F(1, 40) ** 2 * DT ** 3 / (6 * F(1, 10))
    return (lower, upper)

def moving_caps():
    alpha, beta = (cap_for_published_metric(x) for x in ('A', 'B'))
    dip = quotient(scaled_sine_square(alpha, 4), scaled_sine_square(beta, 4))
    assert dip[0] > F('1.3565400') and dip[1] < F('1.3565406')
    for a,b in (alpha,beta):
        assert 0 < a <= b < 1
    assert alpha[0] > ANGLE + WIDTH and beta[1] < ANGLE - WIDTH
    return {'alpha_A': display(alpha), 'alpha_B': display(beta), 'degree1_ratio': display(dip)}

def band_fraction_ideal(cutoff):
    low, high = (ANGLE - WIDTH, ANGLE + WIDTH)
    if cutoff<=low:
        return (F(0), F(0))
    if cutoff>=high:
        return (F(1), F(1))
    # Use cos(low)−cos(cutoff) = 2 sin((low+cutoff)/2) sin((cutoff−low)/2).
    a, b = sin_bounds((cutoff + low) / 2)
    c, d = sin_bounds((cutoff - low) / 2)
    e, f = sin_bounds(ANGLE)
    g, h = sin_bounds(WIDTH)
    return quotient((a * c, b * d), (e * g, f * h))

def plateaus():
    lower, upper = (DT / (ANGLE + WIDTH), DT / (ANGLE - WIDTH))
    rA, rB = (F('8.5'), F('9.9'))
    assert band_fraction_ideal(DT / rA) == (1, 1) and band_fraction_ideal(DT / rB) == (0, 0)
    mid = band_fraction_ideal(DT / F('9.2'))
    assert 0 < mid[0] <= mid[1] < 1
    errA = (lower - rA) / (lower + rA)
    errB = (rB - upper) / (rB + upper)
    assert errA == F(263, 7097) and errB == F(1301, 38101)
    return {'identical_fraction_one_interval':list(map(str,(rA,lower))),
            'identical_fraction_zero_interval':list(map(str,(upper,rB))),
            'minimax_relative_at_plateaus':list(map(str,(errA,errB))),
            'conditional_fraction_at_radius_9.2':display(mid)}

def counterexamples():
    # Early flat calibration a=1 comoving shell chi=10, same R*=9.3.
    # Spatial chord D=20 sin(theta/2), conformal time integrated exactly.
    low = 20 * sin_bounds((ANGLE - WIDTH) / 2)[0]
    high = 20 * sin_bounds((ANGLE + WIDTH) / 2)[1]
    def budget(c):
        return DT * F(100, 93) * (1 + c / 2)
    assert budget(F(1, 1000)) < low and budget(F(1, 20)) > high
    assert F(9) * (ANGLE + WIDTH) < DT and F('7.5') * (ANGLE + WIDTH) < DT
    return {'identical_Rstar':'93/10','B_slow':str(budget(F(1,1000))),
            'B_fast':str(budget(F(1,20))),'chord_enclosure':display((low,high)),
            'static_R_both_yes':['15/2','9'],'minimax_same_single_fraction':str(F(1,11)),
            'strictly_invertible_radii_static_surface':list(map(str,(DT/(ANGLE+WIDTH),DT/(ANGLE-WIDTH))))}

def exposure():
    grid = GRID
    a, b = sin_bounds(ANGLE)
    c, d = sin_bounds(WIDTH)
    pl = int(grid * a * c)
    ph = -(-(grid * b * d) // 1)
    empty_lo = empty_hi = grid
    first_possible = None
    checkpoints = {}
    for n in range(2,1000001):
        k = n - 1
        prev = (empty_lo, empty_hi)
        assert k * ph < grid
        empty_lo = empty_lo * (grid - k * ph) // grid
        empty_hi = min(grid, -(-(empty_hi * (grid - k * pl) + comb(k, 2) * ph * ph) // grid))
        assert 0 <= empty_lo <= empty_hi
        if first_possible is None and 20*empty_lo<=grid:
            first_possible = n
            checkpoints[n - 1] = prev
            checkpoints[n] = (empty_lo, empty_hi)
        if 20*empty_hi<=grid:
            checkpoints[n - 1] = prev
            checkpoints[n] = (empty_lo, empty_hi)
            break
    else:
        raise ArithmeticError('95% exposure not bracketed')
    assert [first_possible, n] == [318471, 318478]
    return {'band_probability':display((F(pl,grid),F(ph,grid))),
            'upper_prob_at_least_one':{str(k):float(comb(k,2)*F(ph,grid)) for k in (48,64)},
            '95_percent_first_exposure_threshold':[first_possible,n],
            'empty_probability_endpoints_scaled_by_1e26':checkpoints}

def charpoly(nodes,edges):
    """Integer coefficients of det(tI-A) by traces/Newton identities."""
    def adj(i,j):
        return int(tuple(sorted((i, j))) in edges)
    n = len(nodes)
    a = [[adj(i, j) for j in nodes] for i in nodes]
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coeff = [1]
    for k in range(1,n+1):
        b = [[sum((a[i][l] * b[l][j] for l in range(n))) for j in range(n)] for i in range(n)]
        t = -sum((b[i][i] for i in range(n)))
        assert t % k == 0
        coeff.append(t // k)
        for i in range(n):
            b[i][i] += coeff[-1]
    return coeff

def radial_and_finite_controls():
    nodes = tuple('ABC')
    all_edges = {('A', 'B'), ('A', 'C'), ('B', 'C')}
    assert charpoly(nodes, all_edges) == [1, 0, -3, -2]
    assert charpoly(nodes, set()) == [1, 0, 0, 0]
    return {'empty_graph_rank': 0, 'complete_K3_rank': 3}

def ltbreplay(basis):
    from importlib.util import spec_from_file_location, module_from_spec
    sums={'Netzaufnahmen.json':'b14d2b80e679c8c00bafef77783790d3d10008cf0b77464bef20bc0e8291303f',
          'Ergebnisse.json':'97c59469388d6f687ed0f51e702f527d1879ef4f5afb4adf5c02c6fbbdaea779',
          'echos.py':'eb451280271dbd86fc6f84053681c65eceb18af5b1585ad37010f8b56e681ff2'}
    for name,expected in sums.items():
        assert sha256((basis / name).read_bytes()).hexdigest() == expected, name
    spec = spec_from_file_location('pr382_echo', basis / 'echos.py')
    e = module_from_spec(spec)
    spec.loader.exec_module(e)
    raw = json.loads((basis / 'Netzaufnahmen.json').read_bytes())
    archive = json.loads((basis / 'Ergebnisse.json').read_bytes())
    out = {}
    for m,data in raw.items():
        a = F(13 * 492, 640)
        state = {}
        masked = []
        for edge,(lo,hi) in data['bounds'].items():
            theta = (e.decode(lo, a / 10, 0)[0], e.decode(hi, a / 10, 0)[1])
            s = e.late(F(m), a, theta)
            state[tuple(edge.split('|'))] = 'YES' if s == ['JA', 'JA'] else 'NO' if s == ['NEIN', 'NEIN'] else 'OPEN'
            if e.contained(theta):
                masked.append(edge)
        assert masked == ['B|D'] and archive['NOT_RUN'] == 60
        yes = {p for p, x in state.items() if x == 'YES'}
        open_edges = [p for p, x in state.items() if x == 'OPEN']
        nodes = sorted({v for p in state for v in p})
        assert len(nodes) == 7 and len(state) == 21
        possible = []
        for bits in product((0,1),repeat=len(open_edges)):
            edges = yes | {p for p, b in zip(open_edges, bits) if b}
            coeff = charpoly(nodes, edges)
            # independent coefficient test via determinant interpolation at integer points
            for t in range(8):
                exact = determinant(nodes, edges, t)
                assert sum((c * t ** (7 - i) for i, c in enumerate(coeff))) == exact
            possible.append({'edges': len(edges), 'chi_coeffs': coeff})
        out[m]={'yes':len(yes),'no':len(state)-len(yes)-len(open_edges),'open':['|'.join(p) for p in open_edges],
                'masked_pair':masked[0],'masked_evaluation':state[tuple(masked[0].split('|'))],
                'possible_characteristic_polynomials':possible,'R0_test':archive['material_echos'][m]['calibrations']}
    assert out['4']['possible_characteristic_polynomials'][0]['chi_coeffs'] == [1, 0, -21, -70, -105, -84, -35, -6]
    return out

def determinant(nodes,edges,t):
    a = [[F(t if i == j else -int(tuple(sorted((i, j))) in edges)) for j in nodes] for i in nodes]
    det = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return 0
        if pivot!=i:
            a[i], a[pivot] = (a[pivot], a[i])
            det = -det
        det *= a[i][i]
        for j in range(i+1,len(a)):
            mult = a[j][i] / a[i][i]
            for l in range(i+1,len(a)):
                a[j][l] -= mult * a[i][l]
    return det

def calibration():
    # Dynamic optical collar R(t)=R*−vt, v>0; at fixed delay and early echo,
    # gamma=z/(exp(z)−1). A rational Taylor enclosure at illustrative z=1/10.
    z = F(1, 10)
    term = F(1)
    partial = F(1)
    for k in range(1,11):
        term *= z / k
        partial += term
    rem = term * z / 11 / (1 - z / 12)
    gamma = (z / (partial + rem - 1), z / (partial - 1))
    assert 0 < gamma[0] <= gamma[1] < 1
    return {'ideal_static_fixed_pair': 1, 'dynamic_example_z_0.1': display(gamma)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    src = parser.add_mutually_exclusive_group()
    src.add_argument('--basis', type=Path, help='Path to the three PR 382 source files')
    src.add_argument('--pr382-zip', type=Path, help='Use the original PR 382 offline ZIP')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    report={'static_caps':const_caps(),'published_kinematic_pair':moving_caps(),
            'inversion_controls':counterexamples(),'band_plateaus':plateaus(),'uniform_exposure':exposure(),
            'finite_graph_controls':radial_and_finite_controls(),'calibration':calibration()}
    default_basis = Path(__file__).resolve().parent / 'basis'
    if args.pr382_zip:
        with TemporaryDirectory() as tmp,ZipFile(args.pr382_zip) as archive:
            for name in ('echos.py','Netzaufnahmen.json','Ergebnisse.json'):
                (Path(tmp) / name).write_bytes(archive.read(name))
            report['LTB'] = ltbreplay(Path(tmp))
    elif args.basis is not None or default_basis.is_dir():
        report['LTB'] = ltbreplay(args.basis if args.basis is not None else default_basis)
    else:
        report['LTB'] = 'NOT_RUN: original PR 382 inputs require basis/ from the accompanying package.'
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print('Analytic checks passed. Ideal static degree-1 ratio:', report['static_caps']['degree1_ratio']['approx'])
        print('Kinematic pair, bulk optical cap bounds:', report['published_kinematic_pair']['degree1_ratio']['approx'])
        print('95% probability of a nonempty iid angular band:', report['uniform_exposure']['95_percent_first_exposure_threshold'])
        print('PR 382:', {m:(r['yes'],r['no'],r['masked_evaluation']) for m,r in report['LTB'].items()}
              if isinstance(report['LTB'],dict) else report['LTB'])
if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Please run without -O.')
    main()
