"""Independent algebra, constrained-optimum and conditional transport controls."""
import ast
import copy
import inspect
import numpy as np
import intrinsic
from im_common import core,config

def check():
    c,_=config();land=np.array([[-10.,0,0],[-7.,2,0],[-4.,0,1.5]])
    points=np.vstack((np.zeros(3),land,[[1.,.6,0],[-1.,0,.6],[2.,0,0],[-2.,0,0]]))
    q=lambda a,b:-float((points[a]-points[b])@intrinsic.ETA@(points[a]-points[b]))
    h,v=intrinsic.gram_and_vectors(q,[1,2,3],0,[4,5,6,7],.8)
    np.testing.assert_allclose(h,land@intrinsic.ETA@land.T/.8**2,atol=1e-12)
    normalized=intrinsic.normalize(h,float('inf'));assert normalized is not None
    t,_,condition=normalized;z=(t@v).T
    np.testing.assert_allclose(t@h@t.T,intrinsic.ETA,atol=1e-12)
    np.testing.assert_allclose(z@intrinsic.ETA@z.T,points[4:]@intrinsic.ETA@points[4:].T/.8**2,atol=1e-11)
    h2,v2=intrinsic.gram_and_vectors(lambda a,b:9*q(a,b),[1,2,3],0,[4,5,6,7],2.4)
    np.testing.assert_allclose(h2,h,atol=1e-12);np.testing.assert_allclose(v2,v,atol=1e-12)
    assert intrinsic.normalize(np.diag([-1.,-1.,1.]),1000) is None
    assert intrinsic.normalize(np.diag([-1.,0.,1.]),1000) is None
    for cap,expected in [(10.,1.5),(1.,1.)]:
        result=intrinsic.quadratic([[1.]],[2.],[1.],1.,cap,c)
        assert result['status']=='VERIFIED';np.testing.assert_allclose(result['coefficients'],[expected],atol=1e-9)
    rejected=0
    for a,cap in [([-1.],10.),([2.],1.),([.5],10.)]:
        try:intrinsic.qp_certificate([[1.]],[2.],[1.],1.,cap,a,c)
        except AssertionError:rejected+=1
    assert rejected==3
    good=intrinsic.noise_guard(intrinsic.ETA,np.eye(3),np.eye(3),[(intrinsic.ETA,np.eye(3))]*2,[32]*4,[[16]*4]*2,1.,c)
    bad=intrinsic.noise_guard(intrinsic.ETA,np.eye(3),np.eye(3),[(3*intrinsic.ETA,np.eye(3))]*2,[32]*4,[[16]*4]*2,1.,c)
    assert good['passed'] and not bad['passed'] and 'gram_stability' in bad['reasons']
    source=inspect.getsource(intrinsic);tree=ast.parse(source)
    imports=[n.module if isinstance(n,ast.ImportFrom) else a.name for n in ast.walk(tree)
             if isinstance(n,(ast.Import,ast.ImportFrom)) for a in (n.names if isinstance(n,ast.Import) else [None])]
    assert set(imports)<={'itertools','math','numpy'}
    assert list(inspect.signature(intrinsic.infer).parameters)==['g','s','rho','boundary','colours','c']
    return dict(status='PASS_SOFTWARE_CONTROLS',exact_polarization=True,uniform_scaling=True,
                signature_rejections=2,analytic_quadratic_optima=2,mutation_rejections=rejected,
                inconsistent_half_guard_rejected=True,coordinate_blind_interface=True)

def transport(g,s,rho,boundary,colours,c,expected,seed):
    if s['status']!='ok':return dict(status='PASS',applicable=False)
    permutation=np.random.default_rng(seed^0x15B29).permutation(g.size);inverse=np.argsort(permutation)
    renamed=copy.deepcopy(s)
    for key in ['root']:renamed[key]=int(inverse[s[key]])
    for key in ['support','temporal']:renamed[key]=[int(inverse[x]) for x in s[key]]
    gp=core.Poset(g.r[np.ix_(permutation,permutation)],g.marks[permutation])
    actual=intrinsic.infer(gp,renamed,rho,[int(inverse[x]) for x in boundary],colours[permutation],c)
    variants=[(actual,lambda a:int(permutation[a]),False)]
    del gp
    gr=core.Poset(g.r.T,g.marks)
    reverse=intrinsic.infer(gr,s,rho,boundary,colours,c)
    variants.append((reverse,lambda a:a,True))
    for row,unmap,reversed_time in variants:
        a=expected['frame'];b=row['frame'];assert a['status']==b['status']
        assert a.get('eligible_triples')==b.get('eligible_triples')
        if a['status']=='ok':
            assert a['landmarks']==[unmap(x) for x in b['landmarks']]
            assert (a['side']!=b['side'])==reversed_time
            for key in ['gram','vectors','feature_gram','lorentz_feature_gram','eigenvalues','condition']:
                np.testing.assert_allclose(a[key],b[key],**c['calibration_replay_tolerance'])
            assert a['guard']['checks']==b['guard']['checks']
        for name in ['intrinsic_raw','intrinsic_guarded']:
            assert expected[name]['adopted']==row[name]['adopted']
            assert expected[name]['fallback_reasons']==row[name]['fallback_reasons']
            np.testing.assert_allclose(expected[name]['weights'],row[name]['weights'],**c['calibration_replay_tolerance'])
    return dict(status='PASS',applicable=True,mark_preserving_relabel=True,transported_time_reversal=True)
