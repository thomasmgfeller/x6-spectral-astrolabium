"""Calculate only the prospective envelope from the locked unmodulated run."""
import hashlib
import json
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
REFERENCE_SHA = "05968e2c6afeb263c66faa15255e1499b7cd6a90a6ff2b6510fd6b48cbc4c1c5"
TYPES = (766, 926, 990, 1790, 2013, 2014, 2015, 5374, 5566, 27006)
DENSITIES = ("1/8", "1/4")


def reference():
    filename = HERE / "reference.zip"
    if hashlib.sha256(filename.read_bytes()).hexdigest() != REFERENCE_SHA:
        raise ValueError("Reference digest mismatch")
    with ZipFile(filename) as package:
        record = json.loads(package.read("result.json"))
    if record["prefix"] != 1564 or set(record["clock_packets_by_end"]) != set(map(str, TYPES)):
        raise ValueError("Unexpected reference sector")
    return record


def certificate():
    ref = reference()
    gram_lo = F(ref["lower_scalar_gram_eigenvalue"])
    gram_hi = 2 - gram_lo  # Unit diagonal, same maximum off-diagonal row sum
    if gram_lo != F(3220693, 5000000):
        raise ValueError("Unexpected Gram bound")
    maxima = {}
    by_density = {}
    for index, rho in enumerate(DENSITIES):
        by_type = {}
        for j in TYPES:
            row = ref["clock_packets_by_end"][str(j)]
            coordinate = row["coordinate_bounds"]["3"]
            a = F(coordinate["quadratic_bound"])
            b = F(coordinate["linear_bound"])
            zlo = F(row["modulus_bounds"][index][0])
            if a < 0 or b < 0 or zlo <= 0:
                raise ValueError("Invalid input bound")
            # Bound sup |f^(6)|/6! for f(u)=exp(i(au^2+bu+c)).
            derivative_over_factorial = sum(
                a**k * (2*a + b)**(6-2*k) / (factorial(k) * factorial(6-2*k))
                for k in range(4)
            )
            # The mean absolute monic interpolation polynomial has norm 1/64.
            # Squared sum of the two lobe normalizations is (2/sqrt(3072))^2.
            new_modulus_squared_cap = (derivative_over_factorial / 64)**2 / 768
            by_type[str(j)] = new_modulus_squared_cap / zlo**2
        limiting = max(by_type, key=by_type.get)
        bound = gram_hi * by_type[limiting] / gram_lo
        if bound >= F(3,400):
            raise ValueError("The declared analytical margin does not follow")
        maxima[rho] = {"limiting_end_type": int(limiting), "ratio_upper": str(bound)}
        by_density[rho] = {j: str(q) for j, q in by_type.items()}
    return {
        "source_sha256": REFERENCE_SHA,
        "gram_lower": str(gram_lo), "gram_upper": str(gram_hi),
        "single_type_squared_ratio_bounds": by_density,
        "all_weight_upper_bounds": maxima,
        "target_datapoints_read": 0,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
