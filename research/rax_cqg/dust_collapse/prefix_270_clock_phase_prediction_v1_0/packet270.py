"""The prospective seven-cell calculation. Importing this module integrates nothing."""
from fractions import Fraction as F
from unittest.mock import patch
from study import DENSITIES, TYPES, TARGET_RADIUS, encode, geometry, source


def u6(x):
    return 64*x**6-80*x**4+24*x*x-1


def cuts():
    pos=[]
    for lo,hi in [(F(1,8),F(1,4)),(F(1,2),F(3,4)),(F(7,8),F(1))]:
        assert u6(lo)*u6(hi)<0
        while hi-lo>F(1,2**50):
            mid=(lo+hi)/2
            if u6(lo)*u6(mid)<0:hi=mid
            else:lo=mid
        assert u6(lo)*u6(hi)<0
        pos.append((lo+hi)/2)
    return [F(-1),*[-x for x in reversed(pos)],*pos,F(1)]


def cells(config):
    ab=config['3']
    a,b=F(ab['quadratic_bound']),F(ab['linear_bound'])
    points=cuts()
    for k,(l,r) in enumerate(zip(points,points[1:])):
        h,p=(r-l)/2,(r+l)/2
        assert 0<h<=1 and h*(b+2*a*abs(p))<=b
        assert F.from_float(float(p))==p and F.from_float(float(h))==h
        yield k,p,h


def evaluate(ref,registration_sha):
    import numpy as np
    with source():
        import boundary
        import clock_integral as clock
        import finite_grid as finite
        finite.verify_constants(clock.BETA,clock.STEP)
        base_rule=finite.checked_rule
        rows={rho:{} for rho in DENSITIES}
        for end in TYPES:
            coeff,grav=geometry(end,boundary)
            config=ref['packets'][str(end)]['coordinate_bounds']
            ns=[config[str(i)]['n'] for i in clock.INNER]
            nout=config['3']['n']
            nr=config.get('density',{}).get('n',1)
            plain=np.zeros(2,dtype=complex)
            mod=np.zeros(2,dtype=complex)
            x,w=base_rule(nout)
            for k,p,h in cells(config):
                mapped=(float(p)+float(h)*x,float(h)*w)
                def mapped_rule(n):
                    return mapped if n==-nout else base_rule(n)
                with patch.object(finite,'checked_rule',mapped_rule):
                    z=clock.packet(coeff,grav,ns,-nout,nr,checked=True)
                plain+=z
                mod+=(-1)**k*z
            for i,rho in enumerate(DENSITIES):
                rows[rho][str(end)]={'complex_center':encode(mod[i]),
                     'complex_disk_radius':str(TARGET_RADIUS),'unmodulated_split_center':encode(plain[i])}
        return {'prefix':270,'registration_sha256':registration_sha,
                'method':'Seven fixed-sign Gauss cells with split positive reference controls',
                'densities':rows}
