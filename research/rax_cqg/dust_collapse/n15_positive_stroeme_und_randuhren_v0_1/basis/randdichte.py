"""Construct a positive interior saddle on a different future collar with certified real roots."""
from fractions import Fraction as F
from intervall import Box, box, SCALE
from pruefung import I, P, FUT, support, variation
from gegenprobe import read_geometry, ends


def sparse_motifs():
    rows={}
    for code in support.catalogue():
        rel,edges,_=read_geometry(code)
        before={j:{i for i in I if (i,j) in rel} for j in I}
        after={i:{j for j in I if (i,j) in rel} for i in I}
        for i in I:
            if before[i] or len(after[i])!=2 or any(after[j] for j in after[i]):
                continue
            j,k=sorted(after[i],key=lambda v:len(before[v]))
            if before[j]!={i} or len(before[k])!=2:
                continue
            assert [edges.get((i,v),0) for v in FUT]==[16,-8,0,0]
            assert edges[i,j]==edges[i,k]==1
            assert [edges.get((q,k),0) for q in P]==[0,0,-8,16]
            assert all(edges[q,k]==1 for q in before[k])
            for v in (j,k):
                assert [edges.get((v,q),0) for q in FUT]==[1,-9,16,-8]
            rows[str(code)]={'minimal':i,'one_predecessor_max':j,'two_predecessor_max':k}
            break
    return rows


def construct(e, return_fields=False):
    code=1767356
    relation,edges,mask=read_geometry(code)
    y={0:box(-5),1:box(-4),2:box(-3),3:e-2,**{v:box(v-5) for v in FUT}}
    h={}
    # For a quadratic node the sign fixes the square-root branch before its density is evaluated.
    plus_root={11:1,12:-1,13:-1,14:-1}
    for j in I:
        row=[(i,b) for (i,v),b in edges.items() if v==j]
        deg=sum(b for i,b in row)
        base=y[3]
        first=sum(b*(y[i]-base) for i,b in row)
        constant=19+sum(b*(y[i]-base).square() for i,b in row)
        if deg==0:
            assert first.lo>0 and j not in plus_root
            y[j]=base+constant/(2*first)
            h[j]=first
        else:
            rad=first.square()-deg*constant
            assert rad.lo>0
            signed=plus_root[j]*rad.sqrt_nonnegative_part()
            y[j]=base+(first+signed)/deg
            h[j]=-signed
    assert all(y[i].hi < y[j].lo for i,j in relation)
    # Solve for density per unit of common future density. This is exactly linear.
    u=dict.fromkeys(FUT,box(1))
    for j in reversed(I):
        outgoing=sum(b*u[v]*(y[v]-y[j]) for (i,v),b in edges.items() if i==j)
        u[j]=(-outgoing)/h[j]
        assert u[j].lo>0
    assert all(u[6].lo>u[j].hi for j in I if j!=6)
    assert (u[6]*F(1,8)).lo>SCALE
    accepted=F(1,64)
    assert max((u[j]*accepted).hi for j in I)<SCALE
    w={j:val*accepted for j,val in u.items()}
    # Every interior ideal, direct sum of signed edge currents for p=-Q.
    charges=[]
    for n in range(1<<len(I)):
        region=set(P)|{j for k,j in enumerate(I) if n & (1<<k)}
        if any(i not in region and j in region for i,j in relation):
            continue
        cut=sum(b*w[j]*(y[i]-y[j]) for (i,j),b in edges.items() if i in region and j not in region and j in w)
        charges.append(cut)
    assert all(v.lo>0 for v in charges)
    shared=Box(max(v.lo for v in charges),min(v.hi for v in charges))
    if return_fields:
        return relation,edges,y,w,shared
    # Check the unreduced square sums and gradients using the original edge generator.
    all_y=[y[v] for v in range(15)]
    all_w=[w.get(v,box(F(1,8))) for v in range(15)]
    raw=variation.edges(mask,15)
    for j in I:
        norm=19+sum(b*(all_y[i]-all_y[j]).square() for i,v,b in raw if v==j)
        grad=sum(b*all_w[j]*(all_y[i]-all_y[j]) for i,v,b in raw if v==j)
        grad+=sum(b*all_w[v]*(all_y[v]-all_y[j]) for i,v,b in raw if i==j)
        assert norm.lo<=0<=norm.hi and grad.lo<=0<=grad.hi
    signs=[b for (i,j),b in edges.items() if i in P and j in I]
    return {'Y_inner':{str(j):ends(y[j]) for j in I},
            'w_inner_new':{str(j):ends(w[j]) for j in I},
            'w6_original_future_1_8':ends(u[6]*F(1,8)),
            'positive_future_density_upper_endpoint':ends(box(1)/u[6]),
            'cut_charge_19Delta_p_new':ends(shared),'ideals_checked':len(charges),
            'positive_and_negative_inlet_edges_p':[sum(b<0 for b in signs),sum(b>0 for b in signs)]}


def run():
    mid=F(1,6)
    width=F(1,2**22)
    e=Box.hull(mid-width,mid+width)
    assert support.DELTA[0]*(mid-width) > support.WINDOWS[1][0]
    assert support.DELTA[1]*(mid+width) < support.WINDOWS[1][1]
    return {'sparse_motifs':sparse_motifs(),'changed_future_case':{'code':1767356,
            'future_density':'1/64','right_window_subinterval_e':list(map(str,(mid-width,mid+width))),
            'at_midpoint':construct(box(mid)),'over_subinterval':construct(e)}}
