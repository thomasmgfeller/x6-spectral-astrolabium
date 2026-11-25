"""Certified paired-history comparisons on the N15 positive witness cells."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'quellen'))
from zertifikat import (I, S, D, K, EDGES, ORDER, INNER, FUTURE, PAST, ETA,
                        W0, profile, box, support)
from intervalle import C, cis, sinc
from ordnung import source_parts

RADIUS = F(1, 2**22)
NOISE = F(1, 2**20)
EPS = F(1, 2**14)
HIDDEN = (12, 13, 14)
Q0 = F(-5, 4)
V5 = dict(zip(PAST, (F(1,4), F(1,8), 0, 0)))
H = F(1, 8)
STEP = H / D.sqrt()
LAYER = (1, -9, 16, -8)


def decimals(z, digits=13):
    scale = 10**digits
    lo, hi = z.lo * scale // S, -(-z.hi * scale // S)
    def fmt(n):
        a, b = divmod(abs(n), scale)
        return ('-' if n < 0 else '') + f'{a}.{b:0{digits}d}'
    return [fmt(lo), fmt(hi)]


def clocks(arm, exact=False):
    u = {j:F(k,8) for k,j in enumerate(INNER, 1)}
    u[5] += F(arm, 1000)
    if not exact:
        u = {j:(I.of(t) if j == 6 else box(t-RADIUS, t+RADIUS)) for j,t in u.items()}
    return u


def box_data(arm):
    u = clocks(arm)
    y,c,d = profile(u)
    for j in PAST + FUTURE:
        y[j] = I.of(y[j])
    for j in FUTURE[1:]:
        y[j] += box(-ETA, ETA)
    faces = [I.of(0)] + [(u[i]+u[j])/2 for i,j in zip(INNER, INNER[1:])] + [I.of(1)]
    f = {j:faces[k+1]-faces[k] for k,j in enumerate(INNER)}
    x = {j:(I.of(F(255,2048)) if j==11 else f[j]) + box(-NOISE, NOISE) for j in INNER}
    return y,c,d,f,x


def coeffs(y):
    out = {j:I.of(F(-1,2)) for j in ORDER}
    for (i,j),b in EDGES.items():
        out[j] -= F(b,38)*(y[j]-y[i])**2
    return out


def input_response(y):
    # Stable exact difference of quadratics. Source changes the action only.
    shift = {i:(1+V5[i])*STEP for i in PAST}
    dc = {j:I.of(0) for j in ORDER}
    for (i,j),b in EDGES.items():
        step = shift.get(j,0)-shift.get(i,0)
        dc[j] -= F(b,38)*step*(2*(y[j]-y[i])+step)
    return dc


def integrated_arms(arm, rho):
    y,_,d,_,x = box_data(arm)
    c = coeffs(y)
    dc = input_response(y)
    weights = {j:D*x[j] for j in INNER}
    weights.update({j:box(W0-ETA, W0+ETA) for j in FUTURE})
    phase0 = sum(weights[j]*c[j] for j in weights)
    change = sum(weights[j]*dc[j] for j in weights)
    # The unperturbed odd part is exactly zero by the old witness identities.
    odd = EPS*D*sum(d[j]*dc[j] for j in d)
    def inlet(past):
        # Analytic integral over the common original physical inlet density.
        return cis(rho*past).scale(sinc(past/32))
    old = inlet(sum(c[j] for j in PAST))*cis(phase0)
    src = inlet(sum(c[j]+dc[j] for j in PAST))*cis(phase0+change)
    low = src*cis(-odd)
    high = src*cis(odd)
    # High - low, evaluated before integration to retain correlated errors.
    delta = src*C(0,2*odd*sinc(odd))
    return (old, low, high, delta), odd*2


def probabilities(rho):
    ar, gap1 = integrated_arms(-1, rho)
    br, gap2 = integrated_arms(1, rho)
    # The two clock lobes have equal flat volume, phase and incoming weight.
    a,low,high,db = [(left+right).scale(F(1,2)) for left,right in zip(ar,br)]
    # Each product is taken at common future z. The intervals thus enclose
    # the integral against any common normalized positive diagonal z weight.
    def norm2(z):
        return (z.conj()*z).re
    n_low, n_high = norm2(a)+norm2(low), norm2(a)+norm2(high)
    assert n_low.lo > 0 and n_high.lo > 0
    j_low = (a.conj()*low).im
    j_diff = (a.conj()*db).im
    n_diff = ((high+low).conj()*db).re
    pdiff = (j_diff - j_low/n_low*n_diff)/n_high
    assert pdiff.lo>0
    return {'fine_phase_high_minus_low_per_lobe':[decimals(gap1),decimals(gap2)],
            'plus_probability_high_minus_low':decimals(pdiff),
            'relative_norm_low':decimals(n_low),'relative_norm_high':decimals(n_high)}


def global_phase_witness(arm):
    y,c,d,f,x = box_data(arm)
    q = sum(c[j]*d[j] for j in HIDDEN)
    shape = {j:(Q0/q)*d[j] for j in HIDDEN}
    min_margin = I.of(1).lo
    min_class = I.of(1).lo
    for s in (-1,1):
        for j in INNER:
            packet = x[j] + s*EPS*shape.get(j,0)
            min_margin = min(min_margin,(packet-F(99,100)*f[j]).lo,
                             (F(101,100)*f[j]-packet).lo)
            if j==12:
                min_class = min(min_class,(s*(packet-W0)).lo,(s*(packet-f[j])).lo)
    assert min_margin>0 and min_class>0 and q.hi<0
    dose = 2*EPS*sum(shape.values())
    assert dose.lo>0
    # Derivative-free determinant on the hidden triple, with rows total,
    # first pulse moment and centered second (clock-weighted) moment.
    a,b,e = (y[j] for j in HIDDEN)
    determinant = -216*(b-a) - 200*(e-b)
    # Independent expansion: det [[1,1,1],[-9,16,-8],[-9a,16b,-8e]].
    det2 = (16*(-8*e)+8*(16*b)) - ((-9)*(-8*e)-(-8)*(-9*a)) + ((-9)*(16*b)-16*(-9*a))
    assert determinant.hi<0 and det2.hi<0
    # Sum of the seven midpoint-defined widths is one. The PR368 fixed tag
    # replaces f11 and all seven independent jitters still enter that sum.
    visible,hidden = source_parts(EDGES)
    assert all(visible[j]+hidden[j]==int(j in INNER) for j in ORDER)
    base = 1+F(255,2048)-f[11]+box(-7*NOISE,7*NOISE)
    mid = F(2047,2048)
    total_low, total_high = base-dose/2, base+dose/2
    lower_margin = min((mid-total_low).lo,(total_high-mid).lo)
    assert lower_margin > I.of(F(18,100000)).hi
    return {'sum_low':decimals(total_low),'sum_high':decimals(total_high),
            'two_sided_sum_margin_lower':decimals(I(lower_margin,lower_margin))[0],
            'q':decimals(q),'relative_density_sum_high_minus_low':decimals(dose),
            'constant_phase_high_minus_low':decimals(2*D*EPS*Q0),
            'band_margin_lower':decimals(I(min_margin,min_margin))[0],
            'class_margin_lower':decimals(I(min_class,min_class))[0],
            'hidden_moment_determinant':decimals(determinant,7)}


def growth():
    src=ROOT/'quellen/uhr'
    edges=json.loads((src/'gewichte.json').read_text())['laws']
    chain=json.loads((src/'kette.json').read_text())
    laws={'Basis':chain['law'],'N13':chain['alternative_same_N13']['law'],
          'N14':chain['alternative_same_new_N14']['law']}
    rows={}
    for e,ep in edges.items():
        for k,cp in laws.items():
            assert sum(map(F,ep.values()))==sum(map(F,cp.values()))==1
            assert '2097151' not in ep
            coeff=F(cp['2097151'])/2
            assert coeff>0
            rows[e+' / '+k]=str(coeff)
    assert len(rows)==6
    return rows


def distinct_calculation():
    # Enumerate original intervals from the full relation, also for all N16
    # ideals. Use exact rational fields and direct actions for both witnesses.
    directed=set(combinations(ORDER,2))
    def full(relation,nodes,y,w,pulse):
        action=-sum(w.values())/2
        for i,j in relation:
            count=sum((i,k) in relation and (k,j) in relation for k in nodes)
            if count<4:
                h=pulse if i==6 and j in HIDDEN else 0
                action-=F(LAYER[count],38)*w[j]*(y[j]-y[i]-h)**2
        return action
    counts={'reference':0,'global_phase':0}
    for arm in (-1,1):
        for off in (-1,0,1):
            u={j:(v if j==6 else v+off*RADIUS*F(1+j%4,5)) for j,v in clocks(arm, True).items()}
            yy,c,d=profile(u)
            q=sum(c[j]*d[j] for j in HIDDEN)
            shapes={'reference':d,'global_phase':{j:Q0*d[j]/q for j in HIDDEN}}
            for k in range(16):
                y=dict(yy)
                shifts={i:F((i+1)*(k-7),117) for i in PAST}
                rel=directed|{(j,15) for j in ORDER[:k]}
                y[15]=F(11,3)
                for j in FUTURE[1:]:
                    y[j]+=off*ETA*F(1,2)
                for key,shape in shapes.items():
                    sy={j:t+(shifts.get(j,0) if key=='global_phase' else 0) for j,t in y.items()}
                    w={j:F(1,8)+F(j+1,2**20) for j in y}
                    for s in (F(0),F(-1,8),F(1,8)):
                        # By linearity only the difference matters. D is common
                        # and scaled out of the rational check.
                        lo={j:z-EPS*shape.get(j,0) for j,z in w.items()}
                        hi={j:z+EPS*shape.get(j,0) for j,z in w.items()}
                        diff=full(rel,tuple(y),sy,hi,s)-full(rel,tuple(y),sy,lo,s)
                        assert diff==(0 if key=='reference' else 2*EPS*Q0)
                        counts[key]+=1
            # Independently compare source increment, using a rational h
            # instead of the radical for this full-action equality check.
            val=F(3,25)
            y1={j:z+(val*(1+V5[j]) if j in PAST else 0) for j,z in yy.items()}
            dw={j:d.get(j,F(0)) for j in ORDER}
            direct=full(directed,ORDER,y1,dw,0)-full(directed,ORDER,yy,dw,0)
            pred=sum(F(b,38)*dw[j]*val*(1+V5[i])*(2*(yy[j]-yy[i])-val*(1+V5[i]))
                     for (i,j),b in EDGES.items() if i in PAST and j in INNER)
            assert direct==pred
    return counts


def run():
    support()
    return {'law_coefficients':growth(),
            'source':{str(r):probabilities(r) for r in (F(1,8),F(1,4))},
            'second_pair':{str(a):global_phase_witness(a) for a in (-1,1)},
            'direct_N16_action_comparisons':distinct_calculation()}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
