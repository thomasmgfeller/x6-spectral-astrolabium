"""Generate stationary instrument records separately from the blind reader."""
from fractions import Fraction as F
import json
from folgetakt import IDENTITY, advance


def read(folder, name):
    return json.loads((folder/(name+'.json')).read_bytes())


def setup(previous, early):
    from proben import samples
    return next(r[1:] for r in samples(previous, early)[0] if r[0]=='quarter')


def setting(y, w, alpha):
    from referenzwechsel import displaced
    return displaced(y,w,alpha) if alpha else (y,w)


def certificate(y, w, fifth=False):
    from empfangsbit import K0, V, R, bounds
    from quelle import box, hull
    from staubgeraet import solve, verify
    from kalibriervergleich import margins, rounded_range
    from nullreferenz import maxabs
    route='positive_bridge'
    vel = (hull(-112*V,112*V),)*3
    q = (hull(-1,1),)*3
    def state(j):
        st = solve(y,w,j,vel,K0,box(-K0),route)
        history, a = verify(st,j,vel,K0,box(-K0),route,q)
        if not all(maxabs(v)<8-4*R for v in (st['y'][18],st['y'][7],history[2][7])):
            raise ValueError('digit range')
        return st, a
    zero,_ = state(F(0))
    z = zero['y'][18]
    result = {'native':rounded_range(y[18]),'loaded_null':rounded_range(z)}
    if fifth:
        rows = {}
        for j in (F(-1,10**6),F(0),F(1,10**6)):
            st, a = state(j)
            dt = st['y'][18]-z
            early = bounds(dt,2*R)
            late = bounds(dt-a[2][7]*vel[2],5*R)
            digital, plateau = margins(early,late,j)
            rows[str(j)] = dict(receiver=early, memory=late, digital_budget=digital, plateau_budget=plateau)
        result['source_intervals'] = rows
    return result


def fields(ref):
    return {k:ref[k] for k in (*IDENTITY,'shot','target_index','reference_id')}


def make_records(y,w,label,slot,ref):
    from empfangsbit import K0, R
    from kontrollprobe import stationary
    from nullreferenz import digit
    from referenzprotokoll import emit
    impulses = {'A':(91,-72,112),'B':(-31,97,-112),'C':(0,0,0)}
    st,h,q = stationary(y,w,F(label),impulses[slot],'positive_bridge',K0,-K0,(F(1,2),-1,F(1,3)))
    common = {**fields(ref),'usable':True,'saturated':False}
    recv = {**common,'receiver_clock':digit(st['y'][18])}
    mem = {**common,'clock7':digit(st['y'][7]),'pointer7_t':digit(h[2][7]),'initial_t':digit(q[2]+R)}
    return {'receiver':recv,'memory':mem,'received':emit(ref,recv)}


def generate(parent, previous, early, opening):
    from empfangsbit import K0, STEP
    from referenzprotokoll import forecast
    from nulluhr_gegenprobe import loaded_codes
    from geometrische_uhr import qcode
    from nullreferenz import digit
    from kontrollprobe import stationary
    controls = read(parent,'Beispiel_Nullserie')
    old = forecast(controls)
    y, w = setup(previous,early)
    geom = read(parent,'Geometrische_Nulluhr')
    suite = next(v for v in read(parent,'Vergleich') if v['m']==112)
    load = suite['null_load_codes'][str(K0)]
    certs = {}
    for idx in range(7,12):
        yy,ww = setting(y,w,(idx-10)*6*STEP)
        certs[str(idx)] = certificate(yy,ww,idx==11)
    # Check all bound-compatible momenta at every tick without using the observations.
    sequence = [v['loaded_null'] for v in certs.values()]
    second = [[a[0]-2*b[1]+c[0], a[1]-2*b[0]+c[1]]
              for a,b,c in zip(sequence,sequence[1:],sequence[2:])]
    assert all(-3<=lo<=hi<=3 for lo,hi in second)
    trial,_,_ = stationary(y,w,0,(-51,19,7),'positive_bridge',K0,-K0,(0,0,0))
    holdout = {**{k:old[k] for k in (*IDENTITY,'shot','reference_id')},'index':10,
               'usable':True,'saturated':False,'source_setting':'zero','code':digit(trial['y'][18]),
               'extra_error_codes':1}
    docs = {'Kontrollen':controls,'Vierte_Null':holdout}
    for slot in ('A','B','C'):
        decision = advance(controls,holdout,'Puls-'+slot)
        ref = decision['reference']
        docs[slot+'_Referenz'] = decision
        yy,ww = setting(y,w,6*STEP)
        pack = make_records(yy,ww,opening['sources'][slot],slot,ref)
        for key,obj in pack.items():
            docs[slot+'_'+key] = obj
    # Independent precursor gate at the target tick. The changed branch uses
    # its own checked load interval, not an extrapolation of a sampled bound.
    ref = docs['A_Referenz']['reference']
    jumps = []
    for jump in (F(0),F(1,10**6)):
        yy,ww = setting(y,w,6*STEP+jump)
        zero,_,_=stationary(yy,ww,0,(0,0,0),'positive_bridge',K0,-K0,(0,0,0))
        band = certificate(yy,ww)
        correction = [band['loaded_null'][0]-band['native'][1],
                      band['loaded_null'][1]-band['native'][0]]
        assert load[0]<=correction[0]<=correction[1]<=load[1]
        step=F(1,10**12)
        u,h=[qcode(yy[i],step) for i in (15,17)]
        _, geometric = loaded_codes(u,h,step,F(0),geom,load)
        observed = digit(zero['y'][18])
        assert geometric[0]<=observed<=geometric[1]
        pack = make_records(yy,ww,'0','A',ref)
        from folgetakt import classify
        output = classify(ref,**pack)
        from voruhren import protected_read
        precursor = {**fields(ref),'saturated':False,'usable':True,'code15':u,'code17':h,
                     'raster':str(step),'bias':'0'}
        mode = 'Sprung' if jump else 'Stabil'
        for key, obj in {**pack,'Voruhren':precursor}.items():
            docs[mode+'_'+key]=obj
        gated = protected_read(parent,ref,precursor,**pack)
        lo,hi = ref['range_codes']
        common = [max(lo,geometric[0]),min(hi,geometric[1])]
        jumps.append({'jump':str(jump),'source':'0','clock15':u,'clock17':h,
                      'time_range':[lo,hi],'geometric_range':list(geometric),
                      'model_null':observed,'load_correction_checked':correction,
                      'intersection':common if common[0]<=common[1] else None,
                      'time_only_label':output['source_label'],'guarded_status':gated['status'],
                      'guarded_label':gated.get('readout',{}).get('source_label')})
    return docs, {'ticks':certs,'model_second_difference_bounds':second,'precursor_comparison':jumps}
