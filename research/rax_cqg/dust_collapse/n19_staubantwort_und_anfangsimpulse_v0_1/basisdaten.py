"""Exact input hashes, fixed point enclosures and algebraic interval arithmetic."""
from fractions import Fraction as Q
from io import BytesIO
from math import isqrt
from pathlib import Path
import json
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
SCALE = 10**32


def ceil(a,b):
    return -(-a//b)


class Box:
    __slots__ = ('lo','hi')
    def __init__(self, lo, hi):
        assert lo<=hi
        self.lo,self.hi=lo,hi

    def __add__(self,v):
        v=box(v);return Box(self.lo+v.lo,self.hi+v.hi)
    __radd__=__add__

    def __neg__(self):
        return Box(-self.hi,-self.lo)

    def __sub__(self,v):
        return self+-box(v)
    def __rsub__(self,v):
        return box(v)+-self

    def __mul__(self,v):
        v=box(v)
        ends=[i*j for i in (self.lo,self.hi) for j in (v.lo,v.hi)]
        return Box(min(ends)//SCALE,ceil(max(ends),SCALE))
    __rmul__=__mul__

    def __truediv__(self,v):
        v=box(v)
        assert not v.lo<=0<=v.hi,'divisor includes zero'
        return self*Box(SCALE**2//v.hi,ceil(SCALE**2,v.lo))
    def __rtruediv__(self,v):
        return box(v)/self

    def sqrt(self):
        assert self.lo>=0
        top=isqrt(self.hi*SCALE)
        return Box(isqrt(self.lo*SCALE),top+int(top**2<self.hi*SCALE))

    def union(self,v):
        return Box(min(self.lo,v.lo),max(self.hi,v.hi))

    def contains_zero(self):
        return self.lo<=0<=self.hi

    def data(self):
        return [str(Q(self.lo,SCALE)),str(Q(self.hi,SCALE))]


def box(v):
    if isinstance(v,Box):return v
    q=Q(v)*SCALE
    return Box(q.numerator//q.denominator,ceil(q.numerator,q.denominator))


def hull(a,b):
    return Box(box(a).lo,box(b).hi)


def dot(a,b):
    return sum((x*y for x,y in zip(a,b,strict=True)),box(0))


def det(a):
    n=len(a)
    if n==1:return a[0][0]
    result=box(0)
    for j,v in enumerate(a[0]):
        if v.lo or v.hi:
            minor=[[x for k,x in enumerate(row) if k!=j] for row in a[1:]]
            result+=(-1)**j*v*det(minor)
    return result


def read():
    with ZipFile(ROOT/'basis/Zeigerstudie.zip') as z:
        prev=z.read('basis/Pulsvergleich.zip')
    with ZipFile(BytesIO(prev)) as z:
        n19=z.read('basis/N19.zip')
    with ZipFile(BytesIO(n19)) as z:
        data=json.loads(z.read('Paar.json')); old=json.loads(z.read('basis/zweig.json'))
        windows=json.loads(z.read('basis/vorversuch.json'))['CST']['x_fenster']
    c=data['case']; f=data['fixed_rounded']
    y={int(k):hull(*iv) for k,iv in f['Y'].items()}
    w={int(k):hull(*iv) for k,iv in f['w'].items()}
    future=old['future']; rel=set(map(tuple,old['order']))
    rel.update((i,j) for i in (0,1,2) for j in (15,16))
    rel.add((15,16));rel.update((i,j) for i in (15,16) for j in future)
    rel.update((i,17) for i in c['old_past_of_h'])
    rel.update((i,18) for i in c['old_past_of_r'])
    assert c['h_before_r'];rel.add((17,18))
    rel.update((i,j) for i in (17,18) for j in c['old_future_of_h_and_r'])
    assert all((i,k) in rel for i,j in rel for l,k in rel if j==l)
    code=(1,-9,16,-8)
    edges={}
    for i,j in rel:
        count=sum((i,k) in rel and (k,j) in rel for k in y)
        edges[i,j]=code[count] if count<len(code) else 0
    e=hull(Q(1,6)-Q(1,2**22),Q(1,6)+Q(1,2**22))
    windows=[tuple(map(Q,p)) for p in windows]
    def clock(j):
        vals=[(t+2-v)/(4-v) for t in (Q(y[j].lo,SCALE),Q(y[j].hi,SCALE))
              for v in (Q(e.lo,SCALE),Q(e.hi,SCALE))]
        return hull(min(vals),max(vals))
    marked=[]
    for low,high in windows:
        possible=[j for j in y if w[j].hi>0 and not
                  (clock(j).hi<low*SCALE or clock(j).lo>high*SCALE)]
        (j,)=possible
        assert w[j].lo>0 and low*SCALE<=clock(j).lo<=clock(j).hi<=high*SCALE
        marked.append(j)
    assert marked==[16,18]
    return y,w,rel,edges,e,windows
