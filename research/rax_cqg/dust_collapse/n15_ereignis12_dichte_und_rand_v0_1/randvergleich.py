"""Conditional half-density states at the ordinary cut after 13."""
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'quellen'))
from randtest import D, H, WINDOW, s, endpoint_grid, nodes, waves

PREPARATIONS = {
    'arm_minus': (1, 0), 'arm_plus': (0, 1),
    '0': (1, 1), 'pi/2': (1, 1j), 'pi': (1, -1), '3pi/2': (1, -1j)
}


def evaluate(method, degree, tag, pulse):
    q, w = nodes(method, degree)
    z = .125 + WINDOW*q[None, :, None]
    incoming_weights = np.outer(w, w).ravel()
    sides, blocks = [], []
    for side, grid, outer in endpoint_grid(method, degree, tag):
        for start in range(0, len(outer), 256):
            part = slice(start, start + 256)
            arms = []
            for sign in (-1, 1):
                u = .25 + sign*s + H*q[None, None, :]
                left, f, c, x13, c13 = waves(method, grid[part], z, u, pulse, components=True)
                arg = D*f*c/200
                base = left * (f/2) * np.exp(1j*D*(f*c+x13*c13))
                half_average = (np.sinc(arg/np.pi) if method == 'gauss'
                                else 1 - arg**2/6 + arg**4/120)
                half_columns = [((base*half_average*np.exp(1j*t*arg)).reshape(len(base), -1)
                                 @ incoming_weights) for t in (-1, 1)]
                full = (base*2*np.sinc(2*arg/np.pi)).reshape(len(base), -1) @ incoming_weights
                np.testing.assert_allclose(sum(half_columns), full, atol=2e-18, rtol=3e-14)
                arms.append(np.column_stack(half_columns))
            blocks.append(np.stack(arms, axis=1) * np.sqrt(outer[part, None, None]))
            sides.append(np.full(len(outer[part]), side))
    elements = np.concatenate(blocks, axis=0)
    lower_side = np.concatenate(sides) < 0
    out = {}
    for name, (a, b) in PREPARATIONS.items():
        low, high = (a*elements[:, 0] + b*elements[:, 1]).T
        weight_l = np.vdot(low, low).real
        weight_h = np.vdot(high, high).real
        gram_cross = np.vdot(low, high)
        residual = high - low*(gram_cross/weight_l)
        distance = np.linalg.norm(residual)/np.sqrt(weight_h)
        # The ratio is invariant under a common rescaling of the two histograms.
        row_weight = abs(low)**2 + abs(high)**2
        native = abs(low+high)**2
        out[name] = {
            'cut13_trace_distance': float(distance),
            'relative_phase_rad': float(np.angle(gram_cross)),
            'nonselective_two_bin_u11_low': float(sum_np(row_weight[lower_side])/sum_np(row_weight)),
            'ordinary_coherent_u11_low': float(sum_np(native[lower_side])/sum_np(native)),
            'nonselective_minus_coherent_over_coherent':
                float((sum_np(row_weight) - sum_np(native))/sum_np(native)),
            'bin_ratio_high_over_low': float(weight_h/weight_l)
        }
    return out


def sum_np(array):
    return np.sum(array, dtype=np.float64)


def main():
    ref = json.loads((ROOT/'quellen/dichte.json').read_text())
    rows = {}
    max_difference = {}
    for tag_name, tag in [('L',255/2048), ('H',257/2048)]:
        rows[tag_name] = {}
        for pulse in (-1, 0, 1):
            primary = evaluate('gauss', 5, tag, pulse)
            alternate = evaluate('cc', 6, tag, pulse)
            for prep, values in primary.items():
                for field, value in values.items():
                    error = abs(value-alternate[prep][field])
                    max_difference[field] = max(max_difference.get(field, 0), error)
                    if error > 2e-10:
                        raise ArithmeticError((tag_name, pulse, prep, field, error))
            rows[tag_name][str(pulse)] = primary
    for i, name in enumerate(('0','pi/2','pi','3pi/2')):
        for size, key in [('1','ordinary_coherent_u11_low'),('2','nonselective_two_bin_u11_low')]:
            data = ref['bins'][size]
            low = rows['L']
            np.testing.assert_allclose(low['0'][name][key], data['native_prob_zero'][i], atol=2e-12, rtol=0)
            gap = low['1'][name][key] - low['-1'][name][key]
            np.testing.assert_allclose(gap,data['plus_minus_difference'][i],atol=2e-12,rtol=0)
    return {'quadrature_difference_max': max_difference, 'rows':rows}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, allow_nan=False))
