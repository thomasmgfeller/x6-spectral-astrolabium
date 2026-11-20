"""Score independent future complex amplitude disks against the registered model prediction."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

from baseline import DENSITIES, HERE, REFERENCE_SHA, TYPES, reference


def rational(value):
    if not isinstance(value, str):
        raise ValueError("A finite rational must be encoded as a JSON string")
    return F(value)


def sqrt_interval(x):
    scale = 10**15
    k = isqrt(x.numerator * scale**2 // x.denominator)
    lo = F(k, scale)
    return lo, lo if lo**2 == x else F(k+1, scale)


def unique_keys(pairs):
    values = {}
    for key, value in pairs:
        if key in values:
            raise ValueError("Duplicate key: " + key)
        values[key] = value
    return values


def classify(intervals):
    if any(lower > F(1,100) for lower, upper in intervals.values()):
        return "FAIL"
    if set(intervals) == set(DENSITIES) and all(upper <= F(1,100) for lower, upper in intervals.values()):
        return "PASS"
    return "HOLD"


def assess(packet, manifest_path=HERE/"registration.json"):
    ref = reference()
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    lock = hashlib.sha256(manifest_bytes).hexdigest()
    if packet["registration_sha256"] != lock or packet["reference_sha256"] != REFERENCE_SHA:
        raise ValueError("Result does not match the frozen registration and reference")
    if not packet.get("method") or not packet.get("error_certificate"):
        raise ValueError("Identify the method and the error certificate")
    if set(packet["densities"]) != set(DENSITIES):
        raise ValueError("A completed run must contain both density rows")
    gram = F(ref["lower_scalar_gram_eigenvalue"])
    if (manifest["decision"]["threshold_ratio"], manifest["decision"]["new_amplitude_radius_max"]) != ("1/100","1/50000"):
        raise ValueError("Unexpected decision parameters")
    intervals = {}
    for k, rho in enumerate(DENSITIES):
        vals = packet["densities"][rho]
        if set(vals) != set(map(str,TYPES)):
            raise ValueError("Require all ten end types")
        lowers, uppers = [], []
        for j in map(str,TYPES):
            item = vals[j]
            radius = rational(item["complex_disk_radius"])
            if not 0 <= radius <= F(1,50000):
                raise ValueError("New amplitude radius outside the registered budget")
            re, im = map(rational,item["complex_center"])
            normlo, normhi = sqrt_interval(re**2+im**2)
            rlo, rhi = map(F, ref["clock_packets_by_end"][j]["modulus_bounds"][k])
            lowers.append((max(F(0),normlo-radius)/rhi)**2)
            uppers.append(((normhi+radius)/rlo)**2)
            control = list(map(rational,item["unmodulated_split_center"]))
            old = [F.from_float(float(x)) for x in ref["clock_packets_by_end"][j]["complex_values"][k]]
            if len(control) != 2 or sum((x-y)**2 for x,y in zip(control,old)) > (radius+F(ref["clock_disk_radius"]))**2:
                raise ValueError("Unmodulated split control disagrees with original disk")
        intervals[rho] = (max(lowers), (2-gram)*max(uppers)/gram)
    return {"status": classify(intervals),"ratio_intervals": {r:[str(x),str(y)] for r,(x,y) in intervals.items()},
            "registration_sha256":lock}


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("input",type=Path)
    path = args.parse_args().input
    packet = json.loads(path.read_text(),object_pairs_hook=unique_keys)
    try:
        result = assess(packet)
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as e:
        result = {"status":"HOLD","reason":str(e)}
    print(json.dumps(result,indent=2))
