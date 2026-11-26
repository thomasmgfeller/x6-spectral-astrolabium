from pathlib import Path
from fractions import Fraction as F
import sys,json
from intervall import I,span
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from quellenpaket import model


def enclosure(t):
    return I.enclose(*map(F,t.data()))


def collect():
    with model() as (_,__,prev,early):
        from gemischt import ORDER,WINDOWS
        from modell import setup
        from wege import ROUTES
        from referenzwechsel import displaced
        from empfangsbit import K0,STEP,V
        from staubgeraet import solve,verify
        from quelle import box,hull
        from driftfamilie import LABELS,LIMIT
        y,w=setup(prev,early)
        cert=json.loads((ROOT/'basis/Driftzertifikat.json').read_text())
        intervals=[tuple(map(F,c['delta'])) for c in cert['leaves']]
        assert len(intervals)==7 and intervals[0][0]==-LIMIT and intervals[-1][1]==LIMIT
        assert all(l<h for l,h in intervals) and all(b==c for (_,b),(c,_) in zip(intervals,intervals[1:]))
        velocity=(hull(-112*V,112*V),)*3
        positions=(hull(-1,1),)*3
        times={j:[] for j in y};weights={j:[] for j in y};cells=0
        for l,h in intervals:
            for i in range(8):
                left=l+i*(h-l)/8;right=l+(i+1)*(h-l)/8
                yy,ww=displaced(y,w,hull(6*STEP+left,6*STEP+right))
                for J in LABELS:
                    st=solve(yy,ww,J,velocity,K0,box(-K0),'positive_bridge')
                    verify(st,J,velocity,K0,box(-K0),'positive_bridge',positions)
                    for k in y:
                        times[k].append(enclosure(st['y'][k]))
                        weights[k].append(enclosure(st['w'][k]))
                    cells+=1
        return (set(ORDER),{k:span(v) for k,v in times.items()},
                {k:span(v) for k,v in weights.items()},WINDOWS,cells,ROUTES['positive_bridge'])
