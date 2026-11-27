"""Independent direct evaluation at the midpoints of the raw field boxes."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
root=Path(__file__).resolve().parent
doc=json.loads((root/'basis/Vergleichspaar.json').read_text())
r=set(map(tuple,doc['relation']))
p=[[F(t) for t in v] for v in json.loads((root/'Ortskoordinaten.json').read_text())]
out=json.loads((root/'Ergebnisse.json').read_text())
def dot(a,b):return sum(v*w for v,w in zip(a,b))
def coeff(rel,i,j):
    if (i,j) not in rel: return F(0)
    pred={u for u,v in rel if v==j};succ={v for u,v in rel if u==i}
    k=(1,-9,16,-8,0)[min(4,len(pred&succ))]
    return k-(F(1,10**11) if (i,j) in ((15,16),(16,18),(17,18),(18,7)) else 0)
for label in ['heavy','light']:
    v=doc[label]; yy,ww=([sum(map(F,t))/2 for t in v[s]] for s in ['clock_box','weight_box'])
    x=[(z-yy[3])/(yy[7]-yy[3]) for z in yy]
    for i,j in combinations(range(22),2):
        spatial=sum((a-b)**2 for a,b in zip(p[i],p[j]))
        assert (abs(x[i]-x[j])**2>spatial)==((i,j) in r or (j,i) in r)
    for i in range(22):
        for R,C in [(1,-1),(2,F(-5,2))]:
            sq=p[i][0]**2+p[i][1]**2+(p[i][2]-C)**2
            assert (sq<(R-(x[i]-F(1,2))/8)**2)==(ww[i]>0)
    for e in out['comparison'][label]['extensions']:
        past=e['order']['past'];future=e['order']['future']
        order=r|{(i,22) for i in past}|{(22,j) for j in future}
        mid=(yy[3]+yy[7])/2
        D=19+sum(coeff(order,i,22)*(mid-yy[i])**2 for i in past)
        G=sum(coeff(order,22,j)*ww[j]*(yy[j]-mid) for j in future)
        for a,key in [(D,'D22_center'),(G,'empty_G22_center')]:
            lo,hi=map(F,e['discrete'][key]);assert lo<=a<=hi<0
    for case in out['comparison'][label]['empty_futures']:
        if not case['allowed']:continue
        future=case['future']; f=r|{(22,j) for j in future}
        weights=[coeff(f,22,j)*ww[j] for j in future]
        z=dot(weights,[yy[j] for j in future])/sum(weights)
        for rec in case['old_field_vetoes']:
            order=f|{(i,22) for i in rec['past']};y=yy+[z]
            for key,(lo,hi) in rec['changed_density'].items():
                j=int(key)
                d=sum(coeff(order,i,j)*(y[i]-y[j])**2 for i in range(23))
                prev=sum(coeff(r,i,j)*(yy[i]-yy[j])**2 for i in range(22))
                assert F(lo)<=d-prev<=F(hi) and F(lo)*F(hi)>0
print('Unabhängige Gegenrechnung für beide Präparationen bestanden.')
