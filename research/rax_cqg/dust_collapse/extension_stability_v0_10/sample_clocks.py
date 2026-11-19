"""Fixed-sample evaluation on each original tensor grid and the continuous clock cube."""
from fractions import Fraction
from pathlib import Path
import argparse,hashlib,json,math
import numpy as np
from source import ROOT,CACHE,reference
from reference import net,layout
N=65536
B=2**32
def thresholds(weights):
    # Exact integer thresholds for normalized binary64 quadrature weights.
    w=[Fraction(float(x)) for x in weights]
    total=sum(w); acc=Fraction(0);out=[]
    for x in w:
        acc+=x
        out.append(int(B*acc/total))
    if out[-1]!=B or abs(float(total)-1)>2e-15:raise ValueError('weight normalization')
    return np.array(out,dtype=np.uint64)
def coordinates(draws,grid):
    if grid=='continuous':
        u=(draws.astype(np.float64)+.5)/B
        return (3*u[:,:7]-1.5,
              -2*net.STEP+np.where(u[:,7]<.5,-1,1)/16+(2*np.mod(2*u[:,7],1)-1)/32)
    n,m={'coarse':(32,6),'fine':(48,8)}[grid]
    nodes,w=net.quadrature(n);outer,ow=net.quadrature(m)
    x=1.5*nodes[np.searchsorted(thresholds(w),draws[:,:7],side='right')]
    t_values=np.r_[-1/16+outer/32,1/16+outer/32]-2*net.STEP
    return x,t_values[np.searchsorted(thresholds(np.tile(ow,2)/2),draws[:,7],side='right')]
def evaluate(mask,x,t):
    inner,coef,gravity=layout((7,mask))
    times={k:(k-5)*net.STEP for k in net.geometry.P+net.geometry.F}
    times[3]=t
    times.update({j:x[:,i] for i,j in enumerate(inner)})
    def arg(j):
        return 1+net.BETA/2*sum(b*(times[j]-times[i])**2 for (i,k),b in coef.items() if k==j and b)
    past=sum(arg(j) for j in net.geometry.P)
    z=np.exp(1j*(gravity-sum(arg(j) for j in net.geometry.F)/16))*np.sinc(past/(64*np.pi))/np.sqrt(768)
    for j in inner:z*=net.density_factor(arg(j))
    if np.max(abs(z))>1/math.sqrt(768)+1e-13:raise ValueError('sample range')
    return [np.mean(z*np.exp(-.5j*r*past)) for r in net.RHO]
def run():
    raw=(ROOT/'uniforms_u32le.bin').read_bytes()
    if hashlib.sha256(raw).hexdigest()!='bc8c8c14e8fbc044c5554d233d4544d2b9607a92580b23b6fb5191a45d8f6c08':
        raise ValueError('sample digest')
    draws=np.frombuffer(raw,dtype='<u4').reshape(N,8)
    bad=json.loads((CACHE/'planes.json').read_text())['outside_types']
    if len(bad)!=119:raise ValueError('scope')
    out={}
    for tag in ('coarse','fine','continuous'):
        x,t=coordinates(draws,tag)
        out[tag]={name:[[z.real,z.imag] for z in evaluate(int(name[4:]),x,t)] for name in bad}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);args=p.parse_args()
    args.out.write_text(json.dumps(run(),indent=2,sort_keys=True)+'\n')
