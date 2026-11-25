"""Replay without changing archived results. Integer checks are exact."""
import hashlib
import json
import math
from pathlib import Path
import fenster
import diamantklassen
import randvergleich
import absoluter_schnitt

ROOT = Path(__file__).resolve().parent

def compare(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for key in a:
            compare(a[key],b[key])
    elif isinstance(a,(tuple,list)):
        assert len(a)==len(b)
        for x,y in zip(a,b):
            compare(x,y)
    elif isinstance(a,float):
        assert math.isclose(a,b,rel_tol=1e-11,abs_tol=2e-13), (a,b)
    else:
        assert a==b, (a,b)

def main():
    meta=json.loads((ROOT/'quellen/herkunft.json').read_text())
    for row in meta['github_inputs']:
        data=(ROOT/'quellen'/row['local']).read_bytes()
        git_blob=b'blob '+str(len(data)).encode()+b'\0'+data
        assert hashlib.sha1(git_blob).hexdigest()==row['blob'],row['local']
    for module in (fenster,diamantklassen,randvergleich,absoluter_schnitt):
        saved=json.loads((ROOT/'ergebnisse'/(module.__name__+'.json')).read_text())
        compare(module.main(),saved)
        print('PASS',module.__name__,flush=True)

if __name__=='__main__':
    main()
