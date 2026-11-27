"""Getrennte synthetische Datenquelle und Überprüfung der ausgegebenen Radiusintervalle."""
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from messen import radius_squared

ROOT = Path(__file__).resolve().parents[1]
TIMES = tuple(map(F, ('15/32', '31/64', '1/2', '33/64', '17/32')))
RESOLUTIONS = (2, 4, 8, 16)
# Die Referenzwerte bleiben ausserhalb der Messfunktion.
SPHERES = (
    ('Kugel_1', (F(0),F(0),F(-1)), F(1), F(1,8)),
    ('Kugel_2', (F(0),F(0),F(-5,2)), F(2), F(1,8)),
    ('versetzte_Kontrolle', (F(1,2),F(-1,3),F(-4,3)), F(5,4), F(3,32)),
)


def sqrt_enclosure(x):
    grid = 10**9
    n = isqrt((x.numerator*grid**2)//x.denominator)
    lower = F(n,grid)
    return lower, lower if lower**2 == x else F(n+1,grid)


def synthetic_reader(center, radius):
    def inside(point):
        return sum((a-b)**2 for a,b in zip(point,center,strict=True)) <= radius**2
    return inside


def run():
    coords = json.loads((ROOT/'eingaben/Ortskoordinaten.json').read_text())
    start = tuple(map(F,coords[11]))
    rows = []
    for name, center, ref, speed in SPHERES:
        for t in TIMES:
            r = ref-speed*(t-F(1,2))
            side = synthetic_reader(center,r)
            for reach in (4,8):
                for n in RESOLUTIONS:
                    status, bounds = radius_squared(side,start,reach,n)
                    assert status == 'INTERVALL'
                    lo,hi = bounds
                    assert lo <= r**2 <= hi
                    good = (F(19,20)*r)**2 <= lo and hi <= (F(21,20)*r)**2
                    rlo,rhi = sqrt_enclosure(lo)[0],sqrt_enclosure(hi)[1]
                    err = max(1-rlo/r,rhi/r-1)
                    rows.append(dict(sphere=name,time=str(t),search_reach=reach,
                                     bisections_per_ray=n,synthetic_side_queries=7+6*n,
                                     radius_truth=str(r),radius_squared=list(map(str,bounds)),
                                     radius_outward_1e_9=[str(rlo),str(rhi)],
                                     relative_error_upper=str(err),within_five_percent=good))
    s = {}
    for n in RESOLUTIONS:
        group=[v for v in rows if v['bisections_per_ray']==n]
        s[n]=dict(cases=len(group),within_five_percent=sum(v['within_five_percent'] for v in group),
                  worst_relative_error_upper=str(max(F(v['relative_error_upper']) for v in group)))
    assert len(rows)==120
    nominal=synthetic_reader(SPHERES[0][1],SPHERES[0][2])
    negative={'start_outside':radius_squared(nominal,(F(10),F(0),F(0)),4,8)[0],
              'no_exterior':radius_squared(nominal,start,F(1,16),8)[0]}
    assert negative=={'start_outside':'START_AUSSEN','no_exterior':'AUSSENSEITE_FEHLT'}
    return {'scope':'Klassische synthetische Seitenmessung; keine CST-Feldmessung',
            'standort':list(map(str,start)), 'summary':s,'controls':negative, 'rows':rows}


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Python ohne -O starten')
    print(json.dumps(run(),indent=2,ensure_ascii=False))
