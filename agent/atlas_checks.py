"""Complete small Graph Atlas sweep in the real X6 browser application."""
from __future__ import annotations

import hashlib
import json
import os
from functools import partial
from http.server import ThreadingHTTPServer
from threading import Thread

import networkx as nx
import numpy as np

from agent.run_agent import ROOT, QuietHandler, require, verify_certificate, write_json


def atlas_cases():
    require(nx.__version__ == "3.4.2", "Unexpected NetworkX version")
    graphs = nx.graph_atlas_g()
    require(len(graphs) == 1253, "Atlas size changed")
    for index, g in enumerate(graphs):
        n = len(g)
        connected = n >= 2 and nx.is_connected(g)
        lines = [f"v{a} v{b} 1" for a, b in sorted(g.edges())]
        if not connected:
            lines = [f"v{i}" for i in g.nodes()] + lines
        yield {"atlas_index": index, "nodes": n, "edges": sorted(g.edges()),
               "components": nx.number_connected_components(g), "connected": connected,
               "source": "\n".join(lines)}


def numpy_spectrum(case):
    n = case["nodes"]
    laplacian = np.zeros((n, n))
    for a, b in case["edges"]:
        laplacian[a, a] += 1
        laplacian[b, b] += 1
        laplacian[a, b] -= 1
        laplacian[b, a] -= 1
    return np.linalg.eigvalsh(laplacian)


def run_atlas(out):
    from playwright.sync_api import sync_playwright
    cases = list(atlas_cases())
    write_json(out/"atlas_inputs.json", cases)
    counts = {"total": len(cases), "checked": 0, "connected_certificates": 0,
              "expected_global_rejections": 0, "failures": 0}
    errors = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT/"app")))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as pw:
            options = {"headless": True}
            if os.environ.get("X6_CHROMIUM_PATH"):
                options["executable_path"] = os.environ["X6_CHROMIUM_PATH"]
            browser = pw.chromium.launch(**options)
            try:
                page = browser.new_page(accept_downloads=True)
                page.on("pageerror", lambda e: errors.append(str(e)))
                origin = f"http://127.0.0.1:{server.server_port}"
                page.route("**/*", lambda route: route.continue_()
                           if route.request.url.startswith(origin + "/") else route.abort())
                response = page.goto(origin+"/index.html", wait_until="load")
                require(response is not None and response.status == 200, "Browser app load failed")
                frame = page.query_selector("#spectrumFrame").content_frame()
                frame.wait_for_selector("#edges", state="attached")
                with (out/"atlas_results.jsonl").open("w") as log:
                    for case in cases:
                        row = {"atlas_index": case["atlas_index"], "status": "FAIL"}
                        try:
                            # Execute existing app functions and real DOM click handlers.
                            # No algorithm is injected or replaced in the browser.
                            actual = frame.evaluate("""c => {
                              const result = {};
                              try {result.analysis = analyze(c.source);}
                              catch(e) {result.analysis_error = String(e);}
                              document.getElementById('edges').value = c.source;
                              document.getElementById('bound28').value = '0.01';
                              document.getElementById('audit28').click();
                              result.global_output = document.getElementById('out28').textContent;
                              if(c.connected) {
                                document.getElementById('steps29').value = '10';
                                document.getElementById('run29').click();
                                result.certificate = JSON.parse(document.getElementById('out29').textContent);
                              }
                              return result;
                            }""", case)
                            row["browser"] = actual
                            if case["nodes"] == 0:
                                require("Empty graph" in actual.get("analysis_error", ""),
                                        "Empty graph was not explicitly rejected")
                            else:
                                analysis = actual["analysis"]
                                require(analysis["exactNullity"] == case["components"], "Nullity mismatch")
                                require(analysis["numerical"]["converged"] is True, "Jacobi did not converge")
                                numeric = np.array([x["value"] for x in analysis["numerical"]["eig"]])
                                reference = numpy_spectrum(case)
                                require(numeric.shape == reference.shape and np.all(np.isfinite(numeric)),
                                        "Invalid browser eigenvalues")
                                error = float(np.max(np.abs(numeric-reference)))
                                require(error <= 1e-9, "Browser/NumPy spectrum discrepancy")
                                row["numpy_eigenvalues"] = reference.tolist()
                                row["max_absolute_eigenvalue_error"] = error
                            if case["connected"]:
                                row["exact_python_check"] = verify_certificate(actual["certificate"], case["source"])
                                counts["connected_certificates"] += 1
                            else:
                                reason = "Disconnected graph" if case["nodes"] >= 2 else "At least two vertices"
                                require(actual["global_output"].startswith("FAIL:") and
                                        reason in actual["global_output"], "Expected global certificate rejection missing")
                                counts["expected_global_rejections"] += 1
                            row["status"] = "PASS"
                        except Exception as exc:
                            row["error"] = f"{type(exc).__name__}: {exc}"
                            counts["failures"] += 1
                        counts["checked"] += 1
                        log.write(json.dumps(row, allow_nan=False) + "\n")
                        log.flush()
                        if counts["checked"] % 100 == 0:
                            print(f"Atlas: {counts['checked']}/1253; failures={counts['failures']}", flush=True)
                summary = {"status": "PASS" if counts["checked"] == 1253 and counts["failures"] == 0 and not errors else "FAIL",
                           "counts": counts, "page_errors": errors, "chromium": browser.version,
                           "networkx": nx.__version__, "numpy": np.__version__,
                           "input_sha256": hashlib.sha256((out/"atlas_inputs.json").read_bytes()).hexdigest(),
                           "source": "NetworkX 3.4.2 bundled Graph Atlas, Read and Wilson (1998)",
                           "scope": "All unweighted simple undirected graphs up to 7 nodes; no claim for all weighted/large graphs",
                           "reference": "NumPy eigvalsh is numerical; Fraction checks are exact for these integer graphs"}
                write_json(out/"atlas_summary.json", summary)
                return summary
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
