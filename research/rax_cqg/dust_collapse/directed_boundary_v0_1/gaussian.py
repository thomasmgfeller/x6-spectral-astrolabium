"""Conditional Gaussian projection, not a CST field-action constructor.

The caller supplies a real symmetric action Hessian, real positive packet
widths, positive hbar, and Lebesgue field measures. Full real interior axes
use sequential Abel/Fresnel integration. Singular interiors are rejected.
"""
import numpy as np

def real_symmetric(value, name):
    z = np.asarray(value)
    if z.ndim != 2 or z.shape[0] != z.shape[1] or not np.all(np.isfinite(z)):
        raise ValueError(name + ': expected finite square matrix')
    if np.iscomplexobj(z) and np.any(z.imag != 0):
        raise ValueError(name + ': expected real matrix')
    a = np.asarray(z.real, dtype=float)
    if not np.array_equal(a, a.T):
        raise ValueError(name + ': symmetry required, not silently imposed')
    return a

def positive_sqrt(a):
    vals, vecs = np.linalg.eigh(a)
    if np.any(vals <= 0):
        raise ValueError('Packet widths must be strictly positive')
    return (vecs * np.sqrt(vals)) @ vecs.T

def continuous_sqrt_det(omega, eff):
    """sqrt(det(omega-i eff)) continued from eff=0, never sqrt(det(...))."""
    root = positive_sqrt(omega)
    inv = np.linalg.inv(root)
    eig = np.linalg.eigvalsh(inv @ eff @ inv)
    return np.exp(0.5*np.linalg.slogdet(omega)[1] + 0.5*np.log(1-1j*eig).sum())

def regulated_project(H, omega_in, omega_out, epsilon, hbar=1.0):
    """Full simultaneous Gaussian at epsilon>0, including singular interiors.

    This function does not take or certify epsilon->0. Output values are
    numerical control values, not certified physical amplitudes.
    """
    H = real_symmetric(H, 'H')
    oi = real_symmetric(omega_in, 'omega_in')
    of = real_symmetric(omega_out, 'omega_out')
    positive_sqrt(oi); positive_sqrt(of)
    if not np.isfinite(epsilon) or epsilon <= 0 or not np.isfinite(hbar) or hbar <= 0:
        raise ValueError('Positive epsilon and hbar required')
    ni, nf = len(oi), len(of)
    nb, n = ni+nf, len(H)
    if ni == 0 or nf == 0 or n < nb:
        raise ValueError('Field dimensions do not match')
    D = np.eye(n)*epsilon
    D[:ni, :ni], D[ni:nb, ni:nb] = oi, of
    norm = np.exp(0.25*(np.linalg.slogdet(oi)[1]+np.linalg.slogdet(of)[1])-nb/4*np.log(np.pi*hbar))
    Q = D-1j*H
    b00 = norm*(2*np.pi*hbar)**(n/2)/continuous_sqrt_det(D, H)
    return {'scope':'REGULATED_GAUSSIAN_CONTROL_ONLY', 'B00':b00, 'Q':Q, 'covariance_over_hbar':np.linalg.inv(Q)}

def project(H, omega_in, omega_out, hbar=1.0, v_in=None, v_out=None):
    H = real_symmetric(H, 'H')
    oi = real_symmetric(omega_in, 'omega_in')
    of = real_symmetric(omega_out, 'omega_out')
    if not np.isfinite(hbar) or hbar <= 0:
        raise ValueError('hbar must be positive and finite')
    ri, rf = positive_sqrt(oi), positive_sqrt(of)
    ni, nf = len(oi), len(of)
    nb = ni+nf
    if ni == 0 or nf == 0 or len(H) < nb:
        raise ValueError('Nonempty input/output fields and matching H required')
    # H variable order = input fields, output fields, interior fields.
    A = H[nb:, nb:]
    J = H[nb:, :nb]
    B = H[:nb, :nb]
    if len(A):
        eig = np.linalg.eigvalsh(A)
        threshold = 1e-12*max(1.0, np.linalg.norm(A, 2))
        if np.min(np.abs(eig)) <= threshold:
            raise ValueError('Singular or numerically unresolved interior: explicit treatment required')
        E = B - J.T @ np.linalg.solve(A, J)
        sig = int(np.sign(eig).sum())
        inner = np.exp(0.5*len(A)*np.log(2*np.pi*hbar)-0.5*np.log(np.abs(eig)).sum()+1j*np.pi*sig/4)
    else:
        E, sig, inner = B.copy(), 0, 1+0j
    omega = np.zeros((nb, nb))
    omega[:ni, :ni], omega[ni:, ni:] = oi, of
    norm = np.exp(0.25*(np.linalg.slogdet(oi)[1]+np.linalg.slogdet(of)[1])-nb/4*np.log(np.pi*hbar))
    b00 = inner*norm*(2*np.pi*hbar)**(nb/2)/continuous_sqrt_det(omega, E)
    C = np.linalg.inv(omega-1j*E)
    vi = np.eye(ni)[0] if v_in is None else np.asarray(v_in, dtype=float)
    vf = np.eye(nf)[0] if v_out is None else np.asarray(v_out, dtype=float)
    if vi.shape != (ni,) or vf.shape != (nf,) or not np.isclose(vi@vi, 1, rtol=0, atol=1e-12) or not np.isclose(vf@vf, 1, rtol=0, atol=1e-12):
        raise ValueError('Mode vectors must be real unit vectors of matching dimension')
    ai, af = np.r_[ri@vi, np.zeros(nf)], np.r_[np.zeros(ni), rf@vf]
    return {
        'scope': 'CONDITIONAL_GAUSSIAN_PROJECTION_ONLY',
        'E': E, 'interior_signature': sig, 'B00': b00,
        'B10': 0j, 'B01': 0j,
        'B11': 2*(af@C@ai)*b00,
        'B20': (2*(af@C@af)-1)*b00/np.sqrt(2),
    }
