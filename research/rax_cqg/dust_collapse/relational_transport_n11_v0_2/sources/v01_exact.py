"""Exact moments and endpoint exclusion. SymPy is used only for polynomial arithmetic."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import sympy as sp


ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("archived_action", ROOT/"sources"/"ward_clock.py")
ward = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ward)
INNER = tuple(ward.INNER)
MASKS = list(product((False, True), repeat=3))


def ideal(mask, relation):
    past = {j for j, included in zip(INNER, mask) if included}
    return all(i in past for i, j in relation if j in past and i in INNER)


def interior_ideal(mask, relation):
    """Largest down-set inside the raw interior sublevel (relations are transitive)."""
    past = {j for j, included in zip(INNER, mask) if included}
    return tuple(j in past and all(i in past for i,k in relation if k==j and i in INNER) for j in INNER)


def exact_phase_variance(preparation):
    # Delta is the positive fourth root of 3/722. beta/2=1/(19 Delta^2).
    d = sp.Symbol("d", positive=True)
    d_minpoly = d**4-sp.Rational(3,722)
    def reduce(expr):
        return sp.rem(sp.expand(expr), d_minpoly, d)
    inv_d_squared = 722*d**2/3
    u = sp.symbols("u:4")  # three independent inner uniform coordinates, one per-lobe coordinate
    sign = sp.Symbol("sign")
    marks = sp.symbols("r:3")
    symbols = (*u,sign,*marks)
    times = [(j-5)*d for j in range(11)]
    times[3] = -2*d
    if preparation != "sharp":
        times[3] += u[3]/32
    if preparation == "split":
        times[3] += sign/16
    for k,j in enumerate(INNER):
        times[j] = 3*u[k]/2
    rel, _ = ward.coeffs(ward.ORDERS["two_cover_deleted"])
    phase = 0
    for j in (*INNER,*ward.FUTURE):
        density = marks[j-4] if j in INNER else sp.Rational(1,8)
        local = sum(v*(times[j]-times[i])**2 for (i,k),v in rel.items() if k==j and v)
        phase += density*(1 + inv_d_squared*local/19)/2
    poly = sp.Poly(phase,*symbols)
    def mean_power(powers):
        # Uniforms on [-1,1], one fair sign, and three half-atom / half-uniform marks.
        if any(power % 2 for power in powers[:5]):
            return 0
        factor = sp.prod(sp.Rational(1,k+1) for k in powers[:4])
        return factor*sp.prod(sp.Rational(1,2*(k+1)) for k in powers[5:] if k)
    moments = []
    for polynomial in (poly, poly*poly):
        moments.append(reduce(sum(coeff*mean_power(powers) for powers,coeff in polynomial.terms())))
    variance = reduce(moments[1]-moments[0]**2)
    # Exact rational interval evaluation on 0.25 < Delta < 0.26.
    low,high = sp.Rational(1,4),sp.Rational(13,50)
    assert low**4 < sp.Rational(3,722) < high**4
    def enclose(poly):
        terms = [(c*low**n,c*high**n) for (n,),c in sp.Poly(poly,d).terms()]
        return sum(min(t) for t in terms),sum(max(t) for t in terms)
    bounds = enclose(variance)
    assert 0 < bounds[0] <= bounds[1] < sp.Rational(1,5)
    return {"mean":str(moments[0]),"variance":str(variance),
            "variance_exact_enclosure":list(map(str,bounds))}


def compute():
    outputs = {}
    readout = json.loads((ROOT/"sources"/"readout.json").read_text())
    floor = F(readout["one_unknown_pulse"]["uniform_branch_floor_enclosure"][0])
    assert floor > F(49,100)
    for s in (F(0),F(1,4)):
        p = (s+F(3,2))/3
        row = {}
        for tag, removed in ward.ORDERS.items():
            relation, _ = ward.coeffs(removed)
            valid = F(0)
            for mask in MASKS:
                delayed = interior_ideal(mask,relation)
                assert ideal(delayed,relation)
                for subset in MASKS:
                    if all(not v or m for v,m in zip(subset,mask)) and ideal(subset,relation):
                        assert all(not v or m for v,m in zip(subset,delayed))
                if ideal(mask,relation):
                    valid += p**sum(mask)*(1-p)**(3-sum(mask))
            invalid = (2 if tag=="chain" else 1)*p*(1-p)
            assert valid+invalid == 1
            row[tag] = {"invalid_volume":str(invalid),"valid_volume":str(valid)}
        valid = F(row["two_cover_deleted"]["valid_volume"])
        direct_raw_lower = F(81,400)
        cut_raw_upper = valid**2/4
        gap = floor*(direct_raw_lower-cut_raw_upper)
        assert gap > F(29,1000)
        row["one_pair"] = {"direct_raw_lower":str(direct_raw_lower),
                           "causal_raw_upper":str(cut_raw_upper),
                           "detected_probability_gap_lower":str(gap)}
        outputs[str(s)] = row
    return {"variance_C1":{k:exact_phase_variance(k) for k in ("sharp","narrow","split")},
            "exact_cuts":outputs}


if __name__ == "__main__":
    print(json.dumps(compute(),indent=2))
