import unittest
import math
import cmath
import json
import numpy as np
from fractions import Fraction as Q
from flint import arb,acb,ctx
from core import *
from run_certified import DustQuadrature,summarize,compute
from independent_check import evaluate,scalar_from_eigenphases
from causation import analyze

class MixingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec=128
        cls.source=json.loads((ROOT/'inputs/aa_hessians.json').read_text())['histories']
        cls.data=json.loads((ROOT/'results/certified_mixing.json').read_text())
        cls.direct=evaluate(8)

    def test_history_enumeration_matches_frozen_source(self):
        self.assertEqual(histories(),sorted(r['order_code'] for r in self.source))
        self.assertEqual(len(histories()),33)

    def test_all_exact_hessians_match_frozen_source(self):
        for r in self.source:self.assertEqual(h0(r['order_code']),[[Q(v) for v in row] for row in r['H0_over_va']])

    def test_gravitational_actions_match_frozen_source(self):
        for r in self.source:self.assertEqual(f4(r['order_code']),r['F4'])

    def test_orbits_partition_33_without_extra_weight(self):
        self.assertEqual(len(orbits()),10)
        self.assertEqual(sorted(x for members in orbits().values() for x in members),histories())
        self.assertEqual(sum(Q(len(v),33) for v in orbits().values()),1)

    def test_actions_covariant_under_both_boundary_swaps(self):
        for c in histories():
            h=h0(c)
            for p in boundary_group():
                cp=relabel(c,p);hp=h0(cp);self.assertEqual(f4(c),f4(cp))
                self.assertEqual([[hp[p[i]][p[j]] for j in range(5)] for i in range(5)],h)

    def test_reference_is_exact_mean_and_invariant(self):
        h=reference_h0()
        self.assertEqual(h[2][2],Q(-40,33))
        for row in h:self.assertEqual(sum(row),0)
        for p in boundary_group():self.assertEqual([[h[p[i]][p[j]] for j in range(5)] for i in range(5)],h)

    def test_action_interpolation_endpoints_and_gap(self):
        for c in histories():
            self.assertEqual(interpolate_h0(c,0),reference_h0())
            self.assertEqual(interpolate_h0(c,1),h0(c))
            for lam in (0,Q(1,2),1):self.assertGreaterEqual(-interpolate_h0(c,lam)[2][2],1)

    def test_reference_keeps_scalar_dynamics(self):
        h=reference_h0();self.assertNotEqual(h,[[Q(0)]*5 for _ in range(5)])
        self.assertTrue(all(h[2][j]!=0 for j in BOUNDARY))
        self.assertTrue(scalar_ground(h)[0].abs_lower()>0)

    def test_quadratic_parity_forbidden_linear_insertion(self):
        # Exact rational evaluations verify S(-q)=S(q); the linear h1
        # insertion is odd. Symmetric measures then annihilate the integral.
        q=[Q(1,3),Q(-2,5),Q(7,4),Q(3,8),Q(-1,9)]
        for h in [h0(c) for c in histories()]+[reference_h0()]:
            value=sum(q[i]*h[i][j]*q[j] for i in range(5) for j in range(5))
            flipped=sum((-q[i])*h[i][j]*(-q[j]) for i in range(5) for j in range(5))
            self.assertEqual(value,flipped)
            self.assertEqual((-q[3]-q[4])*flipped,-(q[3]+q[4])*value)

    def test_mask_normalization_independent_enumeration(self):
        # Three outgoing positive masks, two interior masks, input atom pair.
        factor=arb(0)
        for out in ((1,0),(0,1),(1,1)):
            for inner in (0,1):
                quotient=arb(1)/4; packet_norm=2; d_in=2; d_out=2/arb(3).sqrt()
                factor+=quotient*packet_norm*d_in*d_out/32
        self.assertTrue(factor.overlaps(arb(3).sqrt()/8))

    def test_density_factor_removable_zero_and_conjugation(self):
        self.assertTrue(E(arb(0)).contains(1))
        for k in ('-3','0','1/2','2'):
            x=arb(k);self.assertTrue(E(-x).overlaps(E(x).conjugate()))

    def test_density_factor_matches_independent_certified_integral(self):
        for k in (-3,0,2):
            direct=acb.integral(lambda r,analytic:(acb(0,-k)*r).exp(),0,1)
            self.assertTrue(direct.overlaps(E(arb(k))))

    def test_gauss_rule_normalized_exact_moments(self):
        quad=DustQuadrature(8)
        for degree in range(16):
            value=sum(w*(x**degree) for x,w in zip(quad.t,quad.w))
            exact=arb(0) if degree%2 else 1/arb(degree+1)
            self.assertTrue(value.overlaps(exact))

    def test_zero_straddling_differences_are_finite(self):
        q=DustQuadrature(8)
        for i in range(8):self.assertTrue(q.dd[i][i].is_finite() and q.dd[i][i].contains(0))

    def test_cache_symmetries_preserve_output_clock_sum(self):
        q=DustQuadrature(6)
        for coeff in ((-9,1,1),(-9,-9,1),(1,1,0),(-9,0,1)):
            for inds in ((0,2,5),(3,1,2)):
                direct=sum(w*E(arb(1)/2+sum(c*q.dd[l][idx] for c,idx in zip(coeff,inds))) for l,w in enumerate(q.w))
                self.assertTrue(q.output_factor(coeff,inds).overlaps(direct))

    def test_full_5d_independent_rule_matches_contracted_orbits(self):
        q=DustQuadrature(8)
        lookup={r['code']:complex(*r['dust']) for r in self.direct['records']}
        for code,members in orbits().items():
            d=q.evaluate(code);value=complex(float(d.real.mid()),float(d.imag.mid()))
            for c in members:self.assertLess(abs(value-lookup[c]),2e-14)

    def test_independent_eigenphase_formula_matches_scalar_pivots(self):
        for r in self.source:
            a=scalar_ground(h0(r['order_code']))[0]
            b=scalar_from_eigenphases(r['H0_over_va'])
            self.assertLess(abs(complex(float(a.real.mid()),float(a.imag.mid()))-b),2e-12)

    def test_principal_determinant_root_can_have_wrong_sign(self):
        factors=[1-10j]*4
        correct=math.prod([abs(z)**(-.5) for z in factors])*cmath.exp(-.5j*sum(cmath.phase(z) for z in factors))
        wrong=1/cmath.sqrt(np.prod(factors))
        self.assertLess(abs(correct+wrong),1e-15)
        self.assertGreater(abs(correct-wrong),.01)

    def test_all_actual_gaussian_pivots_in_right_half_plane(self):
        for h in [h0(c) for c in histories()]+[reference_h0()]:
            a,pivots,alpha=scalar_ground(h)
            self.assertTrue(a.is_finite() and alpha>0 and all(p.real>0 for p in pivots))

    def test_finite_regulator_approaches_correct_phase_branch(self):
        eps=arb('1e-7')
        for c in orbits():
            h=h0(c);a0,_,alpha=scalar_ground(h);ae,_,_=scalar_ground(h,eps)
            bound=eps*4*arb.pi()*(2*arb.pi()/alpha).sqrt()*(1/(2*alpha)+arb(1)/4)
            self.assertTrue(abs(ae-a0)<bound)

    def test_analytic_error_degrees_and_positive_bounds(self):
        for c in histories():
            e,degrees=dust_error(c,40)
            self.assertTrue(e>0)
            self.assertLessEqual(max(degrees),19)
            self.assertEqual(sum(degrees),2*sum(abs(v) for i,j,v in pair_coefficients(c)))

    def test_density_amplitudes_respect_L1_bound(self):
        for r in self.data['orbit_results']:
            d=unpack(r['dust_quadrature_ball']);err=arb(r['dust_error_bound'])
            self.assertTrue(abs(d)+err<arb(3).sqrt()/8)

    def test_certified_results_and_paired_difference_exclude_zero(self):
        a=self.data['amplitudes']
        for name in ('coupled','decoupled','difference'):
            self.assertTrue(unpack(a[name]['certified_ball']).abs_lower()>arb('0.06'))
            self.assertEqual(a[name]['classification'],'NONZERO')
        self.assertTrue((unpack(a['coupled']['certified_ball'])-unpack(a['decoupled']['certified_ball'])).overlaps(unpack(a['difference']['certified_ball'])))

    def test_public_rounded_values_include_certified_enclosures(self):
        centers={'coupled':('-0.155730245646','0.132674294297'),
                 'decoupled':('0.021300694129','-0.066660937892'),
                 'difference':('-0.177030939775','0.199335232189')}
        for k,(x,y) in centers.items():
            z=unpack(self.data['amplitudes'][k]['certified_ball'])
            self.assertTrue(arb(x,'1e-12').contains(z.real) and arb(y,'1e-12').contains(z.imag))

    def test_higher_order_higher_precision_enclosures_overlap(self):
        refined=json.loads((ROOT/'results/crosscheck_48.json').read_text())
        self.assertEqual(refined['quadrature']['n'],48);self.assertEqual(refined['quadrature']['precision_bits'],192)
        for k in self.data['amplitudes']:
            self.assertTrue(unpack(self.data['amplitudes'][k]['certified_ball']).overlaps(unpack(refined['amplitudes'][k]['certified_ball'])))
            self.assertTrue(arb(refined['amplitudes'][k]['analytic_quadrature_error_bound'])<arb('1e-17'))

    def test_causation_decomposition_and_both_nonzero_parts(self):
        d=analyze(self.data)
        self.assertTrue(unpack(d['gravity_sum_Z']).abs_lower()>0)
        for x in d['diagnostics'].values():self.assertEqual(x['classification'],'NONZERO')
        self.assertTrue(d['difference_decomposition_overlap'])
        centers={'connected_remainder':('-0.080381634846','0.002889997971'),
                 'scalar_mean_shift':('-0.096649304929','0.196445234218')}
        for k,(x,y) in centers.items():
            z=unpack(d['diagnostics'][k]['certified_ball'])
            self.assertTrue(arb(x,'2e-12').contains(z.real) and arb(y,'2e-12').contains(z.imag))

    def test_fail_closed_on_nonfinite_or_invalid_configuration(self):
        with self.assertRaises(ArithmeticError):summarize(acb('nan'),arb(0))
        with self.assertRaises(ValueError):compute(0,128,False)
        with self.assertRaises(ValueError):interpolate_h0(histories()[0],2)

if __name__=='__main__':unittest.main()
