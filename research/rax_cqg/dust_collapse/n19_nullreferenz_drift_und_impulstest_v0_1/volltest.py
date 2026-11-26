"""Entire published equal-covariance distribution, with exact canonical atom weights."""
from fractions import Fraction as F
from itertools import product
from nullreferenz import R,STEP,SITES,TRACKS,K0,V,digit,local_decode


def run(previous,early):
    from quelle import box
    from uhrauslese import LABELS
    from proben import samples
    from staubgeraet import solve,verify
    from wege import ROUTES
    options=(-64,0,64)
    rate=F(1,9*64**2)
    probabilities={-64:rate/2,0:1-rate,64:rate/2}
    def weight(s):
        a=F(1)
        for val in s:
            a*=probabilities[val]
        return a
    support=[(s,weight(s)) for s in product(options,repeat=3)]
    assert sum(p for _,p in support)==1
    zero={'shot':'model','initial':dict.fromkeys(TRACKS,0)}
    def outcome(a,j):
        if any(x is not None and x!=j for x in a):return 'wrong'
        if None in a:return 'unresolved'
        return 'correct'
    rows=[]
    for route,k,(case,y,w),J in product(ROUTES,(F(1),K0),samples(previous,early)[0],LABELS):
        sums={key:F(0) for key in ('wrong','unresolved','correct')}
        original=sums.copy() if case=='reference' else None
        mism=box(0 if k==1 else -k)
        example=None
        for ys,py in support:
            vel=tuple(box(K0*V*j/k) for j in ys)
            st=solve(y,w,J,vel,k,mism,route)
            hist,_=verify(st,J,vel,k,mism,route,(box(0),)*3)
            clock={j:digit(st['y'][j]) for j in SITES}
            rel={j:{ch:digit(h[j]) for ch,h in zip(TRACKS,hist)} for j in SITES}
            assert all(v is not None for row in rel.values() for v in row.values())
            # All possible initial shifts are at most 112 grid steps (32 + 80).
            assert all((abs(code)+112)*STEP < 8 for row in rel.values() for code in row.values())
            labels=[local_decode(j,'model',clock[j],rel[j],zero) for j in SITES]
            sums[outcome(labels,J)]+=py
            if example is None and outcome(labels,J)=='wrong':
                example={'velocities_over_V_in_reference_units':list(ys),'labels':[str(x) if x is not None else None for x in labels]}
            for xs,px in support if original is not None else [(options,F(1))]:
                shifts=[(R*x-250*V*y)/STEP for x,y in zip(xs,ys)]
                assert all(v.denominator==1 for v in shifts)
                moved={j:{key:rel[j][key]+int(v) for key,v in zip(TRACKS,shifts)} for j in SITES}
                assert all(-8<v*STEP<8 for site in SITES for v in moved[site].values())
                if original is not None:
                    raw=[local_decode(j,'model',clock[j],moved[j],zero) for j in SITES]
                    original[outcome(raw,J)]+=px*py
                if xs==options or xs==(-64,-64,-64):
                    ref={'shot':'model','initial':dict(zip(TRACKS,map(int,shifts)))}
                    assert labels==[local_decode(j,'model',clock[j],moved[j],ref) for j in SITES]
        assert sum(sums.values())==1 and (original is None or sum(original.values())==1)
        rows.append({'route':route,'k':str(k),'background':case,'J':str(J),
                     'referenced':{k:str(v) for k,v in sums.items()},
                     'original':{k:str(v) for k,v in original.items()} if original else None,
                     'first_remaining_wrong':example})
    return {'atomic_states_per_family':729,'velocity_triples_per_family':27,'families':rows}
