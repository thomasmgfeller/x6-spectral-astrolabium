"""Repeat the action and packet integration on a preselected finite N14 pilot."""
import argparse
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

if __name__ == "__main__":
    for variable in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
        os.environ[variable] = "1"

import numpy as np
from growth import layout

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "upstream" / "v03"))
import clock_network as reference

MAX_BRANCHES = 8
GRIDS = ((32, 6), (48, 8), (64, 10), (80, 12))
STOP = 2e-12


def flat(packet):
    lobes, compensated, (_, fixed) = packet
    return np.r_[lobes.ravel(), compensated, fixed]


def direct_grid(key, t, n):
    """Evaluate the full n^6 tensor from the action before variable elimination."""
    inner, coefficients, gravity = layout(key)
    assert len(inner) == 6
    p, f = reference.geometry.P, reference.geometry.F
    beta, step = reference.BETA, reference.STEP
    nodes, weights = np.polynomial.legendre.leggauss(n)
    times = {j: (j - 5) * step for j in (*p, *f)}
    times[3] = t
    quadrature_weights = 1.0
    for axis, j in enumerate(inner):
        shape = [1] * 6
        shape[axis] = n
        times[j] = (1.5 * nodes).reshape(shape)
        quadrature_weights = quadrature_weights * (weights / 2).reshape(shape)

    def density_argument(j):
        return 1 + beta / 2 * sum(c * (times[j] - times[i]) ** 2
                                  for (i, k), c in coefficients.items() if k == j and c)

    result = quadrature_weights * np.exp(1j * (gravity - sum(density_argument(j) for j in f) / 16))
    for j in inner:
        c = density_argument(j)
        result *= (1 + np.exp(-0.25j * c) * np.sinc(c / (4 * np.pi))) / 2
    return sum(density_argument(j) for j in p), result.sum()


def direct_packet(key, n, m):
    """Integrate both lobes on the direct six-axis grid, including fixed-clock control."""
    nodes, weights = np.polynomial.legendre.leggauss(m)
    mid = -2 * reference.STEP
    lobes = np.zeros((2, 2), dtype=complex)
    compensated = 0j
    for side, offset in enumerate((-1 / 16, 1 / 16)):
        for node, weight in zip(nodes, weights):
            past, amplitude = direct_grid(key, mid + offset + node / 32, n)
            contribution = weight / (2 * np.sqrt(32 * 48)) * amplitude
            compensated += contribution / np.sqrt(2)
            for density, rho in enumerate(reference.RHO):
                phase = np.sinc(past / (64 * np.pi)) * np.exp(-0.5j * rho * past)
                lobes[density, side] += contribution * phase
    return lobes, compensated, direct_grid(key, mid, n)


def choose(widths):
    """Cost-only rule. Mask order is the published canonical convention."""
    inexpensive = sorted((w, k) for k, w in widths.items() if w <= 3)
    if inexpensive:
        return [k for _, k in inexpensive[:MAX_BRANCHES]]
    medium = [k for k, w in widths.items() if w == 4]
    return [min(medium)] if medium else []


def evaluate(key, width):
    direct = direct_packet(key, 4, 3)
    eliminated = reference.packet(key, 4, 3)
    direct_t = -2 * reference.STEP + 1 / 16
    point = abs(direct_grid(key, direct_t, 4)[1] - reference.clock_value(key, direct_t, 4)[1])
    packet_error = max(abs(flat(eliminated) - flat(direct)))
    past_error = abs(eliminated[2][0] - direct[2][0])
    assert max(point, packet_error, past_error) < 2e-13, (key, point, packet_error, past_error)
    rows = []
    previous = None
    for n, m in GRIDS:
        values = reference.packet(key, n, m)
        current = flat(values)
        row = {"grid": [n, m], "amplitudes": reference.encode(values)}
        rows.append(row)
        if previous is not None:
            change = float(np.max(np.abs(current - previous)))
            row["max_amplitude_change"] = change
            if change < STOP:
                break
        previous = current
    else:
        raise ArithmeticError(f"Clock grid did not converge within the pilot budget for {key}")
    # Holding one quadrature fixed guards against cancellation when both are refined.
    (nc, mc), (nf, mf) = (r["grid"] for r in rows[-2:])
    cc, ff = (flat(reference.decode(r["amplitudes"])) for r in rows[-2:])
    cf = flat(reference.packet(key, nc, mf))
    fc = flat(reference.packet(key, nf, mc))
    crossed = {
        "outer_change_at_coarse_inner": float(max(abs(cf - cc))),
        "outer_change_at_fine_inner": float(max(abs(ff - fc))),
        "inner_change_at_coarse_outer": float(max(abs(fc - cc))),
        "inner_change_at_fine_outer": float(max(abs(ff - cf))),
    }
    assert max(crossed.values()) < STOP, (key, crossed)
    return {"width": width, "crossed_grid_changes": crossed, "low_grid": [4, 3], "direct_point_error": float(point),
            "direct_packet_error": float(packet_error), "past_phase_argument_error": float(past_error),
            "grids": rows}


def run(growth, remaining_width3=False):
    with patch.object(reference, "layout", layout):
        masks = growth["sequential_admissible"]
        widths = {mask: reference.scheme((6, mask))[0] for mask in masks}
        selected = choose(widths)
        if remaining_width3:
            selected = sorted(k for k, w in widths.items() if w == 3 and k not in selected)
        rows = {}
        for mask in selected:
            rows[f"N14_{mask}"] = evaluate((6, mask), widths[mask])
            print(f"N14_{mask}  {rows[f'N14_{mask}']['grids'][-1]['grid']}", flush=True)
    return {"widths": {f"N14_{mask}": width for mask, width in sorted(widths.items())},
            "selection": selected, "branches": rows}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run with assertions enabled")
    parser = argparse.ArgumentParser()
    parser.add_argument("growth", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--remaining-width3", action="store_true",
                        help="Compute the supplemental width-three branches excluded by the pilot cap.")
    args = parser.parse_args()
    result = run(json.loads(args.growth.read_text()), args.remaining_width3)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
