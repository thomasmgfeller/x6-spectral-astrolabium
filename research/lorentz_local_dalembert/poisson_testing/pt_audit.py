"""Independent integer-kernel controls and archived held-out audit.
SPDX-License-Identifier: Apache-2.0
"""
from pt_common import *
from pt_validate import evaluate
from wv_run import classify_cells

def controls(f):
    rng=np.random.default_rng(71023)
    cells=rng.integers(-25,26,size=(4096,3),dtype=np.int64)
    lo=rng.integers(-20,21,size=(21,3),dtype=np.int64)
    hi=lo+rng.integers(0,2,size=lo.shape,dtype=np.int64)
    pairs=rng.integers(0,21,size=(90,2))
    fi,_,pi,_=classify_cells(cells,lo,hi)
    expected=np.zeros(128,dtype=np.int64)
    fb=np.zeros((21,2),dtype=np.uint64);pb=fb.copy()
    for i,(a,b) in enumerate(pairs):
        expected[i]=np.sum(fi[a]&pi[b])
        fb[a,i//64]|=np.uint64(1)<<np.uint64(i%64)
        pb[b,i//64]|=np.uint64(1)<<np.uint64(i%64)
    assert sum(expected)>0
    for offset in [0,10**10,-10**10]:
        x=cells+offset;l=lo+offset;h=hi+offset;out=np.zeros(128,dtype=np.int64)
        assert f(x.ctypes.data,len(x),l.ctypes.data,h.ctypes.data,21,fb.ctypes.data,pb.ctypes.data,out.ctypes.data)==0
        assert np.array_equal(out,expected)
    # Scale spatial/temporal differences enough that squares exceed int64.
    # Exact pointwise Python integers provide an independent reference.
    x=cells*10**9;l=lo*10**9;h=hi*10**9;out=np.zeros(128,dtype=np.int64)
    assert f(x.ctypes.data,len(x),l.ctypes.data,h.ctypes.data,21,fb.ctypes.data,pb.ctypes.data,out.ctypes.data)==0
    expected=np.zeros(128,dtype=np.int64)
    for cell in x.tolist():
        future=[];past=[]
        for low,high in zip(l.tolist(),h.tolist()):
            r=sum(max(abs(cell[j]-high[j]),abs(cell[j]+1-low[j]))**2 for j in (1,2))
            df=cell[0]-high[0];dp=low[0]-cell[0]-1
            future.append(df>0 and df*df>r);past.append(dp>0 and dp*dp>r)
        for i,(a,b) in enumerate(pairs):expected[i]+=future[a] and past[b]
    assert np.array_equal(out,expected)
    return dict(cells=4096,intervals=90,translation_controls=3,large_square_python_integer_control=True)

def audit():
    frozen();c=read(HERE/'contract.json');m=read(HERE/'model.json')
    assert len(set(c['training_seeds']+c['validation_seeds']))==4
    assert read(HERE/'model_seal.json')['model_sha256']==hashlib.sha256((HERE/'model.json').read_bytes()).hexdigest()
    rows=[];checked=0
    for phase in ['training','validation']:
      for g in range(2):
        r=read(HERE/f'{phase}-{g}.json.gz')
        assert r['geometry']==g and r['phase']==phase and r['seed']==c[phase+'_seeds'][g]
        assert len(r['counts'])==len(r['auxiliary_box_point_counts'])==c[phase+'_trials_per_geometry']
        assert F(r['coupling_upper'])>=setup(g)['coupling_upper']
        for row,size in zip(r['counts'],r['auxiliary_box_point_counts']):
            assert len(row)==90 and all(isinstance(v,int) and 0<=v<=size for v in row)
            exact=sum(a*b for a,b in zip(row,m['coefficients']))
            assert exact==int(np.array(row,dtype=np.int64)@np.array(m['coefficients'],dtype=np.int64))
            checked+=1
        if phase=='training':assert m['training_source_hashes'][g]==hashlib.sha256((HERE/f'{phase}-{g}.json.gz').read_bytes()).hexdigest()
        else:rows.append(r)
    assert evaluate(rows)==read(HERE/'summary.json')
    return dict(status='PASS',integer_scores_checked=checked,kernel_controls=controls(kernel()),frozen_protocol_and_model_hashes=True)
if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
