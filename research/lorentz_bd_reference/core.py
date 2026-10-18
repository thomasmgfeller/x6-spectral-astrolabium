"""4D Poisson BD reference. Coordinates are used only by the synthetic generator.

The estimator consumes interval counts, scalar values and a known density.
All diamonds have externally fixed proper duration T=1; hence R=q=R*T**2.
"""
from pathlib import Path
import ctypes
import hashlib
import importlib.util
import json
import math
import subprocess
import tempfile
import numpy as np
from scipy.special import comb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

geometry = load('bd_geometry', 'research/lorentz_curvature/geometry.py')
reference = load('bd_c2_exact', 'research/lorentz_de_sitter_c2/exact.py')

def contract():
    return json.loads((HERE/'contract.json').read_text())

def seed(label):
    return int.from_bytes(hashlib.sha256((contract()['seed_namespace']+'/'+label).encode()).digest()[:16], 'big')

def physical_volume(h):
    o = geometry.oracle(h)
    return o['volume']/o['proper_time']**4

def truth(h):
    return geometry.oracle(h)['R_tau_squared']

def sprinkle(rng, rho, h):
    """N~Poisson(rho V), then iid physical-volume positions. No N conditioning.

    Store unscaled conformal positions; physical positions differ by the common
    factor 1/tau(h), which leaves the strict causal order unchanged.
    """
    n = int(rng.poisson(rho*physical_volume(h)))
    if n > contract()['limits']['max_points_per_cloud']:
        raise RuntimeError('Poisson draw exceeds predeclared resource guard; do not resample')
    pieces, accepted, proposed = [], 0, 0
    while accepted < n:
        batch = max(256, 2*(n-accepted))
        x = geometry.flat_points(rng, batch)
        keep = rng.random(batch) < ((1-h/2)/(1-h*x[:, 0]))**4
        take = x[keep][:n-accepted]
        pieces.append(take)
        accepted += len(take)
        proposed += batch
        if proposed > 1000000:
            raise RuntimeError('sampler proposal budget exceeded')
    x = np.concatenate(pieces) if pieces else np.empty((0, 4))
    return np.ascontiguousarray(x[np.argsort(x[:, 0], kind='stable')]), proposed

_lib = None
def compile_kernel():
    global _lib
    if _lib is None:
        digest = hashlib.sha256((HERE/'counts.cpp').read_bytes()).hexdigest()[:16]
        dst = Path(tempfile.gettempdir())/('x6_bd_'+digest+'.so')
        subprocess.run(['g++', '-O3', '-std=c++17', '-shared', '-fPIC', str(HERE/'counts.cpp'), '-o', str(dst)], check=True)
        _lib = ctypes.CDLL(str(dst))
        _lib.future_counts.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_longlong)]
        _lib.future_counts.restype = None

def counts(x):
    compile_kernel()
    x = np.ascontiguousarray(x, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != 4 or not np.isfinite(x).all() or np.any(np.diff(x[:, 0]) < 0):
        raise ValueError('finite time-sorted 4D coordinates required')
    out = np.empty(len(x), dtype=np.int64)
    _lib.future_counts(x.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(x), out.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)))
    return out

def weights(n, epsilon):
    """Sum c_k Binomial(n,k) eps^k (1-eps)^(n-k), c=(1,-9,16,-8).

    This form has a finite eps=1 limit and counts strictly interior elements.
    """
    n = np.asarray(n)
    if not 0 < epsilon <= 1 or np.any(n < 0) or np.any(n != np.floor(n)):
        raise ValueError('integer n>=0 and 0<epsilon<=1 required')
    out = np.zeros(n.shape, dtype=float)
    for k, c in enumerate([1., -9., 16., -8.]):
        mask = n >= k
        out[mask] += c*comb(n[mask], k)*epsilon**k*(1-epsilon)**(n[mask]-k)
    return out

def operator(n, rho, epsilon, phi=1., phi_x=1.):
    if not math.isfinite(rho) or rho <= 0:
        raise ValueError('known finite positive physical density required')
    return 4/math.sqrt(6)*math.sqrt(epsilon*rho)*(-phi_x+epsilon*np.sum(weights(n, epsilon)*phi))

def curvature(n, rho, epsilon):
    return -2*operator(n, rho, epsilon)

_forward = None
def forward_grid():
    global _forward
    if _forward is None:
        a, b = reference.coefficients()
        h = np.linspace(0, .5, 8193)
        z = h*h/4
        p = np.polynomial.polynomial.polyval(z, np.array([float(x) for x in a])) / np.polynomial.polynomial.polyval(z, np.array([float(x) for x in b]))**2
        q = 48*np.arctanh(h/2)**2
        if not np.all(np.diff(p)>0):
            raise AssertionError('C2 forward map is not monotone')
        _forward = p, q
    return _forward

def invert(p):
    grid, q = forward_grid()
    return np.interp(p, grid, q)

def c2_interval(lo, hi):
    grid, _ = forward_grid()
    if lo > grid[-1] or hi < grid[0]:
        return None
    return [float(invert(lo)), float(invert(hi))]
