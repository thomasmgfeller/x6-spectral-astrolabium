#!/usr/bin/env python3
"""Supplementary independent float64 Gauss-Legendre check, not certification."""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parent
def run(n):
    x,w=leggauss(n);w=w/2
    kernel=lambda a,b:0.5+0.5*np.expm1(-1j*(0.5+(b-a)**2/4))/(-1j*(0.5+(b-a)**2/4))
    K=kernel(x[None,:],x[:,None]);v0=K@w;v1=K@(w*np.sqrt(3)*x)
    z0=float(np.vdot(v0,w*v0).real);z1=float(np.vdot(v1,w*v1).real)
    vec=[]
    edges=[-1,-1/3,1/3,1]
    for lo,hi in zip(edges[:-1],edges[1:]):
        a=(lo+hi)/2+(hi-lo)*x/2
        vec.append(kernel(a[None,:],x[:,None])@(w*(hi-lo)/2))
    gram=np.array([[np.vdot(v,w*u)/z0 for u in vec] for v in vec])
    return z0,z1,gram
def main():
    c=json.loads((ROOT/'results/continuum_certificates.json').read_text());h=json.loads((ROOT/'results/history_events.json').read_text())
    midpoint=lambda d:(float(d['lower'])+float(d['upper']))/2
    reference=np.array([[midpoint(g['real'])+1j*midpoint(g['imag']) for g in row] for row in h['normalized_gram']])
    records=[]
    for n in [64,96]:
        z0,z1,g=run(n)
        errors=[abs(z0-midpoint(c['Z_constant_mode'])),abs(z1-midpoint(c['Z_linear_normalized_mode']))]
        errors+=list(np.abs(g-reference).ravel())
        errors += [abs(z0/(z0+z1)-midpoint(c['equal_prior_flag0_after_conditioning'])),abs(np.trace(g).real-midpoint(h['sum_diagonal']))]
        maximum=float(max(errors))
        if maximum>2e-12:raise RuntimeError('Independent quadrature mismatch')
        records.append({'order':n,'complex_or_real_comparisons':len(errors),'max_absolute_difference':maximum})
    out={'method':'Independent closed-form density integral and Gauss-Legendre clock integrals','numpy':np.__version__,
         'threshold':2e-12,'certification':False,'records':records,'status':'PASS'}
    (ROOT/'results/quadrature_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
