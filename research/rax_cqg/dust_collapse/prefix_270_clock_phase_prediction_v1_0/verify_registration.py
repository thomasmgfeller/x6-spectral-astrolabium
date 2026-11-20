"""Reference-only checks and synthetic decision cases; no integration of target data."""
from copy import deepcopy
from unittest.mock import patch
from fractions import Fraction as F
import json
import subprocess
import sys
from packet270 import evaluate
from select270 import select
from qualification270 import qualification
from score import checked_registration, classify, score, load_json
from study import DENSITIES,TYPES,HERE,TARGET_RADIUS,source


def verify():
    lock=checked_registration()
    ref=load_json(HERE/'reference.json')
    gram=load_json(HERE/'gram/gram.json')
    assert json.loads(json.dumps(select()))==load_json(HERE/'selection.json')
    assert qualification(ref,gram)==load_json(HERE/'qualification.json')
    subprocess.run([sys.executable,'-B',str(HERE/'gram/verify_gram.py'),str(HERE/'gram/gram.json')],check=True)
    # Exercise the complete future cell routing with a synthetic constant / quadratic
    # replacing the physical tensor contraction. No physical cell integral is called.
    import numpy as np
    with source():
        import clock_integral,finite_grid
        def polynomial_packet(coeff,grav,ns,nout,nr,checked):
            assert nout<0 and checked
            x,w=finite_grid.checked_rule(nout)
            return np.array([sum(w),sum(x*x*w)],dtype=complex)
        with patch.object(clock_integral,'packet',polynomial_packet):
            routed=evaluate(ref,lock)
    for rho,expected_control in zip(DENSITIES,(1.,1/3)):
        for row in routed['densities'][rho].values():
            assert abs(float(F(row['complex_center'][0])))<2e-12
            assert abs(float(F(row['unmodulated_split_center'][0]))-expected_control)<2e-12
    assert classify({r:(F(0),F(1,100)) for r in DENSITIES})=='PASS'
    assert classify({r:(F(1,100),F(2,100)) for r in DENSITIES})=='HOLD'
    fake={'prefix':270,'registration_sha256':lock,'densities':{r:{} for r in DENSITIES}}
    for i,rho in enumerate(DENSITIES):
        for j in map(str,TYPES):
            refrow=ref['packets'][j]['densities'][i]
            fake['densities'][rho][j]={'complex_center':['0','0'],
                    'complex_disk_radius':str(TARGET_RADIUS),'unmodulated_split_center':refrow['complex_center']}
    assert score(fake,lock,ref,gram)['status']=='PASS'
    fake['densities']['1/8']['623']['complex_center']=['1','0']
    assert score(fake,lock,ref,gram)['status']=='FAIL'
    for mutate in (
        lambda p: p['densities'].pop('1/8'),
        lambda p: p['densities']['1/8'].pop('751'),
        lambda p: p['densities']['1/8']['751'].update(complex_disk_radius='0'),
        lambda p: p['densities']['1/8']['751'].update(unmodulated_split_center=['2','2']),
        lambda p:p.update(registration_sha256='incorrect')):
        broken=deepcopy(fake)
        mutate(broken)
        try:score(broken,lock,ref,gram)
        except ValueError:pass
        else:raise ValueError('Invalid synthetic control or input accepted')
    print('PASS: reference preflight, Gram certificate and synthetic decision cases; no modulated target integrated.')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Keep assertions enabled.')
    verify()
