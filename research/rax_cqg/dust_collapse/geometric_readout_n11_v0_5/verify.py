"""Exact N11 checks for a fixed geometric readout under unknown neutral pulses."""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import mpmath as mp
import sympy as sp

BASE = Path(__file__).resolve().parent
SRC = BASE / "sources"
Q = sp.Rational
TRANSVERSE = [1, 2, 4, 5]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def symplectic(n):
    return sp.zeros(n).row_join(sp.eye(n)).col_join((-sp.eye(n)).row_join(sp.zeros(n)))


def rows(matrix):
    return [[str(x) for x in row] for row in matrix.tolist()]


def archive():
    for name, ref in load(BASE / "provenance.json")["files"].items():
        assert hashlib.sha256((SRC / name).read_bytes()).hexdigest() == ref["sha256"]
    with tempfile.TemporaryDirectory() as temp:
        script = Path(temp) / "canonical_check.py"
        shutil.copyfile(SRC / script.name, script)
        subprocess.run([sys.executable, "-B", str(script)], check=True, stdout=subprocess.DEVNULL)
        data = load(script.with_name("results.json"))
    assert data == load(SRC / "canonical.json")
    return data


def fibres(canonical):
    old = load(SRC / "charge_reference.json")
    contract = load(SRC / "collar_contract.json")
    uniform = sp.ones(4, 1).col_join(sp.zeros(4, 1))
    J = symplectic(3)
    red = canonical["common_reduction"]
    charges = []
    for key in ("input_embedding", "output_embedding"):
        charges.append(uniform.T * symplectic(4) * sp.Matrix(red[key]))
    qin, qout = charges
    assert [rows(q)[0] for q in charges] == old["charge_in_out"]
    bare = sp.Matrix(contract["past_coordinate_sources"]).row_join(sp.zeros(2, 4))
    assert bare*uniform == bare*symplectic(4)*sp.Matrix(canonical["constraints"]["A_minus"]).T == sp.zeros(2,1)
    past = bare * sp.Matrix(red["input_embedding"])
    assert past * J * qin.T == sp.zeros(2,1)
    assert rows(past)[1] == load(SRC/"collar_results.json")["fixed_detector_neutral_pulse"]["pulse_reduced_covector"]
    ident = sp.eye(6)
    a, b = qout[:, :3], qout[:, 3:]
    chart = qout
    for i in (1, 2):
        chart = chart.col_join(ident[i, :] - b[i]/b[0]*ident[0, :])
    chart = chart.col_join(-ident[0, :]/b[0])
    for i in (1, 2):
        chart = chart.col_join(ident[3+i, :] + a[i]/b[0]*ident[0, :])
    assert chart * J * chart.T == J
    variance = (qin * qin.T)[0]/2
    assert variance == Q(old["three_mode_invariant"]["charge_variance"])
    covs, slopes, pulses = [], [], []
    for j in (0, 1):
        r = sp.Matrix(red["R" + str(j)])
        assert r.T*J*r == J and qout*r == qin
        transfer = chart*r
        joint = transfer * transfer.T/2
        assert joint[0,0] == variance
        k = joint.extract(TRANSVERSE,[0])/variance
        C = joint.extract(TRANSVERSE,TRANSVERSE) - variance*k*k.T
        assert C.is_positive_definite and C*symplectic(2)*C == symplectic(2)/4
        full = -transfer * J * past.T
        assert full[0,:] == sp.zeros(1,2)
        D = full.extract(TRANSVERSE,[0,1])
        assert D.rank() == 2 and D.T*symplectic(2)*D == sp.zeros(2)
        covs.append(C)
        slopes.append(k)
        pulses.append(D)
    return covs, slopes, pulses, variance


def unaffected_mode(C, d):
    # Pick a quadrature whose vacuum partner also annihilates the displacement.
    J = symplectic(2)
    solutions = (d.row_join(C*J*d)).T.nullspace()
    assert len(solutions) == 2
    a = solutions[0].T
    b = 2*a*C*J
    A = a.col_join(b)
    norm = (2*a*C*a.T)[0]
    assert norm > 0 and A*d == sp.zeros(2,1)
    assert A*J*A.T == norm*symplectic(1) and A*C*A.T == norm*sp.eye(2)/2
    return A, norm


def single_pulse(covs, slopes, pulses, variance):
    tests, alphas, exponents, dets = {}, {}, {}, {}
    for reject in (0,1):
        branch = 1-reject
        A, norm = unaffected_mode(covs[reject],pulses[reject][:,1])
        cov = A*covs[branch]*A.T/norm
        assert cov.det() >= Q(1,4)
        total = cov+sp.eye(2)/2
        determinant = total.det()
        assert determinant > 1
        coeff = A * (slopes[branch]-slopes[reject]).row_join(pulses[branch][:,1])
        K = coeff.T*total.inv()*coeff/(2*norm)
        assert K.is_positive_semidefinite
        # Independent extraction using the same one-mode Gaussian's Wigner overlap.
        Vraw = A*(covs[branch]+covs[reject])*A.T
        assert Vraw.det()/norm**2 == determinant and coeff.T*Vraw.inv()*coeff/2 == K
        alpha = 1-1/sp.sqrt(determinant)
        alphas[branch],exponents[branch],dets[branch] = alpha,K,determinant
        tests["reject_C"+str(reject)] = {"quadratures_before_normalization":rows(A),
            "quadrature_normalization_squared":str(norm),"opposite_vacuum_denominator_squared":str(determinant),
            "opposite_exponent_matrix_u_t":rows(K)}
    # Tests have a classical choice, fixed independently of actual branch and pulse.
    probs = {j:alphas[1-j]/(alphas[0]+alphas[1]) for j in (0,1)}
    floor = alphas[0]*alphas[1]/(alphas[0]+alphas[1])
    # Rational decimal enclosure by comparing exact radicals.
    scale = 10**10
    n = int(sp.floor(floor*scale))
    assert Q(n,scale) < floor < Q(n+1,scale)
    out = {"tests":tests,"choose_test_reporting_C0_C1":[float(probs[j]) for j in (0,1)],
           "single_test_floor_C0_C1":[float(alphas[j]) for j in (0,1)],
           "uniform_branch_floor_enclosure":[str(Q(n,scale)),str(Q(n+1,scale))]}
    # Average at reference p=N(0,v) for several pulse amplitudes with independent quadrature.
    def real(x):
        return mp.mpf(str(x.evalf(60)))
    samples = {}
    with mp.workdps(48):
        v = real(variance)
        for t in (0, 1, -1, 2):
            sample = []
            for j in (0,1):
                K = exponents[j]
                a,b,c = (real(x) for x in (K[0,0],K[0,1],K[1,1]))
                r,p = 1/mp.sqrt(real(dets[j])), real(probs[j])
                width = 1+2*a*v
                avg = mp.exp(-(c-2*b*b*v/width)*t*t)/mp.sqrt(width)
                val = p*(1-r*avg)
                def integrand(u):
                    return p*(1-r*mp.exp(-(a*u*u+2*b*u*t+c*t*t)))*mp.exp(-u*u/(2*v))/mp.sqrt(2*mp.pi*v)
                numeric = mp.quad(integrand,[-mp.inf,0,mp.inf])
                assert abs(val-numeric) < mp.mpf("1e-40") and val >= real(floor)
                sample.append(float(val))
            samples[str(t)] = sample
    out["reference_charge_efficiencies_C0_C1"] = samples
    return out, floor, probs


def recorded_controls(covs, slopes, pulses, variance):
    # The known first source is included in the vacuum centre. Only the unknown
    # second displacement must annihilate the protected mode.
    for j in (0,1):
        A, norm = unaffected_mode(covs[j],pulses[j][:,1])
        u, t1, t2 = sp.symbols("u t1 t2",real=True)
        mu = slopes[j]*u + pulses[j]*sp.Matrix([t1,t2])
        centre = A*(slopes[j]*u + pulses[j][:,0]*t1)
        assert A*mu == centre
        assert A*covs[j]*A.T == norm*sp.eye(2)/2
    # If both settings are recorded, the reciprocal two-ray measurement is
    # defined for their displaced means on every charge fibre.
    total = covs[0]+covs[1]
    B = (slopes[0]-slopes[1]).row_join(pulses[0]-pulses[1])
    K = B.T*total.inv()*B/4
    h4 = 1/total.det()
    old = load(SRC/"charge_reference.json")["three_mode_invariant"]
    assert h4 == Q(old["conditional_overlap_at_zero_fourth_power"])
    assert 2*K[0,0] == Q(old["conditional_abs_overlap_exp_minus_gap_times_q2_over_two"])
    assert K.is_positive_semidefinite
    scale = 10**11
    count = int(sp.floor((1-sp.root(h4,4))*scale))
    assert (1-Q(count+1,scale))**4 < h4 < (1-Q(count,scale))**4
    # Verify the analytic charge integral for a nonzero two-pulse setting.
    t = sp.Matrix([1,-2])
    a = K[0,0]
    b = (K[0,1:]*t)[0]
    c = (t.T*K[1:,1:]*t)[0]
    width = 1+2*a*variance
    loss_prefactor4 = h4/width**2
    exponent = c-2*b*b*variance/width
    assert exponent >= 0
    with mp.workdps(45):
        val = lambda x: mp.mpf(str(x.evalf(60)))
        v, aa, bb, cc = (val(x) for x in (variance,a,b,c))
        h = mp.root(val(h4),4)
        direct_loss = mp.quad(lambda u:h*mp.exp(-aa*u*u-2*bb*u-cc-u*u/(2*v))/
                              mp.sqrt(2*mp.pi*v),[-mp.inf,0,mp.inf])
        analytic_loss = mp.root(val(loss_prefactor4),4)*mp.exp(-val(exponent))
        assert abs(direct_loss-analytic_loss) < mp.mpf("1e-40")
    return {"one_setting_recorded":"Centre the test using known t1. The same one-pulse floor holds.",
            "both_settings_recorded_overlap_exponent_u_t1_t2":rows(K),
            "overlap_prefactor_fourth_power":str(h4),
            "both_known_uniform_floor_enclosure":[str(Q(count,scale)),str(Q(count+1,scale))],
            "both_known_eta_at_reference_p_t1_1_t2_minus2":float(1-analytic_loss)}


def clock_bounds(floor, probs, rates):
    clock = load(SRC/"clock.json")
    def change(model, channel):
        return clock["split"][model][channel]-clock["narrow"][model][channel]
    a,b = [change("coupled",ch) for ch in ("one_pair","three_pairs")]
    assert a < b < 0
    assert all(change("common_C0_dust",ch)==b for ch in ("one_pair","three_pairs"))
    d = a-b
    assert abs(d-clock["score_shift_split_minus_narrow"]["coupled"]) < 1e-15
    lo, hi = float(floor), [float(probs[j]) for j in (0,1)]
    raw = [a*hi[1]-b*lo, a*lo-b*hi[0]]
    control = [b*(hi[1]-lo),b*(lo-hi[0])]
    corrected = [d*hi[1],d*lo]
    assert raw[1] < 0 and corrected[1] < 0
    sample = {}
    for t,(e0,e1) in rates.items():
        r,c = a*e1-b*e0,b*(e1-e0)
        assert abs((r-c)-d*e1)<1e-16 and raw[0] <= r <= raw[1]
        sample[t]={"coupled":r,"common_dust":c,"difference":r-c}
    return {"clock_raw_changes_one_three":[a,b],"inclusive_density_response":0,
            "coupled_outer_interval":raw,"common_dust_outer_interval":control,
            "control_subtracted_outer_interval":corrected,"reference_charge_by_pulse":sample}


def compute():
    covs, slopes, pulses, variance = fibres(archive())
    single, floor, probs = single_pulse(covs,slopes,pulses,variance)
    both = {}
    for j,D in enumerate(pulses):
        indices = list(D.T.rref()[1])
        minor = D.extract(indices,[0,1]).det()
        assert minor != 0
        both["C"+str(j)] = {"displacement_columns":rows(D),"rank":2,"symplectic_pairing":0,
                             "minor_row_indices_zero_based":indices,"nonzero_minor":str(minor)}
    return {"one_unknown_pulse":single,"two_unknown_pulses":both,
            "recorded_controls":recorded_controls(covs,slopes,pulses,variance),
            "backreaction":clock_bounds(floor,probs,single["reference_charge_efficiencies_C0_C1"]),
            "stage_5A":"HOLD"}


def compare(actual, stored):
    if isinstance(actual, dict):
        assert actual.keys() == stored.keys()
        for key in actual:
            compare(actual[key], stored[key])
    elif isinstance(actual, list):
        assert len(actual) == len(stored)
        for value, reference in zip(actual, stored):
            compare(value, reference)
    elif isinstance(actual, float):
        assert math.isclose(actual, stored, rel_tol=1e-13, abs_tol=1e-15)
    else:
        assert actual == stored


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Keep assertions enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    result = compute()
    path = BASE/"results.json"
    if args.write:
        path.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    else:
        compare(result, load(path))
    print("PASS: N11 maps, vacuum modes, uniform floor, independent charge integrals, two-source rank and clock controls.")
