"""Measure all cost-selected N15 clocks, with a direct seven-clock control."""
import json
from unittest.mock import patch
import numpy as np
from model import ROOT, CACHE, layout, write
import clock14
net = clock14.reference

def direct(key,t,n):
    inner,coef,gravity=layout(key)
    u,w=net.quadrature(n); x=1.5*u
    times={i:(i-5)*net.STEP for i in net.geometry.P+net.geometry.F}
    times[3]=t
    weights=1.
    for axis,j in enumerate(inner):
        size=[1]*len(inner);size[axis]=n
        times[j]=x.reshape(size);weights=weights*w.reshape(size)
    def arg(j):
        return 1+net.BETA/2*sum(b*(times[j]-times[i])**2 for (i,k),b in coef.items() if k==j and b)
    val=weights*np.exp(1j*(gravity-sum(arg(j) for j in net.geometry.F)/16))
    for j in inner:
        # Removable singularity evaluated directly via expm1.
        a=np.asarray(arg(j)); ratio=np.divide(np.expm1(-.5j*a),-.5j*a,out=np.ones_like(a,dtype=complex),where=a!=0)
        val*= (1+ratio)/2
    return sum(arg(j) for j in net.geometry.P),np.sum(val)

def direct_packet(key):
    xs,ws=net.quadrature(3);out=np.zeros(2,complex)
    for side in [-1,1]:
        for x,w in zip(xs,ws):
            p,z=direct(key,-2*net.STEP+side/16+x/32,4)
            out+=w*z*np.sinc(p/(64*np.pi))*np.exp(-.5j*np.array(net.RHO)*p)/np.sqrt(3072)
    return out

def run():
    catalog=json.loads((ROOT/'catalog.json').read_text())
    out={}
    def plan(key):
        return 3,tuple(catalog['cheap_orders'][str(key[1])])
    with patch.object(net,'layout',layout),patch.object(net,'scheme',plan):
        for mask in sorted(map(int,catalog['cheap_orders'])):
            key=(7,mask)
            def amplitude(n,m):return net.packet(key,n,m)[0].sum(axis=1)/np.sqrt(2)
            low_error=float(max(abs(direct_packet(key)-amplitude(4,3))))
            assert low_error<1e-13,(mask,low_error)
            grids=[(32,6),(48,8),(64,10)]
            vals=[amplitude(n,m) for n,m in grids]
            error=[float(max(abs(b-a))) for a,b in zip(vals,vals[1:])]
            assert max(error)<1e-7,(mask,error)
            out[f'N15_{mask}']={'rows':{tag:[[float(z.real),float(z.imag)] for z in arr] for tag,arr in zip(['coarse','fine','control'],vals)},
                                'grid_changes':error,'small_direct_error':low_error}
    write('clocks.json',out)
if __name__=='__main__':run()
