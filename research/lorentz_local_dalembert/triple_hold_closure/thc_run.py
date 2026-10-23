"""Frozen deterministic subdivision with inherited exact certification gates.
SPDX-License-Identifier: Apache-2.0
"""
from thc_common import *
import argparse, multiprocessing, time
from concurrent.futures import ProcessPoolExecutor

_B=None;_C=None;_INVS=None;_STRIPS=None;_CACHE=None
def initialize(c):
    global _B,_C,_INVS,_STRIPS,_CACHE
    _C=c;_B=setup(c);_INVS,_STRIPS=transport_inventory();_CACHE={}
def geometric(row):
    return dict(row,**classify(_B,list(map(F,row['box'])),_C,_INVS,_STRIPS,_CACHE))

def run(workers=1,verify=False):
    frozen();c=read(HERE/'contract.json');src,pending=original();active={r['path']:r for r in src}
    b=setup(c);total_cells=0;rounds=[]
    with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('fork'),initializer=initialize,initargs=(c,)) as pool:
        for level in range(1,c['maximum_rounds']+1):
            pending=sorted((r for r in active.values() if r['status']=='HOLD'),key=path_key)
            if not pending:break
            if total_cells+8*len(pending)>c['maximum_new_geometric_cells']:break
            child=[r for parent in pending for r in children(parent)]
            rows=[];start=time.monotonic()
            for row in pool.map(geometric,child,chunksize=1):
                rows.append(row)
                if len(rows)%32==0:print(json.dumps(dict(level=level,geometry=len(rows),total=len(child),states=dict(Counter(r['status'] for r in rows)))),flush=True)
            events=[];marginals=[];laws=[];overlaps=[];mc={};oc={}
            left=sorted((r for r in rows if r['status']=='HOLD'),key=path_key)
            for r in left:marginals.append(marginal(b,r,c,events,mc))
            left=[r for r in marginals if r['status']=='HOLD']
            print(json.dumps(dict(level=level,geometric_states=dict(Counter(r['status'] for r in rows)),overlap_inputs=len(left))),flush=True)
            for r in left:
                v=cached_overlap(b,r,c,laws,oc);overlaps.append(v)
                print(json.dumps(dict(level=level,overlap=len(overlaps),total=len(left),path=v['path'],status=v['status'],tv_lower=v.get('tv_lower'))),flush=True)
            ar=dict(splits=[r['path'] for r in pending],cells=rows,marginal_events=events,marginal=marginals,overlap_laws=laws,overlap=overlaps)
            target=HERE/('round_%02d.json.gz'%level)
            if verify:assert ar==read(target),str(target)
            else:save(target,ar)
            active=replace_round(active,ar);total_cells+=len(rows)
            hold=[r for r in active.values() if r['status']=='HOLD']
            rec=dict(level=level,source_hold_cells=len(pending),child_cells=len(rows),geometric_states=dict(Counter(r['status'] for r in rows)),remaining_cells=len(hold),hold_volume=str(sum((volume(r) for r in hold),F(0))),marginal_input_cells=len(marginals),overlap_input_cells=len(overlaps),distinct_marginal_events=len(events),distinct_overlap_laws=len(laws))
            rounds.append(rec);print(json.dumps(dict(round_complete=rec,seconds=time.monotonic()-start)),flush=True)
    final=sorted(active.values(),key=path_key);states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    held=volumes['HOLD'];assert sum(volumes.values())==F(1,125)
    closed=[p['path'] for p in original()[1] if not any(r['status']=='HOLD' and (r['path']==p['path'] or r['path'].startswith(p['path']+'/')) for r in final)]
    result=dict(status='THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE',rounds=rounds,evaluated_new_geometric_cells=total_cells,source_hold_cells=38,source_exclusions_preserved=1314,closed_source_hold_cells=len(closed),closed_source_paths=closed,terminal_cells=len(final),states=dict(states),volumes={k:str(v) for k,v in volumes.items()},hold_volume=str(held),excluded_volume_fraction=str(1-held*125),unresolved_cells=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD'],scope=c['scope'])
    if verify:assert result==read(HERE/'summary.json')
    else:save(HERE/'summary.json',result)
    print(json.dumps(result),flush=True)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=1);ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    run(args.workers,args.verify)
