"""Explorativer Gegenzeuge nach der Fensterprüfung. Alle Bestätigungen sind rational."""
import json
from fractions import Fraction as F
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HALF = F(1,2)
WINDOW = (F(15,32),F(17,32))
# Nach Sichtung der ersten Fälle gesucht. Alle Einbettungs- und Vorzeichentests sind exakt.
HYPOTHESES = ((F(-1),F(1)),(F(-9,4),F(357,200)))


def radius(r,t):
    return r-(t-HALF)/8


def endpoint_distance_upper(coords, clocks, start, zcenter, t):
    # Affine Verlängerung von start über 11. Positive Zeitabstände sind zertifiziert.
    ta,tb = clocks[start],clocks[11]
    assert ta[1] < tb[0] <= tb[1] < t
    alpha_lo = (t-ta[1])/(tb[1]-ta[0])
    alpha_hi = (t-ta[0])/(tb[0]-ta[1])
    upper = 0
    for pi,pj,center in zip(coords[start],coords[11],(0,0,zcenter),strict=True):
        delta = pj-pi
        upper += max((pi+alpha*delta-center)**2 for alpha in (alpha_lo,alpha_hi))
    return upper


def run():
    pair=json.loads((ROOT/'eingaben/Vergleichspaar.json').read_text())
    xyz=[tuple(map(F,ps)) for ps in json.loads((ROOT/'eingaben/Ortskoordinaten.json').read_text())]
    rows=[]
    for prep in ('heavy','light'):
        clocks=[tuple(map(F,ab)) for ab in pair[prep]['normalized_clocks']]
        weights=[tuple(map(F,ab)) for ab in pair[prep]['weight_box']]
        for z,r in HYPOTHESES:
            side_margin=[]
            radial_intervals=[]
            for ps,(lo,hi),(wlo,whi) in zip(xyz,clocks,weights,strict=True):
                d2=sum((a-c)**2 for a,c in zip(ps,(0,0,z),strict=True))
                rmin,rmax=radius(r,hi),radius(r,lo)
                assert 0<rmin<=rmax
                if wlo>0:
                    side_margin.append(rmin**2-d2)
                    radial_intervals.append((d2/rmax**2,d2/rmin**2))
                else:
                    assert wlo==whi==0
                    side_margin.append(d2-rmax**2)
            assert len(radial_intervals)==19 and min(side_margin)>0
            gaps=[nxt[0]-prev[1] for prev,nxt in pairwise(sorted(radial_intervals))]
            assert min(gaps)>0
            # The ball worldtube is convex for affine r(t)>0. Every straight
            # segment whose two endpoints are strictly inside lies inside throughout.
            ray_gaps=[radius(r,t)**2-endpoint_distance_upper(xyz,clocks,i,z,t)
                      for i in (3,4,5) for t in WINDOW]
            assert min(ray_gaps)>0
            rows.append({'praeparation':prep,'zentrum_z':str(z),'radius_bei_halb':str(r),
                         'kleinste_quadratische_seitenmarge':str(min(side_margin)),
                         'kleinste_quadratische_bahnmarge_an_fensterenden':str(min(ray_gaps)),
                         'kleinste_luecke_radialer_koordinaten_quadratisch':str(min(gaps))})
    a,b=(h[1] for h in HYPOTHESES)
    return {'fenster':list(map(str,WINDOW)),'beide_radien':list(map(str,(a,b))),
            'minimax_radius':str((b-a)/(a+b)),
            'minimax_flaeche':str((b**2-a**2)/(b**2+a**2)),
            'gleiches_bahnsignal':'innen auf allen drei Bahnen im gesamten Fenster', 'faelle':rows}


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Python ohne -O starten')
    print(json.dumps(run(),indent=2,ensure_ascii=False))
