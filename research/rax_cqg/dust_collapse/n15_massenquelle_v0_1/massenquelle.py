"""Model-level boundary density readout. All decision bounds use exact Fractions."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / "basis"), str(ROOT / "basis/synchronisiert")]
import coherence
import randquelle
import support
import tube
import zweifenster

P, I, F = support.PAST, support.I, support.FUTURE
G = Q(1, 2)
ETA = Q(1, 100)
STEPS = ((Q(1, 256), Q(1, 16384)), (Q(1, 512), Q(1, 32768)))


def json_value(name):
    return json.loads((ROOT / name).read_text())


def audit_sources():
    for path, item in json_value("quellen.json")["files"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == item["sha256"], path
    assert sha256((ROOT / "pruefplan.txt").read_bytes()).hexdigest() == (
        ROOT / "pruefplan.sha256").read_text().split()[0]
    assert randquelle.PROFILE == (76, 47, 24, 8)
    assert zweifenster.evaluated() == json_value("basis/zweifenster.json")


def layer_coefficients(code):
    _, order = support.geometry(code)
    return {(i, j): randquelle.edge_weight(sum((i, v) in order and (v, j) in order
                                                for v in range(15))) for i, j in order}


def action(y, w, edges):
    return -sum(w) / 2 - sum(b * w[j] * (y[i] - y[j]) ** 2 for (i, j), b in edges.items()) / 38


def read_boundary(y, evaluate, steps):
    """The reader sees an action oracle and the unshifted duration only."""
    duration = y[7] - y[3]
    assert duration > 0
    return randquelle.visible_sum(evaluate, y, *steps) / duration


def rival_profile(e):
    m2 = Q(19, 20)
    return Q(3, 8) / m2 + (1 / m2 - 1) * (1 - 23 * e) / (3 * (4 - e))


def single_fields(mass, k, e):
    y = [Q(0)] * 15
    for j in P + F:
        y[j] = Q(j - 5)
    y[3] += e
    remaining = [j for j in I if j not in (4, 13)]
    u = {j: Q(1, 2) + Q(i, 2 * (len(remaining) + 1)) for i, j in enumerate(remaining, 1)}
    u.update({4: Q(1, 2) - k, 13: k})
    for j in I:
        y[j] = y[3] + (4 - e) * u[j]
    w = [Q(1, 2) if j in P + F else Q(0) for j in range(15)]
    w[4], w[13] = mass * (4 - e) / 4, 3 * mass * (4 - e) / 4
    return y, w


def pointwise_pair():
    # All offsets lie within this larger interval since Delta > 1/4.
    ends = (Q(-3, 8), Q(3, 8))
    low_k, high_k = rival_profile(ends[1]), rival_profile(ends[0])
    assert Q(1, 4) < low_k < high_k < Q(1, 2)
    assert (1 - 23 * 4) == -91  # derivative of (1-23e)/(4-e), numerator
    assert 3 * (4 * support.DELTA[1] + Q(3, 32)) / 4 < 1
    rel, coeff = zweifenster.order_and_layers()
    assert layer_coefficients(2324) == coeff
    checked = 0
    offsets = tuple(Q(t, 64) for t in (-23, -20, -16, -12, -8, 8, 12, 16, 20, 23))
    for e in offsets:
        assert any(lo < e * dlo < hi and lo < e * dhi < hi for lo, hi in support.WINDOWS
                   for dlo, dhi in (support.DELTA,))
        p = []
        for mass, k in ((Q(1), Q(3, 8)), (Q(19, 20), rival_profile(e))):
            y, w = single_fields(mass, k, e)
            assert all(y[i] < y[j] for i, j in rel)
            p.append(zweifenster.read_action(rel, coeff, k, mass, e))
            assert p[-1] == mass*(4-e)*((1-23*e)+3*k*(4-e))/76
            for steps in STEPS:
                assert read_boundary(y, lambda t: action(t, w, coeff), steps) == mass
                checked += 1
        assert p[0] == p[1]
    # Verify the symbolic identity after clearing 3(4-e): the equality is
    # coefficientwise in A=1-23e and B=3(4-e), with k' B=k B/M'+(1/M'-1)A.
    m2 = Q(19, 20)
    assert m2 * (1 + (1 / m2 - 1)) == 1 and m2 * (Q(3, 8) / m2) == Q(3, 8)
    sample_y, sample_w = single_fields(Q(0), Q(3, 8), Q(1, 4))
    for weights in (sample_w, [Q(0)] * 15):
        for steps in STEPS:
            assert read_boundary(sample_y, lambda t: action(t, weights, coeff), steps) == 0
    return {"M": ["1", "19/20"], "coincident_observation": "pointwise pair (e,p(e))",
            "second_profile_range_on_larger_offset_interval": [low_k, high_k],
            "two_percent_bands_disjoint": m2 * Q(102, 100) < Q(98, 100),
            "original_350_pair_readout_by_profile_independent_identity": ["1", "19/20"],
            "four_action_reconstructions": checked, "vacuum_controls": 2}


def visibility():
    census = json_value("basis/synchronisiert/census.json")["by_type"]
    codes = support.catalogue()
    assert sorted(map(int, census)) == codes
    joint = {}
    deep_example = None
    for code in codes:
        _, order = support.geometry(code)
        edges = layer_coefficients(code)
        def coefficient(j):
            return -sum(edges.get((i, j), 0) * randquelle.PROFILE[i] for i in P) / Q(64)
        assert all(coefficient(j) == 0 for j in F)
        hidden = [j for j in I if coefficient(j) == 0]
        for j in I:
            assert coefficient(j) == int(sum((v, j) in order for v in I) < 4)
        visible, fits = not hidden, census[str(code)]["full_box"]
        key = f"full_visibility={int(visible)}, capacity_gate={int(fits)}"
        joint[key] = joint.get(key, 0) + 1
        if code == 2324:
            assert visible and fits
        if hidden and deep_example is None:
            y, w = single_fields(Q(0), Q(3, 8), Q(1, 4))
            # Source Hessian is independent of y, but choose causal test clocks for this order.
            for j in I:
                y[j] = -1 + Q(sum((v, j) in order for v in I), 4)
            assert all(y[i] < y[j] for i, j in order)
            w2 = w.copy()
            w2[hidden[0]] += Q(1, 8)
            for field in (w, w2):
                assert read_boundary(y, lambda t: action(t, field, edges), STEPS[0]) == 0
            deep_example = {"type": code, "unseen_vertex": hidden[0],
                            "change_in_total_scaled_density": Q(1, 8), "change_in_readout": 0}
    assert sum(joint.values()) == 1048
    return {"joint_counts": joint, "negative_control_free_densities": deep_example}


def distributed():
    profile = tube.run()
    assert json.loads(json.dumps(profile)) == json_value("basis/synchronisiert/tube.json")
    cones = coherence.run()
    assert cones == json_value("basis/synchronisiert/coherence.json")
    edges = layer_coefficients(2324)
    _, order = support.geometry(2324)
    paths, _ = support.paths_and_edges(order)
    count = 0
    for mass, e, jitter, sign in product(support.MASSES, (Q(-1, 4), Q(1, 4)),
                                          (Q(-1, 64), Q(0), Q(1, 64)), (-1, 1)):
        u = {j: Q(profile["clock_center"][str(j)]) + (-1)**j * jitter for j in I}
        shares = support.fractions_on_paths(paths, u)
        assert sum(shares) == 1 and min(shares) > 0
        y = [Q(j - 5) for j in range(15)]
        y[3] += e
        w = [Q(1, 2)] * 15
        for j, share in zip(I, shares):
            y[j] = y[3] + (4 - e) * u[j]
            w[j] = mass * (4 - e) * share * (1 + sign * ETA * (-1)**j)
            assert 0 < w[j] * support.DELTA[1] < 1
        assert all(y[i] < y[j] for i, j in order)
        for steps in STEPS:
            prediction = read_boundary(y, lambda t: action(t, w, edges), steps)
            assert prediction == sum(w[j] for j in I) / (4 - e)
            assert abs(prediction - mass) <= ETA * mass
            count += 1
    controls = {}
    for key, row in cones['rows'].items():
        mass = Q(key.split(';')[0])
        c = Q(row['conditional_modulus_lower_exact'])
        eps_abs = G * mass * ETA / 2
        x = eps_abs / c
        assert 0 < x < 1
        relative_error = ETA / (c - eps_abs)
        # |arg| <= x/(1-x) per arm; 3 < pi certifies no branch cut at +-pi.
        assert mass * G * (1 + relative_error) < 3 and relative_error < Q(2, 100)
        visibility_min = (1-x*x)/(1+x*x)
        controls[key] = {"relative_mass_error_upper": relative_error,
                         "conditional_pointer_visibility_lower": visibility_min,
                         "phase_error_margin_to_2pct_rad": G*mass*(Q(2,100)-relative_error),
                         "arm_modulus_lower_per_normalized_dust_measure": c-eps_abs}
    for name in ('1/4','1','4'):
        assert profile['masses'][name]['max_w_upper_including_width'] < 1
    return {"field_and_step_checks": count, "model_mass_reference": "M=0 exact vacuum",
            "rows_mass_and_initial_density": controls, "physical_P3": "60 x NOT_RUN"}


def run():
    audit_sources()
    return {"source_commit": json_value('quellen.json')['commit'],
            "probe_relative_phase_coupling": G, "paired_histories": pointwise_pair(),
            "catalogue": visibility(), "distributed_carrier": distributed()}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Active assertions required.')
    print(json.dumps(run(), default=str, sort_keys=True, indent=2))
