"""Reconstruct all nine derivatives and the bounds for both preparation densities."""
import os
for var in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[var]='1'
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import isqrt
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zipfile import ZipFile
import json
import sys

import mpmath as mp
import numpy as np
from clock_integral import packet, BETA, STEP, INNER
from finite_grid import verify_constants
from error_bounds import bounds,TOL
from moves import analyse
from old_fields import check_one

BASE=Path(__file__).resolve().parent
SOURCES={'CST_DUST_Randabbildung_1564_v0_1_Pruefpaket.zip':'ab2204236c27e8b804849d78889823927110e8fb41dabde3b8ab8e31018c325f',
         'CST_DUST_Praefix_1564_Rangtest_v0_1.zip':'69447107966b781771b1bcdad6ae62875752b3bf103dc499a786a1002651cb44'}
SOURCE0='CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip'
RADIUS=Q(1,60000)
DENSITIES=('1/8','1/4')

def root_bounds(q,scale=10**12):
    a=isqrt(q.numerator*scale**2//q.denominator)
    lo=Q(a,scale)
    return lo,lo if lo**2==q else Q(a+1,scale)

def zmod(z):
    x,y=Q.from_float(float(z.real)),Q.from_float(float(z.imag))
    lo,hi=root_bounds(x*x+y*y)
    return lo-RADIUS,hi+RADIUS

def unpack(temp):
    folders=[]
    for fn,h in SOURCES.items():
        p=BASE/fn
        assert sha256(p.read_bytes()).hexdigest()==h
        dest=temp/str(len(folders))
        with ZipFile(p) as z:z.extractall(dest)
        folders.append(dest)
    assert (folders[0]/SOURCE0).read_bytes()==(folders[1]/SOURCE0).read_bytes()
    with ZipFile(folders[0]/SOURCE0) as z:z.extractall(temp/'up')
    return *folders,temp/'up'/'prefix_1564_selection_v0_1'

def calculate(temp):
    bd,rg,up=unpack(temp)
    sys.path[:0]=[str(bd),str(rg),str(up)]
    import boundary, check, scalar, certify, clock_network
    load=lambda p:json.loads(p.read_text())
    data=load(bd/'result.json')
    prior=load(up/'result.json')
    idx=load(rg/'certificate.json')['one']['prefix']
    info=analyse(check,load(up/'inputs/exchange.json')['one'],load(up/'inputs/exchange_certificate.json')['one']['residual_orbit_masses'],data['branches'],idx)
    types=sorted([1790]+info['targets']);ref=types.index(1790)
    # Distinct regular quadratic action rates on one old-field line. A common bare
    # phase, positive old-packet factor and boundary section do not affect independence.
    line=list(range(13))
    rates={}
    fibres={}
    for row in data['branches']:
        _,marked_b,_=boundary.geometry_for(row['code'],6)
        fibres[str(row['code'])]=check_one(marked_b)
        if row['scalar']['kind']!='Fresnel':continue
        terms=row['scalar']['correction_upper']
        value=sum((1 if i==k else 2)*line[i]*line[k]*Q(a) for i,k,a in terms)
        rates[str(row['code'])]=str(value)
    assert len(set(rates.values()))==len(rates)==14
    assert len(data['singular_dust_certificate'])==2
    assert all(Q(z['rotated_real_dust_influence_lower'])>0 for z in data['singular_dust_certificate'])
    verify_constants(BETA,STEP)
    assert Q(37,1000)**2>Q(4,3072) and (8*TOL+Q(1,5000))*Q(37,1000)<RADIUS
    packets={};zs=[]
    for end in types:
        code=sum(1<<(6*i+j) for k,(i,j) in enumerate(combinations(range(6),2)) if end&(1<<k))
        _,b,g=boundary.geometry_for(code,6)
        # Independent whole-lobe reference on a small grid. For a broad node the
        # added density rule must resolve its oscillatory integral in this crosscheck.
        small=packet(b,g,[4]*6,3,80)
        with patch.object(clock_network,'layout',scalar.layout):
            archival=clock_network.packet((6,end),4,3)[0].sum(axis=1)/np.sqrt(2)
        assert max(abs(small-archival))<2e-14
        cert=bounds(b); ns=[cert[str(i)]['n'] for i in INNER]
        nout=cert['3']['n']; nr=cert.get('density',{}).get('n',1)
        assert max(ns+[nout,nr])<=80
        assert all(abs(weight)<=16 for weight in b.values()) and len(b)<=91
        z=packet(b,g,ns,nout,nr,checked=True)
        ordinary=packet(b,g,[24]*6,7,24)
        assert max(abs(z-ordinary))<RADIUS
        if end in (1790,5374):
            original=load(up/'inputs/response.json')
            report=next(x for x in original['production_grids'] if x['grid']==[80,12])
            lobes=np.array(report['packets'][original['order'].index(end)]['lobes'])
            full=(lobes[...,0]+1j*lobes[...,1]).sum(axis=1)/np.sqrt(2)
            assert max(abs(z-full))<2e-12
        local=[zmod(v) for v in z]
        assert min(x[0] for x in local)>Q(6,1000)
        zs.append(z)
        packets[str(end)]={'coordinate_bounds':cert,'complex_values':[[float(a.real),float(a.imag)] for a in z],
                           'modulus_bounds':[[str(x),str(y)] for x,y in local],
                           'small_grid_check':float(max(abs(small-archival))),
                           'change_24_to_bounded':float(max(abs(z-ordinary)))}
    keys=[(6,j) for j in types]
    mp.mp.dps=65
    states=scalar.states(keys)
    Gram=mp.matrix([[scalar.overlap(states[k],states[l]) for l in keys] for k in keys])
    Om=[scalar.rate(k) for k in keys]
    overlaps=[[Q(0) for _ in types] for _ in types]
    for i in range(len(types)):
        for j in range(i):
            overlaps[i][j]=overlaps[j][i]=Q(certify.upper_fourth_root(certify.overlap_fourth(Om[i],Om[j])))
    gram_lower=1-max(sum(row) for row in overlaps)
    assert gram_lower==Q(prior['rational_projection_certificate']['lower_eigenvalue_daughter_gram'])
    rows={}; conditioning={}
    for d,rho in enumerate(DENSITIES):
        vals=[r[d] for r in zs]
        mag=[zmod(v) for v in vals]
        al,ah=mag[ref];rows[rho]={}
        for j in info['targets']:
            i=types.index(j);bl,bh=mag[i];u=overlaps[ref][i]
            nominal=mp.sqrt(abs(vals[i])**2+abs(vals[ref])**2-
                2*mp.re(complex(vals[ref]).conjugate()*complex(vals[i])*Gram[ref,i]))/36
            lo=root_bounds(al**2+bl**2-2*ah*bh*u)[0]/36
            hi=root_bounds(ah**2+bh**2+2*ah*bh*u)[1]/36
            assert 0<float(lo)<=float(nominal)<=float(hi)
            rows[rho][str(j)]={'norm_at_step_1_over_36':float(nominal),'rigorous_range':[str(lo),str(hi)]}
        lower=root_bounds(gram_lower)[0]*min(mag[types.index(j)][0] for j in info['targets'])
        E=mp.matrix(len(types),9)
        for k,j in enumerate(info['targets']):
            E[ref,k]=-complex(vals[ref]);E[types.index(j),k]=complex(vals[types.index(j)])
        ev=mp.eighe(E.H*Gram*E,eigvals_only=True)
        conditioning[rho]={'sigma_min_lower':str(lower),'sigma_min_estimate':float(mp.sqrt(ev[0])),
                           'sigma_max_estimate':float(mp.sqrt(ev[8])),'rank':9}
    return {'prefix':1564,'reference_end':1790,'scope':'linear, unnormalized coherent amplitudes in the inherited fixed chart',
            'directions':info,'old_field_line':line,'old_dust_modulus_checks':fibres,'fourteen_distinct_regular_quadratic_rates':rates,
            'clock_disk_radius':str(RADIUS),'clock_packets_by_end':packets,
            'lower_scalar_gram_eigenvalue':str(gram_lower),'boundary_norms_by_density':rows,
            'joint_sensitivity_by_density':conditioning,'stage_6':'HOLD','P3':'HOLD'}

if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O to enable verification.')
    cmd=argparse.ArgumentParser();cmd.add_argument('output',type=Path);a=cmd.parse_args()
    with TemporaryDirectory() as temp:res=calculate(Path(temp))
    a.output.write_text(json.dumps(res,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print('PASS: marked responses, clock bounds for both densities, and nine coupled boundary directions.')
