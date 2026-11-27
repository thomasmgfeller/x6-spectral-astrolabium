"""Validate one 32-equation mixed boundary solution and the inherited reader."""
from decimal import Decimal
from fractions import Fraction as F
from algebra import mid, inv
from feldroehre import absmax
from impulsabgleich import coords, setcoords
from leseregel import digits, decode, ERROR, REFERENCE
from paarstudie import coefficients, upper
from quelle import box, hull, SCALE
from randversuch import build, dot
from versuch import variables, system, LATE


def certify(seed, collar, source, coeff, free, rel, goals, pair, late):
    axes = variables(free)
    fixed_y, fixed_w = build(seed, collar)
    def evaluator(cast, convert):
        edges = coefficients(coeff, convert)
        early = list(map(convert, goals))
        targets = {i: convert(v) for i, v in late.items()}
        def evaluate(y, w):
            return system(y, w, convert(source), edges, free, axes, early, pair, targets, cast)
        return evaluate

    decimal_system = evaluator(Decimal, mid)
    base_y, base_w = list(map(mid, fixed_y)), list(map(mid, fixed_w))
    x = coords(base_y, base_w, axes)
    for _ in range(8):
        values, jac, _ = decimal_system(*setcoords(base_y, base_w, axes, x))
        x = [v-sum(a*b for a,b in zip(row,values)) for v,row in zip(x,inv(jac))]
    center = [box(F(v).limit_denominator(10**21)) for v in x]
    interval_system = evaluator(box, box)
    vals, jac, _ = interval_system(*setcoords(fixed_y,fixed_w,axes,center))
    pre = [[(j,box(v)) for j,v in enumerate(row) if v] for row in inv(jac)]
    radii = [F(1,10**10 if k == "y" else 10**11) for k,_ in axes]
    outer = [v+hull(-r,r) for v,r in zip(center,radii)]
    _, jac_outer, _ = interval_system(*setcoords(fixed_y,fixed_w,axes,outer))
    contractions, images = [], []
    for i,row in enumerate(pre):
        scaled = sum(absmax(int(i==j)-dot(row,col))*r for j,(col,r) in enumerate(zip(zip(*jac_outer),radii)))
        contractions.append(scaled/radii[i])
        images.append((scaled+absmax(dot(row,vals)))/radii[i])
    assert max(images)<1 and max(contractions)<1, (pair,source,float(max(images)))
    inner = [v+hull(-r*q,r*q) for v,r,q in zip(center,radii,images)]
    y,w = setcoords(fixed_y,fixed_w,axes,inner)
    values,_,flows = interval_system(y,w)
    assert len(values)==len(axes)==32 and all(v.contains_zero() for v in values)
    assert len(rel)==152 and all(y[i].hi<y[j].lo for i,j in rel)
    empty={15,17,20}
    assert all(0<w[i].lo<=w[i].hi<SCALE for i in set(range(22))-empty)
    assert all(w[i].lo==w[i].hi==0 for i in empty)
    assert all(absmax(y[j]-y[i])<8 for i,j in ((15,16),(15,18),(17,18),(18,7)))
    lo,hi=map(F,y[21].data())
    codes=list(digits(lo-ERROR,hi+ERROR))
    decisions=sorted({decode(n,r) for n in codes for r in range(REFERENCE-1,REFERENCE+2)})
    return dict(pair=list(pair), source=str(source),codes=[min(codes),max(codes)],decisions=decisions,
                impulses={str(j):flows[j].data() for j in LATE},upper_contraction=upper(max(contractions)),
                upper_image=upper(max(images)), y=[v.data() for v in y],w=[v.data() for v in w])
