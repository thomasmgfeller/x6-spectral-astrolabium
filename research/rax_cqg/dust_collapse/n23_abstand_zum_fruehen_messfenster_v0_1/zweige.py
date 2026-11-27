"""Necessary conditions on the two raw clocks a=Y16 and z=Y22."""
from collections import Counter
from intervall import S, I, Empty, Singular, box, ceiling_ratio, point, positive, zero
from reduktion import EPS, ONE, lin, sqsum

ALLOWED_A = box("-1.07", "-0.89")
H_RANGE = box(".45", "1.93")
V = box("-0.000000002", "0.000000002")
WEIGHT = box(0, 16)


def prerequisites(sys):
    todo = [I(sys.y[2].l, sys.y[7].h)]
    allowed = excluded = 0
    while todo:
        a = todo.pop()
        try:
            _, h, _ = sys.first(a)
            inside_a = ALLOWED_A.l <= a.l <= a.h <= ALLOWED_A.h
            inside_h = point(".45").h <= h.l <= h.h <= point("1.93").l
            if inside_a and inside_h:
                allowed += 1
                continue
        except Empty:
            excluded += 1
            continue
        except Singular:
            pass
        if a.h - a.l <= S//10**10:
            raise RuntimeError("Einschluss der Anfangsvariablen unentschieden")
        todo.extend(a.halves())

    assert ALLOWED_A.h < sys.positive_window.l
    assert (sys.y[7]-sys.y[0]).h < 8*S
    assert sys.y[0].h < sys.window.l and sys.window.h < sys.y[7].l
    assert sys.late_at("18", I(sys.y[0].l, sys.y[7].h)).h < 0

    # The two corrected squared gaps can put p slightly above b.
    err = EPS*128/(2*point(".45"))
    assert err.h < point(".00000001").l
    # b <= p+(h+16 eps)^2/(2h). Expand before bounding over h.
    bmax = sys.positive_window+err+point("1.93")/2+16*EPS+(16*EPS).sq()/(2*point(".45"))
    assert bmax.h < point("1.18").l
    force = sys.late_at("18", I(sys.y[0].l, bmax.h))
    assert (-force/(point("1.93")+16*EPS)).l > point(".0052").h
    assert sys.late["twin"][1].l > point("-.005").h
    # w18/(w18+w21+base) <= 1/(1-.005/.0052) = 26.
    assert (26*8*EPS/2).h < V.h
    return dict(feasible_leaves=allowed, rejected_leaves=excluded)


def ratio_positive(numerator, denominator, bounds=WEIGHT):
    n = positive(numerator, "positives Gewicht unmöglich")
    d = positive(denominator, "strikte Zeitordnung")
    low = n.l*S//d.h
    high = bounds.h if d.l == 0 else min(bounds.h, ceiling_ratio(n.h*S, d.l))
    return I(max(low, bounds.l), high)


def test(sys, a, z, require_contact=True):
    u, h, p = sys.first(a)
    h = h.cut(H_RANGE)
    if require_contact:
        p = p.cut(I(a.l, sys.positive_window.h + point(".00000001").h))

    # Terminal D21,G21. Its clock t exceeds both c=Y17 and d=Y20.
    K = -8*sys.y[2]+16*u-9*a+p+z
    B = 19-8*sys.y[2].sq()+16*u.sq()-9*a.sq()+p.sq()+z.sq()
    r = ((K.sq()-B)*3/2-3*V.sq()).sqrt()
    mean = K-r
    t = K-2*r/3
    clock_range = I(sys.y[0].l, sys.y[7].h)
    c = (mean+V).cut(clock_range)
    d = (mean-V).cut(clock_range)
    if sys.family == 18:
        d = d.cut(z)
        c = c.cut(z+2*V)
    positive(t-z, "21 vor Sonde")
    positive(t-p, "21 vor 19")

    # D18 around p. G18 selects the root with negative derivative.
    terms = ((ONE-EPS, c), (1, d), (-EPS, a))
    if sys.family == 18:
        terms += ((1, z),)
    A = sum(k for k, _ in terms)
    B1 = -2*h+2*lin(terms, p)
    C = sqsum(terms, p)
    disc = (B1.sq()-4*A*C).sqrt()
    lower = max(a.l, c.l, d.l, z.l if sys.family == 18 else clock_range.l)
    b = (p+(-B1-disc)/(2*A)).cut(I(lower, point("1.18").h))
    w18 = ratio_positive(-2*sys.late_at("18", b), disc)
    w21 = ratio_positive(-sys.late_at("twin", d)-w18*(b-d), t-d)
    if sys.family == 14:
        y14, w14 = sys.front14(z)
        w21 = ratio_positive(-sys.late_at("twin", z)-w14*(y14-z), t-z, w21)
        zero(sys.late_at("twin", z)+w14*(y14-z)+w21*(t-z), "G22")

    w19 = ratio_positive(-sys.late_at("full", p)-w21*(t-p), h)
    den = lin(sys.early, a)+(ONE-EPS)*(a-u)
    num = sys.late_at("16", a)+(ONE-EPS)*w18*(b-a)+w19*(p-a)-9*w21*(t-a)
    if den.h < 0:
        w16 = ratio_positive(-num, -den)
    elif den.l > 0:
        w16 = ratio_positive(num, den)
    else:
        w16 = WEIGHT  # Enlarge the domain; an uncertain denominator never excludes a root.
    g15 = sys.late_at("15", u)+(ONE-EPS)*w16*(a-u)-9*w18*(b-u)-9*w19*(p-u)+16*w21*(t-u)
    zero(g15, "G15")
    return a, z, p, b, t, w21


def search(sys, maxdepth=44, limit=1000000):
    stats = Counter()
    todo = [(ALLOWED_A, sys.window, 0)]
    deepest = 0
    remaining = []
    while todo:
        a, z, level = todo.pop()
        try:
            test(sys, a, z)
        except Empty as exc:
            stats[str(exc)] += 1
            deepest = max(deepest, level)
            continue
        except Singular:
            pass
        if level >= maxdepth or sum(stats.values()) >= limit:
            remaining.append((a, z))
            remaining.extend((x, y) for x, y, _ in todo)
            break
        if (a.h-a.l)*32 > z.h-z.l:
            todo.extend((half, z, level+1) for half in a.halves())
        else:
            todo.extend((a, half, level+1) for half in z.halves())
    return dict(leaves=sum(stats.values()), depth=deepest, reasons=dict(sorted(stats.items()))), remaining
