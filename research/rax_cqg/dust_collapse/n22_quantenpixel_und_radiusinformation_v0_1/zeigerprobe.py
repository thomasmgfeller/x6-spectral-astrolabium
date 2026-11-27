"""Formale Zweiarmauswertung eines archivierten Paarterms; keine CST-Apparatepräparation."""
import json
from fractions import Fraction as F
from pathlib import Path
from wirkung.wirkungszeuge import DEVICES, add, mul, point

INPUT=Path(__file__).resolve().parent/'eingaben/Vergleichspaar.json'


def delta(a,b):
    return a[0]-b[1], a[1]-b[0]


def main():
    d=json.loads(INPUT.read_text())
    rel=set(map(tuple,d['relation']))
    k={}
    for i,j in rel:
        n=sum((i,m) in rel and (m,j) in rel for m in range(22))
        k[i,j]=F((1,-9,16,-8,0)[min(4,n)])-F((i,j) in DEVICES,10**11)
    h=F(1,1024)
    rows={}
    for side in ('heavy','light'):
        y=[tuple(map(F,b)) for b in d[side]['clock_box']]
        w=[tuple(map(F,b)) for b in d[side]['weight_box']]
        g=point(0)
        for i,j in sorted(rel):
            if 17 not in (i,j):
                continue
            gap=delta(y[j],y[i])
            # Der ganze symmetrische Uhrtest bleibt innerhalb der strikten Ordnung.
            assert gap[0]>h
            edge=mul(point(k[i,j]),mul(w[j],gap))
            g=add(g,edge if i==17 else mul(point(-1),edge))
        assert g[0]<=0<=g[1]
        # F_plus - F_minus bei Eingriff ausschliesslich in das Startargument 17
        # des ausgewählten empfangsgewichteten Terms (17,18).
        probe=mul(point(-4*h*k[17,18]),mul(w[18],delta(y[18],y[17])))
        assert probe[1]<0
        rows[side]={'one_edge_delta_F':list(map(str,probe)), 'G17_box':list(map(str,g)),
                    'whole_delta_F_on_stationary_solution':'0','paired_radius_difference':'0'}
    return {'half_shift_raw_clock':str(h),'status':'FORMAL_ACTION_CONTROL_ONLY','rows':rows}

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen')
    print(json.dumps(main(),indent=2))
