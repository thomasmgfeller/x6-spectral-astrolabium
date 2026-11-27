"""Test new necessary conditions against the four published in-window solution boxes."""
from fractions import Fraction as Q
from filter import Model, intersect
from intervall import S
from intervall import box
from fruehe_uhren import sharpen
from verfeinerung import refine
from momente import with_cuts
from ordnungen import as_relation

def controls(pair,rel,known):
    for name,sol in known.items():
        fam,side=name.split('_');future=(7,8,9,10,int(fam),21)
        model=Model(as_relation(rel,(),future))
        y,w=model.screen(pair,side,10)
        ref_y=[box(*v) for v in sol['y']]
        scale=16 if side=='light' else 1
        ref_w=[box(*v)*scale for v in sol['w']]
        for j in y:intersect(y,j,ref_y[j])
        for j in w:intersect(w,j,ref_w[j])
        sharpen(model,y,w)
        refine(model,y,w)
        # Every row containing the actual stationary point must be compatible
        # with the enclosure of its lifted monomials. Signed endpoints are exact.
        vals={(i,):(Q(v.l,S),Q(v.h,S)) for i,v in y.items()}
        vals.update({(100+i,):(Q(v.l,S),Q(v.h,S)) for i,v in w.items()})
        cuts=([0,1,0,-1,3,-2,0,0,1],[2,-4,1,0,0,2,3,0,-1])
        boxes,rows=with_cuts(model,y,w,cuts)
        for key in boxes:
            if len(key)==1:continue
            i,j=key
            ends=[a*b for a in vals[i,] for b in vals[j,]]
            vals[key]=(0 if i==j and vals[i,][0]<=0<=vals[i,][1] else min(ends),max(ends))
        for row,rhs in rows:
            assert sum(min(c*lo,c*hi) for k,c in row.items() for lo,hi in [vals[k]])<=rhs,name
