"""Finite combinatorial control and physical exact-geometry counterexample.
SPDX-License-Identifier: Apache-2.0
"""
from types import SimpleNamespace
import itertools
import numpy as np
from eb_common import HERE, read, save
from selector import eligible_prefix,select_four
from selection import select_four as old

def main():
    checks=[]
    def check(name,value,details=None):
        assert value,name
        checks.append(dict(name=name,passed=bool(value),details=details))
    tested=0
    for n in range(13):
        for flags in itertools.product([False,True],repeat=n):
            pool=list(range(n))
            for cap in range(1,5):
                before=set(a for a in pool[:cap] if flags[a]); after=set(eligible_prefix(pool,lambda a:flags[a],cap))
                assert before<=after
                tested+=1
    check('old_eligible_subset_finite_exhaustion',True,tested)
    rng=np.random.default_rng(782083)
    anchors=np.array([[-8,0,0],[-10,1,0],[-12,0,1],[-15,.2,.3]])
    supports=np.column_stack((np.r_[-2.,2.,rng.uniform(-4,-1,9),rng.uniform(1,4,9)],rng.uniform(-.4,.4,(20,2))))
    # Last point is common-past but deliberately fails full/half counts.
    points=np.vstack((anchors,np.zeros(3),supports,[-6.,.1,.1])); delta=points[None]-points[:,None]
    q=delta[:,:,0]**2-delta[:,:,1]**2-delta[:,:,2]**2; order=(delta[:,:,0]>0)&(q>0)
    marks=np.arange(len(points),dtype=float); marks[-1]=-1.
    g=SimpleNamespace(size=len(points),r=order,marks=marks,probes_for_check=[])
    g.pred=[sum(1<<int(i) for i in np.flatnonzero(order[:,j])) for j in range(g.size)]
    g.succ=[sum(1<<int(i) for i in np.flatnonzero(order[j])) for j in range(g.size)]
    class Exact:
        guards=dict(guard_min_interval=16,guard_min_half_interval=4)
        mode='full'
        def values(self,a,b):
            if len(points)-1 in [a,b]:return (15,7,8) if self.mode=='full' else (20,3,17)
            return (100,50,50)
        def q(self,a,b):return q[a,b]
        def good(self,a,b):
            n,x,y=self.values(a,b); return n>=16 and min(x,y)>=4
    selected=dict(root=4,support=list(range(5,25)),temporal=[5,6],landmarks=[0,1,2],scale=1.)
    cfg={**read(HERE/'contract.json')['selection'],'candidate_cap_per_side':1}
    counts=Exact(); legacy=old(g,counts,selected,cfg); new=select_four(g,counts,selected,cfg)
    check('early_cap_counterexample_repaired',legacy['status']=='NO_FOUR_LANDMARK_FRAME' and new['status']=='SELECTED' and new['packet']['landmarks'][3]==3)
    check('minimum_full_count_not_relaxed',any(r['status']=='FULL_COUNT' for r in new['inventory']))
    counts.mode='half'; half=select_four(g,counts,selected,cfg)
    check('minimum_half_count_not_relaxed',any(r['status']=='HALF_COUNT' for r in half['inventory']) and half['status']=='SELECTED')
    tight=select_four(g,counts,selected,{**cfg,'maximum_design_condition':1.})
    check('moment_condition_still_blocks',tight['status']=='NO_FOUR_LANDMARK_FRAME')
    check('no_base_support_hold',select_four(g,counts,None,cfg)['status']=='NO_BASE_SUPPORT')
    # Stable marks retained through arbitrary IDs: preserve the physical choice.
    perm=rng.permutation(g.size); inverse=np.argsort(perm)
    gp=SimpleNamespace(size=g.size,r=g.r[np.ix_(inverse,inverse)],marks=g.marks[inverse],probes_for_check=[])
    gp.pred=[sum(1<<int(i) for i in np.flatnonzero(gp.r[:,j])) for j in range(gp.size)]
    gp.succ=[sum(1<<int(i) for i in np.flatnonzero(gp.r[j])) for j in range(gp.size)]
    class Relabel(Exact):
        def values(self,a,b):return counts.values(int(inverse[a]),int(inverse[b]))
        def q(self,a,b):return counts.q(int(inverse[a]),int(inverse[b]))
    mapped={k:([int(perm[x]) for x in v] if isinstance(v,list) else int(perm[v]) if k=='root' else v) for k,v in selected.items()}
    relabel=select_four(gp,Relabel(),mapped,cfg)
    check('node_relabeling_preserves_physical_landmark',relabel['status']=='SELECTED' and relabel['packet']['landmarks'][3]==int(perm[3]))
    save(HERE/'controls.json',dict(status='PASS',checks=checks,scope='Synthetic exact-interval fixture, not a Poisson observation; bounded finite subset proof test supplements the general argument.'))
    print('PASS',len(checks),'controls;',tested,'prefix cases')

if __name__=='__main__':main()
