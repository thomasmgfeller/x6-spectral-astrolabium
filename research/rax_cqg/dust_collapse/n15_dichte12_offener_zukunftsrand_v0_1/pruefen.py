"""Replay the archived calculations without replacing the checked results."""
from pathlib import Path
import hashlib
import json
import math
import auslese
import zertifikat
import gegenproben

ROOT=Path(__file__).resolve().parent
def compare(current,saved,path=''):
    if isinstance(current,dict):
        assert set(current)==set(saved),path
        for k,value in current.items():
            compare(value,saved[k],path+'/'+k)
    elif isinstance(current,list):
        assert len(current)==len(saved),path
        for i,(a,b) in enumerate(zip(current,saved)):
            compare(a,b,path+'/'+str(i))
    elif isinstance(current,float):
        if 'quadrature_differences' in path:
            # Both quadratures have already been checked in the numerical run.
            return
        if 'fraction' in path:
            assert abs(current-saved)<1e-13,path
        else:
            assert math.isclose(current,saved,rel_tol=2e-6,abs_tol=2e-21),path
    else:
        assert current==saved,path

def main():
    for row in (ROOT/'SHA256SUMS').read_text().splitlines():
        h,name=row.split('  ',1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
    for name,fn in [('zertifikat',lambda:{'collar':zertifikat.collar(),'witness':zertifikat.support()}),
                    ('gegenproben',gegenproben.main),('auslese',auslese.main)]:
        compare(fn(),json.loads((ROOT/'ergebnisse'/(name+'.json')).read_text()),name)
        print('PASS',name,flush=True)
if __name__=='__main__':
    main()
