"""Classical Gaussian graph-field reference, RAX-CQG 0.2.

This is a stable finite Euclidean graph model, not Lorentzian matter,
entanglement geometry or an emergent quantum field theory.
S(phi)=1/2 sum_a phi_a^T Q phi_a, Q=mass^2 I+coupling L.
mass>0 and coupling>=0 ensure positive definiteness on every finite graph.
"""
import json
import math
import numpy as np
from rax_cqg_twin import PCG32, CausalSet, diagnose, finite_real, generate, integer


class ClassicalGraphField:
    def __init__(self, causal_set, mass=1.2, coupling=0.6, internal_dim=4):
        if not isinstance(causal_set, CausalSet):
            raise ValueError("causal_set must be a CausalSet")
        self.cs = causal_set
        self.mass = finite_real(mass, "mass", 0)
        if not self.mass > 0:
            raise ValueError("mass must be strictly positive")
        self.coupling = finite_real(coupling, "coupling", 0)
        self.internal_dim = integer(internal_dim, "internal_dim", 1, 128)
        h = causal_set.R + causal_set.R.T
        self.laplacian = np.diag(h.sum(axis=1))-h
        try:
            with np.errstate(over='raise', invalid='raise'):
                self.Q = self.mass**2*np.eye(causal_set.size) + self.coupling*self.laplacian
        except (OverflowError, FloatingPointError) as exc:
            raise ValueError('parameters exceed the finite floating-point range') from exc
        if not np.all(np.isfinite(self.Q)):
            raise ValueError('precision matrix is nonfinite')
        self.cholesky = np.linalg.cholesky(self.Q)

    def action(self, phi):
        field = np.asarray(phi, dtype=float)
        if field.shape != (self.cs.size, self.internal_dim) or not np.all(np.isfinite(field)):
            raise ValueError("phi has wrong shape or nonfinite entries")
        return float(0.5*np.sum(field*(self.Q@field)))

    def sample(self, seed=104729):
        rng = PCG32(seed)
        z = np.array([rng.normal() for _ in range(self.cs.size*self.internal_dim)])
        z = z.reshape(self.cs.size, self.internal_dim)
        return np.linalg.solve(self.cholesky.T, z)

    def diagnostics(self, seed=104729):
        phi = self.sample(seed)
        n = self.cs.size
        logdet = float(2*np.log(np.diag(self.cholesky)).sum())
        return {"model":"classical_euclidean_gaussian_graph_field", "schema":"RAX-CQG-FIELD-0.2",
                "mass":self.mass, "coupling":self.coupling, "internal_dim":self.internal_dim,
                "field_seed":seed, "precision":"Q=mass^2 I+coupling*(D-H)",
                "min_precision_eigenvalue":float(np.linalg.eigvalsh(self.Q)[0]) if n else None,
                "analytic_lower_bound":self.mass**2,
                "action":self.action(phi), "phi":phi.tolist(),
                "log_partition":self.internal_dim*(n*math.log(2*math.pi)-logdet)/2,
                "graph_metrics":diagnose(self.cs),
                "limitations":["classical reference only", "orientation discarded in graph coupling",
                               "no entanglement, causal propagation or feedback on the order"]}


if __name__ == "__main__":
    cs, _ = generate("minkowski_4d", 30, 42)
    print(json.dumps(ClassicalGraphField(cs).diagnostics(), indent=2, allow_nan=False))
