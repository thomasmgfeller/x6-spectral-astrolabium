"""Boundary impulse targets and the stationary residuals used throughout."""
from contextlib import contextmanager
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json
import sys

ROOT = Path(__file__).resolve().parent
LATE = (7, 8, 9, 10)
PIN = "4a30c59e83c3465983c69f295a01145a91de1877e2d4bdbc72f93371a7cba11a"


@contextmanager
def inputs():
    archive = ROOT / "basis/Zukunftsrandwerte.zip"
    assert sha256(archive.read_bytes()).hexdigest() == PIN
    with TemporaryDirectory() as work, ZipFile(archive) as package:
        package.extractall(work)
        sys.path.insert(0, work)
        from zukunftsbasis import inputs as published_inputs
        previous = json.loads((Path(work) / "Ergebnisse.json").read_text())
        with published_inputs() as data:
            yield previous, data


def midpoint(state):
    return [[sum(map(F, pair))/2 for pair in state[key]] for key in ("y", "w")]


def edge_flows(y, w, edges):
    # Multiply each edge contribution once and add it with opposite signs.
    current = [y[0]*0 for _ in y]
    for i, j, coefficient in edges:
        flow = coefficient*w[j]*(y[j]-y[i])
        current[i] += flow
        current[j] -= flow
    return current


def targets(previous, edges, goals):
    reference, = (r for r in previous["witnesses"]
                  if F(r["source"]) == 0 and r["fixed"] == ["y10", "w10"])
    currents = edge_flows(*midpoint(reference), edges)
    assert sum(currents) == 0
    late = {i: round(currents[i], 15) for i in LATE[:-1]}
    late[10] = -sum(goals[1:])-sum(late.values())
    return late


def system(y, w, source, coeff, free, axes, goals, selected, target, cast):
    from impulsfelder import fields
    from feldroehre import POS
    values, jac, flows = fields(y, w, source, coeff, [*free, *selected], axes, goals, cast)
    start = len(POS)+len(free)
    for position, node in enumerate(selected, start):
        values[position] -= target[node]
    return values, jac, flows


def variables(free):
    from feldroehre import POS
    from zukunftsbasis import FUTURE
    return [("y", i) for i in free]+[("w", i) for i in POS]+list(FUTURE)
