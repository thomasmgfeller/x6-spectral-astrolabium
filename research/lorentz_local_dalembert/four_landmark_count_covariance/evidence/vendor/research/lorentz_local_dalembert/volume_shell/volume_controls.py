"""Independent hand-counted fixtures, invariances and interface boundary."""
import ast
import copy
import inspect
import json
import math
import numpy as np
from volume_common import HERE,core,config
import weighting


def remap(s,inv):
    s=copy.deepcopy(s);s['root']=int(inv[s['root']])
    for k in ['temporal','support','chain']:
        if k in s:s[k]=[int(inv[b]) for b in s[k]]
    for side in s.get('sides',[]):
        for k in ['selected','shell']:
            if k in side:side[k]=[int(inv[b]) for b in side[k]]
        if 'reference' in side:side['reference']=int(inv[side['reference']])
    return s


def relabel_check(g,s,rho,c,seed):
    perm=np.random.default_rng(seed+901).permutation(g.size);inv=np.argsort(perm)
    h=core.Poset(g.r[np.ix_(perm,perm)],g.marks[perm]);ss=remap(s,inv)
    for both in [False,True]:
        a=weighting.reweight(g,s,rho,c,both);b=weighting.reweight(h,ss,rho,c,both)
        assert a['status']==b['status']
        if a['status']=='ok':
            assert a['support']==[int(perm[x]) for x in b['support']]
            np.testing.assert_allclose(a['weights'],b['weights'],atol=1e-12,rtol=1e-12)
        assert [(q['point'],q['interior_count'],q['time']) for q in a['interval_times']]==[(int(perm[q['point']]),q['interior_count'],q['time']) for q in b['interval_times']]
    return True


def check():
    _,cfg=config();c=cfg['coefficient_C'];rho=12/math.pi
    r=np.triu(np.ones((9,9),bool),1);marks=np.arange(9,dtype=float)
    s=dict(status='ok',root=4,temporal=[0,8],tau_n=3.,tau_m=2.,
           sides=[dict(selected=[1,2]),dict(selected=[6,7])])
    s=weighting.assemble(s,marks,c,{1:2.,2:2.,6:2.,7:2.})
    g=core.Poset(r,marks)
    for both in [False,True]:
        a=weighting.reweight(g,s,rho,c,both)
        expected={1:c/(2*2**(2/3)),2:c/2,6:c/2,7:c/(2*2**(2/3)),0:-(c+3)/(3**(2/3) if both else 9),8:-(c+3)/(3**(2/3) if both else 9)}
        for b,w in zip(a['support'],a['weights']):np.testing.assert_allclose(w,expected[b],rtol=1e-13)
        reverse=weighting.reweight(core.Poset(r.T,marks),s,rho,c,both)
        np.testing.assert_allclose(reverse['weights'],a['weights'],atol=1e-13)
    a=weighting.reweight(g,s,rho,c,True);b=weighting.reweight(g,s,8*rho,c,True)
    np.testing.assert_allclose(b['weights'],4*np.array(a['weights']),rtol=1e-13)
    broken=copy.deepcopy(s);broken['sides'][0]['selected']=[2,3]
    assert weighting.reweight(g,broken,rho,c)['status']=='zero_interval'
    assert relabel_check(g,s,rho,c,2026110001)
    # Known times can recover original weights, including collisions between
    # contributions: assembly adds rather than silently replacing weights.
    collision=copy.deepcopy(s);collision['sides'][0]['selected']=[0,2]
    a=weighting.assemble(collision,marks,c,{0:2.,2:2.,6:2.,7:2.})
    np.testing.assert_allclose(a['weights'][a['support'].index(0)],-(c+3)/9+c/8)
    assert core.apply(a,np.ones(9))==0
    tree=ast.parse((HERE/'weighting.py').read_text())
    imports=[node.names[0].name for node in ast.walk(tree) if isinstance(node,ast.Import)]
    assert set(imports)=={'copy','math'} and not any(isinstance(n,ast.ImportFrom) for n in ast.walk(tree))
    assert list(inspect.signature(weighting.reweight).parameters)==['g','stencil','rho','c','both']
    for bad in [0.,-1.,float('inf')]:
        try:weighting.reweight(g,s,bad,c)
        except ValueError:pass
        else:raise AssertionError('invalid density accepted')
    return dict(status='PASS_SOFTWARE_CONTROLS',hand_counted_arms=2,time_reversal_arms=2,
                density_scaling=True,zero_interval_rejected=True,relabel_arms=2,
                repeated_support_accumulates=True,coordinate_blind_interface=True,invalid_densities_rejected=3)

if __name__=='__main__':print(json.dumps(check(),indent=2))
