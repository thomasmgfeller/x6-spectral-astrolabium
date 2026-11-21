"""Auxiliary follow-up: distinguish the original cells and challenge that rule."""
from fractions import Fraction as Q
import json

from strom import (B, I, K, M, ORDER, P, add, box, fields, flux, ideals, mul,
                   scale, src, sub, total)

SEAM = {5, 11}
HIDDEN = (4, 12, 13)


def hidden_axis_pair(radius):
    # Use the first viable three hidden density coordinates in canonical
    # order. The cofactor scale, clocks, cell width and preparation are fixed.
    y, old, _ = fields(radius)
    e = box(Q(-1,4), radius)
    dur = sub(box(4), e)
    u = {v:box(src.CENTER[v], radius) for v in I}
    f = {v:box(0) for v in I}
    for chain in src.local_geometry()[1]:
        bounds = [box(0)] + [scale(Q(1,2),add(u[i],u[j])) for i,j in zip(chain,chain[1:])] + [box(1)]
        for v,a,b in zip(chain,bounds,bounds[1:]):
            f[v] = add(f[v],scale(Q(1,2),sub(b,a)))
    C = {v:add(box(1),scale(Q(1,19),total(
        scale(b,src.square(sub(y[i],y[v]))) for (i,j),b in B.items() if j==v))) for v in HIDDEN}
    a,b,c = HIDDEN
    d = {v:scale(src.COFACTOR_SCALE,sub(C[left],C[right]))
         for v,left,right in ((a,b,c),(b,c,a),(c,a,b))}
    assert SEAM.isdisjoint(d)
    # Sum d = C.d = 0 for arbitrary C (antisymmetry of the cofactor
    # polynomial). Check its monomial coefficients without sampling clocks.
    linear, quadratic = {}, {}
    for v,left,right in ((a,b,c),(b,c,a),(c,a,b)):
        for other, sign in ((left,1),(right,-1)):
            linear[other]=linear.get(other,0)+sign
            power=tuple(sorted((v,other)))
            quadratic[power]=quadratic.get(power,0)+sign
    assert all(n==0 for n in (*linear.values(),*quadratic.values()))
    branches=[]
    for sgn in (-1,1):
        w=dict(old[0])
        for v in I:
            perturb=add(scale(sgn,d.get(v,box(0))),box(0,radius))
            assert max(map(abs,perturb)) < f[v][0]/100
            w[v]=mul(scale(M,dur),add(f[v],perturb))
        branches.append(w)
    return y, branches


def audit():
    initial=set(P)
    _, central_w, _=fields(0)
    _, w, _=fields(src.RADIUS)
    # Unshifted centre value in the existing preparation, in w/Delta units.
    thresholds={v:(central_w[0][v][0]+central_w[1][v][0])/2 for v in K}
    for v, threshold in thresholds.items():
        left,right=w[0][v],w[1][v]
        assert (left[1]<threshold<right[0]) or (right[1]<threshold<left[0])
    assert thresholds[5] == Q(17,160)
    frontier_rows=[]
    for ideal in ideals():
        maximal=sorted(i for i in ideal if not any((i,j) in ORDER for j in ideal))
        separating=sorted(set(maximal)&set(K))
        frontier_rows.append(dict(inner=sorted(ideal-initial), maximale_ereignisse=maximal,
                                  trennende_dichteachsen=separating))
    yc, wc=hidden_axis_pair(0)
    yh, wh=hidden_axis_pair(src.RADIUS)
    charges=[flux(initial,yh,x) for x in wh]
    centres=[flux(initial,yc,x)[0] for x in wc]
    assert charges[0][0]>0>charges[1][1]
    assert all(lo<=p<=hi for (lo,hi),p in zip(charges,centres))
    return {'originale_pakete':{
        'w5_durch_Delta_schwelle':str(thresholds[5]),
        'w5_durch_Delta_bereiche':[list(map(str,branch[5])) for branch in w],
        'ideale_mit_trennender_lokaler_dichte':sum(bool(row['trennende_dichteachsen']) for row in frontier_rows),
        'alle_linken_schnittraender':frontier_rows},
        'zusaetzliches_gegenpaar':{
        'veraenderte_achsen':HIDDEN,'gleiche_schnittachsen':sorted(SEAM),
        'p_anfang_zentren':list(map(str,centres)),
        'p_anfang_bereiche':[list(map(str,q)) for q in charges],
        'uebernommene_cofaktorskala':str(src.COFACTOR_SCALE),
        'wirkung_und_gesamtdichte':'identisch auf beiden gesamten gepaarten Zellen',
        'auslese_auf_schnittkoordinaten_und_zukunft':'gleiche bedingte Amplituden gegen jede gemeinsame beschraenkte Testfunktion'}}


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Bitte ohne -O ausführen.')
    print(json.dumps(audit(),indent=2,ensure_ascii=False))
