"""Enclose a fully loaded zero-source partner independently of every target arm."""
from fractions import Fraction as F
from itertools import product
from math import ceil, floor
from geometrische_uhr import STEPS,BIASES,extras


def margins(early,late,J):
    from empfangsbit import THRESHOLD as threshold
    lo,hi=early;l,h=late
    if J==0:
        peak=max(abs(lo),abs(hi))
        return threshold-peak,99-peak
    direction=lo if J>0 else -hi
    sign=l if J>0 else -h
    return min(direction-threshold-1,sign-1),min(direction-151,sign-1)


def rounded_range(value):
    from empfangsbit import STEP
    from quelle import SCALE
    return [floor(F(v,SCALE)/STEP+F(1,2)) for v in (value.lo,value.hi)]


def correlated_digits(st, zero, transfer, velocity):
    from empfangsbit import STEP, R
    from quelle import SCALE
    a,b = rounded_range(st['y'][18])
    l,h = rounded_range(zero['y'][18])
    e,f = rounded_range(st['y'][7])
    # For any common starting phase q, Q(q+A)-Q(q+B) lies between
    # floor((A-B)/STEP) and ceil((A-B)/STEP), including half-step ties.
    delta = st['y'][18]-st['y'][7]-transfer*velocity
    lower = floor((F(delta.lo,SCALE)-R)/STEP)
    upper = ceil((F(delta.hi,SCALE)+R)/STEP)
    return [a-h,b-l],[e-h+lower,f-l+upper]


def run(previous,early,geo):
    from quelle import hull
    from proben import samples
    from nullreferenz import maxabs
    from staubgeraet import solve,verify
    from wege import ROUTES
    from uhrauslese import LABELS
    from empfangsbit import bounds,K0,V,R
    from quelle import box
    fixtures=samples(previous,early)[0]
    cases=list(fixtures)+list(extras(fixtures))
    results=[]
    registered_radii = (0,48,64,96,112)
    for m in (*registered_radii,113,114,115,116,117,118):
        rows=[];geo_margins={};raw=[];tight=[]
        for idx,((name,y,w),route,k) in enumerate(product(cases,ROUTES,(F(1),K0))):
            vel=(hull(-m*V*K0/k,m*V*K0/k),)*3
            mismatch=hull(-K0,K0) if k==1 else box(-K0)
            zero=solve(y,w,F(0),vel,k,mismatch,route)
            verify(zero,F(0),vel,k,mismatch,route,(hull(-1,1),)*3)
            for J in LABELS:
                st=solve(y,w,J,vel,k,mismatch,route)
                history,A=verify(st,J,vel,k,mismatch,route,(hull(-1,1),)*3)
                assert all(maxabs(x)<8-4*R for x in [st['y'][18],st['y'][7],history[2][7],zero['y'][18]])
                # Independent actual null/test preparations; a common uncertain unloaded
                # coordinate need not be used as an observation by either instrument.
                dt=st['y'][18]-zero['y'][18]
                late_dt=dt-A[2][7]*vel[2]
                er=bounds(dt,2*R); lr=bounds(late_dt,5*R)
                dig,smooth=margins(er,lr,J)
                split='registered' if idx<48 else 'held_out'
                ce,cl=correlated_digits(st,zero,A[2][7],vel[2])
                te=[max(ce[0],er[0]),min(ce[1],er[1])]
                tl=[max(cl[0],lr[0]),min(cl[1],lr[1])]
                assert te[0]<=te[1] and tl[0]<=tl[1]
                tb,tp=margins(te,tl,J)
                tight.append((split,tb,tp))
                rows.append(dict(name=name,route=route,k=str(k),J=str(J),group=split,
                                 early=er,late=lr,extra_digit_budget=dig,extra_plateau_budget=smooth))
                native_dt=st['y'][18]-y[18]
                native_late=native_dt-A[2][7]*vel[2]
                raw.append(dict(name=name,k=str(k),route=route,J=str(J),er=bounds(native_dt,2*R),
                                lr=bounds(native_late,5*R)))
                for entry in geo['precision']:
                    key=(entry['step'],entry['bias'],split)
                    err=F(entry['uniform_analog_error'])
                    d,s=margins(bounds(native_dt,err+2*R),bounds(native_late,err+5*R),J)
                    geo_margins.setdefault(key,[]).append((d,s))
        summary={}
        for split in ('registered','held_out'):
            part=[r for r in rows if r['group']==split]
            summary[split]={'count':len(part),'digital_pass':sum(r['extra_digit_budget']>=0 for r in part),
                            'extra_digit_budget':min(r['extra_digit_budget'] for r in part),
                            'extra_plateau_budget':min(r['extra_plateau_budget'] for r in part)}
        load_bounds={}
        for stiffness in {r['k'] for r in raw}:
            zero_codes=[r['er'] for r in raw if r['k']==stiffness and r['J']=='0']
            load_bounds[stiffness]=[min(lo for lo,hi in zero_codes),max(hi for lo,hi in zero_codes)]
        tightened={}
        for split in summary:
            part=[(dg,pl) for key,dg,pl in tight if key==split]
            tightened[split]=dict(digital_pass=sum(dg>=0 for dg,pl in part),extra_plateau_budget=min(pl for dg,pl in part))
        results.append({'m':m,'registered_radius':m in registered_radii,'paired_summary':summary,
                        'correlated_rounding':tightened,'null_load_codes':load_bounds,'paired_rows':rows if m==96 else [],
                        'native_rows':raw if m==96 else [],
                        'geometry_results':[{'step':key[0],'bias':key[1],'group':key[2],
                                             'all':len(vals),'digital_pass':sum(v[0]>=0 for v in vals),
                                             'min_extra_digital':min(v[0] for v in vals),
                                             'min_extra_plateau':min(v[1] for v in vals)} for key,vals in geo_margins.items()]})
    return results
