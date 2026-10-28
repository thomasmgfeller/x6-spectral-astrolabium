"""Analytical falsification controls, independent of archived detector answers."""
import unittest
from fractions import Fraction as F
from flint import arb, acb, ctx
import numpy as np
import adapter as a


class AdapterTests(unittest.TestCase):
    def setUp(self):
        ctx.prec=128
        self.mesh=a.certify_mesh(np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1.]]))
        self.M=a.mass_matrix(self.mesh)
        self.V=arb(1)/6

    def test_constant_projection_and_conservation(self):
        b=[[acb(self.V/4)] for _ in range(4)]
        c=a.project(self.M,b)
        for row in c:self.assertTrue(row[0].contains(1))
        self.assertTrue(sum(self.V/4*row[0] for row in c).real.contains(self.V))

    def test_affine_reproduction(self):
        nodal=[arb(2),arb(3),arb(4),arb(6)]
        b=[[acb(sum(self.M[i,j]*nodal[j] for j in range(4)))] for i in range(4)]
        c=a.project(self.M,b)
        for z,v in zip(c,nodal):self.assertTrue(z[0].real.contains(v))

    def test_true_projection_idempotent(self):
        b=[[acb(self.V*(arb(1)/20 if i==1 else arb(1)/60))] for i in range(4)]
        c=a.project(self.M,b)
        again=a.project(self.M,[[sum(self.M[i,j]*c[j][0] for j in range(4))] for i in range(4)])
        for i in range(4):self.assertTrue(c[i][0].overlaps(again[i][0]))
        self.assertTrue(c[1][0].real.contains(arb(3)/5))
        self.assertTrue(c[0][0].real.contains(-arb(1)/15))
        # A positive partition of unity does not make L2 projection positive.
        self.assertTrue(c[0][0].real<0)

    def test_zero_nodal_samples_do_not_erase_integral_source(self):
        # f=product(lambda_i), zero at ALL original vertices, but P f=1/840.
        b=[[acb(self.V/3360)] for _ in range(4)]
        c=a.project(self.M,b)
        for row in c:self.assertTrue(row[0].real.contains(arb(1)/840));self.assertTrue(row[0].real>0)
        e2=a.l2_residual_squared(self.V/415800,b,c,0)
        exact=self.V*(arb(1)/415800-arb(1)/705600)
        self.assertTrue(e2.contains(exact));self.assertTrue(e2>0)
        self.assertTrue(e2/(self.V/415800)>arb('0.4'))

    def test_nontrivial_gram_stability(self):
        lower,inv=a.gram_min_eigenvalue_bound(self.M)
        self.assertTrue(lower>0)
        self.assertTrue(lower<=self.V/20)
        self.assertTrue(inv[0,0]>0)

    def test_mesh_rejects_duplicates_and_missing_tetrahedron(self):
        p=np.vstack([self.mesh['points'],[.1,.1,.1]])
        good=a.certify_mesh(p)
        with self.assertRaises(ArithmeticError):a.certify_mesh(p,good['tetrahedra'][:-1])
        with self.assertRaises(ArithmeticError):a.certify_mesh(np.vstack([p,p[0]]))

    def test_certified_source_coverage_and_cubature(self):
        p=np.array([[2,2,2],[2,-2,-2],[-2,2,-2],[-2,-2,2.]])
        mesh=a.certify_mesh(p)
        self.assertTrue(a.ball_covered(mesh))
        self.assertFalse(a.ball_covered(self.mesh))
        B,count=a.integrate_load(mesh,2)
        self.assertEqual(count,4)
        volume=a.ball_fraction(sum(mesh['volumes']))
        for row in B:self.assertTrue(row[0].real.contains(volume/4))
        # Never infer zero just because all quadrature-cell vertices miss the bump.
        self.assertTrue(any(not row[4].is_zero() for row in B))

    def test_general_g_and_signed_time_history(self):
        for t in [-2,-1,0,1,2]:
            z=a.history_polynomial(t,[acb(2),acb(3)],[acb(5),acb(7)])
            exact=arb(2)+5*t-arb(3)*t*t/2-arb(7)*t**3/6
            self.assertTrue(z.real.overlaps(exact))

    def test_wave_moments_against_independent_integral(self):
        mesh=self.mesh;vertices=mesh['rational_points'];v=mesh['volumes'][0]
        # Reference tetrahedron: marginal cross-section area (1-z)^2/2.
        got=a.wave_simplex_load(vertices,v,2)
        ordinary=acb.integral(lambda z,analytic:(acb(0,2)*z).exp()*(1-z)**3/6,0,1)
        top=acb.integral(lambda z,analytic:(acb(0,2)*z).exp()*z*(1-z)**2/2,0,1)
        for j in range(4):self.assertTrue(got[j].overlaps(top if j==3 else ordinary))

    def test_general_g_remainder_not_omitted(self):
        v=a.temporal_remainder(-2,0,arb(3),arb(5))
        expected=(arb(6)+arb(20)/3)/(8*arb.pi()).sqrt()
        self.assertTrue(v.overlaps(expected));self.assertTrue(v>0)
        self.assertTrue(a.temporal_remainder(0,1,arb(3),arb(5)).is_zero())

    def test_retarded_finite_error_recursion(self):
        K=[[F(0)]*4 for _ in range(4)]
        K[2][0]=F(2);K[2][1]=F(-3);K[3][1]=F(1);K[3][2]=F(-2)
        e=a.finite_retarded_bound(K,[F(1,10),F(1,5)],[F(1,100),F(1,50)])
        self.assertEqual(e,[F(1,10),F(1,5),F(81,100),F(46,25)])
        K[0][0]=1
        with self.assertRaises(ArithmeticError):a.finite_retarded_bound(K,[F(1,10)], [F(0)]*3)

    def test_signed_detector_transfer_bound_attainable(self):
        T=[acb(3),acb(-4),acb(0,2)];e=[arb(1)/10,arb(1)/5,arb(3)/10]
        perturb=[acb(e[0]),acb(-e[1]),acb(0,-e[2])]
        exact=sum(t*d for t,d in zip(T,perturb))
        self.assertTrue(a.transfer_bound(T,e).contains(exact.real))

if __name__=='__main__':unittest.main(verbosity=2)
