#!/usr/bin/env python3
"""Bounded Lorentzian replication and adaptive X6 falsification controls.

This is a search program, not an autonomous theorem prover or an LLM. It cannot
promote finite tests to theorems, assert novelty, or infer physical laws.
Scheduling and upload belong to GitHub Actions. No network is used by this code.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import platform
import random
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from fractions import Fraction as F
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "agent/math-agent-config.json"
SCHEMA = "x6-bounded-math-agent-1"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def stamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_time(value):
    t = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(t.tzinfo is not None, "timezone required")
    return t.astimezone(timezone.utc)


def load_config(path):
    c = json.loads(path.read_text())
    require(c.get("schema") == SCHEMA, "unknown config schema")
    require(type(c.get("enabled")) is bool, "enabled must be a boolean")
    start, stop = parse_time(c["start_utc"]), parse_time(c["stop_utc"])
    require(timedelta(0) < stop-start <= timedelta(hours=72), "window must be 0..72 hours")
    for key, lo, hi in [("max_seconds", 5, 120), ("cases_per_track", 8, 128),
                        ("seed", 0, 2**32-1), ("slot_hours", 1, 24)]:
        require(type(c.get(key)) is int and lo <= c[key] <= hi, f"invalid {key}")
    require(isinstance(c.get("app_sha256"), str) and len(c["app_sha256"]) == 64,
            "app digest required")
    return c


def admitted(c, now=None, reserve_seconds=None):
    now = now or datetime.now(timezone.utc)
    reserve = c["max_seconds"] + 15 if reserve_seconds is None else reserve_seconds
    return c["enabled"] and parse_time(c["start_utc"]) <= now and now + timedelta(seconds=reserve) < parse_time(c["stop_utc"])


class Budget:
    def __init__(self, config):
        self.end = time.monotonic() + config["max_seconds"]
        self.stop = parse_time(config["stop_utc"])

    def check(self):
        if time.monotonic() >= self.end or datetime.now(timezone.utc) >= self.stop:
            raise TimeoutError("computation budget or authorised window exhausted")

    def remaining(self):
        self.check()
        return max(0.05, min(self.end-time.monotonic(),
                            (self.stop-datetime.now(timezone.utc)).total_seconds()))


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


class Frames(HTMLParser):
    def __init__(self):
        super().__init__()
        self.frames = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "iframe" and "srcdoc" in attrs:
            self.frames[attrs.get("id")] = attrs["srcdoc"]


def core_functions(app):
    # Deliberately fail closed if the pinned layout changes; no approximate port.
    p = Frames()
    p.feed(app)
    src = p.frames["signalFrame"]
    a, b = src.index("function fft("), src.index("function smooth(")
    block = src[a:b]
    require(block.count("function ") == 3, "unexpected FFT/filter block")
    a, b = app.index("function makeGraph("), app.index("function build(samples,")
    mapping = app[a:b]
    require(mapping.count("function ") == 1, "unexpected mapping block")
    return block, mapping


def js_core(action, functions, cases, budget):
    budget.check()
    run = subprocess.run(["node", str(ROOT / "agent/math_core_runner.cjs")],
                         input=json.dumps({"action": action, "functions": functions,
                                           "cases": cases}, allow_nan=False),
                         capture_output=True, text=True, timeout=min(15, budget.remaining()))
    require(run.returncode == 0, "X6 core execution failed: " + run.stderr[:1000])
    result = json.loads(run.stdout)
    require(len(result) == len(cases), "incomplete JS batch")
    return result


def squared_increments(values):
    return [(b-a)**2 for a, b in zip(values, values[1:])]


def walk(increments):
    values = [0]
    for delta in increments:
        values.append(values[-1] + delta)
    return values


def mapping_track(rng, count, mapping, budget):
    """Refute injectivity even modulo a global sign and additive constant."""
    witnesses, cases = [], []
    for i in range(count):
        budget.check()
        # The first 3-point witness is minimal for ambiguity beyond global sign.
        steps = [1, 1] if i == 0 else [rng.randint(1, 5) for _ in range(rng.randint(2, 8))]
        x = walk(steps)
        signed = steps[:]
        signed[rng.randrange(1, len(signed))] *= -1
        y = walk(signed)
        require(x != y and x != [-v for v in y], "trivial global symmetry")
        require(squared_increments(x) == squared_increments(y), "false collision")
        sigma = max(1, max(steps))
        cases.extend({"values": v, "sigma": sigma, "digits": 6} for v in (x, y))
        witnesses.append({"x": x, "y": y, "sigma": sigma,
                          "squared_increments": squared_increments(x),
                          "exact_symbolic_reason": "identical squared increments at each edge"})
    outputs = js_core("mapping", mapping, cases, budget)
    for i, w in enumerate(witnesses):
        require(outputs[2*i] == outputs[2*i+1], "actual X6 mapping disagrees")
        w["actual_x6_edges"] = outputs[2*i]["edgeText"]
    return {"hypothesis": "The labeled Gaussian path identifies its signal modulo global sign and translation",
            "finding": "FALSIFIED_EXACT_WITNESS", "checked_pairs": count,
            "minimal_witness": witnesses[0], "witnesses": witnesses,
            "novelty": "NOT_CLAIMED_ELEMENTARY_CONSEQUENCE",
            "scope": "fixed positive sigma; original ordered samples; graph and spectrum cannot recover lost signs"}


def laplacian(n, edges):
    L = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j, w in edges:
        require(0 <= i < j < n and w >= 0, "invalid undirected edge")
        L[i][i] += w
        L[j][j] += w
        L[i][j] -= w
        L[j][i] -= w
    return L


def strict_lower(L, b):
    """Exact rational Schur complements on L+(b+1)J/n-bI."""
    n = len(L)
    M = [[L[i][j] + (b+1)/n - (b if i == j else 0)
          for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = M[k][k]
        if pivot <= 0:
            return False
        for i in range(k+1, n):
            for j in range(k+1, n):
                M[i][j] -= M[i][k]*M[k][j]/pivot
    return True


def rayleigh_upper(L):
    n = len(L)
    return min((L[i][i]+L[j][j]-2*L[i][j])/2
               for i in range(n) for j in range(i+1, n))


def exact_bracket(L, budget):
    lo, hi = F(0), rayleigh_upper(L)
    require(strict_lower(L, lo), "generated graph disconnected")
    for _ in range(10):
        budget.check()
        mid = (lo+hi)/2
        if strict_lower(L, mid):
            lo = mid
        else:
            hi = mid
    return lo, hi


def perturbation_track(rng, count, budget):
    import numpy as np
    records, parent, best = [], None, -1.0
    for index in range(count):
        budget.check()
        # Half fresh exploration, half bounded mutations of the tightest witness.
        adaptive = parent is not None and index % 2 == 1
        if adaptive:
            n, weights, changes = parent
            weights, changes = weights[:], changes[:]
            k = rng.randrange(n-1)
            changes[k] = max(-weights[k]+1, min(50, changes[k]+rng.choice([-1, 1])))
        else:
            n = 2 if index == 0 else rng.randint(2, 8)
            weights = [100] if index == 0 else [rng.randint(20, 150) for _ in range(n-1)]
            changes = [10] if index == 0 else [rng.randint(-10, 10) for _ in range(n-1)]
        if not any(changes):
            changes[0] = 1
        original = laplacian(n, [(i, i+1, F(w, 100)) for i, w in enumerate(weights)])
        changed = laplacian(n, [(i, i+1, F(w+d, 100)) for i, (w, d) in enumerate(zip(weights, changes))])
        r = max(F(abs(changes[i-1]) if i else 0, 100) +
                F(abs(changes[i]) if i < n-1 else 0, 100) for i in range(n))
        epsilon = 2*r
        lo1, hi1 = exact_bracket(original, budget)
        lo2, hi2 = exact_bracket(changed, budget)
        # This is an EXACT finite-case check of the transferred lower bound.
        require(strict_lower(changed, lo1-epsilon), "proved factor-two transfer failed")
        require(strict_lower(original, lo2-epsilon), "reverse factor-two transfer failed")
        lam1 = float(np.linalg.eigvalsh(np.array(original, dtype=float))[1])
        lam2 = float(np.linalg.eigvalsh(np.array(changed, dtype=float))[1])
        ratio = abs(lam2-lam1)/float(r)
        # Disjoint EXACT enclosures refute the deliberately overstrong factor-one hypothesis.
        refuted = lo2-hi1 > r or lo1-hi2 > r
        rec = {"n": n, "weights_units_0_01": weights, "changes_units_0_01": changes,
               "adaptive_mutation": adaptive, "row_uncertainty": str(r),
               "proved_transfer_epsilon": str(epsilon),
               "original_gap_enclosure": [str(lo1), str(hi1)],
               "changed_gap_enclosure": [str(lo2), str(hi2)],
               "factor_one_falsified_by_exact_enclosures": refuted,
               "observed_ratio_numerical": ratio, "factor_two_exact_transfer": True}
        records.append(rec)
        if ratio > best:
            best, parent = ratio, (n, weights[:], changes[:])
    return {"hypothesis": "Gap change is at most max incident absolute edge-weight change (factor one)",
            "finding": "FALSIFIED_EXACT_WITNESS" if any(r["factor_one_falsified_by_exact_enclosures"] for r in records) else "SURVIVED_FINITE_SEARCH",
            "factor_two_status": "EXACT_TRANSFERS_CHECKED_ON_FINITE_CASES",
            "cases": count, "records": records,
            "novelty": "NOT_CLAIMED_STANDARD_PERTURBATION_THEORY",
            "policy": "alternate fresh paths and mutations of the largest observed gap-change/uncertainty ratio"}


def numpy_filter(values, angle, width, mode):
    """Separate numerical reference, not an exact proof."""
    import numpy as np
    a = np.asarray(values, dtype=float)
    z = np.fft.rfft(a)
    centre, half = math.radians(angle), math.radians(width)/2
    phase = np.angle(z)
    dist = abs(np.arctan2(np.sin(phase-centre), np.cos(phase-centre)))
    keep = dist <= half
    if mode == "stop":
        keep = ~keep
    return np.fft.irfft(z*keep, n=len(a))


def phase_track(rng, count, functions, budget):
    import numpy as np
    cases, metadata = [], []
    parent, best = None, -1.0
    # Adaptive batches mutate the strongest earlier shift counterexample.
    all_records, source_outputs = [], []
    for offset in range(0, count, 16):
        cases, metadata = [], []
        for i in range(offset, min(count, offset+16)):
            budget.check()
            if i == 0:
                values, shift, angle, width = [1, 0, -1, 0]*8, 1, 0, 45
            elif parent and i % 2:
                values, shift, angle, width = parent
                angle = max(-180, min(180, angle+rng.choice([-5, 5])))
            else:
                n = rng.choice([32, 64, 128])
                k, phase = rng.randint(1, n//2-1), rng.uniform(-math.pi, math.pi)
                values = [math.cos(2*math.pi*k*j/n+phase) for j in range(n)]
                shift, angle, width = rng.randint(1, n-1), rng.randrange(-180, 181, 15), rng.choice([15, 45, 90, 180])
            shifted = np.roll(values, shift).tolist()
            for x in [values, shifted]:
                cases.append({"values": x, "angle": angle, "width": width, "mode": "pass"})
            metadata.append((values, shift, angle, width))
        output = js_core("filter", functions, cases, budget)
        for j, (values, shift, angle, width) in enumerate(metadata):
            a, b = output[2*j], output[2*j+1]
            for q, obs in [(cases[2*j], a), (cases[2*j+1], b)]:
                require(all(math.isfinite(v) for v in obs["values"]), "nonfinite X6 output")
                require(obs["imag"] < 1e-9, "X6 output not real")
                ref = numpy_filter(q["values"], q["angle"], q["width"], q["mode"])
                # Tiny FFT roundoff components can have arbitrary phase. Compare
                # output arrays with absolute tolerance, not tiny-bin mask identity.
                require(float(np.max(abs(ref-np.array(obs["values"])))) < 1e-9,
                        "X6/NumPy filter disagreement")
            norm = float(np.linalg.norm(values))
            defect = float(np.linalg.norm(np.array(b["values"])-np.roll(a["values"], shift))/norm)
            record = {"input": values, "shift_samples": shift, "angle_degrees": angle,
                      "width_degrees": width, "relative_equivariance_defect": defect,
                      "x6_original_output": a["values"], "x6_shifted_output": b["values"],
                      "numpy_crosscheck": "PASS_WITH_ABSOLUTE_TOLERANCE_1e-9"}
            all_records.append(record)
            if defect > best:
                best, parent = defect, (values[:], shift, angle, width)
    return {"hypothesis": "The fixed-angle X6 phase filter commutes with all circular time shifts",
            "finding": "NUMERICAL_COUNTEREXAMPLE" if best > 1e-6 else "SURVIVED_FINITE_SEARCH",
            "max_relative_defect": best, "cases": count,
            "analytically_explained_control": all_records[0], "records": all_records,
            "novelty": "NOT_CLAIMED_DFT_SHIFT_THEOREM_CONSEQUENCE",
            "execution": "unmodified numerical functions extracted from pinned HTML; Node VM, not browser E2E",
            "policy": "alternate new tones/offsets and angle mutations of the strongest prior-batch counterexample"}


def run(config, output, replay_slot=None):
    output.mkdir(parents=True, exist_ok=False)
    report = {"schema": SCHEMA, "started_at": stamp(), "status": "NOT_EXECUTED",
              "novelty": "NOT_ASSESSED", "physical_evidence": "NONE",
              "denoising_benchmark": "NOT_PERFORMED", "config": config, "tracks": {}}
    try:
        if not admitted(config):
            report["status"] = "STOPPED"
            report["reason"] = "disabled, outside authorised window, or insufficient time reserve"
            return 0
        budget = Budget(config)
        # Unix hard alarm complements checks between small bounded cases.
        signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("hard runtime limit")))
        signal.alarm(config["max_seconds"])
        app_path = ROOT / "app/index.html"
        actual_hash = hashlib.sha256(app_path.read_bytes()).hexdigest()
        require(actual_hash == config["app_sha256"], "application hash changed; review required")
        functions, mapping = core_functions(app_path.read_text())
        slot = int((datetime.now(timezone.utc)-parse_time(config["start_utc"])).total_seconds() // (3600*config["slot_hours"]))
        if replay_slot is not None:
            require(type(replay_slot) is int and 0 <= replay_slot <= 72, "invalid replay slot")
        seed_slot = slot if replay_slot is None else replay_slot
        effective_seed = (config["seed"] + seed_slot*1_000_003) % 2**32
        report.update({"slot": slot, "effective_seed": effective_seed,
                       "seed_slot": seed_slot, "mode": "SEARCH" if replay_slot is None else "REPLAY",
                       "app_sha256": actual_hash, "python": platform.python_version(),
                       "node": subprocess.check_output(["node", "--version"], text=True).strip(),
                       "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                       "git_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True))})
        import numpy as np
        report["numpy"] = np.__version__
        # Lazy import preserves a stdlib-only admission guard. When invoked as
        # a script, Python places agent/ on sys.path; as a module use its package.
        if __package__:
            from .lorentz_spectral import finite_order_track, propagator_track
        else:
            from lorentz_spectral import finite_order_track, propagator_track
        report["priority"] = "LORENTZIAN_SPECTRAL_GEOMETRY"
        for index, (name, fn) in enumerate([
            ("lorentz_orders", lambda r: finite_order_track(r, budget)),
            ("lorentz_propagator", lambda r: propagator_track(seed_slot, budget)),
            ("mapping", lambda r: mapping_track(r, config["cases_per_track"], mapping, budget)),
            ("perturbation", lambda r: perturbation_track(r, config["cases_per_track"], budget)),
            ("phase", lambda r: phase_track(r, config["cases_per_track"], functions, budget)),
        ]):
            budget.check()
            track_started = time.monotonic()
            finding = fn(random.Random(effective_seed + index*7919))
            finding["elapsed_seconds"] = time.monotonic() - track_started
            write_json(output / f"{name}.json", finding)
            report["tracks"][name] = {k: v for k, v in finding.items() if k not in
                                      ("records", "witnesses", "collisions", "minimal_witness", "analytically_explained_control")}
        report["status"] = "PASS"
        return 0
    except Exception as exc:
        report.update({"status": "INCOMPLETE" if isinstance(exc, TimeoutError) else "FAIL",
                       "error": f"{type(exc).__name__}: {exc}"})
        return 1
    finally:
        signal.alarm(0)
        report["finished_at"] = stamp()
        write_json(output / "report.json", report)
        summary = ["# X6 bounded math agent: " + report["status"], "",
                   "PASS describes execution/checks, not truth of hypotheses or mathematical novelty.", ""]
        for name, track in report["tracks"].items():
            summary.append(f"- {name}: {track['finding']}")
        if "lorentz_orders" in report["tracks"]:
            summary += ["", "## Exact Lorentzian reference", "",
                        "| Elements | Orders | Spectral classes | With endpoint counts |",
                        "|---|---:|---:|---:|"]
            for row in report["tracks"]["lorentz_orders"]["rows"]:
                summary.append(f"| {row['n']} | {row['nonisomorphic_orders']} | {row['spectral_classes']} | {row['classes_with_minimal_maximal_counts']} |")
        if "lorentz_propagator" in report["tracks"]:
            summary += ["", "## Numerical diamond comparison", "",
                        "Mean relative L2 error of the largest eight positive eigenvalues against the analytic spectrum; three samples per cell.", "",
                        "| Elements | Frozen reference | Independent comparison |",
                        "|---|---:|---:|"]
            for row in report["tracks"]["lorentz_propagator"]["comparisons"]:
                errors = row["mean_relative_l2_error"]
                summary.append(f"| {row['n']} | {errors['reference']:.2%} | {errors['comparison']:.2%} |")
            summary += ["", "Small finite samples; no convergence rate or general spectral-density theorem inferred."]
        if "error" in report:
            summary.append("- Error: " + report["error"])
        summary += ["", "No physical validation or denoising superiority is claimed.",
                    "The searched families are deliberately small. See docs/MATH_AGENT.md."]
        (output / "summary.md").write_text("\n".join(summary)+"\n")
        hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
        hashes["source_files"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in [ROOT/"agent/run_math_agent.py", ROOT/"agent/math_core_runner.cjs",
                                            ROOT/"agent/lorentz_spectral.py",
                                            ROOT/"agent/math-requirements.txt", ROOT/"agent/math-agent-config.json"]}
        write_json(output / "SHA256.json", hashes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=Path("math-agent-output"))
    parser.add_argument("--guard", action="store_true", help="stdlib-only admission check for CI")
    parser.add_argument("--replay-slot", type=int, help="reuse a recorded seed_slot; still obeys the active window")
    args = parser.parse_args()
    config = load_config(args.config)
    if args.guard:
        active = admitted(config, reserve_seconds=360)
        print("active="+str(active).lower())
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("active="+str(active).lower()+"\n")
        return 0
    return run(config, args.output, replay_slot=args.replay_slot)


if __name__ == "__main__":
    sys.exit(main())
