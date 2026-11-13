"""Exact source/clock/geometry eligibility; no new amplitudes or physics adapters.

Run: python boundary_coherence_v0_1/checks/physical_gate.py
Only this module's sibling physical_gate.json is written.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3"
PRIOR_HASHES = {
    "prior_einstein_check.py": "24ad63b52036c7c1caf16c9e66b197b6bc7241f6a13054ff173bc28bb877c85d",
    "prior_einstein_contract.json": "ef597edb45b45882dc2efdcb80926b28b86e920cfce78dcff172450d73f51e19",
    "prior_einstein_calibration.json": "8ad992fb2376e357341965e5ddbfce1537cd94e7b7f2e9438fd9cee8c5e22a68",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zero(expression):
    require(s.cancel(s.expand(expression)) == 0, str(expression))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closure(edges):
    rel = {tuple(edge) for edge in edges}
    while True:
        new = rel | {(i, k) for i, j in rel for jj, k in rel if j == jj}
        if new == rel:
            return rel
        rel = new


pilot_path = ROOT / "sources/pilot.json"
require(sha(pilot_path) == EXPECTED, "Frozen pilot changed")
for filename, expected in PRIOR_HASHES.items():
    require(sha(ROOT / "sources" / filename) == expected, f"Changed prior evidence: {filename}")
pilot = json.loads(pilot_path.read_text())
r_contract_path = ROOT / "contracts/r_records.json"
r_contract = json.loads(r_contract_path.read_text())
require(r_contract["source_contract_sha256"] == EXPECTED, "Wrong R source")
require(r_contract["original_action_measures_histories_preparations_unchanged"],
        "R extension changed pilot variables")

tt = s.symbols("T0:6", real=True)
rr = s.symbols("r0:6", real=True)
qq = s.symbols("q0:6", real=True)
beta = 4 / s.sqrt(6)
reflect = {time: -time for time in tt}
hist = pilot["history_family"]
all_orders = []
for class_index in (1, 2):
    base = closure(hist["common_generating_relations"] + hist[f"class_{class_index}_added_relations"])
    orbit = set()
    for swap_a, swap_r in itertools.product((False, True), repeat=2):
        perm = list(range(6))
        if swap_a:
            perm[1], perm[2] = perm[2], perm[1]
        if swap_r:
            perm[4], perm[5] = perm[5], perm[4]
        orbit.add(tuple(sorted((perm[i], perm[j]) for i, j in base)))
    require(len(orbit) == hist["class_orbit_sizes"][class_index - 1], "Wrong orbit")
    all_orders.extend((class_index, order) for order in sorted(orbit))
require(len(all_orders) == 6, "Wrong history count")

rows = []
boundary_orders = set()
r_orders = set()
current_count = 0
for class_index, ordered in all_orders:
    rel = set(ordered)
    coefficients = {}
    for i, j in ordered:
        n = sum((i, z) in rel and (z, j) in rel for z in range(6))
        coefficients[i, j] = pilot["action"]["interval_coefficients"][n] if n < 4 else 0
    f4 = 6 - sum(coefficients.values())
    require(f4 == hist["gravity_values_F4"][class_index - 1], "Wrong F4")
    constraints = [1 + beta * sum(b * (tt[j] - tt[i]) ** 2
                   for (i, jj), b in coefficients.items() if jj == j) / 2
                   for j in range(6)]
    dust = -sum(rr[j] * constraints[j] for j in range(6)) / 2
    scalar = -beta * sum(b * (qq[j] - qq[i]) ** 2
                        for (i, j), b in coefficients.items()) / 4
    action = f4 + dust + scalar
    for j in (1, 2):
        require([i for i, jj in ordered if jj == j] == [0], "Unexpected A predecessor")
        zero(-2 * s.diff(action, rr[j]) - (1 + beta * (tt[j] - tt[0]) ** 2 / 2))
    zero(action.xreplace(reflect) - action)
    currents = {(i, j): beta * rr[j] * b * (tt[j] - tt[i]) / 2
                for (i, j), b in coefficients.items() if b}
    for current in currents.values():
        zero(current.xreplace(reflect) + current)
        current_count += 1
    balances = []
    for z in range(6):
        balance = (sum(value for (i, j), value in currents.items() if i == z)
                   - sum(value for (i, j), value in currents.items() if j == z))
        zero(balance - s.diff(action, tt[z]))
        balances.append(balance)
    zero(sum(balances))
    terminal_action = action.subs({rr[4]: 0, rr[5]: 0})
    zero(s.diff(terminal_action, tt[4]))
    zero(s.diff(terminal_action, tt[5]))
    r_order = tuple((i, j) for i, j in ordered if i in (4, 5) and j in (4, 5))
    boundary = tuple((i, j) for i, j in ordered if i != 3 and j != 3)
    r_orders.add(r_order)
    boundary_orders.add(boundary)
    rows.append({"class": class_index, "relations": [list(x) for x in ordered],
                 "F4": f4, "A_constraints_verified": 2,
                 "current_edges_verified": len(currents), "R_induced_relations": list(r_order)})
require(r_orders == {()}, "R is not the common antichain")
require(len(boundary_orders) == 1, "Outer boundary orders differ")

# A deliberately unadopted boundary-state candidate: smooth, permutation invariant,
# same action and full original clock support. This is NOT a physical source proof.
eta, shift = s.symbols("eta shift", real=True)
chi = (tt[1] + tt[2]) / 2 - tt[0]
zero(chi.xreplace(reflect) + chi)
zero(chi.xreplace({tt[1]: tt[2], tt[2]: tt[1]}) - chi)
zero(chi.xreplace({time: time + shift for time in tt}) - chi)


def clock_mean(poly):
    poly = s.Poly(s.expand(poly), *tt[:3])
    result = 0
    for powers, coefficient in poly.terms():
        if any(power % 2 for power in powers):
            continue
        result += coefficient * s.prod(s.Rational(1, power + 1) for power in powers)
    return s.simplify(result)


zero(clock_mean(chi))
zero(clock_mean(chi ** 2) - s.Rational(1, 2))
zero(clock_mean(chi ** 3))
tilt_numerator = 1 + eta * chi / 2
tilt_norm_sq = 1 + eta ** 2 / 8
zero(clock_mean(tilt_numerator ** 2) - tilt_norm_sq)
biased_mean = s.cancel(clock_mean(chi * tilt_numerator ** 2) / tilt_norm_sq)
zero(biased_mean - eta / (2 * tilt_norm_sq))
require(all(abs(chi.subs(dict(zip(tt[:3], corner)))) <= 2
            for corner in itertools.product((-1, 1), repeat=3)), "Wrong chi bound")
# The polynomial has no interior extrema; affine extrema occur at these corners.
# For |eta|<1: numerator >=1-|eta|>0; the original cube support is retained.

# Check the declared common finite R-instrument majorant algebraically.
r_bound = 2 * 4 * s.Rational(3, 5) ** 2 * s.Rational(2257, 16) * (65 + 799) / 1024 ** 2
require(0 < r_bound < 1, "R instrument majorant is not a contraction")

# Separate canonical positive-source patch: exact re-derivation of its central
# identities only. The old interval certificate is reused, not silently transplanted.
a, b, c, d, t, u, w, v, h = s.symbols("a b c d t u w v h", real=True)
times = [a, b, c, d, t, u]
B = {(0, 4): -8, (1, 4): 16, (2, 4): -9, (3, 4): 1,
     (1, 5): -8, (2, 5): 16, (3, 5): -9, (4, 5): 1}
weights = {4: w, 5: v}
cc = {j: 1 + sum(s.Rational(bij, 2) * (times[j] - times[i]) ** 2
                 for (i, jj), bij in B.items() if jj == j) for j in (4, 5)}
sd = -(w * cc[4] + v * cc[5]) / 2
jj = {(i, j): weights[j] * bij * (times[j] - times[i]) / 2 for (i, j), bij in B.items()}
k = (70 - 4 * s.sqrt(305)) / 3
p = h - k
l = 9 * k - s.Rational(4, 3) - s.Rational(17, 2) * h
bb = 12 + 36 * h
t_h = 9 * h + h * l / p
u_h = 9 * h + p * bb / l + h * l / (2 * p)
ratio_r = h * l / (2 * p ** 2) - bb / l
j_h = h * l / p
sub = {a: -s.sqrt(305) / 6, b: -s.Rational(5, 2), c: -2,
       d: -s.Rational(4, 3) + h, t: t_h, u: u_h, w: ratio_r * v}
charge = v * j_h / 2
zero(cc[4].subs(sub))
zero(cc[5].subs(sub))
zero(s.diff(sd, t).subs(sub))
zero(s.diff(sd, u).subs(sub) - charge)
for cut in (3, 4):
    zero(sum(value for (i, j), value in jj.items() if i <= cut < j).subs(sub) + charge)
charge_ratio = s.cancel(charge.subs(v, s.Rational(1, 4) / ratio_r)
                        / charge.subs(v, s.Rational(1, 64) / ratio_r))
require(charge_ratio == 16, "Wrong canonical charge ratio")
zero(s.diff(t_h, v))
zero(s.diff(u_h, v))
old_canonical_path = ROOT / "sources/prior_einstein_calibration.json"
old_canonical = json.loads(old_canonical_path.read_text())
require(old_canonical["checks_passed"], "Missing original canonical certificate")
require(old_canonical["contract_sha256"] == PRIOR_HASHES["prior_einstein_contract.json"],
        "Prior certificate contract mismatch")
require(old_canonical["record_preserving_aggregation"]["all_failed_for_both_global_orientations"],
        "Different canonical orientation result")

gate = {
    "id": "BOUNDARY-COHERENCE-PHYSICAL-ELIGIBILITY-0.1",
    "checks_passed": True,
    "status": "NOT_ELIGIBLE_FOR_PHYSICAL_TWO_SOURCE_GEOMETRY_RESPONSE",
    "new_amplitude_integrations": 0,
    "physical_CST_trajectory_computed": False,
    "physical_data_points": 0,
    "six_history_exact_checks": {
        "histories": rows, "history_count": 6, "A_constraint_identities": 12,
        "A_constraint": "C_i=1+beta*(T_i-T_0)^2/2 >= 1, i=1,2; beta=4/sqrt(6)>0",
        "current": "J_ij=beta*r_j*b_ij*(T_j-T_i)/2",
        "derivative_divergence_identities": 36, "global_shift_identities": 6,
        "nonzero_edge_current_parities": current_count,
        "action_parity": "S(-T)=S(T)", "current_parity": "J_ij(-T)=-J_ij(T)",
        "endpoint_clock_derivatives_zero": 12,
        "common_outer_boundary_order": [list(pair) for pair in next(iter(boundary_orders))],
        "common_intrinsic_R_order": "two-element antichain",
        "oriented_insertion_result": "Every single-current or oriented-cut-current amplitude insertion is exactly zero under the frozen reflection-even clock packets. Holds before Abel removal and in an existing paired Abel limit.",
        "new_records_preserve_obstruction": "T-independent class recombination and q-only f0/f2 terminal packets are even under T reflection.",
        "not_claimed": "No physical mean-current, probability, mass-zero, or exclusion of even current correlations."
    },
    "oriented_clock_candidate": {
        "status": "OUTSIDE_FROZEN_CONTRACT", "adopted": False,
        "chi": "(T1+T2)/2-T0", "chi_range": [-2, 2],
        "chi_variance_exact": "1/2",
        "state_factor": "h_eta=(1+eta*chi/2)/sqrt(1+eta^2/8), -1<eta<1",
        "kinematic_norm_squared": "1",
        "biased_kinematic_chi_mean": "eta/[2*(1+eta^2/8)]",
        "symmetries": ["S2(A) invariant", "relative under common clock shift", "reflection sends eta to -eta"],
        "support": "Entire original clock cube; no half-clock cut",
        "source_space": "Multiplication preserves g0/gplus orthogonality through disjoint density strata; weighted scalar input norm unchanged.",
        "current_insertion_identity": "A_J[h_eta*g]=eta/(2*sqrt(1+eta^2/8))*A_(J*chi)[g]",
        "nonzero_current_established": False,
        "physical_selection": "Not derived. The reflection-symmetric action does not select the sign of this new boundary datum; proper-time, current-positivity and physical constraint pairing remain unresolved.",
        "new_values_computed": "Only exact polynomial clock moments; no new action-weighted integral."
    },
    "eligibility": {
        "same_instrument_for_two_preparations": {
            "kinematic_status": "PASS_DECLARED_COMMON_INSTRUMENT",
            "evidence": "The R-record contract fixes one pair f0/f2, one gain and one failure completion on E for both g0/gplus.",
            "R_bound_exact": str(r_bound),
            "physical_status": "UNRESOLVED_DETECTOR_REALIZATION_AND_COHERENCE"
        },
        "admissible_physical_sources": {
            "status": "HOLD_NOT_DERIVED",
            "rigorous_scope": "Freely varied positive stationary A densities are excluded by C_A>=1. Fixed boundary/off-shell quantum packets are not excluded, but g0/gplus is not a calibrated physical source pair."
        },
        "relational_physical_clock": {
            "status": "HOLD_NOT_DERIVED",
            "rigorous_scope": "Frozen oriented single-current insertions vanish. A relative kinematic clock exists, but no proper-time/current/mass calibration follows."
        },
        "geometric_R_observable": {
            "status": "HOLD_NOT_DERIVED",
            "rigorous_scope": "Any intrinsic-order-only function of the common two-element R antichain is constant over the six histories.",
            "allowed_result": "f0/f2 is a pair of terminal scalar matter records; it is not an areal radius, volume, curvature or energy observable. Full-history geometric observables are not excluded."
        },
        "scale_and_refinement": {"status": "HOLD_NOT_DEFINED", "evidence": "Only N=6; no independent geometric scale or continuum/refinement family in the contract."},
        "global_exterior": {"status": "HOLD_NOT_DEFINED", "evidence": "Original global_exterior adapter is null; no matching solution supplied."}
    },
    "separate_canonical_patch": {
        "status": "SEPARATE_ALTERNATIVE_NOT_TRANSPLANTED",
        "rederived_now": ["C4=C5=0", "q_t=0", "q_u=Q", "both complete cuts=-Q", "Q2/Q1=16", "identical order and clocks for charge variation"],
        "reused_certificate": str(old_canonical_path.relative_to(ROOT)),
        "prior_script_scope": "sources/prior_einstein_check.py is a pinned provenance copy, not a standalone replay target without its original source package. This physical_gate.py re-derives the explicitly listed identities and only reuses the stated interval certificate.",
        "reused_restricted_obstruction": "Complete-cut flux=-Q<0 while J_tu>0; both global orientations fail a positive local flow for all eight order-convex partitions preserving d,t,u. Absolute-value rectification breaks interior conservation.",
        "restricted_adapter_exclusion": "Same F(C,T), G(C,T) yield identical curves for Q and 16Q; under hypothetical M=cQ, cannot reproduce nonzero reference collapse slope ratio4.",
        "limitations": "Different clock normalization, order and boundary roles from six-history quantum pilot. No physical M(Q), radius, exterior or continuum limit follows. Broader derived observables and other order families remain open."
    },
    "tests_executable_now": [
        "Exact source, current, clock-parity and intrinsic R-order exclusions (executed here)",
        "Finite coherent/dephased instrument comparison using existing amplitudes (separate agent check)",
        "Two terminal scalar-record diagnostic using analytic Gaussian moments and inherited clock amplitudes (separate agent check)",
        "Kinematic normalization and parity analysis of an unadopted boundary-clock candidate (executed here)"
    ],
    "physical_response_test_executable_now": False,
    "stop_rule": "Do not increase histories, clock quadrature or precision to stand in for an absent physical source/clock/geometry calibration. Reopen a physical comparison only with one independently derived common source-to-observable adapter and justified scale/refinement/exterior scope.",
    "source_sha256": {
        str(path.relative_to(ROOT)): sha(path)
        for path in (pilot_path, r_contract_path, ROOT / "sources/prior_einstein_check.py",
                     ROOT / "sources/prior_einstein_contract.json", old_canonical_path)
    }
}
(ROOT / "checks/physical_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps({"status": gate["status"], "histories": 6,
                  "A_constraint_identities": 12, "current_parities": current_count,
                  "oriented_clock_candidate": "OUTSIDE_FROZEN_CONTRACT; UNADOPTED",
                  "physical_data_points": 0, "checks_passed": True}))
