"""Conditional inversion. W=w/Delta; H in this file is Delta*d²S/dT²."""
from fractions import Fraction as Q

from basis import density_translation_375841 as ref

P,I,F=ref.PAST,ref.INNER,ref.FUTURE
_,_,B=ref.local_geometry()
IDEAL=set(P+(4,5,6,11))


def initial_readout(y, known_w, total_inner, E5, E11, curvature11=None, cut_current=None):
    """Supply E5,E11 and exactly one additional response, plus the listed side data.

    known_w contains the two seam densities and the four future densities.
    The clocks y of the whole history and its actual inner density sum are inputs.
    """
    if (curvature11 is None)==(cut_current is None):
        raise ValueError('Exactly one second response is needed.')
    def inner_outgoing(s,E):
        incoming=known_w[s]*sum(b*(y[i]-y[s]) for (i,j),b in B.items() if j==s)
        future=sum(B.get((s,j),0)*known_w[j]*(y[s]-y[j]) for j in F)
        return incoming-future-19*E
    j5,j11=inner_outgoing(5,E5),inner_outgoing(11,E11)
    w14=j5/(y[5]-y[14])
    a=y[11]-y[12]
    b=-9*(y[11]-y[13])
    if curvature11 is not None:
        incoming_count=sum(k for (i,j),k in B.items() if j==11)
        l11=(-19*curvature11-known_w[11]*incoming_count
             -sum(B.get((11,j),0)*known_w[j] for j in F))
        w13=(j11-a*l11)/(9*(y[13]-y[12]))
        w12=l11+9*w13
    else:
        def row(j):
            return sum(B.get((i,j),0)*(y[i]-y[j]) for i in IDEAL)
        q=19*cut_current-sum(row(j)*known_w[j] for j in F)-row(14)*w14
        c,d=row(12),row(13)
        det=a*d-b*c
        if not det:
            raise ValueError('The flux response does not add an independent equation.')
        w12,w13=(d*j11-b*q)/det,(a*q-c*j11)/det
    w_early=total_inner-known_w[5]-known_w[11]-w12-w13-w14
    def k(v):
        return sum(B[i,v]*(y[i]-y[v]) for i in P)
    assert k(4)==k(6)
    value=(k(4)*w_early+k(5)*known_w[5]+k(11)*known_w[11]
           +k(12)*w12+k(13)*w13+k(14)*w14)/19
    return value,(w_early,w12,w13,w14)


def bounds():
    # Global monotone tube has u13-u12,u14-u5 >= 1/5-2/64.
    # Both real offset windows are within |delta|<=3/32 and Delta>1/4.
    gap=(4-Q(3,8))*(Q(1,5)-Q(2,64))
    assert gap>0
    from schnittimpulse import coordinates,SHIFT,sc,sub,mul,total
    determinants={}
    for name,shift in [('alte_zellen',0),('neue_zellen',SHIFT)]:
        _,y,_,_,_=coordinates(ref.RADIUS,shift)
        a=sub(y[11],y[12])
        b=sc(-9,sub(y[11],y[13]))
        def row(j):
            return total(sc(B.get((i,j),0),sub(y[i],y[j])) for i in IDEAL)
        det=sub(mul(a,row(13)),mul(b,row(12)))
        assert det[1]<0
        determinants[name]=list(map(str,det))
    return {'uhrluecke_Y13_minus_Y12_und_Y14_minus_Y5_untere_schranke':str(gap),
            'determinantenvariante_mit_gesamtfluss_auf_den_Zellen':determinants,
            'zusaetzliche_eingaben':'Uhrprofil, zwei Schnittdichten, Zukunftsdichten und tatsächliche Summe der sieben inneren Dichten',
            'zweite_antwort':'Krümmung bei 11, alternativ geprüfter schnittübergreifender Fluss bei invertierbarem Zweizeilensystem'}

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    import json
    print(json.dumps(bounds(),ensure_ascii=False,indent=2))
