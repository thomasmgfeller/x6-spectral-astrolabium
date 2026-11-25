"""Closed intervals on a decimal grid, with every endpoint rounded outwards."""
from fractions import Fraction
from math import isqrt

SCALE = 10**14

def ceil_div(n, d):
    return -((-n) // d)


class Box:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        assert lo <= hi
        self.lo, self.hi = lo, hi

    @classmethod
    def exact(cls, q):
        q = Fraction(q) * SCALE
        return cls(q.numerator // q.denominator, ceil_div(q.numerator, q.denominator))

    @classmethod
    def hull(cls, lo, hi):
        return cls(cls.exact(lo).lo, cls.exact(hi).hi)

    def __add__(self, other):
        other = box(other)
        return Box(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Box(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-box(other))

    def __rsub__(self, other):
        return box(other) + (-self)

    def __mul__(self, other):
        other = box(other)
        vals = [a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return Box(min(vals)//SCALE, ceil_div(max(vals), SCALE))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = box(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError
        return self * Box(SCALE**2 // other.hi, ceil_div(SCALE**2, other.lo))

    def square(self):
        l = 0 if self.lo <= 0 <= self.hi else min(self.lo**2,self.hi**2)
        return Box(l // SCALE, ceil_div(max(self.lo**2,self.hi**2),SCALE))

    def sqrt_nonnegative_part(self):
        assert self.hi >= 0
        top = isqrt(self.hi*SCALE)
        return Box(isqrt(max(0,self.lo)*SCALE),top + (top**2 < self.hi*SCALE))

    def intersection(self, other):
        lo, hi = max(self.lo, other.lo), min(self.hi, other.hi)
        return None if lo > hi else Box(lo,hi)


def box(x):
    return x if isinstance(x, Box) else Box.exact(x)
