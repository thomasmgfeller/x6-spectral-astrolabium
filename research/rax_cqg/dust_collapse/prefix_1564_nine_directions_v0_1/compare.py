"""Compare replayed certificates, computed amplitudes and exact records."""
import json
import math
import sys
from pathlib import Path

def compare(a,b,where):
    if isinstance(a,dict) and isinstance(b,dict) and a.keys()==b.keys():
        for k in a:compare(a[k],b[k],where+'.'+k)
    elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,f'{where}[{i}]')
    elif isinstance(a,float) and isinstance(b,float):
        if not math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-13):
            raise ValueError(where)
    elif a!=b:
        raise ValueError(where)

if __name__=='__main__':
    left,right=[json.loads(Path(p).read_text()) for p in sys.argv[1:]]
    compare(left,right,'result')
    print('PASS: replay agrees with the archived direction and clock certificates')
