"""Exakte Wirkungsidentitäten, Träger, Gram-Schranken und Fourier-Kontrollen."""
import argparse
import json
import sys
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "quellen"
sys.path.insert(0, str(SRC))
from intervalle import I, S
from modell import EDGES, ORDER, INNER, INNER_MEANS, coefficients, clocks, dwell

K, E = F(15, 4), F(1, 4)
D = K * I.of(F(3, 722)).sqrt().sqrt()
s = 1 / (72 * D * K**2)
h = F(1, 16384)
x0 = F(1, 8)


def band(lo, hi):
    return I(I.of(lo).lo, I.of(hi).hi)


def verify_inputs():
    m = json.loads((SRC / "herkunft.json").read_text())
    for name, row in m["files"].items():
        data = (SRC / name).read_bytes()
        assert sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == row["git_blob"]
        assert sha256(data).hexdigest() == row["sha256"]
    for name, digest in m["vorversuch"]["dateien"].items():
        assert sha256((SRC / name).read_bytes()).hexdigest() == digest
    assert sha256((ROOT / "pruefplan.txt").read_bytes()).hexdigest() == (ROOT / "pruefplan.sha256").read_text().split()[0]
    registry = json.loads((SRC / "p3.json").read_text())
    counts = Counter(row["execution"] for row in registry if row["checkpoint_id"] == "P3")
    assert len(registry) == 60 and counts == {"NOT_RUN": 60}
    return m["commit"], dict(counts)


def reduced_phase(z, t, shift):
    return (F(225, 608)*shift**2 + F(675, 608)*t**2 + F(1575, 1216)*t
            - F(2475, 608)*z**2 + F(5835, 2432)*z - F(32331, 38912))


def prefix(z, t, shift):
    u = INNER_MEANS.copy()
    u[0] += z
    u[1] += t + shift
    c = coefficients(clocks(E, u))
    f = dwell(u)
    return sum(f[j] * c[j] for j in (4, 5, 6)) + x0 * c[11]


def check_action():
    # Both candidate polynomials have degree <=3 in each variable.
    grid = [F(0), F(-1, 53), F(1, 47), F(2, 31)]
    for z, t, shift in product(grid, repeat=3):
        assert prefix(z, t, shift) - prefix(z, t, -shift) == shift * reduced_phase(z, t, shift)
    later = ORDER[ORDER.index(11)+1:]
    assert [(j, EDGES[5,j]) for j in later if (5,j) in EDGES] == [(12,16),(13,-8)]
    # Compare the suffix phase formula to both original action columns separately.
    checks = 0
    for t, shift, u12, u13 in product(grid, repeat=4):
        u = INNER_MEANS.copy()
        u[4] += u12
        u[5] += u13
        base = F(1,4) + t
        u[1] = base + shift
        a = coefficients(clocks(E, u))
        u[1] = base - shift
        b = coefficients(clocks(E, u))
        for j in later:
            weight = EDGES.get((5,j), 0)
            target = u[INNER.index(j)] if j in INNER else 0
            assert a[j] - b[j] == F(2,19)*K**2*shift*weight*(target-base)
            checks += 1
    return checks


def phase_and_gram():
    # Outcomes fix all later clocks and densities. The packet offset t remains coherent.
    # Conservative intervals include even futures excluded by the selected x11 window.
    t = band(-h, h)
    window = F(1,64)
    u12, u13, u14 = [band(F(j,8)-window, F(j,8)+window) for j in (5,6,7)]
    jitter = band(F(99,100), F(101,100))
    x12 = jitter*(u13-F(1,2))/2
    x13 = jitter*(u14-u12)/2
    centre = F(1,4) + t
    delta = (16*x12*(u12-centre)-8*x13*(u13-centre))/684
    theta = reduced_phase(0, 0, s)/(72*K**2)
    epsilon = F((theta + delta).absmax(), S)
    # On either real rail, changing t perturbs the common suffix phase by <= L |t|.
    excursion = F(3,2500)
    assert s.hi < I.of(excursion).lo
    L = D*K**2/19*(16*x12*(u12-centre+excursion)+8*x13*(u13-centre+excursion))
    arc = F(L.hi, S)*h
    m = 1 - arc**2/2
    assert 0 < m < 1 and epsilon < F(1,1000)
    dark = epsilon**2/(4*m**2)
    cond = (1-dark)/dark
    # On the older, t-dependent calibrated rails use the triangle inequality
    # for the chirped positive arm. Handles every admissible z as well.
    z = band(-window, window)
    theta_family = reduced_phase(z, t, s)/(72*K**2)
    eps_family = F((theta_family+delta).absmax(), S)
    dark_family = eps_family**2 / (2*(m**2+(m-eps_family)**2))
    assert 0 < eps_family < m
    return {
        "dark_fraction_upper_previous_calibrations": I.of(dark_family).rounded(13)[1],
        "condition_lower_previous_calibrations": I.of((1-dark_family)/dark_family).rounded(0)[0],
        "reference_phase_rad": theta.rounded(14),
        "suffix_phase_rad": delta.rounded(14),
        "residual_angle_rad": (delta+theta).rounded(14),
        "packet_half_arc_upper": I.of(arc).rounded(12)[1],
        "dark_fraction_upper": I.of(dark).rounded(13)[1],
        "condition_number_lower_if_full_rank": I.of(cond).rounded(0)[0],
    }


def pi_interval():
    # Machin formula. Alternating consecutive partial sums enclose each arctangent.
    def atan(v):
        terms = [(-1)**k * v**(2*k+1)/(2*k+1) for k in range(31)]
        a, b = sum(terms[:-1]), sum(terms)
        return band(min(a,b), max(a,b))
    return 16*atan(F(1,5))-4*atan(F(1,239))



def tag_bounds(eta):
    # Same z,t and uniform jitter in each mark. Norm weight is independent of x.
    maxshift = F(3,2500)
    fmin, fmax = F(7,64), F(13,64)
    for z, off in product((-F(1,64),F(1,64)),(-maxshift-h,maxshift+h)):
        u = INNER_MEANS.copy()
        u[0] += z
        u[1] += off
        f, y = dwell(u), clocks(E,u)
        assert all(fmin <= f[j] <= fmax for j in (4,5,6))
        assert all(abs(y[j]-y[i]) < 5 for i,j in EDGES if j in (4,5,6))
    assert D.hi < S and s.hi < I.of(maxshift).lo
    cmax = F(1,2)+F(34*25,38)
    sinc_min = 1-(fmax*cmax/100)**2/6
    ratio = (1+maxshift/fmin)**2/sinc_min**3
    vis = 2*ratio/(1+ratio**2)
    z, t = band(-F(1,64),F(1,64)), band(-h,h)
    drift = (reduced_phase(z,t,s)-reduced_phase(0,0,s))/(72*K**2)
    kmin,kmax=(1-4*h)/304,(1+4*h)/304
    angle = F(drift.absmax(),S)+kmax*h
    dx = F(1,2048)
    small = kmin*dx
    gap_lo = eta*vis*(1-angle**2/2)*(small-small**3/6)
    gap_hi = eta*kmax*dx
    assert I.of(F(1,10**6)).hi < gap_lo.lo
    return {"plus_gap": [gap_lo.rounded(14)[0],gap_hi.rounded(14)[1]],
            "success_equal_priors":[((1+gap_lo)/2).rounded(14)[0],((1+gap_hi)/2).rounded(14)[1]]}

def two_ports():
    old = json.loads((SRC / "vorversuch_paarung.json").read_text())
    det = band(*map(F, old["normalized_det"]))
    overlap = (1-det**2).sqrt()
    # Rationalised expression avoids subtractive cancellation.
    p = det**2 / (2*(1+overlap))
    return {"common_success":p.rounded(20), "inverse_success":(1/p).rounded(0),
            "amplitude_condition":((1-p)/p).sqrt().rounded(2)}


def run():
    commit, counts = verify_inputs()
    checks = check_action()
    eta = 2/pi_interval()
    gap = 2*s-2*h
    assert gap.lo > 0
    return {"commit":commit, "P3":counts, "prefix_polynomial_nodes":64,
            "suffix_column_checks":checks, "rail_spacing":(2*s).rounded(12),
            "support_gap":gap.rounded(12), "native_minimax_error":"1/2",
            "gram":phase_and_gram(), "two_ports":two_ports(), "tag_certificate":tag_bounds(eta),
            "fourier_periodic_effect_visibility":eta.rounded(14),
            "projected_out_of_two_packets":((1-eta**2)/2).rounded(14)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        assert result == json.loads((ROOT / "exakt.json").read_text())
        print("PASS · Herkunft, Polynomidentitäten, Trägerschwelle, Randpaarung, Zweikanalfilter und P3")
