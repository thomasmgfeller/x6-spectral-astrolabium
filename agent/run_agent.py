#!/usr/bin/env python3
"""One bounded X6 data-agent iteration. Scheduling/upload belong to the workflow.

Uses the actual unmodified HTML application in Chromium. No LLM/API key needed.
All live data are public NOAA SWPC GOES XRS observations, not quantum data.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import statistics
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"
MAX_BYTES = 2_000_000
SAMPLE_COUNT = 128
ENERGY = "0.1-0.8nm"
VERSION = "x6-data-agent-1"


def utcnow():
    return datetime.now(timezone.utc)


def stamp(value=None):
    return (value or utcnow()).isoformat().replace("+00:00", "Z")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def require(condition, message):
    if not condition:
        raise ValueError(message)


class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urlsplit(newurl)
        require(parsed.scheme == "https" and parsed.hostname == "services.swpc.noaa.gov",
                "Data source redirected outside the approved NOAA host")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_source():
    opener = urllib.request.build_opener(SameHostRedirect)
    last = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(SOURCE, headers={"User-Agent": VERSION,
                                                          "Accept": "application/json"})
            with opener.open(req, timeout=25) as response:
                raw = response.read(MAX_BYTES + 1)
                require(len(raw) <= MAX_BYTES, "NOAA response exceeds byte limit")
                return raw, {"url": SOURCE, "http_status": response.status,
                             "retrieved_at": stamp(), "attempts": attempt + 1,
                             "etag": response.headers.get("ETag"),
                             "last_modified": response.headers.get("Last-Modified")}
        except Exception as exc:
            last = exc
            if attempt == 0:
                time.sleep(2)
    raise RuntimeError(f"NOAA fetch failed: {last}")


def prepare_samples(raw, now=None, replay=False):
    """Latest contiguous 128-minute single-satellite window; never interpolate."""
    require(len(raw) <= MAX_BYTES, "Input exceeds byte limit")
    rows = json.loads(raw)
    require(isinstance(rows, list) and 1 <= len(rows) <= 20_000, "Invalid NOAA row array")
    observations = {}
    rejected = 0
    for row in rows:
        if not isinstance(row, dict) or row.get("energy") != ENERGY:
            continue
        try:
            flux = row["flux"]
            # The operational NOAA JSON currently spells this field 'contaminaton'.
            flag = row.get("electron_contaminaton", row.get("electron_contamination"))
            require(flag is False, "Missing/positive electron contamination flag")
            require(type(flux) in (float, int) and math.isfinite(flux) and flux > 0,
                    "Nonpositive/nonfinite flux")
            satellite = row["satellite"]
            require(type(satellite) is int and satellite > 0, "Invalid satellite")
            ts = datetime.fromisoformat(row["time_tag"].replace("Z", "+00:00"))
            require(ts.tzinfo is not None, "Timestamp lacks timezone")
            key = ts.astimezone(timezone.utc)
            require(key.second == 0 and key.microsecond == 0, "Off-minute timestamp")
            require(key not in observations, "Duplicate timestamp")
            observations[key] = {"time_tag": stamp(key), "satellite": satellite,
                                 "flux_w_m2": flux}
        except (ValueError, KeyError, TypeError, AttributeError):
            rejected += 1
    ordered = sorted(observations.items())
    contiguous, latest = [], None
    previous = None
    for ts, row in ordered:
        if previous and ((ts - previous[0]).total_seconds() != 60 or
                         row["satellite"] != previous[1]["satellite"]):
            contiguous = []
        contiguous.append(row)
        if len(contiguous) >= SAMPLE_COUNT:
            latest = contiguous[-SAMPLE_COUNT:]
        previous = (ts, row)
    require(latest is not None, "No contiguous 128-minute valid single-satellite window")
    age = ((now or utcnow()) - datetime.fromisoformat(latest[-1]["time_tag"].replace("Z", "+00:00"))).total_seconds()
    if not replay:
        require(-300 <= age <= 7200, "Selected window is stale (>2 hours) or future-dated")
    logs = [math.log10(row["flux_w_m2"]) for row in latest]
    mean, std = statistics.mean(logs), statistics.pstdev(logs)
    require(std > 1e-12, "Constant/near-constant log flux: normalization undefined")
    values = [(x - mean) / std for x in logs]
    return {"rows_received": len(rows), "rejected_target_band_rows": rejected,
            "energy": ENERGY, "sample_count": SAMPLE_COUNT, "cadence_seconds": 60,
            "start": latest[0]["time_tag"], "end": latest[-1]["time_tag"],
            "satellite": latest[0]["satellite"], "age_seconds_at_selection": age,
            "selection": "latest contiguous 128 samples; no gap filling or interpolation",
            "transform": {"name": "zscore(log10(flux_w_m2))", "mean": mean,
                          "population_std": std}, "observations": latest, "values": values}


def fraction(value):
    require(isinstance(value, str) and len(value) <= 4096 and
            re.fullmatch(r"-?\d+(?:/\d+|\.\d+)?", value), "Invalid rational token")
    return F(value)


def matrix_from_edges(source):
    lines = [x.split() for x in source.splitlines() if x.strip()]
    require(1 <= len(lines) <= 276, "Invalid edge count")
    names = []
    for edge in lines:
        require(len(edge) == 3, "Expected a b weight")
        for name in edge[:2]:
            if name not in names:
                names.append(name)
    require(2 <= len(names) <= 24, "Expected 2..24 vertices")
    ix = {name: i for i, name in enumerate(names)}
    L = [[F(0) for _ in names] for _ in names]
    adjacency = [set() for _ in names]
    for a, b, token in lines:
        i, j, w = ix[a], ix[b], fraction(token)
        require(i != j and w > 0, "Invalid edge")
        L[i][i] += w
        L[j][j] += w
        L[i][j] -= w
        L[j][i] -= w
        adjacency[i].add(j)
        adjacency[j].add(i)
    seen, todo = {0}, [0]
    while todo:
        for node in adjacency[todo.pop()] - seen:
            seen.add(node)
            todo.append(node)
    require(len(seen) == len(names), "Disconnected graph: no positive global gap")
    return names, L


def positive_definite(M):
    """Separate implementation: rational Schur complements (no JS imports)."""
    A = [row[:] for row in M]
    for k in range(len(A)):
        pivot = A[k][k]
        if pivot <= 0:
            return False
        for i in range(k + 1, len(A)):
            for j in range(k + 1, len(A)):
                A[i][j] -= A[i][k] * A[k][j] / pivot
    return True


def lower_holds(L, bound):
    n = len(L)
    return positive_definite([[L[i][j] + (bound + 1) / n - (bound if i == j else 0)
                               for j in range(n)] for i in range(n)])


def verify_certificate(cert, expected_source):
    """Verify actual browser-exported bounds, witness and all search decisions."""
    require(cert.get("source") == expected_source, "Certificate source changed")
    require(cert.get("scope") == "connected-undirected-positive-rational-weights",
            "Unsupported certificate scope")
    names, L = matrix_from_edges(expected_source)
    lower, upper = fraction(cert["strictLower"]), fraction(cert["upperBound"])
    require(cert.get("strictLowerCertified") is True and 0 < lower <= upper,
            "Positive strict lower bound was not certified")
    require(lower_holds(L, lower), "Browser lower bound is false")
    pair = cert["upperWitnessPair"]
    require(isinstance(pair, list) and len(pair) == 2 and pair[0] != pair[1],
            "Invalid Rayleigh witness")
    i, j = names.index(pair[0]), names.index(pair[1])
    require((L[i][i] + L[j][j] - 2 * L[i][j]) / 2 == upper,
            "Upper bound does not equal its Rayleigh witness")
    trace = cert["searchTrace"]
    require(isinstance(trace, list) and 1 <= len(trace) <= 16, "Invalid search trace")
    for step in trace:
        require(type(step["positiveDefinite"]) is bool and
                lower_holds(L, fraction(step["bound"])) == step["positiveDefinite"],
                "Browser/Python disagreement in search trace")
    return {"status": "PASS", "vertices": len(names), "strict_lower": str(lower),
            "upper": str(upper), "trace_decisions_checked": len(trace),
            "arithmetic": "Python fractions.Fraction",
            "scope": "rounded rational graph only; software cross-check, not external peer review"}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def wait_json(page, selector, predicate="x => !!x"):
    page.wait_for_function("""({selector, predicate}) => {
      try { return eval('(' + predicate + ')')(JSON.parse(document.querySelector(selector).textContent)); }
      catch (_) { return false; }
    }""", arg={"selector": selector, "predicate": predicate}, timeout=30000)
    return json.loads(page.locator(selector).inner_text())


def browser_run(out, prepared):
    from playwright.sync_api import sync_playwright
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT / "app")))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    result = {"status": "NOT_EXECUTED", "page_errors": [], "controls": []}
    try:
        with sync_playwright() as pw:
            launch = {"headless": True}
            binary = os.environ.get("X6_CHROMIUM_PATH")
            if binary:
                launch["executable_path"] = binary
            browser = pw.chromium.launch(**launch)
            result["chromium_version"] = browser.version
            try:
                page = browser.new_page(accept_downloads=True)
                page.set_default_timeout(30000)
                page.on("pageerror", lambda e: result["page_errors"].append(str(e)))
                # The application cannot upload inputs or call external services.
                origin = f"http://127.0.0.1:{server.server_port}"
                page.route("**/*", lambda route: route.continue_()
                           if route.request.url.startswith(origin + "/") else route.abort())
                response = page.goto(origin + "/index.html", wait_until="load")
                require(response is not None and response.status == 200, "App HTTP load failed")
                spectral = page.frame_locator("#spectrumFrame")
                spectral.locator("#edges").wait_for(state="attached")
                page.locator("#tab-spectrum").click()
                # Known analytic cases, including equality/too-high rejection.
                for name, source, bound, expected in [
                    ("path4_lower", "a b 1\nb c 1\nc d 1", "0.5", True),
                    ("path4_too_high", "a b 1\nb c 1\nc d 1", "0.6", False),
                    ("triangle_equality", "a b 1\nb c 1\na c 1", "3", False),
                    ("weighted2_equality", "a b 0.125", "0.25", False),
                ]:
                    spectral.locator("#edges").fill(source)
                    spectral.locator("#bound28").fill(bound)
                    spectral.locator("#audit28").click()
                    value = json.loads(spectral.locator("#out28").inner_text())
                    ok = value.get("strictLowerCertified") is expected
                    result["controls"].append({"name": name, "pass": ok, "output": value})
                    require(ok, "Analytic control failed: " + name)
                require(not result["page_errors"], "Browser error during controls")
                result["controls_status"] = "PASS"
                write_json(out / "browser_controls.json", result["controls"])
                if prepared is None:
                    result["status"] = "NOT_EXECUTED"
                    result["reason"] = "Live data unavailable; controls ran separately"
                    return result
                page.locator("#tab-signal").click()
                signal = page.frame_locator("#signalFrame")
                signal.locator("#mc").fill("20")
                signal.locator("#seed").fill("104729")
                signal.locator("#file").set_input_files(str(out / "signal.csv"))
                signal.locator("#fileInfo").filter(has_text="128 Werte").wait_for()
                require("Fehler:" not in signal.locator("#status").inner_text(), "Signal analysis failed")
                signal.locator("#test").click()
                with page.expect_download() as event:
                    signal.locator("#export").click()
                event.value.save_as(str(out / "signal_evidence.json"))
                evidence = json.loads((out / "signal_evidence.json").read_text())
                require(evidence["source"]["reference"] == "moving average", "Unexpected SNR reference")
                require(evidence["raw_data"] == prepared["values"], "Imported samples changed")
                tests = evidence["tests"]
                require(len(tests) >= 10 and all(t["pass"] is True for t in tests), "Signal self-test failed")
                require(evidence["gates"]["finite_output"] is True and
                        evidence["gates"]["conjugate_symmetry"] is True, "Numerical signal gate failed")
                result["signal_selftests"] = len(tests)
                result["signal_observables"] = evidence["observables"]
                result["signal_gate_interpretation"] = "SNR/MC thresholds are observations, not agent success criteria"
                page.locator("#tab-model").click()
                page.locator("#arrayField35").select_option("raw")
                page.locator("#captureArray35").click()
                capture = wait_json(page, "#pipelineOut35", "x => x.status === 'CAPTURED_NOT_MODELED' || x.status === 'FAIL'")
                require(capture["status"] == "CAPTURED_NOT_MODELED", "Sample handoff failed")
                write_json(out / "sample_handoff.json", capture)
                provenance = capture["provenance"]
                indices = provenance["indices"]
                expected_indices = list(range(0, SAMPLE_COUNT, math.ceil(SAMPLE_COUNT / 24)))
                require(indices == expected_indices and
                        provenance["samples"] == [prepared["values"][i] for i in indices],
                        "Browser subsampling differs from declared stride")
                samples = provenance["samples"]
                sigma = max(1.0, max(abs(b - a) for a, b in zip(samples, samples[1:])))
                page.locator("#sigma34").fill(repr(sigma))
                page.locator("#digits34").select_option("6")
                page.locator("#ack34").check()
                page.locator("#certRun36").click()
                pipeline = wait_json(page, "#certOut36", "x => x.schema === 'x6-pipeline-evidence-2' || x.status === 'FAIL'")
                require(pipeline.get("schema") == "x6-pipeline-evidence-2", str(pipeline.get("error")))
                with page.expect_download() as event:
                    page.locator("#certExport36").click()
                event.value.save_as(str(out / "browser_certificate.json"))
                exported = json.loads((out / "browser_certificate.json").read_text())
                require(exported == pipeline, "Downloaded certificate differs from displayed result")
                require(exported["externalVerification"] == "NOT_EXECUTED", "App unexpectedly claims external verification")
                model = exported["model"]
                require(len(model["samples"]) == len(samples) and
                        all(math.isclose(a, b, rel_tol=1e-14, abs_tol=1e-14)
                            for a, b in zip(model["samples"], samples)), "Model sample handoff changed")
                # JS uses toPrecision(15) on handoff. Recompute the mapping from those values.
                expected_edges = []
                for i, (a, b) in enumerate(zip(model["samples"], model["samples"][1:])):
                    w = math.exp(-((b - a) / sigma) ** 2)
                    actual = F(model["graph"]["edges"][i]["weight"])
                    require(abs(float(actual) - w) <= 0.500001e-6, "Rounded graph weight disagrees")
                    edge = model["graph"]["edges"][i]
                    require(edge["a"] == f"s{i}" and edge["b"] == f"s{i+1}", "Graph is not the declared path")
                    expected_edges.append(f"s{i} s{i+1} {edge['weight']}")
                expected_source = "\n".join(expected_edges)
                require(expected_source == model["graph"]["edgeText"], "Model edge text mismatch")
                checked = verify_certificate(exported["certification"]["refined"], expected_source)
                write_json(out / "python_certificate_check.json", checked)
                result["certificate_check"] = checked
                result["mapping"] = {"sigma": sigma, "digits": 6,
                                     "sigma_rule": "max(1, largest adjacent captured-sample difference)",
                                     "physical_interpretation": "NONE"}
                require(not result["page_errors"], "Browser emitted page errors")
                result["status"] = "PASS"
                return result
            finally:
                browser.close()
    except Exception as exc:
        result["status"] = "FAIL"
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        write_json(out / "browser_run.json", result)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "agent-output")
    parser.add_argument("--replay", type=Path, help="Explicit offline replay; bypasses freshness only, never labelled LIVE")
    args = parser.parse_args(argv)
    out = args.output.resolve()
    require(not out.exists() or not any(out.iterdir()), "Output directory must be empty (avoid mixing runs)")
    out.mkdir(parents=True, exist_ok=True)
    report = {"schema": VERSION, "started_at": stamp(), "status": "NOT_EXECUTED",
              "mode": "REPLAY" if args.replay else "LIVE", "physical_validation": "NOT_CLAIMED",
              "independent_peer_review": "NOT_CLAIMED", "release_approval": False,
              "limits": ["One 128-minute window from the public six-hour feed",
                         "Imported SNR uses a moving-average proxy, not ground truth",
                         "Graph is a model of a decimated transformed signal",
                         "Exact certificate covers rounded rational weights only",
                         "Same-project automation is not independent scientific validation"],
              "runtime": {"python": platform.python_version(), "platform": platform.platform()},
              "provenance": {"app_sha256": hashlib.sha256((ROOT / "app/index.html").read_bytes()).hexdigest(),
                             "agent_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    try:
        report["runtime"]["playwright"] = importlib.metadata.version("playwright")
        report["provenance"]["git_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        report["provenance"]["working_tree_dirty"] = bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True).strip())
    except Exception:
        report["provenance"]["environment_metadata_incomplete"] = True
    prepared = None
    try:
        if args.replay:
            raw = args.replay.read_bytes()
            metadata = {"url": SOURCE, "retrieved_at": None, "transport": "EXPLICIT_LOCAL_REPLAY"}
        else:
            raw, metadata = fetch_source()
        (out / "noaa_raw.json").write_bytes(raw)
        metadata.update({"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                         "attribution": "NOAA / NWS Space Weather Prediction Center, GOES XRS",
                         "endorsement": "No NOAA endorsement or affiliation is implied"})
        report["source"] = metadata
        prepared = prepare_samples(raw, replay=bool(args.replay))
        write_json(out / "selected_samples.json", prepared)
        (out / "signal.csv").write_text("value\n" + "\n".join(repr(x) for x in prepared["values"]) + "\n")
        report["data_status"] = "PASS"
    except Exception as exc:
        report["data_status"] = "FAIL"
        report["data_error"] = f"{type(exc).__name__}: {exc}"
    try:
        report["browser"] = browser_run(out, prepared)
    except Exception as exc:
        report["browser"] = {"status": "NOT_EXECUTED", "error": f"{type(exc).__name__}: {exc}"}
    report["status"] = "PASS" if report["data_status"] == "PASS" and report["browser"]["status"] == "PASS" else "FAIL"
    report["finished_at"] = stamp()
    write_json(out / "report.json", report)
    summary = (f"# X6 data agent: {report['status']}\n\n"
               f"Mode: **{report['mode']}**. Started: {report['started_at']}.\n\n"
               f"Data: **{report['data_status']}**. Browser: **{report['browser']['status']}**.\n\n"
               "Source: NOAA / NWS SWPC GOES XRS (0.1–0.8 nm). No NOAA endorsement.\n\n"
               "This is an automated application/certificate check, not a claim of improved denoising, "
               "quantum behaviour, independent peer review or release approval.\n\n"
               "See report.json and the unmodified browser exports for details.\n")
    if report.get("data_error"):
        summary += "\nData failure: " + report["data_error"] + "\n"
    if report["browser"].get("error"):
        summary += "\nBrowser failure: " + report["browser"]["error"] + "\n"
    (out / "summary.md").write_text(summary, encoding="utf-8")
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(out.iterdir()) if p.is_file() and p.name != "SHA256.json"}
    write_json(out / "SHA256.json", {"algorithm": "sha256", "files": manifest})
    print(summary)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
