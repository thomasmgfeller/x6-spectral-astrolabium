"""Correct the original local source residual with a preparation-conditional early momentum estimate."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import floor
from empfangsbit import K0,V,R,STEP,valid

OPTIONS=(-64,0,64)
RADII=(F(0),F(1,16),F(1,4),F(1,2),F(1),F(2),F(4))
SITES=(18,7)
GAIN_ERROR=F(1,16)


@lru_cache(maxsize=128)
def windows(radius):
    if radius<0:raise ValueError('negative band radius')
    out=[]
    # x_c and y_c have equal spacing, but their readout shifts differ.
    for x,y in product(OPTIONS,repeat=2):
        center=R*(x-F(5,2)*y)
        spread=R*((1+F(5,2))*radius+1)
        lo,hi=(floor(q/STEP+F(1,2)) for q in (center-spread,center+spread))
        out.append((lo,hi,y))
    return tuple(out)


@lru_cache(maxsize=8192)
def branch(code,radius):
    if not valid(code):return None
    choices={y for lo,hi,y in windows(radius) if lo<=code<=hi}
    return next(iter(choices)) if len(choices)==1 else None


def null_gains(route,w):
    from wege import ROUTES
    from quelle import box,SCALE
    result={site:[] for site in SITES}
    for chain in ROUTES[route]:
        a=box(0)
        for j,inertia,_ in chain:
            a+=1/w[inertia]
            if j in result:
                result[j].append(F(round(F(a.lo+a.hi,2*SCALE)*32),32))
    return result


def decode(site,k,gains,clock,ends,starts,radius):
    from quelle import box
    from uhrauslese import decode as source
    n=2 if site==18 else 3 if site==7 else 0
    if not n or not valid(clock) or len(ends)!=n or len(starts)!=n or not all(map(valid,ends)):
        return None
    centers=[branch(code,radius) for code in starts]
    if None in centers:return None
    disp=[box(STEP*(z-a)-g*v*V*K0/k) for z,a,g,v in zip(ends,starts,gains[site],centers)]
    t=box(STEP*clock) if site==18 else box(STEP*clock)-disp[2]
    try:return source(t-disp[0],t-disp[1],t)
    except AssertionError:return None


def certificate(st,A,base,site,J,mismatch,k,radius):
    from quelle import hull,box,SCALE
    from nullreferenz import split_residual,maxabs
    from speichermodell import square
    from uhrauslese import sender,LABELS
    y=st['y'];t,u,h,s=(y[i] for i in (18,15,17,16))
    # All three centres and all error signs; the zero-reference gains are rounded.
    factor=V*K0/k
    errors=[3*R+factor*(64*(maxabs(row[site]-g)+GAIN_ERROR)+radius*maxabs(row[site]))
            for row,g in zip(A,base[site])]
    eb=R+(errors[2] if site==7 else 0)
    e,a,b=(hull(-z,z) for z in (eb,errors[0],errors[1]))
    native=st['extra']*(2*t-s-sender(u,J))-st['receiver_defect']-mismatch*(square(t-s)+square(t-h))
    defect=maxabs(native+split_residual(t,u,h,J,e,a,b))
    uu=u+e-a;tt=t+e;levels=sender(uu,hull(LABELS[0],LABELS[-1]))
    assert (tt-levels).lo>0 and (uu+3).lo>0
    sep=F((box(LABELS[1]-LABELS[0])*(tt-levels)/(uu+3)).lo,SCALE)
    return sep-2*defect


def run(previous,early):
    from quelle import hull,box
    from nullreferenz import digit
    from uhrauslese import LABELS
    from proben import samples
    from staubgeraet import solve,verify
    from wege import ROUTES
    fixtures,_=samples(previous,early)
    shapes=list(product(OPTIONS,repeat=3))
    rates={r:[] for r in RADII}
    exact=[];badref_count=0;concrete=0
    for (name,y,w),route,k in product(fixtures,ROUTES,(F(1),K0)):
        gains=null_gains(route,w)
        incorrect=null_gains(route,fixtures[0][2])
        for J in LABELS:
            for r in RADII:
                for low,high,c in windows(r):
                    assert all(branch(i,r)==c for i in range(low,high+1))
                limit=(64+r)*V*K0/k
                vel=(hull(-limit,limit),)*3
                mismatch=hull(-K0,K0) if k==1 else box(-k)
                st=solve(y,w,J,vel,k,mismatch,route)
                hist,A=verify(st,J,vel,k,mismatch,route,(hull(-1,1),)*3)
                from nullreferenz import maxabs
                assert all(maxabs(z)<8-2*STEP for z in [st['y'][18],st['y'][7],*[h[s] for s in SITES for h in hist]])
                margins=[certificate(st,A,gains,site,J,mismatch,k,r) for site in SITES]
                rates[r].append((min(margins),name,route,str(k),str(J)))
            on_target=0
            for ys in shapes:
                vel=tuple(box(K0*V*v/k) for v in ys)
                delta=box(0 if k==1 else -k)
                st=solve(y,w,J,vel,k,delta,route)
                hist,_=verify(st,J,vel,k,delta,route,(box(0),)*3)
                rel={site:[digit(h[site]) for h in hist[:2 if site==18 else 3]] for site in SITES}
                representative=[int(-F(5,4)*v) for v in ys]
                ok=True
                for site in SITES:
                    n=len(rel[site]);starts=representative[:n];clock=digit(st['y'][site])
                    ends=[a+d for a,d in zip(starts,rel[site])]
                    label=decode(site,k,gains,clock,ends,starts,F(0))
                    ok=ok and label==J
                    if name=='quarter' and k==K0 and decode(site,k,incorrect,clock,ends,starts,F(0))!=J:
                        badref_count+=1
                # Integer grid translation preserves each end minus start as well as inferred y.
                for xs in shapes:
                    starts=[int(F(x,2)-F(5,4)*v) for x,v in zip(xs,ys)]
                    assert all(branch(c,F(0))==v for c,v in zip(starts,ys))
                    assert all(valid(c+d) and (c+d)-c==d for site in SITES for c,d in zip(starts,rel[site]))
                    on_target+=int(ok);concrete+=1
            exact.append(dict(case=name,route=route,k=str(k),J=str(J),correct_both=on_target,total=729))
    overlap=windows(F(401,100))
    ambiguities={i for a,b,y in overlap for i in range(a,b+1) if branch(i,F(401,100)) is None}
    assert ambiguities
    return {'all_atom_families':exact,'count':concrete,'wrong_or_unresolved_wrong_reference':badref_count,
            'ambiguous_initial_codes_at_r_4_01':sorted(ambiguities),
            'initial_code_to_y':{str(int(F(x,2)-F(5,4)*y)):y for x,y in product(OPTIONS,repeat=2)},
            'continuous_bands':[dict(r=str(r),joint_pass=sum(v[0]>0 for v in values),
                                     minimum_margin=str(min(values)[0]),worst_family=min(values)[1:])
                                for r,values in rates.items()]}
