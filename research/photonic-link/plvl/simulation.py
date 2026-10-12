"""One source-event stream drives joint loss, polarization and timing outcomes."""
from dataclasses import asdict
import numpy as np
from .physics import (stationary_ou, rotation, density, probabilities, efficiency,
                      delay, negativity, SINGLET)
from .timing import stamp, fit_affine, residual_summary
from .counting import count_events, diagnostics


def apply_dead_time(times, ports, dead_time_s):
    """Nonparalyzable, independent detector per output port, physical time."""
    times, ports = np.asarray(times, float), np.asarray(ports)
    if (times.ndim != 1 or ports.shape != times.shape or
        not np.isfinite(times).all() or np.any(np.diff(times) < 0) or
        ports.dtype.kind not in "ui" or np.any((ports < 0)|(ports > 1)) or
        not np.isfinite(dead_time_s) or dead_time_s < 0):
        raise ValueError("Invalid detector stream")
    keep = np.zeros(len(times), bool)
    ready = [-np.inf, -np.inf]
    for j, (t, port) in enumerate(zip(times, ports)):
        if t >= ready[int(port)]:
            keep[j] = True
            ready[int(port)] = t+dead_time_s
    return keep


def acquisition(times_by_arm, ports_by_arm, cfg):
    accepted_t, accepted_ch, excluded = [], [], []
    for side, (ts, ports) in enumerate(zip(times_by_arm, ports_by_arm)):
        # Rounded common-epoch ps, not a change of hardware TDC resolution.
        ps = np.rint(np.asarray(ts)*1e12).astype(np.int64)
        keep = (ps >= 0)&(ps < cfg.duration_ps)
        excluded.append(int((~keep).sum()))
        accepted_t.append(ps[keep])
        accepted_ch.append(2*side+ports[keep])
    ts, ch = np.concatenate(accepted_t), np.concatenate(accepted_ch)
    order = np.argsort(ts, kind="stable")
    counters = count_events(ts[order], ch[order], start_ps=0,
                            stop_ps=cfg.duration_ps, window_ps=cfg.window_ps)
    return {"counters": counters, "excluded_outside_gate_by_arm": excluded,
            "diagnostics": diagnostics(counters)}, (ts[order], ch[order])


def run(cfg):
    cfg.validate()
    # Separate reproducible streams prevent calibration from consuming event RNG.
    streams = [np.random.Generator(np.random.PCG64(s))
               for s in np.random.SeedSequence(cfg.seed).spawn(8)]
    env_rng, source_rng, outcome_rng, loss_a_rng, loss_b_rng, det_a_rng, det_b_rng, cal_rng = streams
    cells = cfg.duration_ps//cfg.cell_ps
    dt = cfg.cell_ps*1e-12
    midpoint = (np.arange(cells)+.5)*dt
    env = stationary_ou(env_rng, cells, dt, cfg.environment_tau_s, cfg.environment_sigma)
    arms = (cfg.arm_a, cfg.arm_b)
    etas = [np.broadcast_to(efficiency(a, env), (cells,)) for a in arms]
    delays = [np.broadcast_to(delay(a, env), (cells,)) for a in arms]
    for d in delays:
        if np.max(np.abs(np.diff(d)), initial=0) > dt/100:
            raise ValueError("Delay steps exceed 1% of model cell; refine the physical model")
    rhos, probs = [], []
    for k, t in enumerate(midpoint):
        us = [rotation(a.rotation_y_rad+a.rotation_y_rate_rad_per_s*t+
                       a.rotation_y_rad_per_environment*env[k],
                       a.rotation_z_rad+a.rotation_z_rad_per_environment*env[k]) for a in arms]
        rho = density(cfg.singlet_visibility, *us,
                      cfg.arm_a.dephasing_probability, cfg.arm_b.dephasing_probability)
        rhos.append(rho)
        probs.append(probabilities(rho, cfg.arm_a.analyzer_angle_deg, cfg.arm_b.analyzer_angle_deg))
    probs = np.asarray(probs)
    n = int(source_rng.poisson(cfg.pair_rate_hz*cfg.duration_s))
    t = np.sort(source_rng.uniform(0, cfg.duration_s, n))
    idx = np.minimum((t/dt).astype(int), cells-1)
    u = outcome_rng.random(n)
    # Sampling includes both outcomes before loss; lost outcomes never enter analysis.
    outcome = np.sum(u[:,None] >= np.cumsum(probs[idx], axis=1)[:,:3], axis=1)
    source_ports = (outcome//2, outcome%2)
    local_times, port_streams, corrected, detector_stats, calibrations = [], [], [], [], []
    survival_masks = []
    for side, (arm, loss_rng, det_rng) in enumerate(zip(arms, (loss_a_rng,loss_b_rng), (det_a_rng,det_b_rng))):
        detected = loss_rng.random(n) < etas[side][idx]
        survival_masks.append(detected)
        photon_times = t[detected]+delays[side][idx[detected]]
        photon_ports = source_ports[side][detected]
        dark_times, dark_ports = [], []
        for port in (0,1):
            nd = int(det_rng.poisson(arm.dark_rate_per_port_hz*cfg.duration_s))
            # Dark arrivals are stationary detector events, not propagated photons.
            dark_times.append(det_rng.uniform(0,cfg.duration_s,nd)+float(delay(arm,0)))
            dark_ports.append(np.full(nd,port,dtype=int))
        physical = np.concatenate([photon_times, *dark_times])
        ports = np.concatenate([photon_ports, *dark_ports])
        order = np.argsort(physical, kind="stable")
        physical, ports = physical[order], ports[order]
        keep = apply_dead_time(physical, ports, arm.dead_time_s)
        local = stamp(physical[keep],arm.clock,det_rng,arm.jitter_sigma_s)
        ports = ports[keep]
        # Independent, accurately labelled calibration pulses on the same modeled
        # path. This assumption must be experimentally established; no inferred
        # access to a hidden photon-pair identity and no WR implementation.
        ref = np.linspace(0,cfg.duration_s,cfg.calibration_anchors)
        ci = np.minimum((ref/dt).astype(int),cells-1)
        anchor_local = stamp(ref+delays[side][ci],arm.clock,cal_rng,cfg.calibration_jitter_sigma_s)
        train = np.arange(len(ref))%2==0
        cal = fit_affine(ref[train],anchor_local[train])
        holdout = residual_summary(cal,ref[~train],anchor_local[~train])
        calibrations.append({"fit":asdict(cal), "training_n":int(train.sum()),
                             "holdout":holdout, "source":"independent_synthetic_reference_pulses"})
        corr = cal.correct(local)
        local_times.append(local)
        port_streams.append(ports)
        corrected.append(corr)
        detector_stats.append({"signal_candidates_before_dead_time":int(detected.sum()),
                               "dark_candidates_before_dead_time":sum(map(len,dark_times)),
                               "dead_time_rejected":int((~keep).sum()),
                               "recorded":len(local)})
    uncalibrated, _ = acquisition(local_times, port_streams, cfg)
    calibrated, common_events = acquisition(corrected, port_streams, cfg)
    weighted = etas[0]*etas[1]
    avg_rho = np.mean(rhos,axis=0)
    detected_rho = np.average(rhos,axis=0,weights=weighted) if weighted.sum() else None
    truth = {
        "label":"SIMULATOR_LATENT_TRUTH_NOT_AN_ESTIMATE_FROM_CLICKS",
        "generated_pairs":n, "environment":env.tolist(),
        "realized_pair_survivals_before_dead_time_and_timing":int(np.sum(survival_masks[0]&survival_masks[1])),
        "efficiency_a":etas[0].tolist(),"efficiency_b":etas[1].tolist(),
        "delay_a_s":delays[0].tolist(),"delay_b_s":delays[1].tolist(),
        "mean_instantaneous_negativity":float(np.mean([negativity(r) for r in rhos])),
        "negativity_time_averaged_state":negativity(avg_rho),
        "negativity_survival_weighted_state":negativity(detected_rho) if detected_rho is not None else None,
        "singlet_overlap_time_averaged":float(np.real(SINGLET.conj()@avg_rho@SINGLET)),
        "ideal_same_port_probability_by_cell":(probs[:,0]+probs[:,3]).tolist(),
        "expected_signal_candidates_by_arm": [float(cfg.pair_rate_hz*cfg.duration_s*e.mean()) for e in etas],
        "expected_pair_survivals_before_dead_time_and_timing":float(cfg.pair_rate_hz*cfg.duration_s*weighted.mean()),
        "factorized_mean_loss_pair_prediction":float(cfg.pair_rate_hz*cfg.duration_s*etas[0].mean()*etas[1].mean()),
    }
    maximum = max(c["holdout"]["max_abs_s"] for c in calibrations)
    report = {"schema":"plvl.report.v1", "origin":"synthetic", "config":cfg.to_dict(),
              "physical_validation":"NOT_ASSESSED", "qkd_security":"NOT_ASSESSED",
              "novel_physics":"NOT_ASSESSED", "topological_protection":"NOT_CLAIMED",
              "calibration":calibrations,"detectors":detector_stats,
              "timing_screen":{"criterion":"max absolute held-out residual per arm <= W/4",
                               "budget_s":cfg.window_ps*1e-12/4,
                               "within_assumed_budget":maximum<=cfg.window_ps*1e-12/4,
                               "meaning":"engineering screen on synthetic anchors; not a guarantee"},
              "uncalibrated":uncalibrated,"calibrated":calibrated,"latent_truth":truth}
    raw = {"local_time_a_s":local_times[0],"port_a":port_streams[0],
           "local_time_b_s":local_times[1],"port_b":port_streams[1],
           "common_time_ps":common_events[0],"common_channel":common_events[1]}
    return report, raw
