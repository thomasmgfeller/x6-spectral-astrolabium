"""Validate the sealed design, reference-only bounds, and synthetic controls."""
import hashlib
import json
from fractions import Fraction as F
from unittest.mock import patch

from baseline import HERE, DENSITIES, TYPES, certificate, reference
import run_later
import score


def verify():
    manifest_path = HERE/"registration.json"
    locked = json.loads(manifest_path.read_bytes())
    for name,expected in locked["frozen_files_sha256"].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != expected:
            raise ValueError("Frozen file mismatch: " + name)
    if json.loads((HERE/"certificate.json").read_bytes()) != certificate():
        raise ValueError("Reference-only certificate mismatch")
    points = run_later.cuts()
    for k in range(6):
        signed = sum((-1)**i*(b**(k+1)-a**(k+1))/(2*(k+1))
                     for i,(a,b) in enumerate(zip(points,points[1:])))
        if abs(signed)>F(6,2**51):
            raise ValueError("Polynomial moment control failed")
    if score.classify({r:(F(0),F(1,100)) for r in DENSITIES}) != "PASS":
        raise ValueError("Equality is accepted")
    if score.classify({r:(F(1,100),F(11,1000)) for r in DENSITIES}) != "HOLD":
        raise ValueError("Interval crossing is unresolved")
    if score.classify({r:(F(11,1000),F(12,1000)) for r in DENSITIES}) != "FAIL":
        raise ValueError("Strict contradiction is rejected")
    # The numerical pipeline is exercised only on a synthetic polynomial. This
    # test substitutes the entire physical kernel and supplies its own clock rule.
    import numpy as np
    from types import SimpleNamespace
    def simple_gauss(n):
        nodes,weights = np.polynomial.legendre.leggauss(n)
        return nodes,weights/2
    fake_grid = SimpleNamespace(checked_rule=simple_gauss,verify_constants=lambda *args:None)
    def synthetic_packet(couplings,gravity,ns,nout,nr,checked):
        nodes,weights = fake_grid.checked_rule(nout)
        value = weights @ (1+nodes**2+nodes**4)
        return np.array([value,2*value],dtype=complex)
    fake_boundary = SimpleNamespace(geometry_for=lambda *args:(None,{},0))
    fake_clock = SimpleNamespace(BETA=1,STEP=1,INNER=(4,5,6,11,12,13),packet=synthetic_packet)
    with patch.object(run_later,"kernel_setup",return_value=(fake_boundary,fake_clock,fake_grid)):
        synthetic = run_later.evaluate(manifest_path)
    for idx,rho in enumerate(DENSITIES,1):
        for entry in synthetic["densities"][rho].values():
            val = list(map(F,entry["complex_center"]))
            positive = list(map(F,entry["unmodulated_split_center"]))
            if max(map(abs,val)) > F(1,10**12) or abs(positive[0]-idx*F(23,15)) > F(1,10**12):
                raise ValueError("Synthetic split/merge failed")
    # Exercise the scorer on a fabricated zero target. Only the baseline controls
    # come from the historical file, and nothing is written as a target result.
    ref = reference()
    for idx,rho in enumerate(DENSITIES):
        for j in map(str,TYPES):
            entry = synthetic["densities"][rho][j]
            entry["complex_center"] = ["0","0"]
            entry["unmodulated_split_center"] = [str(F.from_float(float(x))) for x in
                ref["clock_packets_by_end"][j]["complex_values"][idx]]
    if score.assess(synthetic)["status"] != "PASS":
        raise ValueError("Synthetic scorer test failed")
    print("Registration verified. Only reference data and synthetic polynomials used.")


if __name__ == "__main__":
    verify()
