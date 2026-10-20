"""Meaningful counterexamples and independent numerical/algebraic controls."""
import unittest
import numpy as np
from scipy.optimize._numdiff import approx_derivative
from cg_common import contract
from cg_relations import project, check, constraints, validate_order
from cg_analyze import simplex2


class Controls(unittest.TestCase):
    def test_missing_and_extra_relations_repaired(self):
        x = np.array([[0.,0.,0.],[1.,1.2,0.],[-.3,.1,.1],[.2,.05,-.05]])
        r = np.zeros((4,4),bool)
        r[0,1] = True
        # All other pairs must be spacelike, including two spurious initial edges.
        old = check(x,r)
        self.assertGreater(old['missing'],0)
        self.assertGreater(old['extra'],0)
        cfg = {**contract()['projection'],'maximum_relative_shift':10.}
        p = project(x,r,cfg)
        self.assertEqual(p['status'],'ACCEPTED')
        self.assertTrue(check(np.vstack(([0,0,0],p['features'])),r)['passed'])
        self.assertGreaterEqual(p['minimum_constraint_slack'],-1e-8)

    def test_order_input_rejection(self):
        for r in [np.eye(3),np.array([[0,1,0],[0,0,1],[0,0,0]]),np.ones((3,3))]:
            with self.assertRaises(ValueError): validate_order(r)

    def test_jacobian_and_transport(self):
        x = np.array([[0.,0.,0.],[1.,1.2,.1],[-.7,-.8,.2],[.1,.8,-.3]])
        r = np.zeros((4,4),bool)
        r[2,0] = r[0,1] = r[2,1] = True
        fun,jac,_ = constraints(x,r,1e-4)
        np.testing.assert_allclose(jac(x[1:].ravel()),approx_derivative(fun,x[1:].ravel()),atol=1e-7,rtol=1e-7)
        cfg = {**contract()['projection'],'maximum_relative_shift':10.}
        p = project(x,r,cfg)
        self.assertEqual(p['status'],'ACCEPTED')
        perm = np.array([0,3,1,2])
        q = project(x[perm],r[np.ix_(perm,perm)],cfg)
        a = np.vstack(([0,0,0],p['features']))
        b = np.vstack(([0,0,0],q['features']))
        np.testing.assert_allclose(a[perm],b,atol=2e-6)
        rot = np.array([[0.,-1.],[1.,0.]])
        y = x.copy(); y[:,1:] = y[:,1:]@rot
        q = project(y,r,cfg)
        a[:,1:] = a[:,1:]@rot
        np.testing.assert_allclose(a,np.vstack(([0,0,0],q['features'])),atol=2e-6)
        y = x.copy();y[:,0] *= -1
        q = project(y,r.T,cfg)
        a = np.vstack(([0,0,0],p['features']));a[:,0] *= -1
        np.testing.assert_allclose(a,np.vstack(([0,0,0],q['features'])),atol=2e-6)

    def test_shared_root_noise_and_duplicate_arm(self):
        w = np.array([[1.,2.,-1.],[1.,2.,-1.]])
        b = np.column_stack((-w.sum(axis=1),w))
        n = b@b.T
        self.assertEqual(n[0,0],10.)
        self.assertEqual((w@w.T)[0,0],6.)  # Omitting root is demonstrably wrong.
        f = simplex2(n)
        self.assertAlmostEqual(float(f@n@f),10.)
        self.assertAlmostEqual(float(np.array([.5,.5])@np.diag(np.diag(n))@np.array([.5,.5])),5.)
        rng = np.random.default_rng(70130000)
        # Noise repetitions on fixed geometry, NOT independent physical clouds.
        noise = rng.normal(size=(40000,4))@b.T
        np.testing.assert_allclose(np.cov(noise,rowvar=False),n,rtol=.025)

    def test_total_covariance_separation(self):
        # Exact finite ensemble: geometry and zero-mean noise have zero cross term.
        clean = np.array([[-2.,1.],[0.,-1.],[3.,2.]])
        maps = np.array([[[1.,0.],[.5,1.]],[[3.,0.],[1.,2.]],[[.2,0.],[.1,.4]]])
        eps = np.array([[1.,1.],[1.,-1.],[-1.,1.],[-1.,-1.]])
        observations = np.array([a+eps@b.T for a,b in zip(clean,maps)]).reshape(-1,2)
        total = np.cov(observations,rowvar=False,bias=True)
        geometry = np.cov(clean,rowvar=False,bias=True)
        noise = np.mean([b@b.T for b in maps],axis=0)
        np.testing.assert_allclose(total,geometry+noise,atol=1e-14)
        self.assertGreater(np.linalg.norm(total-(total+noise)),1.)
        np.testing.assert_allclose(np.cov(np.repeat(clean,4,axis=0),rowvar=False,bias=True),geometry)


if __name__ == '__main__':
    unittest.main()
