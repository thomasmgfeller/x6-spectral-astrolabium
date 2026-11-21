"""Run python -B pruefen.py [--output DIRECTORY]. Requires NumPy and SciPy."""
import argparse
import csv
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources"
sys.path[:0] = [str(SRC / "studie"),str(SRC)]
import numpy as np
import model
import density_translation_375841 as published_cells
from geometrie import Geometry, Input, enumerate_orders, exact_transport, pair_code
from numerik import check_close, deviation, evaluate, points


def read(path):
    return json.loads(path.read_text())


def complex_data(values):
    arr = np.asarray(values)
    return np.stack([arr.real,arr.imag],axis=-1).tolist()


def archived_precision():
    texts = read(SRC/"precision_375841.json")["by_type"]["375841"]
    def parse(entry):
        real, imag = entry.replace(" - "," + -").split(" + ")
        return complex(Q(real),Q(imag.replace("*I","")))
    return np.array([parse(entry) for entry in texts])*model.BETA


def compare_numeric(run, baseline, tolerance):
    precision,factor,levels = run
    pref_precision,pref_factor,reference_levels = baseline
    residuals = {"precision":check_close(precision,pref_precision,tolerance),
                 "prefactor":check_close(factor,pref_factor,tolerance),
                 "amplitude_coefficient":0.,"wavefunction_probe":0.,"gram":0.}
    for level, ref in zip(levels,reference_levels):
        for key, name in [("coefficients","amplitude_coefficient"),("wave","wavefunction_probe"),("gram","gram")]:
            residuals[name] = max(residuals[name],check_close(level[key],ref[key],tolerance))
        check_close(level["coefficients"][:,0],level["coefficients"][:,1],tolerance)
        gram = level["gram"]
        check_close(gram,gram.conj().T,tolerance)
        check_close(gram,gram[0,0],tolerance)
        assert gram[0,0].real > 0
    return residuals


def run():
    if not __debug__:
        raise RuntimeError("Use Python with assertions enabled.")
    contract_file = ROOT/"pruefvertrag.json"
    contract_hash = hashlib.sha256(contract_file.read_bytes()).hexdigest()
    assert contract_hash == (ROOT/"pruefvertrag.sha256").read_text().split()[0]
    cfg = read(contract_file)
    published = subprocess.check_output([sys.executable,"-B",str(SRC/"pruefen.py")])
    assert published == (SRC/"ergebnis.json").read_bytes()
    source_result = json.loads(published)
    centers_gold = tuple(Q(x) for x in source_result["center_p_over_M"])
    boxes_gold = tuple(tuple(map(Q,source_result["translation_intervals"][sign]))
                       for sign in ("positive","negative"))
    assert boxes_gold[0][0] > 0 > boxes_gold[1][1]
    old = tuple(cfg["reference_inner_order"])
    roles = tuple(cfg["ordered_packet_axes"])
    nodes, rel = model.support.geometry(cfg["type"])
    assert nodes == old and rel == published_cells.local_geometry()[0]
    ref = Geometry(Input(model.support.PAST,old,model.support.FUTURE,roles,frozenset(rel)))
    orders = enumerate_orders(ref)
    assert len(orders) == cfg["number_of_extensions"]
    law1 = read(SRC/"studie/weights.json")["laws"]["1:1"]
    law2 = read(SRC/"studie/chain.json")["law"]
    archived_weight = (Q(law1.get(str(cfg["type"]),0))+Q(law2.get(str(cfg["type"]),0)))/2
    assert archived_weight > 0
    radius, eta = Q(cfg["cell_halfwidth"]), Q(cfg["future_halfwidth"])
    numeric = cfg["numerical_check"]
    tolerance = numeric["absolute_plus_relative_tolerance"]
    cloud = points(numeric)
    levels = tuple(zip(numeric["inner_points"],numeric["outer_points"]))
    baseline = evaluate(ref,dict(enumerate(range(15))),old,cloud,levels,float(radius),float(eta))
    upper = np.triu_indices(3)
    archived_gap = check_close(baseline[0][upper],archived_precision(),tolerance)
    maxima = {}
    rows, controls = [], {}
    for order in orders:
        # Birth label j is the position in the complete linear extension.
        birth_order = ref.data.past + order + ref.data.future
        mapping = {v:j for j,v in enumerate(birth_order)}
        try:
            new = Geometry(ref.data.transport(mapping))
            assert all(a < b for a,b in new.data.relation)
            exact_transport(ref,new,mapping)
            assert new.endpoint_weight(law1,law2) == archived_weight
            centers = tuple(lo for lo,hi in new.charge(Q(0)) if lo == hi)
            assert centers == centers_gold and new.charge(radius) == boxes_gold
            run_new = evaluate(new,mapping,old,cloud,levels,float(radius),float(eta))
            errors = compare_numeric(run_new,baseline,tolerance)
            for key,x in errors.items():
                maxima[key] = max(maxima.get(key,0.),x)
            fine = run_new[2][-1]
            rows.append({"old_event_ids_in_birth_order":list(order),
                         "native_inner_bit_code":pair_code(new.data.inside,new.inner_edges),
                         "ordered_translation_axes_in_birth_labels":list(new.data.axes),
                         "F4":new.gravity,"endpoint_weight":str(archived_weight),
                         "center_p_over_M":list(map(str,centers)),
                         "positive_and_negative_cell_bounds":[list(map(str,p)) for p in boxes_gold],
                         "exact_transport":"PASS","max_abs":errors,
                         "amplitudes_first_future_point":complex_data(fine["coefficients"][0]),
                         "gram_common_scale":complex_data(fine["gram"])})
            if order == (4,6,5,11,12,13,14):
                wrong_axes = (mapping[6],mapping[12],mapping[13])
                wrong = tuple(lo for lo,hi in new.charge(Q(0),wrong_axes) if lo == hi)
                assert wrong != centers_gold
                controls["untransported_density_mark"] = {
                    "order":list(order),"right_axes":list(new.data.axes),"wrong_axes":list(wrong_axes),
                    "center_p_over_M":list(map(str,wrong)),"detected_by_exact_current":True}
                # Apply the wrong association of the two selector outputs. The
                # Gram is explicitly conjugated by the branch-swap permutation.
                swap = [1,0]
                swapped = fine["gram"][np.ix_(swap,swap)]
                reversed_currents = [centers[i] for i in swap]
                assert reversed_currents[0] < 0 < reversed_currents[1]
                controls["reversed_selectors"] = {
                    "order":list(order),"center_p_over_M":list(map(str,reversed_currents)),
                    "max_numeric_gram_change":check_close(swapped,fine["gram"],tolerance),
                    "exact_gram_change":"0 (equal packet images)",
                    "detected_by_signed_packets":True}
        except Exception as exc:
            raise RuntimeError(f"Failed at physical event order {order}: {exc!r}") from exc
    assert len(controls) == 2
    assert len({row["native_inner_bit_code"] for row in rows}) == len(orders)
    ref_levels = baseline[2]
    return {"status":"PASS","source_commit":cfg["source_commit"],"contract_sha256":contract_hash,
            "checked_orders":len(rows),"native_encodings":len(orders),"F4":ref.gravity,
            "source_replay_byte_identical":True,"exact_transport_residual":"0",
            "center_p_over_M":list(map(str,centers_gold)),
            "exact_gram_over_gamma":[[1,1],[1,1]],"gamma_strictly_positive":True,
            "charge_selector_preserves_null_space":False,"conditional_weight":"1",
            "fixed_endpoint_ensemble_coefficient":str(archived_weight),
            "elementary_path_factors":"unspecified in source",
            "max_abs_transport_errors":maxima,
            "baseline_precision_vs_archived_max_abs":archived_gap,
            "scalar_precision":complex_data(baseline[0]),"scalar_prefactor":complex_data(baseline[1]),
            "reference_amplitudes_first_future_point":complex_data(ref_levels[-1]["coefficients"][0]),
            "reference_gram_common_scale":complex_data(ref_levels[-1]["gram"]),
            "reference_gram_coarse_to_fine_max_abs":deviation(ref_levels[0]["gram"],ref_levels[-1]["gram"]),
            "negative_controls":controls,"scope":"PR 338 two-packet reference. P3 NOT_RUN.","rows":rows}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--output",type=Path,help="Save full JSON and compact CSV in this directory.")
    dest = cli.parse_args().output
    result = run()
    if dest:
        dest.mkdir(parents=True,exist_ok=True)
        (dest/"ergebnis.json").write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
        with (dest/"35_beschriftungen.csv").open("w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Geburtsreihenfolge (Originalereignisse)","Beschrifteter Code","F4",
                "Endtypgewicht","p/M positiv","p/M negativ","Exakter Transport",
                "max |delta Randamplitude| (H3-Proben)","max |delta D|"])
            for row in result["rows"]:
                writer.writerow([" ".join(map(str,row["old_event_ids_in_birth_order"])),
                    row["native_inner_bit_code"],row["F4"],row["endpoint_weight"],*row["center_p_over_M"],
                    row["exact_transport"],row["max_abs"]["wavefunction_probe"],row["max_abs"]["gram"]])
    print(json.dumps({k:v for k,v in result.items() if k not in ("rows","scalar_precision")},indent=2))


if __name__ == "__main__":
    main()
