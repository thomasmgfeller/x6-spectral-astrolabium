"""Whole-lobe references only. This file contains no modulated integration."""
import argparse
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
from unittest.mock import patch
from study import DENSITIES, TYPES, REF_RADIUS, SOURCE_HASH, encode, geometry, source, write_fresh


def root_bounds(x):
    scale=10**15
    n=isqrt(x.numerator*scale**2//x.denominator)
    lo=Q(n,scale)
    return lo,lo if lo*lo==x else Q(n+1,scale)


def compute():
    import numpy as np
    with source():
        import boundary, scalar, clock_network
        import clock_integral as clock
        import finite_grid as finite
        from error_bounds import bounds
        finite.verify_constants(clock.BETA,clock.STEP)
        packets={}
        for end in TYPES:
            coeff,grav=geometry(end,boundary)
            assert len(coeff)<=91 and max(abs(x) for x in coeff.values())<=16
            inner=clock.INNER
            broad=next((j for j in inner if sum(bool(coeff.get((i,j))) for i in inner)>=4),None)
            assert broad is None or broad in (11,12,13)
            leaves=(11,12,13) if broad is None else [j for j in inner if j not in (4,5,broad)]
            assert not any(coeff.get((i,j)) for i in leaves for j in leaves)
            assert broad is None or not any(coeff.get((broad,j)) for j in inner)
            cert=bounds(coeff)
            ns=[cert[str(j)]['n'] for j in inner]
            nout=cert['3']['n']
            nr=cert.get('density',{}).get('n',1)
            assert max(ns+[nout,nr])<=80
            # Every individual sum in the certified broad expression stays within 80**3.
            assert len(ns)==6 and nr+1<=80
            small=clock.packet(coeff,grav,[4]*6,3,80)
            with patch.object(clock_network,'layout',scalar.layout):
                old=clock_network.packet((6,end),4,3)[0].sum(axis=1)/np.sqrt(2)
            discrepancy=float(max(abs(old-small)))
            assert discrepancy<2e-14
            values=clock.packet(coeff,grav,ns,nout,nr,checked=True)
            rows=[]
            for rho,z in zip(DENSITIES, values):
                re,im=map(Q,encode(z))
                lo,hi=root_bounds(re*re+im*im)
                assert lo>REF_RADIUS
                rows.append({'density':rho,'complex_center':encode(z),
                             'modulus_interval':[str(lo-REF_RADIUS),str(hi+REF_RADIUS)]})
            packets[str(end)]={'broad_node':broad,'coordinate_bounds':cert,'densities':rows,
                               'independent_small_grid_max_abs_difference':discrepancy}
            print('Qualified unmodulated end type',end,flush=True)
        return {'prefix':270,'source_sha256':SOURCE_HASH,'reference_radius':str(REF_RADIUS),
                'densities':list(DENSITIES),'packets':packets,'modulated_samples_evaluated':0}


if __name__=='__main__':
    if not __debug__:raise SystemExit('Keep assertions enabled.')
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    write_fresh(ap.parse_args().output,compute())
