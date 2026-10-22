"""Replay failed A selections and exhaust the fixed fourth-landmark domain.
No geometry truth enters the exhaustive eligibility audit.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,gzip,hashlib,json,resource,signal,time
from collections import Counter
from pathlib import Path
import numpy as np
from models import PRIOR
from run import encode,save
from selection import select_four as original,pairs_for
from inference import four_geometry,normalize,design
import simulation

HERE=Path(__file__).resolve().parent
LAST=None
def audit(g,counts,selected,cfg):
    global LAST
    old=original(g,counts,selected,cfg)
    fixed=[selected['root']]+selected['support']+selected['landmarks']
    excluded=set(fixed)|set(getattr(g,'probes_for_check',[]));records=[];funnel=Counter()
    for side,cones in [('past',g.pred),('future',g.succ)]:
        common=(1<<g.size)-1
        for b in [selected['root']]+selected['support']:common&=cones[b]
        pool=[]
        while common:
            low=common&-common;common^=low;a=low.bit_length()-1
            if a not in excluded:pool.append(a)
        pool.sort(key=lambda a:g.marks[a])
        for rank,a in enumerate(pool):
            row=dict(candidate=a,side=side,rank=rank,in_original_cap=rank<cfg['candidate_cap_per_side'])
            funnel['pool']+=1
            bad=[b for b in fixed if not(g.r[a,b] or g.r[b,a])]
            if bad:
                row.update(status='INCOMPARABLE',witness=bad[0]);funnel['INCOMPARABLE']+=1;records.append(row);continue
            values=[counts.values(a,b) for b in fixed]
            low=[(b,list(v)) for b,v in zip(fixed,values) if v[0]<counts.guards['guard_min_interval']]
            half=[(b,list(v)) for b,v in zip(fixed,values) if min(v[1:])<counts.guards['guard_min_half_interval']]
            if low or half:
                row.update(status='FULL_COUNT' if low else 'HALF_COUNT',witness=(low or half)[0],minimum_full=min(v[0] for v in values),minimum_half=min(min(v[1:]) for v in values));funnel[row['status']]+=1;records.append(row);continue
            funnel['count_eligible']+=1
            landmarks=selected['landmarks']+[a];nodes=landmarks+[selected['root']]+selected['support']
            p=dict(root=selected['root'],support=selected['support'],temporal=selected['temporal'],landmarks=landmarks,pairs=pairs_for(landmarks,selected['root'],selected['support']),scale=selected['scale'],full_order=g.r[np.ix_(nodes,nodes)].astype(bool))
            q=np.array([counts.q(a,b) for a,b in p['pairs']])/selected['scale']**2
            h,z,_,_=four_geometry(q,p)
            try:
                _,condition=normalize(h);row['landmark_condition']=condition
                if condition>cfg['maximum_landmark_condition']:raise ValueError('landmark condition')
                funnel['lorentz_eligible']+=1;D=design(z[5:]);dc=float(np.linalg.cond(D));row['design_condition']=dc if np.isfinite(dc) else None
                if np.linalg.matrix_rank(D)!=9 or dc>cfg['maximum_design_condition']:raise ValueError('moment rank/condition')
                row['status']='ELIGIBLE';funnel['eligible']+=1
                row.update(packet=p,counts=[counts.values(a,b) for a,b in p['pairs']])
            except (ValueError,np.linalg.LinAlgError) as exc:row.update(status='GEOMETRY_HOLD',reason=str(exc));funnel['GEOMETRY_HOLD']+=1
            records.append(row)
    # Every member of both complete pools has one explicit decision/witness.
    assert len(records)==funnel['pool']
    assert not any(r['status']=='ELIGIBLE' and r['in_original_cap'] for r in records)
    LAST=dict(original=old,funnel=dict(funnel),records=records,exhausted=True)
    return old

def main():
    ap=argparse.ArgumentParser();ap.add_argument('worker',type=int,choices=[0,1]);a=ap.parse_args()
    from runner import verify_freeze
    verify_freeze();c=json.loads((HERE/'contract.json').read_text());oldc=json.loads((PRIOR/'contract.json').read_text());simulation.select_four=audit
    def alarm(*_):raise TimeoutError('selection audit worker budget')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(1200);begin=time.monotonic();records=[]
    for index in c['selection_failure_indices'][a.worker::2]:
        path=PRIOR/f'results/cloud-{index:02d}.json.gz';raw=path.read_bytes();r=json.loads(gzip.decompress(raw));t=time.monotonic()
        selection,_=simulation.selection_cloud(r['seed'],oldc)
        assert encode(selection)==encode(r['selection']),'A replay mismatch'
        out=dict(index=index,seed=r['seed'],source_sha256=hashlib.sha256(raw).hexdigest(),selection_identical=True,seconds=time.monotonic()-t,**LAST)
        save(HERE/f'selection/cloud-{index:02d}.json.gz',out);records.append(dict(index=index,seconds=out['seconds'],funnel=out['funnel']))
        print(json.dumps(records[-1]),flush=True)
    signal.alarm(0);save(HERE/f'selection/worker-{a.worker}.json',dict(status='COMPLETE',seconds=time.monotonic()-begin,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,records=records))

if __name__=='__main__':main()
