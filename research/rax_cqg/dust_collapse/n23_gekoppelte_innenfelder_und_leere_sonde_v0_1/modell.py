"""The zero-source action rows on a one-event extension of the published order."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
import json

ROOT=Path(__file__).resolve().parent
ARCHIVE='8edc699efa941db67101e2fa6c138d6fba59c9c2d3a0db366f27bebb91974db5'
COLLAR=(0,1,2,3,7,8,9,10)
FREE=(4,5,6,*range(11,23))
POS=(4,5,6,11,12,13,14,16,18,19,21)
ZERO=(15,17,20,22)
DEVICE=((15,16),(16,18),(17,18),(18,7))
WINDOW=(F(15,32),F(17,32))

def inputs():
    path=ROOT/'basis/Randgeometrie.zip'
    assert sha256(path.read_bytes()).hexdigest()==ARCHIVE
    with ZipFile(path) as z:
        pair=json.loads(z.read('basis/Vergleichspaar.json'))
        prev=json.loads(z.read('Ergebnisse.json'))
    assert pair['order_id']==prev['order_id'] and prev['physical_P3_count']==60
    result={}
    for side in ['heavy','light']:
        sets={tuple(q['future']):[tuple(r['past']) for r in q['old_field_vetoes']]
              for q in prev['comparison'][side]['empty_futures'] if q['allowed']}
        assert sorted(map(len,sets.values()))==[4,21]
        result[side]=sets
    assert result['heavy']==result['light']
    return pair,result['heavy']

def make(pair,past,future):
    old=set(map(tuple,pair['relation']))
    rel=old|{(i,22) for i in past}|{(22,j) for j in future}
    assert len(rel)==152+len(past)+len(future)
    assert all((i,k) in rel and i!=k for i,j in rel for l,k in rel if j==l)
    edges={}
    for i,j in sorted(rel):
        size=sum((i,k) in rel and (k,j) in rel for k in range(23))
        k=F((1,-9,16,-8,0)[min(size,4)])-F((i,j) in DEVICE,10**11)
        if k:edges[i,j]=k
    return rel,edges

def active(edges):
    return {(i,j):v for (i,j),v in edges.items() if j not in ZERO and (i in FREE or j in FREE)}

def evaluate(y,w,edges,zero):
    """D, G and Jacobian, in the order positive densities, then free clock rows."""
    n=23
    D=[zero+19 for _ in range(n)]; G=[zero]*n
    H=[[zero for j in range(n)] for i in range(n)]
    C=[[zero for j in range(n)] for i in range(n)]
    for (i,j),k in edges.items():
        dy=y[j]-y[i]; p=k*dy; f=w[j]*p; c=k*w[j]
        D[j]+=p*dy; G[i]+=f;G[j]-=f
        C[i][j]+=p;C[j][j]-=p
        H[i][j]+=c;H[j][i]+=c;H[i][i]-=c;H[j][j]-=c
    J=[[-2*C[i][j] for i in FREE]+[zero]*len(POS) for j in POS]
    J+=[[H[i][j] for j in FREE]+[C[i][j] for j in POS] for i in FREE]
    return [D[j] for j in POS]+[G[i] for i in FREE],J,G
