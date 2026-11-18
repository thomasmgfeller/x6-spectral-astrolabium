"""Verify the published bytes and replay both experiments without replacing references."""
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def equivalent(a, b):
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(equivalent(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(equivalent(x, y) for x, y in zip(a, b))
    if type(a) is not type(b):
        return False
    if a == b:
        return True
    if isinstance(a, str):
        try:
            return abs(Decimal(a) - Decimal(b)) <= Decimal("5e-12")
        except InvalidOperation:
            return False
    return False


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    inventory = json.loads((HERE / "SHA256.json").read_text())
    for path, digest in inventory.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "controls"
        shutil.copytree(HERE / "controls", copy)
        (copy / "results.json").unlink()
        subprocess.run([sys.executable, "-B", str(copy / "check.py")], check=True, stdout=subprocess.DEVNULL)
        expected = json.loads((HERE / "controls/results.json").read_text())
        assert equivalent(expected, json.loads((copy / "results.json").read_text())), "scalar replay mismatch"
    subprocess.run([sys.executable, "-B", str(HERE / "clock_packets.py")], check=True)
    print(f"Verified {len(inventory)} file hashes and both numerical replays.")


if __name__ == "__main__":
    main()
