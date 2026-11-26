"""Single-setting, sacrificial post-copy momentum test on an independently prepared batch."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from nullreferenz import K0,V,R,STEP,TRACKS


def settings(doc,cal):
    from intervall import interval
    from eichen import MU
    if doc['reference_device_id']!=cal['weak_device_id']:
        raise ValueError('weak collar and witness device differ')
    collar=interval(cal['fits'][str(K0)]['gain'])
    if set(doc['channels'])!=set(TRACKS):raise ValueError('three separate witness channels required')
    prepared={}
    for track,ref in doc['channels'].items():
        if not all(ref.get(k) for k in ('kick_reference','position_reference','offset_reference','range_linearity_reference','copy_reference')):
            raise ValueError('reference records missing')
        beta=interval(ref['output_kick_span_q'])/interval(ref['kick_Ns'])
        gain=beta*V/(R*MU*collar)
        leak=interval(ref['output_position_span_q'])/interval(ref['input_position_span_q'])
        bias=F(ref['output_offset_bound']);copy_error=F(ref['initial_reference_error'])
        if not gain.inside(['31.68','32.32']) or not leak.inside([-R,R]):
            raise ValueError('gain or position leakage out of range')
        if not 0<=bias<=R/4 or not 0<=copy_error<=R:
            raise ValueError('offset or initial copy error exceeds allowance')
        prepared[track]=(gain.lo,max(abs(leak.lo),abs(leak.hi)),bias,copy_error)
    return prepared


def evaluate(doc,cal):
    from zeugen import cdf_below
    if doc.get('kind')=='no_observations' and not doc.get('trials'):
        return {'record_kind':'no_observations','registered_physical_trials':0,
                'status':'NOT_MEASURED','physical_P3':'60 NOT_RUN'}
    kind=doc.get('kind')
    if kind not in ('measurement_records','synthetic') or kind!=cal['record_kind']:
        raise ValueError('mixed or unknown origin')
    if not all(doc.get(k) for k in ('batch','sampling_reference','normal_copy_process','channel_association')):
        raise ValueError('preparation provenance incomplete')
    if doc.get('independent_identical_sampling') is not True:raise ValueError('requires iid sampling')
    refs=settings(doc,cal)
    n=doc['fixed_n']
    if type(n) is not int or n<=0:raise ValueError('invalid registered trial count')
    observed={}
    for trial in doc['trials']:
        idx=trial['id']
        if type(idx) is not int or not 1<=idx<=n or idx in observed:raise ValueError('unregistered or duplicate id')
        observed[idx]=trial
    flags=0
    for idx in range(1,n+1):
        row=observed.get(idx)
        if not row or row.get('usable') is not True or row.get('saturated') is not False:
            flags+=1
            continue
        passed=True
        if not isinstance(row.get('initial_codes'),dict) or not isinstance(row.get('momentum_codes'),dict):
            flags+=1
            continue
        for name,(gain,leak,bias,copy_error) in refs.items():
            q=row.get('initial_codes',{}).get(name)
            z=row.get('momentum_codes',{}).get(name)
            if any(type(v) is not int or not -8<=v*STEP<8 for v in (q,z)):
                passed=False
                break
            qmax=abs(q)*STEP+R+copy_error
            ymax=(abs(z)*STEP+R+bias+leak*qmax)/(gain*R)
            if qmax>1 or ymax>1:passed=False
        flags+=int(not passed)
    ok=cdf_below(n,flags,F(1,20),F(1,20))
    return {'record_kind':kind,'fixed_n':n,'flags_including_missing':flags,
            'status':'MEETS_95_AT_95_UNDER_MODEL' if ok else 'NOT_DEMONSTRATED','physical_P3':'60 NOT_RUN'}


if __name__=='__main__':
    from basisdaten import inputs
    from drifteichung import evaluate as calibrate
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('calibration',type=Path)
    p.add_argument('records',type=Path)
    args=p.parse_args()
    try:
        with inputs():
            result=evaluate(json.loads(args.records.read_text()),calibrate(json.loads(args.calibration.read_text())))
    except (ValueError,TypeError,KeyError,ZeroDivisionError) as exc:
        p.exit(2,'INVALID: '+str(exc)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
