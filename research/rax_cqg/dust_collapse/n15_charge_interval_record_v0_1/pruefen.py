"""Replay the interval and overlap diagnostics from the pinned PR 336 study directory."""
import argparse
import csv
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np


def coefficients(amplitudes, gram, weights):
    first = amplitudes * weights[0, :, None]
    delta = amplitudes * (weights[1] - weights[0])[:, None]
    g_first = gram @ first
    g_delta = gram @ delta
    return np.stack([
        (first.conj() * g_first).sum(axis=0).real,
        2 * (first.conj() * g_delta).sum(axis=0).real,
        (delta.conj() * g_delta).sum(axis=0).real
    ], axis=1)


def extrema(numerator, denominator):
    a, b, c = numerator
    d, e, f = denominator
    poly = np.polynomial.polynomial.polyval
    candidates = [0., 1.]
    if f > 0:
        candidates.append(np.clip(-e / (2 * f), 0, 1))
    assert min(poly(t, denominator) for t in candidates) > 0
    roots = np.roots([c * e - b * f, 2 * (c * d - a * f), b * d - a * e])
    candidates = [0., 1.] + [z.real for z in roots if abs(z.imag) < 1e-9 and 0 < z.real < 1]
    values = [(poly(t, numerator) / poly(t, denominator), t) for t in candidates]
    return min(values), max(values)


def audit(study, output):
    sys.path.insert(0, str(study.resolve()))
    from model import combined_laws, gram

    output.mkdir(exist_ok=True, parents=True)
    keys, base = combined_laws()
    with np.load(study / 'scalars.npz') as scalar:
        idx = np.searchsorted(scalar['keys'], keys)
        assert np.array_equal(scalar['keys'][idx], keys)
        metric = gram(list(zip(scalar['precision'][idx], scalar['factor'][idx])))
    with np.load(study / 'combined_raw.npz') as raw:
        assert list(raw['keys']) == keys
        samples = raw['amp']
    joint = json.loads((study / 'joint.json').read_bytes())['rows']
    chain = json.loads((study / 'chain.json').read_bytes())
    scenarios = {'primary': base}
    for label in ['alternative_same_N13', 'alternative_same_new_N14']:
        original = chain['law']
        alternate = chain[label]['law']
        delta = [float((Fraction(alternate.get(str(k), 0)) -
                        Fraction(original.get(str(k), 0))) / 2) for k in keys]
        scenarios[label] = base + np.asarray(delta)
    names = ['p < -1', '-1 <= p < -1/4', '-1/4 <= p < 0', '0 < p < 1/4',
             '1/4 <= p < 1', '1 <= p']
    with (output / 'intervalle.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['chain', 'M', 'r', 'observable', 'min_probability',
                         'max_probability', 'width_percentage_points', 'mix_at_min', 'mix_at_max'])
        for label, weights in scenarios.items():
            assert np.all(weights > 0) and np.allclose(weights.sum(axis=1), 1)
            for i, mass in enumerate([0.25, 1., 4.]):
                for j, density in enumerate([0.125, 0.25]):
                    amplitudes = samples[:, -1, i, j].mean(axis=0)
                    bins = coefficients(amplitudes, metric, weights)
                    total = bins.sum(axis=0)
                    marked = np.column_stack([amplitudes[:, :3].sum(axis=1),
                                              amplitudes[:, 3:].sum(axis=1)])
                    signs = coefficients(marked, metric, weights)
                    cases = [(n, v, total) for n, v in zip(names, bins)]
                    cases += [('positive, six outcomes', bins[3:].sum(axis=0), total),
                              ('positive, sign only', signs[1], signs.sum(axis=0))]
                    for name, numerator, denominator in cases:
                        (low, t_low), (high, t_high) = extrema(numerator, denominator)
                        if label == 'primary' and name == 'positive, sign only':
                            ref = joint[f'{mass:g}/{density:g}']['convex_line_signed_record']
                            np.testing.assert_allclose([low, high], [ref['min'], ref['max']],
                                                       rtol=2e-10, atol=1e-13)
                        writer.writerow([label, mass, density, name, low, high,
                                         100 * (high - low), t_low, t_high])
    with (output / 'ueberlapp.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['M', 'r', 'A:B', 'normalized_sign_overlap'])
        for tag, row in joint.items():
            for label in ('1:1', '1:3'):
                data = row[label]['decoherence_matrix_scaled_by_record_trace']
                matrix = np.array(data['re']) + 1j * np.array(data['im'])
                diagonal = matrix[:3, :3].sum().real * matrix[3:, 3:].sum().real
                assert diagonal > 0
                writer.writerow([*tag.split('/'), label, abs(matrix[:3, 3:].sum()) / np.sqrt(diagonal)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    audit(args.study, args.output)
