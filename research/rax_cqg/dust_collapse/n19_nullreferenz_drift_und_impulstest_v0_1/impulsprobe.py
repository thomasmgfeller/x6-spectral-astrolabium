"""Single-quadrature synthetic records and exact canonical back-action checks."""
from fractions import Fraction as F
from copy import deepcopy
from nullreferenz import K0,V,R,STEP,TRACKS


def fixture():
    from eichen import MU
    g=1/(2*K0*MU*2350)
    force=F(1,10**15)
    response=32*R*MU*g/V*force
    refs={ch:{'kick_reference':'synthetic effective impulse','position_reference':'synthetic broad position scan',
              'offset_reference':'synthetic zero signal','copy_reference':'synthetic initial meter bound',
              'range_linearity_reference':'synthetic affine response contract','kick_Ns':str(force),
              'output_kick_span_q':str(response),'input_position_span_q':'1','output_position_span_q':[str(-R),str(R)],
              'output_offset_bound':str(R/4),'initial_reference_error':str(R)} for ch in TRACKS}
    shots=[]
    for i in range(1,60):
        shots.append({'id':i,'usable':True,'saturated':False,
                      'initial_codes':dict(zip(TRACKS,[(-1)**i*10**11,2*10**11,0])),
                      'momentum_codes':dict(zip(TRACKS,[i%23-11,(-1)**i*9,1]))})
    return {'kind':'synthetic','fixed_n':59,'independent_identical_sampling':True,
            'batch':'synthetic core','sampling_reference':'deterministic positive controls',
            'normal_copy_process':'synthetic standard initial recording','channel_association':'u/h/t same normalized inputs',
            'reference_device_id':'synthetic-k='+str(K0),'channels':refs,'trials':shots}


def run():
    from eichen import action_floor
    from zeugen import cdf_below
    from impulstest import evaluate
    import driftprobe,drifteichung
    cal=drifteichung.evaluate(driftprobe.fixture())
    doc=fixture();res=evaluate(doc,cal)
    assert res['status']=='MEETS_95_AT_95_UNDER_MODEL'
    n0=next(n for n in range(1,150) if cdf_below(n,0,F(1,20),F(1,20)))
    n1=next(n for n in range(1,150) if cdf_below(n,1,F(1,20),F(1,20)))
    assert n0==59 and n1==93
    flags=[]
    for mode in ('missing','clipping','large_momentum','large_initial_position','bad_code'):
        x=deepcopy(doc);row=x['trials'][0]
        if mode=='missing':x['trials'].pop()
        if mode=='clipping':row['saturated']=True
        if mode=='large_momentum':row['momentum_codes']['u']=25
        if mode=='large_initial_position':row['initial_codes']['u']=10**12
        if mode=='bad_code':del row['momentum_codes']['t']
        r=evaluate(x,cal)
        assert r['flags_including_missing']==1 and r['status']=='NOT_DEMONSTRATED'
        flags.append(mode)
    invalid={}
    for mode in ('wrong_polarity','position_leakage','different_device','wrong_origin','excess_copy_error'):
        x=deepcopy(doc);ch=x['channels']['u']
        if mode=='wrong_polarity':ch['kick_Ns']='-1'
        if mode=='position_leakage':ch['output_position_span_q']=str(2*R)
        if mode=='different_device':x['reference_device_id']='different'
        if mode=='wrong_origin':x['kind']='measurement_records'
        if mode=='excess_copy_error':ch['initial_reference_error']=str(2*R)
        try:evaluate(x,cal)
        except ValueError as exc:invalid[mode]=str(exc)
        else:raise AssertionError(mode)
    def form(x,y):
        return x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2]
    def copy(x,g):
        q,p,r,pi=x
        return (q,p-g*pi,r+g*q,pi)
    basis=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    for g in (F(1),F(2,3),F(32)):
        for a in basis:
            for b in basis:assert form(a,b)==form(copy(a,g),copy(b,g))
    # Necessity only: analog RMS copy error <= R, RMS physical kick in model P <= K0 V.
    # The canonical kick is allotted half of the full canonical post-copy budget 2 K0 V.
    floor=action_floor(2*R*K0*V)
    return {'synthetic':res,'minimum_zero_flags':n0,'minimum_one_flag':n1,
            'one_flag_challenges':flags,'invalid_controls':invalid,'symplectic_pair_checks':48,
            'necessary_S0_Js_half_budget':floor.data(),'quantum_full_process':'NOT_TESTED'}
