"""Hand-solvable witnesses, genuine obstructions and mutation rejection."""
import json
import numpy as np
from feas_common import config
from feasibility import design,solve,checked_feasible,checked_infeasible,TARGET

def check():
    contract,_=config();r=.6;p=1/(2*r*r);q=p+.25
    z=np.array([[t,x,y] for t in [-1.,1.] for x,y in [(r,0),(-r,0),(0,r),(0,-r)]]+[[-2.,0.,0.],[2.,0.,0.]])
    a0=np.array([p]*8+[-q]*2);mask=np.array([False]*8+[True]*2);d=design(z)
    np.testing.assert_allclose(d@a0,TARGET,atol=1e-13)
    mass=8*p+2*q
    for policy in contract['policies']:
        row=solve(d,a0,mask,policy,contract);assert row['status']=='FEASIBLE'
        np.testing.assert_allclose(row['minimum_mass'],mass,atol=1e-10)
        perm=np.random.default_rng(612).permutation(len(z))
        moved=solve(d[:,perm],a0[perm],mask[perm],policy,contract)
        np.testing.assert_allclose(moved['minimum_mass'],mass,atol=1e-10)
        scaled=design((7*z)/7);np.testing.assert_allclose(scaled,d,atol=1e-14)
    row=solve(d,a0,mask,'fixed_time',contract)
    for x,y in [(np.zeros(len(row['primal'])),row['dual']),(row['primal'],np.ones(9)*10)]:
        try:checked_feasible(d,a0,mask,'fixed_time',x,y,contract)
        except AssertionError:pass
        else:raise AssertionError('invalid feasible witness accepted')
    line=z.copy();line[:,2]=0.;line_d=design(line)
    for policy in contract['policies']:
        bad=solve(line_d,a0,mask,policy,contract);assert bad['status']=='INFEASIBLE'
        assert bad['certificate']['separation_margin']>0
    try:checked_infeasible(line_d,a0,mask,'fixed_time',np.zeros(9),contract)
    except AssertionError:pass
    else:raise AssertionError('invalid separating witness accepted')
    # All-future timelike support: positive weights cannot give a negative tt
    # moment. A full-rank signed system can; this is a sign, not rank obstruction.
    rng=np.random.default_rng(2026101909);future=rng.uniform(-.25,.25,(20,3));future[:,0]=rng.uniform(1.,3.,20)
    fd=design(future);assert np.linalg.matrix_rank(fd)==9
    assert solve(fd,np.ones(20),np.zeros(20,bool),'fixed_time',contract)['status']=='INFEASIBLE'
    assert solve(fd,np.ones(20),np.zeros(20,bool),'unrestricted',contract)['status']=='FEASIBLE'
    return dict(status='PASS_SOFTWARE_CONTROLS',symmetric_exact_mass=mass,
                policy_fixtures=3,one_direction_infeasibility_policies=3,
                sign_obstruction_resolved_by_signed_weights=True,mutation_rejections=3,
                permutation_and_uniform_scaling=True)

def cloud_controls(supports,contract,seed):
    rng=np.random.default_rng(seed+2901)
    for support in supports.values():
        if support['status']!='ok':continue
        d=np.array(support['design']);a0=np.array(support['baseline_coefficients']);mask=np.array(support['temporal_mask'])
        perm=rng.permutation(len(a0));dd=d[:,perm].copy()
        # Transported time reversal: t, tx and ty rows change sign; targets zero.
        dd[[0,6,7]]*=-1
        for policy,original in support['policies'].items():
            moved=solve(dd,a0[perm],mask[perm],policy,contract)
            assert original['status']==moved['status']
            if moved['status']=='FEASIBLE':
                np.testing.assert_allclose(moved['minimum_mass'],original['minimum_mass'],atol=1e-8,rtol=1e-7)
    return dict(status='PASS',permutation_and_transported_time_reversal=True)

if __name__=='__main__':print(json.dumps(check(),indent=2))
