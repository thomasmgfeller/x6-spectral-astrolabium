"""Predict a loaded reference from earlier control digits and use it locally at 18 and 7."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
from n19_archiv394 import ROOT

STEP=F(2,10**12)
THRESHOLD=125


def integer(v):
    return type(v) is int


def digit(v):
    return integer(v) and -8<=v*STEP<8


def fingerprint(doc):
    raw=json.dumps(doc,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
    return sha256(raw).hexdigest()


def ceilhalf(n):
    return -((-n)//2)


def next_envelope(bands,curvature):
    """Sharp integer hull under the two consecutive second-difference constraints."""
    if len(bands)!=3 or not integer(curvature) or curvature<0:
        raise ValueError('three time-ordered controls and nonnegative integer curvature required')
    if any(len(v)!=2 or any(not integer(x) for x in v) or v[0]>v[1] for v in bands):
        raise ValueError('invalid input interval')
    (l1,u1),(l2,u2),(l3,u3)=bands
    endpoints=[]
    for parity in (0,1):
        # Let the last true code be w=2s+parity. Then the preceding v must
        # be in both [l2,u2] and [s+a,s+b] for a compatible first control.
        a=ceilhalf(l1+parity-curvature);b=(u1+parity+curvature)//2
        low=max(ceilhalf(l3-parity),l2-b);high=min((u3-parity)//2,u2-a)
        if low>high or a>b:continue
        lower=2*(2*low+parity)-min(u2,low+b)-curvature
        upper=2*(2*high+parity)-max(l2,high+a)+curvature
        endpoints.append((lower,upper))
    if not endpoints:raise ValueError('past null digits incompatible with curvature contract')
    return min(z[0] for z in endpoints),max(z[1] for z in endpoints)


def model_budgets(m):
    if not integer(m):raise ValueError('integer registered momentum bound required')
    comparison=json.loads((ROOT/'Vergleich.json').read_bytes())
    for row in comparison:
        if row['m']==m and row['registered_radius']:
            return min(g['extra_plateau_budget'] for g in row['paired_summary'].values())
    raise ValueError('unregistered momentum bound')


def forecast(doc):
    if doc.get('kind')=='no_observations' and not doc.get('controls'):
        return {'kind':'no_observations','status':'NOT_MEASURED','physical_P3':'60 NOT_RUN'}
    if doc.get('kind') not in ('synthetic','measurement_records'):
        raise ValueError('unknown provenance')
    keys=('device','campaign','clock_reference','cadence_reference','shot','curvature_reference','momentum_reference')
    if not all(isinstance(doc.get(k),str) and doc[k].strip() for k in keys):
        raise ValueError('missing reference or target identity')
    m=doc['momentum_bound'];budget=model_budgets(m)
    idx=doc['target_index'];c=doc['curvature_codes'];rows=doc['controls']
    if not integer(idx) or len(rows)!=3:raise ValueError('three preceding controls required')
    bands=[]
    for i,row in enumerate(rows,idx-3):
        if not integer(row.get('index')) or row['index']!=i or row.get('source_setting')!='zero':
            raise ValueError('controls must precede target at registered cadence with source gated off')
        if any(row.get(k)!=doc[k] for k in ('device','campaign','clock_reference')):
            raise ValueError('unmatched null calibration')
        if row.get('usable') is not True or row.get('saturated') is not False:
            raise ValueError('unusable control')
        z=row.get('code');e=row.get('extra_error_codes')
        if not digit(z) or not integer(e) or e<0 or not digit(z-e) or not digit(z+e):
            raise ValueError('invalid control reading or error')
        bands.append((z-e,z+e))
    lo,hi=next_envelope(bands,c);chosen=(lo+hi)//2;radius=max(chosen-lo,hi-chosen)
    if not digit(lo) or not digit(hi) or radius>budget:
        raise ValueError('forecast outside usable range or plateau budget')
    result={k:doc[k] for k in ('kind','device','campaign','clock_reference','shot','target_index')}
    result.update(status='CONDITIONAL_MODEL_REFERENCE',momentum_bound=m,baseline_code=chosen,range_codes=[lo,hi],
                  worst_error_codes=radius,allowed_error_codes=budget,control_record_sha256=fingerprint(doc))
    result['reference_id']=fingerprint(result)
    return result


def association(ref,record):
    if ref.get('status')!='CONDITIONAL_MODEL_REFERENCE' or ref.get('reference_id')!=fingerprint({k:v for k,v in ref.items() if k!='reference_id'}):
        raise ValueError('missing or inconsistent frozen reference')
    keys=('kind','device','campaign','clock_reference','shot','target_index')
    if any(record.get(k)!=ref[k] for k in keys) or record.get('reference_id')!=ref['reference_id']:
        raise ValueError('wrong target or reference')
    if record.get('saturated') is not False or record.get('usable') is not True:
        raise ValueError('unusable reading')
    return {k:ref[k] for k in (*keys,'reference_id')}


def emit(ref,record):
    fields=association(ref,record)
    v=record.get('receiver_clock')
    if not digit(v):raise ValueError('invalid receiver digit')
    return {**fields,'bit':int(abs(v-ref['baseline_code'])>THRESHOLD)}


def late_read(ref,record,packet):
    fields=association(ref,record)
    if not isinstance(packet,dict) or any(packet.get(k)!=v for k,v in fields.items()):
        raise ValueError('missing or mismatched payload')
    bit=packet.get('bit');codes=[record.get(k) for k in ('clock7','pointer7_t','initial_t')]
    if not integer(bit) or bit not in (0,1) or not all(map(digit,codes)):
        raise ValueError('invalid bit or readout')
    signed=codes[0]-codes[1]+codes[2]-ref['baseline_code']
    if bit and signed==0:raise ValueError('ambiguous direction')
    label='0' if bit==0 else ('1/1000000' if signed>0 else '-1/1000000')
    return {'kind':ref['kind'],'source_label':label,'status':'CONDITIONAL_MODEL_CLASSIFICATION','physical_P3':'60 NOT_RUN'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=('eichen','senden','lesen'));p.add_argument('files',nargs='+',type=Path)
    args=p.parse_args()
    if len(args.files)!=('eichen','senden','lesen').index(args.mode)+1:p.error('incorrect number of files')
    try:
        result={'eichen':forecast,'senden':emit,'lesen':late_read}[args.mode](*[json.loads(path.read_bytes()) for path in args.files])
    except (ValueError,KeyError,ZeroDivisionError,TypeError) as exc:p.exit(2,'UNRESOLVED: '+str(exc)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
