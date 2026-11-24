"""Replikation und Sensitivität des Omega_m0-Priors für Everpresent Lambda."""
import argparse
import csv
import json
import os
from pathlib import Path
import sys

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["PILOT_THREADS"] = "1"

import numpy as np
import scipy
from scipy.special import ndtr, ndtri
from scipy.stats import qmc

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "basis"))
import lauf
import gegenprobe

SEED = 36520261124
REPLICATES = 16
LEVELS = (12, 13, 14)
LO, HI = 0.01, 0.99
ENDPOINT = lauf.basis(0.)
SIGMA = np.linalg.norm(ENDPOINT)
DIRECTION = ENDPOINT / SIGMA
# Orthogonal reflection maps the first coordinate to the endpoint direction.
V = np.eye(1, lauf.MODES)[0] - DIRECTION
ROTATION = np.eye(lauf.MODES) - 2 * np.outer(V, V) / (V @ V)
MASS = ndtr(np.arctanh(1 - LO) / SIGMA) - ndtr(np.arctanh(1 - HI) / SIGMA)
VARIANTS = ('native', 'restricted', 'uniform_weighted', 'uniform_direct')
DATA = ('DESI', 'DESI_Pantheon')

def endpoint_weights(omega):
    inside = (omega >= LO) & (omega <= HI)
    uniform = np.zeros(len(omega))
    m = omega[inside]
    g = np.arctanh(1 - m)
    normal_density = np.exp(-0.5 * (g / SIGMA)**2) / (np.sqrt(2*np.pi) * SIGMA)
    uniform[inside] = m * (2-m) / ((HI-LO) * normal_density)
    return inside / MASS, uniform

def new_coefficients(q, normal, direct):
    latent = normal.copy()
    if direct:
        # Decreasing map keeps rank orientation of native Omega_m0 under common points.
        target_m = HI - (HI-LO)*q[:, 0]
        latent[:, 0] = np.arctanh(1 - target_m) / SIGMA
    coeff = ROTATION @ latent.T
    omega = np.exp(lauf.log_matter_fraction(ENDPOINT @ coeff))
    expected = target_m if direct else 1 - np.tanh(SIGMA*normal[:, 0])
    if not np.allclose(omega, expected, rtol=0, atol=2e-14):
        raise ArithmeticError("Randwert stimmt nicht mit der gezogenen Koordinate überein")
    return coeff, omega

def run(cache, out):
    original = json.loads((ROOT/'basis'/'erstlauf.json').read_text())
    files = lauf.ref.inputs(cache)
    bao, sn = lauf.ref.BAO(files), lauf.ref.Pantheon(files)
    if (len(bao.z), sn.n) != (13, 1590):
        raise ValueError('Unerwartete Beobachtungszahl')
    z = np.r_[bao.z, sn.distance.z]
    curve = lauf.Curve(z)
    logz_b = np.log1p(bao.z)
    design_b = lauf.basis(-logz_b)
    log_ref = lauf.reference(bao, sn, 32)
    old_log_ref = np.array([original['ensemble'][k]['log_Z_ref'] for k in ('BAO','BAO_SN')])
    ref_error = np.max(abs(log_ref-old_log_ref))
    if ref_error >= 1e-8:
        raise ArithmeticError('Referenzintegral weicht ab')
    out.mkdir(exist_ok=True, parents=True)
    controls = []
    records = []
    for j, seed in enumerate(np.random.SeedSequence(SEED).spawn(REPLICATES)):
        u = qmc.Sobol(d=lauf.MODES, scramble=True, bits=52,
                      rng=np.random.default_rng(seed)).random_base2(max(LEVELS))
        if not np.all((u > 0) & (u < 1)):
            raise ArithmeticError('Inverse Normaltransformation an einer Intervallgrenze')
        normal = ndtri(u)
        estimates = np.empty((len(u), len(VARIANTS), len(DATA)))
        weights_check = np.empty((len(u), 2))
        for i in range(0, len(u), lauf.BATCH):
            batch = slice(i, i+lauf.BATCH)
            for direct in (False, True):
                coeff, omega = new_coefficients(u[batch], normal[batch], direct)
                dm = curve.comoving(coeff)
                dh = lauf.inv_e(logz_b, coeff, design_b)
                rows = lauf.evaluate(bao, sn, dm[:len(bao.z)], dh, dm[len(bao.z):], omega)
                lr = np.exp(lauf.log_like(rows) - log_ref)
                if j == 0 and i == 0:
                    for k in (0,127):
                        alt_dm, alt_dh = gegenprobe.distances(z,coeff[:,k])
                        err = max(np.max(abs(dm[:,k]/alt_dm-1)), np.max(abs(dh[:,k]/alt_dh[:len(bao.z)]-1)))
                        controls.append(dict(uniform=direct, index=k, relative_max=float(err)))
                if direct:
                    estimates[batch, 3] = lr
                else:
                    restricted, uniform = endpoint_weights(omega)
                    weights_check[batch] = np.column_stack((restricted, uniform))
                    estimates[batch, 0] = lr
                    estimates[batch, 1] = lr * restricted[:,None]
                    estimates[batch, 2] = lr * uniform[:,None]
        if not np.all(np.isfinite(estimates)):
            raise ArithmeticError('Ungültiges Evidenzintegral')
        for level in LEVELS:
            n = 2**level
            means = estimates[:n].mean(axis=0)
            norm = weights_check[:n].mean(axis=0)
            records.append(dict(replicate=j, n=n, mean_restriction_weight=norm[0],
                                mean_uniform_weight=norm[1],
                                **{f'{v}_{d}':means[a,b] for a,v in enumerate(VARIANTS)
                                   for b,d in enumerate(DATA)}))
        print(f'Netz {j+1}/{REPLICATES} abgeschlossen', flush=True)
    with (out/'netze.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    def stats(x):
        return dict(mean=float(np.mean(x)), se=float(np.std(x,ddof=1)/np.sqrt(len(x))))

    def ratio(a,b):
        # Delta method for ratio of correlated replicate means.
        f = np.mean(a)/np.mean(b)
        se = np.std(a-f*b,ddof=1)/np.sqrt(len(a))/np.mean(b)
        return dict(mean=float(f), se=float(se))

    summary = {}
    for level in LEVELS:
        n = 2**level
        group = [r for r in records if r['n'] == n]
        columns = {k:np.array([r[k] for r in group]) for k in group[0]}
        summary[n] = {v:{d:stats(columns[f'{v}_{d}']) for d in DATA} for v in VARIANTS}
        diagnostics = {}
        for d in DATA:
            direct = columns[f'uniform_direct_{d}']
            weighted = columns[f'uniform_weighted_{d}']
            native = columns[f'native_{d}']
            restricted = columns[f'restricted_{d}']
            diagnostics[d] = dict(direct_minus_reweighted=stats(direct-weighted),
                                  restriction_factor=ratio(restricted,native),
                                  within_interval_factor=ratio(direct,restricted),
                                  uniform_to_native=ratio(direct,native))
        summary[n]['paired'] = diagnostics
        summary[n]['weight_means'] = {k:stats(columns[k]) for k in
                                       ('mean_restriction_weight','mean_uniform_weight')}

    full = summary[2**max(LEVELS)]
    joint = 'DESI_Pantheon'
    native = full['native'][joint]
    uniform = full['uniform_direct'][joint]
    old = original['ensemble']['BAO_SN']
    z_old = abs(old['ratio']-native['mean']) / np.hypot(native['se'],old['MC_se_iid'])
    delta = full['paired'][joint]['direct_minus_reweighted']
    z_methods = abs(delta['mean']) / delta['se']
    gates = dict(reference=bool(ref_error < 1e-8),
                 independent_distance=bool(max(e['relative_max'] for e in controls) < 1e-7),
                 repeat_native=bool(z_old <= 3), methods_uniform=bool(z_methods <= 3),
                 precision_native=bool(native['se']/native['mean'] < .10),
                 precision_uniform=bool(uniform['se']/uniform['mean'] < .10),
                 direction_native=bool(native['mean']+3*native['se'] < 1),
                 direction_uniform=bool(uniform['mean']+3*uniform['se'] < 1))
    result = dict(seed=SEED,replicates=REPLICATES, levels=list(LEVELS),
                  histories_per_direct_variant=REPLICATES * 2**max(LEVELS),
                  observations=dict(DESI=len(bao.z),PantheonPlus=sn.n),
                  versions=dict(numpy=np.__version__,scipy=scipy.__version__),
                  endpoint_sigma=float(SIGMA),native_interval_mass=float(MASS),
                  log_reference=log_ref.tolist(),reference_error=float(ref_error),
                  distances=controls,prior_replication_z=float(z_old),paired_method_z=float(z_methods),
                  gates=gates,levels_results=summary)
    (out/'ergebnis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(gates)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache',type=Path, default=ROOT/'cache')
    p.add_argument('--out',type=Path, default=ROOT/'resultate')
    args = p.parse_args()
    run(args.cache, args.out)
