"""N15_356087. Sum clocks 12 and 13 conditionally on two phase coefficients."""
import argparse,ctypes,json,subprocess,tempfile
from math import factorial
import numpy as np
from source import ROOT,reference
from reference import net
from coupled import Grid
from controls import cartesian
MASK=356087
# Spacing powers of two; grid includes three spare nodes on either edge.
DU=1/4
DV=1/8
class MixedGrid(Grid):
    def __init__(self, orders):
        super().__init__(MASK, 3)
        self.axis, self.unary = {}, {}
        for j,n in zip(self.inner,orders,strict=True):
            node,w=net.quadrature(n)
            x=self.axis[j]=1.5*node
            self.unary[j]=w*np.exp(-1j*net.BETA/32*sum(self.coeff[j,i]*(self.fixed[i]-x)**2 for i in self.f))

    def density(self,j,t):
        parents=self.parents[j]
        x=self.axis[j]
        arg=1+net.BETA/2*sum(self.coeff[i,j]*((t if i==3 else self.fixed[i])-x)**2 for i in self.p)
        for k,i in enumerate(parents):
            shape=[1]*(len(parents)+1)
            shape[k]=len(self.axis[i])
            arg=arg+self.coeff[i,j]*(net.BETA/2)*(self.axis[i].reshape(shape)-x)**2
        return self.unary[j]*net.density_factor(arg)

CONTINUUM_ORDERS=(96,68,48,48,24,56,48)
def run(n,m,lib):
    orders=(n,)*7 if isinstance(n,int) else n
    grid=MixedGrid(orders)
    if list(grid.parents.values())!=[(),(4,),(4,5),(4,5,6),(),(4,5,6,11,12),(4,5,6)]:
        raise ValueError('unexpected graph')
    cs=[grid.coeff[j,13] for j in grid.parents[13]]
    if cs!=[-8,16,-9,1,1] or any(grid.coeff[j,13] for j in grid.p):
        raise ValueError('phase coefficients')
    e,l=grid.axis[13],grid.axis[12];scale=reference.net.BETA/2
    # Dynamic argument C=1+scale*(U-2eV+e^2+l^2-2le).
    # Over padded rectangular interpolation domain |C|< 210; midpoint
    # Gauss Taylor remainder <= (210/4)^(2q)/(2q)! for H.
    ug=np.arange(-39,39+DU/2,DU)
    vg=np.arange(-52,52+DV/2,DV)
    assert max(abs(ug))+3*max(abs(vg))+2.25+2.25+4.5 < 205/scale
    q=100
    assert 53**(2*q)/factorial(2*q)<1e-24
    nodes,gw=reference.net.quadrature(q)
    u=np.r_[0.,(1+nodes)/2]
    w=np.r_[.5,gw/2]
    # All interpolation points queried in the interior, so for six nodes
    # the distances are bounded by 3,2,1,1,2,3 times the respective spacing.
    # Norm bounds use sum of absolute cardinal weights < 8 (checked separately).
    left=np.exp(-.5j*scale*ug[:,None]*u)*w*np.exp(-.5j*u)
    mid=np.exp(1j*scale*vg[:,None,None]*u[None,:,None]*e)
    lp=l[:,None]**2-2*l[:,None]*e[None,:]
    lphase=np.exp(-.5j*scale*u[:,None,None]*lp[None,:,:])
    ephase=grid.unary[13]*np.exp(-.5j*scale*u[:,None]*e**2)
    def sample(t):
        d12=grid.density(12,t)
        tail=ephase*np.einsum('l,ule->ue',d12,lphase)
        right=np.einsum('vue,ue->vu',mid,tail)
        table=np.ascontiguousarray(left@right.T)
        f4,f5,f6=(grid.density(j,t) for j in (4,5,6))
        prefix=np.ascontiguousarray(f4[:,None,None]*f5[:,:,None]*f6*grid.density(14,t).sum(axis=3))
        d11=np.ascontiguousarray(grid.density(11,t))
        result=np.zeros(1,complex)
        lib.reduce(*orders[:4],len(ug),len(vg),ug[0],vg[0],DU,DV,*(grid.axis[j] for j in (4,5,6,11)),table,prefix,d11,result)
        return result[0]
    return grid.packet(m,sample)
def build(d):
    so=str(d/'reduce.so')
    subprocess.run(['cc','-O3','-std=c99','-ffp-contract=off','-fPIC','-shared',str(ROOT/'clock_lookup.c'),'-o',so,'-lm'],check=True)
    from numpy.ctypeslib import ndpointer
    c=ctypes;lib=c.CDLL(so)
    lib.reduce.argtypes=[c.c_int]*6+[c.c_double]*4+[ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')]*4+[ndpointer(dtype=np.complex128,flags='C_CONTIGUOUS')]*4
    lib.reduce.restype=None
    return lib
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=__import__('pathlib').Path,required=True);p.add_argument('--max',type=int,default=64);p.add_argument('--continuous',action='store_true');args=p.parse_args()
    data={}
    with tempfile.TemporaryDirectory() as d:
        lib=build(__import__('pathlib').Path(d))
        for n,m in ([(CONTINUUM_ORDERS,10)] if args.continuous else [(4,3),(5,4),(32,6),(48,8),(64,10)]):
            if isinstance(n,int) and n>args.max:continue
            a=run(n,m,lib);row={'amplitudes':[[z.real,z.imag] for z in a]}
            if n in (4,5):
                err=max(abs(a-cartesian(MASK,n,m)));row['cartesian_error']=float(err)
                if err>1e-10:raise ValueError(err)
            data[f'{n},{m}']=row
            args.out.write_text(json.dumps(data,indent=2)+'\n')
            print(n,m,row,flush=True)
