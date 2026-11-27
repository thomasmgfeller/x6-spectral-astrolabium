"""Sehnenmessung einer sphärischen Materialfläche an einer festen Uhrzeit."""
from fractions import Fraction as F


def square_interval(lo, hi):
    return (0 if lo <= 0 <= hi else min(lo**2, hi**2), max(lo**2, hi**2))


def radius_squared(probe, start, reach, steps):
    """probe(position) liefert nur die Seite. Suchgrenzen und Orte in derselben Längeneinheit."""
    if reach <= 0 or not isinstance(steps, int) or steps < 0:
        raise ValueError("Positive Suchgrenze und nichtnegative ganze Schrittzahl erforderlich")
    if not probe(start):
        return "START_AUSSEN", None
    centers, half_lengths = [], []
    for axis in range(3):
        intervals = {}
        for sign in (-1, 1):
            def point(distance):
                coords = list(start)
                coords[axis] += sign * distance
                return tuple(coords)
            lo, hi = F(0), F(reach)
            if probe(point(hi)):
                return "AUSSENSEITE_FEHLT", None
            for _ in range(steps):
                mid = (lo + hi) / 2
                if probe(point(mid)):
                    lo = mid
                else:
                    hi = mid
            intervals[sign] = lo, hi
        nlow, nhigh = intervals[-1]
        plow, phigh = intervals[1]
        centers.append(((plow-nhigh)/2, (phigh-nlow)/2))
        half_lengths.append(((nlow+plow)/2, (nhigh+phigh)/2))
    estimates = []
    for axis in range(3):
        losq, hisq = square_interval(*half_lengths[axis])
        for j in range(3):
            if j != axis:
                low, high = square_interval(*centers[j])
                losq += low
                hisq += high
        estimates.append((losq, hisq))
    lo = max(x[0] for x in estimates)
    hi = min(x[1] for x in estimates)
    if lo > hi:
        return "INKONSISTENTE_SEHNEN", None
    return "INTERVALL", (lo, hi)
