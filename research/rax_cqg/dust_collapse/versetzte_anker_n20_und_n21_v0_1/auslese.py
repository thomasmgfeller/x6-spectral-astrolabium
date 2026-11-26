from intervall import I,span
from ordnungen import coefficients
from fractions import Fraction as F


def target(Y):
    return Y[3]+(Y[7]-Y[3])*I.enclose(F(31,64),F(33,64))


def affine(c,Y,W,t):
    # Extremize in the shared clock t at its endpoints before combining intervals.
    def at(k):
        return sum((v*W[j]*(Y[j]-I(k,k)) for j,v in c.items()),I.enclose(0))
    return span([at(t.l),at(t.h)])


def screen(records,order,Y,W):
    window=target(Y);counts={};passed=[];unresolved=[]
    inner_left=Y[3]+(Y[7]-Y[3])*I.enclose(F(31,64))
    inner_right=Y[3]+(Y[7]-Y[3])*I.enclose(F(33,64))
    assert all(inner_left.h<Y[j].l<=Y[j].h<inner_right.l for j in (16,18))
    groups={}
    for p,f,markers in records:
        l=max(window.l,max(Y[i].l for i in p))
        h=min(window.h,min(Y[j].h for j in f))
        if l>h:continue
        # All group counts reported as compatible require a common strict interior.
        guaranteed=max(inner_left.h,max(Y[i].h for i in p))<min(inner_right.l,min(Y[j].l for j in f))
        assert guaranteed
        key=tuple(sorted(f))
        section=I(l,h);coeff=coefficients(order,f)
        residual=affine(coeff,Y,W,section)
        groups.setdefault(key,[]).append(residual)
        passed.append((p,f,markers))
        if residual.haszero():unresolved.append((p,f,markers))
    for k,v in groups.items():
        counts[k]=(len(v),span(v))
    return counts,passed,unresolved
