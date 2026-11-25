"""Outward 256-bit enclosures; all model inputs are rationals or radicals."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'quellen/quellen'))
from intervalle import I, S
from ordnung import ORDER, PAST, INNER, FUTURE, links_to, pairs_from_intervals

K = F(15, 4)
D = I.of(F(3, 722)).sqrt().sqrt()*K
RADIUS = 1/(72*D*K*K) + F(1, 16384)
WINDOW = F(1, 64)
EDGES = pairs_from_intervals()
assert EDGES == {(i,j): b for rank,j in enumerate(ORDER) for i,b in links_to(rank)}

def box(low, high):
    return I(I.of(low).lo, I.of(high).hi)

def rounded(value, digits=12):
    return value.rounded(digits)

def up(value, digits=12):
    return str(F(-(-value*10**digits).__floor__(), 10**digits))

def down(value, digits=12):
    return str(F((value*10**digits).__floor__(), 10**digits))

def half_diameter(value):
    return F(value.hi-value.lo, 2*S)

def phases(pulse, central=False):
    u = {j: I.of(F(k,8)) for k,j in enumerate(INNER,1)}
    if not central:
        for j in INNER:
            if j == 6:
                continue
            r = RADIUS if j == 5 else WINDOW
            u[j] = box(u[j]-r,u[j]+r)
    f = {}
    faces = [I.of(0)]+[(u[i]+u[j])/2 for i,j in zip(INNER,INNER[1:])]+[I.of(1)]
    # Analytic cancellation of the clock of the cell itself for internal cells.
    for k,j in enumerate(INNER):
        if 0 < k < len(INNER)-1:
            f[j] = (u[INNER[k+1]] - u[INNER[k-1]])/2
        else:
            f[j] = faces[k+1]-faces[k]
    y = {j:I.of(j-5) for j in PAST+FUTURE}
    y[3] += F(1,4)
    y.update({j:y[3]+K*t for j,t in u.items()})
    c = {j:I.of(F(-1,2)) for j in ORDER}
    for (i,j), weight in EDGES.items():
        shift = pulse/(8*D.sqrt()) if i==6 and j in (12,13,14) else 0
        c[j] -= (y[j]-y[i]-shift)**2 * F(weight,38)
    # Every class is matched with its translated partner before integration.
    gap = D * f[12]*c[12]/100
    x = {j:f[j]*box(F(99,100),F(101,100)) for j in INNER}
    # Outer box for the union of both fixed early tags (nonempty support only).
    x[11] = box(F(255,2048)-F(1,16384), F(257,2048)+F(1,16384))
    cut = sum(D*x[j]*c[j] for j in INNER[:6])
    # Past collar factor is common and integrated independently at fixed e.
    future = sum(I.of(F(1,8))*c[j] for j in FUTURE)
    closed = cut + D*x[14]*c[14] + future
    return gap, cut, closed, sum(c[j] for j in PAST)

def main():
    out = {}
    for pulse in (-1,0,1):
        gap, cut, closed, past = phases(pulse)
        d, theta, theta_end = map(half_diameter, (gap,cut,closed))
        # cos(t) >= 1 - t^2/2. Phase envelopes cover both bins.
        cut_cos = 1-theta**2/2
        end_cos = 1-theta_end**2/2
        assert cut_cos>0 and end_cos>0 and F(past.absmax(),32*S)<1
        trace_bound = d/cut_cos
        assert trace_bound<1 and gap.hi<0
        corr = F(I.of(1-trace_bound**2).sqrt().lo, S)
        out[str(pulse)] = {
            'paired_fine_phase_gap_rad': rounded(gap),
            'phase_gap_midpoint_clocks_rad': rounded(phases(pulse,central=True)[0]),
            'cut13_phase_half_diameter_upper': up(theta),
            'final_phase_half_diameter_upper': up(theta_end),
            'final_amplitude_lower_relative_to_positive_mass': down(end_cos),
            'cut13_normalized_overlap_lower': down(corr),
            'cut13_trace_distance_upper': up(trace_bound),
            'cut13_equal_prior_success_upper': up((1+trace_bound)/2),
        }
    data = json.loads((ROOT/'quellen/p3.json').read_text())
    assert len(data)==60 and all(r['execution']=='NOT_RUN' and r['checkpoint_id']=='P3' for r in data)
    centre_c = F(-1,2)-sum(F(b,38)*(K*F(ORDER.index(12)-ORDER.index(i),8))**2
                            for (i,j),b in EDGES.items() if j==12)
    return {'pulses':out, 'central_no_pulse_c12':str(centre_c),
            'central_no_pulse_gap_in_units_D':str(centre_c/800),
            'P3_not_run':len(data),'closed_output_span_dimension_nonzero_common_scalar':1}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
