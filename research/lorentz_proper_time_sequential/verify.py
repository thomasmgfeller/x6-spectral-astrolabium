"""Verify predictable updates, stopping loss, archived counts, rank calibration."""
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy.stats import binomtest
from sequential import Context, SequentialTime, stitched_bound
from chains import height, heights_from_points, rank_pvalue
from domain import full_relation_squared

HERE = Path(__file__).resolve().parent


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def must_reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("invalid input accepted")


def design_checks():
    context = Context("diamond", "pair", 4, .2, 4, 64)
    stream = SequentialTime(context)
    # Literal observations independently reconstruct the predictable squared residuals.
    history, variance = [], 0.
    for block in ([0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]):
        prediction = sum(history)/len(history) if history else 0.
        variance += sum((x-prediction)**2 for x in block)
        stream.append_counts(sum(block), start_index=len(history), context=context)
        history.extend(block)
        check(abs(stream.variance-variance) < 1e-14, "predictable block residual identity")
    must_reject(lambda: stream.append_counts(1, start_index=0, context=context))
    must_reject(lambda: stream.append_counts(1, start_index=stream.n, context=replace(context, domain_id="changed")))
    must_reject(lambda: stream.append_counts(5, start_index=stream.n, context=context))
    must_reject(lambda: replace(context, sampling_law="unknown_inhomogeneous"))
    # Verify relative-error certificate at both extrema, without implementation helper.
    for low, high in [(0.09, .11), (.3, .5), (1e-10, 2e-10)]:
        middle = 2*low*high/(low+high)
        r = (high-low)/(high+low)
        check(abs((middle/low-1)-r) < 1e-14 and abs((1-middle/high)-r) < 1e-14, "relative minimax midpoint identity")
    chain = np.triu(np.ones((6, 6), dtype=bool), 1)
    check(height(chain) == 6 and height(np.zeros((6, 6), dtype=bool)) == 1, "height conventions")
    points = np.array([[[-.4, 0.], [-.1, 0.], [.1, .1], [.4, 0.]],
                       [[-.3, .1], [0., -.2], [0., .2], [.3, .1]]])
    oracle = heights_from_points(points)
    for i in range(len(points)):
        check(height(full_relation_squared(points[i])) == oracle[i], "independent chain solver")
    perm = [2, 0, 3, 1]
    c = full_relation_squared(points[0])
    check(height(c[np.ix_(perm, perm)]) == height(c), "height relabel invariance")
    # Exact enumeration of a tiny discrete null proves tie handling is conservative here.
    rejection_probability = 0.
    import itertools
    for sample in itertools.product((1, 2, 3), repeat=4):
        p = rank_pvalue(sample[0], sample[1:])
        rejection_probability += (p <= .5)/3**4
    check(rejection_probability <= .5+1e-14, "conservative tied ranks")
    check(rank_pvalue(2, [2]*255) == 1 and rank_pvalue(100, [2]*255) == 2/256, "rank endpoints")
    check(float(stitched_bound(0, .0125)) == float(stitched_bound(1, .0125)), "variance floor")
    check(float(stitched_bound(100, .0125)) > float(stitched_bound(100, .025)), "two-sided allocation increases bound")
    return {"status": "PASS", "predictable_residuals": True, "context_and_duplicate_rejection": True,
            "relative_error_identity": True, "independent_chain_solver": True,
            "rank_ties": True, "two_tail_error_allocation": True}


def verify():
    design = design_checks()
    if len(sys.argv) > 1 and sys.argv[1] == "--design-only":
        print(json.dumps(design, indent=2)); return
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE/"results"
    contract = json.loads((HERE/"contract.json").read_text())
    frozen = json.loads((output/"freeze.json").read_text())
    for name, digest in frozen["sha256"].items():
        check(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, "source modified after freeze: "+name)
    result = json.loads((output/"summary.json").read_text())
    replayed, rank_checks = 0, 0
    with np.load(output/"batch_counts.npz", allow_pickle=False) as raw:
        for study in result["stream_results"]+[result["dependence_negative_control"]]:
            cell = study["cell"]
            counts = raw[cell["id"]]
            check(counts.shape == (cell["max_n"]//cell["batch"], cell["replicates"]), "count archive dimensions")
            check(np.all((counts >= 0) & (counts <= cell["batch"])), "count archive range")
            cumulative = np.cumsum(counts, axis=0, dtype=np.int64)
            # Selected individual replays test the public scalar controller against batch simulation.
            for index in (0, 1, 2, cell["replicates"]-1):
                context = Context(cell["id"], "fixed", cell["d"], cell["scale"], cell["batch"], cell["max_n"], contract["alpha_time"], contract["relative_tolerance"])
                stream = SequentialTime(context)
                for inc in counts[:, index]:
                    stream.append_counts(int(inc), start_index=stream.n, context=context)
                    if stream.status != "SAMPLING":
                        break
                ref = study["records"][index]
                check(stream.status == ref["status"] and stream.n == ref["n"] and stream.k == ref["K"], "scalar stopping replay")
                if ref["estimate"] is not None:
                    check(abs(stream.snapshot()["certified_point_estimate"]-ref["estimate"]) < 1e-13, "scalar estimate replay")
                replayed += 1
            check(sum(r["ever_miscovered_on_full_check_grid"] for r in study["records"]) == study["ever_miscoverage_count"], "miscoverage count")
            check(sum(r["status"] == "PRECISION_REACHED" for r in study["records"]) == study["precision_reached"], "stop count")
            for index, record in enumerate(study["records"]):
                check(cumulative[record["n"]//cell["batch"]-1, index] == record["K"], "all stopped K from raw counts")
            pv = binomtest(study["ever_miscoverage_count"], cell["replicates"], contract["alpha_time"], alternative="greater").pvalue
            check(abs(pv-study["excess_miscoverage_test_p"]) < 1e-14, "miscoverage gate")
    for study in result["chain_results"]:
        refs = study["reference_heights"]
        check(len(refs) == contract["chain_trials_per_cell"], "reference group count")
        for name, assessment in study["assessments"].items():
            pvalues = []
            for h, bank in zip(assessment["heights"], refs):
                check(len(bank) == contract["chain_reference_count"] and all(1 <= x <= study["K"] for x in bank), "reference height range")
                # Direct ranks, separate from diagnostic function.
                pvalues.append(min(1., 2*(1+min(sum(x <= h for x in bank), sum(x >= h for x in bank)))/(len(bank)+1)))
                rank_checks += 1
            check(pvalues == assessment["p_values"], "rank recomputation")
            check(sum(p <= contract["alpha_chain"] for p in pvalues) == assessment["rejections"], "rejection recount")
        pv = binomtest(study["assessments"]["flat_null"]["rejections"], study["trials"], contract["alpha_chain"], alternative="greater").pvalue
        check(abs(pv-study["excess_null_rejection_test_p"]) < 1e-14, "null gate")
    demo = result["integration_demo"]
    context = Context(**demo["context"])
    stream = SequentialTime(context)
    for count in demo["batches"]:
        stream.append_counts(count, start_index=stream.n, context=context)
    check(stream.snapshot() == demo["time"], "geometric count replay")
    c = full_relation_squared(np.asarray(demo["inner_points"]))
    check(len(c) == stream.k and height(c) == demo["chain"]["height"], "geometric chain replay")
    check(demo["chain"]["curvature_identified"] is False, "no curvature overclaim")
    pvalues = [s["excess_miscoverage_test_p"] for s in result["stream_results"]]+[s["excess_null_rejection_test_p"] for s in result["chain_results"]]
    threshold = contract["implementation_gate_family_alpha"]/contract["implementation_gate_tests"]
    passed = all(p >= threshold for p in pvalues)
    check((result["status"] == "DECLARED_SEQUENTIAL_REFERENCE_CHECK_PASSED") == passed, "overall gate")
    report = {"verification": "PASS", "design": design, "source_freeze": "UNCHANGED",
              "scalar_stream_replays": replayed, "chain_rank_recomputations": rank_checks,
              "geometric_integration_replay": "PASS", "scientific_status": result["status"],
              "curvature_detection": "NOT_ESTABLISHED", "external_replication": False}
    save = json.dumps(report, indent=2)+"\n"
    (output/"verification.json").write_text(save)
    print(save)


if __name__ == "__main__":
    verify()
