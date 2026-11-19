"""Reproduce the N11 neutral source algebra, charge response and false-click witness."""
import argparse
import hashlib
import json
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


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def symplectic(n):
    return sp.zeros(n).row_join(sp.eye(n)).col_join((-sp.eye(n)).row_join(sp.zeros(n)))


def rebuild():
    for name, record in load(BASE / "provenance.json")["files"].items():
        assert hashlib.sha256((SRC / name).read_bytes()).hexdigest() == record["sha256"]
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "canonical_check.py"
        shutil.copyfile(SRC / script.name, script)
        subprocess.run([sys.executable, "-B", str(script)], check=True, stdout=subprocess.DEVNULL)
        canonical = load(script.with_name("results.json"))
    assert canonical == load(SRC / "canonical.json")
    return canonical


def scalar(matrix):
    assert matrix.shape == (1, 1)
    return matrix[0]


def source_algebra(canonical, previous):
    contract = load(BASE / "contract.json")
    past, future = (sp.Matrix(contract[key]) for key in ("past_coordinate_sources", "future_coordinate_sources"))
    reduction = canonical["common_reduction"]
    maps = [sp.Matrix(reduction["R" + str(i)]) for i in range(2)]
    shifts = [sp.Matrix(v) for v in previous["shift_in_out"]]
    pull = []
    for side, basis, shift, name, section, end in zip(
        ("minus", "plus"), (past, future), shifts, ("A_minus", "A_plus"),
        ("input_embedding", "output_embedding"), (3, 0)
    ):
        constraint = sp.Matrix(canonical["constraints"][name])
        embedding = sp.Matrix(reduction[section])
        gauge = (symplectic(4) * constraint.T)[:4, :]
        tests = sp.ones(4, 1).row_join(gauge)
        assert tests.rank() == basis.rank() == 2 and basis * tests == sp.zeros(2)
        reduced = basis.row_join(sp.zeros(2, 4)) * embedding
        assert reduced * shift == sp.zeros(2, 1)
        charged = sp.eye(4)[end, :]
        assert scalar(charged * gauge) == 0
        assert scalar(charged.row_join(sp.zeros(1, 4)) * embedding * shift) == 1, side
        pull.append(reduced)
    past_rows, future_rows = pull
    w_in, w_out = shifts
    J = symplectic(3)
    for r in maps:
        assert r.T * J * r == J and r * w_in == w_out
    rows = past_rows.col_join(future_rows * maps[0]).col_join(future_rows * maps[1])
    assert rows * w_in == sp.zeros(6, 1) and rows.rank() == 5
    independent = list(rows.T.rref()[1])
    cols = list(rows.rref()[1])
    minor = rows.extract(independent, cols).det()
    assert minor != 0
    charge = w_in.T * J
    assert rows.col_join(charge).rank() == 5
    assert rows * J * charge.T == sp.zeros(6, 1) and (rows * J * rows.T).rank() == 4
    # Isometry on both branches implies commutation with the relative metaplectic map.
    relative = maps[0].inv() * maps[1]
    orbit = past_rows[:1, :]
    ranks = [1]
    for unused in range(4):
        orbit = orbit.col_join(orbit[-1, :] * relative)
        ranks.append(orbit.rank())
    assert ranks == [1, 2, 3, 4, 5] and orbit * w_in == sp.zeros(5, 1)
    return maps, shifts, past_rows, {
        "full_source_rank": 5, "commutator_form_rank": 4,
        "nonzero_minor_zero_based_rows": independent, "nonzero_minor_zero_based_cols": cols,
        "nonzero_minor": str(minor), "past_first_source_relative_orbit_ranks": ranks,
        "single_end_charge_shift_per_unit_pulse": 1,
    }


def charge_fibres(maps, shifts, previous):
    w_in, w_out = shifts
    J = symplectic(3)
    charge = w_out.T * J
    a, b = charge[:, :3].T, charge[:, 3:].T
    unit = sp.eye(6)
    chart = charge
    for i in (1, 2):
        chart = chart.col_join(unit[i, :] - b[i] / b[0] * unit[0, :])
    chart = chart.col_join(-unit[0, :] / b[0])
    for i in (1, 2):
        chart = chart.col_join(unit[3+i, :] + a[i] / b[0] * unit[0, :])
    assert chart * J * chart.T == J
    axes = [1, 2, 4, 5]
    variance = scalar(w_in.T * w_in) / 2
    covs, slopes = [], []
    for r in maps:
        joint = chart * r * r.T * chart.T / 2
        assert joint[0, 0] == variance
        k = joint.extract(axes, [0]) / variance
        cov = joint.extract(axes, axes) - variance * k * k.T
        assert cov * symplectic(2) * cov == symplectic(2) / 4
        covs.append(cov)
        slopes.append(k)
    total = covs[0] + covs[1]
    slope = slopes[0] - slopes[1]
    precision = total.inv()
    h4 = 1 / total.det()
    g = scalar(slope.T * precision * slope) / 2
    old = previous["three_mode_invariant"]
    assert (variance, h4, g) == tuple(Q(old[key]) for key in (
        "charge_variance", "conditional_overlap_at_zero_fourth_power",
        "conditional_abs_overlap_exp_minus_gap_times_q2_over_two"))
    return variance, h4, g, chart, axes, covs, slope, precision


def pulse_certificate(row, r, variance, h4, g, chart, axes, covs, slope, precision):
    shift = -chart * r * symplectic(3) * row.T
    assert shift[0] == 0
    d = shift.extract(axes, [0])
    A = scalar(d.T * precision * d) / 4
    B = scalar(d.T * (2*covs[0]).inv() * d) / 4
    L = scalar(slope.T * precision * d) / 2
    # On |u| <= 1, exp(-A-Lu) > 9/10 and exp(-B) < 1/2.
    assert 0 < A and A + abs(L) < Q(1, 10) and B > 1
    # The overlap obeys 1/30 < |s(u)| < 1/20 on the same interval.
    assert Q(1,25)**4 < h4 < Q(1,20)**4 and 0 < g < Q(28,100)
    assert Q(1,25)*(1-Q(14,100)) > Q(1,30)
    # 30 < v < 31, pi < 22/7 and exp(-x) >= 1-x imply Pr(|u|<=1) > 1/8.
    assert 30 < variance < 31 and 2*Q(22,7)*31 < 14**2
    assert 2*(1-Q(1,60))/14 > Q(1,8)
    lower = Q(1,8)*Q(19,20)*Q(1,30)**2*Q(2,5)**2
    return {"pulse_reduced_covector": list(map(str, row)), "branch": "C0",
            "false_outcome": "C1", "A": str(A), "B": str(B), "L": str(L),
            "false_probability_strict_lower_bound": str(lower)}


def efficiencies(variance, h4, gap, previous):
    clock = load(SRC / "clock.json")
    raw = clock["score_shift_split_minus_narrow"]
    assert clock["split"]["coupled"]["score"] - clock["narrow"]["coupled"]["score"] == raw["coupled"]
    assert raw["common_C0_dust"] == 0
    assert previous["backreaction"]["changes"]["density"]["all_modes"]["coupled"] == 0
    with mp.workdps(48):
        v, h, g = (mp.mpf(x.p)/int(x.q) for x in (variance, h4, gap))
        h = mp.root(h, 4)
        def gaussian(x, mu, var):
            return mp.exp(-(x-mu)**2/(2*var))/mp.sqrt(2*mp.pi*var)
        examples = {}
        for key, mu, var in (("reference", 0, v), ("two_lobes", mp.sqrt(3*v/4), v/4)):
            # For mu>0 use the equal mixture at +mu and -mu.
            assert abs(mu**2 + var - v) < mp.mpf("1e-44")
            eff = 1 - h/mp.sqrt(1+g*var)*mp.exp(-g*mu**2/(2*(1+g*var)))
            def density(x):
                return (gaussian(x, mu, var) + gaussian(x, -mu, var))/2
            direct = mp.quad(lambda x: density(x)*(1-h*mp.exp(-g*x*x/2)), [-mp.inf, 0, mp.inf])
            assert abs(direct-eff) < mp.mpf("1e-42")
            examples[key] = float(eff)
        assert abs(examples["reference"]-previous["three_mode_invariant"]["optimal_balanced_efficiency"]) < 1e-14
        assert examples["two_lobes"] > examples["reference"]
        return {"h_fourth_power":str(h4), "g":str(gap), "v":str(variance),
                "sharp_infimum":float(1-h), "sharp_supremum":1,
                "supremum_at_second_moment_v":float(1-h*mp.exp(-g*v/2)),
                "same_mean_and_variance_examples":examples,
                "archived_clock_delta":raw["coupled"],
                "clock_delta_open_endpoints":[raw["coupled"],float((1-h)*raw["coupled"])],
                "inclusive_density_delta":0,"common_dust_clock_delta":0}


def verify():
    canonical = rebuild()
    previous = load(SRC / "v03.json")
    maps, shifts, rows, algebra = source_algebra(canonical, previous)
    v, h4, g, chart, axes, covs, slope, precision = charge_fibres(maps, shifts, previous)
    return {"source_algebra":algebra, "charge_family":efficiencies(v,h4,g,previous),
            "fixed_detector_neutral_pulse":pulse_certificate(rows[1,:],maps[0],v,h4,g,chart,axes,covs,slope,precision),
            "physical_stage_5A":"HOLD"}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = verify()
    path = BASE / "results.json"
    if args.write:
        path.write_text(json.dumps(data, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    else:
        assert data == load(path), "Stored output disagrees with the replay."
    print("PASS: action reconstruction, neutral sources, charge-fibre rates, quadrature and false-click bound.")
