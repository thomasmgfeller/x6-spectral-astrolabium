"""Exact necessity and sufficiency of empty-interior boundary conditions."""
from collections import Counter
from fractions import Fraction as F
import json
from felder import PAST,FUTURE,INNER,U,Z,NODES,COLLAR,Equations,filters

FREE = (*INNER,U,Z)
PIVOTS = (6,11,12,14)


def independent_weights(rel):
    past={j:{i for i,k in rel if k==j} for j in NODES}
    weights={}
    for i,j in sorted(rel):
        intermediates=[k for k in past[j] if i in past[k]]
        if len(intermediates)<4:
            weights[i,j]=(1,-9,16,-8)[len(intermediates)]
    return weights


def rational_clocks(rel):
    order=sorted(NODES,key=lambda j:(sum(k==j for i,k in rel),j))
    known={j:F(j-5) for j in PAST+FUTURE}
    known[3]=F(-11,6)
    anchors=[(-1,min(known.values())-10)]
    anchors.extend((index,known[j]) for index,j in enumerate(order) if j in known)
    anchors.append((len(order),max(known.values())+10))
    y=known.copy()
    for (a,lo),(b,hi) in zip(anchors,anchors[1:]):
        assert lo<hi
        for k in range(a+1,b):
            y[order[k]]=lo+(hi-lo)*F(k-a,b-a)
    assert all(y[i]<y[j] for i,j in rel)
    return y


def matter(h,y,w):
    return 19*sum(w.values()) + sum(b*w[j]*(y[j]-y[i])**2 for (i,j),b in h.items())


def direct_clock(h,y,w,j):
    delta=F(1,2048)
    return -(matter(h,{**y,j:y[j]+delta},w)-matter(h,{**y,j:y[j]-delta},w))/(4*delta)


def run():
    patterns=Counter()
    matrix=None
    for fu,fz in filters():
        eq=Equations(fu,fz,'shift')
        h=independent_weights(eq.rel)
        assert h=={(i,j):b for i in NODES for j,b in eq.outgoing[i]}
        rows=tuple(tuple(h.get((i,j),0) for j in FUTURE) for i in PIVOTS)
        assert rows==((-8,0,0,0),(16,-8,0,0),(-9,16,-8,0),(1,-9,16,-8))
        assert all((i,j) in eq.rel for i,j in zip(PIVOTS,FUTURE))
        matrix=rows
        additional={(i,j):b for (i,j),b in h.items() if i in FREE and j in PAST}
        if 3 in fz:
            assert additional=={(U,3):-9,(Z,3):1}
            pattern='u_and_z_before_3'
        elif 3 in fu:
            assert additional=={(U,3):1}
            pattern='only_u_before_3'
        else:
            assert additional=={}
            pattern='neither_before_3'
        patterns[pattern]+=1
        # Test sufficiency directly by differentiating the full matter action
        # for every allowed incoming collar basis vector. Linearity covers mixtures.
        y=rational_clocks(eq.rel)
        assert all(y[j]-y[i]>F(1,2048) for i,j in eq.rel)
        for k in PAST:
            w={i:F(int(i==k),8) for i in NODES}
            gradients=[direct_clock(h,y,w,j) for j in FREE]
            assert all(g==0 for g in gradients)==(k!=3 or pattern=='neither_before_3')
        for index,k in enumerate(FUTURE):
            w={i:F(int(i==k),64) for i in NODES}
            j=PIVOTS[index]
            assert direct_clock(h,y,w,j)==-8*w[k]*(y[k]-y[j])!=0
    assert sum(patterns.values())==193
    return {'free_empty':list(FREE),'future_nodes':list(FUTURE),'witness_rows':list(PIVOTS),
            'future_coefficients':[list(row) for row in matrix], 'families':dict(patterns),
            'future_weights_required':['0']*4, 'additional_condition_if_before_3':'w3=0',
            'all_zero_charge':'0','all_zero_free_clock_directions':len(FREE)}


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
