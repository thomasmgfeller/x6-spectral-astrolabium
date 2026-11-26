"""Geometry, finite-sample thresholds and synthetic acceptance controls."""
import json
import random
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from intervall import I,relative
from eichen import evaluate as calibrate
from eichprobe import fixture
from streuung import B,K0,round_code
from zeugen import evaluate,cdf_below,ETA


def fixture_witness():
    rng=random.Random(391392)
    refs={}
    for sign in (-1,1):
        A=250+100*sign
        gain=F(32)
        beta=gain*A/(2*K0*3000)
        refs[str(sign)]=[{'position_ref':'synthetic length standard','impulse_ref':'synthetic independent kicks',
                          'input_span_q':'1/1000','output_span_q':relative(gain/1000,F(1,10000)).data(),
                          'kick_span_Ns':'1/1000000000000000',
                          'kick_output_span_q':relative(beta/F(10**15),F(1,10000)).data(),
                          'max_output_offset_q':str(B/4)} for _ in range(3)]
    n=119;shots=[]
    for i in range(1,n+1):
        xy=[(F(rng.choice((-1,1)),3),F(rng.choice((-1,1)),3)) for _ in range(3)]
        s=rng.choice((-1,1))
        shots.append({'id':i,'setting':s,'usable':True,'saturated':False,
                      'display_codes':[round_code(32*B*(x+s*y)) for x,y in xy]})
    return {'kind':'synthetic','apparatus_association':'synthetic common N19 ensemble',
            'reference_collar_device_id':'synthetic-k='+str(K0),
            'preparation_batch':'synthetic Rademacher core','randomization_record':'deterministic replay seed 391392',
            'settings_uniform_after_preparation':True,'independent_identical_preparations':True,
            'fixed_trial_count':n,'reference_settings':refs,'trials':shots}


def log_pos(x,terms=56):
    z=(x-1)/(x+1)
    assert 0<z<1
    s=2*sum((z**(2*j+1)/(2*j+1) for j in range(terms)),F(0))
    rem=2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    return I(s,s+rem)


def runs_for_zero(f):
    log20=4*log_pos(F(2))+log_pos(F(5,4))
    terms=12
    s=sum((f**j/j for j in range(1,terms+1)),F(0))
    neglog=I(s,s+f**(terms+1)/((terms+1)*(1-f)))
    bound=log20/neglog
    assert bound.lo.__ceil__()==bound.hi.__ceil__()
    return bound.hi.__ceil__()


def run(baseline):
    actual_floor=F(json.loads((baseline/'GleichePraeparation.json').read_bytes())['gaussian_joint_success_lower'])
    direct=runs_for_zero(1-actual_floor)
    rate=F(1,40)
    assert runs_for_zero(rate)==119
    assert not cdf_below(118,0,rate,F(1,20)) and cdf_below(119,0,rate,F(1,20))
    with_one=next(n for n in range(119,300) if cdf_below(n,1,rate,F(1,20)))
    cal=calibrate(fixture(F(3000)))
    doc=fixture_witness()
    result=evaluate(cal,doc)
    assert result['flags_including_missing']==0 and result['accepted_target_joint_probability']=='19/20'
    assert evaluate({},{'kind':'no_observations'})['witness_status']=='NOT_MEASURED'
    counter=[]
    for mode in ('missing','saturated','large_code'):
        changed=deepcopy(doc)
        if mode=='missing':changed['trials'].pop()
        if mode=='saturated':changed['trials'][5]['saturated']=True
        if mode=='large_code':changed['trials'][7]['display_codes']=[0,128,0]
        out=evaluate(cal,changed)
        assert out['flags_including_missing']==1 and out['witness_status']=='NOT_DEMONSTRATED'
        counter.append(mode)
    invalid={}
    for mode in ('reference_device','measurement_origin','gain','shear','duplicate','late_choice'):
        altered=deepcopy(doc)
        if mode=='reference_device':altered['reference_collar_device_id']='different'
        if mode=='measurement_origin':altered['kind']='measurement_records'
        if mode=='gain':altered['reference_settings']['1'][0]['output_span_q']='1/100'
        if mode=='shear':altered['reference_settings']['1'][0]['kick_span_Ns']='1/10000000000'
        if mode=='duplicate':altered['trials'][1]['id']=1
        if mode=='late_choice':altered['settings_uniform_after_preparation']=False
        try:evaluate(cal,altered)
        except ValueError as exc:invalid[mode]=str(exc)
        else:raise AssertionError(mode+' unexpectedly accepted')
    # Check the extremal vertices independently of the analytic triangle bound.
    accepted=2*(1-ETA)
    upper=F(0)
    for ep,em,vp,vm in product((-1,1),repeat=4):
        a,b=1+ep*ETA,-1+em*ETA
        y=accepted*(vp-vm)/(a-b)
        x=vp*accepted-a*y
        upper=max(upper,x*x+y*y)
    assert upper<=4
    x=y=F(3,2)
    assert x*x+y*y>4 and x-y==0 and x+y>2
    return {'synthetic_119_shot_replay':result,'one_flag_controls':counter,'invalid_design_controls':invalid,
            'registered_zero_flag_min_n':119,'one_flag_min_n_if_that_design_is_fixed_in_advance':with_one,
            'direct_zero_failure_min_n_at_PR391_lower_bound':direct,
            'PR391_gaussian_joint_success_lower':str(actual_floor),'largest_vertex_E':str(upper),
            'random_setting_detection_factor':2}
