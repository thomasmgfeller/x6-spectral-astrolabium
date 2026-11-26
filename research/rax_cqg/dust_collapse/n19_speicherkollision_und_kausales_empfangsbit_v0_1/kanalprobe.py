"""Stationary register extension, local interface controls and independent concrete digit replay."""
from fractions import Fraction as F
from itertools import product
from empfangsbit import K0,V,R,STEP,CAL,THRESHOLD
from leseprotokoll import emit,read


def smooth(d):
    a=abs(d)
    if a<=100:return F(0),F(0)
    if a>=150:return F(1),F(0)
    x=(a-100)/50
    return x*x*(3-2*x),(1 if d>0 else -1)*6*x*(1-x)/50


def action(d,r,s,load):
    f,_=smooth(d)
    return (r-f)**2/2+(s-r)**2-load*s


def exact_register():
    total=0;slopes={}
    for d,load in product(map(F,(-250,-125,-36,0,36,125,250)),(F(-1,8),F(0),F(1,8))):
        f,df=smooth(d)
        r=f+load;s=r+load/2
        assert (r-f)-2*(s-r)==0 and 2*(s-r)==load
        assert action(d,r,s,load)==-load*f-F(3,4)*load**2
        c=(-1,9,-45,0,45,-9,1);h=F(1,17)
        derivative=sum(w*action(d+j*h,r,s,load) for j,w in zip(range(-3,4),c))/(60*h)
        assert derivative==-load*df
        slopes[f'{d}/{load}']=str(derivative)
        for err in [F(-1,8),F(1,8)]:
            if abs(d)<=100 or abs(d)>=150:assert int(s+err>F(1,2))==int(f)
        total+=1
    assert smooth(F(125))[1]!=0
    return {'stationary_and_derivative_checks':total,'total_output_error_bound':'5/16',
            'remaining_threshold_margin':'3/16','receiver_force_examples':slopes}


def run(previous,early,proof):
    from quelle import box
    from nullreferenz import digit
    from proben import samples
    from wege import ROUTES
    from staubgeraet import solve,verify
    from gemischt import ORDER,COEFF
    from uhrauslese import LABELS
    assert (18,7) in ORDER and COEFF[18,7]==1 and not any((18,i) in ORDER and (i,7) in ORDER for i in range(19))
    for row in proof:
        assert row['receiver_null_abs_max']+1<=100
        assert row['receiver_pulse_abs_min']-1>=150
    examples=None;trials=0
    for (name,y,w),route,k,J in product(samples(previous,early)[0],ROUTES,(F(1),K0),LABELS):
        for sign in (-1,1):
            vel=tuple(box(K0*V/k*sign*a) for a in (F(96),F(-511,7),F(957,10)))
            q=tuple(box(sign*a) for a in (F(23,100),F(-1),F(67,100)))
            delta=box(sign*K0 if k==1 else -k)
            st=solve(y,w,J,vel,k,delta,route)
            h,_=verify(st,J,vel,k,delta,route,q)
            metadata={'kind':'synthetic','shot':'example','device':route+'_'+str(k),
                      'baseline_id':'null_'+name,'baseline_code':digit(y[18]+sign*CAL),
                      'baseline_error_q':str(CAL),'usable':True,'saturated':False}
            receiver={**metadata,'receiver_clock':digit(st['y'][18])}
            late={**metadata,'clock7':digit(st['y'][7]),'pointer7_t':digit(h[2][7]),
                  'initial_t':digit(q[2]-sign*R)}
            packet=emit(receiver)
            result=read(late,packet)
            assert result['source_label']==str(J)
            if name=='quarter' and route=='positive_bridge' and k==K0 and J>0 and sign==1:
                examples=dict(receiver=receiver,late=late,packet=packet,result=result)
            trials+=1
    assert examples
    errors={}
    for mode in ('missing','wrong_shot','wrong_reference','wrong_origin','too_coarse','saturated','missing_bit','wrong_bit'):
        packet=examples['packet'].copy();late=examples['late'].copy()
        if mode=='missing':packet=None
        if mode=='wrong_shot':packet['shot']='other'
        if mode=='wrong_reference':packet['baseline_id']='other'
        if mode=='wrong_origin':packet['kind']='measurement_records'
        if mode=='too_coarse':late['baseline_error_q']='1/1000'
        if mode=='saturated':late['saturated']=True
        if mode=='missing_bit':del packet['bit']
        if mode=='wrong_bit':packet['bit']=0
        try:
            result=read(late,packet)
            if mode=='wrong_bit':assert result['source_label']=='0'
            else:assert result['source_label'] is None
            errors[mode]=result
        except ValueError as exc:
            errors[mode]=str(exc)
            assert mode not in ('missing_bit','wrong_bit')
    margins={}
    for row in proof:
        if row['joint_one_bit']==144:
            margins[str(row['m'])]=min(THRESHOLD-row['receiver_null_abs_max'],
                    row['receiver_pulse_abs_min']-THRESHOLD-1,row['minimum_nonzero_late_signed_code']-1)
    return {'register':exact_register(),'examples':examples,'concrete_trials':trials,'input_controls':errors,
            'extra_common_reference_code_error_guarantee':margins,'native_edge':[18,7],'physical_P3':'60 NOT_RUN'}
