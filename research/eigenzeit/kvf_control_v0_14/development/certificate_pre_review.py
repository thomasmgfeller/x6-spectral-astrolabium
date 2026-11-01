"""Directed Decimal enclosures for the positive scalar-field integral.

The midpoint quadrature uses a proved total-variation error bound, not the
error estimate returned by an adaptive floating-point integrator.
"""
from decimal import Decimal as D, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path

PREC = 42
CELLS = 32768


def down(fn):
    with localcontext() as c:
        c.prec = PREC
        c.rounding = ROUND_FLOOR
        return +fn()


def up(fn):
    with localcontext() as c:
        c.prec = PREC
        c.rounding = ROUND_CEILING
        return +fn()


def fraction_bounds(x):
    x = F(x)
    return down(lambda: D(x.numerator)/D(x.denominator)), up(lambda: D(x.numerator)/D(x.denominator))


def exp_bounds(lo, hi):
    # Decimal.exp is correctly rounded; one adjacent number encloses it.
    with localcontext() as c:
        c.prec = PREC
        return lo.exp().next_minus(), hi.exp().next_plus()


@lru_cache(None)
def integral(mu, distance, cells=CELLS):
    mu, distance = F(mu), F(distance)
    if mu < 0 or distance < 0 or cells <= 0:
        raise ValueError('nonnegative parameters and positive cell count required')
    if mu == 0 and distance == 0:
        return D('.5'), D('.5')
    low, high = D(0), D(0)
    for j in range(cells):
        z = F(2*j+1, 2*cells)
        z2 = z*z
        exponent = -mu*mu*z2/(1-z2)-distance*distance*(1-z2)/4
        el, eh = fraction_bounds(exponent)
        gl, gh = exp_bounds(el, eh)
        low = down(lambda: low+gl)
        high = up(lambda: high+gh)
    # g(z) is monotone or has one maximum and lies in [0,1].
    # |integral(g)-midpoint(g)| <= TV(g)/cells.
    # I=integral(g)/2. TV<=1 if mu=0 or distance=0, otherwise TV<=2.
    variation = 1 if mu == 0 or distance == 0 else 2
    radius = up(lambda: D(variation)/D(2*cells))
    return max(D(0), down(lambda: low/D(2*cells)-radius)), up(lambda: high/D(2*cells)+radius)


def rho_bounds(mu, distance):
    nl, nh = integral(F(mu), F(distance))
    dl, dh = integral(F(mu), F(0))
    if dl <= 0:
        raise ValueError('denominator not certified positive')
    return down(lambda: nl/dh), up(lambda: nh/dl)


def atan_fraction(x, tolerance=F(1, 10**48)):
    x = F(x)
    if not 0 <= x < 1:
        raise ValueError('atan series domain')
    total, power, j = F(0), x, 0
    while True:
        term = power/(2*j+1)
        total += term if j % 2 == 0 else -term
        power *= x*x
        nxt = power/(2*j+3)
        if nxt <= tolerance:
            other = total + (-nxt if j % 2 == 0 else nxt)
            return min(total, other), max(total, other)
        j += 1


def pi_bounds():
    a, b = atan_fraction(F(1,5)), atan_fraction(F(1,239))
    return fraction_bounds(16*a[0]-4*b[1])[0], fraction_bounds(16*a[1]-4*b[0])[1]


def asin_bounds(x):
    x = D(x)
    if not 0 <= x < 1:
        raise ValueError('positive arcsine domain')
    xl2, xh2 = down(lambda: x*x), up(lambda: x*x)
    tl = th = sl = sh = x
    for n in range(1000):
        numerator, denominator = (2*n+1)**2, 2*(n+1)*(2*n+3)
        tl = down(lambda: tl*xl2*D(numerator)/D(denominator))
        th = up(lambda: th*xh2*D(numerator)/D(denominator))
        tail = up(lambda: th/(1-xh2))
        if tail < D('1e-37'):
            return sl, up(lambda: sh+tail)
        sl = down(lambda: sl+tl)
        sh = up(lambda: sh+th)
    raise RuntimeError('arcsine series did not converge')


def same_sign_bounds(rho):
    pl, ph = pi_bounds()
    al, _ = asin_bounds(rho[0])
    _, ah = asin_bounds(rho[1])
    return down(lambda: D('.5')+al/ph), up(lambda: D('.5')+ah/pl)


def build():
    wlo, whi = F(49,50), F(51,50)
    rows = []
    for distance in (1,2,3):
        models = []
        for mass in (F(0),F(1,2)):
            # rho decreases separately with nonnegative mu and R.
            rlo = rho_bounds(mass*whi,F(distance)/wlo)[0]
            rhi = rho_bounds(mass*wlo,F(distance)/whi)[1]
            raw = (down(lambda: (rlo-D('.001'))/D('1.052')),
                   up(lambda: (rhi+D('.001'))/D('1.048')))
            p = same_sign_bounds(raw)
            models.append({'mass_times_nominal_width':str(mass),
                           'rho_interval':[str(rlo),str(rhi)],
                           'raw_correlation_interval':list(map(str,raw)),
                           'same_sign_probability_interval':list(map(str,p))})
        rows.append({'distance_over_nominal_width':distance,'models':models})
    # Pick the best of the three prespecified distances using theory only.
    selected = max(rows,key=lambda r:D(r['models'][0]['same_sign_probability_interval'][0])-D(r['models'][1]['same_sign_probability_interval'][1]))
    a = D(selected['models'][0]['same_sign_probability_interval'][0]).quantize(D('.00001'),rounding=ROUND_FLOOR)
    b = D(selected['models'][1]['same_sign_probability_interval'][1]).quantize(D('.00001'),rounding=ROUND_CEILING)
    gap = down(lambda:a-b)
    if gap <= 0:
        raise ValueError('HOLD_IDENTIFIABILITY')
    with localcontext() as c:
        c.prec=PREC
        ln100=D(100).ln().next_plus()
    n = int(up(lambda:2*ln100/gap**2).to_integral_value(rounding=ROUND_CEILING))
    midpoint = (F(a)+F(b))/2
    k = (n*midpoint).numerator//(n*midpoint).denominator
    m0_delta = F(a)-F(k,n)
    m1_delta = F(k+1,n)-F(b)
    h0 = exp_bounds(*fraction_bounds(-2*n*m0_delta*m0_delta))[1]
    h1 = exp_bounds(*fraction_bounds(-2*n*m1_delta*m1_delta))[1]
    assert max(h0,h1) <= D('.01')
    return {'arithmetic':'directed Decimal plus total-variation midpoint enclosure',
            'decimal_precision':PREC,'midpoint_cells':CELLS,
            'width_interval':['0.98','1.02'],
            'noise_variance_ratio_interval':['0.048','0.052'],
            'noise_covariance_ratio_interval':['-0.001','0.001'],
            'settings':rows,
            'decision':{'selected_distance':selected['distance_over_nominal_width'],
                        'p0_lower':str(a),'p1_upper':str(b),'gap':str(gap),
                        'pairs':n,'threshold':k,
                        'rule':'choose M0 if same_sign_count > threshold, else M1; conditional two-model test',
                        'hoeffding_false_M1_upper':str(h0),
                        'hoeffding_false_M0_upper':str(h1)}}


if __name__=='__main__':
    Path('records').mkdir(exist_ok=True)
    result=build()
    Path('records/certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['decision'],indent=2))
