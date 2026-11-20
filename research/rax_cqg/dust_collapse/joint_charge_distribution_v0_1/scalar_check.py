"""Compare canonical phases and widths to the symbolic archived reference."""
import sys
import mpmath as mp
import numpy as np
from model import BASE,I,scalar,edges,laws
sys.path.insert(0,str(BASE/'inputs/scalar'))
import geometry
mp.mp.dps=55
def run():
    keys,_=laws()
    catalog=__import__('json').loads((BASE/'inputs/four/catalog.json').read_text())['ranks_pure_free_mixed']
    tests=[keys[0],keys[-1],next(k for k in keys if catalog[str(k)][1]>0)] if any(catalog[str(k)][1]>0 for k in keys) else [keys[0],keys[len(keys)//2],keys[-1]]
    result={}
    for k in sorted(set(tests)):
        b=edges(k)
        def layout(_):
            return tuple(map(int,I)),{(int(i),int(j)):int(b[i,j]) for i,j in zip(*np.nonzero(b))},int(15-b.sum())
        geometry.order=layout
        details,(m,n)=geometry.kernel(k)
        a,fac=scalar(b)
        err=max(np.max(np.abs(np.array(m.tolist(),complex)-a))/np.max(abs(a)),abs(complex(n)-fac)/abs(fac))
        assert err<1e-6, (k,err)
        result[k]=float(err)
    return result
if __name__=='__main__': print(run())
