"""Whole-cell proof for the first and second clock response of a fixed seam."""
from fractions import Fraction as Q
from math import isqrt
from hashlib import sha256
from pathlib import Path
import json

from basis import density_translation_375841 as ref

ROOT = Path(__file__).resolve().parent
P, I, F = ref.PAST, ref.INNER, ref.FUTURE
SEAM = (5, 11)
ORDER, PATHS, B = ref.local_geometry()
M = Q(1, 4)
ZERO = ref.box(0)
box, add, sub, mul, sc, total = ref.box, ref.plus, ref.minus, ref.times, ref.scale, ref.add_all
TRIPLES = {'pr340':(5,12,13), 'pr341':(4,12,13)}
SHIFT = Q(1,128)
RECENTRE = Q(1,8320)
SCALE = Q(1,10000)


def coordinates(radius, asymmetry):
    e = box(-Q(1,4),radius)
    dur = sub(box(4),e)
    u = {v:box(ref.CENTER[v]+{4:asymmetry,6:-asymmetry}.get(v,0),radius) for v in I}
    for v in I:
        assert max(abs(x-ref.CENTER[v]) for x in u[v]) < Q(1,64)
    assert all(u[a][1]<u[b][0] for a,b in ORDER if a in I and b in I)
    y={v:box(v-5) for v in P+F}
    y[3]=add(y[3],e)
    outer_radius=Q(1,2**20) if radius else 0
    for v in F[1:]:
        y[v]=box(v-5,outer_radius)
    y.update({v:add(add(box(-2),e),mul(dur,u[v])) for v in I})
    assert all(y[v][1]<0 for v in P+(4,5,6,11)) and all(y[v][0]>0 for v in (12,13,14)+F)
    f=dict.fromkeys(I,ZERO)
    for chain in PATHS:
        end=[ZERO]+[sc(Q(1,2),add(u[i],u[j])) for i,j in zip(chain,chain[1:])]+[box(1)]
        for v,lo,hi in zip(chain,end,end[1:]):
            f[v]=add(f[v],sc(Q(1,len(PATHS)),sub(hi,lo)))
    c={j:add(box(1),sc(Q(1,19),total(sc(b,ref.square(sub(y[i],y[j])))
        for (i,v),b in B.items() if v==j))) for j in I}
    k={v:mul(sc(Q(1,19),dur),total(sc(B[i,v],sub(y[i],y[v])) for i in P)) for v in I}
    return dur,y,f,c,k


def displacements(name, c, y):
    if name in TRIPLES:
        a,b,g=TRIPLES[name]
        return {v:sc(ref.COFACTOR_SCALE,sub(c[i],c[j]))
                for v,i,j in ((a,b,g),(b,g,a),(g,a,b))}
    if name=='ohne_gesamtinformation':
        return {4:sc(Q(1,64),c[6]),6:sc(-Q(1,64),c[4])}
    assert name=='gegenpaar'
    # r,t span the nullspace of the outgoing first derivative on the long chain.
    r=sc(B[11,13],sub(y[11],y[13]))
    t=sc(-B[11,12],sub(y[11],y[12]))
    a=sub(c[4],c[6])
    h=add(mul(sub(c[12],c[6]),r),mul(sub(c[13],c[6]),t))
    return {4:sc(-SCALE,h), 6:sc(SCALE,sub(h,mul(a,add(r,t)))),
            12:sc(SCALE,mul(a,r)),13:sc(SCALE,mul(a,t))}


def ranges(name,radius):
    new=name not in TRIPLES
    dur,y,f,c,k=coordinates(radius,SHIFT if new else 0)
    d=displacements(name,c,y)
    centre=dict(f)
    if new:
        centre[12]=add(centre[12],box(RECENTRE))
        centre[13]=sub(centre[13],box(RECENTRE))
    # Published pairs use f-d for their positive branch, the new pair uses +d.
    orient=1 if new else -1
    branches=[]
    for sgn in (orient,-orient):
        x={}
        for v in I:
            shift=add(sc(sgn,d.get(v,ZERO)),box(0,radius))
            adjust=RECENTRE if new and v==12 else -RECENTRE if new and v==13 else 0
            relative=add(shift,box(adjust))
            assert max(map(abs,relative))<f[v][0]/100
            x[v]=add(centre[v],shift)
            assert x[v][0]>0
        branches.append(x)
    diff={v:mul(sc(2*orient*M,dur),step) for v,step in d.items()}  # delta(w/Delta)
    charges=[sc(M,total(mul(k[v],x[v]) for v in I)) for x in branches]
    def dw(v):
        return diff.get(v,ZERO)
    responses={}
    for s in SEAM:
        incoming=mul(dw(s),total(sc(b,sub(y[i],y[s])) for (i,j),b in B.items() if j==s))
        outgoing=total(mul(dw(j),sc(b,sub(y[s],y[j]))) for (i,j),b in B.items() if i==s)
        hessian=add(sc(sum(b for (i,j),b in B.items() if j==s),dw(s)),
                    total(sc(b,dw(j)) for (i,j),b in B.items() if i==s))
        responses[str(s)]={'delta_w_durch_Delta':dw(s),'delta_E_ein':sc(Q(1,19),incoming),
            'delta_E_aus':sc(-Q(1,19),outgoing),'delta_E':sc(Q(1,19),sub(incoming,outgoing)),
            'delta_Delta_H':sc(-Q(1,19),hessian)}
    # Exact zeroes caused by cancellation are certified by polynomial identities
    # in identitaeten.py; naive interval subtraction need not recognize them.
    cut=set(P+(4,5,6,11))
    flux_contrast=sc(Q(1,19),total(mul(dw(j),sc(b,sub(y[i],y[j])))
        for (i,j),b in B.items() if i in cut and j not in cut))
    return charges,responses,flux_contrast


def dust_phase():
    # One shared past density; integrate the same scalar/geometry factor on
    # both sides. The bound uses the full 1% envelope around the new clocks.
    n=10**18
    root=isqrt(isqrt(3*n**4//722))
    delta=(Q(root,n),Q(root+1,n))
    assert delta[0]**4<=Q(3,722)<=delta[1]**4
    dur,y,f,c,_=coordinates(ref.RADIUS,SHIFT)
    weights={v:mul(mul(sc(M,dur),delta),mul((Q(99,100),Q(101,100)),f[v])) for v in I}
    weights.update({v:box(Q(1,8),Q(1,2**20)) for v in F})
    for j in P+F:
        c[j]=add(box(1),sc(Q(1,19),total(sc(b,ref.square(sub(y[i],y[j])))
                 for (i,k),b in B.items() if k==j)))
    past=mul((Q(3,32),Q(5,32)),total(c[j] for j in P))
    phase=sc(-Q(1,2),add(past,total(mul(weights[j],c[j]) for j in I+F)))
    assert -Q(5,8)<phase[0]<phase[1]<0
    return phase


def serial(value):
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(x) for x in value]
    return str(value)


def audit():
    from identitaeten import identities
    proof=identities()
    h=sha256((ROOT/'pruefvertrag.json').read_bytes()).hexdigest()
    assert h==(ROOT/'pruefvertrag.sha256').read_text().split()[0]
    cases={}
    for name in ('pr340','pr341','gegenpaar','ohne_gesamtinformation'):
        p0,g0,mid0=ranges(name,0)
        ps,g,mid=ranges(name,ref.RADIUS)
        assert ps[0][0]>0>ps[1][1]
        if name=='gegenpaar':
            for s in SEAM:
                for q in ('delta_w_durch_Delta','delta_E_ein','delta_E_aus','delta_E'):
                    assert g0[str(s)][q]==ZERO and g[str(s)][q][0]<=0<=g[str(s)][q][1]
                    g[str(s)][q]=ZERO
            assert g['11']['delta_Delta_H'][0]*g['11']['delta_Delta_H'][1]>0
        if name=='ohne_gesamtinformation':
            assert mid==ZERO and all(interval==ZERO for values in g.values() for interval in values.values())
            assert not any(i in SEAM+F and j in (4,6) for i,j in ORDER)
        cases[name]={'p_zentrum':[str(v[0]) for v in p0],'p_intervalle':serial(ps),
                'impulsdifferenzen_zentrum':{s:{k:str(v[0]) for k,v in vals.items()} for s,vals in g0.items()},
                'impulsdifferenzen_intervalle':serial(g),
                'differenz_gesamtfluss_Y0':serial(mid)}
    # The two inherited tests have a resolved first-derivative response.
    for name in TRIPLES:
        assert any(Q(v['delta_E'][0])*Q(v['delta_E'][1])>0
                   for v in cases[name]['impulsdifferenzen_intervalle'].values())
    phase=dust_phase()
    lower=Q(cases['gegenpaar']['impulsdifferenzen_intervalle']['11']['delta_Delta_H'][0])
    assert 1-Q(5,8)**2/2>Q(4,5)
    assert lower*Q(4,5)>Q(35,10**8)
    return {'phaseneinschluss_neue_zellen':serial(phase),
            'integrierte_kruemmungsdifferenz_re_nach_minus_i_Delta_je_Paketmass_strikt_groesser':str(Q(35,10**8)),
            'typ':ref.ORDER,'zellenhalbbreite':str(ref.RADIUS),
            'differenzen':'positives minus negatives Anfangspaket, E=dS/dT',
            'nachtraegliche_kontrolle':'ohne_gesamtinformation erlaubt verschiedene innere Dichtesummen innerhalb derselben Präparation',
            'identitaeten':proof,'faelle':cases,
            'physikalische_paarung_und_messung':'HOLD'}

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
