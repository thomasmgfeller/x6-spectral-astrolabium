"""Test for a common rank-one history sector of the inherited two-density readout."""
import argparse
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.linalg import eigh
import sympy as sp


ROOT = Path(__file__).resolve().parent


def complex_array(pairs):
    parts = np.asarray(pairs)
    return parts[..., 0] + 1j * parts[..., 1]


def hermitian_form(pairs):
    # Rationalize the actual stored binary64 coordinates. Only the Hermitian
    # part contributes to real expectations; the discarded skew is checked.
    mat = sp.Matrix([[sp.Rational(x) + sp.I * sp.Rational(y) for x, y in row]
                     for row in pairs])
    form = (mat + mat.H) / 2
    assert form[0, 0] > 0 and sp.cancel(form.det()) > 0
    return form


def exact_obstruction(densities):
    operators = []
    for bins in densities:
        forms = [hermitian_form(pairs) for pairs in bins]
        total = sum(forms, sp.zeros(2))
        operators.append((total.inv() * forms[1]).applyfunc(sp.cancel))
    low, high = operators
    commutator = (low * high - high * low).applyfunc(sp.cancel)
    det = sp.cancel(commutator.det())
    # Direct check of the centralizer on the traceless matrix basis. The
    # identity supplies the remaining complex dimension.
    traceless = [sp.diag(1, -1), sp.Matrix([[0, 1], [0, 0]]), sp.Matrix([[0, 0], [1, 0]])]
    columns = [sp.Matrix([entry for op in operators for entry in (op*x - x*op)])
               for x in traceless]
    assert sp.Matrix.hstack(*columns).rank() == 3
    # Exact strict bounds for this finite archived readout, before conversion
    # to floats for presentation. Invertibility excludes a common eigenline.
    assert sp.Rational('1.64e-13') < sp.re(det) < sp.Rational('1.66e-13')
    assert sp.Rational('4.6e-15') < sp.im(det) < sp.Rational('4.7e-15')
    return [float(sp.re(det)), float(sp.im(det))]


def complex_box(pair, radius):
    shift = mp.iv.mpf([-1, 1]) * mp.iv.mpf(radius)
    return mp.iv.mpc(mp.iv.mpf(pair[0]) + shift, mp.iv.mpf(pair[1]) + shift)


def perturbation_box(sector, packets):
    # Independent route from scalar Gram, Gaussian bin and individual lobes.
    # All real/imaginary coordinates vary independently in the specified boxes.
    mp.iv.dps = 50
    gram, middle = [tuple(complex_box(entry, '1e-12') for row in matrix for entry in row)
                    for matrix in (sector['gram_scalar'], sector['pointer_effects_scalar'][1])]
    g, h, k, j = gram
    u, v, w, z = middle
    norm = g*j - h*k
    a, b, c, d = (j*u-h*w)/norm, (j*v-h*z)/norm, (g*w-k*u)/norm, (g*z-k*v)/norm
    amplitudes = [[sum(complex_box(pair, '2e-10') for pair in lobes)
                   for lobes in packet['lobes']] for packet in packets]
    # sqrt(2) cancels in each branch ratio. r = (B_high/A_high)/(B_low/A_low).
    r = (amplitudes[1][1] * amplitudes[0][0]) / (amplitudes[0][1] * amplitudes[1][0])
    # L(t) = [[a,b*t],[c/t,d]]. Factoring the commutator determinant avoids
    # subtracting nearby O(1) quantities when the phase ratios nearly agree.
    difference, addition, diagonal = 1-r, 1+r, a-d
    det = -b*c*difference*difference*(diagonal*diagonal*r + b*c*addition*addition)/(r*r)
    assert det.real.a > 0
    def bounds(interval):
        return [math.nextafter(float(interval.a), -math.inf),
                math.nextafter(float(interval.b), math.inf)]
    return {'real': bounds(det.real), 'imag': bounds(det.imag)}


def run(inputs):
    if not __debug__:
        raise RuntimeError('Run with assertions active')
    sector, response = [json.loads((inputs / name).read_text())
                        for name in ('sector.json', 'response.json')]
    assert sector['order'] == response['order'] == [1790, 5374]
    assert response['densities'] == ['1/8', '1/4']
    assert response['outcomes'] == ['left', 'middle', 'right', 'failure']
    gram = complex_array(sector['gram_scalar'])
    bins = complex_array(sector['pointer_effects_scalar'])
    assert np.array_equal(bins[0], bins[2])
    assert np.max(abs(bins.sum(axis=0) - gram)) < 1e-14
    eigenvalues, vectors = eigh(bins[1], gram)
    assert 0 < eigenvalues[0] < eigenvalues[1] < 1
    # Positive control: a genuine reducing projector on the *output* span.
    vector = vectors[:, 0]
    projector = np.outer(vector, vector.conj()) @ gram
    assert np.max(abs(projector @ projector - projector)) < 1e-14
    assert max(np.max(abs(projector.conj().T @ f - f @ projector)) for f in bins) < 1e-14
    output_operator = np.linalg.solve(gram, bins[1])
    rows = []
    for row in response['production_grids']:
        raw = complex_array(row['coherent_effects'])
        assert np.max(abs(raw - raw.conj().swapaxes(-2, -1))) < 1e-19
        amplitudes = np.array([complex_array(p['lobes']).sum(axis=1)/np.sqrt(2)
                               for p in row['packets']]).T
        operators = []
        for index, factors in enumerate(amplitudes):
            preparation = np.diag(factors)
            assert np.min(abs(factors)) > .006
            assert np.max(abs(preparation.conj().T @ bins @ preparation - raw[index])) < 1e-19
            induced = np.linalg.solve(raw[index].sum(axis=0), raw[index, 1])
            assert np.max(abs(induced - np.linalg.solve(preparation, output_operator @ preparation))) < 1e-14
            # A density-specific projector DOES work on all three accepted bins.
            adapted = np.linalg.solve(preparation, projector @ preparation)
            assert np.max(abs(adapted.conj().T @ raw[index] - raw[index] @ adapted)) < 1e-18
            operators.append(induced)
        low, high = operators
        commutator = low @ high - high @ low
        det = exact_obstruction(row['coherent_effects'])
        assert abs(complex(*det) - np.linalg.det(commutator)) < 1e-23
        enclosure = perturbation_box(sector, row['packets'])
        assert all(enclosure[key][0] < x < enclosure[key][1]
                   for key, x in zip(('real', 'imag'), det))
        ratio = (amplitudes[1, 1]/amplitudes[1, 0]) / (amplitudes[0, 1]/amplitudes[0, 0])
        rows.append({'grid': row['grid'], 'relative_branch_ratio': [float(ratio.real), float(ratio.imag)],
                     'commutator_determinant': det, 'determinant_perturbation_box': enclosure})
    return {'order': response['order'], 'densities': response['densities'],
            'scalar_output_middle_eigenvalues': eigenvalues.tolist(),
            'common_history_commutant_dimension_over_C': 1,
            'perturbation_radii_per_real_and_imaginary_coordinate':
                {'scalar_gram_and_middle_bin': '1e-12', 'clock_lobes': '2e-10'},
            'scope': 'Exact obstruction for Hermitian parts of the archived binary64 effects. '
                     'Independent input-box propagation is conditional on the indicated radii; '
                     'quadrature convergence is empirical.', 'grids': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=ROOT/'prior')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(args.inputs), indent=2, sort_keys=True) + '\n')
