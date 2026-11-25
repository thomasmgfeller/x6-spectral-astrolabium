"""Conservative intervals for the LTB control and for availability of real N15 markers."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys
from kontrollen import corner, FACTORS
from leser import classify

ROOT=Path(__file__).resolve().parent
SCALE=10**18

def root_bracket(q,n):
    assert q>=0
    inf=q.numerator*SCALE**n//q.denominator
    if n==2:
        root=isqrt(inf)
    else:
        lo,hi=0,1
        while hi**n<=inf:hi*=2
        while lo+1<hi:
            mid=(lo+hi)//2
            if mid**n<=inf:lo=mid
            else:hi=mid
        root=lo
    a=F(root,SCALE)
    return a,a if a**n==q else F(root+1,SCALE)

def surface_at(m,t):
    """t is the local proper-time offset from T*; R³=1000(1−sqrt(M)/8−(3/2)t sqrt(2M/1000))²."""
    s,exact=root_bracket(m,2)
    assert s==exact
    b=root_bracket(2*m/1000,2)
    f=sorted(1-s/8-F(3,2)*t*v for v in b)
    assert f[0]>0
    return root_bracket(1000*f[0]**2,3)[0],root_bracket(1000*f[1]**2,3)[1]

def ltb_case(m,f,hard):
    e,v,theta=corner(f,hard)
    lo,hi=surface_at(m,e)
    dt=v-e
    # On R>=7, |dR/dT| <= 1 + sqrt(2m(a)/R) < 3.
    # First-exit argument: even this worst-case speed cannot reach R=7.
    assert lo-3*dt>7 and 2*m/7<4
    if hi<=dt/theta:
        status='JA'
    elif lo-3*dt>dt/theta:
        status='NEIN'
    else:
        status='UNBESTIMMT'
    return status

def ltb():
    out={}
    for m in (F(1,4),F(1),F(4)):
        values={str(f):[ltb_case(m,f,hard) for hard in (True,False)] for f in FACTORS}
        out[str(m)]={'R_Tstar':list(map(str,surface_at(m,F(0)))),
                     'ecken':values,'klasse':{k:classify(*v) for k,v in values.items()}}
    return out

def cst():
    sys.path.insert(0,str(ROOT/'basis/schale'))
    from schicht import inside_layer,Box
    data=json.loads((ROOT/'basis/n15_ergebnisse.json').read_bytes())
    old={k:tuple(map(F,b)) for k,b in data['geometry']['normalized_clock_intervals'].items()}
    assert len(old)==15 and data['geometry']['type']==1767356
    assert data['physical_NOT_RUN']==60
    end=tuple(5*v/3 for v in root_bracket(F(5),2))
    windows=[]
    for event in (0,1):
        off=[corner(8,h)[event] for h in (True,False)]
        xs=[F(1,2)+t/d for t in off for d in end]
        windows.append((min(xs),max(xs)))
    def distance(w,row):
        lo,hi=row
        return max(w[0]-hi,lo-w[1],F(0))
    min_gaps=[min(distance(w,b) for b in old.values()) for w in windows]
    assert min(min_gaps)>0
    refined=inside_layer(Box.hull(F(1,6)-F(1,2**22),F(1,6)+F(1,2**22)))
    assert refined['old_ideals']==23 and len(refined['candidates'])==9 and not refined['unresolved']
    rows=[tuple(map(F,r['relative_time'])) for r in refined['candidates']]
    slab=(min(w[0] for w in windows),max(w[1] for w in windows))
    gap=min(distance(slab,b) for b in rows)
    assert gap>0
    return {'stresstest_faktor':8,'x_fenster':[list(map(str,w)) for w in windows],
            'anzahl_archivuhren':len(old),'archivuhren_in_fenstern':[0,0],
            'minimale_abstaende_alt_x':list(map(str,min_gaps)),
            'alte_ideale':23,'wurzelintervalle':9,
            'abstand_minimales_positives_neuereignis_zum_zeitband_x':str(gap),
            'auslese':'MISSING_EXPOSURE','P3':'HOLD_NOT_ELIGIBLE','NOT_RUN':60}
