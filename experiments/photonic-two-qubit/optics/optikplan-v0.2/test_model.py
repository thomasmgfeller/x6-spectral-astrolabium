import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from model import FWHM, HERE, coupling, evaluate, indices, spectral, timing, window_probability
from timing_calibration import analyse, read_hits
from spectral_calibration import compare as compare_spectra

P=json.loads((HERE/"design_inputs.json").read_text())


class DesignChecks(unittest.TestCase):
    def test_material_and_reference_range(self):
        for axis in ("y","z"):
            lam=.810
            n,ng=indices(lam,axis)
            derivative=(indices(lam+1e-6,axis)[0]-indices(lam-1e-6,axis)[0])/2e-6
            self.assertAlmostEqual(ng,n-lam*derivative,8)
        with self.assertRaises(ValueError):
            indices(.405,"y")

    def test_interference_controls(self):
        self.assertAlmostEqual(spectral(P)["gamma_abs"],1,12)
        self.assertAlmostEqual(spectral(P,mismatch_m=(300,300))["gamma_abs"],1,12)
        fine=spectral(P,.5,.2,(0,300),1,grid=481,extent=8)
        coarse=spectral(P,.5,.2,(0,300),1)
        for key in ("gamma_abs","integrated_weight_THz2","signed_DA_contrast_before_background"):
            self.assertAlmostEqual(coarse[key],fine[key],9)
        self.assertLess(spectral(P,2)["gamma_abs"],.4)
        self.assertAlmostEqual(spectral(dict(P,phase_error_rad=math.pi))["signed_DA_contrast_before_background"],
                               -spectral(dict(P,phase_error_rad=0))["signed_DA_contrast_before_background"])
        self.assertAlmostEqual(spectral(dict(P,ccw_over_cw_power_ratio=0))["signed_DA_contrast_before_background"],0)

    def test_overlap_of_two_gaussian_fields(self):
        w,lam=2.5,.810
        zr=math.pi*w*w/lam
        self.assertAlmostEqual(coupling(lam,w,w),1)
        self.assertAlmostEqual(coupling(lam,w,2*w),.64)
        self.assertAlmostEqual(coupling(lam,w,w,z=2*zr),.5)
        self.assertAlmostEqual(coupling(lam,w,w,dx=w),math.exp(-1))
        self.assertAlmostEqual(coupling(lam,w,w,tx=lam/(math.pi*w)),math.exp(-1))
        # Direct field integral for simultaneous tilt, focus error and decenter.
        x=np.linspace(-15,15,401)
        X,Y=np.meshgrid(x,x)
        z,dx,dy,tx,ty=9.,.7,-.2,.015,-.004
        w1=w*math.hypot(1,z/zr); k=2*math.pi/lam
        a=1/w1**2+1j*k*z/(2*(z*z+zr*zr))
        beam=np.exp(-a*((X-dx)**2+(Y-dy)**2)+1j*k*(tx*X+ty*Y))
        fiber=np.exp(-(X*X+Y*Y)/w**2)
        numer=abs(np.sum(beam*fiber))**2
        eta=numer/(np.sum(abs(beam)**2)*np.sum(fiber**2))
        self.assertAlmostEqual(eta,coupling(lam,w,w,dx,dy,z,tx,ty),10)

    def test_four_channels_with_synthetic_timestamps(self):
        rng=np.random.default_rng(431204)
        n=40000; q=P["tdc_step_ps"]; expected=timing(P)
        # Common clock phase; detector and front-end contributions independently injected.
        base=5000*np.arange(n)+rng.uniform(0,q,n)
        tags=[]
        for ch in range(4):
            dt=rng.normal(0,P["detector_sigma_ps_scenario"][ch],n)
            dt+=rng.normal(0,P["electronics_sigma_ps_scenario"][ch],n)
            tags.append((q*np.rint((base+dt+P["offset_residual_ps_scenario"][ch])/q)).astype(int))
        assert len(expected)==4
        for row in expected:
            a,b=row["ports"]
            d=tags[b]-tags[a]
            self.assertLess(abs(d.mean()-row["pair_offset_ps"]),5)
            self.assertLess(abs(d.std()*FWHM-row["core_fwhm_ps"]),10)
            self.assertLess(abs(np.mean(abs(d)<=1000)-row["core_window"]),.003)
            self.assertLess(row["delayed_5pct_window"],.96)
        self.assertAlmostEqual(sum(r["accidentals_per_s"] for r in expected),.8)
        self.assertLess(window_probability(250,1600,2000),.02)

    def test_calibration_replay_and_large_ticks(self):
        groups={i:{ch:2**60+i*5000+[0,50,-20,30][ch] for ch in range(4)} for i in range(40)}
        groups[39].pop(3)
        rows=analyse(groups,[0,50,-20,30],2000,50)["pairs"]
        for row in rows:
            self.assertEqual(row["pair_mean_ps"],0)
            self.assertEqual(row["fraction_in_fixed_window"],1)
            self.assertEqual(row["paired_pulses"],39 if row["ports"][1]==3 else 40)
        with TemporaryDirectory() as tmp:
            file=Path(tmp)/"hits.csv"
            file.write_text("pulse_id,channel,raw_ps\n0,0,20\n0,1,22\n")
            self.assertEqual(read_hits(file)[0],{0:20,1:22})
            with file.open("a") as stream:
                stream.write("0,1,36\n")
            with self.assertRaises(ValueError):
                read_hits(file)
        with self.assertRaises(ValueError):
            analyse({1:{0:3}},[0]*4,2000,50)

    def test_spectral_phase_and_incomplete_grid(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/"grid.csv"
            head="u_THz,v_THz,cw_density,ccw_density"
            cells=["0,0,1,4","0,1,1,4","1,0,1,4","1,1,1,4"]
            path.write_text(head+"\n"+"\n".join(cells)+"\n")
            self.assertIsNone(compare_spectra(path)["gamma_abs"])
            self.assertAlmostEqual(compare_spectra(path)["spectral_overlap_abs_upper"],1)
            def with_phase(phases):
                path.write_text(head+",relative_phase_rad\n"+"\n".join(
                    s+","+str(p) for s,p in zip(cells,phases))+"\n")
            with_phase([0]*4)
            self.assertAlmostEqual(compare_spectra(path)["signed_DA_coherent_term"],.8)
            with_phase([0,0,math.pi,math.pi])
            self.assertLess(compare_spectra(path)["gamma_abs"],1e-12)
            with_phase([0,0,0])
            with self.assertRaises(ValueError):
                compare_spectra(path)

    def test_published_numbers_and_real_status(self):
        reference=json.loads((HERE/"design_result.json").read_text())
        actual=evaluate(P)
        def compare(a,b):
            if isinstance(a,dict):
                self.assertEqual(a.keys(),b.keys())
                for k in a: compare(a[k],b[k])
            elif isinstance(a,list):
                self.assertEqual(len(a),len(b))
                for x,y in zip(a,b):compare(x,y)
            elif isinstance(a,float):
                self.assertTrue(math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10),(a,b))
            else:
                self.assertEqual(a,b)
        compare(actual,reference)
        self.assertEqual(actual["hardware_gates"]["CHSH"],"NOT_RUN")
        self.assertLess(actual["nominal_residual_delay_ps_at_90pct"],.5)
        self.assertGreater(actual["coincidence_budget"]["matched"]["raw_DA_symmetric_background_scenario"],.9)
        self.assertLess(actual["coincidence_budget"]["stress_combined"]["raw_DA_symmetric_background_scenario"],.9)


if __name__=="__main__":
    unittest.main()
