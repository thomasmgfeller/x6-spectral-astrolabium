"""Assemble the all-geometry coherent readout and fixed-weight comparisons."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
import numpy as np
from quadrature import ROOT, decode, flat
from analyze import matrices, probabilities, assess, transfer, branch_splits
from orders import ROOTS, orbit_table, label, paths, screen, daughter_counts, scalar_layouts, geometry
from path_laws import summarize_paths
from abel_check import numerical_state


def weights_array(named, names):
    return np.array([float(named.get(k,0)) for k in names])


def reconstruct(grids):
    prior=json.loads((ROOT/'v03/results.json').read_text())
    original=json.loads((ROOT/'v03/clocks_n13.json').read_text())
    earlier=json.loads((ROOT/'v03/upstream/v02_grids.json').read_text())
    histories=paths()
    audit,states=screen(histories)
    parents=[(3,orbit_table(3)[r]) for r in ROOTS.values()]
    mids=sorted(k for k in states if k[0]==4)
    ends=sorted({(5,g) for h in mids for g in daughter_counts(h) if (5,g) in states})
    assert {label(k) for k in ends}==set(grids)==set(prior['width_per_sequential_type'])
    names=parents+mids+ends
    oldnames={**dict(zip(parents,ROOTS)),**{h:f'poset{h[1]:02d}_lift' for h in mids}}
    geometry.mp.mp.dps=80
    abel={}
    with scalar_layouts():
        for k in ends:
            p,phase=numerical_state(k,geometry.mp.mpf('1e-28'))
            p0,norm=states[k]
            abel[label(k)]=[float(max(abs(x) for x in p-p0)),float(abs(phase-norm/abs(norm)))]
            assert max(abel[label(k)])<1e-17
    stored={}
    for i,tag in ((-2,'coarse'),(-1,'fine')):
        amp={k:decode(earlier['grids'][v][i]['amplitudes']) for k,v in oldnames.items()}
        amp.update({k:decode(grids[label(k)]['grids'][i]['amplitudes']) for k in ends})
        stored[tag]=matrices(names,states,amp)
    max_difference=max(float(np.max(abs(v-stored['coarse'][k]))) for k,v in stored['fine'].items())
    idx=[list(map(label,names)).index(k) for k in prior['branch_order']]
    old_delta=float(np.max(abs(stored['fine']['coherent'][:,:,idx,:][:,:,:,idx]-prior['outcome_matrices_fine_coherent'])))
    old_clock=max(float(max(abs(flat(decode(original[k]['grids'][-1]['amplitudes']))-
                                flat(decode(grids[k]['grids'][-1]['amplitudes']))))) for k in original)
    assert max(max_difference,old_delta)<5e-12 and old_clock<3e-10
    path_rows={}
    for name,fam in histories.items():
        row=summarize_paths(name,fam,states)
        assert row==prior['paths_by_root'][name]
        path_rows[name]=row
    info={'admissible_end_without_admissible_intermediate':[label(k) for k in states if k[0]==5 and k not in ends],
          'original_amplitude_replay_max':old_clock,'original_readout_replay_max':old_delta,
          'max_readout_grid_difference_all_modes':max_difference,'independent_abel':abel,
          'max_cartesian_point_error':max(v['direct_point_error'] for v in grids.values()),
          'max_independent_low_grid_packet_error':max(v['independent_packet_error'] for v in grids.values())}
    return parents,mids,ends,names,stored,path_rows,info


def allocations(parents,mids,ends,path_rows):
    base={k:Q(1,2) for k in parents}
    laws={}
    for name in ('marked','shapes'):
        middle=transfer(base,3,Q(1),set(mids),name)
        end=transfer(middle,4,Q(1),set(ends),name)
        laws[name]=(middle,end)
    for name in ('sequential','uniform_complete_paths','symmetric_completion'):
        middle,end=Counter(),Counter()
        for row in path_rows.values():
            for path in row['marked_ledger']:
                a,_,g=path['middle_reverse_end_masks']
                weight=Q(path['conditional_weights'][name])/2
                if weight:
                    middle[4,a]+=weight
                    end[5,g]+=weight
        assert sum(middle.values())==sum(end.values())==1
        if name=='sequential':
            assert middle==Counter(laws['marked'][0]) and end==Counter(laws['marked'][1])
        else:
            laws[name]=(middle,end)
    assert Counter(laws['marked'][0])==Counter(laws['symmetric_completion'][0])
    return laws


def campaigns(names,mats,parents,laws):
    root={k:Q(1,2) for k in parents};b=weights_array(root,names)
    p0=probabilities(mats,b)
    runs={}
    for name,(mid,end) in laws.items():
        x,y=weights_array(mid,names),weights_array(end,names)
        rows=[]
        for lam in (0.,.05,1.):
            before=probabilities(mats,(1-lam)*b+lam*x)
            for mu in (0.,.05,.5,1.):
                w=(1-lam)*b+lam*((1-mu)*x+mu*y)
                response=probabilities(mats,w)
                rows.append({'lambda':lam,'mu':mu,'mass_N13':lam*mu,
                             'outcomes':{k:v.tolist() for k,v in response.items()},
                             'vs_N11':assess(response,p0),'vs_intermediate':assess(response,before)})
        runs[name]={'N12_weights':{label(k):str(v) for k,v in mid.items() if v},
                    'N13_weights':{label(k):str(v) for k,v in end.items() if v},'samples':rows}
    return runs


def corner_data(names,parents,mids,ends):
    reach=[]
    for p in parents:
        middle=set(branch_splits(p,set(mids),'marked'))
        reach.append(sorted(middle | {k for h in middle for k in branch_splits(h,set(ends),'marked')}))
    pairs=list(product(*reach))
    eye=np.eye(len(names))
    return pairs,np.array([(eye[names.index(a)]+eye[names.index(b)])/2 for a,b in pairs])


def radius(m,names,parents,mids,ends):
    pairs,corners=corner_data(names,parents,mids,ends)
    b=weights_array({p:.5 for p in parents},names)
    base=b@m@b
    def norms(d):
        lev=np.abs(d).sum(axis=1)/(.2*base[:,:3].sum(axis=1))[:,None]
        c=d[1]-d[0]; old=base[1]-base[0]
        return np.vstack([lev,abs(c).sum(axis=0)/(.25*abs(old).sum()),abs(c[:3].sum(axis=0)/old[:3].sum())])
    cross=(b@m)@corners.T
    a=norms(cross-base[:,:,None]).max(axis=1)
    d=(corners@m@corners.T).reshape(2,4,-1)
    bb=norms(d-base[:,:,None]).max(axis=1)
    cap=lambda x: 2*x*(1-x)*a+x*x*bb
    sufficient=max(i/1000 for i in range(501) if cap(i/1000).max()<1)
    # Find a real counterexample above the sufficient ball. A failing corner
    # is feasible by sending each root's entire transferred portion along its named path.
    endvals=np.einsum('vc,dkce,ve->dkv',corners,m,corners,optimize=True)
    for i in range(int(sufficient*1000)+1,1001):
        z=i/1000
        candidate=(1-z)**2*base[:,:,None]+2*z*(1-z)*cross+z*z*endvals
        gates=norms(candidate-base[:,:,None])[:3]
        if gates.max()>1+1e-8:
            which=np.unravel_index(gates.argmax(),gates.shape)[1]
            selected=pairs[which]
            break
    else:
        raise AssertionError('No observed failing corner')
    return {'pair_count':len(pairs),'sufficient_fraction':sufficient,'bound_at_five_percent':cap(.05).tolist(),
            'bound_at_sufficient_fraction':cap(sufficient).tolist(),'triangle_coefficients':[a.tolist(),bb.tolist()],
            'upper_counterexample':{'fraction':z,'root_to':[label(k) for k in selected],
                                    'metrics':assess({'coherent':candidate[:,:,which]},{'coherent':base})}}
