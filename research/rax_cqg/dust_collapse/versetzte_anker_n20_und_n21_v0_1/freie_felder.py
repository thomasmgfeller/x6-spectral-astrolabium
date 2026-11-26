"""Necessary conditions with a fresh solution of the source-free dust branch."""
from collections import Counter
from fractions import Fraction as F
from intervall import I,Q,span
from auslese import target,affine
from ordnungen import LAYERS

DUST=(4,5,6,11,12,13,14)
COLLAR=(0,1,2,3,7,8,9,10)


def intersection(*boxes):
    l=max(v.l for v in boxes);h=min(v.h for v in boxes)
    return I(l,h) if l<=h else None


def solve_quadratic(c,Y):
    A=sum(c.values())
    B=sum((-2*v*Y[i] for i,v in c.items()),I.enclose(0))
    C=19+sum((v*Y[i].sq() for i,v in c.items()),I.enclose(0))
    if not A:
        return None if B.haszero() else [-C/B]
    disc=B.sq()-4*A*C
    if disc.h<0:return []
    root=I(max(disc.l,0),disc.h).sqrt()
    return [(-B+sign*root)/(2*A) for sign in (-1,1)]


def structure(order,p,f):
    rel=order|{(i,19) for i in p}|{(19,j) for j in f}
    nodes=range(20)
    pred={j:{i for i in nodes if (i,j) in rel} for j in nodes}
    succ={i:{j for j in nodes if (i,j) in rel} for i in nodes}
    cin={j:{} for j in nodes};cout={j:{} for j in nodes}
    for i,j in rel:
        count=len(succ[i]&pred[j])
        if count<len(LAYERS):
            cin[j][i]=cout[i][j]=LAYERS[count]
    return pred,succ,cin,cout


def dust_pass(data,by,bw,z):
    pred,succ,cin,cout=data
    initial=dict(by);initial[19]=z
    if any(initial[i].l>=initial[j].h for i in initial for j in succ[i]&initial.keys()):
        return 'collar_order'
    states=[initial]
    for j in DUST:
        next_states=[]
        for yy in states:
            # All source-free predecessors have already been computed.
            assert pred[j]<=yy.keys()
            roots=solve_quadratic(cin[j],yy)
            if roots is None:return 'open'
            lower=max(yy[i].l for i in pred[j])
            upper=min(yy[i].h for i in succ[j]&yy.keys())
            for root in roots:
                y=intersection(I(lower,upper),root) if lower<upper else None
                if y:next_states.append({**yy,j:y})
        if not next_states:return 'dust_density_or_time'
        states=next_states
    reasons=[]
    for yy in states:
        ww=dict(bw);ww[19]=I.enclose(0)
        for j in reversed(DUST):
            assert set(cout[j])<=yy.keys() and set(cout[j])<=ww.keys()
            numerator=sum((v*ww[k]*(yy[k]-yy[j]) for k,v in cout[j].items()),I.enclose(0))
            denom=sum((v*(yy[j]-yy[k]) for k,v in cin[j].items()),I.enclose(0))
            if denom.haszero():
                if not (numerator-denom*I(0,Q)).haszero():break
                ww[j]=I(0,Q)
            else:
                value=intersection(numerator/denom,I(0,Q))
                if value is None:break
                ww[j]=value
        else:
            # 15 and 17 have zero weight in the stipulated sector. If the receiver
            # is in the future of z, allow its entire causal range up to Y7.
            parts=[]
            for k,v in cout[19].items():
                if k in (15,17):continue
                if k==18:
                    parts.append(v*I(0,by[7].h-z.l));continue
                assert k in yy and k in ww
                parts.append(v*ww[k]*(yy[k]-z))
            g=sum(parts,I.enclose(0))
            if g.haszero():return 'open'
            reasons.append('empty_clock');continue
        reasons.append('dust_weight_or_clock')
    return reasons[0] if len(set(reasons))==1 else 'branches_excluded'


def validate_dust(order,p,f,by,bw,depth):
    data=structure(order,p,f); counts=Counter()
    def visit(z,d):
        result=dust_pass(data,by,bw,z)
        if result!='open' or d==0:
            counts[result]+=1
        else:
            for piece in z.split():visit(piece,d-1)
    visit(target(by),depth)
    return counts
