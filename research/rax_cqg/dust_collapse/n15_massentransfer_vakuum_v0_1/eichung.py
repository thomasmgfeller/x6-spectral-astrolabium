from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from antwort import spectrum

ROOT=Path(__file__).resolve().parent

def calibrate():
    runs={}
    for n,k in [(3,4),(4,8),(5,10)]:
        empty=spectrum(0,.125,'empty',n,k)
        quarter=spectrum(.25,.125,'positive',n,k)
        runs[f'{n}x{k}']={'empty':empty['raw'],'quarter':quarter['raw']}
    high=runs['5x10']
    assert max(abs(high[x]-runs['4x8'][x]) for x in high)<1e-8
    with localcontext() as ctx:
        ctx.prec=40
        offset=Decimal(str(high['empty']))
        gain=Decimal('0.25')/(Decimal(str(high['quarter']))-offset)
    return {'plan_sha256':hashlib.sha256((ROOT/'pruefplan.txt').read_bytes()).hexdigest(),
            'calibration_centre':'1/8','standard':'1/4','zero':'empty',
            'gain':format(gain,'.12f'),'offset':format(offset,'.12f'),'levels':runs}

if __name__=='__main__':
    print(json.dumps(calibrate(),sort_keys=True,indent=2))
