"""Calibrate the action from blind free-collar records; all bounds are exact rationals."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from intervall import interval,around,pi_bounds

MU=F(1,8)
KS=(F(1),F(1,10**11))
SIGNS=(1,-1,-1,1)
H=F('6.62607015e-34')
H_LIMIT=F(4,9)*F(1,10**11)*F(1,10**12)*F(1,10**14)
HOLD_TOL=F(1,50)


def action_floor(limit=H_LIMIT):
    return H/(2*pi_bounds()*limit)


def triangle(t):
    return max(F(0),1-abs(t))


def force_weight(a,b):
    a,b=F(a),F(b)
    if a>b:raise ValueError('pulse segment runs backwards')
    if a==b:return triangle(a)
    grid=sorted({a,b}|{x for x in (F(-1),F(0),F(1)) if a<x<b})
    return sum((r-l)*(triangle(l)+triangle(r))/2 for l,r in zip(grid,grid[1:]))/(b-a)


def sample(record):
    if record.get('dust_source')!='0':
        raise ValueError('calibration requires the dust source off')
    q=list(map(interval,record['positions_q']))
    if len(q)!=3:raise ValueError('three positions required')
    kick=sum((force_weight(v['start'],v['end'])*interval(v['total_Ns'])
              for v in record['impulse_segments']),interval(0))
    return q[0]-2*q[1]+q[2],kick,F(record['block_time'])


def block(records,role):
    if len(records)!=4:raise ValueError('four runs required for ABBA')
    data=list(map(sample,records))
    t=[v[2] for v in data]
    if not(t[1]-t[0]==t[2]-t[1]==t[3]-t[2]>0):
        raise ValueError('recorded block times are not equally spaced')
    if role=='zero':
        if any(k.lo!=0 or k.hi!=0 for _,k,_ in data):
            raise ValueError('nonzero impulse in zero control')
    elif any((s*k).lo<=0 for s,(_,k,_) in zip(SIGNS,data)):
        raise ValueError('reversed or unresolved reference impulse')
    def contrast(coeff,column):return sum((c*row[column] for c,row in zip(coeff,data)),interval(0))
    return {'D':contrast(SIGNS,0),'I':contrast(SIGNS,1),
            'third_D':contrast((-1,3,-3,1),0),'third_I':contrast((-1,3,-3,1),1)}


def calibration(device):
    k=F(device['kappa'])
    if k not in KS:raise ValueError('unregistered device inertia')
    ell=interval(device['metres_per_q'])
    mass=interval(device['kg'])
    dt=interval(device['seconds_per_step'])
    if min(ell.lo,mass.lo,dt.lo)<=0:raise ValueError('nonpositive physical reference')
    if any(not str(device.get(key,'')).strip() for key in ('device_id','length_reference','impulse_reference','mass_time_reference')):
        raise ValueError('physical or reference identifier missing')
    blocks={role:block(device['blocks'][role],role) for role in ('fit','hold','zero')}
    fit,hold,zero=(blocks[key] for key in ('fit','hold','zero'))
    if fit['D'].lo<=0:raise ValueError('response sign or resolution fails')
    gain=fit['D']/fit['I']
    if not hold['I'].lo>fit['I'].hi:raise ValueError('held-out impulse must exceed fitted level')
    residuals={name:(row['third_D']-gain*row['third_I']) for name,row in blocks.items()}
    if any(not v.overlaps(0) for v in residuals.values()):
        raise ValueError('within-block non-affine residual')
    # The entire holdout envelope must lie inside a predeclared 2% ratio band.
    ratio=hold['D']/(gain*hold['I'])
    if not ratio.inside(around(1,HOLD_TOL)):raise ValueError('held-out gain outside tolerance')
    if not zero['D'].overlaps(0) or not zero['D'].inside(around(0,HOLD_TOL*fit['D'].lo)):
        raise ValueError('zero contrast or resolution fails')
    scale=ell/(2*k*MU*gain)
    inertial=mass*ell.square()/(2*k*MU*dt)
    if not scale.overlaps(inertial):raise ValueError('independent inertial check disagrees')
    return scale,{'device_id':device['device_id'],'S0_kick_Js':scale.data(),'S0_mass_time_Js':inertial.data(),
                  'fit_gain_q_per_Ns':gain.data(),'holdout_gain_ratio':ratio.data(),
                  'zero_contrast_q':zero['D'].data(),'within_block_residuals':{i:v.data() for i,v in residuals.items()}}


def evaluate(data):
    kind=data.get('kind')
    if kind not in ('synthetic','measurement_records','no_observations'):
        raise ValueError('unknown record provenance')
    if kind=='no_observations':
        if data.get('devices'):raise ValueError('empty status with nonempty device records')
        return {'record_kind':kind,'scale_status':'NOT_MEASURED','common_S0_Js':None,
                'preparation_status':'NOT_MEASURED','physical_P3':'60 NOT_RUN'}
    devices=data.get('devices',[])
    if len(devices)!=2 or {F(d['kappa']) for d in devices}!=set(KS):
        raise ValueError('both device settings required')
    by_device={}
    combined=None
    for d in devices:
        scale,row=calibration(d)
        if combined is not None and not combined.overlaps(scale):
            raise ValueError('device scale intervals disjoint')
        combined=scale if combined is None else combined.intersect(scale)
        by_device[str(F(d['kappa']))]=row
    floor=action_floor()
    status='ABOVE' if combined.lo>=floor.hi else 'BELOW' if combined.hi<floor.lo else 'UNRESOLVED'
    return {'record_kind':kind,'scale_status':status,'common_S0_Js':combined.data(),'device_fits':by_device,
            'preparation_status':'NOT_MEASURED','physical_P3':'60 NOT_RUN'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('records',type=Path)
    args=p.parse_args()
    try:
        out=evaluate(json.loads(args.records.read_text()))
    except (KeyError,ValueError,ZeroDivisionError,TypeError) as exc:
        p.exit(2,'INVALID: '+str(exc)+'\n')
    print(json.dumps(out,sort_keys=True,indent=2))
