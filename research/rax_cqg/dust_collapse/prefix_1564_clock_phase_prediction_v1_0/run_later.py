"""Prospective runner. Execute only when the follow-up evaluation is requested."""
import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zipfile import ZipFile

from baseline import DENSITIES, HERE, REFERENCE_SHA, TYPES, reference


def U6(x):
    return 64*x**6 - 80*x**4 + 24*x*x - 1


def cuts():
    positive = []
    for lo,hi in ((F(1,8), F(1,4)),(F(1,2), F(3,4)),(F(7,8), F(1))):
        if U6(lo)*U6(hi) >= 0:
            raise ValueError("Invalid bracket")
        while hi-lo > F(1,2**50):
            mid = (lo+hi)/2
            if U6(lo)*U6(mid) < 0:
                hi = mid
            else:
                lo = mid
        positive.append((lo+hi)/2)
    return [F(-1), *[-u for u in reversed(positive)], *positive, F(1)]


def kernel_setup(tmp):
    path = HERE/"reference.zip"
    if hashlib.sha256(path.read_bytes()).hexdigest() != REFERENCE_SHA:
        raise ValueError("Incorrect reference")
    with ZipFile(path) as z:
        z.extractall(tmp/"nine")
    with ZipFile(tmp/"nine"/"CST_DUST_Randabbildung_1564_v0_1_Pruefpaket.zip") as z:
        z.extractall(tmp/"boundary")
    sys.path[:0] = [str(tmp/"nine"),str(tmp/"boundary")]
    import boundary
    import clock_integral as clock
    import finite_grid
    return boundary,clock,finite_grid


def encode(z):
    return [str(F.from_float(float(z.real))),str(F.from_float(float(z.imag)))]


def evaluate(manifest_path):
    for env in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS"):
        os.environ[env] = "1"
    import numpy as np
    ref = reference()
    lock = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    result = {"registration_sha256":lock,"reference_sha256":REFERENCE_SHA,
              "method":"Seven phase-constant cells with recomputed archived Gauss rules",
              "error_certificate":"Protocol section on the seven cell error budget; see run and source records",
              "densities":{r:{} for r in DENSITIES}}
    points = cuts()
    with TemporaryDirectory() as work:
        boundary,clock,finite = kernel_setup(Path(work))
        finite.verify_constants(clock.BETA,clock.STEP)
        base_rule = finite.checked_rule
        for j in TYPES:
            code = sum(1<<(6*i+k) for idx,(i,k) in enumerate(combinations(range(6),2)) if j & (1<<idx))
            _,couplings,gravity = boundary.geometry_for(code,6)
            config = ref["clock_packets_by_end"][str(j)]["coordinate_bounds"]
            ns = [config[str(i)]["n"] for i in clock.INNER]
            nout = config["3"]["n"]
            nr = config.get("density",{}).get("n",1)
            a = F(config["3"]["quadratic_bound"])
            b = F(config["3"]["linear_bound"])
            plain = np.zeros(2,dtype=complex)
            modified = np.zeros(2,dtype=complex)
            for k,(left,right) in enumerate(zip(points,points[1:])):
                center,half = (right+left)/2,(right-left)/2
                if half*(b+2*a*abs(center)) > b:
                    raise ValueError("Cell exceeds analytic linear coefficient bound")
                x,w = base_rule(nout)
                mapped = (float(center)+float(half)*x, float(half)*w)
                # A negative sentinel selects only the outer-coordinate rule.
                def cell_rule(n):
                    return mapped if n == -nout else base_rule(n)
                with patch.object(finite,"checked_rule",cell_rule):
                    value = clock.packet(couplings,gravity,ns,-nout,nr,checked=True)
                plain += value
                modified += (-1)**k*value
            for index,rho in enumerate(DENSITIES):
                result["densities"][rho][str(j)] = {
                    "complex_center":encode(modified[index]),
                    "complex_disk_radius":"1/50000",
                    "unmodulated_split_center":encode(plain[index]),
                }
    return result


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    if not __debug__:
        raise SystemExit("Keep the certified reference assertions enabled")
    if args.output.exists():
        raise SystemExit("Choose a fresh result path to preserve earlier runs")
    data = evaluate(HERE/"registration.json")
    with args.output.open("x") as out:
        out.write(json.dumps(data,indent=2)+"\n")
