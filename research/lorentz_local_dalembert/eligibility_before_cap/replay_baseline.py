"""Explicit numerical-field replay for the archived baseline eigensolver.
SPDX-License-Identifier: Apache-2.0
"""
import json,math
from eb_common import encode
NUMERIC={
 'certificate/transform/#/#','certificate/features/#/#',
 'certificate/eigenvalues/#','certificate/condition',
 'funnel/#/frames/minimum_lorentz_condition',
 'certificate/guard/halves/#/gram_error','certificate/guard/halves/#/feature_error',
 'design/condition','design/singular_values/#','point_feature_errors/#',
}

def compare_baseline(actual,expected,root=None):
    actual=json.loads(encode(actual));expected=json.loads(encode(expected));changed={}
    def walk(a,b,path):
        key='/'.join(path)
        assert type(a) is type(b),(key,'type changed')
        if isinstance(b,dict):
            assert a.keys()==b.keys(),(key,'keys changed')
            for k in b:walk(a[k],b[k],path+[k])
        elif isinstance(b,list):
            assert len(a)==len(b),(key,'length changed')
            for x,y in zip(a,b):walk(x,y,path+['#'])
        elif key in NUMERIC:
            assert type(a) is float and math.isfinite(a) and math.isfinite(b),(key,a,b)
            assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12),(key,a,b)
            if a!=b:changed[key]=max(changed.get(key,0),abs(a-b))
        else:assert a==b,(key,a,b)
    walk(actual,expected,[] if root is None else [root])
    if changed:print('Baseline numeric replay maximum differences:',json.dumps(changed,sort_keys=True))
    return changed

def controls():
    import copy
    base=dict(root=17,scale=0.5,certificate=dict(interval_counts=[12],guard=dict(passed=True)),
              design=dict(rank=9,passed=True,condition=30.0,singular_values=[2.0]))
    good=copy.deepcopy(base);good['design']['condition']+=1e-13
    compare_baseline(good,base)
    for path,value in [(('root',),18),(('scale',),.5+1e-14),
                       (('certificate','interval_counts'),[13]),(('certificate','guard','passed'),False),
                       (('design','rank'),8),(('design','passed'),False),
                       (('design','condition'),30.+1e-6),(('design','condition'),float('nan')),
                       (('design','singular_values'),[2.,3.])]:
        bad=copy.deepcopy(base);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:compare_baseline(bad,base)
        except (AssertionError,ValueError):continue
        raise AssertionError(('invalid baseline accepted',path))
