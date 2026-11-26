"""Independent integer enumeration, direct stationary null controls and end-to-end trials."""
from fractions import Fraction as F
from copy import deepcopy
from itertools import product
from referenzprotokoll import next_envelope,forecast,emit,late_read
from geometrische_uhr import extras,qcode,interval_analog


def integer_check():
    count=0;empty=0
    bands=[(i,i+j) for i in range(-2,3) for j in range(3)]
    for a,b,c in product(bands,repeat=3):
        for limit in (0,1,2):
            limits=[]
            for u,v,w in product(*(range(x,y+1) for x,y in (a,b,c))):
                if abs(w-2*v+u)<=limit:
                    limits.extend([2*w-v-limit,2*w-v+limit])
            try:enclosure=next_envelope([a,b,c],limit)
            except ValueError:
                assert not limits
                empty+=1
            else:assert enclosure==(min(limits),max(limits))
            count+=1
    return {'enumerated_cases':count,'infeasible':empty}


def stationary(y,w,J,ys,route,k,delta,qs):
    from quelle import box
    from empfangsbit import K0,V
    from staubgeraet import solve,verify
    vel=tuple(box(K0*V*v/k) for v in ys);mismatch=box(delta);q=tuple(map(box,qs))
    st=solve(y,w,J,vel,k,mismatch,route)
    h,_=verify(st,J,vel,k,mismatch,route,q)
    return st,h,q


def run(previous,early):
    from quelle import box
    from proben import samples
    from uhrauslese import LABELS
    from wege import ROUTES
    from nullreferenz import digit
    from empfangsbit import K0,R,STEP
    from referenzwechsel import displaced
    tests=integer_check()
    fixtures=samples(previous,early)[0];cases=list(fixtures)+list(extras(fixtures))
    _,y,w=next(r for r in cases if r[0]=='quarter')
    cfg={'kind':'synthetic','device':'weak_positive_bridge','campaign':'quarter_run','clock_reference':'common_adc',
         'cadence_reference':'unit-spaced synthetic run clock','shot':'blind_target','target_index':10,
         'curvature_reference':'synthetic bound on the ideal loaded null codes','momentum_reference':'synthetic post-copy bound',
         'curvature_codes':3,'momentum_bound':112,'controls':[]}
    for j,sgn in zip((-3,-2,-1),(1,-1,1)):
        yy,ww=displaced(y,w,j*6*STEP)
        st,_,_=stationary(yy,ww,0,(sgn*31,sgn*47,sgn*9),'positive_bridge',K0,-K0,(0,0,0))
        cfg['controls'].append({**{k:cfg[k] for k in ('device','campaign','clock_reference')},
                                'index':10+j,'source_setting':'zero','code':digit(st['y'][18])+sgn,
                                'extra_error_codes':1,'usable':True,'saturated':False})
    ref=forecast(cfg)
    null,_,_=stationary(y,w,0,(-51,19,7),'positive_bridge',K0,-K0,(0,0,0))
    true=digit(null['y'][18]);assert ref['range_codes'][0]<=true<=ref['range_codes'][1]
    common={k:ref[k] for k in ('kind','device','campaign','shot','clock_reference','target_index','reference_id')}
    common.update(usable=True,saturated=False)
    example={};arms=[]
    for J in LABELS:
        st,h,q=stationary(y,w,J,(91,-72,112),'positive_bridge',K0,-K0,(F(1,2),-1,F(1,3)))
        re={**common,'receiver_clock':digit(st['y'][18])}
        la={**common,'clock7':digit(st['y'][7]),'pointer7_t':digit(h[2][7]),'initial_t':digit(q[2]+R)}
        bit=emit(ref,re);result=late_read(ref,la,bit)
        assert result['source_label']==str(J)
        arms.append([str(J),bit['bit'],result['source_label']])
        if J>0:example={'control_input':cfg,'forecast':ref,'receiver':re,'late':la,'packet':bit}
    bad={}
    for mode in ('saturation','future_reference','different_device','imprecise','curve_violation','target_pulsed','negative_curvature'):
        d=deepcopy(cfg)
        if mode=='saturation':d['controls'][0]['saturated']=True
        if mode=='future_reference':d['controls'][-1]['index']=11
        if mode=='different_device':d['controls'][0]['device']='other'
        if mode=='imprecise':
            for row in d['controls']:row['extra_error_codes']=200
        if mode=='curve_violation':d['controls'][0]['code']+=40
        if mode=='target_pulsed':d['controls'][1]['source_setting']='positive'
        if mode=='negative_curvature':d['curvature_codes']=-1
        try:forecast(d)
        except ValueError as exc:bad[mode]=str(exc)
        else:raise AssertionError(mode)
    # Same control readouts, a hidden change of native background before the next shot.
    yy,ww=displaced(y,w,F(1,10**6))
    quiet,h,q=stationary(yy,ww,0,(0,0,0),'positive_bridge',K0,-K0,(0,0,0))
    b=emit(ref,{**common,'receiver_clock':digit(quiet['y'][18])})
    out=late_read(ref,{**common,'clock7':digit(quiet['y'][7]),'pointer7_t':digit(h[2][7]),'initial_t':0},b)
    assert out['source_label']!=str(0)
    # Independently check the two geometric precursors at finite, rounded bias corners.
    geom_count=0
    for (name,yy,ww),route,k,J,sgn in product(cases,ROUTES,(F(1),K0),LABELS,(-1,1)):
        st,h,q=stationary(yy,ww,J,(sgn*83,-sgn*96,sgn*96),route,k,-K0 if k==K0 else sgn*K0,(1,-1,F(1,3)))
        u,hc=qcode(yy[15]+sgn*R,STEP),qcode(yy[17]-sgn*R,STEP)
        ctr,_,_=interval_analog(u,hc,STEP,R)
        base=digit(ctr)
        assert base is not None
        flag=abs(digit(st['y'][18])-base)>125
        sign=digit(st['y'][7])-digit(h[2][7])+digit(q[2]+sgn*R)-base
        answer=(F(1,10**6) if sign>0 else -F(1,10**6)) if flag else F(0)
        assert (not flag or sign!=0) and answer==J
        geom_count+=1
    return {'integer_solver':tests,'example':example,'true_target_null_code':true,'all_arms':arms,'bad_controls':bad,
            'hidden_jump_quiet_classified_as':out['source_label'],'geometric_finite_trials':geom_count}
