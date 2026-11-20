"""Offline two-mass material-surface audit, standard library only."""
from hashlib import sha1,sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent

def main():
    if not __debug__:
        raise SystemExit("Verification requires Python assertions, run without -O.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    sources = json.loads((HERE/"sources.json").read_text())
    design = json.loads((HERE/"design.json").read_text())
    assert design["base"]==sources["commit"]
    for src in sources["inputs"]:
        b=(HERE/"inputs"/src["path"]).read_bytes()
        assert sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==src["git_blob"],src["path"]
    contract=json.loads((HERE/"inputs/initial_preparation_v0_1/packet_contract.json").read_text())
    assert contract["clock_lobe_half_width"]==1/32 and contract["clock_offsets_from_affine_T3"]==[-1/16,1/16]
    plan=json.loads((HERE/"inputs/correspondence_v0_1/plan.json").read_text())["reference"]
    assert plan["G"]==plan["c"]==1 and plan["R0"]==10 and plan["T_end"]=="5*sqrt(5)/3"
    assert design["targets"]==[plan["masses"][0],plan["masses"][-1]] and "1/2" in plan["time_fractions"]
    from finite_current import run as finite
    from reference_surface import run as continuum
    result = {"git_base":sources["commit"],"design_sha256":sha256((HERE/"design.json").read_bytes()).hexdigest(),
              "finite_currents":finite(),**continuum(),
              "physical_CST":{"candidate":"CST-DUST-C1","status":"HOLD_NOT_ELIGIBLE","execution":"NOT_RUN",
                              "physical_mass_prepared":{"1/4":None,"4":None},"material_surface_at_Tstar":None,
                              "area_at_Tstar":{"1/4":None,"4":None},"radius_contrast_for_all_global_weights":None,
                              "new_dynamical_4D_histories":0}}
    old = json.loads((HERE/"inputs/early_areal_radius_two_masses_v0_1/results.json").read_text())
    for mass,measure in result["reference"]["masses"].items():
        assert abs(measure["radius"]["approx"]-old["p3_reference_check"]["reference"][mass]["radius_approx"])<1e-13
    data=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.out: args.out.write_text(data)
    else: print(data,end="")

if __name__=="__main__":
    main()
