"""One predeclared bounded simulation; write a freeze BEFORE any target draw."""
import hashlib
import itertools
import json
import platform
import sys
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import binomtest
from domain import (chronological, endpoints, exact_summary, full_relation_squared,
                    order_count, probability_limits, sample_diamond)

HERE = Path(__file__).resolve().parent


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def run():
    contract = json.loads((HERE/"contract.json").read_text())
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE/"results"
    output.mkdir(parents=True, exist_ok=False)
    hashes = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in contract["frozen_files"]}
    save(output/"freeze.json", {"created_unix": time.time(), "files_sha256": hashes,
         "meaning": "Local source fixation before new target samples; not external preregistration"})
    start = time.perf_counter()
    alpha = contract["alpha_interval"]
    all_cells = list(itertools.product(contract["dimensions"], contract["background_counts"],
                                     enumerate(contract["true_theta"]), enumerate(contract["placements"])))
    gate = contract["familywise_implementation_check_alpha"]/(len(all_cells)*2)
    counts, summaries = [], []
    for d, m, (ti, theta), (pi, placement) in all_cells:
        rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([contract["seed"], d, m, ti, pi])))
        p, q = endpoints(d, theta, placement, contract["boost_rapidity"], contract["shift_x"])
        replicate_k = []
        near_boundary = 0
        full_check = None
        for first in range(0, contract["replicates_per_cell"], contract["batch_size"]):
            b = min(contract["batch_size"], contract["replicates_per_cell"]-first)
            points = sample_diamond(rng, (b, m), d)
            if not np.all(abs(points[..., 0])+np.linalg.norm(points[..., 1:], axis=-1) <= 0.5+1e-15):
                raise AssertionError("sampler escaped outer diamond")
            margin_p = points[..., 0]-p[0]-np.linalg.norm(points[..., 1:]-p[1:], axis=-1)
            margin_q = q[0]-points[..., 0]-np.linalg.norm(q[1:]-points[..., 1:], axis=-1)
            near_boundary += int(np.count_nonzero((abs(margin_p) <= contract["numerical_margin_warning"]) | (abs(margin_q) <= contract["numerical_margin_warning"])))
            ks = np.count_nonzero((margin_p > 0) & (margin_q > 0), axis=1)
            replicate_k.extend(ks.tolist())
            if first == 0 and m == 256:
                all_points = np.vstack((p, q, points[0]))
                c = full_relation_squared(all_points)
                order_k, order_m = order_count(c, [0, 1])
                if order_k != int(ks[0]) or order_m != m:
                    raise AssertionError("full relation and direct interval counter disagree")
                sys.path.insert(0, str(HERE.parent/"lorentz_proper_time"))
                from proper_core import features
                packet = {"N": m+2, "marks": [0, 1], "relation_rows": ["".join("1" if v else "0" for v in row) for row in c]}
                legacy = features(packet)
                if legacy["K"] != order_k:
                    raise AssertionError("existing order extractor mismatch")
                full_check = {"K": order_k, "m": m, "existing_extractor_K": legacy["K"], "status": "PASS"}
        ks = np.asarray(replicate_k)
        theory = exact_summary(d, m, theta, alpha)
        lo, hi = probability_limits(m, alpha)
        a = theta**d
        covered = (lo[ks] <= a) & (a <= hi[ks])
        estimate = (ks/m)**(1/d)
        tests = {"interval_count_p": float(binomtest(int(ks.sum()), len(ks)*m, a).pvalue),
                 "coverage_p": float(binomtest(int(covered.sum()), len(ks), min(1.0, theory["coverage"])).pvalue)}
        passed = all(pvalue >= gate for pvalue in tests.values()) and near_boundary == 0
        key = f"d{d}_m{m}_theta{theta:g}_{placement}"
        row = {"cell": key, "d": d, "m": m, "theta": theta, "placement": placement,
               "replicates": len(ks), "empirical_bias": float(np.mean(estimate-theta)),
               "empirical_rmse": float(np.sqrt(np.mean((estimate-theta)**2))),
               "empirical_coverage": float(np.mean(covered)), "coverage_count": int(covered.sum()),
               "empirical_zero_fraction": float(np.mean(ks == 0)), "total_K": int(ks.sum()),
               "wrong_sqrt_rmse": float(np.sqrt(np.mean((np.sqrt(ks/m)-theta)**2))) if d != 2 else None,
               "theory": theory, "tests": tests, "bonferroni_threshold": gate,
               "near_boundary_backgrounds": near_boundary, "full_order_crosscheck": full_check,
               "implementation_check": "PASS" if passed else "INCONCLUSIVE_FOR_IMPLEMENTATION"}
        counts.append({"cell": key, "K": replicate_k})
        summaries.append(row)
        print(f"{key}: RMSE={row['empirical_rmse']:.6f}, coverage={row['empirical_coverage']:.4f}, {row['implementation_check']}", flush=True)
    analytic = [exact_summary(d, m, theta, alpha) for d, m, theta in itertools.product(contract["dimensions"], contract["analytic_grid"]["m"], contract["analytic_grid"]["theta"])]
    result = {"scope": contract["scope"], "status": "CONDITIONAL_FLAT_MODEL_CHECK_PASSED" if all(r["implementation_check"] == "PASS" for r in summaries) else "INCONCLUSIVE_FOR_IMPLEMENTATION",
              "replicates_total": sum(r["replicates"] for r in summaries),
              "backgrounds_total": sum(r["replicates"]*r["m"] for r in summaries),
              "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
              "elapsed_seconds": time.perf_counter()-start, "cells": summaries, "analytic_grid": analytic}
    save(output/"counts.json", counts)
    save(output/"summary.json", result)
    lines = ["# Bedingte Eigenzeitschätzung in flachen Diamanten", "", f"Status: **{result['status']}**.", "",
             "Ein fester lokaler Lauf, keine externe Replikation. Die nominalen 95%-Intervalle beruhen auf dem Binomialmodell. Keine Aussage über gekrümmte Raumzeiten, unbekannte Stichprobengesetze oder industrielle Leistung.", "",
             f"{result['replicates_total']:,} unabhängige Punktwolken, {result['backgrounds_total']:,} Hintergrundpunkte, 24 Zellen. Laufzeit {result['elapsed_seconds']:.2f} s auf dieser Maschine; kein Leistungsvergleich.", "",
             "Die Binomialformeln sind analytisch exakt; ihre Summen und Quantile werden in float64 ausgewertet. Empirische Deckung darf zufällig unter 95% liegen und wird gegen die tatsächliche konservative Modelldeckung geprüft.", "",
             "| d | m | theta | Lage | RMSE MC | RMSE Modell | Deckung MC | Deckung Modell |", "|---|---|---|---|---|---|---|---|"]
    for r in summaries:
        lines.append(f"| {r['d']} | {r['m']} | {r['theta']} | {r['placement']} | {r['empirical_rmse']:.6f} | {r['theory']['rmse']:.6f} | {r['empirical_coverage']:.4f} | {r['theory']['coverage']:.4f} |")
    lines += ["", "## Auflösungsgrenze", "", "| d | m | theta | E[K] | P(K=0) | obere 95%-Grenze bei K=0 |", "|---|---|---|---|---|---|"]
    for r in analytic:
        if r["m"] == 256 and r["theta"] == 0.1:
            lines.append(f"| {r['d']} | {r['m']} | {r['theta']} | {r['expected_K']:.6f} | {r['zero_probability']:.6f} | {r['theta_upper_if_zero']:.6f} |")
    lines += ["", "Eine hohe Deckung bei kleinen Intervallen bedeutet keine hohe Genauigkeit: breite Intervalle können korrekt sein, obwohl die Punktschätzung meistens null ist.", "", "## Kontrollen und Grenze", "", "48 vorab festgelegte zweiseitige Binomialtests, Bonferroni-Familienniveau 1%. Alle p-Werte bleiben in summary.json. Zwölf volle Relationsmatrizen wurden getrennt aufgebaut, auf strikte Ordnung geprüft und mit dem vorhandenen Merkmalsextraktor verglichen. Die restlichen Wolken werden nur über die beiden Kegeltests gezählt; dies ist kein Laufzeitbenchmark vollständiger Ordnungsanalysen.", "", "freeze.json fixiert Quellen vor den neuen Ziehungen. counts.json enthält alle K-Werte; Seeds und Generator stehen im Vertrag. verify.py prüft Rohzählungen, Quantilinversion, Kausalitäts-Gegenbeispiele und die Quellenbindung. Ein sauberer diskreter Poset zertifiziert keine Minguzzi-Kontinuumsbedingung.", ""]
    (output/"RESULTS.md").write_text("\n".join(lines))


if __name__ == "__main__":
    run()
