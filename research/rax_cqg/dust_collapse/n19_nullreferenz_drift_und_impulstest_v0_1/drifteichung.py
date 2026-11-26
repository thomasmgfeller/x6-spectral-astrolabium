"""Fit a positive impulse gain with an independent quadratic background in each block."""
import argparse
import json
from fractions import Fraction as F
from itertools import combinations,product
from math import prod
from pathlib import Path

PATTERN=(1,-1,-1,1,-1,1,1,-1)


def coefficients(times):
    return [1/prod(t-u for j,u in enumerate(times) if j!=i) for i,t in enumerate(times)]


def raw_block(rows,role):
    from eichen import sample
    from intervall import interval,around
    if len(rows)!=8:
        raise ValueError('eight complete observations required')
    data=[]
    for row,sign in zip(rows,PATTERN):
        d,k,t=sample(row)
        bound=F(row['nonquadratic_error_q'])
        if bound<0 or not str(row.get('error_reference','')).strip():
            raise ValueError('bounded residual and its reference are required')
        if role=='zero':
            if k.data()!=['0','0']:
                raise ValueError('drive in zero block')
        elif (sign*k).lo<=0:
            raise ValueError('effective impulse inconsistent with registered polarity')
        data.append((t,d+around(0,bound),k))
    if any(b[0]<=a[0] for a,b in zip(data,data[1:])):
        raise ValueError('times must increase strictly')
    return data


def constraints(block):
    from intervall import interval
    for subset in combinations(block,4):
        cs=coefficients([t for t,_,_ in subset])
        d=sum((c*row[1] for c,row in zip(cs,subset)),interval(0))
        k=sum((c*row[2] for c,row in zip(cs,subset)),interval(0))
        yield d,k


def polynomial_witness(block,g):
    # At fixed g, each allowed quadratic is an intersection of 8 parallel-plane pairs.
    # Three distinct times determine its three coefficients. A bounded nonempty
    # polytope has a vertex, including when it is lower dimensional.
    bands=[(t,d-g*k) for t,d,k in block]
    for triple in combinations(bands,3):
        for sides in product(('lo','hi'),repeat=3):
            abc=[F(0)]*3
            for i,(t,band) in enumerate(triple):
                u,v=[row[0] for j,row in enumerate(triple) if i!=j]
                a=getattr(band,sides[i])/((t-u)*(t-v))
                for j,val in enumerate((u*v,-u-v,1)):
                    abc[j]+=a*val
            if all(b.lo<=abc[0]+t*(abc[1]+t*abc[2])<=b.hi for t,b in bands):
                return list(map(str,abc))
    raise ValueError('no quadratic background at claimed gain')


def gain_interval(block):
    from intervall import I
    low,high=F(0),None
    for d,k in constraints(block):
        # A nonnegative gain is compatible only if d.lo <= g*k.hi and g*k.lo <= d.hi.
        for a,b in ((-k.hi,-d.lo),(k.lo,d.hi)):
            if a==0:
                if b<0:raise ValueError('nonquadratic residual exceeds registered allowance')
            elif a<0:low=max(low,b/a)
            else:high=b/a if high is None else min(high,b/a)
    if high is None or low<=0 or high<low:
        raise ValueError('unresolved gain or incompatible residual bounds')
    # Feasible endpoints and convexity certify that every intermediate g is feasible.
    return I(low,high),[polynomial_witness(block,g) for g in (low,high)]


def null_resolution(block,fit):
    # A divided difference normalized by its response to the registered signs.
    from intervall import interval
    candidates=[]
    for indices in combinations(range(8),4):
        cs=coefficients([block[i][0] for i in indices])
        sensitivity=abs(sum(PATTERN[i]*c for i,c in zip(indices,cs)))
        if sensitivity:
            resolution=sum(abs(c) for c in cs)/sensitivity
            candidates.append((resolution,indices,cs,sensitivity))
    _,indices,cs,sensitivity=min(candidates,key=lambda r:(r[0],r[1]))
    sig=sum((c*block[i][1] for i,c in zip(indices,cs)),interval(0))/sensitivity
    minimum_impulse=min((s*k).lo for s,(_,_,k) in zip(PATTERN,fit))
    return max(abs(sig.lo),abs(sig.hi))/minimum_impulse


def evaluate(doc):
    from eichen import KS,MU,action_floor
    from intervall import interval,around
    kind=doc.get('kind')
    if kind=='no_observations' and not doc.get('devices'):
        return {'record_kind':kind,'scale_status':'NOT_MEASURED','common_S0_Js':None,'physical_P3':'60 NOT_RUN'}
    devices=doc['devices']
    if kind not in ('synthetic','measurement_records') or len(devices)!=2 or {F(d['kappa']) for d in devices}!=set(KS):
        raise ValueError('two registered devices and data origin required')
    combined=None
    fits={}
    for d in devices:
        k=F(d['kappa'])
        if not all(d.get(f) for f in ('device_id','length_reference','impulse_reference','mass_time_reference')):
            raise ValueError('missing independent reference')
        ell,mass,dt=map(interval,[d['metres_per_q'],d['kg'],d['seconds_per_step']])
        if min(ell.lo,mass.lo,dt.lo)<=0:raise ValueError('nonpositive physical reference')
        fit,hold,zero=(raw_block(d['blocks'][role],role) for role in ('fit','hold','zero'))
        g,witness=gain_interval(fit)
        hg,_=gain_interval(hold)
        if min((s*a[2]).lo for s,a in zip(PATTERN,hold))<=max((s*a[2]).hi for s,a in zip(PATTERN,fit)):
            raise ValueError('independent held-out level must be larger')
        if not (hg/g).inside(around(1,F(1,50))):
            raise ValueError('holdout gain not contained within two percent')
        polynomial_witness(zero,F(0))
        if null_resolution(zero,fit)>g.lo/50:
            raise ValueError('null control too coarse')
        kick=ell/(2*k*MU*g)
        inertial=mass*ell.square()/(2*k*MU*dt)
        if not kick.overlaps(inertial):raise ValueError('inertial reference disagrees')
        joint=kick.intersect(inertial)
        if combined is not None and not joint.overlaps(combined):
            raise ValueError('device scales disagree')
        combined=joint if combined is None else combined.intersect(joint)
        fits[str(k)]={'device_id':d['device_id'],'gain':g.data(),'kick_S0_Js':kick.data(),'inertial_S0_Js':inertial.data(),
                      'hold_ratio':(hg/g).data(),'fit_endpoint_quadratics':witness}
    floor=action_floor()
    result='ABOVE' if combined.lo>=floor.hi else 'BELOW' if combined.hi<floor.lo else 'UNRESOLVED'
    return {'record_kind':kind,'scale_status':result,'common_S0_Js':combined.data(),'fits':fits,'weak_device_id':fits[str(min(KS))]['device_id'],'physical_P3':'60 NOT_RUN'}


if __name__=='__main__':
    from basisdaten import inputs
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records',type=Path)
    args=parser.parse_args()
    try:
        with inputs():
            report=evaluate(json.loads(args.records.read_text()))
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as exc:
        parser.exit(2,'INVALID: '+str(exc)+'\n')
    print(json.dumps(report,sort_keys=True,indent=2))
