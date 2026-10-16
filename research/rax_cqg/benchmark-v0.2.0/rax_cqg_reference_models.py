"""Explicitly assumed finite quantum clock and classical move references.

Neither reference supplies a QSG model. No unavailable Gmail formulas are
reconstructed. hbar=1; omega sets the inverse clock-parameter unit.
"""
import json
import math
import numpy as np
from rax_cqg_twin import CausalSet, finite_real


def clock_state(tau, omega=1.):
    tau = finite_real(tau, "tau")
    omega = finite_real(omega, "omega", 0)
    if omega <= 0:
        raise ValueError("omega must be positive")
    energies = np.array([-omega/2, omega/2])
    clock_ket = np.exp(-1j*energies*tau)/math.sqrt(2)
    # Bell-type anticorrelated stationary joint state; tensor order clock, system.
    psi = np.array([0, 1, 1, 0], dtype=complex)/math.sqrt(2)
    conditional = clock_ket.conj()@psi.reshape(2, 2)
    overlap_weight = float(np.vdot(conditional, conditional).real)
    conditional /= math.sqrt(overlap_weight)
    return conditional, overlap_weight


def clock_reference(omega=1., samples=33):
    omega = finite_real(omega, "omega", 0)
    if omega <= 0:
        raise ValueError("omega must be positive")
    if isinstance(samples, bool) or not isinstance(samples, int) or not 3 <= samples <= 10000:
        raise ValueError("samples must be an integer from 3 to 10000")
    hs = np.diag([-omega/2, omega/2])
    constraint = np.kron(hs, np.eye(2))+np.kron(np.eye(2), hs)
    joint = np.array([0, 1, 1, 0], dtype=complex)/math.sqrt(2)
    period = 2*math.pi/omega
    dt = 1e-5/omega
    rows = []
    for tau in np.linspace(0, period, samples):
        state, weight = clock_state(float(tau), omega)
        derivative = (clock_state(float(tau+dt), omega)[0]-clock_state(float(tau-dt), omega)[0])/(2*dt)
        expected = np.exp(-1j*np.diag(hs)*tau)/math.sqrt(2)
        rows.append({"tau":float(tau), "overlap_weight":weight,
                     "clock_probability_density":1/period,
                     "p_plus_x":float(abs(state.sum()/math.sqrt(2))**2),
                     "unitary_reference_error":float(np.linalg.norm(state-expected)),
                     "schrodinger_residual":float(np.linalg.norm(1j*derivative-hs@state))})
    return {"schema":"RAX-CQG-CLOCK-REFERENCE-0.2", "model":"assumed_two_qubit_periodic_clock",
            "hbar":1, "omega":omega, "period":period,
            "clock_POVM_density":"E(tau)=(2/period)|tau><tau| on [0,period)",
            "constraint_residual":float(np.linalg.norm(constraint@joint)),
            "derivative_step":dt, "samples":rows,
            "max_unitary_reference_error":max(x["unitary_reference_error"] for x in rows),
            "max_schrodinger_residual":max(x["schrodinger_residual"] for x in rows),
            "scope":"Assumed finite quantum mechanics; periodic clock, no exact canonical CCR; no emergence from the causal-set generator"}


def move_reference():
    matrices = []
    for order in [[(1, 2), (2, 3)], [(2, 3), (1, 2)]]:
        c = CausalSet.from_edges(4, [(0, 1)])
        for edge in order:
            c.add_relation(*edge)
        matrices.append(c.R)
    p0, p1 = np.array([[1, 1], [0, 0]]), np.array([[0, 0], [1, 1]])
    return {"schema":"RAX-CQG-MOVE-REFERENCE-0.2",
            "exact_relation_insertions_commute":bool(np.array_equal(*matrices)),
            "result":matrices[0].tolist(),
            "classical_reset_commutator":(p0@p1-p1@p0).tolist(),
            "QSG_status":"NOT_IMPLEMENTED",
            "scope":"Two separate classical checks; noncommutativity alone is not quantum evidence"}


if __name__ == "__main__":
    print(json.dumps({"clock":clock_reference(), "moves":move_reference()},indent=2,allow_nan=False))
