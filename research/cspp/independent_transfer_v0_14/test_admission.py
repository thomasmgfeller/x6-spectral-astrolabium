import copy
from fractions import Fraction as F
from math import comb
import unittest
from flint import arb, acb, ctx
import admission as a
from inference import observables, moments, confidence_interval, classify, sufficient_size


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        ctx.prec = 192

    def test_source_geometry_independent_integral(self):
        self.assertEqual(a.exact_geometry()['source_volume_over_pi'], F(7,16))
        self.assertEqual(a.exact_geometry()['history_volume_over_pi'], 27)

    def test_probability_and_macro_scope(self):
        s = a.structural_certificates()
        self.assertTrue(s['zero_response_probability_lower'] > arb('.2691463487'))
        self.assertTrue(s['joint_historical_tolerance_success_probability_upper'] < arb('.7308536513'))
        self.assertFalse(s['macroscopic_mean_rejected'])
        self.assertFalse(s['new_RMS_target_selected'])

    def test_original_rms_floors_rederived(self):
        s = a.structural_certificates()
        for z, lower in zip(s['RMS_error_floor_enclosures'], ['.0107911599','.0045552310']):
            self.assertTrue(z > arb(lower))

    def test_positive_probability_adapter_failure(self):
        s = a.structural_certificates()
        self.assertTrue(0 < s['nonlocal_undefined_probability_lower'] < arb('1e-30'))

    def test_fourth_moment_control_is_not_prediction(self):
        s = a.structural_certificates()
        self.assertTrue(s['local_fourth_moment_majorant'] > s['local_second_moment_majorant']**2)
        self.assertFalse(s['moment_majorants_are_predictions'])

    def test_controls_do_not_release_original(self):
        checks = a.read(a.PREVIOUS/'results/CHECKS.json')
        pred = a.read(a.PREVIOUS/'results/PREDICTIONS_192.json')
        result = a.assess(checks, pred, {'local_H1': {'control_reproduction':'PASS'}})
        self.assertEqual(result['local_H1']['decision'], 'REJECTED_FOR_CONFIRMATORY_RUN')
        self.assertIn('joint_original_moments', result['local_H1']['missing_certificates'])

    def test_unknown_evidence_revision_is_not_silently_accepted(self):
        checks = a.read(a.PREVIOUS/'results/CHECKS.json')
        pred = copy.deepcopy(a.read(a.PREVIOUS/'results/PREDICTIONS_192.json'))
        pred['original_ensemble_moments'] = 'CERTIFIED'
        with self.assertRaises(ValueError): a.assess(checks, pred, {})

    def test_pass_labels_cannot_override_missing_certificate(self):
        checks = a.read(a.PREVIOUS/'results/CHECKS.json')
        pred = a.read(a.PREVIOUS/'results/PREDICTIONS_192.json')
        evidence = {k:'PASS' for k in a.read(a.HERE/'PROTOCOL.json')['required_method_certificates']}
        with self.assertRaises(ValueError): a.assess(checks, pred, {'local_H1':evidence})

    def test_substitute_control_model_cannot_be_admitted(self):
        checks = a.read(a.PREVIOUS/'results/CHECKS.json')
        pred = a.read(a.PREVIOUS/'results/PREDICTIONS_192.json')
        with self.assertRaises(ValueError): a.assess(checks, pred, {'oscillator':{}})

    def test_two_windows_are_one_four_component_unit(self):
        self.assertEqual(len(observables([1,2,3,4])), 14)
        with self.assertRaises(ValueError): observables([1,2])

    def test_joint_complex_moments_from_exact_two_state_law(self):
        x = [arb(1),arb(2),arb(3),arb(4)]
        y = [arb(-2),arb(1),arb(0),arb(-1)]
        theta = [(u+v)/2 for u,v in zip(observables(x), observables(y))]
        mu, C, P = moments(theta)
        z = [acb(x[r],x[r+2]) for r in range(2)]
        w = [acb(y[r],y[r+2]) for r in range(2)]
        for r in range(2):
            self.assertTrue(mu[r].contains((z[r]+w[r])/2))
            for s in range(2):
                self.assertTrue(C[r][s].contains((z[r]-w[r])*(z[s]-w[s]).conjugate()/4))
                self.assertTrue(P[r][s].contains((z[r]-w[r])*(z[s]-w[s])/4))
        self.assertFalse(P[0][1].contains(0))

    def test_equal_second_moment_does_not_fix_fourth(self):
        # Rademacher and P(0)=3/4, P(+/-2)=1/8 have identical mean/variance.
        laws = [[(F(-1),F(1,2)),(F(1),F(1,2))],
                [(F(0),F(3,4)),(F(-2),F(1,8)),(F(2),F(1,8))]]
        ms = [[sum(p*x**k for x,p in law) for k in [1,2,4]] for law in laws]
        self.assertEqual(ms[0][:2], ms[1][:2]); self.assertNotEqual(ms[0][2], ms[1][2])

    def test_nonrejection_is_not_equivalence(self):
        self.assertEqual(classify(arb(0,2),arb(0),arb('.1')), 'INCONCLUSIVE')
        self.assertEqual(classify(arb(0,'.01'),arb(0),arb('.1')), 'PASS')
        self.assertEqual(classify(arb(1,'.01'),arb(0),arb('.1')), 'REJECT')

    def test_prediction_and_numerical_uncertainty_retained(self):
        c = confidence_interval(0, '.2', 0, 1, '.1')
        self.assertEqual(classify(c,arb(0),arb('.1')), 'INCONCLUSIVE')
        self.assertEqual(classify(arb(0),arb(0,'.2'),arb('.1')), 'INCONCLUSIVE')

    def test_chebyshev_coverage_by_exact_binomial_enumeration(self):
        # A deterministic unit test, not a model-validation ensemble.
        n = 16; outside = F(0)
        for k in range(n+1):
            interval = confidence_interval(arb(k)/n, 0, '1/4', n, '1/4')
            if not interval.contains(arb('1/2')):
                outside += F(comb(n,k),2**n)
        self.assertLessEqual(outside, F(1,4))

    def test_conditional_power_size_and_nonshrinkable_error(self):
        n = sufficient_size(1,'1/4','1/4',1,'1/10','1/20')
        self.assertGreaterEqual(n,25); self.assertLessEqual(n,26)
        with self.assertRaises(ValueError): sufficient_size(1,'1/4','1/4','1/5','1/10','1/20')

    def test_no_new_design_or_random_calls(self):
        d = a.compute(128)
        self.assertTrue(all(v is None for v in d['new_design'].values()))
        self.assertEqual(d['new_random_clouds'],0); self.assertEqual(d['new_rng_calls'],0)
        self.assertFalse(d['confirmation_seed_used'])
        self.assertIsNone(d['fresh_data_evidence'])
        self.assertEqual(d['fluctuation_prediction_decision'],'NOT_TESTED_METHOD_GATE_FAILED')


if __name__ == '__main__': unittest.main(verbosity=2)
