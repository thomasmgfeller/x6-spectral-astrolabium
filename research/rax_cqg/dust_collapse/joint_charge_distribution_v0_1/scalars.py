"""Reconstruct the scalar output state of every type and validate overlaps."""
import json
import numpy as np
from model import BASE,edges,scalar,gram
def run():
    cat=json.loads((BASE/'inputs/four/catalog.json').read_text())
    keys=sorted(int(k) for k,(a,_,b) in cat['ranks_pure_free_mixed'].items() if a==b==0)
    states=[scalar(edges(k)) for k in keys]
    gm=gram(states)
    np.savez_compressed(BASE/'scalars.npz',keys=keys,precision=[s[0] for s in states],factor=[s[1] for s in states])
    print('unit-norm deviation',np.max(np.abs(gm.diagonal()-1)), 'Gram spectrum',np.linalg.eigvalsh(gm)[[0,-1]])
if __name__=='__main__': run()
