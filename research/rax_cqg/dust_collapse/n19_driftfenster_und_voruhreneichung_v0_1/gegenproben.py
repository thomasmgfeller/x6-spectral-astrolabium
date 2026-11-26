"""Independent direct checks against stationary readouts and withheld time records."""
from fractions import Fraction as F
from itertools import product
from driftfamilie import LIMIT
from freigabefenster import code_range
from uhrvergleich import TINY, clock_band,decision,guarded,quantize


def geometry_contract(y,w,geo):
    from empfangsbit import STEP
    from quelle import hull,SCALE
    from referenzwechsel import displaced
    from geometrische_uhr import derivatives
    uu,hh = derivatives(*(hull(*map(F,geo[k])) for k in ('u_cover','h_cover')))
    assert uu.data()==geo['derivative_u'] and hh.data()==geo['derivative_h'] and uu.lo>0>hh.hi
    yy,_=displaced(y,w,hull(6*STEP-LIMIT,6*STEP+LIMIT))
    for axis,key in ((15,'u_cover'),(17,'h_cover')):
        lo,hi=map(F,geo[key])
        # Cover a true coordinate and every compatible reconstructed coordinate.
        assert lo<F(yy[axis].lo,SCALE)-4*TINY and F(yy[axis].hi,SCALE)+4*TINY<hi
    return {'derivative_u':uu.data(),'derivative_h':hh.data(),'full_input_rectangle_checked':True}


def in_windows(x,windows):
    # Reject an unresolved numerical comparison with a rounded algebraic boundary.
    for interval in windows:
        la,lb=map(F,interval['left_open'])
        ra,rb=map(F,interval['right_closed'])
        if lb<x<=ra:
            return True
        if la<=x<=lb or ra<x<=rb:
            raise AssertionError('test point too close to enclosed boundary')
    return False


def scan(y,w,ref,geo,cert,analysis):
    from empfangsbit import STEP
    from modell import setting,make_records
    from folgetakt import classify
    from kalibriervergleich import rounded_range
    from quelle import box,hull
    from staubgeraet import solve
    from empfangsbit import K0,V
    cached={}
    def band(method,step,bias,pair):
        key=(method,step,bias,pair)
        if key not in cached:
            cached[key]=clock_band(method,pair,step,bias,geo,cert)
        return cached[key]
    # Include both sides of each geometric boundary, plus half-step offsets,
    # the observed false-bit transitions and both ends of the certified domain.
    xset={F(v,2) for v in range(-40,41)}
    xset.update(F(v) for v in (-500000,-127,-126,124,125,500000))
    for row in analysis['profiles']:
        for ranges in row['drift_windows_in_steps'].values():
            for r in ranges:
                for lim in r.values():
                    xset.update((F(lim[0])-F(1,10**4),F(lim[1])+F(1,10**4)))
    inputs=passed=arms=0
    for x in sorted(xset):
        yy,ww=setting(y,w,(6+x)*STEP)
        state=solve(yy,ww,F(0),(hull(-112*V,112*V),)*3,K0,box(-K0),'positive_bridge')
        true_zero=rounded_range(state['y'][18])
        observed={}
        for j,slot in zip((-LIMIT,F(0),LIMIT),('A','B','C')):
            pack=make_records(yy,ww,j,slot,ref)
            try:
                observed[j]=classify(ref,**pack)['source_label']
            except ValueError as exc:
                if str(exc)!='ambiguous direction':
                    raise
                observed[j]='UNRESOLVED'
        for row in analysis['profiles']:
            s,b=F(row['raster']),F(row['bias'])
            possible=product(code_range(yy[15],s,b),code_range(yy[17],s,b))
            flags=[]
            for pair in possible:
                bounds=band(row['method'],s,b,pair)
                assert bounds[0]<=true_zero[0]<=true_zero[1]<=bounds[1]
                accept=decision(ref,bounds)=='ACCEPT'
                flags.append(accept)
                inputs+=1
                if accept:
                    assert all(observed[j]==str(j) for j in observed)
                    passed+=1
                    arms+=len(observed)
            win=row['drift_windows_in_steps']
            assert any(flags)==in_windows(x,win['any'])
            assert all(flags)==in_windows(x,win['all'])
    return {'direct_drift_points':len(xset),'candidate_code_pair_checks':inputs,
            'accepted_code_pair_checks':passed,'accepted_source_comparisons':arms}


def stale(pkg,y,w,ref,geo,cert):
    from modell import read,setting,make_records
    from empfangsbit import STEP
    from quelle import SCALE
    from geometrische_uhr import qcode
    from folgetakt import classify
    original=read(pkg/'daten','Stabil_Voruhren')
    base=y[18]+6*STEP
    load=list(map(F,cert['load_analog']))
    limits=[quantize(F(base.lo,SCALE)+load[0],STEP),quantize(F(base.hi,SCALE)+load[1],STEP)]
    assert limits==[ref['baseline_code']+1]*2
    records=[]
    examples={}
    for n in (-127,-126,124,125):
        yy,ww=setting(y,w,(6+n)*STEP)
        pack=make_records(yy,ww,0,'C',ref)
        current={**original,'code15':qcode(yy[15],TINY),'code17':qcode(yy[17],TINY)}
        good=guarded(ref,current,**pack,geo=geo,cert=cert)
        held=guarded(ref,original,**pack,geo=geo,cert=cert)
        timed=classify(ref,**pack)
        assert good['status']=='DISJOINT_REFERENCES' and held['status']=='ACCEPT'
        assert pack['receiver']['receiver_clock']==ref['baseline_code']+1+n
        assert held['readout']['source_label']==timed['source_label']
        assert (timed['source_label']!='0')==(n in (-127,125))
        records.append({'displacement_steps':n,'source':'0','time_only_bit':timed['bit'],
                        'with_current_clocks':good['status'],'with_stable_clock_values':held['readout']['source_label']})
        if n==125:
            examples={'Referenz':read(pkg/'daten','A_Referenz'),'Voruhren_aktuell':current,
                      'Voruhren_festgehalten':original,**pack}
    try:
        guarded(ref,{**original,'target_index':10},**pack,geo=geo,cert=cert)
    except ValueError:
        pass
    else:
        raise AssertionError('explicitly wrong timestamp accepted')
    return {'integer_shift_baseline':limits,'time_only_bit_zero_integer_range':[-126,124],
            'counterfactuals':records,'wrong_index_rejected':True},examples
