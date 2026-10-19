"""Independent geometric fixtures and transported-poset software controls."""
import ast
import copy
import inspect
import json
import math
import numpy as np
from axis_common import HERE,core,config,compare,weighting
from volume_controls import remap,check as weight_controls
import selection
from assembly import rebuild

def check():
    # Off-axis root in the endpoint rest frame: dt must still be displacement
    # from the root, not absolute time from either endpoint.
    z=np.array([[-3.,0.,0.],[3.,0.,0.],[.2,.4,-.1],[1.3,.6,.2],[-1.1,.1,.15]])
    def proper(v):return math.sqrt(v[0]**2-v[1]**2-v[2]**2)
    eta=np.diag([-1.,1.,1.]);beta=.4;gamma=1/math.sqrt(1-beta**2)
    boost=np.array([[gamma,-gamma*beta,0.],[-gamma*beta,gamma,0.],[0.,0.,1.]])
    np.testing.assert_allclose(boost.T@eta@boost,eta,atol=1e-14)
    geometric=[]
    for transform,offset in [(np.eye(3),np.zeros(3)),(boost,np.array([.7,-.3,1.2]))]:
        q=z@transform.T+offset
        for x,sign in [(3,1),(4,-1)]:
            vals=[proper(q[v]-q[u]) for u,v in [(0,1),(0,2),(2,1),(0,x),(x,1),(2,x)]]
            a=selection.score(*vals,sign);dt=z[x,0]-z[2,0]
            expected=((z[x,1:]-z[2,1:])**2).sum()/proper(z[x]-z[2])**2
            np.testing.assert_allclose([a['dt'],a['h']],[dt,expected],atol=1e-13)
            rev=selection.score(vals[0],vals[2],vals[1],vals[4],vals[3],vals[5],-sign)
            np.testing.assert_allclose([rev['dt'],rev['h']],[-dt,expected],atol=1e-13)
            geometric.append(a['h'])
    negative=selection.score(2.,1.,1.,1.5,.5,1.,1)
    assert negative['status']=='ok' and negative['h']==-.75 and negative['score']==.75
    assert selection.score(2.,1.,1.,1.5,.5,1.,-1)['status']=='wrong_time_sign'
    assert selection.score(0.,1.,1.,1.5,.5,1.,1)['status']=='invalid_time'
    # Hand-counted total order, exact linear time gives tied zero-axis scores.
    g=core.Poset(np.triu(np.ones((11,11),bool),1),np.arange(11)[::-1].astype(float))
    s=dict(status='ok',root=5,temporal=[0,10],sides=[dict(shell=[7,8]),dict(shell=[2,3])])
    chosen=selection.choose_with_times(g,s,lambda u,v,n:float(v-u))
    assert chosen['common_counts']==[9,4,4]
    assert [q['reference'] for q in chosen['sides']]==[8,3]
    assert chosen['sides'][0]['candidates'][0]['counts']==[7,1,2]
    broken=copy.deepcopy(s);broken['sides'][0]['shell']=[6]
    assert selection.select(g,broken,2048)['status']=='no_axis_reference'
    broken=copy.deepcopy(s);broken['temporal']=[4,10]
    assert selection.select(g,broken,2048)['status']=='zero_common_interval'
    tree=ast.parse((HERE/'selection.py').read_text())
    assert [n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.Import)]==['math']
    assert not any(isinstance(n,ast.ImportFrom) for n in ast.walk(tree))
    assert list(inspect.signature(selection.select).parameters)==['g','s','rho']
    for rho in [0.,-1.,float('inf')]:
        try:selection.select(g,s,rho)
        except ValueError:pass
        else:raise AssertionError('invalid density accepted')
    return dict(status='PASS_SOFTWARE_CONTROLS',off_axis_geometry_cases=len(geometric),
                lorentz_translation_and_reversal=True,hand_counted_intervals=True,
                negative_h_unclipped=True,sign_and_zero_rejection=True,mark_ties=True,
                coordinate_blind_interface=True,inherited_weights=weight_controls())

def cloud_controls(g,base,rho,cfg,seed):
    a=selection.select(g,base,rho)
    if 'sides' not in base:return dict(status='PASS',short_chain=True)
    # Exact wrapper parity includes failed population cases.
    refs=dict(status='ok',sides=[dict(reference=s['reference']) for s in base['sides']])
    compare(base,rebuild(g,base,refs,rho,cfg))
    scale=selection.select(g,base,8*rho)
    assert a['status']==scale['status']
    if a['status']=='ok':
        assert [s['reference'] for s in a['sides']]==[s['reference'] for s in scale['sides']]
        for sa,sb in zip(a['sides'],scale['sides']):
            for x,y in zip(sa['candidates'],sb['candidates']):
                assert x['status']==y['status']
                if 'h' in x:np.testing.assert_allclose(x['h'],y['h'],atol=1e-13,rtol=1e-13)
    c=cfg['coefficient_C'];original=weighting.reweight(g,rebuild(g,base,a,rho,cfg),rho,c)
    perm=np.random.default_rng(seed+1901).permutation(g.size);inv=np.argsort(perm)
    for reverse in [False,True]:
        b=remap(base,inv)
        if reverse:
            b['temporal'].reverse();b['sides'].reverse();b['chain'].reverse()
        h=core.Poset((g.r.T if reverse else g.r)[np.ix_(perm,perm)],g.marks[perm])
        chosen=selection.select(h,b,rho)
        assert a['status']==chosen['status']
        if a['status']=='ok':
            aa=a['sides'][::-1] if reverse else a['sides']
            assert [s['reference'] for s in aa]==[int(perm[s['reference']]) for s in chosen['sides']]
        weighted=weighting.reweight(h,rebuild(h,b,chosen,rho,cfg),rho,c)
        assert original['status']==weighted['status']
        if original['status']=='ok':
            assert original['support']==[int(perm[x]) for x in weighted['support']]
            np.testing.assert_allclose(original['weights'],weighted['weights'],atol=1e-10,rtol=1e-12)
    return dict(status='PASS',baseline_reassembly=True,density_scaling=True,
                transported_root_relabel_and_reversal=True)

if __name__=='__main__':print(json.dumps(check(),indent=2))
