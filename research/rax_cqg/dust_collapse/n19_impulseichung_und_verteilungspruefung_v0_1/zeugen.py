"""Two-setting classical preparation witness with an exact fixed-sample binomial test."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from eichen import MU
from intervall import interval
from streuung import B,V,K0,FOCUS,STEP

ETA=F(1,100)
CONFIDENCE=F(19,20)
BAD_TARGET=F(1,20)


def settings(collar,doc):
    reference=collar['device_fits'][str(K0)]
    if doc.get('reference_collar_device_id')!=reference['device_id']:
        raise ValueError('witness and weak collar reference different devices')
    g_c=interval(reference['fit_gain_q_per_Ns'])
    result={}
    for sign in (-1,1):
        rows=doc['reference_settings'][str(sign)]
        if len(rows)!=3:raise ValueError('three individually calibrated witness channels required')
        data=[]
        for ch in rows:
            if not ch.get('position_ref') or not ch.get('impulse_ref'):
                raise ValueError('missing witness reference')
            gain=interval(ch['output_span_q'])/interval(ch['input_span_q'])
            beta=interval(ch['kick_output_span_q'])/interval(ch['kick_span_Ns'])
            if not gain.inside([32*(1-ETA),32*(1+ETA)]):
                raise ValueError('witness gain outside registered band')
            if beta.lo<=0:raise ValueError('positive kick response required')
            A=beta/(gain*MU*g_c)
            normalized=(A-FOCUS)*V/B
            if not normalized.inside([sign-ETA,sign+ETA]):
                raise ValueError('witness shear outside registered guard band')
            bias=F(ch['max_output_offset_q'])
            if bias<0:raise ValueError('negative offset bound')
            data.append((gain.lo,bias,A))
        result[sign]=data
    return result


def cdf_below(total,count,p0,alpha):
    q=1-p0
    term=q**total
    acc=term
    for i in range(1,count+1):
        if acc>alpha:return False
        term*=F(total-i+1,i)*p0/q
        acc+=term
    return acc<=alpha


def evaluate(calibration_result,doc):
    if doc.get('kind')=='no_observations':
        return {'record_kind':'no_observations','witness_status':'NOT_MEASURED','physical_P3':'60 NOT_RUN'}
    kind=doc.get('kind')
    if kind not in ('synthetic','measurement_records') or kind!=calibration_result.get('record_kind'):
        raise ValueError('unmatched data origin')
    if not all(doc.get(s) for s in ('apparatus_association','preparation_batch','randomization_record')):
        raise ValueError('witness references are incomplete')
    n=doc['fixed_trial_count']
    if type(n) is not int or n<1:raise ValueError('invalid registered trial count')
    if not (doc.get('settings_uniform_after_preparation') is True and doc.get('independent_identical_preparations') is True):
        raise ValueError('fixed-N inference requires these sampling assumptions')
    refs=settings(calibration_result,doc)
    by_id={}
    for shot in doc['trials']:
        j=shot['id']
        if type(j) is not int or j in by_id or not 1<=j<=n:raise ValueError('repeated or unregistered trial')
        by_id[j]=shot
    flags=0
    for j in range(1,n+1):
        shot=by_id.get(j)
        if not shot or shot.get('usable') is not True or shot.get('saturated') is not False:
            flags+=1;continue
        sign=shot.get('setting')
        if type(sign) is not int or sign not in refs:raise ValueError('invalid setting code')
        codes=shot.get('display_codes')
        if not isinstance(codes,list) or len(codes)!=3 or any(type(v) is not int for v in codes):
            flags+=1;continue
        upper=[(abs(code)*STEP+STEP/2+bias)/(gain*B) for code,(gain,bias,_) in zip(codes,refs[sign])]
        flags+=int(max(upper)>2*(1-ETA))
    ok=cdf_below(n,flags,BAD_TARGET/2,1-CONFIDENCE)
    return {'record_kind':kind,'registered_trials':n,'flags_including_missing':flags,
            'witness_status':'MEETS_95_AT_95_UNDER_SAMPLING_ASSUMPTIONS' if ok else 'NOT_DEMONSTRATED',
            'accepted_target_joint_probability':str(1-BAD_TARGET) if ok else None,
            'shear_intervals':{str(i):[row[2].data() for row in values] for i,values in refs.items()},
            'physical_P3':'60 NOT_RUN'}


if __name__=='__main__':
    from eichen import evaluate as calibrate
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('calibration',type=Path,help='raw action calibration JSON')
    p.add_argument('witness',type=Path,help='witness JSON')
    args=p.parse_args()
    try:
        out=evaluate(calibrate(json.loads(args.calibration.read_text())),json.loads(args.witness.read_text()))
    except (ValueError,KeyError,ZeroDivisionError,TypeError) as exc:
        p.exit(2,'INVALID: '+str(exc)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
