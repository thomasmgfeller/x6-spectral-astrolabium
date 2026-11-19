"""Verify the finite N15 evidence and optionally rebuild the new numerical inputs."""
from argparse import ArgumentParser
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent

def check_files():
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Input checksum differs: {name}")

def main():
    if not __debug__:
        raise RuntimeError("Run without -O")
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    check_files()
    from basis import HERE, direct_packet
    from uhrtest import MASKS, calculate as clocks
    from volltraeger import both_rounds
    from teiltraeger import extend_gram, certify
    from kontrolle import calculate as individuals
    import numpy as np

    def read(name):
        return json.loads((HERE / name).read_text())

    # Match the rational certificates as data, independent of JSON formatting.
    if json.loads(json.dumps(both_rounds())) != read("volltraeger.json"):
        raise ValueError("Full-support certificate")
    reference = read("teiltraeger.json")
    pilot = certify()
    scalar_checks = reference.pop("scalar_checks")
    stored_residuals = reference.pop("positive_congruence_residuals")
    residuals = pilot.pop("positive_congruence_residuals")
    if max(residuals + stored_residuals) >= 1e-7 or pilot != reference:
        raise ValueError("Pilot certificate")
    direct = read("einzeltests.json")
    for tag, rows in individuals().items():
        for mask, metrics in rows.items():
            for metric, value in metrics.items():
                if not np.allclose(value, direct[tag][mask][metric], rtol=0, atol=1e-13):
                    raise ValueError((tag, mask, metric))
    # Repeat the small independent seven-clock actions and compare both densities.
    from basis import build, layout, tails
    from unittest.mock import patch
    recorded = read("uhren.json")
    with TemporaryDirectory() as tmp, patch.object(tails.prior.growth, "layout", layout):
        lib = build(tmp)
        for mask in MASKS:
            key = (7, mask)
            if max(abs(tails.packet(key, 4, 3, lib) - direct_packet(key))) >= 1e-13:
                raise ValueError(("small independent clock control", mask))
    print("PASS: input checksums, both 1217-state certificates, positive 196-state pilot, four-outcome tests, four direct clock controls.", flush=True)
    if args.rebuild:
        fresh = clocks(MASKS)
        for mask, row in fresh.items():
            for tag, values in row["rows"].items():
                if not np.allclose(values, recorded[mask]["rows"][tag], rtol=0, atol=1e-13):
                    raise ValueError(("New clock differs", mask, tag))
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "gram.npy"
            checked = extend_gram(path)
            if np.max(abs(np.load(path) - np.load(HERE / "gram.npy"))) >= 1e-13:
                raise ValueError("Rebuilt Gram matrices differ")
            if set(checked) != set(scalar_checks):
                raise ValueError("Scalar test membership")
            for name, row in checked.items():
                for metric, value in row.items():
                    if abs(value - scalar_checks[name][metric]) > 1e-15:
                        raise ValueError(("Scalar check differs", name, metric))
        print("PASS: three grids per new type and reconstructed Gram entries.", flush=True)

if __name__ == "__main__":
    main()
