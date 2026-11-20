"""Necessary first-layer test for a free positive-density stationary point.

In units of Delta the four past clocks are (-5,-4,-3,-2+theta);
the first future clock is 2. The original action gives 19*(1+Gamma_v)
= 19 + sum b_vp*(Y_v-Y_p)**2. This script tests independent variations
of w on the open positive stratum. It does not constrain the quantum sum.
"""
from fractions import Fraction as F

import support


PAST = (0, 1, 2, 3)
KERNEL = (1, -9, 16, -8)
POINTS = (F(-1, 4), F(1, 4))
# Cover both full lobes by outward rational bounds. The third interval
# is contained in the negative lobe; its interior has positive width.
REGIONS = {
    "whole_left_lobe": (F(-3, 8), F(-3, 25)),
    "whole_right_lobe": (F(3, 25), F(3, 8)),
    "negative_subinterval": (F(-17, 64), F(-15, 64)),
}
TILES = 256


def collar_row(d):
    return tuple(KERNEL[j] if j < len(KERNEL) else 0
                 for j in (d + 3 - i for i in PAST))


def minimal_clock(theta):
    return (theta**2 - 4*theta - 2) / (2*(1 + theta))


def coefficients(d, theta):
    """Coefficients in descending powers of z = Y_v - Y_min."""
    a = minimal_clock(theta)
    incoming = tuple(zip(collar_row(d), (-5, -4, -3, -2 + theta)))
    return (d + sum(b for b, _ in incoming),
            2*sum(b*(a - p) for b, p in incoming),
            19 + sum(b*(a - p)**2 for b, p in incoming))


def has_interior_root(quadratic, upper):
    """Exact test in the open interval (0,upper), including double roots."""
    a, b, c = quadratic
    if upper <= 0:
        return False
    if a == 0:
        return (c == 0) if b == 0 else (0 < -c/b < upper)
    values = [c]
    vertex = -b/(2*a)
    if 0 < vertex < upper:
        at_vertex = (a*vertex + b)*vertex + c
        if at_vertex == 0:
            return True
        values.append(at_vertex)
    values.append((a*upper + b)*upper + c)
    return any(x*y < 0 for x, y in zip(values, values[1:]))


def times_interval(k, value):
    return min(k*value[0], k*value[1]), max(k*value[0], k*value[1])


def square_interval(value):
    l, r = value
    return (0 if l <= 0 <= r else min(l*l, r*r), max(l*l, r*r))


def minimal_interval(l, r):
    # Denominator 2(1+theta) is positive across all tested domains.
    sl, sr = square_interval((l, r))
    nl, nr = sl - 4*r - 2, sr - 4*l - 2
    denominators = (2*(1 + l), 2*(1 + r))
    quotients = [n/d for n in (nl, nr) for d in denominators]
    return min(quotients), max(quotients)


def one_sign_on_tile(d, l, r):
    # A*z^2+B*z+C cannot vanish for z>0 when all coefficients have
    # one weak sign and C has its strict sign throughout this theta tile.
    al, ar = minimal_interval(l, r)
    row = collar_row(d)
    past = ((-5, -5), (-4, -4), (-3, -3), (-2 + l, -2 + r))
    bl = br = 0
    cl = cr = 19
    for weight, (pl, pr) in zip(row, past):
        difference = al - pr, ar - pl
        low_b, high_b = times_interval(2*weight, difference)
        low_c, high_c = times_interval(weight, square_interval(difference))
        bl += low_b
        br += high_b
        cl += low_c
        cr += high_c
    a = sum(row) + d
    return (a >= 0 and bl >= 0 and cl > 0) or (a <= 0 and br <= 0 and cr < 0)


def excludes_region(d, domain):
    l, r = domain
    step = (r - l)/TILES
    return all(one_sign_on_tile(d, l + j*step, l + (j + 1)*step)
               for j in range(TILES))


def layer_signature(inner, rel):
    predecessors = {v: {u for u in inner if (u, v) in rel} for v in inner}
    minimal = {v for v in inner if not predecessors[v]}
    layers = {}
    for v in inner:
        p = predecessors[v]
        if not p <= minimal:
            continue
        d = len(p)
        # Cross-check the BD row against the actual 15-event intervals.
        actual = []
        for u in PAST:
            assert (u, v) in rel
            n = sum((u, z) in rel and (z, v) in rel for z in range(15))
            actual.append(KERNEL[n] if n < len(KERNEL) else 0)
        assert tuple(actual) == collar_row(d)
        assert all(not any((u, z) in rel and (z, v) in rel for z in range(15))
                   for u in p)
        if d:
            layers.setdefault(d, v)
    return tuple(sorted(layers)), layers


def lobe_bounds_check():
    # Delta^2=sqrt(6)/38. If t=1/(32*Delta), the lobe limits have
    # magnitudes t and 3t. Fourth powers make all comparisons rational.
    t4 = F(38**2, 6*32**4)
    assert F(3, 25)**4 < t4 < F(1, 8)**4
    assert (3**4)*t4 < F(3, 8)**4
    assert t4 < F(15, 64)**4 < F(17, 64)**4 < (3**4)*t4
    assert t4 < F(1, 4)**4 < (3**4)*t4


def run():
    lobe_bounds_check()
    diagnostics = {}
    exclusions = {}
    for d in range(1, 7):
        points = {}
        excluded = {}
        for theta in POINTS:
            a = minimal_clock(theta)
            assert -2 + theta < a < 2
            q = coefficients(d, theta)
            ok = has_interior_root(q, 2 - a)
            key = "theta=" + str(theta)
            points[key] = {"minimal_clock": str(a),
                           "coefficients_in_z_descending": list(map(str, q)),
                           "root_in_open_interval_0_to_2_minus_minimal_clock": ok}
            excluded[key] = not ok
        regions = {key: excludes_region(d, domain) for key, domain in REGIONS.items()}
        excluded.update(regions)
        exclusions[d] = excluded
        diagnostics[str(d)] = {"past_BD_row": list(collar_row(d)),
                               "point_tests": points,
                               "interval_exclusion_certified": regions}
    groups = {}
    count = {key: 0 for key in exclusions[1]}
    codes = sorted(support.catalogue())
    assert len(codes) == len(set(codes))
    for code in codes:
        inner, rel = support.geometry(code)
        signature, nodes = layer_signature(inner, rel)
        witnesses = groups.setdefault(signature, {"type_codes": [],
                                      "first_type_node_by_degree": {str(d): v for d, v in nodes.items()}})
        witnesses["type_codes"].append(code)
        for key in count:
            if any(exclusions[d][key] for d in signature):
                count[key] += 1
    return {
        "scope": "Independent interior w variations in the open positive stratum; every tested successor and its inner predecessors must have free positive w. Necessary local density equations only. No clock-stationarity, physical norm or quantum constraint inferred.",
        "coordinates": "theta=delta/Delta; a=(theta^2-4theta-2)/(2*(1+theta)) is the unique minimal clock in Delta units; z=Y_successor-a must belong to (0,2-a).",
        "equation": "19*(1+Gamma)=d*z^2+19+sum_i past_BD_row[i]*(z+a-P_i)^2; P=(-5,-4,-3,-2+theta). Each of the d inner predecessors is minimal and a cover.",
        "interval_method": "Exact rational interval arithmetic, equal closed tiles, common sign of the quadratic coefficients in z with strict constant term. False indicates lack of this certificate.",
        "theta_intervals": {k: list(map(str, v)) for k, v in REGIONS.items()},
        "tiles_per_interval": TILES,
        "degree_diagnostics": diagnostics,
        "type_count": len(codes),
        "excluded_type_count": count,
        "groups_by_set_of_first_nonminimal_predecessor_counts": {
            ",".join(map(str, sig)) or "none": data for sig, data in sorted(groups.items())},
    }
