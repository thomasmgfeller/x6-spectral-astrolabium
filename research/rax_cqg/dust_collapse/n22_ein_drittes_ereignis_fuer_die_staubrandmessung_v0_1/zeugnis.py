"""Rational Krawczyk/contraction certificate for all of the free field equations."""
from fractions import Fraction as F
from pathlib import Path
import json,subprocess,sys
from ordnung22 import structure

FREE=(4,5,6,11,12,13,14,15,16,17,18,19,20,21)
PROBES=((15,16),(16,18),(17,18),(18,7))
ROOT=Path(__file__).resolve().parent

class B:
    def __init__(self,l=0,h=None):
        self.lo=F(l);self.hi=F(h) if h is not None else self.lo
        assert self.lo<=self.hi
    def __add__(self,v):
        if isinstance(v,B):return B(self.lo+v.lo,self.hi+v.hi)
        return B(self.lo+v,self.hi+v)
    __radd__=__add__
    def __neg__(self):return B(-self.hi,-self.lo)
    def __sub__(self,v):return self+(-v)
    def __rsub__(self,v):return -self+v
    def __mul__(self,v):
        if isinstance(v,B):
            k=[a*b for a in (self.lo,self.hi) for b in (v.lo,v.hi)]
            return B(min(k),max(k))
        lo=self.lo*v;hi=self.hi*v
        return B(lo,hi) if v>=0 else B(hi,lo)
    __rmul__=__mul__
    def mid(self):return (self.lo+self.hi)/2
    def mag(self):return max(abs(self.lo),abs(self.hi))
    def to_json(self):return [str(self.lo),str(self.hi)]


def inverse(matrix):
    n=len(matrix)
    a=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if a[i][j])
        a[pivot],a[j]=a[j],a[pivot]
        c=a[j][j];a[j]=[v/c for v in a[j]]
        for i in range(n):
            if i==j or not a[i][j]:continue
            c=a[i][j];a[i]=[v-c*t for v,t in zip(a[i],a[j])]
    assert all(a[i][j]==int(i==j) for i in range(n) for j in range(n))
    return [row[n:] for row in a]


def certify(d,proposal):
    case=proposal['case'];row=proposal['row']
    rel,c=structure(set(d['order']),row,case[0])
    for edge in PROBES:c[edge]=c.get(edge,0)-F(1,10**11)
    pos=[i for i in FREE if i not in (15,17,20) and (i!=21 or case[1]=='+')]
    drift=F(proposal.get('drift','0'));strength=F(proposal.get('source','0'))
    collar=json.loads(subprocess.check_output([sys.executable,'-B',str(ROOT/'eichpunkt.py'),str(drift),str(strength)]))
    sy=[B(v) for v in proposal['y']];sw=[B(v) for v in proposal['w']]
    for j in (0,1,2,3,7,8,9,10):sy[j],sw[j]=[B(*a) for a in collar[str(j)]]
    for j in set(FREE)-set(pos):assert sw[j].lo==sw[j].hi==0
    # Clock variables followed by positive weights; density equations followed by clocks.
    radii=[F(1,10**7)]*len(FREE)+[F(1,10**8)]*len(pos)
    ly=sy.copy();lw=sw.copy()
    for i,j in enumerate(FREE):ly[j]=sy[j]+B(-radii[i],radii[i])
    for i,j in enumerate(pos):lw[j]=sw[j]+B(-radii[len(FREE)+i],radii[len(FREE)+i])

    def field(y,w):
        D=[B(19) for _ in y];G=[B() for _ in y]
        # Cross block dG_i/dw_j; clock block dG_i/dY_j is symmetric.
        cross=[[B() for _ in y] for _ in y];clock=[[B() for _ in y] for _ in y]
        for (i,j),k in c.items():
            h=y[j]-y[i];p=k*h;v=k*w[j]
            D[j]+=p*h;G[i]+=w[j]*p;G[j]-=w[j]*p
            cross[i][j]+=p;cross[j][j]-=p
            clock[i][j]+=v;clock[j][i]+=v;clock[i][i]-=v;clock[j][j]-=v
        D[16]-=strength
        jac=[[-2*cross[i][j] for i in FREE]+[B() for _ in pos] for j in pos]
        jac.extend([[clock[i][j] for j in FREE]+[cross[i][j] for j in pos] for i in FREE])
        return [D[j] for j in pos]+[G[i] for i in FREE],jac

    value,J=field(sy,sw);_,Jbox=field(ly,lw);n=len(radii)
    pre=inverse([[v.mid() for v in row] for row in J])
    beta=q=F(0)
    for i in range(n):
        beta=max(beta,sum((pre[i][k]*value[k] for k in range(n) if pre[i][k]),B()).mag()/radii[i])
        norm=F(0)
        for j in range(n):
            error=int(i==j)-sum((pre[i][k]*Jbox[k][j] for k in range(n) if pre[i][k]),B())
            norm+=error.mag()*radii[j]/radii[i]
        q=max(q,norm)
    assert beta+q<1,(float(beta),float(q))
    assert all(ly[i].hi<ly[j].lo for i,j in rel)
    assert all(0<lw[j].lo<=lw[j].hi<1 for j in pos)
    # The N19 time reference is exact; use the enclosure for Y3 for a uniform bound.
    def x(j):
        a=ly[j]-ly[3];b=ly[7]-ly[3];assert b.lo>0
        vals=[v/t for v in (a.lo,a.hi) for t in (b.lo,b.hi)]
        return B(min(vals),max(vals))
    norm=[x(j) for j in (19,20,21)]
    zero=B()
    steps=[ly[16]-ly[15]+ly[18]-ly[16],ly[18]-ly[17],ly[7]-ly[18]]
    assert all(v.mag()<8 for v in steps+[ly[16]-ly[15],zero])
    # The q_a start at zero and follow the four probe gaps. Thus all three
    # pointer momenta vanish exactly and the device kinetic gradients vanish.
    up=lambda v:str(F(-(-v.numerator*10**12//v.denominator),10**12))
    return {'case':case,'row':row,'normalized_clocks':[v.to_json() for v in norm],
            'inside_window':[v.lo>=F(31,64) and v.hi<=F(33,64) for v in norm],
            'below_window':[v.hi<F(31,64) for v in norm],'above_window':[v.lo>F(33,64) for v in norm],
            'upper_beta':up(beta),'upper_q':up(q),'upper_sum':up(beta+q),
            'equations':n,'strict_relations':len(rel),'positive_weights':len(pos),
            'collar':collar,'upper_all_pointer_magnitudes':up(max(v.mag() for v in steps+[ly[16]-ly[15]]))}
