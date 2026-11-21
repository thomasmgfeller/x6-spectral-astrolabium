"""Rational enclosures for descent, whole packets and the two-mode seam."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json

from anschluss import old,check_caps,check_covariance,classical,one_birth
from optimal import compare

ROOT=Path(__file__).resolve().parent
H=old.H


def algebra():
    # Gaussian integer matrices. With r=exp(-ia), J=2E-I in flat/odd coordinates
    # equals sin(a)*S + cos(a)*C. Check S²=C²=I and SC+CS=0 exactly.
    S=((-1,0),(0,1))
    C=((0,-1j),(1j,0))
    identity=((1,0),(0,1))
    def mult(a,b):
        return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    assert mult(S,S)==mult(C,C)==identity
    sc,cs=mult(S,C),mult(C,S)
    assert all(sc[i][j]==-cs[i][j] for i in range(2) for j in range(2))
    assert all(C[i][j]==complex(C[j][i]).conjugate() for i in range(2) for j in range(2))


def bounds(data):
    ref=Q(data['D_referenz'])
    arg=H*ref
    cos_ref=1-arg**2/2
    central={}
    error_r={}
    error_two={}
    error_quot={}
    jump={}
    for name,entry in data['pakete'].items():
        phase=tuple(map(Q,entry['staubphase']))
        cone=1-(phase[1]-phase[0])**2/8
        tmax=max(abs(Q(v)) for v in entry['theta'])
        jump[name]=cone*(1-tmax**2/2)
        d=ref+Q(entry['D7_zentrum_minus_referenz'])
        central[name]=d
        # Per-packet mass, pointwise in open future data, from the symmetric
        # 15-axis average in PR 345. The common entrance density stays integrated.
        e=Q(data['optimum_flache_randpaarung']['paketfehler'][name]['amplitudenfehler_max_je_paketmass'])
        sinc1=1-(H*d)**2/6
        sinc2=1-(H*d/2)**2/6
        assert min(cone,sinc1,sinc2)>Q(99,100)
        error_r[name]=2*e/(cone*sinc1)
        error_two[name]=2*e/(cone*sinc2)
        # For y/x = R E f / R f evaluated on each spectator fiber.
        error_quot[name]=e*(1+1/sinc1)/(cone*sinc1-e)
    dt=H*(central['positiv']-central['negativ'])
    largest=max(abs(H*d/2) for d in central.values())
    ideal_null=(cos_ref*dt/4,dt/(4*(1-largest**2/2)**2))
    null_real=old.add(ideal_null,old.box(0,sum(error_quot.values())))
    assert null_real[0]>Q(29014,10**16)
    # The conditional centroid half-bin means have common sinc(hD/2), so
    # their normalized port still reads (1+sin(h*(D-D*)))/2.
    angles=[H*(central[s]-ref) for s in ('positiv','negativ')]
    sin_error=sum(abs(t)**3/6 for t in angles)/2
    two=old.box(dt/2,sum(error_two.values())+sin_error)
    assert sum(error_r.values())<Q(466,10**20)
    assert two[0]>Q(58029,10**16)
    assert min(jump.values())>Q(99,100)
    return {'h':H,'D_stern':ref,'cos_hD_stern_untere_schranke':cos_ref,
            'ein_modus_spurabstand_max':sum(error_r.values()),
            'zwei_moden_P_differenz':two,'fluss_in_nullraum_kommutatornorm':(cos_ref/2,Q(1,2)),
            'restnorm_RE_bei_flachem_und_linearem_modus':(cos_ref/4,Q(1,4)),
            'normierter_glatter_nullzeuge_RE_betragsquadrat':(3*cos_ref**2/16,Q(3,16)),
            'Re_RE_zeugnis_aus_ganzen_paketen':null_real,'sprung_min_je_paketmass':jump,
            'D_zentren':central,'fehler_ein_modus':error_r,'fehler_zwei_moden':error_two}


def run():
    contract=(ROOT/'pruefvertrag.json').read_bytes()
    assert sha256(contract).hexdigest()==(ROOT/'pruefvertrag.sha256').read_text().split()[0]
    data=json.loads((ROOT/'basis/port/ergebnis.json').read_text())
    assert data['typ']==375841 and data['physikalisches_randprodukt']=='HOLD'
    # Recompute the prior intervals and the error envelope used in this study.
    regions=old.run()['pakete']
    for k,v in regions.items():
        assert json.loads(json.dumps(v,default=str))==data['pakete'][k]
    paired,_=old.centers()
    assert json.loads(json.dumps(compare(paired,regions),default=str))==data['optimum_flache_randpaarung']
    algebra()
    return {'typ':375841,'anschluesse':check_caps(),'ein_geburt':one_birth(),'kovarianz':check_covariance(),
            'klassische_dichtevariationen_C':classical(),'abstieg_und_kontrast':bounds(data),
            'abstieg_flache_naht':'FAIL','abschluss_flat_und_antisymmetrisch':'PASS',
            'physikalische_constraints_und_paarung':'HOLD'}


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(run(),indent=2,ensure_ascii=False,default=str))
