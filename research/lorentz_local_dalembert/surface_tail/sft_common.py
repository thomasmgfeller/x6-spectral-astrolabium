"""Fixed-budget tail coverage for the 744 previously untested surface cells.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'paired_surface'))
from ps_run import (F,read,save,outward,setup,area,priority,final_cells,marginal_candidates,
                    overlap_candidates,overlap,event_certificate,Counter,qrange,mean_bounds,
                    interval,moved,boosted,sqrt_bounds,statistics)
HERE=Path(__file__).resolve().parent

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def inputs():
    archive=read(HERE.parent/'paired_surface/certificates.json.gz');summary=read(HERE.parent/'paired_surface/summary.json')
    final=final_cells(archive);tested={r['path'] for stage in ('marginal','overlap') for r in archive[stage]}
    pending=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD' and r['path'] not in tested]
    assert len(pending)==744 and sum(r['status']=='HOLD' for r in final)==775
    assert all(area(r)==F(1,409600) for r in pending)
    return archive,summary,final,pending

def marginal(b,row,c,events,cache):
    attempts=[]
    for v in marginal_candidates(b,list(map(F,row['box'])))[:c['maximum_marginal_events_per_cell']]:
        a,d=v['base'],v['moved'];reason=None
        if max(a+d)>c['poisson']['maximum_mean']:reason='HOLD_RATE_BUDGET'
        elif not (a[1]<d[0] or d[1]<a[0]):reason='HOLD_OVERLAPPING_MEAN_BOUNDS'
        if reason:
            attempts.append(dict(index=v['index'],score=str(v['score']),reason=reason));continue
        key=(v['index'],a,d)
        if key not in cache:
            try:cert=event_certificate(a,d,c['poisson'])
            except AssertionError:
                attempts.append(dict(index=v['index'],score=str(v['score']),reason='HOLD_EVENT_BUDGET'));continue
            cache[key]=len(events);events.append(dict(index=v['index'],base=list(map(str,a)),moved=list(map(str,d)),certificate=cert))
        event_id=cache[key];attempts.append(dict(event_id=event_id,score=str(v['score'])))
        if F(events[event_id]['certificate']['full_law_tv_lower'])>F(c['tv_gate']):
            return dict(row,status='MARGINAL_TAIL_EXCLUDED',attempts=attempts)
    return dict(row,status='HOLD',attempts=attempts)

def overlap_priority(b,row):
    choices=overlap_candidates(b,list(map(F,row['box'])))
    return (-(choices[0]['score'] if choices else F(0)),tuple(map(int,row['path'].split('/'))))

def combined(archive):
    _,_,old,_=inputs();active={r['path']:r for r in old}
    for stage in ('marginal','overlap'):
        for r in archive[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box']
            active[r['path']]=r
    return sorted(active.values(),key=lambda r:tuple(map(int,r['path'].split('/'))))
