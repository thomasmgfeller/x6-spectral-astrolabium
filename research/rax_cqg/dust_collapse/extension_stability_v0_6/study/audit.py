"""Independent checks of archived detector effects and of six feasible witness paths."""
from common import HERE, setup, archived, load, coherent, prior
import numpy as np
import json
from exact import jsonread

def run():
    names,reach=setup();old=archived()
    baseline=load('upstream/results.json')
    pilot=load('readout14_extra.json')
    growth=load('growth.json')
    g=np.load(HERE/'gram.npy'); ids=[names.index(n) for n in pilot['branch_order']]
    g=g[:,ids][:,:,ids]; checks={}; extra=jsonread('direct.json')
    assert len(names)==169 and len(old)==40 and len(extra)==24
    for name,data in extra.items():
        assert data['cartesian_error']<1e-13
    for tag,idx in [('coarse',-2),('fine',-1)]:
        amps=np.array([coherent(old[n][idx]) for n in pilot['branch_order']]).T
        err=0.
        for d,z in enumerate(amps):
            ac=(g*z.conj()[None,:,None]*z[None,None,:]).real
            four=np.concatenate((ac,(1-ac.sum(axis=0))[None]),axis=0)
            err=max(err,float(np.max(abs(four[:,:30,:30]-baseline['coherent_readout_grid_matrices'][tag][d]))),
                    float(np.max(abs(four[:,30:,:]-pilot['grids'][tag]['new_coherent_rows'][d]))))
        assert err<5e-14
        zall=np.array([coherent(old[n][idx]) for n in old]+
                      [[complex(*p) for p in branch['rows'][tag]] for branch in extra.values()])
        dif=abs(zall[:,1]*np.exp(1j*151/304)-zall[:,0])
        assert max(dif)<.001812 and np.max(abs(zall))<.036085
        checks[tag]={'archived_40x40_max_error':err,'max_rephased_difference_known':float(max(dif))}
    keys=[prior.key(n) for n in names]
    mids={k for k in keys if k[0]==4};end={k for k in keys if k[0]==5}
    paths={}
    for root in keys[:2]:
        for goal in (734,760,8191):
            valid=[(p[1],q[1]) for p in prior.branch_splits(root,mids,'marked')
                   for q in prior.branch_splits(p,end,'marked')
                   if growth['parents'][str(q[1])].get(str(goal),0)>0]
            assert valid
            mid,pen=min(valid)
            paths[f'{root[1]} to {goal}']=[f'N11_{root[1]}',f'N12_{mid}',f'N13_{pen}',f'N14_{goal}']
    assert max(abs(complex(*z)-complex(*w)) for b in extra.values() for z,w in
               zip(b['rows']['coarse'],b['rows']['fine']))<1e-7
    return {'checks':checks,'witness_paths':paths,
            'max_direct_grid_amplitude_difference':max(abs(complex(*z)-complex(*w)) for b in extra.values()
            for z,w in zip(b['rows']['coarse'],b['rows']['fine'])),
            'max_small_grid_cartesian_error':max(b['cartesian_error'] for b in extra.values())}

if __name__=='__main__':
    result=run()
    (HERE/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
