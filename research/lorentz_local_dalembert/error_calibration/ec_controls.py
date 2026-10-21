"""SPDX-License-Identifier: Apache-2.0
Exact covariance algebra, finite-difference field oracle, relation and rank controls.
"""
import json
import numpy as np
from ec_common import cfg
from ec_measure import field_values,geometry,noise_bank,noise_tests
from ec_analyze import rejects


def main():
    # Shared root contributes an outer product, not four independent root reads.
    a=np.array([[1.,2.,3.],[2.,-1.,4.],[0.,1.,2.],[3.,2.,-1.]])
    b=np.column_stack((-a.sum(axis=1),a))
    n=cfg()['field_noise_sigma']**2*(b@b.T)
    np.testing.assert_allclose(n,cfg()['field_noise_sigma']**2*(a@a.T+np.outer(a.sum(axis=1),a.sum(axis=1))),atol=1e-20)
    assert np.max(np.abs(n-cfg()['field_noise_sigma']**2*(a@a.T)))>1e-5
    np.testing.assert_allclose(b.sum(axis=1),0,atol=0)
    for spec in cfg()['fields']:
        h=1e-4;basis=np.eye(3)*h
        values,_=field_values(np.vstack((basis,-basis)),spec)
        second=(values[:3]+values[3:])/h**2
        _,truth=field_values(np.zeros((1,3)),spec)
        np.testing.assert_allclose(-second[0]+second[1]+second[2],truth,atol=1e-7)
    points=np.array([[0,0,0],[1,0,0],[1,.2,0]],float)
    order=np.array([[0,1,1],[0,0,0],[0,0,0]])
    good=geometry(points,points,order)
    assert good['gram_relative_error']==good['proper_time_rmse']==0
    bad=points.copy();bad[2]=[.1,.3,0]
    assert geometry(points,bad,order)['missing_relations']>0
    bank=noise_bank(b,12345,0)
    alpha=cfg()['noise_test_family_alpha']/cfg()['noise_test_maximum_count']
    assert not rejects(noise_tests(bank,n),alpha)
    assert rejects(noise_tests(bank,cfg()['field_noise_sigma']**2*(a@a.T)),alpha)
    assert rejects(noise_tests(bank,np.diag(np.diag(n))),alpha)
    # Averaging changes noise variance but cannot remove a fixed geometry bias.
    e=np.array([2.,-1.]);noises=np.array([[1.,2.],[-1.,-2.]])
    np.testing.assert_array_equal((e+noises).mean(axis=0),e)
    print(json.dumps(dict(status='PASS',groups=['shared_root_and_covariance','new_field_derivatives',
        'proper_time_and_relations','defective_noise_models','bias_survives_averaging'])))


if __name__=='__main__':main()
