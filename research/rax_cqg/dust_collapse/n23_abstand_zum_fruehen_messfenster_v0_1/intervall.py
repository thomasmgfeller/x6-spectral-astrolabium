"""Closed, outward-rounded intervals on the 2**-64 lattice."""
from fractions import Fraction
from math import isqrt

S = 1 << 64


class Empty(Exception):
    """No real point can satisfy a necessary condition."""


class Singular(Exception):
    """Division is undecided on this box. The covering must subdivide it."""


def ceiling_ratio(num, den):
    return -((-num) // den)


class I:
    __slots__ = ("l", "h")

    def __init__(self, low, high):
        if low > high:
            raise Empty("leerer Schnitt")
        self.l = low
        self.h = high

    def __add__(self, other):
        if isinstance(other, int):
            return I(self.l + other*S, self.h + other*S)
        return I(self.l + other.l, self.h + other.h)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.h, -self.l)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if isinstance(other, int):
            ends = self.l * other, self.h * other
            return I(min(ends), max(ends))
        products = (self.l*other.l, self.h*other.l, self.l*other.h, self.h*other.h)
        return I(min(products)//S, ceiling_ratio(max(products), S))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int):
            other = point(other)
        if other.l <= 0 <= other.h:
            raise Singular("Nenner enthält null")
        return self * I(S*S // other.h, ceiling_ratio(S*S, other.l))

    def sq(self):
        left, right = self.l*self.l, self.h*self.h
        low = 0 if self.l <= 0 <= self.h else min(left, right)//S
        return I(low, ceiling_ratio(max(left, right), S))

    def sqrt(self):
        if self.h < 0:
            raise Empty("negative Diskriminante")
        high = isqrt(self.h * S)
        return I(isqrt(max(0, self.l)*S), high + (high*high != self.h*S))

    def cut(self, other):
        return I(max(self.l, other.l), min(self.h, other.h))

    def halves(self):
        mid = (self.l + self.h)//2
        if not self.l < mid < self.h:
            raise ValueError("Teilungsgrenze")
        return I(self.l, mid), I(mid, self.h)


def box(low, high):
    low, high = Fraction(low)*S, Fraction(high)*S
    return I(low.numerator // low.denominator, ceiling_ratio(high.numerator, high.denominator))


def point(value):
    return box(value, value)


def zero(interval, reason):
    if not interval.l <= 0 <= interval.h:
        raise Empty(reason)


def positive(interval, reason):
    if interval.h <= 0:
        raise Empty(reason)
    return I(max(0, interval.l), interval.h)
