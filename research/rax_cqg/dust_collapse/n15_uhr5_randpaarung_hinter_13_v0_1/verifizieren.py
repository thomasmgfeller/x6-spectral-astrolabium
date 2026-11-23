"""Replay all calculations, compare archived values and the earlier central N15 outputs."""
from pathlib import Path
from hashlib import sha256
import json
import os
import subprocess
import sys

os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from randtest import amplitudes, H

ROOT=Path(__file__).resolve().parent


def compare(expected,actual,atol=4e-13):
    if isinstance(expected,dict):
        assert expected.keys()==actual.keys()
        for key,value in expected.items():
            compare(value,actual[key],atol)
    elif isinstance(expected,str):
        assert expected==actual
    else:
        np.testing.assert_allclose(actual,expected,rtol=4e-8,atol=atol)


def main():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    reproduced = {}
    for name in ('einschluss','randtest','dichte'):
        raw=subprocess.check_output([sys.executable,'-B',str(ROOT/(name+'.py'))],cwd=ROOT)
        current=json.loads(raw)
        reproduced[name] = current
        ref=json.loads((ROOT/(name+'.json')).read_text())
        if name=='einschluss':
            assert ref==current
        else:
            compare(ref,current)
    early = reproduced['randtest']['L']
    single = reproduced['dichte']['bins']['1']
    pulses = early['right_pulse_checks']
    native_difference = (np.array(pulses['plus']['native_lower_u11_probabilities'])
                         - np.array(pulses['minus']['native_lower_u11_probabilities']))
    np.testing.assert_allclose(single['native_prob_zero'], early['native_lower_u11_probabilities'],
                               rtol=0, atol=1e-13)
    np.testing.assert_allclose(single['plus_minus_difference'], native_difference, rtol=0, atol=1e-13)
    archived=json.loads((ROOT/'quellen/zentralvergleich.json').read_text())['gauss20']
    for pulse in (-1,0,1):
        values=[]
        for tag in (255/2048,257/2048):
            both=amplitudes('gauss',9,np.array([[.5,.625,.75,.125,tag,H]]),pulse)[0][0]
            low,high=abs(both[0]-1j*both[1])**2,abs(both[0]+1j*both[1])**2
            values.append((low-high)/(low+high))
        ref=archived[str(pulse)+'|0.125']
        np.testing.assert_allclose(values,[ref['balance_low'],ref['balance_high']],rtol=0,atol=2e-13)
        np.testing.assert_allclose(values[1]-values[0],ref['difference_in_balance'],rtol=0,atol=2e-13)
    print('PASS · Hashes, Intervallschranken, beide Quadraturen, Puls- und Klassentests sowie drei publizierte Zentralfälle.')


if __name__=='__main__':
    main()
