"""Exact polynomial identity tests over an interpolation grid, with degree bounds."""
from fractions import Fraction as Q
from itertools import product

from basis import density_translation_375841 as ref


def identities():
    _,_,b=ref.local_geometry()
    # Incoming support of the two earliest inner events, and outgoing hidden
    # support of the seam. These are structural assumptions of the decoder.
    assert [b[i,4] for i in ref.PAST]==[b[i,6] for i in ref.PAST]==[-8,16,-9,1]
    assert {j:k for (i,j),k in b.items() if i==5 and j in ref.INNER and k}=={14:1}
    assert {j:k for (i,j),k in b.items() if i==11 and j in ref.INNER and k}=={12:1,13:-9}
    assert all(b[i,j]==0 for i in ref.PAST for j in ref.FUTURE)
    assert (5,11) not in b and (11,5) not in b
    assert not any(i in ref.FUTURE and j in ref.INNER for i,j in b)
    # Treat C4,C6,C12,C13,r,t as independent formal variables.
    # Each residual below has individual degree <=2 in each C and <=2 in
    # r,t (outgoing derivative). Three points on each axis are unisolvent.
    count=0
    for c4,c6,c12,c13,r,t in product((-1,0,1),repeat=6):
        a=c4-c6
        h=(c12-c6)*r+(c13-c6)*t
        d4,d6,d12,d13=-h,h-a*(r+t),a*r,a*t
        assert d4+d6+d12+d13==0
        assert c4*d4+c6*d6+c12*d12+c13*d13==0
        assert (-t)*d12+r*d13==0
        count+=1
    return {'interpolationsgitter':count,'grad_je_variable_hoechstens':2,
            'summendichte_wirkung_erste_schnittantwort':'identisch',
            'nachfolger_im_inneren':{'5':[14],'11':[12,13]}}
