"""Frozen phase stencil. Its only input is the 15 complex kernel readings."""
from fractions import Fraction
from itertools import product
import cmath

H = Fraction(1, 8)

def settings():
    h = H
    zero = (0,) * 5
    rows = {'0': (zero, -532 / h**2)}
    for direction, weight in ((0, -19), (1, 285)):
        for sign in (-1, 1):
            shift = list(zero)
            shift[direction] = sign * h
            rows['AB'[direction] + ('+' if sign > 0 else '-')] = (tuple(shift), weight / h**2)
    for pair, weight in [('AB', Fraction(-190, 9)), ('UV', 19)]:
        for p, q in product((-1, 1), repeat=2):
            shift = (p*h, q*h, 0, 0, 0) if pair == 'AB' else (0, 0, p*h, q*h, 0)
            label = pair[0] + ('+' if p > 0 else '-') + pair[1] + ('+' if q > 0 else '-')
            rows[label] = (shift, weight*p*q / (4*h**2))
    for p in (-1, 1):
        rows['C'+('+' if p > 0 else '-')] = ((0, 0, 0, 0, p*h), p / (2*h))
    assert len(rows) == 15 and sum(w for _, w in rows.values()) == 0
    assert sum(abs(w) for _, w in rows.values()) == Fraction(679816, 9)
    return rows

def readout(kernels):
    values = settings()
    assert kernels.keys() == values.keys()
    phases = {key: cmath.phase(z / kernels['0']) for key,z in kernels.items()}
    assert max(map(abs, phases.values())) < 1
    from math import fsum
    return fsum(float(weight)*phases[key] for key,(_, weight) in values.items())
