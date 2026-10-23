"""Two frozen overlap resolutions on the final 31 paired-surface rectangles.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'surface_tail'))
from sft_common import (F,read,save,outward,setup,area,overlap_candidates,overlap,
    Counter,mean_bounds,interval,moved,boosted)
from sft_common import combined as source_combined, frozen as source_frozen
HERE=Path(__file__).resolve().parent

def frozen():
    source_frozen()
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def path_key(r):return tuple(map(int,r['path'].split('/')))

def inputs():
    source=read(HERE.parent/'surface_tail/certificates.json.gz')
    previous=read(HERE.parent/'surface_tail/summary.json')
    final=source_combined(source);pending=[r for r in final if r['status']=='HOLD']
    assert len(final)==2104 and len(pending)==31
    assert all(area(r)==F(1,409600) for r in pending)
    missing=[r for r in pending if 'anchor' not in r]
    old=[r for r in pending if 'anchor' in r]
    assert len(missing)==16 and len(old)==15
    assert all('base_law' in r and 'moved_law' in r for r in old)
    return previous,final,pending,missing,old

def stage_contract(c,stage):
    v=dict(c);v['overlap']=dict(c['overlap'],overlap_slices=c['slices'][stage]);return v

def pending_refinement(missing_results):
    _,_,pending,_,_=inputs();active={r['path']:r for r in pending}
    for r in missing_results:
        assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box']
        active[r['path']]=r
    return sorted((r for r in active.values() if r['status']=='HOLD'),key=path_key)

def combined(archive):
    _,old,_,_,_=inputs();active={r['path']:r for r in old}
    for stage in ('missing','refined'):
        for r in archive[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box']
            active[r['path']]=r
    return sorted(active.values(),key=path_key)

def evaluate_stage(b,rows,c,stage,bases):
    settings=stage_contract(c,stage);cache={};base_ids={};results=[]
    for r in rows:
        result=overlap(b,r,settings,cache)
        if 'base_law' in result:
            key=(result['anchor'],result['threshold']);law=result.pop('base_law')
            if key not in base_ids:
                base_ids[key]=len(bases)
                bases.append(dict(stage=stage,slices=c['slices'][stage],anchor=key[0],threshold=key[1],law=law))
            result['base_law_id']=base_ids[key]
        results.append(result)
        print(json.dumps(dict(stage=stage,cells=len(results),total=len(rows),path=r['path'],status=result['status'],tv_lower=result.get('tv_lower'))),flush=True)
    return results
