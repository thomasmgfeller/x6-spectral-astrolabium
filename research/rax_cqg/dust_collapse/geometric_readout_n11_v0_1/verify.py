"""Replay the finite N11 geometric readout, using the pinned upstream kernel."""
import argparse
import importlib.util
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
UP = HERE / "inputs" / "initial_preparation_v0_1"
sys.dont_write_bytecode = True


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


contract = read(HERE / "contract.json")
spec = importlib.util.spec_from_file_location("upstream_packets", UP / "clock_packets.py")
packets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packets)
ward = packets.ward
tol = contract["numerical_replay_absolute_tolerance"]


def close(a, b):
    np.testing.assert_allclose(a, b, atol=tol, rtol=0)


def geometry_and_phase():
    u = sp.symbols("u", real=True)
    clocks = [j - 5 for j in range(11)]
    clocks[3] = u  # T3 / Delta, beta * Delta^2 / 2 = 1 / 19
    polynomials, pairs, gravities = [], [], []
    outer = set(ward.PAST + ward.FUTURE)
    common_edges = None
    for removed in ward.ORDERS.values():
        c, gravity = ward.coeffs(removed)
        edges = set(c)
        assert all((i,k) in edges for i,j in edges for h,k in edges if j == h)
        collar_edges = {(i,j) for i,j in edges if i in outer or j in outer}
        if common_edges is not None:
            assert common_edges == collar_edges
        common_edges = collar_edges
        inner_edges = {(i,j) for i,j in edges if i in ward.INNER and j in ward.INNER}
        for perm in itertools.permutations(ward.INNER):
            relabel = dict(zip(ward.INNER, perm))
            assert len({(relabel[i], relabel[j]) for i,j in inner_edges}) == len(inner_edges)
        pairs.append(len(inner_edges))
        past = [(i,j,v) for (i,j),v in c.items() if j in ward.PAST]
        assert all(i in ward.PAST for i,j,v in past)
        B = 4 + sum(v*(clocks[j]-clocks[i])**2 for i,j,v in past) / sp.Integer(19)
        polynomials.append(sp.expand(B))
        gravities.append(gravity)
    assert pairs == [3, 1] and polynomials[0] == polynomials[1]
    assert polynomials[0].subs(u,-2) == sp.Rational(151,19)
    return {"pairs_chain_alternative":pairs,"common_past_polynomial_u_eq_T3_over_Delta":str(polynomials[0]),
            "affine_B": "151/19","gravity_actions":gravities}


def scalar_overlap():
    stored = read(UP / "controls/sources/gaussian_outputs.json")
    mats = [sp.Matrix([[sp.sympify(v) for v in row] for row in b["Omega_scaled_exact"]])
            for b in stored["branches"]]
    real = [m.applyfunc(sp.re) for m in mats]
    for m in real:
        assert all(m[:k,:k].det()>0 for k in (1,2,3))
    joint_det = (mats[0].conjugate() + mats[1]).det()
    s4 = sp.cancel(64 * real[0].det() * real[1].det() / (joint_det * sp.conjugate(joint_det)))
    assert 0 < s4 < 1
    s = complex(*[float(stored["overlap_z_equals_integral_conj_psi0_psi1"][k]) for k in ("re","im")])
    close(abs(s),float(s4**sp.Rational(1,4)))
    return {"magnitude_fourth_power_exact":str(s4),"magnitude":abs(s)}, s


def outcomes(full, projection):
    failure = 1 - sum(full)
    complement = full - projection
    assert min(*projection,*complement,failure) >= 0
    close(sum(projection) + sum(complement) + failure, 1)
    return {"one_pair":float(full[1]),"three_pairs":float(full[0]),"failure":float(failure),
            "one_constant":float(projection[1]),"one_other_modes":float(complement[1]),
            "three_constant":float(projection[0]),"three_other_modes":float(complement[0])}


def run_grid(inner, outer, overlap, gravity):
    params = packets.CONTRACT
    half_r, half_t = params["density_half_width"], params["clock_lobe_half_width"]
    m = 2 * half_r * (2*half_t/3)  # total packet support under the ambient measure
    time_nodes, lobew = packets.quadrature(outer)
    dw_nodes, dw = packets.quadrature(contract["direct_density_quadrature"])
    tw = np.tile(lobew/2, 2)
    clock_grid = packets.quadrature(inner)
    samples = [packets.reduced_weight(-2*ward.DELTA+off+half_t*t,inner,clock_grid)
               for off in params["clock_offsets_from_affine_T3"] for t in time_nodes]
    b = np.array([p[0] for p in samples])
    v = np.array([p[1] for p in samples])
    # Reference changes dust action only: undo and restore each pure gravity phase.
    ref = v[:,[0]] * np.exp(1j*(np.array(gravity)-gravity[0]))
    rows = {}
    diagnostics = {}
    archive = read(UP / "clock_packet_results.json")["finest_grid"]["clock_density_packets"]
    for kernel, values in (("coupled",v),("common_C0_dust",ref)):
        rows[kernel] = {}
        for label, center, old in zip(("low","high"),params["density_centers"],archive,strict=True):
            phase = np.exp(-0.5j*center*b)*np.sinc(half_r*b/(2*np.pi))
            branch_mean = (tw*phase) @ values
            amplitudes = np.sqrt(m)*branch_mean/2
            projected = np.abs(amplitudes)**2
            # Direct integration over density and time, independent form of mode split.
            rr = (center+half_r*dw_nodes)[:,None]
            raw = np.exp(-0.5j*rr*b)[...,None]*values[None,:,:]
            lengths = np.einsum("r,t,rtc->c",dw,tw,np.abs(raw)**2)/4
            close(lengths,(tw @ np.abs(values)**2)/4)
            close(branch_mean,np.einsum("r,t,rtc->c",dw,tw,raw))
            direct_other = (np.einsum("r,t,rtc->c",dw,tw,np.abs(raw-m*branch_mean)**2)
                            + (1-m)*m*np.abs(branch_mean)**2)/4
            close(direct_other,lengths-projected)
            rows[kernel][label] = outcomes(lengths,projected)
            if kernel == "coupled":
                cross = 2*(amplitudes[0].conj()*amplitudes[1]*overlap).real
                coherent_success = float(sum(projected) + cross)
                close(coherent_success,old["coherent"]["success"])
                close(amplitudes[1]/amplitudes[0], complex(*old["W1_over_W0_coherent_re_im"]))
                diagnostics[label] = {"native_scalar_interference":float(cross),
                                      "native_scalar_success":coherent_success}
        low, high = rows[kernel]["low"], rows[kernel]["high"]
        diff = {key:high[key]-low[key] for key in low}
        for key in ("one_pair","three_pairs","failure"):
            close(diff[key],0)
        close(diff["one_constant"],-diff["one_other_modes"])
        rows[kernel]["high_minus_low"] = diff
    effect = {k: rows["coupled"]["high_minus_low"][k] - rows["common_C0_dust"]["high_minus_low"][k]
              for k in rows["coupled"]["low"]}
    return {"runs":rows,"difference_in_differences":effect,"scalar_crosscheck":diagnostics}


def numbers(node):
    if isinstance(node,dict):
        for key in sorted(node):
            yield from numbers(node[key])
    else:
        yield float(node)


def compute():
    geo = geometry_and_phase()
    gram, overlap = scalar_overlap()
    grids = contract["grids_inner_outer"]
    runs = [run_grid(*grid,overlap,geo["gravity_actions"]) for grid in grids]
    gaps = [max(abs(x-y) for x,y in zip(numbers(a),numbers(b),strict=True)) for a,b in zip(runs,runs[1:])]
    # The two fine grids agree; report the coarse-grid diagnostic separately.
    assert gaps[-1] < tol
    return {"geometry":geo,"scalar_gram":gram,"grids":grids,"adjacent_grid_max_abs_changes":gaps,
            "fine_grid":runs[-1],"primary_delta1_delta0_interaction_exact":["0","0","0"],
            "physical_5A":"HOLD"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    opts = parser.parse_args()
    result = compute()
    path = HERE / "results.json"
    if opts.write:
        path.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    else:
        ref = read(path)
        for key in ("geometry","grids","primary_delta1_delta0_interaction_exact","physical_5A","scalar_gram"):
            if key == "scalar_gram":
                assert ref[key]["magnitude_fourth_power_exact"] == result[key]["magnitude_fourth_power_exact"]
                close(ref[key]["magnitude"],result[key]["magnitude"])
            else:
                assert ref[key] == result[key]
        close(list(numbers(result["fine_grid"])),list(numbers(ref["fine_grid"])))
        close(result["adjacent_grid_max_abs_changes"],ref["adjacent_grid_max_abs_changes"])
    print(json.dumps(result,indent=2))
