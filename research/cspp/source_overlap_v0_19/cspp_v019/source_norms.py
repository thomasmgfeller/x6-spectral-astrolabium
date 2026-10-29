"""Exact derivative polynomials and Arb enclosures of the fixed source norms."""
from collections import defaultdict
from functools import lru_cache
from flint import arb, ctx


def clean(p):
    return {k: v for k, v in p.items() if v}


def add(*terms):
    out = defaultdict(int)
    for factor, poly in terms:
        for k, v in poly.items():
            out[k] += factor * v
    return clean(out)


def shift(p, dh=0, du=0):
    return {(n-dh, m+du): c for (n, m), c in p.items()}


def D(p):
    # e^(1/h-1) d/dh [e^(1-1/h) P(h,u)]. Keys denote h^(-n) u^m.
    out = defaultdict(int)
    for (n, m), c in p.items():
        out[n+1, m] -= n*c
        out[n+2, m] += c
    return clean(out)


def du(p):
    return {(n, m-1): m*c for (n, m), c in p.items() if m}


def H(p):
    # H=1-Delta after f=e^(1-1/h+4 i z), h=1-4r^2, u=i z.
    d, d2, pu = D(p), D(D(p)), du(p)
    return add((17, p), (-16, d2), (16, shift(d2, dh=1)),
               (24, d), (16, shift(D(pu), du=1)), (1, du(pu)),
               (64, shift(d, du=1)), (8, pu))


def polynomials(max_j):
    seq = [{(0, 0): 1}]
    for _ in range(max_j):
        seq.append(H(seq[-1]))
    return seq


def square_angular(p):
    # |P(h,i z)|^2, before angular integration; second key is z power / 2.
    out = defaultdict(int)
    for (n, m), c in p.items():
        for (nn, mm), cc in p.items():
            if (m+mm) % 2 == 0:
                sign = 1 if ((m-mm)//2) % 2 == 0 else -1
                out[n+nn, (m+mm)//2] += c*cc*sign
    return clean(out)


@lru_cache(None)
def radial_moment(n, l, bits):
    # Integral |b(r)|^2 h^-n z^(2l) d^3x, b=e^(1-1/h).
    # DLMF 13.4.4: s=1/h-1, a=l+3/2, b=n, z=2.
    a = arb(2*l+3)/2
    return arb.pi()*a.gamma()*arb(2).hypgeom_u(a, n)/(4**(l+1)*(2*l+1))


def norm_squared(p, bits):
    ctx.prec = bits
    return sum((c*radial_moment(n, l, bits)
                for (n, l), c in square_angular(p).items()), arb(0))


def norm_squared_by_parts(p2j, bits):
    # Independent identity <f,H^(2J)f> = ||H^J f||_2^2.
    ctx.prec = bits
    return sum((c*(-1)**(m//2)*radial_moment(n, m//2, bits)
                for (n, m), c in p2j.items() if m % 2 == 0), arb(0))


def source_data(max_j, bits):
    ctx.prec = bits
    polys = polynomials(max_j)
    norms = {j: norm_squared(polys[j], bits) for j in range(max_j+1)}
    for j, n in norms.items():
        if not n > 0:
            raise ArithmeticError(f'Nonpositive or unresolved norm J={j}: {n}')
    Dtilt = {j: (arb.pi()/6).sqrt()*(arb(1)/4).exp()*(arb(5)/4)**j*n.sqrt()
             for j, n in norms.items()}
    M0 = (norms[1]/(8*arb.pi())).sqrt()
    return polys, norms, Dtilt, M0
