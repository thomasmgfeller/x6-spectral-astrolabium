"""Paired residual-domain injection/recovery on irregular EPTA observing times."""
import argparse
import csv
import gzip
import io
import json
import math
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from agent.epta_timing import CREDIT, HERE, PROTOCOL as P, STUDY, acquire, reconstruct, unpack
from agent.run_agent import require
from agent.source_transport import sha256

ARMS = ("identity", "cspp")
Z95 = 1.959963984540054


def history_taps():
    code = ("import {analyze,makeModel} from './app/causal-stability/engine.mjs';"
            "console.log(JSON.stringify(analyze(makeModel({preset:'cspp',n:5,theta:21})).transfer));")
    taps = np.array(json.loads(subprocess.check_output(["node", "--input-type=module", "-e", code], cwd=HERE)))
    require(len(taps) == 3 and abs(taps.sum()) > 1e-10, "Unusable CSPP history transfer")
    return taps


def hellings_downs(sky):
    cosines = np.clip(sky @ sky.T, -1, 1)
    x = (1 - cosines) / 2
    hd = 0.5 - x/4 + 1.5*x*np.log(np.maximum(x, 1e-100))
    np.fill_diagonal(hd, 1)
    return hd, np.degrees(np.arccos(cosines))


def prepare(obs, start, span, taps):
    t = obs["bat"]
    w = 1 / obs["error"]**2
    _, group = np.unique(np.floor(t), return_inverse=True)
    total = np.bincount(group, weights=w)
    def group_mean(values):
        return np.bincount(group, weights=w*values) / total
    epochs = group_mean(t)
    u = (t-start)/span
    phase = 2*np.pi*u[:, None]*np.arange(1, P["modes"]+1)
    native = np.concatenate([np.sin(phase), np.cos(phase)], axis=1)
    basis = np.column_stack([group_mean(col) for col in native.T])
    time_columns = np.column_stack([group_mean(u**k) for k in range(3)])
    past = []
    mask = np.ones(len(epochs), dtype=bool)
    for lag in P["lags_days"][:-1]:
        anchor = epochs-lag
        ids = np.searchsorted(epochs, anchor, side="right")-1
        mask &= (ids >= 0) & (anchor-epochs[ids] <= P["max_extra_lag_days"])
        past.append(ids)
    now = np.flatnonzero(mask)
    columns = np.column_stack([time_columns, basis])[mask]
    weighted = columns * np.sqrt(total[mask, None])
    require(np.linalg.matrix_rank(weighted) == weighted.shape[1], "Insufficient sampling for mode recovery")
    fit = np.linalg.pinv(weighted)[3:] * np.sqrt(total[mask])
    identity = np.zeros((fit.shape[0], len(epochs)))
    identity[:, now] = fit
    candidate = np.zeros_like(identity)
    # Repeated past anchors must accumulate, including when several rows share an epoch.
    for idx, scale in zip([past[0][mask], past[1][mask], now], taps):
        np.add.at(candidate.T, idx, scale*fit.T)
    arms = np.stack([identity, candidate])
    return {"name": obs["name"], "maps": arms @ basis, "white": arms/np.sqrt(total),
            "measured": arms @ group_mean(obs["us"]), "epochs": len(epochs), "used": len(now), "fit_condition": float(np.linalg.cond(weighted))}


def regression_pairs(values, pairs):
    a, b = pairs
    return np.einsum("bapf,bapf->bap", values[:, :, a, :], values[:, :, b, :]) / 2


def simulate(pulsars, correlation, pairs, stream):
    size = P["sample_sizes"][stream]
    rng = np.random.Generator(np.random.PCG64(P["streams"][stream]))
    k = np.arange(1, P["modes"]+1)
    power = k**P["residual_power_slope"]
    sd = np.tile(np.sqrt(power/power.sum()), 2)
    chol = np.linalg.cholesky(correlation)
    maps = np.stack([p["maps"] for p in pulsars], axis=1)
    measured = np.stack([p["measured"] for p in pulsars], axis=1)
    baseline = regression_pairs(measured[None], pairs)
    output = []
    for offset in range(0, size, 64):
        n = min(64, size-offset)
        shape = (n, len(pulsars), len(sd))
        if stream == "observed_replay":
            coeffs = np.broadcast_to(measured, (n,) + measured.shape).copy()
        else:
            red = rng.normal(size=shape)*sd*P["red_rms_us"]
            coeffs = np.einsum("apij,bpj->bapi", maps, red)
            for j, p in enumerate(pulsars):
                noise = rng.normal(size=(n, p["epochs"]))
                coeffs[:, :, j, :] += np.einsum("aij,bj->bai", p["white"], noise, optimize=True)
        if stream in ("observed_replay", "injection_test"):
            signal = np.einsum("ij,bjk->bik", chol, rng.normal(size=shape))*sd*P["injected_rms_us"]
            coeffs += np.einsum("apij,bpj->bapi", maps, signal)
        cross = regression_pairs(coeffs, pairs)
        if stream == "observed_replay":
            cross -= baseline
        output.append(cross)
    return np.concatenate(output)


def proportion(decisions):
    n = len(decisions)
    p = float(np.mean(decisions))
    den = 1+Z95**2/n
    centre = (p+Z95**2/(2*n))/den
    radius = Z95*np.sqrt(p*(1-p)/n+Z95**2/(4*n*n))/den
    return {"hits": int(np.sum(decisions)), "n": n, "fraction": p, "wilson95": [centre-radius, centre+radius]}


def evaluate(obs):
    start, stop = min(s["bat"].min() for s in obs), max(s["bat"].max() for s in obs)
    raw = history_taps()
    taps = raw/raw.sum()
    models = [prepare(s, start, stop-start, taps) for s in obs]
    hd, angles = hellings_downs(np.array([s["sky"] for s in obs]))
    pairs = np.triu_indices(len(obs), 1)
    angular = hd[pairs]
    score_weights = angular/(angular @ angular)
    # Independent calibration, evaluation, and replay streams, paired arms within each.
    scores = {}
    for stream in ("calibration", "null_test", "injection_test"):
        scores[stream] = simulate(models, hd, pairs, stream) @ score_weights
    ncal = len(scores["calibration"])
    rank = math.ceil((1-P["alpha"])*(ncal+1))
    cutoff = np.sort(scores["calibration"], axis=0)[rank-1]
    null_detect = scores["null_test"] > cutoff
    alt_detect = scores["injection_test"] > cutoff
    diff = alt_detect[:, 1].astype(int)-alt_detect[:, 0].astype(int)
    delta, margin = float(diff.mean()), Z95*diff.std(ddof=1)/np.sqrt(len(diff))
    # Descriptive ROC comparison added after the frozen decision. Match the observed
    # null count in both arms, without using signal trials to select a threshold.
    target = math.floor(P["alpha"]*len(null_detect))
    roc_cut = np.sort(scores["null_test"], axis=0)[-target-1]
    roc_null = scores["null_test"] > roc_cut
    require(np.all(roc_null.sum(axis=0) == target), "Tied scores at the empirical ROC cutoff")
    roc_hits = scores["injection_test"] > roc_cut
    roc_diff = roc_hits[:,1].astype(int)-roc_hits[:,0].astype(int)
    roc_delta = float(roc_diff.mean())
    roc_margin = Z95*roc_diff.std(ddof=1)/np.sqrt(len(roc_diff))
    matched = {"condition": "descriptive, thresholds chosen on null_test, evaluated on injection_test",
               "false_alarms_per_arm": target, "null_trials": len(roc_null),
               "signal_trials": len(roc_hits), "paired_difference": roc_delta,
               "conditional_mc95": [roc_delta-roc_margin, roc_delta+roc_margin],
               "arms": {key: {"detections": int(roc_hits[:,j].sum()), "threshold_us2": float(roc_cut[j])}
                        for j,key in enumerate(ARMS)}}
    replay = simulate(models, hd, pairs, "observed_replay")/P["injected_rms_us"]**2
    recovered = replay.mean(axis=0)
    arms = {}
    for j, arm in enumerate(ARMS):
        fractions = replay[:, j] @ score_weights
        mean = float(fractions.mean())
        half = Z95*fractions.std(ddof=1)/np.sqrt(len(fractions))
        arms[arm] = {"false_alarm": proportion(null_detect[:, j]), "detection": proportion(alt_detect[:, j]),
                     "threshold_us2": float(cutoff[j]), "power_fraction": mean, "power_mean_mc95": [mean-half, mean+half],
                     "angular_cosine": float(recovered[j] @ angular/(np.linalg.norm(recovered[j])*np.linalg.norm(angular)))}
    checks = {
        "false_alarm_intervals_cover_5pct": all(a["false_alarm"]["wilson95"][0] <= P["alpha"] <=
                                                a["false_alarm"]["wilson95"][1] for a in arms.values()),
        "paired_power_gain": bool(delta-margin > 0),
        "power_retention": 0.90 <= arms["cspp"]["power_fraction"] <= 1.10,
        "angular_shape": arms["cspp"]["angular_cosine"] >= 0.95}
    # Supplementary design diagnostic: exact Gaussian second moments at fixed times.
    # Fixed measured residuals drop out of the expectation of score(r+s)-score(r).
    k = np.arange(1, P["modes"]+1)**P["residual_power_slope"]
    variance = np.tile(k/k.sum(), 2)
    analytic = np.array([hd[a,b]*np.sum(models[a]["maps"]*models[b]["maps"]*variance, axis=(1,2))/2
                         for a,b in zip(*pairs)])
    for j, arm in enumerate(ARMS):
        arms[arm]["expected_hd_power_projection"] = float(analytic[:, j] @ score_weights)
        arms[arm]["expected_angular_cosine"] = float(analytic[:, j] @ angular /
                                             (np.linalg.norm(analytic[:, j])*np.linalg.norm(angular)))
    require(np.allclose(analytic[:, 0], angular, rtol=1e-7, atol=1e-9), "Identity recovery control failed")
    pair_rows = [{"p": obs[a]["name"], "q": obs[b]["name"], "angle_deg": angles[a,b], "hd": angular[i],
                  "identity": recovered[0,i], "cspp": recovered[1,i],
                  "expected_identity": analytic[i,0], "expected_cspp": analytic[i,1]} for i,(a,b) in enumerate(zip(*pairs))]
    pulsars = [{"name": s["name"], "toas": len(s["bat"]), "wrms_us": s["wrms"], "epochs": m["epochs"],
                "retained": m["used"], "fit_condition": m["fit_condition"], "start_mjd_tcb": s["bat"][0], "end_mjd_tcb": s["bat"][-1]}
               for s,m in zip(obs, models)]
    return {"schema": "x6.epta-filter/1", "source": CREDIT, "release_sha256": P["archive_sha256"],
            "protocol_sha256": sha256(STUDY/"protocol.json"), "tempo_lock_sha256": sha256(STUDY/"tempo2.lock"),
            "engine_sha256": sha256(HERE/"app/causal-stability/engine.mjs"), "pulsars": pulsars, "raw_taps": raw.tolist(),
            "unit_sum_taps": taps.tolist(), "span_days": stop-start, "calibration_rank": rank, "arms": arms,
            "paired_detection_difference": delta, "paired_difference_mc95": [delta-margin, delta+margin],
            "pairs": pair_rows, "empirical_roc": matched, "checks": checks, "decision": "QUALIFIES" if all(checks.values()) else "DOES_NOT_QUALIFY"}


def reference_plot(obs):
    t, y = obs["bat"], obs["us"]
    group = np.floor((t-t[0])/90).astype(int)
    rows = []
    for n in np.unique(group):
        mask = group == n
        w = 1/obs["error"][mask]**2
        rows.append([round(float(np.average(t[mask], weights=w)), 4),
                     round(float(np.average(y[mask], weights=w)), 6), int(mask.sum())])
    return rows


def publish(out, obs, result):
    result["reference_90d"] = reference_plot(obs[0])
    result["numpy"] = np.__version__
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out) as temp:
        work = Path(temp)
        csv_file = work/"timing.csv.gz"
        with csv_file.open("wb") as dest, gzip.GzipFile(filename="", mode="wb", fileobj=dest, mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding="utf-8", newline="") as txt:
                writer = csv.writer(txt, lineterminator="\n")
                writer.writerow(["pulsar", "site_mjd", "barycentric_mjd_tcb", "fixed_residual_us", "toa_error_us"])
                for s in obs:
                    for sat,bat,y,err in zip(s["sat"],s["bat"],s["us"],s["error"]):
                        writer.writerow([s["name"], f"{sat:.11f}", f"{bat:.11f}", f"{y:.7f}", f"{err:.5f}"])
        digest = sha256(csv_file)
        fname = f"timing-{digest[:16]}.csv.gz"
        result["timing_csv"] = {"name": fname, "sha256": digest}
        (work/"summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
        os.replace(csv_file, out/fname)
        os.replace(work/"summary.json", out/"summary.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tempo-prefix", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--archive", type=Path, help="Optional offline copy of the pinned 39 MB Zenodo release")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        unpack(args.archive if args.archive else acquire(work), work)
        obs = reconstruct(work, args.tempo_prefix.resolve())
        result = evaluate(obs)
        publish(args.output, obs, result)
    print(result["decision"], json.dumps(result["checks"]))


if __name__ == "__main__":
    main()
