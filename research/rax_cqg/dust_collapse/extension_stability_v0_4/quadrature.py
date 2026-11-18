"""Compute the full N13 support with bounded memory and a single local CPU thread."""
import argparse
import ctypes as ct
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'v03'))
from orders import layout
from clock_network import BETA, STEP, RHO, quadrature, density_factor, encode, decode, cartesian
import clock_network as reference

DOUBLE=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
COMPLEX=np.ctypeslib.ndpointer(dtype=np.complex128,flags='C_CONTIGUOUS')
STRIDE=np.ctypeslib.ndpointer(dtype=np.int64,flags='C_CONTIGUOUS')


def build(directory):
    target=Path(directory)/'contraction.so'
    subprocess.run(['cc','-O3','-std=c99','-fPIC','-shared','-ffp-contract=off','-march=native',
                    str(ROOT/'contraction.c'),'-o',str(target)],check=True)
    lib=ct.CDLL(str(target))
    lib.tail.argtypes=[ct.c_int,ct.c_int,DOUBLE,COMPLEX,COMPLEX,DOUBLE,COMPLEX,COMPLEX]
    lib.finish.argtypes=[ct.c_int,COMPLEX,DOUBLE,COMPLEX,COMPLEX,DOUBLE,COMPLEX,COMPLEX,STRIDE,COMPLEX]
    lib.tail.restype=lib.finish.restype=None
    return lib


class ClockGrid:
    def __init__(self, mask, n, lib):
        self.n,self.lib=n,lib
        self.inner,self.coeff,self.gravity=layout((5,mask))
        self.p,self.f=reference.geometry.P,reference.geometry.F
        x,w=quadrature(n)
        self.x=1.5*x
        self.fixed={i:(i-5)*STEP for i in (*self.p,*self.f)}
        dist=(self.x[:,None]-self.x[None,:])**2
        self.edges=[]
        self.edge_phase=[]
        self.unary=[]
        self.cbase=[]
        for k,j in enumerate(self.inner):
            self.cbase.append(1+BETA/2*sum(self.coeff[i,j]*(self.x-self.fixed[i])**2 for i in self.p if i!=3))
            e=np.array([BETA/2*self.coeff.get((i,j),0)*dist for i in self.inner[:k]],dtype=float)
            self.edges.append(e)
            self.edge_phase.append(np.exp(-.5j*e))
            self.unary.append(w*np.exp(-1j*BETA/32*sum(self.coeff[j,i]*(self.fixed[i]-self.x)**2 for i in self.f)))
        self.parents=[i for i,node in enumerate(self.inner[:4]) if self.coeff.get((node,self.inner[4]),0)]
        self.stride=np.zeros(4,dtype=np.int64)
        for j,i in enumerate(reversed(self.parents)):
            self.stride[i]=n**j
        self.last_edge=np.ascontiguousarray(self.edges[4][self.parents])
        self.last_phase=np.ascontiguousarray(self.edge_phase[4][self.parents])
        self.cached_tail=None

    def sample(self,t):
        n=self.n
        fixed={**self.fixed,3:t}
        def collar(j):
            return 1+BETA/2*sum(b*(fixed[j]-fixed[i])**2 for (i,k),b in self.coeff.items() if k==j and i in fixed)
        past=sum(collar(j) for j in self.p)
        overall=np.exp(1j*(self.gravity-sum(collar(j) for j in self.f)/16))
        base=[v+BETA/2*self.coeff[3,j]*(self.x-t)**2 for v,j in zip(self.cbase,self.inner)]
        if self.cached_tail is None:
            last=np.empty(n**len(self.parents),dtype=complex)
            self.lib.tail(n,len(self.parents),base[4],np.exp(-.5j*base[4]),self.unary[4],
                          self.last_edge,self.last_phase,last)
            if self.coeff[3,self.inner[4]]==0:
                self.cached_tail=last
        else:
            last=self.cached_tail
        f0=self.unary[0]*density_factor(base[0])
        f1=self.unary[1]*density_factor(base[1]+self.edges[1][0])
        c2=base[2]+self.edges[2][0][:,None,:]+self.edges[2][1][None,:,:]
        prefix=f0[:,None,None]*f1[:,:,None]*(self.unary[2]*density_factor(c2))
        val=np.empty(1,dtype=complex)
        self.lib.finish(n,prefix,base[3],np.exp(-.5j*base[3]),self.unary[3],
                        self.edges[3],self.edge_phase[3],last,self.stride,val)
        return past,overall*val[0]


def packet(mask,n,m,lib):
    solver=ClockGrid(mask,n,lib)
    nodes,w=quadrature(m)
    norm=np.sqrt(1/48/32);lobes=[];comp=[]
    for side in (-1,1):
        rows=[solver.sample(-2*STEP+side/16+x/32) for x in nodes]
        p,z=np.transpose(rows);p=p.real
        lobes.append([norm*((w*np.sinc(p/(64*np.pi))*np.exp(-.5j*r*p))@z) for r in RHO])
        comp.append(norm*(w@z))
    return np.array(lobes).T,sum(comp)/np.sqrt(2),solver.sample(-2*STEP)


def flat(values):
    lobes,comp,(_,fixed)=values
    return np.r_[lobes.ravel(),comp,fixed]


def compute(mask,lib):
    key=(5,mask);t=-2*STEP+1/16
    direct=float(abs(ClockGrid(mask,4,lib).sample(t)[1]-cartesian(key,t,4)))
    alternative=float(max(abs(flat(packet(mask,6,3,lib))-flat(reference.packet(key,6,3)))))
    assert max(direct,alternative)<2e-13,(mask,direct,alternative)
    series=[];old=None
    for n,m in [(32,6),(48,8),(64,10),(80,12)]:
        values=packet(mask,n,m,lib);current=flat(values)
        row={'grid':[n,m],'amplitudes':encode(values)}
        series.append(row)
        if old is not None:
            row['max_amplitude_change']=float(max(abs(current-old)))
            # The fixed-clock control is unattenuated. A tighter internal
            # stopping threshold also resolves the joint five-mode matrix check.
            if row['max_amplitude_change']<2e-12:
                break
        old=current
    else:
        raise ArithmeticError(f'Unresolved clock integral for {mask}')
    return {'direct_point_error':direct,'independent_packet_error':alternative,'grids':series}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    prior=json.loads((ROOT/'v03/results.json').read_text())
    masks=sorted(int(name.split('_')[1]) for name in prior['width_per_sequential_type'])
    assert len(masks)==23
    rows={}
    with TemporaryDirectory() as tmp:
        lib=build(tmp)
        for mask in masks:
            rows[f'N13_{mask}']=compute(mask,lib)
            print(mask,rows[f'N13_{mask}']['grids'][-1]['grid'],flush=True)
    args.output.write_text(json.dumps(rows,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':
    main()
