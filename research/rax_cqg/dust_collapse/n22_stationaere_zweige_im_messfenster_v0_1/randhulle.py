"""Compute a uniform collar enclosure on a closed partition of the drift interval."""
from fractions import Fraction as F
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
import json,sys

def collect(parent, pieces):
    assert pieces>0
    with TemporaryDirectory() as td,ZipFile(parent) as archive:
        with ZipFile(BytesIO(archive.read('basis/N21.zip'))) as prev:
            with ZipFile(BytesIO(prev.read('basis/Ankerpaket.zip'))) as source:
                source.extractall(td)
        sys.path[:0]=[td,str(Path(td)/'basis')]
        from quellenpaket import model
        with model() as (_,__,previous,early):
            from modell import setup
            from referenzwechsel import displaced
            from empfangsbit import K0,STEP,V
            from staubgeraet import solve,verify
            from quelle import box,hull
            from driftfamilie import LABELS,LIMIT
            from gemischt import ORDER
            y,w=setup(previous,early)
            vel=(hull(-112*V,112*V),)*3; q=(hull(-1,1),)*3
            bounds={};assert LIMIT==F(1,10**6)
            for j in range(pieces):
                l=6*STEP-LIMIT+2*LIMIT*j/pieces
                h=6*STEP-LIMIT+2*LIMIT*(j+1)/pieces
                yy,ww=displaced(y,w,hull(l,h))
                for strength in LABELS:
                    st=solve(yy,ww,strength,vel,K0,box(-K0),'positive_bridge')
                    verify(st,strength,vel,K0,box(-K0),'positive_bridge',q)
                    for k in (0,1,2,3,7,8,9,10):
                        vals=[F(s)*10**9 for a in ('y','w') for s in st[a][k].data()]
                        row=[int(z//1) if i%2==0 else int(-(-z//1)) for i,z in enumerate(vals)]
                        old=bounds.setdefault(k,row)
                        bounds[k]=[(max if i%2 else min)(v,n) for i,(v,n) in enumerate(zip(old,row))]
            return {'pieces':pieces,'sources':len(LABELS),'order':sorted(ORDER),'collar':bounds}

if __name__=='__main__':
    print(json.dumps(collect(Path(__file__).resolve().parent/'basis/N22.zip',int(sys.argv[1]))))
