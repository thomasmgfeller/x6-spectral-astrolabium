"""Frozen synthetic scenarios; ensemble uncertainty is not apparatus uncertainty."""
import argparse
from dataclasses import replace
import json
import math
from pathlib import Path
import numpy as np
from plvl.config import Experiment, Arm, Clock
from plvl.simulation import run
from plvl.__main__ import provenance


def scenarios():
    baseline = Experiment()
    clock = replace(baseline,arm_b=replace(baseline.arm_b,
                    clock=Clock(offset_s=80e-9,skew_ppm=3,drift_ppm_per_s=.02)))
    coupled = replace(clock,environment_tau_s=.02,
                      arm_a=replace(clock.arm_a,insertion_loss_db=4,
                                    loss_db_per_environment=.6,
                                    rotation_y_rad_per_environment=.1,
                                    delay_s_per_environment=50e-12),
                      arm_b=replace(clock.arm_b,insertion_loss_db=4,
                                    loss_db_per_environment=.6,
                                    rotation_y_rad_per_environment=.8,
                                    rotation_y_rate_rad_per_s=2,
                                    delay_s_per_environment=200e-12))
    nonlinear = replace(clock,arm_b=replace(clock.arm_b,
                        clock=Clock(offset_s=80e-9,skew_ppm=3,drift_ppm_per_s=20)))
    return {"baseline":baseline,"clock_error":clock,
            "coupled":coupled,"nonlinear_clock_stress":nonlinear}


def statistics(values):
    x = np.asarray(values,float)
    if len(x)<2 or not np.isfinite(x).all():
        raise ValueError("At least two finite independent-run statistics required")
    sd = float(x.std(ddof=1))
    return {"n":len(x),"mean":float(x.mean()),"sample_sd":sd,
            "standard_error_of_mean":sd/math.sqrt(len(x))}


def convergence():
    # Composite midpoint rule against exact integral for deterministic Ry drift.
    # Source singlet, A fixed, B angle omega*t; same-port probability=(1-cos)/2.
    omega,T = 17.,.1
    exact = .5*(1-math.sin(omega*T)/(omega*T))
    rows=[]
    for n in (10,20,40,80):
        mid=(np.arange(n)+.5)*T/n
        approx=float(np.mean((1-np.cos(omega*mid))/2))
        rows.append({"cells":n,"same_port_probability":approx,"abs_error":abs(approx-exact)})
    return {"scope":"deterministic midpoint discretization only; OU convergence remains open",
            "exact":exact,"rows":rows}


def build():
    output={"schema":"plvl.experiments.v1","origin":"synthetic",
            "claim":"model illustration, not fitted hardware predictions",
            "reproducibility":provenance(),"seed_sequence":list(range(2000,2030)),
            "ensemble_uncertainty":"independent synthetic runs at fixed assumed parameters; no hardware confidence statement",
            "scenarios":{},"deterministic_convergence":convergence()}
    for name,cfg in scenarios().items():
        report,_ = run(cfg)
        repeats=[]
        for seed in output["seed_sequence"]:
            r,_=run(replace(cfg,seed=seed))
            c=r["calibrated"]["diagnostics"]
            u=r["uncalibrated"]["diagnostics"]
            repeats.append({"seed":seed,"calibrated_port_bins":c["conditional_port_bins"],
                            "uncalibrated_port_bins":u["conditional_port_bins"],
                            "same_port_fraction":c["conditional_same_port_fraction"],
                            "timing_screen_pass":r["timing_screen"]["within_assumed_budget"]})
        output["scenarios"][name]={"single_seed_report":report,"replicates":repeats,
            "summary":{"calibrated_port_bins":statistics([r["calibrated_port_bins"] for r in repeats]),
                       "same_port_fraction":statistics([r["same_port_fraction"] for r in repeats]),
                       "paired_calibration_count_change":statistics([r["calibrated_port_bins"]-r["uncalibrated_port_bins"] for r in repeats]),
                       "timing_screen_passes":sum(r["timing_screen_pass"] for r in repeats)}}
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=build()
    with a.output.open("x") as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write("\n")
    print(json.dumps({name:obj["summary"] for name,obj in result["scenarios"].items()},indent=2))


if __name__=="__main__":
    main()
