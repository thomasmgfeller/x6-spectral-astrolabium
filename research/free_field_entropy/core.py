"""Finite Gaussian field correlations and Sorkin entropy; conventions in MODEL.md."""
from dataclasses import dataclass, asdict
import math
import numpy as np
from scipy.linalg import eigh, eig

EPS = np.finfo(float).eps
CHECK_TOL = 1e-9
EIG_TOL = 1e-8


def require(ok, message):
    if not ok:
        raise ValueError(message)


def numerical_zero(values):
    """Floating point rank tolerance, not a physical UV cutoff."""
    return 50 * max(1, len(values)) * EPS * max(1., float(np.max(np.abs(values), initial=0)))


def validate_order(order):
    a = np.asarray(order)
    require(a.ndim == 2 and a.shape[0] == a.shape[1] and len(a) > 0, 'nonempty square order')
    require(np.all((a == 0) | (a == 1)), 'binary order')
    a = a.astype(bool)
    require(not np.any(np.diag(a)) and not np.any(a & a.T), 'strict asymmetric order')
    # Boolean matrix products are slower than BLAS; row containment tests avoid overflow.
    for i in range(len(a)):
        require(not np.any(a[a[i]] & ~a[i]), 'transitive order required')
    return a


def diamond_order(points):
    p = np.asarray(points, dtype=float)
    require(p.ndim == 2 and p.shape[1] == 2 and len(p) > 0 and np.isfinite(p).all(), 'finite null coordinates')
    return np.all(p[:, None, :] < p[None, :, :], axis=2)


def commutator(order):
    c = validate_order(order).astype(float)
    return .5j * (c.T - c)


def positive_part(h):
    h = np.asarray(h, dtype=complex)
    require(h.ndim == 2 and h.shape[0] == h.shape[1] and np.isfinite(h).all(), 'finite square H')
    require(np.linalg.norm(h-h.conj().T) <= CHECK_TOL * max(1., np.linalg.norm(h)), 'Hermitian H')
    values, vectors = eigh(h, check_finite=False)
    keep = values > numerical_zero(values)
    w = (vectors[:, keep] * values[keep]) @ vectors[:, keep].conj().T
    return w


def sj_state(order):
    h = commutator(order)
    return positive_part(h), h


@dataclass
class EntropyResult:
    status: str
    entropy_nats: float | None = None
    retained_rank: int = 0
    numerical_nullity: int = 0
    physical_discarded: int = 0
    numerical_tolerance: float = 0.
    physical_cutoff: float | None = None
    kernel_leakage: float = 0.
    eigen_residual: float | None = None
    pair_residual: float | None = None
    max_imaginary: float | None = None
    snapped_eigenvalues: int = 0

    def record(self):
        return asdict(self)


def entropy(w, h, physical_cutoff=None):
    """Entropy of a real-field Gaussian algebra, with explicit kernel diagnostics.

    Input matrices use a real field basis. A physical cutoff explicitly changes
    the algebra; numerical kernel mismatch otherwise refuses a finite answer.
    The reduced generalized eigenproblem has an indefinite second matrix.
    """
    w, h = np.asarray(w, complex), np.asarray(h, complex)
    require(w.ndim == 2 and w.shape == h.shape and w.shape[0] == w.shape[1], 'matching square W,H')
    require(np.isfinite(w).all() and np.isfinite(h).all(), 'finite W,H')
    n = len(w)
    require(n > 0, 'nonempty algebra')
    scale = max(1., float(np.linalg.norm(w)), float(np.linalg.norm(h)))
    require(np.linalg.norm(w-w.conj().T) <= CHECK_TOL*scale, 'Hermitian W')
    require(np.linalg.norm(h-h.conj().T) <= CHECK_TOL*scale, 'Hermitian H')
    require(np.linalg.norm(h+h.T) <= CHECK_TOL*scale, 'antisymmetric real-field commutator')
    require(np.linalg.norm(w-w.T-h) <= CHECK_TOL*scale, 'CCR W-W.T=H')
    require(eigh(w, eigvals_only=True, check_finite=False)[0] >= -CHECK_TOL*scale, 'positive W')
    d, u = eigh(h, check_finite=False)
    tol = numerical_zero(d)
    null = np.abs(d) <= tol
    leakage = float(np.linalg.norm(w @ u[:, null]) / max(1., np.linalg.norm(w)))
    if physical_cutoff is not None:
        require(math.isfinite(physical_cutoff) and physical_cutoff > tol, 'physical cutoff exceeds numerical tolerance')
    threshold = tol if physical_cutoff is None else physical_cutoff
    keep = np.abs(d) > threshold
    result = EntropyResult('UNSET', retained_rank=int(keep.sum()), numerical_nullity=int(null.sum()),
                           physical_discarded=int((~keep & ~null).sum()), numerical_tolerance=tol,
                           physical_cutoff=physical_cutoff, kernel_leakage=leakage)
    if physical_cutoff is None and leakage > CHECK_TOL:
        result.status = 'KERNEL_MISMATCH'
        return result
    # Real antisymmetric matrices have +/- pairs; cuts must retain both.
    if int(np.count_nonzero(d[keep] > 0)) != int(np.count_nonzero(d[keep] < 0)):
        result.status = 'UNPAIRED_CUTOFF'
        return result
    if not np.any(keep):
        result.status = 'EMPTY_PHYSICAL_ALGEBRA' if physical_cutoff is not None else 'OK'
        result.entropy_nats = None if physical_cutoff is not None else 0.
        return result
    basis = u[:, keep]
    wr = basis.conj().T @ w @ basis
    hr = np.diag(d[keep])
    values, vectors = eig(wr, hr, check_finite=False)
    if not np.isfinite(values).all():
        result.status = 'NONFINITE_EIGENVALUES'
        return result
    residual = np.linalg.norm(wr @ vectors - (hr @ vectors)*values, axis=0)
    denom = (np.linalg.norm(wr) + np.abs(values)*np.linalg.norm(hr))*np.linalg.norm(vectors, axis=0)
    result.eigen_residual = float(np.max(residual/np.maximum(denom, EPS)))
    result.max_imaginary = float(np.max(np.abs(values.imag)))
    v = np.sort(values.real)
    result.pair_residual = float(np.max(np.abs(v + v[::-1] - 1)))
    if (result.eigen_residual > EIG_TOL or result.max_imaginary > EIG_TOL
            or result.pair_residual > EIG_TOL or np.any((v > EIG_TOL) & (v < 1-EIG_TOL))):
        result.status = 'NUMERICAL_FAILURE'
        return result
    near0, near1 = np.abs(v) <= EIG_TOL, np.abs(v-1) <= EIG_TOL
    result.snapped_eigenvalues = int(np.count_nonzero(near0 | near1))
    v[near0], v[near1] = 0., 1.
    nz = v != 0
    s = float(np.sum(v[nz] * np.log(np.abs(v[nz]))))
    if s < -EIG_TOL:
        result.status = 'NEGATIVE_ENTROPY'
        return result
    result.status, result.entropy_nats = 'OK', max(0., s)
    return result


def regional_diagnostics(order, indices, coefficients=(.75, 1., 1.25)):
    """One global eigensolve; construct only the requested regional matrices."""
    h = commutator(order)
    a = np.asarray(indices)
    require(a.ndim == 1 and len(a) > 0 and np.issubdtype(a.dtype, np.integer), 'nonempty integer region')
    require(len(set(a.tolist())) == len(a) and np.all((0 <= a) & (a < len(h))), 'unique valid region')
    d, u = eigh(h, check_finite=False)
    ua = u[a, :]
    tol = numerical_zero(d)
    positive = d > tol
    wa = (ua[:, positive] * d[positive]) @ ua[:, positive].conj().T
    ha = h[np.ix_(a, a)]
    out = {'raw': entropy(wa, ha).record(), 'cutoffs': {}}
    for coefficient in coefficients:
        global_cutoff = coefficient * math.sqrt(len(h)) / (4*math.pi)
        regional_cutoff = coefficient * math.sqrt(len(a)) / (4*math.pi)
        keep = np.abs(d) > global_cutoff
        require(np.count_nonzero(d[keep] > 0) == np.count_nonzero(d[keep] < 0), 'paired global cutoff')
        pos = d > global_cutoff
        wc = (ua[:, pos]*d[pos]) @ ua[:, pos].conj().T
        hc = (ua[:, keep]*d[keep]) @ ua[:, keep].conj().T
        out['cutoffs'][str(float(coefficient))] = {
            'global_cutoff': global_cutoff, 'regional_cutoff': regional_cutoff,
            'global_rank': int(keep.sum()),
            'commutator_relative_change': float(np.linalg.norm(hc-ha)/max(1., np.linalg.norm(ha))),
            'global_only': entropy(wc, hc).record(),
            'double': entropy(wc, hc, regional_cutoff).record()}
    return out
