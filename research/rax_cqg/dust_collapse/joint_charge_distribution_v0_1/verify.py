"""Replay the certificates, normalized laws, vacuum and independent integration checks."""
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from model import BASE,laws,combined_laws
import weights,chain,exact_norm,direct,scalar_check,sensitivity,evaluate

def read(name):return json.loads((BASE/name).read_text())
def close(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:close(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):close(x,y)
    elif isinstance(a,(int,float)) and not isinstance(a,bool):assert np.isclose(a,b,atol=2e-9,rtol=2e-8),(a,b)
    else:assert a==b

def check():
    src=read('sources.json')
    for k,rec in src['files'].items():
        val=(BASE/k).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(val)).encode()+b'\0'+val).hexdigest()==rec['sha']
    assert weights.run()==read('weights.json')
    assert chain.run(read('chain.json'))==read('chain.json')
    exact=exact_norm.run();assert exact==read('exact_norm_final.json')
    assert set(exact['witnesses'])=={'++','--'}
    states=np.load(BASE/'scalars.npz')
    import sympy as sp
    from model import BETA
    max_shape_error=0.
    for code,vals in exact['by_type'].items():
        ref=np.array([complex(sp.sympify(z)) for z in vals])*BETA
        i=np.searchsorted(states['keys'],int(code))
        v=states['precision'][i][np.triu_indices(3)]
        rel=np.max(abs(v-ref))/max(abs(ref))
        max_shape_error=max(rel,max_shape_error)
    assert max_shape_error<1e-4
    actions=scalar_check.run()
    joint=evaluate.run(True); close(joint,read('joint.json'))
    one=evaluate.run();close(one,read('results.json'))
    sens=sensitivity.run();close(sens,read('sensitivity.json'))
    alternate=direct.run();close(alternate,read('direct.json'))
    maxbins=maxsign=0.
    for k,v in alternate.items():
        _,mass,law=k.split('/')
        which=f'{float(mass):g}/0.125'
        if law=='chain_reverse':
            ref=sens['alternative_same_N13']['rows'][which]
            bins,sign=ref['bins'],ref['sign_positive']
        else:
            ref=joint['rows'][which][law];bins,sign=ref['bin_probabilities'],ref['positive_sign_record']
        maxbins=max(maxbins,max(abs(np.subtract(v['fine_bins'],bins))))
        maxsign=max(maxsign,abs(v['positive_sign_record']-sign))
    assert maxbins<.001 and maxsign<.001
    alltypes=np.load(BASE/'all_raw.npz')
    by=read('inputs/sync/census.json')['by_type']
    checked=0
    for j,k in enumerate(alltypes['keys']):
        pat=by[str(k)].get('signs')
        if pat in ('++','--'):
            wrong=alltypes['amp'][:,:,:,:,j,:3 if pat=='++' else 6]
            if pat=='--':wrong=wrong[...,3:]
            assert np.max(abs(wrong))<1e-16
            checked+=1
    assert checked==120
    return {'source_git_blobs':len(src['files']),'positive_definite_reference_shapes':exact['distinct_exact_scalar_shapes'],
            'all_type_sign_controls':checked,'max_relative_scalar_shape_error':max_shape_error,
            'symbolic_scalar_checks':actions,'independent_bin_error':maxbins,'independent_sign_error':maxsign,
            'physical_gate':read('inputs/eligibility.json')['decision']}
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Please run without -O')
    print(json.dumps(check(),indent=2))
