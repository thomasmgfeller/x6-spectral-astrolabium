"""Independent layer count, action residual and analytic-Jacobian check."""
from fractions import Fraction as F
import json
from modell import ROOT,FREE,POS,WINDOW,inputs,evaluate,make
from intervall import I

def coeff(rel):
    out={}
    for i,j in rel:
        past={a for a,b in rel if b==j};future={b for a,b in rel if a==i}
        k=F((1,-9,16,-8,0)[min(4,len(past&future))])
        if (i,j) in [(15,16),(16,18),(17,18),(18,7)]:k-=F(1,10**11)
        if k:out[i,j]=k
    return out

def direct(y,w,c):
    d=[19+sum(k*(y[j]-y[i])*(y[j]-y[i]) for (i,j),k in c.items() if j==v) for v in POS]
    g=[]
    for v in range(len(y)):
        incoming=sum(k*w[v]*(y[i]-y[v]) for (i,j),k in c.items() if j==v)
        outgoing=sum(k*w[j]*(y[j]-y[v]) for (i,j),k in c.items() if i==v)
        g.append(incoming+outgoing)
    return d+[g[j] for j in FREE],g

def check():
    pair,sets=inputs()
    doc=json.loads((ROOT/'Ergebnisse.json').read_text())
    counts=[0,0];seen=set()
    for r in doc['cases']:
        rel={(i,j) for i,j in pair['relation']}
        rel.update((i,22) for i in r['past']);rel.update((22,j) for j in r['future'])
        c=coeff(rel);assert c==make(pair,r['past'],r['future'])[1]
        if r['status']=='EXCLUDED':counts[1]+=1;continue
        counts[0]+=1
        for side in ('heavy','light'):
            tag=r[side];sol=doc['solutions'][tag]
            y,w=([I(*v) for v in sol[name]] for name in ('y','w'))
            vals,g=direct(y,w,c)
            assert all(v.l<=0<=v.h for v in vals)
            assert sum(g,I()).l<=0<=sum(g,I()).h
            mid=[t.mid() for t in y];ww=[t.mid() for t in w]
            cut=[(mid[j]-mid[3])/(mid[7]-mid[3]) for j in range(23)]
            assert [j for j,v in enumerate(cut) if WINDOW[0]<=v<=WINDOW[1]]==[17,20,22]
            assert all(ww[j]==0 for j in [17,20,22])
            if tag in seen:continue
            seen.add(tag)
            A,J,_=evaluate(mid,ww,c,F(0));assert A==direct(mid,ww,c)[0]
            # Residuals are at most quadratic in a single coordinate. A rational
            # two-sided difference gives the exact derivative at the midpoint.
            step=F(1,512)
            for t,(j,kind) in enumerate([(i,'y') for i in FREE]+[(i,'w') for i in POS]):
                results=[]
                for delta in [-step,step]:
                    Y=mid.copy();W=ww.copy()
                    (Y if kind=='y' else W)[j]+=delta
                    results.append(direct(Y,W,c)[0])
                assert [(hi-lo)/(2*step) for lo,hi in zip(*results)]==[row[t] for row in J]
    assert counts==[5,20] and len(seen)==4
    print('Alle 25 Ordnungen und vier verschiedene Lösungszeugnisse gegengeprüft.')

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen')
    check()
