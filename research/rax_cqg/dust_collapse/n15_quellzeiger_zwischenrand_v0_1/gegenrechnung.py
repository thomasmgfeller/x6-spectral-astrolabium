"""Full-packet quadrature cross-check, in a common positive auxiliary pairing."""
import json
import sys

import numpy as np
from scipy.stats import qmc

from nachweis import (FUTURE, FUTURE_WIDTH, INNER, MASS, PAST, ROOT,
                      cut_orders, ref)

I, P, F = (list(group) for group in (INNER, PAST, FUTURE))
DELTA = (3/722)**0.25
RADIUS = float(ref.RADIUS)


def sobol(dim, size, seed):
    return 2*qmc.Sobol(dim, scramble=True, seed=seed).random_base2(size.bit_length()-1)-1


def global_rows(y, matrix):
    return 1+(y*y@matrix-2*y*(y@matrix)+y*y*matrix.sum(0))/19


def direct(y, matrix):
    c = global_rows(y, matrix)
    step = 1/64
    shifts = np.zeros(15)
    shifts[P] = step/(2*DELTA)
    charge = (global_rows(y+shifts, matrix)-global_rows(y-shifts, matrix))/(2*step)
    return c, charge


def sewn(y, sides, pieces, omit_crossing=False):
    # Local actions include every local vertex; subtract the repeated seam.
    # Conditional fields, density support and pointer arm remain coherent.
    c = np.zeros_like(y)
    c[:, sorted(sides[0])] += 1
    c[:, sorted(sides[1])] += 1
    c[:, sorted(sides[2])] -= 1
    charge = np.zeros_like(y)
    for table in (pieces[:2] if omit_crossing else pieces):
        for (i, j), b in sorted(table.items()):
            if b:
                dy = y[:, i]-y[:, j]
                c[:, j] += b/19*dy**2
                if i in P and j not in P:
                    charge[:, j] += b/(19*DELTA)*dy
    return c, charge


def clocks_and_dwell(points, paths):
    e = -0.25+RADIUS*points[:, 0]
    u = np.array([float(ref.CENTER[v]) for v in I]) + RADIUS*points[:, 1:]
    duration = DELTA*(4-e)
    y = np.zeros((len(points), 15))
    y[:, P] = [-5, -4, -3, -2]
    y[:, 3] += e
    y[:, I] = -2+e[:, None]+(4-e[:, None])*u
    y[:, F] = [2, 3, 4, 5]
    dwell = np.zeros_like(u)
    for path in paths:
        loc = [I.index(v) for v in path]
        cuts = np.column_stack([np.zeros(len(points)),
                                (u[:, loc[:-1]]+u[:, loc[1:]])/2, np.ones(len(points))])
        dwell[:, loc] += np.diff(cuts, axis=1)/len(paths)
    return y, duration, dwell


def packet_centres(c, dwell):
    # These windows always use the ORIGINAL unshifted preparation, including
    # in the deliberately broken sewing control. The source never moves them.
    shift = np.zeros_like(dwell)
    for v, left, right in ((5, 12, 13), (12, 13, 5), (13, 5, 12)):
        shift[:, I.index(v)] = float(ref.COFACTOR_SCALE)*(c[:, left]-c[:, right])
    return [dwell-shift, dwell+shift]


def density_integrals(phase_row, duration, centres, future_w):
    # Exact integrals of a linear phase over the shared past density and the
    # seven independent xi windows. QMC is used only for e,u and outer z.
    mass_time = float(MASS)*duration
    past_sum = phase_row[:, P].sum(axis=1)
    phase = past_sum/8 + phase_row[:, F]@future_w
    scaled_inner = phase_row[:, I]*mass_time[:, None]
    past_filter = np.sinc(past_sum/(32*np.pi))
    inner_filter = np.prod(np.sinc(scaled_inner*RADIUS/np.pi), axis=1)
    # Seven dT factors and seven dw factors; normalize with one common reference.
    weight = (duration/(4.25*DELTA))**14
    common = weight*past_filter*inner_filter*np.exp(1j*phase)
    return [np.mean(common*np.exp(1j*np.sum(scaled_inner*x, axis=1))) for x in centres]


def matrices(arms):
    # axes: z, history packet, pointer arm. Initial arm weights 1/sqrt(2).
    a, b = arms[:, :, 0], arms[:, :, 1]
    def gram(v):
        return v.conj().T@v/len(v)
    full = (gram(a)+gram(b))/2
    plus, minus = gram((a-1j*b)/2), gram((a+1j*b)/2)
    assert np.allclose(plus+minus, full, rtol=0, atol=1e-13)
    assert np.linalg.eigvalsh(full).min() >= -1e-13
    return np.array([full, plus, minus]), (np.diag(plus)/np.diag(full)).real


def run_level(inner, outer, paths, matrix, sides, pieces, broken=False):
    y, duration, dwell = clocks_and_dwell(inner, paths)
    # Preparation is common to both algorithms. C at the three interior nodes
    # does not depend on sampled future data.
    centres = packet_centres(global_rows(y, matrix), dwell)
    routes = ['direkt', 'verklebt'] + (['ohne_kreuzwirkung'] if broken else [])
    arms = {route: [] for route in routes}
    for z in outer:
        y[:, F[1:]] = [3, 4, 5]+float(FUTURE_WIDTH)*z[:3]
        future_w = 1/8+float(FUTURE_WIDTH)*z[3:]
        for route in routes:
            c, p = (direct(y, matrix) if route == 'direkt' else
                    sewn(y, sides, pieces, omit_crossing=route == 'ohne_kreuzwirkung'))
            values = [density_integrals(-0.5*c+coupling*p, duration, centres, future_w)
                      for coupling in (0, 1)]
            arms[route].append(np.array(values).T)
    return {key: np.array(value) for key, value in arms.items()}


def complex_entries(array):
    return np.stack([array.real, array.imag], axis=-1).tolist()


def evaluate():
    config = json.loads((ROOT/'pruefvertrag.json').read_text())['numerik']
    paths, coeff, sides, pieces = cut_orders()
    matrix = np.zeros((15, 15), dtype=int)
    for edge, value in coeff.items():
        matrix[edge] = value
    levels = []
    for si, sz in config['scrambles']:
        n, m = config['stufen'][-1]
        ins, outs = sobol(8, n, si), sobol(7, m, sz)
        for n, m in config['stufen']:
            final = [n, m] == config['stufen'][-1]
            arms = run_level(ins[:n], outs[:m], paths, matrix, sides, pieces, broken=final)
            direct_m, prob = matrices(arms['direkt'])
            sewn_m, sewn_p = matrices(arms['verklebt'])
            off = np.repeat(arms['direkt'][:, :, :1], 2, axis=2)
            off_m, off_p = matrices(off)
            err = float(np.max(np.abs(direct_m-sewn_m)))
            amp_err = float(np.max(np.abs(arms['direkt']-arms['verklebt'])))
            tol = config['absolute_vergleichstoleranz']
            assert err < tol and amp_err < tol
            assert max(abs(prob-sewn_p)) < tol
            assert np.max(np.abs(off_m[0]-off_m[0, 0, 0])) < tol
            assert max(abs(off_p-0.5)) < tol
            assert prob[0] > 200333/400000 and prob[1] < 399541/800000
            row = {'seeds':[si, sz], 'innen':n, 'aussen':m,
                   'P_Yplus':prob.tolist(), 'P_abstand':float(prob[0]-prob[1]),
                   'max_fehler_arme':amp_err, 'max_fehler_drei_matrizen':err}
            if final:
                bad_m, bad_p = matrices(arms['ohne_kreuzwirkung'])
                bad_error = float(np.max(np.abs(direct_m-bad_m)))
                assert bad_error > tol and max(abs(bad_p-prob)) > tol
                row.update(matrixformat='Zeilen/Spalten positives, negatives Paket; Zahl [Re, Im]',
                           reihenfolge=['D', 'D_Yplus', 'D_Yminus'],
                           direkt=complex_entries(direct_m), verklebt=complex_entries(sewn_m),
                           kontrolle_aus=complex_entries(off_m[0]),
                           ohne_kreuzwirkung_P=bad_p.tolist(),
                           ohne_kreuzwirkung_max_matrixdifferenz=bad_error)
            levels.append(row)
    return levels


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Python ohne -O verwenden.')
    print(json.dumps(evaluate(), indent=2, ensure_ascii=False))
