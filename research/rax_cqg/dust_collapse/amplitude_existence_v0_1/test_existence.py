import unittest
import itertools
import json
import math
import sympy as s
from existence import *

class ExistenceTests(unittest.TestCase):
    def test_reconstructed_carrier_matches_inherited_33(self):
        data=json.loads((ROOT/'inputs/aa_hessians.json').read_text())
        self.assertEqual(aa_codes(),sorted(r['order_code'] for r in data['histories']))
        self.assertEqual(len(aa_codes()),33)

    def test_independent_hessians_match_all_inherited_matrices(self):
        for r in json.loads((ROOT/'inputs/aa_hessians.json').read_text())['histories']:
            self.assertEqual(reconstruct_h0(r['order_code']),s.Matrix(r['H0_over_va']))

    def test_uniform_gap_and_joint_norm_ratio(self):
        for c in aa_codes():
            h=reconstruct_h0(c);rel=relations(c);k=sum((i,2) in rel for i in (0,1))+sum((2,j) in rel for j in (3,4))
            self.assertIn(k,(2,3,4));self.assertEqual(h[2,2],-s.Rational(k,2))
            j=(BETA*h).extract([2],[0,1,3,4]);alpha=BETA*k/2
            self.assertEqual(s.simplify((j*j.T)[0]/alpha**2),s.Rational(1,k))

    def test_mass_cannot_close_gap(self):
        x=s.symbols('m2ell2',nonnegative=True)
        for k in (2,3,4):self.assertTrue((BETA*k/2+x-BETA).is_nonnegative)

    def test_scalar_and_dust_inputs_retain_separation(self):
        contract=json.loads((ROOT/'inputs/action_contract.json').read_text())
        self.assertEqual(contract['parameters']['direct_dust_scalar_coupling'],0)
        self.assertIn('not directly on T or w',contract['action']['dependence'])
        boundary=json.loads((ROOT/'inputs/boundary_contract.json').read_text())
        self.assertEqual(boundary['density_masks']['plus'],['10','01','11'])

    def test_density_fourier_formula_and_removable_limit(self):
        k=s.symbols('k',real=True,nonzero=True);r=s.symbols('r',real=True)
        direct=s.integrate(s.exp(-s.I*k*r),(r,0,1))
        self.assertEqual(s.simplify(direct-(1-s.exp(-s.I*k))/(s.I*k)),0)
        self.assertEqual(s.limit(direct,k,0),1)

    def test_density_factors_match_mask_enumeration(self):
        u,v=s.symbols('u v');f=[s.Rational(1,2),u/2];g=[s.Rational(1,2),v/2]
        amplitudes={'zero':[2,0,0,0],'mixed':[0,s.sqrt(2),s.sqrt(2),0],'double':[0,0,0,2],'plus':[0,2/s.sqrt(3),2/s.sqrt(3),2/s.sqrt(3)]}
        masks=[(0,0),(1,0),(0,1),(1,1)]
        for name,a in amplitudes.items():
            brute=sum(a[i]*f[x]*g[y] for i,(x,y) in enumerate(masks))
            self.assertEqual(s.simplify(brute-sector_factor(name,u,v)),0)

    def test_density_factors_at_zero_action_equal_L1_masses(self):
        expected={'zero':s.Rational(1,2),'mixed':1/s.sqrt(2),'double':s.Rational(1,2),'plus':s.sqrt(3)/2}
        for name,a in expected.items():self.assertEqual(s.simplify(sector_factor(name,1,1)-a),0)

    def test_stable_density_factor_numerical_controls(self):
        for k in (0,1e-14,-1e-8,.5,1,-4,20,100):
            value=positive_density_integral(k)
            self.assertLessEqual(abs(value),1+1e-15)
            self.assertAlmostEqual(abs(value.conjugate()-positive_density_integral(-k)),0,places=14)
        self.assertEqual(positive_density_integral(0),1)

    def test_scalar_L1_norms_direct_integrals(self):
        x,y=s.symbols('x y',real=True)
        h0=s.exp(-(x*x+y*y)/2)/s.sqrt(s.pi)
        h1=s.sqrt(2)*x*h0
        self.assertEqual(s.integrate(s.integrate(h0,(x,-s.oo,s.oo)),(y,-s.oo,s.oo)),2*s.sqrt(s.pi))
        self.assertEqual(s.integrate(s.integrate(s.Abs(h1),(x,-s.oo,s.oo)),(y,-s.oo,s.oo)),4)

    def test_absolute_packet_second_moments(self):
        x=s.symbols('x',real=True)
        for n,variance in ((0,1),(1,2)):
            w=s.Abs(x)**n*s.exp(-x*x/2)
            result=s.integrate(x*x*w,(x,-s.oo,s.oo))/s.integrate(w,(x,-s.oo,s.oo))
            self.assertEqual(result,variance)

    def test_interior_gaussian_modulus_bound(self):
        for a,eta,e in itertools.product((float(BETA),2.,5.),(0.,1.,-3.,20.),(0.,1e-8,.01,1.)):
            self.assertLessEqual(abs(scalar_inner(a,eta,e)),math.sqrt(2*math.pi/a)*(1+1e-14))

    def test_abel_linear_error_pointwise_control(self):
        for a,eta,e in itertools.product((float(BETA),3.),(0.,1.,-3.),(1e-5,.001,.05)):
            bound=e*math.sqrt(2*math.pi/a)*(1/(2*a)+eta*eta/(2*a*a))
            self.assertLessEqual(abs(scalar_inner(a,eta,e)-scalar_inner(a,eta,0)),bound*(1+1e-10))

    def test_interior_phase_at_zero_source(self):
        a=float(BETA)
        expected=math.sqrt(2*math.pi/a)*cmath.exp(-.25j*math.pi)
        self.assertAlmostEqual(abs(scalar_inner(a,0,0)-expected),0,places=14)

    def test_quotient_and_packet_bound_matrix(self):
        a={'zero':s.Rational(1,2),'plus':s.sqrt(3)/2};l=[2*s.sqrt(s.pi),4]
        labels=[('zero',0),('zero',1),('plus',0),('plus',1)]
        independent=s.Matrix(4,4,lambda i,j:s.sqrt(2*s.pi/BETA)*a[labels[i][0]]*a[labels[j][0]]*l[labels[i][1]]*l[labels[j][1]]/2)
        self.assertEqual(s.simplify(independent-bound_matrix()),s.zeros(4))

    def test_full_Q_coupled_singular_interior(self):
        e=s.symbols('eps',nonnegative=True)
        Q=s.Matrix([[1,-s.I],[-s.I,e]])
        self.assertEqual(Q.det(),1+e);self.assertEqual(Q.subs(e,0).det(),1)

    def test_pointwise_criterion_misses_density_endpoint_divergence(self):
        e,r=s.symbols('eps r',positive=True)
        Q=s.Matrix([[1,-s.I*r],[-s.I*r,e]])
        self.assertEqual(Q.det(),e+r*r)
        self.assertEqual(Q.subs(e,0).det(),r*r)
        primitive=s.asinh(r/s.sqrt(e))
        self.assertEqual(s.simplify(s.diff(primitive,r)-1/s.sqrt(e+r*r)),0)
        self.assertEqual(s.limit(s.asinh(1/s.sqrt(e)),e,0,dir='+'),s.oo)

    def test_log_divergence_coefficient(self):
        e=s.symbols('e',positive=True)
        self.assertEqual(s.limit(s.asinh(1/s.sqrt(e))+s.log(e)/2,e,0,dir='+'),s.log(2))

    def test_integrable_continuous_singularity_and_atom_divergence(self):
        e,r=s.symbols('e r',positive=True)
        primitive=2*s.I*(s.sqrt(e-s.I*r)-s.sqrt(e))
        self.assertEqual(s.simplify(s.diff(primitive,r)-(e-s.I*r)**(-s.Rational(1,2))),0)
        self.assertEqual(s.simplify(s.expand_complex(s.limit(primitive.subs(r,1),e,0,dir='+'))-s.sqrt(2)*(1+s.I)),0)
        self.assertEqual(s.integrate(r**(-s.Rational(1,2)),(r,0,1)),2)
        self.assertEqual(s.limit(e**(-s.Rational(1,2)),e,0,dir='+'),s.oo)

    def test_atom_strength_in_log_example(self):
        e=s.symbols('e',positive=True)
        total=1/(2*s.sqrt(e))+s.asinh(1/s.sqrt(e))/2
        self.assertEqual(s.limit(s.sqrt(e)*total,e,0,dir='+'),s.Rational(1,2))

    def test_box_integral_has_no_zero_hessian_pole(self):
        t,a=s.symbols('t a',real=True)
        # At the singular Hessian the actual normalized compact integral is one.
        self.assertEqual(s.integrate(s.exp(s.I*a*t*t/2).subs(a,0)/2,(t,-1,1)),1)

    def test_unnormalized_clock_removal_diverges(self):
        t=s.symbols('t',real=True);L=s.symbols('L',positive=True)
        self.assertEqual(s.integrate(1,(t,-L,L)),2*L)
        self.assertEqual(s.limit(2*L,L,s.oo),s.oo)

if __name__=='__main__':unittest.main()
