"""Explicit imports; predecessor files are immutable inputs."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'detector_transfer_v0_9'
sys.path.insert(0, str(PREVIOUS))
import support as previous
from support import check, pack, unpack, gzread, gzwrite, write, sha, digest
from flint import arb, acb, ctx


def plan():
    return json.loads((HERE / 'PROTOCOL.json').read_text())


def freeze_check():
    for name, expected in json.loads((HERE / 'FREEZE.json').read_text())['files'].items():
        check(sha(HERE / name) == expected, 'frozen input: ' + name)


def endpoints(z, exponent):
    """Exact outward integers, never binary64 display values."""
    v = z * (1 << exponent)
    return int(v.lower().floor().unique_fmpz()), int(v.upper().ceil().unique_fmpz())


def ball(lo, hi, exponent=0):
    check(lo <= hi, 'ordered integer endpoints')
    return arb(lo).union(arb(hi)) / (1 << exponent)
