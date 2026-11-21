"""Exact finite-source round trips, with inputs separated from withheld scores."""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from hashlib import sha256
from pathlib import Path
from random import Random
import json
import sys

from randquelle import PAST, PROFILE, UNIFORM, DEPTH_ROWS, mixed_response, translate, visible_sum
import katalogtest
import zellen

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / 'vorarbeit'))
import gegenprobe as direct
from rueckrechnung import initial_readout


def predict(y, at, known_w, steps):
    # at accepts clock coordinates only; hidden densities are inaccessible here.
    sums = [visible_sum(at,y,h,k) for h,k in steps]
    assert sums[0] == sums[1]
    def seam(j):
        h = Q(1,128)
        plus, minus = (at(direct.perturb(y,(j,),s*h)) for s in (1,-1))
        return (plus-minus)/(2*h), (plus+minus-2*at(y))/h**2
    e5,_ = seam(5)
    e11,h11 = seam(11)
    value, _ = initial_readout(y, known_w, sums[0], e5, e11, curvature11=h11)
    return sums[0], value


def score(y,w,steps):
    at = lambda clocks: direct.action(clocks,w)
    known = {j:w[j] for j in direct.SEAM + direct.F}
    amount, value = predict(y, at, known, steps)
    withheld_charge = -direct.response(y,w,PAST)[0]
    withheld_amount = sum(w[j] for j in direct.I)
    assert amount == withheld_amount and value == withheld_charge
    return amount, value


def covariance_at_center(y,left,right):
    """Unscaled by Delta². The two equal-action histories have equal phase weights."""
    assert direct.action(y,left) == direct.action(y,right)
    def slope(direction,w):
        h = Q(1,8192)
        def one(s):
            return direct.action(translate(y,s*h,direction,0,UNIFORM),w)
        return (one(1)-one(-1))/(2*h)
    covariance = (slope(UNIFORM,left)-slope(UNIFORM,right)) * (slope(PROFILE,left)-slope(PROFILE,right)) / 4
    assert covariance != 0
    return covariance


def amplitude_control(y, left, right, steps):
    """Independent finite source check of Im(A_+ - A_-) at the packet centers."""
    def decimal(q):
        return Decimal(q.numerator)/Decimal(q.denominator)
    def sine(x):
        assert abs(x) < 1
        term = x
        result = term
        for n in range(1,32):
            term *= -x*x / ((2*n)*(2*n+1))
            result += term
        return result
    with localcontext() as ctx:
        ctx.prec = 72
        delta = (Decimal(3)/722).sqrt().sqrt()
        estimates = []
        for h,k in steps:
            difference = Decimal(0)
            for s in (1,-1):
                for t in (1,-1):
                    shifted = translate(y,s*h,UNIFORM,t*k,PROFILE)
                    phases = [delta*decimal(direct.action(shifted,w)) for w in (left,right)]
                    difference += s*t*(sine(phases[0])-sine(phases[1]))
            estimate = difference / decimal(4*h*k)
            assert estimate > Decimal('0.0001')
            estimates.append(format(estimate,'.14f'))
        return estimates


def run():
    contract = BASE/'pruefvertrag.json'
    assert sha256(contract.read_bytes()).hexdigest() == (BASE/'pruefvertrag.sha256').read_text().split()[0]
    plan = json.loads(contract.read_text())
    steps = [tuple(map(Q,pair)) for pair in plan['schrittpaare']]
    tests = plan['proben']
    rng = Random(tests['startwert'])
    pairs = tests['paare_je_bekannter_familie']
    broad = tests['weitere_feldbelegungen']
    checks = 0
    negative = 0
    center = {}
    broad_signs = {'positiv':0, 'negativ':0, 'null':0}
    for name in direct.NAMES:
        for i in range(pairs):
            y,(left,right) = direct.sample(rng,name,center=(i==0))
            results = [score(y,w,steps) for w in (left,right)]
            checks += 2
            assert results[0][1] > 0 > results[1][1]
            if name != 'ohne_gesamtinformation':
                assert results[0][0] == results[1][0]
            if name == 'ohne_gesamtinformation':
                at_pair = [lambda yy, w=w:direct.action(yy,w) for w in (left,right)]
                sham = [mixed_response(at,y,*steps[0],second=UNIFORM) for at in at_pair]
                assert sham[0] == sham[1] and results[0][0] > results[1][0]
                negative += 1
                if i==0:
                    center = {'W_gesamt_und_p_je_zweig':results,
                              'delta_W':results[0][0]-results[1][0],
                              'differenz_der_konstanten_kontrollantwort':sham[0]-sham[1],
                              'endliche_gemischte_Amplitudenantwort_Im_je_Schrittpaar':
                                  amplitude_control(y,left,right,steps),
                              'kovarianz_SaSb_durch_Delta_quadrat_bei_gleichen_zentralgewichten':
                                  covariance_at_center(y,left,right)}
    for _ in range(broad):
        y,(w,_) = direct.sample(rng,'allgemein',broad=True)
        _,value = score(y,w,steps)
        label = 'positiv' if value > 0 else 'negativ' if value < 0 else 'null'
        broad_signs[label] += 1
        checks += 1
    cell = zellen.certificate()
    assert cell['delta_W'][0] < center['delta_W'] < cell['delta_W'][1]
    assert cell['re_minus_i_gemischte_amplitudenantwort_untere_schranke'] > Q(1,10000)
    assert PROFILE == (76,47,24,8)
    return {'typ':375841, 'inzidenzmatrix':DEPTH_ROWS, 'quellprofil':tuple(map(int,PROFILE)),
            'paare_pro_familie':dict.fromkeys(direct.NAMES,pairs),
            'weitere_feldbelegungen':broad,'vorzeichen_der_weiteren_belegungen':broad_signs,
            'exakte_rueckrechnungen':checks,
            'konstante_negativkontrollen':negative,'zusatzpaar_zentrum':center,
            'zellzertifikat':cell,'katalog':katalogtest.audit(),
            'messinstrument_und_physikalische_paarung':'HOLD'}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Ohne -O ausführen, damit alle Prüfungen aktiv sind.')
    print(json.dumps(run(),default=str,indent=2,ensure_ascii=False))
