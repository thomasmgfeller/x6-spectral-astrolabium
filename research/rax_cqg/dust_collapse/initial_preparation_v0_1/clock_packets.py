"""Past-collar preparation for the two published N11 histories."""
import argparse
import importlib.util
import json
from pathlib import Path

import mpmath
import numpy as np

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "physical_boundary_readout_v0_1"
CONTRACT = json.loads((HERE / "packet_contract.json").read_text())
# Reuse the action, labels, measure parameters and affine clocks from PR 293.
spec = importlib.util.spec_from_file_location("ward_clock", PARENT / "checks/ward_clock/check.py")
ward = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ward)


def quadrature(order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return nodes, weights / 2


def reduced_weight(t, order, clock_grid):
    """Return B_past(t) and both weights with the common past phase removed."""
    nodes, weights = clock_grid
    x = ward.L * nodes
    w_plane = weights[:, None] * weights[None, :]
    values = []
    past_terms = []
    for removed in ward.ORDERS.values():
        coeffs, action = ward.coeffs(removed)
        times = [(j - 5) * ward.DELTA for j in range(ward.N)]
        times[3] = t
        past_terms.append(sum(ward.cvalue(j, times, coeffs) for j in ward.PAST))
        times[5], times[6] = x[:, None], x[None, :]
        total = 0j
        for k in range(order):
            times[4] = x[k]
            future = sum(ward.cvalue(j, times, coeffs) for j in ward.FUTURE)
            integrand = np.exp(-1j * future / 16)
            for j in ward.INNER:
                C = ward.cvalue(j, times, coeffs)
                # Exact half atom plus half interval in each of three densities.
                integrand = integrand * (1 + np.exp(-0.25j*C)*np.sinc(C/(4*np.pi))) / 2
            total += weights[k] * np.sum(w_plane * integrand)
        values.append(np.exp(1j * action) * total)
    np.testing.assert_allclose(past_terms[0], past_terms[1], rtol=0, atol=1e-14)
    return past_terms[0], np.array(values)


def detector_effects():
    controls = json.loads((HERE / "controls/results.json").read_text())
    centered = next(row for row in controls["scalar_controls"] if row["displacement"] == ["0"]*3)
    def z(field):
        datum = centered[field]
        return complex(float(datum["real"]), float(datum["imag"]))
    overlap, cross_var = z("overlap"), z("cross_pointer_variance")
    middle_cross = overlap * complex(mpmath.erf(1 / mpmath.sqrt(2*cross_var)))
    tail_cross = (overlap - middle_cross) / 2
    b0, b1 = np.array(centered["branch_pointer_bins"], dtype=float)
    effects = np.array([[[p0, cross], [np.conj(cross), p1]]
                        for p0, p1, cross in zip(b0, b1, (tail_cross, middle_cross, tail_cross))])
    assert np.min(np.linalg.eigvalsh(effects)) >= 0
    return effects


def records(history_weights, effects):
    a = history_weights / 2
    joint = np.einsum('i,bij,j->b', a.conj(), effects, a).real
    return np.append(joint, 1 - sum(joint))


def pack(record):
    assert np.all(record >= 0) and abs(sum(record)-1) < 5e-15
    accepted = sum(record[:3])
    return {"joint_left_middle_right_failure": record.tolist(), "success": accepted,
            "conditional_middle": record[1] / accepted}


def ratio(weights):
    z = weights[1] / weights[0]
    return [z.real, z.imag]


def experiment(inner, outer):
    clock_grid = quadrature(inner)
    nodes, weights = quadrature(outer)
    t0 = -2 * ward.DELTA
    offsets = CONTRACT["clock_offsets_from_affine_T3"]
    radii = CONTRACT["density_centers"]
    h = CONTRACT["clock_lobe_half_width"]
    e = CONTRACT["density_half_width"]
    # Single normalized lobe under dt/3 times normalized density indicator under dr/2.
    norm_factor = np.sqrt((2*h / 3) * e)
    effects = detector_effects()
    fixed = []
    for offset in [offsets[0], 0, offsets[1]]:
        b, v = reduced_weight(t0 + offset, inner, clock_grid)
        values = [v * np.exp(-0.5j*r*b) for r in radii]
        rows = [records(w, effects) for w in values]
        np.testing.assert_allclose(rows[0], rows[1], rtol=0, atol=3e-15)
        if offset == 0:
            # Compare the amplitude including its phase to the independent PR 293 replay.
            frozen = json.loads((HERE / "controls/sources/clock_results.json").read_text())
            for index, name in enumerate(ward.ORDERS):
                source = frozen["quadrature"][name][-1]["sources"]["1/8|1/8"]["W"]
                assert abs(complex(source["real"], source["imag"]) - values[0][index]) < 5e-12
        fixed.append({"T3_offset": offset, "W1_over_W0_re_im": ratio(v),
                      "rho_1_8": pack(rows[0]), "rho_1_4": pack(rows[1])})
    assert abs(fixed[0]["rho_1_8"]["success"] - fixed[2]["rho_1_8"]["success"]) > 1e-8

    # Each entry is integrated in amplitude inside its lobe.
    samples = [[reduced_weight(t0+offset+h*node, inner, clock_grid) for node in nodes]
               for offset in offsets]
    packets = []
    density_nodes, density_weights = quadrature(12)
    for r in radii:
        lobes = []
        compensated = []
        classical = np.zeros(4)
        for samples_in_lobe in samples:
            b = np.array([s[0] for s in samples_in_lobe])
            v = np.array([s[1] for s in samples_in_lobe])
            # Uniform positive-density interval integral; sinc(x)=sin(pi*x)/(pi*x).
            phases = np.exp(-0.5j*r*b) * np.sinc(e*b/(2*np.pi))
            raw_phases = np.exp(-0.5j * (r + e*density_nodes[:, None])*b)
            np.testing.assert_allclose(density_weights @ raw_phases, phases, rtol=0, atol=1e-14)
            corrected = density_weights @ (raw_phases * raw_phases.conj())
            lobes.append(norm_factor * ((weights*phases) @ v))
            compensated.append(norm_factor * ((weights*corrected) @ v))
            # Separate sharp-clock ensemble, with no projection of the input clock.
            for weight, branch in zip(weights, v):
                classical += (weight/2)*records(branch, effects)
        plus = (lobes[0]+lobes[1])/np.sqrt(2)
        minus = (lobes[0]-lobes[1])/np.sqrt(2)
        mix = (records(lobes[0], effects)+records(lobes[1], effects))/2
        np.testing.assert_allclose(mix, (records(plus,effects)+records(minus,effects))/2,
                                   rtol=0, atol=3e-15)
        packets.append({"rho_center": r, "coherent": pack(records(plus, effects)),
                        "dephased_lobes": pack(mix), "relative_pi_phase": pack(records(minus, effects)),
                        "W1_over_W0_coherent_re_im": ratio(plus),
                        "phase_compensated": pack(records(sum(compensated)/np.sqrt(2), effects)),
                        "classical_sharp_ensemble": pack(classical)})
    np.testing.assert_allclose(list(numbers(packets[0]["phase_compensated"])),
                               list(numbers(packets[1]["phase_compensated"])), rtol=0, atol=3e-15)
    assert packets[0]["classical_sharp_ensemble"] == packets[1]["classical_sharp_ensemble"]
    return {"fixed_clocks": fixed, "clock_density_packets": packets}


def numbers(node):
    if isinstance(node, dict):
        for key in sorted(node):
            yield from numbers(node[key])
    elif isinstance(node, list):
        for item in node:
            yield from numbers(item)
    else:
        yield float(node)


def compute():
    runs = [experiment(inner, outer) for inner, outer in CONTRACT["quadrature_inner_outer"]]
    spread = max(abs(a-b) for a,b in zip(numbers(runs[0]), numbers(runs[1]), strict=True))
    assert spread < CONTRACT["absolute_replay_tolerance"], spread
    low, high = runs[-1]["clock_density_packets"]
    deltas = {mode: high[mode]["success"]-low[mode]["success"]
              for mode in ["coherent", "dephased_lobes", "relative_pi_phase",
                           "phase_compensated", "classical_sharp_ensemble"]}
    assert abs(deltas["coherent"]) > 100 * CONTRACT["absolute_replay_tolerance"]
    assert abs(deltas["coherent"]-deltas["dephased_lobes"]) > 100 * CONTRACT["absolute_replay_tolerance"]
    return {"quadrature_inner_outer": CONTRACT["quadrature_inner_outer"], "finest_grid": runs[-1],
            "max_absolute_grid_change": spread, "success_change_high_minus_low": deltas}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write a freshly calculated reference")
    args = parser.parse_args()
    result = compute()
    path = HERE / "clock_packet_results.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    else:
        expected = json.loads(path.read_text())
        np.testing.assert_allclose(list(numbers(result)), list(numbers(expected)),
                                   rtol=0, atol=CONTRACT["absolute_replay_tolerance"])
    print(json.dumps({"max_absolute_grid_change": result["max_absolute_grid_change"],
                      "success_change_high_minus_low": result["success_change_high_minus_low"]}, indent=2))
