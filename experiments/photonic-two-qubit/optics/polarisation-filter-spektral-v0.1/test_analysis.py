import cmath
import copy
import math
import unittest
from analysis import waveplate,pbs_port,filter_budget,accidental_rate,spectral_overlap,design_results,tail_overlap_bounds

class PhysicalChecks(unittest.TestCase):
    def grid(self):
        return {'reference_plane':'AFTER_INSTALLED_FILTERS',
                'density_units':'relative_rate_per_THz2','nu_A_THz':[369.,370.],
                'nu_B_THz':[369.,370.],'cw_density':[[1.,1.],[1.,1.]],
                'ccw_density':[[1.,1.],[1.,1.]],'relative_phase_rad':None}
    def test_reciprocal_pbs_ports(self):
        for pol in ['H','V']:
            for port in 'WENS': self.assertEqual(pbs_port(pbs_port(port,pol),pol),port)
        self.assertEqual(pbs_port('E','H'),'W')
        self.assertEqual(pbs_port('E','V'),'S')
        self.assertEqual(pbs_port('N','V'),'W')
        self.assertEqual(pbs_port('N','H'),'S')
    def test_half_half_and_reverse_basis(self):
        for angle in (-45,45):
            self.assertAlmostEqual(abs(waveplate(angle,math.pi,(1,0))[1])**2,1)
            self.assertAlmostEqual(abs(waveplate(angle,math.pi,(0,1))[0])**2,1)
    def test_full_wave_pump_is_wrong_configuration(self):
        self.assertAlmostEqual(abs(waveplate(45,2*math.pi,(0,1))[0])**2,0)
    def test_unitary_nonideal_retarder(self):
        e=(1/math.sqrt(2),1j/math.sqrt(2))
        o=waveplate(17.3,math.pi+.08,e)
        self.assertAlmostEqual(sum(abs(z)**2 for z in o),1)
    def test_leakage_independent_formula(self):
        out=waveplate(45.25,math.pi+2*math.pi/100,(1,0))
        self.assertAlmostEqual(abs(out[0])**2,design_results()['waveplate_wrong_fraction'])
    def test_od_units_and_scaling(self):
        b=filter_budget(.003,405,1,100,14)
        self.assertTrue(13.7<b['required_od']<13.9)
        self.assertTrue(60<b['pump_background_upper_s']<62)
        self.assertAlmostEqual(filter_budget(.003,405,1,100,15)['pump_background_upper_s'],b['pump_background_upper_s']/10)
        self.assertEqual(filter_budget(0,405,1,100,0)['required_od'],0)
        with self.assertRaises(ValueError):filter_budget(.1,405,1.1,100,4)
    def test_full_width_and_four_pairs(self):
        self.assertAlmostEqual(accidental_rate([100000]*4,2e-9),80)
        self.assertAlmostEqual(accidental_rate([3000]*4,2e-9),.072)
    def test_phase_missing_cannot_report_gamma(self):
        r=spectral_overlap(self.grid());self.assertEqual(r['intensity_overlap_upper_bound'],1)
        self.assertIsNone(r['gamma_abs']);self.assertEqual(r['hardware_status'],'NOT_RUN')
    def test_identical_intensity_opposite_phase(self):
        x=self.grid();x['relative_phase_rad']=[[0,math.pi],[0,math.pi]]
        r=spectral_overlap(x)
        self.assertAlmostEqual(r['intensity_overlap_upper_bound'],1)
        self.assertLess(r['gamma_abs'],1e-15)
    def test_equal_marginals_disjoint_joint_support(self):
        x=self.grid();x['cw_density']=[[2,0],[0,2]];x['ccw_density']=[[0,2],[2,0]]
        r=spectral_overlap(x);self.assertEqual(r['intensity_overlap_upper_bound'],0)
        self.assertEqual([sum(row) for row in x['cw_density']],[sum(row) for row in x['ccw_density']])
    def test_shared_filter_reduces_rate_not_overlap(self):
        x=self.grid();x['relative_phase_rad']=[[0,0],[0,0]]
        a=spectral_overlap(x)
        x['cw_density']=x['ccw_density']=[[.1,.3],[.2,.4]]
        b=spectral_overlap(x);self.assertAlmostEqual(b['gamma_abs'],1)
        self.assertLess(b['integrated_cw'],a['integrated_cw'])
    def test_nonuniform_grid_and_imbalance(self):
        x=self.grid();x['nu_A_THz']=[1,2,4];x['cw_density']=[[1,1]]*3;x['ccw_density']=[[4,4]]*3
        r=spectral_overlap(x);self.assertAlmostEqual(r['integrated_cw'],3)
        self.assertAlmostEqual(r['integrated_ccw'],12);self.assertAlmostEqual(r['balance_factor'],.8)
    def test_phase_conjugation(self):
        x=self.grid();x['relative_phase_rad']=[[.4,.4],[.4,.4]]
        a=spectral_overlap(x);x['relative_phase_rad']=[[-.4,-.4],[-.4,-.4]];b=spectral_overlap(x)
        self.assertAlmostEqual(a['gamma_abs'],b['gamma_abs'])
        self.assertAlmostEqual(a['gamma_im'],-b['gamma_im'])
    def test_missing_tail_cannot_be_silently_normalized_away(self):
        b=tail_overlap_bounds(.99,.005,.005)
        self.assertAlmostEqual(b['lower'],.98005)
        self.assertAlmostEqual(tail_overlap_bounds(1,0,0)['lower'],1)
        self.assertEqual(tail_overlap_bounds(0,.1,.1)['lower'],0)
    def test_invalid_grid_negative_nan_plane(self):
        for key,val in [('nu_A_THz',[1,1]),('cw_density',[[1,-1],[1,1]]),('ccw_density',[[1,1],[1,float('nan')]]),('relative_phase_rad',[[0]]),('reference_plane','BEFORE_FILTERS')]:
            x=self.grid();x[key]=val
            with self.subTest(key=key), self.assertRaises(ValueError):spectral_overlap(x)

if __name__=='__main__':unittest.main(verbosity=2)
