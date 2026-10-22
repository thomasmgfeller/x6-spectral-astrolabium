"""Simulation boundary: generate A once; pass only intrinsic inputs to selectors.
The A construction is copied from the pinned original simulation.py unchanged.
SPDX-License-Identifier: Apache-2.0
"""
import gc
import time
import eb_common
import numpy as np
from simulation import (config, core, estimator, experiment, weighting, shell,
    PhysicalPoset, relation, select, audit, Counts, digest, counting_cloud)
from selection import select_four as legacy
from selector import select_four as candidate

def selection_pair(seed, contract):
    rho=contract['selection_density']; c,oc,guards,cfg=config()
    z,r,marks,bottom,top=experiment.sprinkle(rho,seed)
    ni=len(z); probes=[bottom,top]
    gi=core.Poset(r,marks)
    baseline=weighting.reweight(gi,estimator.neighborhood(gi,rho,bottom,top,cfg),rho,cfg['coefficient_C'])
    root,chain=baseline['root'],baseline['chain']; scale=baseline['tau_m']
    del gi,r
    colours=np.random.default_rng(seed^guards['colour_seed_xor']).integers(0,2,size=ni,dtype=np.uint8)
    for index,(lo,hi) in enumerate(zip(oc['outer_durations'][:-1],oc['outer_durations'][1:]),1):
        zz,mm,cc,_=shell(rho,seed,index,lo,hi,oc)
        z=np.vstack((z,zz)); marks=np.r_[marks,mm]; colours=np.r_[colours,cc]
    if len(z)>c['maximum_points']: raise MemoryError('A point budget')
    g=PhysicalPoset(relation(z,c['relation_block_rows']),marks,probes); g.probes_for_check=probes
    inner=[i for i in range(ni) if i not in probes]
    selected=select(g,root,chain,inner,probes,colours,rho,c,guards,scale)
    hidden=np.random.default_rng(np.random.SeedSequence([seed,c['audit_colour_seed_tag']])).integers(0,2,size=g.size,dtype=np.uint8)
    audited=audit(g,selected['selected'],hidden,rho,guards)
    arms={}; private={}; times={}
    for name,fn in [('legacy',legacy),('candidate',candidate)]:
        start=time.monotonic()
        fourth=fn(g,Counts(g,colours,rho,guards),selected['selected'],contract['selection']) if audited['passed'] else dict(status='BASE_AUDIT_HOLD')
        times[name]=time.monotonic()-start; arms[name]=fourth
        if fourth['status']=='SELECTED':
            p=fourth['packet']; ids=p['landmarks']+[p['root']]+p['support']
            private[name]=dict(ids=ids,points=z[ids].copy())
    old,new=arms['legacy'],arms['candidate']
    if old['status']=='SELECTED':
        assert new['status']=='SELECTED', 'availability monotonicity'
        old_id=old['packet']['landmarks'][3]
        assert any(r['candidate']==old_id and r.get('geometry_status')=='ELIGIBLE' for r in new['inventory'])
        assert new['landmark_condition'] <= old['landmark_condition']*(1+1e-12)
    record=dict(arms=arms,base_audit=audited['passed'],physical_count=len(z)-2,
        coordinates_sha256=digest(z),relation_sha256=digest(g.r),baseline_selected=selected['selected'],
        base_selection_funnel=[{k:v for k,v in row.items() if k!='trials'} for row in selected['shells']],
        selector_seconds=times)
    del g; gc.collect()
    return record,private
