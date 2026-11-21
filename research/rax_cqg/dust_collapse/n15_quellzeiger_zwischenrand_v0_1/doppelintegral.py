"""Supplement: sample independent bra/ket fields and a shared future directly."""
import json
import numpy as np
from scipy.stats import qmc

from gegenrechnung import (DELTA, F, I, P, RADIUS, clocks_and_dwell,
                            global_rows, packet_centres)
from nachweis import FUTURE_WIDTH, MASS, ROOT, cut_orders


def bare_arms(points, z, paths, matrix):
    y, duration, dwell = clocks_and_dwell(points[:, :8], paths)
    y[:, F[1:]] = [3, 4, 5]+float(FUTURE_WIDTH)*z[:, :3]
    w = np.zeros_like(y)
    w[:, P] = (1/8+points[:, 8]/32)[:, None]
    w[:, F] = 1/8+float(FUTURE_WIDTH)*z[:, 3:]
    c = global_rows(y, matrix)
    jac = (duration/(4.25*DELTA))**14
    values = []
    for centres in packet_centres(c, dwell):
        w[:, I] = float(MASS)*duration[:, None]*(centres+RADIUS*points[:, 9:])
        dust = -0.5*np.sum(w*c, axis=1)
        charge = np.zeros(len(points))
        for i in P:
            for j in I:
                if matrix[i, j]:
                    charge += w[:, j]*matrix[i, j]*(y[:, i]-y[:, j])/(19*DELTA)
        a = jac*np.exp(1j*dust)
        b = a*np.exp(1j*charge)
        values.append([a, b, (a-1j*b)/2, (a+1j*b)/2])
    return np.transpose(values, (2, 0, 1))


def run():
    paths, coeff, _, _ = cut_orders()
    matrix = np.zeros((15, 15), dtype=int)
    for edge, value in coeff.items():
        matrix[edge] = value
    reference = np.asarray(json.loads((ROOT/'quadratur.json').read_text())[-1]['direkt'])
    reference = reference[..., 0]+1j*reference[..., 1]
    results = []
    for seed in [17371, 30781]:
        dimensions = 16+16+7
        # Scrambled Sobol integrates the product measure in disjoint dimensions.
        # Process batches to keep peak memory bounded.
        sampler = qmc.Sobol(dimensions, scramble=True, seed=seed)
        total = np.zeros((3, 2, 2), dtype=complex)
        samples = 2**16
        batch = 1024
        for _ in range(samples//batch):
            s = 2*sampler.random(batch)-1
            left = bare_arms(s[:, :16], s[:, 32:], paths, matrix)
            right = bare_arms(s[:, 16:32], s[:, 32:], paths, matrix)
            products = [left[:, :, j].conj().T@right[:, :, j] for j in range(4)]
            total += [(products[0]+products[1])/2, products[2], products[3]]
        values = total/samples
        # No imposed Hermitian symmetrization. Empirical cross-check only.
        error = float(np.max(abs(values-reference)))
        assert error < 1e-5
        results.append({'seed':seed, 'raumdimension':dimensions, 'punkte':samples,
                        'absolute_maximaldifferenz_gegen_analytische_dichteintegration':error})
    return results


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Python ohne -O verwenden.')
    print(json.dumps(run(), indent=2))
