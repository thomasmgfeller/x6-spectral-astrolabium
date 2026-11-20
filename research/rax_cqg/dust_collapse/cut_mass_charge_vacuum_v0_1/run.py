"""Recompute the vacuum and positive-mass pairing audit offline."""
import argparse
from collections import Counter
from hashlib import sha1,sha256
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent

def write(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")

def main():
    if not __debug__:raise SystemExit("Run without -O to enable audit checks.")
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--types",type=Path)
    args=parser.parse_args()
    sources=json.loads((ROOT/"sources.json").read_text())
    for e in sources["files"]:
        b=(ROOT/"upstream"/e["file"]).read_bytes()
        assert sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==e["git_blob"],e["file"]
    def source(p):return json.loads((ROOT/"upstream"/p).read_text())
    con=source("initial_preparation_v0_1/packet_contract.json")
    assert con["density_centers"]==[1/8,1/4] and con["clock_lobe_half_width"]==con["density_half_width"]==1/32
    assert con["clock_offsets_from_affine_T3"]==[-1/16,1/16]
    records=source("correspondence_v0_1/results/checkpoint_P3_records.json")
    runs=Counter(v["execution"] for v in records)
    start=[r["checkpoint_context"] for r in records if r["checkpoint_context"]["x"]=="0"]
    assert len(start)==12 and len(records)==60 and runs=={"NOT_RUN":60}
    assert source("correspondence_v0_1/results/eligibility.json")["decision"]=="HOLD_NOT_ELIGIBLE"
    assert source("correspondence_v0_1/plan.json")["primary_tolerances"]["mass_or_flux_over_M"]==.02
    assert source("boundary_mass_sector_v0_1/results.json")["physical"]["calibrated_CST_mass_per_unit_charge"] is None
    import calibrate,packet,original_packet
    typ,info=calibrate.main_audit()
    paired=packet.run(info["selected_order"],info["selected_route"])
    result={"repo_commit":sources["commit"],"design_sha256":sha256((ROOT/"design.json").read_bytes()).hexdigest(),
            "supplement_sha256":sha256((ROOT/"supplement.json").read_bytes()).hexdigest(),
            "upstream_P3":{"checkpoints":len(records),"initial_time_records":len(start),"executions":dict(runs)},
            "initial_density_insertion":original_packet.run(),"tagged_finite_calibration":info,
            "paired_readings":paired,"physical":{"independent_positive_cut_mass_same_CST_preparation":None,
            "measured_physical_charge_for_that_mass":None,"physical_vacuum_readout_same_protocol":None,
            "physical_gain":None,"physical_area":None,"P3":"HOLD_NOT_ELIGIBLE","dynamics":"NOT_RUN"}}
    write(args.out,result)
    if args.types:write(args.types,typ)
if __name__=="__main__":main()
