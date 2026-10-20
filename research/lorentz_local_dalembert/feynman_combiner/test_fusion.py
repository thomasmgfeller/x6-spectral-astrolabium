import json
import unittest
from pathlib import Path
import numpy as np
from fusion import combine,blue_weights,update,causal_check

class Controls(unittest.TestCase):
    def test_duplicate_has_no_information_gain(self):
        z,r,_=combine([[2.],[2.]],np.ones((2,2)),[.5,.5])
        np.testing.assert_allclose(z,[2.]); np.testing.assert_allclose(r,[[1.]])
    def test_correlated_update(self):
        a=update([0.],[[1.]],[2.],[[1.]],[[1.]],[[.5]])
        np.testing.assert_allclose(a['gain'],[[.5]])
        np.testing.assert_allclose(a['posterior_covariance'],[[.25]])
    def test_bad_covariance(self):
        with self.assertRaises(ValueError): combine([[0.],[0.]],[[1,2],[2,1]],[.5,.5])
    def test_causal_violation_visible(self):
        r=np.array([[0,1],[0,0]],bool)
        self.assertTrue(causal_check([[0,0,0],[1,0,0]],r)['passed'])
        self.assertFalse(causal_check([[0,0,0],[1,2,0]],r)['passed'])
    def test_affine_unbiasedness(self):
        r=np.array([[1,.5],[.5,4]])
        w=blue_weights(r); self.assertAlmostEqual(w.sum(),1.)
        self.assertLess(w@r@w,1.)

def benchmark():
    # Protocol: fixed shared variance .9, private .1; 2000 training draws,
    # 20000 independent test draws. No tuning from the test outcomes.
    rng=np.random.default_rng(2026102001)
    train=np.sqrt(.9)*rng.normal(size=(2000,1))+np.sqrt(.1)*rng.normal(size=(2000,3))
    estimate=np.cov(train,rowvar=False); w=blue_weights(estimate)
    rng=np.random.default_rng(2026102002)
    obs=np.sqrt(.9)*rng.normal(size=(20000,1))+np.sqrt(.1)*rng.normal(size=(20000,3))
    pred=rng.normal(size=20000) # true state zero, independent prediction error variance 1
    outputs={}
    for name,weights,reported in [('single',[1,0,0],1.),('naive_independence',[1/3]*3,1/3),
                                  ('joint_covariance',w,float(w@estimate@w)),('conservative_equal',[1/3]*3,1.)]:
        z=obs@np.asarray(weights); gain=1/(1+reported); p=reported/(1+reported)
        post=pred+gain*(z-pred)
        outputs[name]=dict(measurement_variance_reported=reported,measurement_mse=float(np.mean(z*z)),
            posterior_rmse=float(np.sqrt(np.mean(post*post))),posterior_variance_reported=p,
            coverage_95=float(np.mean(np.abs(post)<=1.95996398454*np.sqrt(p))),
            mean_nees=float(np.mean(post*post)/p),mean_nis=float(np.mean((z-pred)**2)/(1+reported)))
    result=dict(scope='Scalar one-step synthetic control; not causal-reconstruction or sequential-filter validation',
                train=2000,test=20000,weights=w.tolist(),results=outputs)
    (Path(__file__).parent/'synthetic_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    if not unittest.TextTestRunner().run(suite).wasSuccessful(): raise SystemExit(1)
    benchmark()
