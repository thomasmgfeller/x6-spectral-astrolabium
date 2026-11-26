"""Exact finite scalar-action candidate; not a physical CST kernel.

B includes its diagonal and has row x, column y for y preceding x.
The new scalar field has a volume-weighted action, not a dust-weighted action.
This module never chooses quantum boundary states or an integration measure.
"""
from pathlib import Path
import sys
import sympy as s

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'inputs' / 'directed_boundary'))
from analyze import carrier, g


def _real_finite(z, name):
    z = s.sympify(z)
    if z.is_real is not True or z.is_finite is not True:
        raise ValueError(name + ' must be provably real and finite')
    return z


def validate(B, volumes, mu2):
    B = s.Matrix(B)
    if B.rows == 0 or B.rows != B.cols:
        raise ValueError('B must be nonempty and square')
    for z in B:
        _real_finite(z, 'B entry')
    v = s.Matrix(volumes)
    if v.shape != (B.rows, 1):
        raise ValueError('one positive volume per element is required')
    for z in v:
        if _real_finite(z, 'volume').is_positive is not True:
            raise ValueError('volumes must be strictly positive')
    mu2 = _real_finite(mu2, 'mu squared')
    if mu2.is_nonnegative is not True:
        raise ValueError('mu squared must be nonnegative in this candidate')
    return B, v, mu2


def bd_matrix(code, n, scale=1):
    """Unsmoothed 4D BD row operator. Physical scale a=4/(sqrt(6)*ell**2)."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    if not isinstance(code, int) or code < 0 or code >= 1 << (n*n) or not g.valid(code, n):
        raise ValueError('code must be a strict, transitive order without excess bits')
    scale = _real_finite(scale, 'BD scale')
    if scale.is_positive is not True:
        raise ValueError('BD scale must be positive')
    B = -scale * s.eye(n)
    for y, x, inside in g.intervals(code, n):
        k = inside.bit_count()
        B[x, y] = scale * ((1, -9, 16, -8)[k] if k < 4 else 0)
    return B


def gamma(B, f, h=None):
    """Polarized product identity, independently of the incidence formula."""
    B, f = s.Matrix(B), s.Matrix(f)
    h = f if h is None else s.Matrix(h)
    if B.rows != B.cols or f.shape != (B.rows, 1) or h.shape != f.shape:
        raise ValueError('incompatible field dimensions')
    one = s.ones(B.rows, 1)
    return (B*f.multiply_elementwise(h) - f.multiply_elementwise(B*h)
            - h.multiply_elementwise(B*f)
            + f.multiply_elementwise(h).multiply_elementwise(B*one))/2


def scalar_action(B, phi, volumes, mu2=0):
    B, v, mu2 = validate(B, volumes, mu2)
    phi = s.Matrix(phi)
    if phi.shape != (B.rows, 1):
        raise ValueError('incompatible scalar dimension')
    for z in phi:
        _real_finite(z, 'scalar field')
    return s.expand(-(v.dot(gamma(B, phi)) + mu2*v.dot(phi.multiply_elementwise(phi)))/2)


def dust_action(B, T, w):
    T, w = s.Matrix(T), s.Matrix(w)
    if T.shape != (s.Matrix(B).rows, 1) or w.shape != T.shape:
        raise ValueError('incompatible dust dimensions')
    for z in T:
        _real_finite(z, 'dust potential')
    for z in w:
        if _real_finite(z, 'dust weight').is_nonnegative is not True:
            raise ValueError('dust weights must be nonnegative')
    return s.expand(-w.dot(s.ones(len(T), 1) + gamma(B, T))/2)


def scalar_hessian(B, volumes, mu2=0):
    """Construct the symmetric Hessian from signed pair differences."""
    B, v, mu2 = validate(B, volumes, mu2)
    n = B.rows
    H = -mu2*s.diag(*v)
    for x in range(n):
        for y in range(n):
            if x == y or B[x,y] == 0:
                continue
            d = s.zeros(n, 1)
            d[x], d[y] = 1, -1
            H -= v[x]*B[x,y]*(d*d.T)/2
    return H


def green_data(B, volumes, mu2=0):
    B, v, mu2 = validate(B, volumes, mu2)
    V = s.diag(*v)
    r = B*s.ones(B.rows, 1)
    D = B-s.diag(*r)
    tau = B.T*v-V*r
    H = (V*D+D.T*V)/2-s.diag(*tau)/2-mu2*V
    return {'D':D, 'tau':tau, 'H':H}


def gaussian_order(H):
    """For the inherited five-element carrier: input, output, interior."""
    H = s.Matrix(H)
    if H.shape != (5,5):
        raise ValueError('this adapter applies only to the five-element carrier')
    p = [0,1,3,4,2]
    return H.extract(p,p)
