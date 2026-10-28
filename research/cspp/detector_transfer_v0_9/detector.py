"""Certified spacetime-ball integration of an explicitly defined retarded extension.

Every point/box causal decision is exact integer arithmetic. Cells crossing the
detector sphere or a causal cone retain an interval contribution, never a sampled
midpoint with an assumed quadrature error.
"""
import hashlib
import heapq
import json
from fractions import Fraction

import numpy as np
from flint import arb, acb
from support import check


def bits(indices):
    out = 0
    for i in indices:
        out |= 1 << int(i)
    return out


class IntegerGeometry:
    def __init__(self, x, counts):
        ratios = [[float(v).as_integer_ratio() for v in row] for row in x]
        self.exponent = max(128, max(d.bit_length() - 1 for row in ratios for n, d in row))
        self.D = 1 << self.exponent
        self.x = [tuple(n * (self.D // d) for n, d in row) for row in ratios]
        self.successors = [bits(np.flatnonzero(counts[:, j] >= 0)) for j in range(len(x))]
        self.center = (0, 0, 3 * self.D // 2)
        self.radius2 = (self.D // 2) ** 2

    def box(self, time):
        a, b = [Fraction(v) for v in time]
        return ((int(a * self.D), -self.D // 2, -self.D // 2, self.D),
                (int(b * self.D), self.D // 2, self.D // 2, 2 * self.D))

    @staticmethod
    def distance_bounds(point, lo, hi):
        lower = upper = 0
        for v, a, b in zip(point, lo, hi):
            near = a - v if v < a else v - b if v > b else 0
            far = max(abs(a - v), abs(b - v))
            lower += near * near
            upper += far * far
        return lower, upper

    def classify(self, box):
        lo, hi = box
        rmin, rmax = self.distance_bounds(self.center, lo[1:], hi[1:])
        if rmin >= self.radius2:
            return 0, 0, 0  # Outside except possibly a measure-zero tangent set.
        domain = 2 if rmax <= self.radius2 else 1
        definitely = possibly = 0
        for j, y in enumerate(self.x):
            dtmax = hi[0] - y[0]
            if dtmax <= 0:
                continue
            dmin, dmax = self.distance_bounds(y[1:], lo[1:], hi[1:])
            if dtmax * dtmax <= dmin:
                continue
            possibly |= 1 << j
            dtmin = lo[0] - y[0]
            if dtmin > 0 and dtmin * dtmin > dmax:
                definitely |= 1 << j
        return domain, definitely, possibly

    def point_past(self, point):
        q = [Fraction(float(v)) for v in point]
        p = [Fraction(v, self.D) for v in self.x[0]] if self.x else []
        out = 0
        for j, row in enumerate(self.x):
            p = [Fraction(v, self.D) for v in row]
            d = [a - b for a, b in zip(q, p)]
            if d[0] > 0 and d[0] ** 2 > sum(z * z for z in d[1:]):
                out |= 1 << j
        return out

    def partition(self, time, cap):
        """Geometry-only refinement: identical cells at both Arb precisions."""
        leaves = {}
        heap = []
        serial = 0

        def add(box):
            nonlocal serial
            info = self.classify(box)
            vol = 1
            for a, b in zip(*box):
                vol *= b - a
            uncertain = (info[2] ^ info[1]).bit_count()
            score = vol * (uncertain + (len(self.x) if info[0] == 1 else 0))
            idx = serial
            serial += 1
            leaves[idx] = (box, info, vol)
            heapq.heappush(heap, (-score, idx))

        add(self.box(time))
        while len(leaves) < cap:
            score, idx = heapq.heappop(heap)
            if score == 0:
                break
            box, info, vol = leaves.pop(idx)
            lo, hi = box
            axis = max(range(4), key=lambda k: hi[k] - lo[k])
            check((lo[axis] + hi[axis]) % 2 == 0, 'integer bisection remains exact')
            mid = (lo[axis] + hi[axis]) // 2
            left_hi, right_lo = list(hi), list(lo)
            left_hi[axis], right_lo[axis] = mid, mid
            add((lo, tuple(left_hi)))
            add((tuple(right_lo), hi))
        result = [leaves[k] for k in sorted(leaves)]
        payload = [[box, info, vol] for box, info, vol in result]
        identity = hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest()
        return result, identity


class CoefficientRanges:
    def __init__(self, table):
        self.levels = [list(table)]
        width = 1
        while 2 * width <= len(table):
            prev = self.levels[-1]
            self.levels.append([prev[i].union(prev[i + width])
                                for i in range(len(table) - 2 * width + 1)])
            width *= 2

    def get(self, lo, hi):
        check(0 <= lo <= hi < len(self.levels[0]), 'interval-count range')
        k = (hi - lo + 1).bit_length() - 1
        width = 1 << k
        return self.levels[k][lo].union(self.levels[k][hi - width + 1])


def cell_integral(geo, cell, ranges, anchor):
    box, (domain, definitely, possibly), volume = cell
    out = [arb(0) for _ in anchor]
    if domain == 0:
        return out
    for j in range(len(anchor)):
        bit = 1 << j
        w = arb(0)
        if possibly & bit:
            lo = (geo.successors[j] & definitely).bit_count()
            hi = (geo.successors[j] & possibly).bit_count()
            w = ranges.get(lo, hi)
            if not definitely & bit:
                w = w.union(arb(0))
        out[j] = w - anchor[j]
        if domain == 1:
            out[j] = out[j].union(arb(0))
    measure = arb(volume) / arb(geo.D) ** 4
    return [measure * z for z in out]


def integrate(geo, table, time, cap):
    cells, identity = geo.partition(time, cap)
    ranges = CoefficientRanges(table)
    middle = [float((Fraction(time[0]) + Fraction(time[1])) / 2), 0., 0., 1.5]
    past = geo.point_past(middle)
    anchor = [table[(geo.successors[j] & past).bit_count()] if past & (1 << j)
              else arb(0) for j in range(len(geo.x))]
    out = [arb(0) for _ in anchor]
    for cell in cells:
        out = [a + b for a, b in zip(out, cell_integral(geo, cell, ranges, anchor))]
    duration = arb(time[1]) - arb(time[0])
    normalization = arb.pi() / 6 * duration
    out = [c + z / normalization for c, z in zip(anchor, out)]
    boundary_volume = sum(cell[2] for cell in cells if cell[1][0] == 1)
    return out, {
        'partition_sha256': identity, 'leaves': len(cells),
        'inside_cells': sum(cell[1][0] == 2 for cell in cells),
        'sphere_boundary_cells': sum(cell[1][0] == 1 for cell in cells),
        'outside_cells': sum(cell[1][0] == 0 for cell in cells),
        'boundary_cover_volume_over_detector': float((arb(boundary_volume) / arb(geo.D) ** 4 / normalization).upper()),
        'integer_coordinate_exponent': geo.exponent,
        'all_point_box_and_sphere_decisions_exact': True,
    }


def wave_reference(k, time):
    """Exact continuum average of exp(i*k*z-i*sqrt(k^2+1)*(t+1))."""
    k = arb(k)
    omega = (k * k + 1).sqrt()
    lo, hi = arb(time[0]), arb(time[1])
    u = k / 2
    spatial = arb(1) if k.is_zero() else 3 * (u.sin() - u * u.cos()) / u ** 3
    v = omega * (hi - lo) / 2
    temporal = v.sin() / v
    return spatial * temporal * acb(0, 3 * k / 2 - omega * ((hi + lo) / 2 + 1)).exp()


def sample_moments(samples):
    """Enclose finite-sample moments; these are NOT population confidence bounds."""
    n = len(samples)
    check(n >= 2 and all(len(row) == 2 for row in samples), 'paired time windows')
    means = [sum(row[t] for row in samples) / n for t in range(2)]
    covariance = []
    for t in range(2):
        row = []
        for u in range(2):
            value = acb(0)
            for i in range(n):
                for j in range(i):
                    a = samples[i][t] - samples[j][t]
                    b = samples[i][u] - samples[j][u]
                    value += acb(a.real ** 2 + a.imag ** 2) if t == u else a * b.conjugate()
            row.append(value / (n * (n - 1)))
        covariance.append(row)
    return means, covariance
