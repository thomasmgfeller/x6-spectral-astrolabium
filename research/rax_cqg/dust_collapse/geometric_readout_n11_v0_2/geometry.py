"""Exact Gaussian and quotient tests for an N11 boundary record."""
import json
from itertools import combinations
from pathlib import Path
import sympy as s
from sector import analyze, lower_upper_efficiency

HERE = Path(__file__).resolve().parent
SRC = HERE / "sources"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def matrix(raw):
    return s.Matrix(raw).applyfunc(s.sympify)


def simple(m):
    return m.applyfunc(lambda v: s.cancel(s.expand_complex(v)))


def symplectic(n):
    return s.zeros(n).row_join(s.eye(n)).col_join((-s.eye(n)).row_join(s.zeros(n)))


def gauge_check(data):
    # Dimensionless canonical units, q_10=0 section. Overall powers of beta cancel.
    a = matrix(data["constraints"]["A_plus"])
    if a.rows != 1:
        a = a.T
    flow = symplectic(4)*a.T
    emb = matrix(data["common_reduction"]["output_embedding"])
    sec = s.eye(8) - flow*s.eye(8)[3,:]/flow[3]
    lift = sec.extract((0,1,2,4,5,6),range(8))
    assert lift*flow == s.zeros(6,1)
    assert lift*emb == s.eye(6) and lift*symplectic(4)*lift.T == symplectic(3)
    return [[str(x) for x in row] for row in lift.tolist()]


def cov_from_precision(omega):
    r, t = omega.applyfunc(s.re), omega.applyfunc(s.im)
    assert all(r[:n,:n].det()>0 for n in (1,2,3))
    a = r.inv()
    return a.row_join(-a*t).col_join((-t*a).row_join(r+t*a*t))/2


def vacuum_test(omega, covariances, ref, pair):
    """Normalized oscillator annihilates ref and uses only the selected pair."""
    i,j = pair
    omit, = set(range(3))-set(pair)
    w = omega[ref]
    ell = s.zeros(1,3)
    ell[i],ell[j] = w[j,omit],-w[i,omit]
    alpha = simple((-s.I*ell*w).row_join(ell))
    assert alpha[omit] == alpha[omit+3] == 0
    re, im = alpha.applyfunc(s.re), alpha.applyfunc(s.im)
    norm = 2*(re*symplectic(3)*im.T)[0]
    assert norm > 0
    quadratures = re.col_join(im)
    assert 2*quadratures*symplectic(3)*quadratures.T/norm == symplectic(1)
    determinants = []
    for k in range(2):
        v = 2*quadratures*covariances[k]*quadratures.T/norm
        vacuum_det = (v+s.eye(2)/2).det()
        # A second derivation acts on the Gaussian wavefunction in configuration space.
        d = simple(ell*(omega[k]-w))
        inv_r = omega[k].applyfunc(s.re).inv()
        n = simple(d*inv_r*d.H)[0]/(2*norm)
        aa = s.cancel(s.expand_complex(((d*ell.T)[0]-(d*inv_r*d.T)[0]/2)/norm))
        assert s.simplify((1+n)**2 - s.Abs(aa)**2 - vacuum_det)==0
        if k == ref:
            assert v == s.eye(2)/2 and vacuum_det == 1 and n == aa == 0
        else:
            assert vacuum_det > 1 and n > 0
        determinants.append(vacuum_det)
    return {"vacuum_det_on_C0_C1":[str(d) for d in determinants],
            "unnormalized_coefficients_q_then_p":[str(a) for a in alpha],
            "commutator_norm":str(norm)}, determinants[1-ref]


def compute():
    data = read(SRC/"canonical.json")
    gauss = read(SRC/"gaussians.json")
    omega = [matrix(row["Omega_scaled_exact"]) for row in gauss["branches"]]
    cov = [cov_from_precision(w) for w in omega]
    for c in range(2):
        r = matrix(data["common_reduction"]["R"+str(c)])
        assert r*symplectic(3)*r.T == symplectic(3)
        assert cov[c] == r*r.T/2  # normalized centered input has covariance I/2
    result={"quotient_lift":gauge_check(data),"single_mode":{},"two_modes":{}}
    for i in range(3):
        axes=(i,3+i)
        dets=[v.extract(axes,axes).det() for v in cov]
        assert all(d>s.Rational(1,4) for d in dets)
        result["single_mode"][str(7+i)]={"cov_det_exact_C0_C1":list(map(str,dets)),
                                        "nu_C0_C1":[float(s.sqrt(d)) for d in dets]}
    for pair in combinations(range(3),2):
        checks, ds, dets = [],[],[]
        for reject in range(2):
            check, det = vacuum_test(omega,cov,reject,pair)
            checks.append(check)
            dets.append(det)
            ds.append(1-1/s.sqrt(det))  # click on the *opposite* branch
        # P(use the test rejecting 0) gives equal conclusive efficiencies.
        p_reject0 = ds[1]/(ds[0]+ds[1])
        eta = ds[0]*p_reject0
        assert s.simplify(eta-ds[1]*(1-p_reject0))==0
        result["two_modes"][f"{7+pair[0]},{7+pair[1]}"]={
            "tests_rejecting_C0_C1":checks,
            "click_if_test_targets_C0_C1":[float(ds[1]),float(ds[0])],
            "probability_use_test_rejecting_C0":float(p_reject0),
            "balanced_efficiency":float(eta),"efficiency_enclosure":lower_upper_efficiency(dets)}
        if pair==(0,1):
            maps=[matrix(data["common_reduction"]["R"+str(j)]) for j in range(2)]
            region=analyze(checks,maps)
            shifted=[]
            for j in range(2):
                exponent=s.Rational(region["wrong_vacuum_probability_exponents_on_opposite_branch"][j])
                click=1-(1-ds[j])*s.exp(-exponent)
                shifted.append(float((p_reject0 if j==0 else 1-p_reject0)*click))
            region["efficiency_on_displaced_C1_C0"]=shifted
            result["fixed_instrument_input_sector"]=region
    s4 = s.cancel(64*omega[0].applyfunc(s.re).det()*omega[1].applyfunc(s.re).det() /
                  s.Abs((omega[0].conjugate()+omega[1]).det())**2)
    assert 0<s4<1 and str(s4)==read(SRC/"parent_geometry.json")["scalar_gram"]["magnitude_fourth_power_exact"]
    result["full_three_modes"]={"overlap_fourth_power":str(s4),"optimal_balanced_efficiency":float(1-s4**s.Rational(1,4))}
    return result


if __name__=="__main__":
    print(json.dumps(compute(),indent=2))
