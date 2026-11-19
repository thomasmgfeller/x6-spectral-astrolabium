"""Finite-grid contractions for the first two limiting N15 histories in v0.8."""
from argparse import ArgumentParser
import ctypes as ct
from math import factorial
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from reference import ROOT, layout, net, direct_packet, save_json
from uhrtest import GRIDS
import quadrature
import numpy as np

FORK, CHAIN = 339773, 524287

class Grid:
    def __init__(self, mask, n):
        self.n = n
        self.inner, self.coeff, self.gravity = layout((7, mask))
        self.p, self.f = net.geometry.P, net.geometry.F
        self.fixed = {i: (i-5)*net.STEP for i in self.p+self.f}
        nodes, weights = net.quadrature(n)
        self.x = 1.5*nodes
        self.dist = net.BETA/2*(self.x[:, None]-self.x[None, :])**2
        self.unary = {j: weights*np.exp(-1j*net.BETA/32*sum(
            self.coeff[j,i]*(self.fixed[i]-self.x)**2 for i in self.f)) for j in self.inner}
        self.parents = {j: tuple(i for i in self.inner if self.coeff.get((i,j),0))
                        for j in self.inner}

    def base(self, j, t):
        return 1 + net.BETA/2*sum(self.coeff[i,j]*((t if i==3 else self.fixed[i])-self.x)**2
                                   for i in self.p)

    def density(self, j, t):
        parents = self.parents[j]
        shape = (1,)*len(parents)+(self.n,)
        c = self.base(j,t).reshape(shape)
        for axis,i in enumerate(parents):
            shape = [1]*len(parents)+[self.n]
            shape[axis] = self.n
            c = c + self.coeff[i,j]*self.dist.reshape(shape)
        return self.unary[j]*net.density_factor(c)

    def packet(self, m, sample):
        ox, ow = net.quadrature(m)
        result = np.zeros(2,complex)
        for side in (-1,1):
            for node,weight in zip(ox,ow):
                t = -2*net.STEP+side/16+node/32
                fixed = {**self.fixed, 3:t}
                def collar(j):
                    return 1+net.BETA/2*sum(b*(fixed[j]-fixed[i])**2
                        for (i,k),b in self.coeff.items() if k==j and i in fixed)
                past = sum(collar(j) for j in self.p)
                phase = np.exp(1j*(self.gravity-sum(collar(j) for j in self.f)/16))
                readout = np.sinc(past/(64*np.pi))*np.exp(-.5j*past*np.array(net.RHO))
                result += weight*sample(t)*phase*readout/np.sqrt(3072)
        return result

def fork(n,m,order=86):
    grid = Grid(FORK,n)
    if tuple(grid.parents.values()) != ((),(4,),(),(4,6),(4,5),(4,5,6,11,12),(4,5)):
        raise ValueError("Unexpected fork topology")
    coefficients = [grid.coeff[i,13] for i in grid.parents[13]]
    if coefficients != [-8,-9,-9,1,1] or any(grid.coeff[i,13] for i in grid.p):
        raise ValueError("Unexpected five-parent phase")
    # H(C) = (1 + integral_0^1 exp(-iu C/2) du)/2. For a positive
    # order-q Gaussian rule the integrated midpoint Taylor remainder and
    # its quadrature counterpart bound the H error by (|C|/4)^(2q)/(2q)!.
    # |C| <= 1 + (beta/2)*9*28 < 208 for every allowed clock.
    if 1+net.BETA/2*9*sum(map(abs,coefficients)) >= 208:
        raise ValueError("Phase enclosure")
    remainder = 52**(2*order)/factorial(2*order)
    if remainder >= 1e-15:
        raise ArithmeticError(("Auxiliary quadrature order",order,remainder))
    nodes, weights = net.quadrature(order)
    us = np.r_[0., (1+nodes)/2]
    weights = np.r_[.5, weights/2]*np.exp(-.5j*us)
    kernels = {k: np.exp(-.5j*k*us[:,None,None]*grid.dist) for k in (1,-8,-9)}
    def sample(t):
        root = grid.density(4,t)
        side6 = grid.density(6,t)
        side5 = grid.density(5,t)*grid.density(14,t).sum(axis=-1)
        to11 = grid.density(11,t).reshape(n*n,n)
        to12 = grid.density(12,t).reshape(n*n,n)
        total = 0j
        for w,weak,strong,first in zip(weights,kernels[1],kernels[-9],kernels[-8]):
            # Axes of each partial branch are (4,6,13) or (4,5,13).
            branch6 = np.einsum('agc,g,gc->ac',(to11@weak).reshape(n,n,n),side6,strong)
            branch5 = np.einsum('abc,ab,bc->ac',(to12@weak).reshape(n,n,n),side5,strong)
            total += w*np.einsum('a,ac,ac,ac,c->',root,first,branch5,branch6,grid.unary[13])
        return total
    return grid.packet(m,sample)

def build_nested(directory):
    target = Path(directory)/'nested.so'
    subprocess.run(['cc','-O3','-std=c99','-fPIC','-shared','-ffp-contract=off','-march=native',
                    '-I',str(quadrature.ROOT),str(ROOT/'nested.c'),'-o',str(target),'-lm'],check=True)
    lib = ct.CDLL(str(target))
    D,Z = quadrature.DOUBLE, quadrature.COMPLEX
    lib.tail.argtypes = [ct.c_int,ct.c_int,D,Z,Z,D,Z,Z]
    lib.finish.argtypes = [ct.c_int,Z,D,Z,Z,D,Z,Z,quadrature.STRIDE,Z]
    lib.nested.argtypes = [ct.c_int,D,Z,Z,Z,Z]
    lib.tail.restype = lib.finish.restype = lib.nested.restype = None
    return lib

def chain(n,m,lib):
    grid = Grid(CHAIN,n)
    if tuple(grid.parents.values()) != ((),(4,),(4,5),(4,5,6),(4,5,6,11),
                                        (5,6,11,12),(4,5,6,11)):
        raise ValueError("Unexpected nested topology")
    if any(grid.coeff[i,j] for i in grid.p for j in (12,13,14)):
        raise ValueError("Boundary-dependent tail")
    def edges(parents,j):
        e = np.asarray([grid.coeff[i,j]*grid.dist for i in parents])
        return e, np.exp(-.5j*e)
    def tail(parents,j):
        e,z = edges(parents,j)
        out = np.empty(n**4,complex)
        base = grid.base(j,0)
        lib.tail(n,4,base,np.exp(-.5j*base),grid.unary[j],e,z,out)
        return out
    other = tail((5,6,12,11),13)
    last = tail((4,5,6,11),14)
    e,z = edges((4,5,6,11),12)
    lib.nested(n,e,z,grid.unary[12],other,last)
    del other
    e,z = edges((4,5,6),11)
    strides = np.array([n**3,n**2,n,1],dtype=np.int64)
    def sample(t):
        f0,f1,f2 = (grid.density(j,t) for j in (4,5,6))
        prefix = f0[:,None,None]*f1[:,:,None]*f2
        base = grid.base(11,t)
        out = np.empty(1,complex)
        lib.finish(n,prefix,base,np.exp(-.5j*base),grid.unary[11],e,z,last,strides,out)
        return out[0]
    return grid.packet(m,sample)

def run(mask):
    with TemporaryDirectory() as tmp:
        lib = build_nested(tmp) if mask == CHAIN else None
        def evaluate(n,m):
            return chain(n,m,lib) if mask==CHAIN else fork(n,m)
        error = float(max(abs(evaluate(4,3)-direct_packet((7,mask)))))
        if error >= 1e-13:
            raise ArithmeticError(("Independent Cartesian control",mask,error))
        rows = {}
        for tag,grid in GRIDS.items():
            rows[tag] = evaluate(*grid)
            print(mask,tag,rows[tag],flush=True)
        changes = [float(max(abs(rows[a]-rows[b]))) for a,b in (("coarse","fine"),("fine","control"))]
        if max(changes) >= 1e-7:
            raise ArithmeticError(("Grid refinement",mask,changes))
        return {"rows":{t:[[z.real,z.imag] for z in v] for t,v in rows.items()},
                "cartesian_error":error,"grid_changes":changes}

if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("mask",type=int,choices=(FORK,CHAIN))
    mask = parser.parse_args().mask
    save_json(ROOT/f"clock_{mask}.json", {str(mask):run(mask)})
