"""Concrete failure witnesses and independent controls for search ordering."""
import ast
import json
import math
import numpy as np
from common import HERE, core, config
import estimator
import tests as legacy_tests


def compare(expected, actual, path='root'):
    if isinstance(expected,dict):
        assert isinstance(actual,dict) and expected.keys()==actual.keys(),path
        for key in expected:
            if key in ['seconds','peak_mib','method_seconds','coordinates_sha256']: continue
            compare(expected[key],actual[key],path+'.'+key)
    elif isinstance(expected,list):
        assert len(expected)==len(actual),path
        for i,(a,b) in enumerate(zip(expected,actual)): compare(a,b,path+f'[{i}]')
    elif isinstance(expected,float):
        assert np.isfinite(expected) and np.isfinite(actual),path
        assert abs(expected-actual)<=1e-10+1e-9*abs(expected),path
    else:
        assert expected==actual,path


def witness():
    # 65 unbalanced anchors rank before a useful 66th. Eight shared events,
    # eight A-only events and one B-only event make a genuine transitive poset.
    r=np.zeros((85,85),bool); a,b=83,84
    shared=list(range(66,74)); aonly=list(range(74,82)); bonly=82
    r[:65,shared+aonly+[bonly]]=True
    r[65,shared+[74,bonly]]=True
    r[shared+[bonly],b]=True; r[shared+aonly,a]=True
    for k in range(len(r)): r |= r[:,k,None]&r[None,k,:]
    return r,np.arange(len(r),dtype=float)/len(r),a,b


def check():
    inherited=legacy_tests.check(); _,cfg=config(); r,marks,a,b=witness()
    results=[]
    rng=np.random.default_rng(2026102266)
    for reverse in [False,True]:
        rel=r.T.copy() if reverse else r
        for permute in [False,True]:
            perm=rng.permutation(len(r)) if permute else np.arange(len(r))
            inv=np.argsort(perm); g=core.Poset(rel[np.ix_(perm,perm)],marks[perm])
            old,oi=core.spatial_distance(g,int(inv[a]),int(inv[b]),32768,cfg,reverse)
            new,ni=estimator.spatial_distance(g,int(inv[a]),int(inv[b]),32768,cfg,reverse)
            assert old is None and new is not None
            assert ni['first_valid_rank']==66 and ni['anchors']==1
            assert ni['eligible_beyond_original_cap']==1 and ni['searched']==66
            # Exhausting the original implementation independently agrees.
            exhaustive,_=core.spatial_distance(g,int(inv[a]),int(inv[b]),32768,{**cfg,'overlap_max_anchors':10000},reverse)
            np.testing.assert_allclose(new,exhaustive,rtol=1e-13)
            expected=4*cfg['alpha2']*32768**(-1/3)*core.invert_overlap(8/9)
            np.testing.assert_allclose(new,expected,rtol=1e-13)
            assert estimator.spatial_distance(g,int(inv[a]),int(inv[a]),32768,cfg,reverse)[0]==0
            results.append(new)
    np.testing.assert_allclose(results,results[0],rtol=1e-13)
    # A complete shared interval gives overlap one and remains unresolved.
    one=np.zeros((12,12),bool); one[0,1:10]=True; one[1:10,10:12]=True; one[0,10:12]=True
    zero=one.copy(); zero[1:10,10:12]=False; zero[1:5,10]=True; zero[5:9,11]=True
    for rel in [one,zero]:
        g=core.Poset(rel,np.arange(12,dtype=float))
        assert estimator.spatial_distance(g,10,11,32768,{**cfg,'overlap_min_interval':1})[0] is None
    # Legacy wrapper parity on a finite coordinate-free random poset, not a target cloud.
    n=70; rel=np.triu(rng.random((n,n))<.15,1)
    rel[0,1:]=True; rel[:-1,-1]=True
    for k in range(n): rel|=rel[:,k,None]&rel[None,k,:]
    g=core.Poset(rel,rng.random(n))
    old=core.neighborhood(g,2048,0,n-1,cfg)
    wrapped=estimator.neighborhood(g,2048,0,n-1,cfg,distance_function=core.spatial_distance)
    compare(old,wrapped)
    for expected,actual in [({'v':1.},{'v':1.0001}),({'hash':'a'},{'hash':'b'}),({'missing':None},{'missing':0})]:
        try: compare(expected,actual)
        except AssertionError: pass
        else: raise AssertionError('mutation guard failed')
    tree=ast.parse((HERE/'estimator.py').read_text())
    assert not any(isinstance(node,(ast.Import,ast.ImportFrom)) and any(word in ast.unparse(node) for word in ['experiment','run_audit']) for node in ast.walk(tree))
    return dict(status='PASS_SOFTWARE_CONTROLS',cap_order_witness_variants=4,
                legacy_wrapper_parity=True,zero_one_unresolved=True,mutation_rejections=3,
                inherited=inherited,curvature_qualification=False)


if __name__=='__main__': print(json.dumps(check(),indent=2))
