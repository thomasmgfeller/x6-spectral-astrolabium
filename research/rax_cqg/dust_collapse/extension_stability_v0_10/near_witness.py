"""Independent deterministic follow-up on the smallest sampled plane margin."""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,json
import numpy as np
from source import reference
from coupled import Grid
from controls import cartesian
import quadrature
MASK=39485
def evaluate(n,m,lib):
    g=Grid(MASK,n)
    if list(g.parents.values())!=[(),(4,),(),(4,6),(4,6,11),(4,5),(4,)]:
        raise ValueError('unrecognized geometry')
    parts={}
    for j in (12,13,14):
        edges=np.ascontiguousarray([g.coeff[i,j]*g.dist for i in g.parents[j]])
        parts[j]=(edges,np.ascontiguousarray(np.exp(-.5j*edges)))
    def point(t):
        tail={}
        for j,(edge,phase) in parts.items():
            a=g.base(j,t)
            out=np.empty((n,)*len(g.parents[j]),complex)
            lib.tail(n,len(g.parents[j]),a,np.exp(-.5j*a),g.unary[j],edge,phase,out.reshape(-1))
            tail[j]=out
        v4=g.density(4,t)*tail[14]*(g.density(5,t)*tail[13]).sum(axis=1)
        v11=(g.density(11,t)*tail[12]).sum(axis=2)
        return np.einsum('a,c,ac->',v4,g.density(6,t),v11)
    return g.packet(m,point)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    results={}
    with TemporaryDirectory() as d:
        lib=quadrature.build(d)
        for n,m in ((4,3),(5,4),(32,6),(48,8),(64,10)):
            a=evaluate(n,m,lib);row={'amplitudes':[[z.real,z.imag] for z in a]}
            if n<=5:
                e=float(max(abs(a-cartesian(MASK,n,m))))
                if e>1e-13:raise ValueError(e)
                row['cartesian_error']=e
            results[f'{n},{m}']=row
    args.out.write_text(json.dumps(results,indent=2)+'\n')
