"""Frozen one-parameter linear planning, not a calibrated curvature interval."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import numpy as np
from scipy.stats import norm, t

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
P = np.array([1/10, 1/350, 1/29400])
B = np.array([1/90, 1/42, 1/27])
METHODS = ('C2', 'GLS23', 'GLS234')


def dependency(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT/relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


geometry = dependency('information_geometry', 'research/lorentz_curvature/geometry.py')
chains = dependency('information_chains', 'research/lorentz_rss_fixed_n/core.py')
quadrature = dependency('information_quadrature', 'research/lorentz_rss_fixed_n/quadrature.py')


def contract():
    return json.loads((HERE/'contract.json').read_text())


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(ref):
    out = {}
    for path in contract()['frozen_paths']:
        raw = (ROOT/path).read_bytes()
        historic = subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)
        if raw != historic:
            raise ValueError('source differs from public freeze: '+path)
        out[path] = hashlib.sha256(raw).hexdigest()
    for path, expected in contract()['pilot_sha256'].items():
        if digest(ROOT/path) != expected:
            raise ValueError('published pilot mismatch: '+path)
    return out


def seed(label):
    raw = (contract()['seed_namespace']+'/'+label).encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:16], 'big')


def features(counts, n):
    return np.asarray(counts)/np.array([math.comb(n, k) for k in (2, 3, 4)])/P-1


def gls(cov, size):
    cov = np.asarray(cov, dtype=float)
    if cov.shape != (3, 3) or size not in (1, 2, 3) or not np.all(np.isfinite(cov)):
        raise ValueError('finite 3x3 covariance and size 1..3 required')
    sub = cov[:size, :size]
    if not np.allclose(sub, sub.T, atol=1e-14) or np.linalg.eigvalsh(sub).min() <= 0:
        raise ValueError('positive definite covariance required')
    v = np.linalg.solve(sub, B[:size])
    w = np.zeros(3)
    w[:size] = v/(B[:size]@v)
    return w


def budget(variance, radius):
    if not np.isfinite(variance) or variance < 0 or not np.isfinite(radius) or radius <= 0:
        raise ValueError('nonnegative finite variance and positive radius required')
    return max(1, math.ceil(norm.ppf(.975)**2*variance/radius**2))


def plan():
    pilot = ROOT/'research/lorentz_rss_fixed_n/results'
    raw = np.load(pilot/'raw.npz', allow_pickle=False)['direct_counts']
    refs = json.loads((pilot/'reference.json').read_text())['geometry']
    weights, rows = {}, []
    for i, (n, h, geo) in enumerate(refs):
        if h == 0:
            cov = np.cov(features(raw[i], n), rowvar=False, ddof=1)
            weights[str(n)] = {name: gls(cov, j+1).tolist() for j, name in enumerate(METHODS)}
    for i, (n, h, geo) in enumerate(refs):
        y = features(raw[i], n)
        cov = np.cov(y, rowvar=False, ddof=1)
        q = geo['R_tau_squared']
        for name in METHODS:
            w = np.array(weights[str(n)][name])
            var = float(w@cov@w)
            rows.append(dict(n=n, h=h, q=q, method=name, sd=var**.5,
                pilot_bias=float(y.mean(axis=0)@w-q),
                budget_absolute={str(d): budget(var, d) for d in (.25, .5, 1.)},
                budget_relative_20pct=budget(var, .2*q) if q else None))
    eligible = [r for r in rows if r['n'] == 128 and r['h'] == .5]
    gate = min(r['budget_relative_20pct'] for r in eligible) <= contract()['maximum_planned_clouds']
    return dict(status='DESCRIPTIVE_PUBLISHED_PILOT_REANALYSIS', weights=weights,
                rows=rows, fresh_run_budget_gate=gate,
                budget_scope='Pointwise normal approximation, noise only; no coverage or bias guarantee')


def relation_hash(c):
    return hashlib.sha256(np.packbits(c.reshape(-1), bitorder='little').tobytes()).hexdigest()


def count_check(c):
    """Independent middle-vertex/middle-edge decomposition of C2, C3, C4."""
    a = c.astype(np.int64)
    incoming, outgoing = a.sum(axis=0), a.sum(axis=1)
    return np.array([a.sum(), incoming@outgoing, incoming@a@outgoing], dtype=np.int64)


def summarize(counts, planning):
    rows, estimates = [], {}
    m = contract()['fresh_clouds_per_cell']
    # Twelve cell/method mean-bias intervals, 95% familywise Student approximation.
    critical = t.ppf(1-.05/(2*12), m-1)
    for j, h in enumerate(contract()['h_grid']):
        q = geometry.oracle(h)['R_tau_squared']
        y = features(counts[j], 128)
        estimates[h] = {}
        pair = quadrature.pair_probability(h, 32)
        for name in METHODS:
            estimate = y@np.array(planning['weights']['128'][name])
            estimates[h][name] = estimate
            error = estimate-q
            sd, bias = float(estimate.std(ddof=1)), float(error.mean())
            half = float(critical*sd/math.sqrt(m))
            rows.append(dict(n=128, h=h, q=q, method=name, clouds=m,
                bias=bias, sd=sd, rmse=float(np.sqrt(np.mean(error**2))),
                mean_bias_simultaneous_approx95=[bias-half, bias+half],
                budget_relative_20pct=budget(sd**2, .2*q) if q else None,
                c2_quadrature_bias=90*(pair/P[0]-1)-q if name == 'C2' else None))
    q = geometry.oracle(.5)['R_tau_squared']
    e2 = (estimates[.5]['C2']-q)**2
    eg = (estimates[.5]['GLS234']-q)**2
    rng = np.random.Generator(np.random.PCG64(seed('paired-bootstrap-primary')))
    boot = []
    for _ in range(contract()['bootstrap_replicates']):
        idx = rng.integers(0, m, size=m)
        boot.append(float(np.sqrt(eg[idx].mean()/e2[idx].mean())))
    interval = np.quantile(boot, [.025, .975]).tolist()
    passed = interval[1] <= contract()['primary_rmse_ratio_upper_threshold']
    return dict(rows=rows, primary=dict(h=.5, n=128, contrast='GLS234 / C2',
        rmse_ratio=float(np.sqrt(eg.mean()/e2.mean())),
        paired_percentile_bootstrap_approx95=interval,
        status='TEN_PERCENT_RMSE_GAIN_SUPPORTED' if passed else 'TEN_PERCENT_RMSE_GAIN_NOT_ESTABLISHED'),
        curvature_interval_status='NOT_QUALIFIED',
        limitation='Internal fresh-seed validation; approximate bootstrap; no external replication')
