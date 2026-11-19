"""Positive finite-quadrature majorants by summing every unary and binary density factor."""
from functools import cache
import json
import numpy as np
from pilot import net
from model import ROOT, layout, write

def calculator(n,m):
    nodes,w=net.quadrature(n);x=1.5*nodes
    outer,ow=net.quadrature(m)
    t=-2*net.STEP+np.concatenate([-1/16+outer/32,1/16+outer/32])
    ow=np.tile(ow,2)/2
    p=net.geometry.P
    # The number of distinct coefficient patterns is small; keep only finite O(m*n^2) arrays.
    @cache
    def factors(past,edge):
        arg=np.ones((len(t),n))
        for k,b in zip(p,past):
            ti=t[:,None] if k==3 else (k-5)*net.STEP
            arg+=net.BETA/2*b*(x[None,:]-ti)**2
        if edge:
            arg=arg[:,:,None]+net.BETA/2*edge*(x[:,None]-x[None,:])**2
        return abs(net.density_factor(arg))
    def bound(mask):
        inner,coeff,_=layout((7,mask))
        outgoing={i:np.ones((len(t),n)) for i in inner}
        value=np.ones(len(t))
        for j in reversed(inner):
            inc=[i for i in inner if coeff.get((i,j),0)]
            weight=outgoing[j]*w
            past=tuple(coeff.get((i,j),0) for i in p)
            if len(inc)==1:
                i=inc[0]
                assert inner.index(i)<inner.index(j)
                outgoing[i]*=np.einsum('ts,tsr->tr',weight,factors(past,coeff[i,j]),optimize=True)
            else:
                if not inc:weight=weight*factors(past,0)
                value*=weight.sum(axis=1)
        return float(ow@value/np.sqrt(768))+1e-12
    return bound

def run():
    c=json.loads((ROOT/'catalog.json').read_text());known=json.loads((ROOT/'clocks.json').read_text())
    masks=sorted({int(s) for r in c['roots'].values() for s in r['ends']})
    result={str(m):{} for m in masks}
    for tag,(n,m) in [('coarse',(32,6)),('fine',(48,8))]:
        bound=calculator(n,m)
        for mask in masks:
            result[str(mask)][tag]=bound(mask)
            if (row:=known.get(f'N15_{mask}')) is not None:
                assert max(abs(complex(*z)) for z in row['rows'][tag])<=result[str(mask)][tag]
    write('caps.json',result)
if __name__=='__main__':run()
