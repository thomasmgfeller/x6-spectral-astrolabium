"""RAX-CQG Causal-Set Benchmark 0.2.0.

Finite, reproducible order/graph diagnostics. No quantum-gravity validation.
The 4D BDG bracket B4=N-N0+9*N1-16*N2+8*N3 omits dimensional prefactors.
Nk counts open order intervals with k interior elements, including links N0.
See MODEL_CONTRACT.md for conventions, limits and evidence boundaries.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import numbers
from pathlib import Path
from typing import Iterable

import numpy as np

VERSION = "0.2.0"
MAX_SIZE = 512
MODELS = ("chain", "antichain", "percolation", "three_layer", "minkowski_2d", "minkowski_4d")


def integer(value, name, low=0, high=MAX_SIZE):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be an integer")
    value = int(value)
    if not low <= value <= high:
        raise ValueError(f"{name} must lie in [{low}, {high}]")
    return value


def finite_real(value, name, low=None, high=None):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise ValueError(f"{name} must be a real number")
    value = float(value)
    if not math.isfinite(value) or (low is not None and value < low) or (high is not None and value > high):
        raise ValueError(f"invalid {name}")
    return value


class PCG32:
    """Local PCG-XSH-RR 64/32 stream; portable contract, not cryptographic.

    Algorithm: M. E. O'Neill, pcg-random.org. See THIRD_PARTY_NOTICES.txt.
    Fixed default stream 54; seed 0..2**32-1. uniform() returns (x+0.5)/2**32.
    """
    def __init__(self, seed=42, stream=54):
        seed = integer(seed, "seed", 0, 2**32-1)
        stream = integer(stream, "stream", 0, 2**32-1)
        self.state = 0
        self.inc = (stream << 1) | 1
        self.next_uint32()
        self.state = (self.state + seed) & ((1 << 64)-1)
        self.next_uint32()

    def next_uint32(self):
        old = self.state
        self.state = (old*6364136223846793005 + self.inc) & ((1 << 64)-1)
        word = (((old >> 18) ^ old) >> 27) & 0xffffffff
        rot = old >> 59
        return ((word >> rot) | (word << ((-rot) & 31))) & 0xffffffff

    def uniform(self):
        return (self.next_uint32()+0.5)/4294967296.0

    def normal(self):
        # Fixed two draws per call, no hidden cached state.
        return math.sqrt(-2*math.log(self.uniform()))*math.cos(2*math.pi*self.uniform())


def transitive_closure(matrix):
    r = np.array(matrix, dtype=bool, copy=True)
    for k in range(len(r)):
        r |= r[:, k, None] & r[None, k, :]
    return r


class CausalSet:
    """Strict partial order. Public R is a copy; edits go through checked methods."""
    def __init__(self, size=0):
        self.size = integer(size, "size")
        self._r = np.zeros((self.size, self.size), dtype=bool)

    @property
    def R(self):
        return self._r.astype(np.int64, copy=True)

    @classmethod
    def from_matrix(cls, matrix):
        raw = np.asarray(matrix)
        if raw.shape == (0,):
            raw = np.empty((0, 0), dtype=int)
        if raw.ndim != 2 or raw.shape[0] != raw.shape[1]:
            raise ValueError("relation matrix must be square")
        c = cls(raw.shape[0])
        if not np.all((raw == 0) | (raw == 1)):
            raise ValueError("relation matrix must be binary")
        r = raw.astype(bool)
        closure = transitive_closure(r)
        if np.any(np.diag(closure)):
            raise ValueError("strict order must be irreflexive and acyclic")
        if not np.array_equal(r, closure):
            raise ValueError("matrix must already be transitive; use from_edges for a DAG")
        c._r = r.copy()
        return c

    @classmethod
    def from_edges(cls, size, edges: Iterable[tuple[int, int]]):
        c = cls(size)
        for i, j in edges:
            c.add_relation(i, j)
        return c

    def add_relation(self, i, j):
        i = integer(i, "i", 0, self.size-1)
        j = integer(j, "j", 0, self.size-1)
        if i == j or self._r[j, i]:
            raise ValueError("relation would introduce a cycle")
        ancestors = self._r[:, i].copy(); ancestors[i] = True
        descendants = self._r[j, :].copy(); descendants[j] = True
        self._r |= ancestors[:, None] & descendants[None, :]

    def set_random_poset(self, p=0.25, seed=42):
        self._r = generate("percolation", self.size, seed, p)[0]._r.copy()

    def interval_histogram(self):
        r = self.R
        interiors = (r @ r)[self._r]
        if not len(interiors):
            return []
        return np.bincount(interiors).astype(int).tolist()

    def link_matrix(self):
        r = self.R
        return self._r & ((r @ r) == 0)

    def height(self):
        if not self.size:
            return 0
        # Number of ancestors strictly increases along every order relation.
        order = np.argsort(self._r.sum(axis=0), kind="stable")
        depth = np.ones(self.size, dtype=int)
        for j in order:
            preds = np.flatnonzero(self._r[:, j])
            if len(preds):
                depth[j] = int(depth[preds].max())+1
        return int(depth.max())

    def induced(self, indices):
        ids = [integer(i, "subset index", 0, self.size-1) for i in indices]
        if len(ids) != len(set(ids)):
            raise ValueError("subset indices must be unique")
        return CausalSet.from_matrix(self._r[np.ix_(ids, ids)])

    def rows(self):
        return ["".join("1" if v else "0" for v in row) for row in self._r]

    def digest(self):
        # Includes N; trailing LF after each row. Same format can be hashed in any language.
        text = str(self.size)+"\n"+"".join(row+"\n" for row in self.rows())
        return hashlib.sha256(text.encode("ascii")).hexdigest()


class BDGAction:
    """4D interval combination only; no fitted alpha or asserted curvature limit."""
    @staticmethod
    def bracket_4d(causal_set):
        counts = causal_set.interval_histogram()
        return causal_set.size + sum(coef*(counts[k] if k < len(counts) else 0)
                                     for k, coef in enumerate((-1, 9, -16, 8)))

    compute = bracket_4d


def sample_diamond_points(size, dimension, rng):
    size = integer(size, "sample size", 0, 1000000)
    if dimension not in (2, 4):
        raise ValueError("only dimensions 2 and 4 are implemented")
    points = []
    for _ in range(size):
        if dimension == 2:
            u, v = rng.uniform(), rng.uniform()
            points.append([(u+v)/2-0.5, (v-u)/2])
        else:
            u = rng.uniform()
            t = -0.5+0.5*(2*u)**0.25 if u < 0.5 else 0.5-0.5*(2*(1-u))**0.25
            radius = (0.5-abs(t))*rng.uniform()**(1/3)
            z = 2*rng.uniform()-1
            angle = 2*math.pi*rng.uniform()
            transverse = math.sqrt(max(0., 1-z*z))
            points.append([t, radius*transverse*math.cos(angle),
                           radius*transverse*math.sin(angle), radius*z])
    return np.asarray(points, dtype=float).reshape(size, dimension)


def generate(model="percolation", size=30, seed=42, p=0.25):
    n = integer(size, "size")
    seed = integer(seed, "seed", 0, 2**32-1)
    p = finite_real(p, "p", 0, 1)
    if model not in MODELS:
        raise ValueError(f"unknown model {model}")
    rng = PCG32(seed)
    r = np.zeros((n, n), dtype=bool)
    metadata = {"model":model, "size":n, "seed":seed,
                "rng":"PCG-XSH-RR-64-32", "stream":54, "version":VERSION,
                "uniform":"(uint32+0.5)/2**32", "p":p if model in ("percolation", "three_layer") else None}
    if model == "chain":
        r = np.triu(np.ones((n, n), dtype=bool), 1)
    elif model == "percolation":
        for i in range(n):
            for j in range(i+1, n):
                r[i, j] = rng.uniform() < p
        r = transitive_closure(r)
    elif model == "three_layer":
        if n < 4:
            raise ValueError("three_layer requires N>=4")
        a, b = n//4, n//2
        layers = [list(range(a)), list(range(a, a+b)), list(range(a+b, n))]
        for lower, upper in zip(layers, layers[1:]):
            for i in lower:
                for j in upper:
                    r[i, j] = rng.uniform() < p
        r = transitive_closure(r)
        metadata.update(layer_sizes=[len(x) for x in layers],
                        ensemble_note="Independent adjacent-layer edges; fixed labels; not a uniform sample of all KR orders")
    elif model.startswith("minkowski_"):
        dim = 2 if model == "minkowski_2d" else 4
        pts = sample_diamond_points(n, dim, rng)
        for i in range(n):
            for j in range(n):
                dt = pts[j, 0]-pts[i, 0]
                ds2 = sum((float(pts[j, k])-float(pts[i, k]))**2 for k in range(1, dim))
                r[i, j] = dt > 0 and dt*dt >= ds2
        metadata.update(dimension=dim, coordinates=pts.tolist(),
                        diamond_endpoints=[[-0.5]+[0.]*(dim-1), [0.5]+[0.]*(dim-1)],
                        volume=0.5 if dim == 2 else math.pi/24,
                        sampling="Uniform spacetime volume conditioned on fixed N; N is not Poisson sampled",
                        causal_comparison="float64 dt>0 and dt^2>=sum(dx^2); no tolerance or closure repair")
    return CausalSet.from_matrix(r), metadata


def diagnose(causal_set):
    n = causal_set.size
    r = causal_set.R
    h = (r+r.T).astype(float)
    m = int(r.sum())
    hist = causal_set.interval_histogram()
    eig = np.linalg.eigvalsh(h) if n else np.empty(0)
    lap = np.diag(h.sum(axis=1))-h
    leig = np.linalg.eigvalsh(lap) if n else np.empty(0)
    entropy = None
    if m:
        weights = eig*eig/(2*m)
        entropy = float(-np.sum(weights[weights > 0]*np.log(weights[weights > 0])))
    triangles = int(np.trace((r+r.T)@(r+r.T)@(r+r.T))//6)
    return {
        "size":n, "relations":m, "links":hist[0] if hist else 0,
        "ordering_fraction":2*m/(n*(n-1)) if n > 1 else 0.,
        "height":causal_set.height(), "interval_counts":hist,
        "bdg4_bracket":BDGAction.bracket_4d(causal_set),
        "adjacency_spectrum":eig.tolist(), "laplacian_spectrum":leig.tolist(),
        "spectral_radius":float(np.max(np.abs(eig))) if n else 0.,
        "adjacency_spectral_width":float(eig[-1]-eig[0]) if n else 0.,
        "algebraic_connectivity":max(0., float(leig[1])) if n > 1 else None,
        "h2_spectral_entropy":entropy,
        "adjacency_spectral_std":math.sqrt(2*m/n) if n else 0.,
        "triangles":triangles,
        "triangles_per_vertex":triangles/n if n else 0.,
    }


def experiment(model="percolation", size=30, seed=42, p=0.25):
    c, meta = generate(model, size, seed, p)
    return {"schema":"RAX-CQG-EXPERIMENT-0.2", "software_version":VERSION,
            "evidence_class":"FINITE_ORDER_BENCHMARK", "generator":meta,
            "relation_rows":c.rows(), "relation_sha256":c.digest(), "metrics":diagnose(c)}


def load_experiment(record):
    if record.get("schema") != "RAX-CQG-EXPERIMENT-0.2":
        raise ValueError("unsupported experiment schema")
    rows = record.get("relation_rows")
    if not isinstance(rows, list) or any(not isinstance(x, str) for x in rows):
        raise ValueError("relation_rows must be a list of bit strings")
    n = integer(len(rows), "size")
    if any(len(row) != n or set(row)-set("01") for row in rows):
        raise ValueError("invalid relation row")
    c = CausalSet.from_matrix([[int(x) for x in row] for row in rows])
    if record.get("relation_sha256") not in (None, c.digest()):
        raise ValueError("matrix hash mismatch")
    # Never trust stored diagnostics: callers recompute with diagnose(c).
    return c


def thinning_path(causal_set, retention=0.75, steps=4, seed=104729):
    q = finite_real(retention, "retention", 0, 1)
    steps = integer(steps, "steps", 0, 20)
    rng = PCG32(seed)
    ids = list(range(causal_set.size))
    path = []
    for step in range(steps+1):
        subset = causal_set.induced(ids)
        path.append({"step":step, "original_indices":ids.copy(), "relation_rows":subset.rows(),
                     "metrics":diagnose(subset)})
        if step < steps:
            ids = [i for i in ids if rng.uniform() < q]
    return {"method":"independent Bernoulli retention, induced suborders", "retention":q,
            "seed":seed, "steps":steps, "interpretation":"Thinning only; no fitted RG flow or continuum claim", "path":path}


class RAX_CQG_SimulationEngine:
    """Compatibility entry point; returned schema deliberately changes in 0.2."""
    def __init__(self, size=30, model="percolation", p=0.25, seed=42):
        self.cs, self.metadata = generate(model, size, seed, p)

    def run_diagnostics(self):
        return {"schema":"RAX-CQG-EXPERIMENT-0.2", "software_version":VERSION,
                "evidence_class":"FINITE_ORDER_BENCHMARK", "generator":self.metadata,
                "relation_rows":self.cs.rows(), "relation_sha256":self.cs.digest(), "metrics":diagnose(self.cs)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, default="minkowski_4d")
    parser.add_argument("--size", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--p", type=float, default=.25)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = experiment(args.model, args.size, args.seed, args.p)
    except ValueError as exc:
        parser.error(str(exc))
    text = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
