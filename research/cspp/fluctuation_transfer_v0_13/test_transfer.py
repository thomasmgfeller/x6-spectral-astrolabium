import sys,unittest
from pathlib import Path
from fractions import Fraction as F
from math import factorial,comb
import numpy as np
from flint import arb,acb,ctx,fmpq as Q
from kernel import *
from algebra import *
from transfer import *
import geometry,oscillator

class Bernoulli:
    def moment(self,powers):return arb(0 if sum(powers)%2 else 1)

class TransferTests(unittest.TestCase):
    def setUp(self):ctx.prec=128

    def test_one_point_closed_poisson_formula(self):
        for e in [F(1,16),F(1,4),F(1)]:
            law=JointWeights([({0},F(7,3))],e,(0,))
            u=ball(e)*arb(7)/3
            expected=(-u).exp()*(1-9*u+8*u*u-arb(4)/3*u**3)
            self.assertTrue(law.moment((1,)).overlaps(expected))

    def test_two_point_matches_previous_independent_kernel(self):
        sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'variance_budget_v0_4'))
        import variance as v4
        for e in [F(1,16),F(1,4),F(1)]:
            for shifts in [(0,0),(1,0),(0,1)]:
                means=F(3,2),F(7,3),F(2,3)
                law=JointWeights([({0},means[0]-means[2]),({1},means[1]-means[2]),({0,1},means[2])],e,shifts)
                expected=v4.joint_kernel(v4.palm(C,e,shifts[0]),v4.palm(C,e,shifts[1]),e*means[0],e*means[1],e*e*means[2])
                self.assertTrue(law.moment((1,1)).overlaps(expected))

    def test_disjoint_factorization(self):
        law=JointWeights([({0},2),({1},3)],F(1,16),(0,0))
        self.assertTrue(law.moment((2,1)).overlaps(law.moment((2,0))*law.moment((0,1))))

    def test_repeated_factor_is_same_noise(self):
        law=JointWeights([({0},2)],F(1,16),(0,))
        self.assertTrue(law.moment((2,))>law.moment((1,))**2)

    def test_multiple_Palm_insertions_against_count_sum(self):
        lam=arb(2);law=JointWeights([({0},2)],F(1,4),(3,))
        total=sum(((-lam).exp()*lam**n/factorial(n)*weight(n,F(1,4),3) for n in range(51)),arb(0))
        err=16*poisson_chernoff_tail(lam,50)
        self.assertLessEqual((law.moment((1,))-total).abs_lower(),err)

    def test_pair_function_covariance(self):
        a,b,j,c=pair_weight_covariance(2,3,1,1,F(1,16))
        self.assertTrue((j-a*b-c).contains(0));self.assertFalse(c.contains(0))

    def test_Mecke_centering_uses_unshifted_means(self):
        a,b,j,c=pair_weight_covariance(2,3,1,1,F(1,16),1,0)
        aa,bb,_,_=pair_weight_covariance(2,3,1,1,F(1,16),0,0)
        m=mecke_connected_pair(2,3,1,1,F(1,16),1,0)
        self.assertTrue((m-j+aa*bb).contains(0));self.assertFalse((m-c).contains(0))

    def test_reject_invalid_overlap(self):
        with self.assertRaises(ArithmeticError):pair_weight_covariance(1,1,2,1,F(1,16))

    def test_geometry_single_volume_and_half(self):
        self.assertEqual(vertical_overlap_over_pi(-2,0,-2,0,0),Q(2,3))
        self.assertEqual(vertical_overlap_over_pi(-2,0,-2,0,0,-1),Q(1,3))

    def test_geometry_symmetry_disjoint_nested(self):
        a=vertical_overlap_over_pi(-2,0,-2,1,Q(1,2))
        self.assertEqual(a,vertical_overlap_over_pi(-2,1,-2,0,Q(1,2)))
        self.assertEqual(vertical_overlap_over_pi(-2,0,-2,0,3),0)
        self.assertEqual(vertical_overlap_over_pi(-2,0,-3,1,0),Q(2,3))

    def test_geometry_atom_partition(self):
        atoms,g=control_atoms()
        for i,expected in enumerate([F(2),F(81,8),F(9,128),F(135,256)]):
            self.assertEqual(sum(mean for mask,mean in atoms if i in mask),expected)
        self.assertEqual(sum(mean for mask,mean in atoms if 0 in mask and 2 in mask),0)

    def test_generic_box_overlap_encloses_exact_lens(self):
        ints=[((-2,0,0,0),(0,0,0,0)),((-2,0,0,F(1,2)),(1,0,0,F(1,2)))]
        coarse,_=geometry.overlap(ints,8);fine,info=geometry.overlap(ints,12)
        target=arb(15)*arb.pi()/32
        self.assertTrue(coarse.contains(target));self.assertTrue(fine.contains(target))
        self.assertLessEqual(fine.rad(),coarse.rad());self.assertGreater(info['unresolved_boxes'],0)

    def test_empty_temporal_overlap(self):
        z,_=geometry.overlap([((-2,0,0,0),(-1,0,0,0)),((0,0,0,0),(1,0,0,0))])
        self.assertTrue(z.is_zero())

    def test_spacelike_interval_rejected(self):
        with self.assertRaises(ArithmeticError):geometry.overlap([((0,0,0,0),(1,2,0,0))])

    def test_exact_retarded_expansion(self):
        law=JointWeights(control_atoms()[0]);K,b=skeleton(law)
        orders=causal_orders(K,b,law);full=solve_polynomial(K,b)
        for values in [[1,1,1,1],[0,-1,F(1,2),F(-1,3)]]:
            for i in range(4):
                self.assertTrue((full[i].evaluate(values)-sum(row[i].evaluate(values) for row in orders)).contains(0))

    def test_mean_first_variation_is_zero(self):
        law=JointWeights(control_atoms()[0]);K,b=skeleton(law)
        self.assertTrue(all(v.mean(law).contains(0) for v in causal_orders(K,b,law)[1]))

    def test_random_inverse_must_not_be_frozen(self):
        x=Poly.variable(0);z=Poly();K=[[z,z,z],[x,z,z],[z,x,z]];b=[Poly.const(1),z,z]
        orders=causal_orders(K,b,Bernoulli())
        self.assertTrue(orders[0][2].mean(Bernoulli()).is_zero())
        self.assertTrue(solve_polynomial(K,b)[2].mean(Bernoulli()).contains(1))
        self.assertTrue(orders[2][2].mean(Bernoulli()).contains(1))

    def test_random_detector_is_included(self):
        x=Poly.variable(0);orders=[[Poly.const(1)],[x]];Q=[[1+x]]
        result=observation_orders(Q,orders,Bernoulli())
        self.assertTrue(sum(row[0].mean(Bernoulli()) for row in result).contains(2))
        self.assertTrue(result[2][0].mean(Bernoulli()).contains(1))

    def test_zero_initial_correlation_mean_closure_specific_graph(self):
        law=JointWeights(control_atoms()[0]);K,b=skeleton(law,F(0))
        full=solve_polynomial(K,b);orders=causal_orders(K,b,law)
        self.assertTrue(all((full[i].mean(law)-orders[0][i].mean(law)).contains(0) for i in [2,3]))

    def test_predictions_remainders_and_negative_controls(self):
        r=predict_skeleton()
        for name,counter in r['counterfactuals'].items():
            discrepancy=max((r['covariance'][i][j]-counter['covariance'][i][j]).abs_lower() for i in range(2) for j in range(2))
            self.assertGreater(discrepancy,arb('1e-8'),name)
        self.assertFalse(r['third_joint_centered_moment_ABH'].contains(0))
        self.assertTrue(r['covariance_determinant'].real>0)

    def test_real_covariance_and_nonproper_complex_signal(self):
        r=predict_skeleton();C=np.array([[complex(float(z.real.mid()),float(z.imag.mid())) for z in row] for row in r['covariance']]);P=np.array([[complex(float(z.real.mid()),float(z.imag.mid())) for z in row] for row in r['relation']])
        real=np.block([[np.real(C+P),np.imag(P-C)],[np.imag(P+C),np.real(C-P)]])/2
        self.assertGreater(np.linalg.norm(P),1e-5)
        self.assertGreaterEqual(np.linalg.eigvalsh(real).min(),-1e-18)

    def test_original_geometry_zero_source_prediction(self):
        p=original_source_predictions();q=(-arb(21)/16).exp()
        self.assertTrue(p['zero_response_probability_lower'].overlaps(q))
        self.assertTrue(q>arb('.26') and q<arb('.28'))
        self.assertTrue(all(v>arb('.001') for v in p['RMS_error_lower']))
        self.assertTrue(p['nonlocal_adapter_fewer_than_four_history_points_probability']>0)

    def test_path_tail_deterministic_inequality(self):
        alpha=arb(2);b=arb(1)/20;R=3
        for n in range(4,25):
            lhs=sum(comb(n,k)*b**k for k in range(R+1,n+1))
            self.assertLessEqual(lhs,alpha**(-R-1)*(1+alpha*b)**n)

    def test_original_tail_certificates_tighten(self):
        a=original_local_history_envelopes(64,768);b=original_local_history_envelopes(128,1024)
        self.assertLess(b['path_tail_L2_upper'],a['path_tail_L2_upper'])
        self.assertLess(b['count_tail_L2_upper'],a['count_tail_L2_upper'])
        self.assertLess(b['finite_weight_max_upper'],b['weight_global_upper'])

    def test_oscillator_exact_window_direct_integral(self):
        for sign in [-1,1]:
            w=(1+arb(sign)/4).sqrt();f=1+arb(sign)/5;g=arb(sign)/10
            z=acb.integral(lambda t,analytic:f*(w*t).cos()+g*(w*t).sin()/w,acb('7/4'),acb(2),abs_tol=arb('1e-25'))*4
            self.assertTrue(z.real.overlaps(oscillator.average(sign,arb('7/4'),arb(2))))

    def test_oscillator_mean_shift_and_quadratic_correction(self):
        r=oscillator.predict()
        for w in r['windows']:
            self.assertFalse(w['mean_shift'].contains(0))
            self.assertLess((w['mean_shift']-w['quadratic_mean_correction']).abs_upper(),w['mean_shift'].abs_lower())
        C=r['covariance'];self.assertTrue((C[0][0]*C[1][1]-C[0][1]*C[1][0]).contains(0))

    def test_same_two_moments_do_not_determine_path_mean(self):
        a=-1/arb(2).sqrt();b=arb(2).sqrt()
        self.assertTrue((2*a/3+b/3).contains(0));self.assertTrue((2*a*a/3+b*b/3).contains(1))
        self.assertTrue(2*a**3/3+b**3/3>0)  # Symmetric +/-1 has the same mean/variance, but zero third moment.

if __name__=='__main__':unittest.main(verbosity=2)
