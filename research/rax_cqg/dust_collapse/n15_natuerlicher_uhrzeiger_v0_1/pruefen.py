"""Exact identities, shared-support supremum and full-action controls. Python 3.10+."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import product
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'quellen'
sys.path.insert(0, str(SRC))
from modell import clocks, dwell, INNER_MEANS
from ordnung import ORDER, INNER, PAST, FUTURE, links_to, pairs_from_intervals
from intervalle import I

DELTA = I.of(F(3, 722)).sqrt().sqrt()
ETA, E = F(1, 100), F(1, 4)
R0, DR = F(1, 8), F(1, 1024)
X0, DX, HALF = F(1, 8), F(1, 2048), F(1, 16384)
MU = F(15, 64)
COUPLING = F(9, 304)
EDGES = pairs_from_intervals()


def check(value, label):
    if not value:
        raise ValueError(label)


def source():
    meta = json.loads((SRC/'herkunft.json').read_text())
    for name, r in meta['files'].items():
        data = (SRC/name).read_bytes()
        gid = sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        check(gid == r['git_blob'] and sha256(data).hexdigest() == r['sha256'], name)
    for plan in ROOT.glob('*plan.txt'):
        check(sha256(plan.read_bytes()).hexdigest() == plan.with_suffix('.sha256').read_text().split()[0], plan.name)
    p3 = json.loads((SRC/'p3.json').read_text())
    states = Counter(r['execution'] for r in p3 if r['checkpoint_id'] == 'P3')
    check(len(p3) == 60 and states == {'NOT_RUN': 60}, 'P3')
    return meta['commit'], dict(states)


def u_for(r):
    u = INNER_MEANS.copy()
    u[INNER.index(5)] = MU + r/8
    u[INNER.index(6)] = MU + 9*r/8
    return u


def coords():
    memory = {}
    for cut in (6, 11, 12, 13, 14):
        stop = ORDER.index(cut)+1
        memory[str(cut)] = list(ORDER[stop-4:stop])
    check(set(memory['6']) & set(memory['11']) & set(memory['12']) & set(INNER) == {5, 6}, 'Speicherwahl')
    check(EDGES[5, 11] == -9 and EDGES[6, 11] == 1, 'Eingangskoeffizienten')
    cases = 0
    for y5, y6, y11 in product((F(-3, 4), F(1, 8), F(7, 9)), repeat=3):
        m, g = (9*y5-y6)/8, y6-y5
        check((m+g/8, m+9*g/8) == (y5, y6), 'Inverse')
        direct = -9*(y11-y5)**2+(y11-y6)**2
        check(direct == -8*(y11-m)**2+F(9, 8)*g*g, 'Exakte quadratische Identität')
        cases += 1
    return {'memory': memory, 'algebra_cases': cases, 'coefficient_of_minus_w_gap_squared': COUPLING}


def shared_capacity():
    # At fixed centre mu, u5 and u6 advance by s/8 and 9s/8 for s=r_high-r_low.
    ulo5, uhi5, ulo6, uhi6, uhi12 = [F(j, 64) for j in (15, 17, 23, 25, 41)]
    slope = 9*(1+ETA)/(16*ETA)
    crossing = (uhi12-uhi6)/(slope-F(9, 8))
    smax = (uhi12-ulo6)/slope
    check(0 < crossing < smax < 8*(uhi5-ulo5), 'Stückgrenzen')
    def piece(intercept, decay, s):
        return 2*(intercept-ulo5)*s + (1-2*decay)*s*s
    def deriv(intercept, decay, s):
        return 2*(intercept-ulo5)+2*(1-2*decay)*s
    check(deriv(uhi6, F(9, 8), crossing)>0 and deriv(uhi12, slope, crossing)<0, 'Scharfes Maximum')
    width = piece(uhi6, F(9, 8), crossing)
    check(width == piece(uhi12, slope, crossing), 'Aktive Schranken')
    a, b = ulo5, uhi6-9*crossing/8
    low_f, high_f = (uhi12-b-9*crossing/8)/2, (uhi12-b)/2
    x = (1+ETA)*low_f
    check(x == (1-ETA)*high_f and b+9*crossing/8 == uhi6, 'Zulässiger Randzeuge')
    check((b-a+crossing)**2-(b-a)**2 == width and ulo6 <= b and a+crossing/8 <= uhi5, 'Erreichbarkeit')
    kmax = 4+F(3, 32)/DELTA
    qmax = COUPLING*DELTA*kmax**3*width
    ratio = qmax*304
    check(ratio.hi < I.of(F(27, 100)).lo, 'Vergleich mit Vorstudie')
    return {'gap_step_at_max': crossing, 'largest_feasible_gap_step': smax,
            'max_width_r_squared': width, 'witness_u5_u6_u12_x': [a,b,uhi12,x],
            'max_phase_per_x': qmax.rounded(13), 'relative_to_1_over_304': ratio.rounded(12)}


def full_action(y, densities, cut, pulse=F(0)):
    # Compute S / D at unit-scaled densities, with the actual 6-pulse expressed in Y units.
    ends = set(ORDER[:ORDER.index(cut)+1])
    value = -sum(densities[j] for j in ends)/2
    for (i,j), b in EDGES.items():
        if j in ends:
            shift = pulse if i==6 and ORDER.index(j)>ORDER.index(11) else 0
            value -= F(b,38)*densities[j]*(y[j]-y[i]-shift)**2
    return value


def witness():
    collars = {j: F(1, 4) if j in PAST else F(1,8) if j in FUTURE else F(0) for j in ORDER}
    common = dict.fromkeys(ORDER, F(0))
    common.update(dwell(INNER_MEANS))
    def mixed(stop, pulse, radial=DR, density=DX):
        value=collar_mixed=F(0)
        for arm, mark in product((-1,1), repeat=2):
            u = u_for(R0+arm*radial)
            f = dwell(u)
            check(all(abs(z-m)<F(1,64) for z,m in zip(u,INNER_MEANS)), 'Uhrfenster')
            x = dict(common)
            x[11] = X0+mark*density
            for j in INNER:
                margin = HALF if j==11 else 0
                check((1-ETA)*f[j] < x[j]-margin <= x[j]+margin < (1+ETA)*f[j], 'Gemeinsames Dichteinnere')
            y = clocks(E, u)
            value += arm*mark*full_action(y, x, stop, pulse)
            collar_mixed += arm*mark*full_action(y, collars, stop, pulse)
        check(collar_mixed == 0, "Physische Kragendichten heben sich im Mischterm auf")
        return value
    delta_r_sq = (R0+DR)**2-(R0-DR)**2
    relative = -COUPLING*(4-E)**2*delta_r_sq*2*DX
    checks = 0
    for cut in (6,11,12,13,14,10):
        for pulse in (F(-1, 5), F(0), F(1, 5)):
            check(mixed(cut, pulse) == (0 if cut==6 else relative), 'Volle Vierpunktdifferenz')
            checks += 1
    check(mixed(10,0,radial=0) == mixed(10,0,density=0) == 0, 'Nullkontrollen')
    duration = (4-E)*DELTA
    return {'x_low_high': [X0-DX,X0+DX], 'r_low_high': [R0-DR,R0+DR],
            'common_band_halfwidth': HALF, 'full_action_checks':checks,
            'mixed_phase_over_D':relative, 'mixed_phase_radians':(duration*relative).rounded(15),
            'positive_phase_spacing_per_x':(duration*(-relative)/(2*DX)).rounded(13)}


def run():
    commit,p3=source()
    return {'commit':commit,'natural_pair':coords(),'support':shared_capacity(),'witness':witness(),'P3':p3}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--json',action='store_true')
    args=p.parse_args()
    actual=json.dumps(run(),default=str,ensure_ascii=False,indent=2)+'\n'
    if args.json:
        print(actual,end='')
    else:
        check(actual==(ROOT/'exakt.json').read_text(),'Archivierte Ergebnisse')
        print('PASS · Quellen, Uhrpaar, exaktes Supremum, vier Historien und P3-Status')
