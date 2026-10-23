"""Two frozen overlap resolutions for the 78 remaining three-support boxes.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'triple_tail'))
from tt_common import *
from tt_common import combined as source_combined, frozen as source_frozen
HERE=Path(__file__).resolve().parent

def frozen():
    source_frozen()
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def inputs():
    ar=read(HERE.parent/'triple_tail/certificates.json.gz');previous=read(HERE.parent/'triple_tail/summary.json')
    source=source_combined(ar);pending=[r for r in source if r['status']=='HOLD']
    missing=[r for r in pending if 'anchor' not in r];prior=[r for r in pending if 'anchor' in r]
    assert len(source)==960 and len(pending)==78 and len(missing)==15 and len(prior)==63
    assert previous['excluded_volume_fraction']=='3787/4096'
    assert all('base_statistics' in r and 'moved_statistics' in r for r in prior)
    return ar,previous,source,pending,missing,prior

def pending_refinement(first):
    _,_,_,pending,_,_=inputs();active={r['path']:r for r in pending}
    for r in first:
        assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    return sorted((r for r in active.values() if r['status']=='HOLD'),key=path_key)

def combined(ar):
    _,_,source,_,_,_=inputs();active={r['path']:r for r in source}
    for stage in ('missing','refined'):
        for r in ar[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    return sorted(active.values(),key=path_key)

def cached_event(b,row,c,stage,laws,cache):
    choices=overlap_candidates(b,list(map(F,row['box'])));slices=c['slices'][stage]
    if not choices:return dict(path=row['path'],box=row['box'],stage=stage,status='HOLD',reason='NO_TIMELIKE_PAIR_ANCHOR')
    e=choices[0]
    if stage=='refined' and 'anchor' in row:
        assert all(row[k]==e[k] for k in ('pair','anchor','side','threshold'))
        assert row['base_statistics']==e['base'] and row['moved_statistics']==e['moved']
    ids=[];settings=dict(c['overlap'],overlap_slices=slices)
    for stats in (e['base'],e['moved']):
        key=json.dumps([stage,slices,e['pair'],e['anchor'],e['threshold'],stats],sort_keys=True,separators=(',',':'))
        if key not in cache:
            cache[key]=len(laws)
            laws.append(dict(stage=stage,slices=slices,pair=e['pair'],anchor=e['anchor'],threshold=e['threshold'],statistics=stats,
                             law=enclose_difference(stats,e['threshold'],settings)))
        ids.append(cache[key])
    a,d=[tuple(map(F,laws[i]['law']['probability'])) for i in ids];tv=max(F(0),a[0]-d[1],d[0]-a[1])
    return dict(path=row['path'],box=row['box'],stage=stage,slices=slices,status='OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD',
                pair=e['pair'],anchor=e['anchor'],side=e['side'],threshold=e['threshold'],score=str(e['score']),
                base_statistics=e['base'],moved_statistics=e['moved'],base_law_id=ids[0],moved_law_id=ids[1],tv_lower=outward(tv)[0])

def evaluate_stage(b,rows,c,stage,laws,cache):
    result=[]
    for r in rows:
        v=cached_event(b,r,c,stage,laws,cache);result.append(v)
        print(json.dumps(dict(stage=stage,cells=len(result),total=len(rows),path=v['path'],status=v['status'],tv_lower=v.get('tv_lower'),distinct_laws=len(laws))),flush=True)
    return result
