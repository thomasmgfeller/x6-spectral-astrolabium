"""Zurückgehaltene vierte Kugel aus der nachträglichen Gegenbeispielsuche."""
import json
from fractions import Fraction as F
from kontrolle import ROOT, TIMES, sqrt_enclosure, synthetic_reader
from messen import radius_squared


def run():
    coords = json.loads((ROOT/'eingaben/Ortskoordinaten.json').read_text())
    start = tuple(map(F,coords[11]))
    out=[]
    for t in TIMES:
        r=F(357,200)-(t-F(1,2))/8
        reader=synthetic_reader((0,0,F(-9,4)),r)
        for reach in (4,8):
            status,(lo,hi)=radius_squared(reader,start,reach,8)
            assert status=='INTERVALL' and (F(19,20)*r)**2<=lo<=r**2<=hi<=(F(21,20)*r)**2
            out.append({'zeit':str(t),'suchgrenze':reach,'radius_wahr':str(r),
                        'radius_eingeschlossen':[str(sqrt_enclosure(lo)[0]),str(sqrt_enclosure(hi)[1])]})
    return out

if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Python ohne -O starten')
    print(json.dumps(run(),indent=2))
