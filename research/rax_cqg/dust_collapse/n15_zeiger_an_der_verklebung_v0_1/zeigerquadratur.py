"""Integrate the proposed local instrument across the two original broad windows."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/"quellen"))
from modell import ORDER, INNER, PAST, FUTURE, clocks, dwell
from quadratur import DELTA, average, coefficients, rule

RHO = (("1/8", 0.125), ("1/4", 0.25))


def integrate(method, n, k):
    x, _ = rule(n, method)
    u = [(idx+1)/8 + x.reshape((1,)*idx+(n,)+(1,)*(6-idx))/64 for idx in range(7)]
    f = dwell(u)
    norms = 0.0
    positive_spin = 0.0
    totals = {key: np.zeros(3, dtype=complex) for key, _ in RHO}
    for centre in (-1/16, 1/16):
        for coordinate, weight in zip(*rule(k, method)):
            offset = centre + coordinate/32
            e, duration = offset/DELTA, 4*DELTA-offset
            y = clocks(e, u)
            c = coefficients(y, None, 0, method)
            # Target 11 is closed here. Directly re-evaluate each incoming square on Gauss.
            arm_c = []
            gap = y[4]-y[3]
            for sign in (-1, 0, 1):
                c11 = c[11]
                if sign and method == "gauss":
                    shift = -sign/(256*duration*(gap+np.sqrt(gap*gap+sign/(256*duration))))
                    c11 = -.5
                    for i, b in zip((3, 4, 5, 6), (-8, 16, -9, 1)):
                        old = y[i] + {3: 2, 4: 1}.get(i, 0)*shift
                        c11 = c11 - (b/38)*(y[11]-old)**2
                elif sign:
                    c11 = c11 + sign/(608*duration)
                arm_c.append(c11)
            scale = weight*duration**14/2
            base = [8*f[j] for j in INNER]
            norms += scale*average(base, n, method).real
            positive_spin += scale*average(base + [np.sin(f[11]/304)*np.sinc(f[11]/(30400*np.pi))], n, method).real
            cpast, cfuture = sum(c[j] for j in PAST), sum(c[j] for j in FUTURE)/8
            for pos, coef in enumerate(arm_c):
                factors = [np.exp(1j*cfuture)*np.sinc(cpast/(32*np.pi))]
                for j in INNER:
                    theta = duration*f[j]*(coef if j == 11 else c[j])
                    factors.append(8*f[j]*np.exp(1j*theta)*np.sinc(theta/(100*np.pi)))
                reduced = scale*average(factors, n, method)
                for key, rho in RHO:
                    totals[key][pos] += reduced*np.exp(1j*rho*cpast)
    original = json.loads((ROOT/"quellen/auslese.json").read_text())[f"1|{method}{n}x{k}"]
    result = {"positive_bit": (1+positive_spin/norms)/2}
    for key, _ in RHO:
        minus, ref, plus = totals[key]/norms
        baseline = complex(*original[key+"|0"]["amplituden"]["null"]["ref"])
        if abs(ref-baseline) > 1e-12:
            raise ValueError("Nullamplitude stimmt nicht mit PR 361 überein")
        # Balanced arms and a common coherent dust-endpoint projection.
        probability = abs(plus+1j*minus)**2/(2*(abs(plus)**2+abs(minus)**2))
        result[key] = {"endpoint_bit": probability, "relative_phase": float(np.angle(plus*minus.conjugate())),
                       "real_imag_arms": [[v.real, v.imag] for v in (minus, ref, plus)]}
    return result


def compute():
    data = {method: integrate(method, 5, k) for method, k in (("gauss", 10), ("cc", 9))}
    for key, _ in RHO:
        for field in ("endpoint_bit", "relative_phase", "real_imag_arms"):
            if np.max(np.abs(np.array(data["gauss"][key][field])-data["cc"][key][field])) > 2e-11:
                raise ValueError("Verfahrensvergleich: "+field)
    if abs(data["gauss"]["positive_bit"]-data["cc"]["positive_bit"]) > 2e-11:
        raise ValueError("Positives Referenzmass")
    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    data = compute()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        ref = json.loads((ROOT/"quadratur.json").read_text())
        for method, values in data.items():
            if abs(values["positive_bit"]-ref[method]["positive_bit"])>2e-11:
                raise ValueError("Archivierter positiver Zeigerwert")
            for key, _ in RHO:
                for field, value in values[key].items():
                    if np.max(np.abs(np.array(value)-ref[method][key][field]))>2e-11:
                        raise ValueError("Archivierter Wert: "+field)
        print("PASS · Gauss-Legendre, Clenshaw-Curtis und Nullamplituden aus PR 361")
