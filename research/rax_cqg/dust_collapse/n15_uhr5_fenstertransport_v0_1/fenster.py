"""Zertifizierte Fensteranteile, offene Uhrkette und starre Translationssymmetrien."""
import argparse
import json
import sys
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "quellen"
sys.path.insert(0, str(SRC))
from intervalle import I, cis
from modell import clocks, coefficients, EDGES, INNER, INNER_MEANS, ORDER
from randquelle import RADIUS

K = F(15,4)
D = K*I.of(F(3,722)).sqrt().sqrt()
SPACING = 1/(36*D*K**2)
HALF = F(1,16384)
FIRST, LAST = -7, 8


def interval(a,b):
    return I(I.of(a).lo,I.of(b).hi)


def pi_bound():
    def atan_inverse(k):
        terms = [F((-1)**i, (2*i+1)*k**(2*i+1)) for i in range(31)]
        return interval(sum(terms[:-1]),sum(terms))
    return 16*atan_inverse(5)-4*atan_inverse(239)


def check_sources():
    sources = json.loads((SRC/"herkunft.json").read_text())
    for name,record in sources["files"].items():
        data = (SRC/name).read_bytes()
        assert sha256(data).hexdigest()==record["sha256"]
        assert sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==record["git_blob"]
    for name,digest in sources["vorversuch"]["sha256"].items():
        assert sha256((SRC/name).read_bytes()).hexdigest()==digest
    assert sha256((SRC/"nullausgang.json").read_bytes()).hexdigest()==sources["nullausgang"]["sha256"]
    for plan in ("pruefplan","ausgangsplan","kontrollplan","eindeutigkeitsplan"):
        digest = sha256((ROOT/(plan+".txt")).read_bytes()).hexdigest()
        assert digest==(ROOT/(plan+".sha256")).read_text().split()[0]
    registry = json.loads((SRC/"p3.json").read_text())
    count = Counter(row["execution"] for row in registry if row["checkpoint_id"]=="P3")
    assert count=={"NOT_RUN":60} and len(registry)==60
    return sources["commit"],dict(count)


def rank(rows):
    a = [list(map(F,row)) for row in rows]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        p = a[r][col]
        a[r] = [v/p for v in a[r]]
        for i in range(r+1,len(a)):
            if a[i][col]:
                k = a[i][col]
                a[i] = [u-k*v for u,v in zip(a[i],a[r])]
        r += 1
    return r


def current():
    # Coefficient of each independent Y_i w_j in the linear variation.
    def rows(names):
        return [[b*(int(j==k)-int(i==k)) for k in names] for (i,j),b in EDGES.items()]
    all_rank, inner_rank = rank(rows(ORDER)),rank(rows(INNER))
    assert all_rank==14 and inner_rank==7 and all(sum(r)==0 for r in rows(ORDER))
    y = clocks(F(1,4), INNER_MEANS)
    def translated(a):
        return {j:y[j]+(K*a if j==5 else 0) for j in ORDER}
    deriv = EDGES[5,11]*K**2*F(1,4)/19
    for a in (F(1,256),F(-1,777)):
        c1,c2 = coefficients(translated(a)),coefficients(translated(-a))
        assert (c1[11]-c2[11])/(2*a)==deriv
    assert coefficients({j:v+F(7,100) for j,v in y.items()})==coefficients(y)
    return {"active_pairs":len(EDGES),"full_rank":all_rank,"pinned_exterior_rank":inner_rank,
            "local_derivative_c11_at_centre":str(deriv)}


def width_threshold(target):
    # d(e) = 1/(36 Delta (4-e)^3) increases monotonically.
    def below(e):
        return (36*target*(4-e)**3)**4*F(3,722)>1
    a,b=F(-1,2),F(1,2)
    assert below(a) and not below(b)
    for _ in range(88):
        mid=(a+b)/2
        if below(mid):
            a=mid
        else:
            b=mid
    return interval(a,b)


def run():
    commit,counts = check_sources()
    old = json.loads((SRC/"exakt.json").read_text())
    pi = pi_bound()
    margin = RADIUS-F(15,2)*SPACING-HALF
    outside = F(17,2)*SPACING-HALF-RADIUS
    assert margin.lo>0 and outside.lo>0
    assert SPACING.lo>I.of(2*HALF).hi
    # Equal norms and orthogonal columns of the cropped sign multiplier.
    for m in (0,1):
        offsets = [k-m for k in range(FIRST,LAST+1) if (k-m)%2]
        assert sorted(offsets)==[-7,-5,-3,-1,1,3,5,7]
    twopi = 2/pi
    c = 2*twopi**2*sum(F(1,j*j) for j in (1,3,5,7))
    ell = (1-c)/2
    central = (1+twopi**2)/2
    inside = 1-ell
    others = inside-central
    assert (1-central).lo>=I.of(F(old["projected_out_of_two_packets"][0])).lo
    assert (1-central).hi<=I.of(F(old["projected_out_of_two_packets"][1])).hi
    best_error = (1-c.sqrt())**2/4
    assert c.lo>twopi.hi  # Both unambiguous conclusive effects are positive.
    # Spectral decomposition of the open path, using the two central sites.
    contrast = I.of(0)
    for k in range(1,9):
        contrast += F(4,17)*cis(8*k*pi/17).im*cis(9*k*pi/17).im
    assert contrast.lo > 0 and contrast.hi < twopi.lo
    previous_success = interval(*map(F,old["tag_certificate"]["success_equal_priors"]))
    success = F(1,2)+(previous_success-F(1,2))*contrast/twopi
    values = {"initial_packets":central,"other_fourteen_in_window":others,"outside_window":ell,
              "accepted_in_window":inside, "window_margin_inner":margin,"distance_next_packet":outside,
              "overlap_opposite_records":ell/2,"repeat_error_given_window":ell/(2*inside),
              "optimal_error_given_window":best_error/inside,"optimal_correct_given_window":1-best_error/inside,
              "optimal_error_per_input":best_error,
              "unambiguous_conclusive_per_input":c,"unambiguous_conclusive_given_window":c/inside,
              "unambiguous_inconclusive_given_window":ell/inside,"open_contrast":contrast,
              "open_four_phase_matrix_element":contrast/2,"open_tag_success_bound":success}
    return {"commit":commit,"P3":counts,"indices":[FIRST,LAST],"translation":current(),
            "all_16_complete_e_thresholds":{
                "lower":width_threshold((RADIUS+HALF)*F(2,17)).rounded(14),
                "upper":width_threshold((RADIUS-HALF)*F(2,15)).rounded(14)},
            "intervals":{k:v.rounded(14) for k,v in values.items()}}


if __name__=="__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json",action="store_true")
    opts = p.parse_args()
    results = run()
    if opts.json:
        print(json.dumps(results,indent=2))
    else:
        assert results==json.loads((ROOT/"fenster.json").read_text())
        print("PASS · Fensteranteile, beste zweite Auslese, endliche Messung, Wirkungssymmetrie und P3")
