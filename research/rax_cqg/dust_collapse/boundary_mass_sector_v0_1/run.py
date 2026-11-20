"""Reconstruct the finite mass-window and calibration audit from pinned sources."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha1,sha256
import argparse
import json

ROOT=Path(__file__).resolve().parent

def main():
    if not __debug__:raise SystemExit("Run Python without -O to retain the exact checks.")
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--types",type=Path)
    args=parser.parse_args()
    sources=json.loads((ROOT/"sources.json").read_text())
    design=json.loads((ROOT/"design.json").read_text())
    assert design["base"]==sources["commit"]
    for e in sources["files"]:
        data=(ROOT/"inputs"/e["path"]).read_bytes()
        assert sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==e["blob"],e["path"]
    old=json.loads((ROOT/"inputs/material_current_surface_v0_1/results.json").read_text())
    assert old["finite_currents"]["orders"]==1048 and old["physical_CST"]["execution"]=="NOT_RUN"
    packet=json.loads((ROOT/"inputs/initial_preparation_v0_1/packet_contract.json").read_text())
    assert packet["clock_offsets_from_affine_T3"]==[-1/16,1/16] and packet["clock_lobe_half_width"]==1/32
    plan=json.loads((ROOT/"inputs/correspondence_v0_1/plan.json").read_text())
    assert design["targets"]==[plan["reference"]["masses"][i] for i in (0,-1)]
    assert F(design["diagnostic_band_relative_half_width"])==F(1,100)
    import charge,ordered,selector,boundary_packet
    summary,raw=charge.run()
    ordered_summary,ord_types=ordered.run()
    for t,v in ord_types.items():
        entry=raw[str(t)]
        assert F(v["ordered_sup_bounds"][0])<=F(entry["momentum_sup_bounds"][1])
        assert all(not yes or entry["trial_windows_nonempty_positive_measure"][m] for m,yes in v["trial_windows"].items())
        entry.update(v)
    assert ordered_summary["ideal_vertices_all_orders"]==old["finite_currents"]["ideal_cuts_per_mass"]
    selector.test_selector()
    records={"commit":sources["commit"],"design_sha256":sha256((ROOT/"design.json").read_bytes()).hexdigest(),
             "raw_charge":summary,"supplement_ordered_clocks":ordered_summary,
             "tagged_calibration":selector.tag_calibration(),"conditional_amplitude":selector.witness(),
             "ordinary_boundary_momentum_test":boundary_packet.run(),
             "supplement_scale_matching":boundary_packet.scale_audit(summary),
             "physical":{"calibrated_CST_mass_per_unit_charge":None,"accepted_CST_mass_sector":{"1/4":None,"4":None},
                         "CST_surface_areas":None,"mass_contrast_uniform_in_weights":None,
                         "P3_eligibility":"HOLD_NOT_ELIGIBLE","P3_dynamics":"NOT_RUN","new_physical_4D_histories":0}}
    args.out.write_text(json.dumps(records,indent=2,ensure_ascii=False)+"\n")
    if args.types:args.types.write_text(json.dumps(raw,indent=2)+"\n")

if __name__=="__main__":main()
