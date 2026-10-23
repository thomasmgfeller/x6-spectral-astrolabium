"""Fixed-budget missing-event pass on the existing three-support cube.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'triple_cube'))
from tc_common import *
from tc_common import frozen as parent_frozen, final_cells as parent_final
HERE=Path(__file__).resolve().parent

def frozen():
    parent_frozen()
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def inputs():
    ar=read(HERE.parent/'triple_cube/certificates.json.gz')
    summary=read(HERE.parent/'triple_cube/summary.json');final=parent_final(ar)
    tested={r['path'] for stage in ('marginal','overlap') for r in ar[stage]}
    pending=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD' and r['path'] not in tested]
    assert len(final)==960 and len(pending)==398 and sum(r['status']=='HOLD' for r in final)==421
    assert summary['excluded_volume_fraction']=='2989/4096'
    return ar,summary,final,pending

def law_key(pair,anchor,threshold,stats):
    return json.dumps([pair,anchor,threshold,stats],sort_keys=True,separators=(',',':'))

def cached_overlap(b,row,c,laws,cache):
    choices=overlap_candidates(b,list(map(F,row['box'])))
    if not choices:return dict(row,status='HOLD',reason='NO_TIMELIKE_PAIR_ANCHOR')
    e=choices[0];ids=[]
    for stats in (e['base'],e['moved']):
        key=law_key(e['pair'],e['anchor'],e['threshold'],stats)
        if key not in cache:
            cache[key]=len(laws)
            laws.append(dict(pair=e['pair'],anchor=e['anchor'],threshold=e['threshold'],statistics=stats,
                             law=enclose_difference(stats,e['threshold'],c['overlap'])))
        ids.append(cache[key])
    a,d=[tuple(map(F,laws[i]['law']['probability'])) for i in ids]
    tv=max(F(0),a[0]-d[1],d[0]-a[1])
    return dict(path=row['path'],box=row['box'],status='OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD',
                pair=e['pair'],anchor=e['anchor'],side=e['side'],threshold=e['threshold'],score=str(e['score']),
                base_statistics=e['base'],moved_statistics=e['moved'],base_law_id=ids[0],moved_law_id=ids[1],tv_lower=outward(tv)[0])

def combined(ar):
    _,_,old,_=inputs();active={r['path']:r for r in old}
    for stage in ('marginal','overlap'):
        for r in ar[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box']
            active[r['path']]=r
    return sorted(active.values(),key=path_key)

def event_coverage(ar):
    marg={r['path'] for r in ar['marginal'] if any('event_id' in a for a in r['attempts'])}
    overlap={r['path'] for r in ar['overlap'] if 'reason' not in r and all(ar['overlap_laws'][r[k]]['law']['status']=='ENCLOSED' for k in ('base_law_id','moved_law_id'))}
    return marg,overlap
