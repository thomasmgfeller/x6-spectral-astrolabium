"""Controls for changed mathematics, leakage boundary, and shared field noise."""
import copy
import json
import unittest
import numpy as np
from mb_common import contract
from mb_model import basis, corrected, prepare, ARMS
from mb_fields import values
from feasibility import design, TARGET
from variance_weights import minimum_variance


def fixture():
    x=np.random.default_rng(713).normal(size=(24,3))
    a=minimum_variance(design(x))['weights']
    return dict(status='COMPLETE',original_features=x.tolist(),projection=dict(features=x.tolist()),
                weights=[a,a],scale=.3)


def model(b):
    return dict(use_metadata=True,center=b['metadata'].tolist(),spread=[1.,1.,1.],
                minimum=(b['metadata']-2).tolist(),maximum=(b['metadata']+2).tolist(),
                beta=[[1.,.1,-.1,.2],[-.5,.2,.1,.1]])


class Controls(unittest.TestCase):
    def test_constants_linearity_and_quadratic_moments(self):
        intr=fixture(); b=basis(intr,0); a,diag=corrected(b,model(b))
        self.assertTrue(diag['clipped'])
        np.testing.assert_allclose(design(intr['original_features'])@a,TARGET,atol=1e-9)
        full=np.r_[-a.sum(),a]/intr['scale']**2
        self.assertAlmostEqual(float(full@np.ones(len(full))),0.,places=11)
        f=np.random.default_rng(7).normal(size=len(full)); g=f**2
        self.assertAlmostEqual(float(full@(2*f-3*g)),float(2*(full@f)-3*(full@g)),places=10)
        self.assertAlmostEqual(diag['noise_ratio'],1.25,places=9)

    def test_permutation_equivariance(self):
        intr=fixture(); b=basis(intr,0); a,_=corrected(b,model(b))
        perm=np.random.default_rng(77).permutation(len(a)); other=copy.deepcopy(intr)
        other['original_features']=np.array(intr['original_features'])[perm].tolist()
        other['weights'][0]=np.array(intr['weights'][0])[perm].tolist()
        aa,_=corrected(basis(other,0),model(b))
        np.testing.assert_allclose(aa,a[perm],atol=1e-9)

    def test_ood_fallback_and_no_field_input(self):
        intr=fixture(); b=basis(intr,0); m=model(b)
        m['maximum']=(b['metadata']-1).tolist()
        a,diag=corrected(b,m)
        self.assertTrue(diag['ood']); np.testing.assert_array_equal(a,b['a'])
        models={n:model(b) for n in ['metadata','projected_metadata','constant_ablation','projected_constant_ablation']}
        p=prepare(intr,models)
        self.assertEqual(p,json.loads(json.dumps(p,allow_nan=False)))
        altered=copy.deepcopy(intr); altered['hidden_truth']=1e20; altered['field']=[999]*24
        self.assertEqual(p,prepare(altered,models))

    def test_shared_root_noise_and_cross_terms(self):
        intr=fixture(); b=basis(intr,0)
        models={n:model(b) for n in ['metadata','projected_metadata','constant_ablation','projected_constant_ablation']}
        p=prepare(intr,models); a=np.array(p['weights']); n=np.array(p['conditional_field_covariance'])
        want=contract()['field_noise_sigma']**2*(a@a.T+np.outer(a.sum(axis=1),a.sum(axis=1)))/intr['scale']**4
        np.testing.assert_allclose(n,want,rtol=1e-12,atol=1e-15)
        self.assertGreater(np.linalg.norm(n-np.diag(np.diag(n))),0)
        self.assertGreater(np.linalg.norm(n-contract()['field_noise_sigma']**2*a@a.T/intr['scale']**4),1e-12)

    def test_field_truth_against_second_difference(self):
        # Includes transfer specifications symbolically, but no transfer cloud responses.
        h=1e-3
        for spec in contract()['training_fields']+contract()['transfer_fields']:
            points=np.vstack((np.zeros(3),h*np.eye(3),-h*np.eye(3)))
            f,truth=values(points,spec)
            second=(f[1:4]+f[4:7]-2*f[0])/h**2
            self.assertAlmostEqual(float(np.array([-1.,1.,1.])@second),truth,places=6)


if __name__=='__main__':
    unittest.main()
