"""Predeclared Monte Carlo checks and one real coordinate-stream integration."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import numpy as np
import scipy
from scipy.stats import binomtest
from sequential import Context, SequentialTime, estimate_interval, probability_interval
from chains import diagnose_at_stop, rank_pvalue, sample_heights
from domain import endpoints, full_relation_squared, chronological, sample_diamond

HERE = Path(__file__).resolve().parent


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def rng_for(seed, *key):
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed, *key])))


def stream_study(cell, contract, rng, dependent=False):
    r, b, p = cell["replicates"], cell["batch"], cell["p"]
    k = np.zeros(r, dtype=np.int64)
    v = np.zeros(r)
    low, high = np.zeros(r), np.ones(r)
    ever_bad = np.zeros(r, dtype=bool)
    stopped = np.zeros(r, dtype=np.int64)
    stop_k = np.zeros(r, dtype=np.int64)
    stop_estimate = np.zeros(r)
    stop_radius = np.ones(r)
    precision = np.zeros(r, dtype=bool)
    empty = np.zeros(r, dtype=bool)
    counts = []
    repeating = rng.binomial(1, p, size=r) if dependent else None
    true_time = cell["scale"]*p**(1/cell["d"])
    for n in range(b, cell["max_n"]+1, b):
        pred = k/(n-b) if n > b else np.zeros(r)
        inc = repeating*b if dependent else rng.binomial(b, p, size=r)
        counts.append(inc.astype(np.uint16))
        v += inc*(1-pred)**2+(b-inc)*pred**2
        k += inc
        lo, hi = probability_interval(k, n, v, contract["alpha_time"])
        low, high = np.maximum(low, lo), np.minimum(high, hi)
        ever_bad |= (low > p) | (high < p)
        new_empty = (stopped == 0) & (low > high)
        stopped[new_empty], stop_k[new_empty], empty[new_empty] = n, k[new_empty], True
        tl, th, est, radius = estimate_interval(low, high, cell["d"], cell["scale"])
        new_stop = (stopped == 0) & (tl > 0) & (radius < contract["relative_tolerance"])
        stopped[new_stop], stop_k[new_stop] = n, k[new_stop]
        stop_estimate[new_stop], stop_radius[new_stop], precision[new_stop] = est[new_stop], radius[new_stop], True
    unfinished = stopped == 0
    stopped[unfinished], stop_k[unfinished] = cell["max_n"], k[unfinished]
    stop_estimate[unfinished], stop_radius[unfinished] = est[unfinished], radius[unfinished]
    bad_report = precision & (np.abs(stop_estimate-true_time) > contract["relative_tolerance"]*true_time)
    p_gate = float(binomtest(int(ever_bad.sum()), r, contract["alpha_time"], alternative="greater").pvalue)
    records = [{"n": int(stopped[i]), "K": int(stop_k[i]), "estimate": float(stop_estimate[i]) if not empty[i] else None,
                "relative_radius": float(stop_radius[i]) if not empty[i] else None,
                "status": "PRECISION_REACHED" if precision[i] else "EMPTY_CONFIDENCE_SEQUENCE" if empty[i] else "BUDGET_EXHAUSTED",
                "ever_miscovered_on_full_check_grid": bool(ever_bad[i]), "bad_precision_report": bool(bad_report[i])} for i in range(r)]
    row = {"cell": cell, "true_time": true_time, "precision_reached": int(precision.sum()),
           "budget_exhausted": int(unfinished.sum()), "empty_sequence": int(empty.sum()),
           "ever_miscoverage_count": int(ever_bad.sum()), "bad_precision_report_count": int(bad_report.sum()),
           "precision_stop_n_median": float(np.median(stopped[precision])) if precision.any() else None,
           "precision_stop_n_q10_q90": np.quantile(stopped[precision], [.1, .9]).tolist() if precision.any() else None,
           "precision_stop_K_median": float(np.median(stop_k[precision])) if precision.any() else None,
           "excess_miscoverage_test_p": p_gate, "records": records}
    return row, np.stack(counts)


def chain_study(d, k, contract, rng):
    r, B = contract["chain_trials_per_cell"], contract["chain_reference_count"]
    all_h = sample_heights(rng, d, k, r*(B+1)).reshape(r, B+1)
    observed, refs = all_h[:, 0], all_h[:, 1:]
    compressed = sample_heights(rng, d, k, r, compression=0.1)
    sets = {"flat_null": observed, "flat_density_compression": compressed,
            "complete_chain": np.full(r, k), "antichain": np.ones(r, dtype=int)}
    assessments = {}
    for name, values in sets.items():
        pvals = [rank_pvalue(int(h), bank) for h, bank in zip(values, refs)]
        assessments[name] = {"heights": values.tolist(), "p_values": pvals,
                             "rejections": sum(p <= contract["alpha_chain"] for p in pvals)}
    gate = float(binomtest(assessments["flat_null"]["rejections"], r, contract["alpha_chain"], alternative="greater").pvalue)
    return {"d": d, "K": k, "trials": r, "references_per_trial": B,
            "reference_heights": refs.tolist(), "assessments": assessments,
            "excess_null_rejection_test_p": gate, "curvature_identified": False}


def integration_demo(contract):
    rng = rng_for(contract["seed"], 3, 0)
    context = Context("fixed-local-diamond-S=0.2T", "independent-fixed-central-pq", 4, 0.2, 32, 16384,
                      contract["alpha_time"], contract["relative_tolerance"])
    state = SequentialTime(context)
    p, q = endpoints(4, 0.5, "central")
    inner, batches = [], []
    while state.status == "SAMPLING":
        points = sample_diamond(rng, (context.batch_size,), 4)
        inside = chronological(p, points) & chronological(points, q)
        inner.extend(points[inside].tolist())
        count = int(inside.sum())
        batches.append(count)
        state.append_counts(count, start_index=state.n, context=context)
    relation = full_relation_squared(np.asarray(inner))
    diagnostic = diagnose_at_stop(state, relation, rng=rng_for(contract["seed"], 3, 1),
                                  alpha=contract["alpha_chain"], reference_count=contract["chain_reference_count"])
    return {"context": asdict(context), "true_time": 0.1, "batches": batches,
            "inner_points": inner, "time": state.snapshot(), "chain": diagnostic}


def run():
    contract = json.loads((HERE/"contract.json").read_text())
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE/"results"
    output.mkdir(parents=True, exist_ok=False)
    freeze = {"created_unix": time.time(), "meaning": "Local source fixation before new target samples; not external preregistration",
              "sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in contract["freeze_files"]}}
    save(output/"freeze.json", freeze)
    start = time.perf_counter()
    streams, raw = [], {}
    for i, cell in enumerate(contract["stream_cells"]):
        row, counts = stream_study(cell, contract, rng_for(contract["seed"], 1, i))
        streams.append(row); raw[cell["id"]] = counts
        print(f"{cell['id']}: reached={row['precision_reached']}/{cell['replicates']}, median n={row['precision_stop_n_median']}, ever-miscoverage={row['ever_miscoverage_count']}", flush=True)
    negative_cell = {"id": "dependent_negative_control", "d": 4, "p": 0.5, "scale": 1., "batch": 32, "max_n": 16384, "replicates": 128}
    dependent, counts = stream_study(negative_cell, contract, rng_for(contract["seed"], 1, 99), dependent=True)
    raw[negative_cell["id"]] = counts
    chains = []
    for d in contract["chain_dimensions"]:
        for k in contract["chain_K"]:
            row = chain_study(d, k, contract, rng_for(contract["seed"], 2, d, k))
            chains.append(row)
            print(f"chain d={d} K={k}: null flags={row['assessments']['flat_null']['rejections']}, flat-density flags={row['assessments']['flat_density_compression']['rejections']}", flush=True)
    demo = integration_demo(contract)
    pvalues = [r["excess_miscoverage_test_p"] for r in streams]+[r["excess_null_rejection_test_p"] for r in chains]
    gate = contract["implementation_gate_family_alpha"]/contract["implementation_gate_tests"]
    status = "DECLARED_SEQUENTIAL_REFERENCE_CHECK_PASSED" if all(p >= gate for p in pvalues) else "INCONCLUSIVE_FOR_IMPLEMENTATION"
    summary = {"status": status, "seconds": time.perf_counter()-start,
               "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
               "implementation_gate_threshold": gate, "implementation_gate_pvalues": pvalues,
               "stream_results": streams, "dependence_negative_control": dependent,
               "chain_results": chains, "integration_demo": demo,
               "curvature_detection_status": "NOT_ESTABLISHED_AND_NOT_IDENTIFIABLE_WITH_UNKNOWN_SAMPLING",
               "external_replication": False}
    np.savez_compressed(output/"batch_counts.npz", **raw)
    save(output/"summary.json", summary)
    save(output/"integration_demo.json", demo)
    lines = ["# Sequenzielle Eigenzeit und bedingte Ordnungsdiagnostik", "", f"Status: **{status}**.", "",
             "Zeituniforme Absicherung nach Howard et al. unter festem Stichprobengesetz; keine Krümmungsidentifikation. Intern ausgeführt und geprüft, keine externe Replikation.", "",
             "Zeitfehlerbudget 2,5%, einmalige Kettendiagnostik 2,5%; unter dem deklarierten flachen Modell gemeinsame Fehlereigniswahrscheinlichkeit höchstens 5% per Union Bound. Ein nicht signifikanter Kettentest beweist das Modell nicht.", "",
             "## Sequenzielle Monte-Carlo-Kontrolle", "", "Die Hauptläufe simulieren Binomial-Zählungen unabhängiger Beobachtungsblöcke, keine vollständigen Punktwolken. Ein zusätzlicher Lauf prüft den tatsächlichen Koordinaten-/Relationsdatenweg. Die zeituniforme Garantie stammt aus dem Satz; die Monte-Carlo-Kontrolle beobachtet nur die festgelegten Batch-Endpunkte.", "",
             "| Fall | Läufe | Präzision erreicht | Median n bei Erreichen | Median K | Pfade mit Fehlüberdeckung |", "|---|---|---|---|---|---|"]
    for r in streams:
        lines.append(f"| {r['cell']['id']} | {r['cell']['replicates']} | {r['precision_reached']} | {r['precision_stop_n_median']} | {r['precision_stop_K_median']} | {r['ever_miscoverage_count']} |")
    lines += ["", "Die Medianwerte sind beobachtete Stichprobenbedarfe, keine garantierten Budgets. Die globale und lokale Referenz verwenden unterschiedliche Batchgrößen. Früher berechnete Feststichprobenbudgets sind keine Budgets dieser breiteren sequenziellen Schranke.", "", "## Kettendiagnostik bei festem K", "", "| d | K | Nullmodell-Warnungen / 128 | Dichtestörung im flachen Raum / 128 | Kette / 128 | Antikette / 128 |", "|---|---|---|---|---|---|"]
    for r in chains:
        a = r["assessments"]
        lines.append(f"| {r['d']} | {r['K']} | {a['flat_null']['rejections']} | {a['flat_density_compression']['rejections']} | {a['complete_chain']['rejections']} | {a['antichain']['rejections']} |")
    lines += ["", "Jeder Nulltest verwendet eine frische unabhängige Referenzbank von 255 Höhen. Zweiseitige Rang-p-Werte schließen Bindungen konservativ ein. Die Dichtestörung ändert die räumlichen Koordinaten, nicht die flache Metrik: Warnungen in dieser Kontrolle sind ausdrücklich kein Krümmungsnachweis.", "",
              "## Integrierter Geometrielauf", "", f"Status {demo['time']['status']}; n={demo['time']['n']}, K={demo['time']['K']}, Eigenzeitintervall {demo['time']['time_interval']}, Punktschätzung {demo['time']['certified_point_estimate']:.8f} bei wahrem Wert 0,1. Kettendiagnostik: {demo['chain']['status']}.", "",
              "## Annahmenverletzung", "", f"Beim absichtlich abhängigen Kontrollstrom wird ein einmal gezogener Wert endlos wiederholt. {dependent['ever_miscoverage_count']} von 128 Pfaden verlieren die Überdeckung. Diese Kontrolle liegt außerhalb der Garantie und zeigt, warum Metadaten oder Software allein kein gültiges Stichprobengesetz herstellen.", "",
              f"Laufzeit: {summary['seconds']:.2f} s, kein kontrollierter Leistungsvergleich. Quellenfixierung in freeze.json; Zählblöcke in batch_counts.npz; vollständige Referenzhöhen, Stoppergebnisse und p-Werte in summary.json. Keine nachträgliche Wahl eines günstigeren Parameters oder Seeds.", ""]
    (output/"RESULTS.md").write_text("\n".join(lines))


if __name__ == "__main__":
    run()
