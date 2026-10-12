import copy
from dataclasses import replace
import importlib.util
import json
import math
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
import numpy as np

from plvl.config import Experiment, Arm, Clock, from_dict
from plvl.physics import (I, X, Z, SINGLET, density, rotation, negativity,
                          probabilities, efficiency, fixed_bin_retention, stationary_ou)
from plvl.timing import stamp, fit_affine, residual_summary
from plvl.counting import count_events
from plvl.simulation import run, apply_dead_time
from plvl.bridge import encode_snapshot
from plvl.__main__ import reject_duplicates

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SGNC = REPO/"experiments/photonic-two-qubit/reference/sagnac_v0_7"
sys.path.insert(0,str(SGNC/"host"))
import frame_codec
import analyze


def module(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


reference = module("batch_reference",SGNC/"sim/reference.py").reference
nqk = module("nqk_reference",ROOT/"vendor/nqk/quantum_core.py")


def ideal_arm(**kwargs):
    return replace(Arm(length_km=0,insertion_loss_db=0,coupling=1,
                       detector_efficiency=1,dark_rate_per_port_hz=0,
                       dead_time_s=0,jitter_sigma_s=0),**kwargs)


class ConfigTests(unittest.TestCase):
    def test_roundtrip(self):
        self.assertEqual(from_dict(Experiment().to_dict()),Experiment())

    def test_invalid_parameters_and_unknown_fields(self):
        cases = [{"window_ps":0},{"seed":True},{"duration_ps":1001},
                 {"pair_rate_hz":float("nan")},{"environment_sigma":float("inf")},
                 {"arm_b":{"detector_efficiency":1.01}},
                 {"arm_a":{"clock":{"tick_ps":0}}},{"typo":1},
                 {"arm_a":{"typo":1}},{"calibration_anchors":100},
                 {"provenance":"hardware"},{"arm_a":{"coupling":True}},
                 {"duration_ps":10**13,"pair_rate_hz":1e8}]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                from_dict(case)

    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"seed":1,"seed":2}',object_pairs_hook=reject_duplicates)


class PhysicsTests(unittest.TestCase):
    def test_loss_decibels_and_pair_product(self):
        a = ideal_arm(length_km=10,attenuation_db_per_km=2.5)
        b = replace(a,attenuation_db_per_km=.2)
        self.assertAlmostEqual(float(efficiency(a,0)),10**-2.5)
        self.assertAlmostEqual(float(efficiency(b,0)),10**-.2)
        self.assertAlmostEqual(float(efficiency(b,0))**2,10**-.4)
        with self.assertRaises(ValueError):
            efficiency(replace(a,loss_db_per_environment=30),-1)

    def test_shared_loss_mean_is_not_factorized(self):
        a = ideal_arm(insertion_loss_db=4,loss_db_per_environment=2)
        eta = efficiency(a,np.array([-1.,1.]))
        self.assertGreater(float(np.mean(eta*eta)),float(np.mean(eta)**2))

    def test_werner_negativity_known_solution_and_nqk(self):
        for v in (0,.2,1/3,.5,.98,1):
            r = density(v,I,I)
            self.assertAlmostEqual(negativity(r),max(0,(3*v-1)/4),places=12)
            self.assertAlmostEqual(negativity(r),nqk.negativity(r,[0],2),places=12)
            self.assertTrue(nqk.inspect_density(r)["valid"])

    def test_local_unitaries_preserve_negativity(self):
        for angle in np.linspace(-math.pi,math.pi,17):
            r = density(.9,rotation(angle,.7),rotation(-.4,2*angle))
            self.assertAlmostEqual(negativity(r),.425,places=12)

    def test_common_rotation_preserves_singlet(self):
        u = rotation(1.23,-.91)
        np.testing.assert_allclose(density(1,u,u),density(1,I,I),atol=1e-14)

    def test_mixture_can_erase_entanglement(self):
        r1, r2 = density(1,I,I),density(1,I,Z)
        self.assertAlmostEqual(negativity(r1),.5)
        self.assertAlmostEqual(negativity(r2),.5)
        self.assertAlmostEqual(negativity((r1+r2)/2),0,places=12)

    def test_dephasing_matches_adopted_kraus_reference(self):
        for p in (0,.25,1):
            r = density(.9,rotation(.7,.3),rotation(.2,-.1))
            expected = nqk.channel_all(r,"dephase",p,2)
            actual = density(.9,rotation(.7,.3),rotation(.2,-.1),p,p)
            np.testing.assert_allclose(actual,expected,atol=1e-14)

    def test_born_probabilities_analytic_singlet(self):
        for a,b in ((0,0),(0,22.5),(45,-22.5),(90,0)):
            p = probabilities(density(.98,I,I),a,b)
            e = p[0]-p[1]-p[2]+p[3]
            self.assertAlmostEqual(e,-.98*math.cos(math.radians(2*(a-b))),places=12)
            self.assertAlmostEqual(p[0]+p[1],.5)

    def test_invalid_state_is_not_repaired(self):
        r = np.eye(4)/4
        r[0,0] = -.1
        with self.assertRaises(ValueError):
            negativity(r)
        with self.assertRaises(ValueError):
            density(1,np.diag([math.sqrt(2),0]),I)

    def test_geometric_marginal_false_positive_regression(self):
        # Previous proposal accepts these factorizing joint frequencies.
        counts = np.array([4268,4268,732,732])
        p = counts/counts.sum()
        self.assertAlmostEqual(p[0]*p[3],p[1]*p[2])
        distance = math.acos(math.sqrt(p[0]+p[1]))
        self.assertLess(abs(2*distance-math.pi/4),.05)
        self.assertAlmostEqual(negativity(np.diag(p)),0)
        # Original alleged protected rows return pi/2, not pi/4.
        self.assertAlmostEqual(2*math.acos(math.sqrt(.5)),math.pi/2)

    def test_ou_stationarity_and_lag(self):
        x = stationary_ou(np.random.default_rng(9001),150000,.1,1,2)
        self.assertLess(abs(x.mean()),.08)
        self.assertLess(abs(x.var()-4),.2)
        self.assertLess(abs(np.corrcoef(x[:-1],x[1:])[0,1]-math.exp(-.1)),.01)


class TimingTests(unittest.TestCase):
    def test_affine_clock_holdout(self):
        ref = np.linspace(0,.1,101)
        local = 80e-9+(1+3e-6)*ref
        cal = fit_affine(ref[::2],local[::2])
        result = residual_summary(cal,ref[1::2],local[1::2])
        self.assertLess(result["max_abs_s"],1e-16)
        self.assertAlmostEqual(cal.scale,1+3e-6,places=14)

    def test_nonlinearity_visible_in_holdout(self):
        ref = np.linspace(0,1,101)
        local = ref+1e-6*ref**2
        cal = fit_affine(ref[::2],local[::2])
        self.assertGreater(residual_summary(cal,ref[1::2],local[1::2])["rms_s"],50e-9)

    def test_degenerate_or_extrapolated_calibration_rejected(self):
        with self.assertRaises(ValueError):
            fit_affine([0,0,0],[0,1,2])
        cal = fit_affine([0,1,2],[0,1,2])
        with self.assertRaises(ValueError):
            residual_summary(cal,[3],[3])

    def test_quantizer_bounds(self):
        x = np.linspace(.001,.0011,1000)
        out = stamp(x,Clock(tick_ps=100),np.random.default_rng(1),0)
        self.assertLessEqual(float(np.max(np.abs(out-x))),50e-12+1e-17)

    def test_fixed_bin_retention_limits(self):
        self.assertEqual(fixed_bin_retention(1,0,0),1)
        self.assertEqual(fixed_bin_retention(1,1.2,0),0)
        self.assertEqual(fixed_bin_retention(1,-.25,0),.75)
        expected = 1e-12/math.sqrt(2*math.pi)
        self.assertAlmostEqual(fixed_bin_retention(1e-12,0,1)/expected,1,places=12)

    def test_retention_against_independent_quadrature(self):
        w,s = 5e-9,1e-9
        x = np.linspace(-w,w,200001)
        for mu in (0,.3*w,w,2*w,-.3*w):
            integrand = (1-np.abs(x)/w)*np.exp(-.5*((x-mu)/s)**2)/(s*np.sqrt(2*np.pi))
            numeric = np.trapezoid(integrand,x)
            self.assertAlmostEqual(fixed_bin_retention(w,mu,s),numeric,places=9)

    def test_retention_against_event_monte_carlo(self):
        rng = np.random.default_rng(8021)
        n,w,mu,s = 300000,5e-9,1e-9,1e-9
        t = rng.uniform(0,w,n)
        observed = np.mean(np.floor(t/w)==np.floor((t+rng.normal(mu,s,n))/w))
        expected = fixed_bin_retention(w,mu,s)
        self.assertLess(abs(observed-expected),6*math.sqrt(expected*(1-expected)/n))


class CountingTests(unittest.TestCase):
    def test_boundaries_empty_repeat_multiport_and_reference(self):
        ts = np.array([0,0,0,9,10,19,20,29],dtype=np.uint64)
        ch = np.array([0,0,2,3,1,3,0,2])
        c = count_events(ts,ch,start_ps=0,stop_ps=40,window_ps=10)
        events = [(int(k),int(t),7,False) for t,k in zip(ts,ch)]+[(4,40,7,False)]
        expected, flags = reference(0,40,10,events)
        self.assertEqual(flags,0)
        self.assertEqual(c,expected)
        self.assertEqual(c[0],1)
        self.assertEqual(c[17],1)
        self.assertEqual(c[22],1)
        self.assertEqual(c[23],1)

    def test_large_uint64_epoch_preserves_exact_bins(self):
        start = 2**63+100
        ts = np.array([start,start+9,start+10,start+19],dtype=np.uint64)
        c = count_events(ts,np.array([0,2,1,3]),start_ps=start,stop_ps=start+20,window_ps=10)
        self.assertEqual(c[5],1)
        self.assertEqual(c[10],1)

    def test_bad_order_range_and_fractional_timestamps_rejected(self):
        for ts,ch in (([2,1],[0,1]),([10],[0]),([-1],[0]),([1],[4]),([1.5],[0])):
            with self.subTest(ts=ts,ch=ch), self.assertRaises(ValueError):
                count_events(np.array(ts),np.array(ch),start_ps=0,stop_ps=10,window_ps=1)

    def test_sparse_huge_number_of_empty_bins(self):
        c = count_events(np.array([],dtype=np.int64),np.array([],dtype=int),
                         start_ps=0,stop_ps=2**63,window_ps=1)
        self.assertEqual(c[0],2**63)
        self.assertEqual(c[16],2**63)

    def test_random_differential_reference(self):
        rng = np.random.default_rng(6)
        for n in (0,1,10,1000):
            ts = np.sort(rng.integers(0,10000,n))
            ch = rng.integers(0,4,n)
            c = count_events(ts,ch,start_ps=0,stop_ps=10000,window_ps=100)
            expected, flags = reference(0,10000,100,[(int(k),int(t),7,False) for t,k in zip(ts,ch)]+[(4,10000,7,False)])
            self.assertEqual((c,0),(expected,flags))

    def test_nonparalyzable_dead_time_per_port(self):
        keep = apply_dead_time(np.array([0.,.1,.2,.9,1.,1.1]),np.array([0,0,1,0,0,1]),1.)
        np.testing.assert_equal(keep,[True,False,True,False,True,False])

    def test_dead_time_stationary_rate_law(self):
        rng = np.random.default_rng(371)
        rate, duration, dead = 1e5,1.,1e-5
        times = np.cumsum(rng.exponential(1/rate,200000))
        times = times[times < duration]
        keep = apply_dead_time(times,np.zeros(len(times),int),dead)
        expected = duration*rate/(1+rate*dead)
        self.assertLess(abs(keep.sum()-expected),6*math.sqrt(expected))


class IntegrationTests(unittest.TestCase):
    def test_simulator_deterministic_cell_convergence(self):
        omega,T = 17.,.1
        exact = .5*(1-math.sin(omega*T)/(omega*T))
        errors=[]
        for cells in (10,20,40):
            a = ideal_arm()
            b = replace(a,rotation_y_rate_rad_per_s=omega)
            cfg = Experiment(pair_rate_hz=0,singlet_visibility=1,
                             cell_ps=100_000_000_000//cells,arm_a=a,arm_b=b)
            r,_ = run(cfg)
            approx = np.mean(r["latent_truth"]["ideal_same_port_probability_by_cell"])
            errors.append(abs(approx-exact))
        self.assertGreater(errors[0]/errors[1],3.9)
        self.assertGreater(errors[1]/errors[2],3.9)

    def test_realized_unphysical_environment_is_rejected(self):
        a = ideal_arm(loss_db_per_environment=1)
        with self.assertRaises(ValueError):
            run(Experiment(arm_a=a,seed=2000))

    def test_reproducibility_and_event_accounting(self):
        cfg = Experiment(duration_ps=10_000_000_000,cell_ps=1_000_000_000)
        a,raw = run(cfg)
        b,_ = run(cfg)
        self.assertEqual(a,b)
        self.assertEqual(sum(a["calibrated"]["counters"][18:22]),len(raw["common_time_ps"]))
        for i in range(2):
            self.assertEqual(a["detectors"][i]["recorded"],
                             sum(a["calibrated"]["counters"][18+2*i:20+2*i])+
                             a["calibrated"]["excluded_outside_gate_by_arm"][i])
        self.assertEqual(a["qkd_security"],"NOT_ASSESSED")

    def test_no_photons_no_dark_returns_null_not_success(self):
        arm = ideal_arm()
        report,_ = run(Experiment(pair_rate_hz=0,arm_a=arm,arm_b=arm))
        d = report["calibrated"]["diagnostics"]
        self.assertIsNone(d["conditional_same_port_fraction"])
        self.assertEqual(d["conditional_port_bins"],0)

    def test_loss_against_poisson_thinning_multiple_seeds(self):
        arm = ideal_arm(detector_efficiency=.4)
        total = np.zeros(3)
        for seed in range(12):
            cfg = Experiment(duration_ps=20_000_000_000,cell_ps=5_000_000_000,
                             arm_a=arm,arm_b=arm,seed=seed)
            report,_ = run(cfg)
            total += [d["signal_candidates_before_dead_time"] for d in report["detectors"]]+[
                report["latent_truth"]["realized_pair_survivals_before_dead_time_and_timing"]]
        expectation = 12*4000*np.array([.4,.4,.16])
        self.assertTrue(np.all(np.abs(total-expectation) < 6*np.sqrt(expectation)))

    def test_clock_calibration_restores_coincidences(self):
        a = ideal_arm(jitter_sigma_s=100e-12)
        b = replace(a,clock=Clock(offset_s=80e-9,skew_ppm=3))
        report,_ = run(Experiment(arm_a=a,arm_b=b,singlet_visibility=1))
        raw = report["uncalibrated"]["diagnostics"]["conditional_port_bins"]
        corrected = report["calibrated"]["diagnostics"]["conditional_port_bins"]
        self.assertGreater(corrected,100*max(1,raw))
        self.assertTrue(report["timing_screen"]["within_assumed_budget"])

    def test_joint_drift_changes_weighted_state_without_security_claim(self):
        a = ideal_arm(insertion_loss_db=5,loss_db_per_environment=1)
        b = replace(a,rotation_y_rad_per_environment=1.5)
        report,_ = run(Experiment(arm_a=a,arm_b=b,environment_tau_s=.01))
        truth = report["latent_truth"]
        self.assertGreater(truth["expected_pair_survivals_before_dead_time_and_timing"],truth["factorized_mean_loss_pair_prediction"])
        self.assertGreater(truth["mean_instantaneous_negativity"],truth["negativity_time_averaged_state"])
        self.assertNotAlmostEqual(truth["negativity_survival_weighted_state"],truth["negativity_time_averaged_state"],places=5)

    def test_snapshot_roundtrip_crc_and_integrity(self):
        report,_ = run(Experiment(duration_ps=10_000_000_000,cell_ps=1_000_000_000))
        frame = encode_snapshot(report,sequence=9)
        self.assertEqual(len(frame),244)
        rec = frame_codec.decode_frame(frame,origin="synthetic",expected_sequence=9)
        self.assertEqual(analyze.validate(rec)[3],report["calibrated"]["counters"])
        damaged = bytearray(frame); damaged[100]^=1
        with self.assertRaises(frame_codec.FrameError):
            frame_codec.decode_frame(damaged,origin="synthetic")
        with self.assertRaises(frame_codec.FrameError):
            frame_codec.decode_frame(frame,origin="synthetic",expected_sequence=10)
        rec["flags"]=4
        with self.assertRaises(analyze.InvalidRecord):
            analyze.validate(rec)


class CLITests(unittest.TestCase):
    def test_cli_exports_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg = root/"config.json"
            cfg.write_text(json.dumps(Experiment(pair_rate_hz=1000).to_dict()))
            out,raw,frame = root/"report.json",root/"events.npz",root/"snapshot.bin"
            cmd = [sys.executable,"-m","plvl",str(cfg),"--output",str(out),
                   "--raw-output",str(raw),"--snapshot-output",str(frame)]
            r = subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            report = json.loads(out.read_text())
            self.assertEqual(report["origin"],"synthetic")
            with np.load(raw,allow_pickle=False) as arrays:
                self.assertIn("common_time_ps",arrays)
            self.assertEqual(frame.stat().st_size,244)
            before = out.read_bytes()
            r = subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
            self.assertEqual(out.read_bytes(),before)

    def test_cli_duplicate_or_unwritable_outputs_leave_no_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg,out = root/"config.json",root/"report.json"
            cfg.write_text(json.dumps(Experiment(pair_rate_hz=0).to_dict()))
            for raw in (out,root/"missing"/"raw.npz"):
                r = subprocess.run([sys.executable,"-m","plvl",str(cfg),"--output",str(out),
                                    "--raw-output",str(raw)],cwd=ROOT,capture_output=True,text=True)
                self.assertEqual(r.returncode,2,r.stderr)
                self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
