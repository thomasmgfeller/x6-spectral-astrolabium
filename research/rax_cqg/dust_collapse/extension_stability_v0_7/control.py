"""Independent checks of the scalar rejection cases and finite-clock modulus relaxation."""
import json
from unittest.mock import patch
from model import ROOT, geometry, layout, write
from caps import calculator
from pilot import net
import numpy as np

def brute_forest(mask,n,m):
    inner,coeff,_=layout((7,mask));nodes,w=net.quadrature(n)
    outer,ow=net.quadrature(m);t={i:(i-5)*net.STEP for i in net.geometry.P}
    weight=1
    for i,j in enumerate(inner):
        shape=[1]*7;shape[i]=n
        t[j]=nodes.reshape(shape)*1.5;weight=weight*w.reshape(shape)
    val=0.
    for side in [-1,1]:
        for u,wu in zip(outer,ow):
            t[3]=-2*net.STEP+side/16+u/32;prod=weight
            for j in inner:
                if sum(bool(coeff.get((i,j),0)) for i in inner)>1:continue
                arg=1+net.BETA/2*sum(c*(t[j]-t[i])**2 for (i,h),c in coeff.items() if h==j and c)
                ratio=np.divide(np.expm1(-.5j*arg),-.5j*arg,out=np.ones_like(arg,dtype=complex),where=arg!=0)
                prod=prod*abs((1+ratio)/2)
            val+=wu*prod.sum()
    return val/(2*np.sqrt(768))

def run():
    cat=json.loads((ROOT/'catalog.json').read_text())
    excluded={k:v for k,v in cat['ranks_pure_free_mixed'].items() if v[0] or v[2]}
    with patch.object(geometry,'order',layout):
        for k,(a,b,c) in excluded.items():
            info,state=geometry.kernel((7,int(k)))
            assert state is None and info['status']=='OBSTRUCTION'
            assert [len(info['pure_bulk_null_vectors']),info['free_directions'],info['legendre_size']-info['legendre_rank']]==[a,b,c]
    good=sorted({int(k) for r in cat['roots'].values() for k in r['ends']})
    masks=good[::80]+[good[-1]]; getcap=calculator(4,3)
    error=max(abs(getcap(m)-1e-12-brute_forest(m,4,3)) for m in masks)
    assert error<1e-14
    return {'original_kernel_obstructions_rechecked':len(excluded),'forest_direct_masks':masks,'forest_direct_max_error':float(error)}
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O')
    write('controls.json',run())
