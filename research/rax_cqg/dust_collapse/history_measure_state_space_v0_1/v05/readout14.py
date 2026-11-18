"""Reachability-constrained N11/N12/N13/N14 pilot readout and finite-grid certificate."""
import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
UP = ROOT / 'upstream'
sys.path.insert(0, str(UP))
import growth
from readout import branch_splits, matrices, decode
from certify import exact_effects
from abel_check import numerical_state

ROOT_NAMES = ('chain', 'one')
CAP = Q(6, 100)
UNIT = 10**6


def load(path):
    return json.loads(path.read_text())


def key(label):
    n, mask = label.removeprefix('N').split('_')
    return int(n)-8, int(mask)


def assemble(directory, clock):
    old = load(UP / 'results.json')
    labels = old['branch_order'] + [f'N14_{mask}' for mask in clock['selection']]
    keys = [key(k) for k in labels]
    old_grid = load(UP / 'v03/upstream/v02_grids.json')['grids']
    all_grids = {key:old_grid[source] for key,source in zip(labels[:2],ROOT_NAMES)}
    all_grids.update({label:old_grid[f'poset{key(label)[1]:02}_lift']
                      for label in labels if key(label)[0]==4})
    all_grids.update({label:row['grids'] for label,row in load(UP/'clocks_all.json').items()})
    all_grids.update({label:row['grids'] for label,row in clock['branches'].items()})
    assert set(all_grids) == set(labels)
    geometry = growth.geometry
    geometry.mp.mp.dps = 80
    states, abel_errors = {}, {}
    with growth.scalar_layouts():
        for label, node in zip(labels, keys):
            row, state = geometry.kernel(node)
            assert row['status']=='ADMISSIBLE' and state is not None, label
            states[node] = state
            if node[0]==6:
                precision,phase = numerical_state(node,geometry.mp.mpf('1e-28'))
                ref,amp = state
                errs = [float(max(abs(z) for z in precision-ref)),float(abs(phase-amp/abs(amp)))]
                assert max(errs)<1e-17, (label,errs)
                abel_errors[label] = errs
    grids, anchors = {}, {}
    old_size = len(old['branch_order'])
    for tag,i in [('coarse',-2),('fine',-1)]:
        amps = {node:decode(all_grids[label][i]['amplitudes']) for node,label in zip(keys,labels)}
        grids[tag] = matrices(keys,states,amps)
        ref = np.array(old['coherent_readout_grid_matrices'][tag])
        anchors[tag] = float(np.max(abs(grids[tag]['coherent'][:,:,:old_size,:old_size]-ref)))
        assert anchors[tag]<5e-12, (tag,anchors[tag])
    diffs = {mode:float(np.max(abs(arr-grids['coarse'][mode]))) for mode,arr in grids['fine'].items()}
    assert max(diffs.values())<5e-12, diffs
    mids = {k for k in keys if k[0]==4}
    ends = {k for k in keys if k[0]==5}
    reachable = []
    for root,root_name in zip(keys[:2],ROOT_NAMES):
        first = set(branch_splits(root,mids,'marked'))
        end = {k for p in first for k in branch_splits(p,ends,'marked')}
        nexts = {(6,int(g)) for p in end for g,count in directory['parents'][str(p[1])].items()
                 if count and (6,int(g)) in keys}
        certified = {int(g) for g in directory['by_root'][root_name]['admissible_end_marked_paths']}
        assert {k[1] for k in nexts} == set(clock['selection']) & certified
        reachable.append(sorted(keys.index(k) for k in first|end|nexts))
    assert set.union(*map(set,reachable))==set(range(2,len(keys)))
    return labels, reachable, grids, {'v04_coherent_replay_max':anchors,
            'grid_difference_by_mode':diffs,'independent_abel_epsilon_1e_minus_28':abel_errors}


def pos_lower(s):
    # Fast exact diagonal-dominance test; exact Schur pivots if correlations dominate.
    lower = min(s[i,i]-sum(abs(s[i,j]) for j in range(len(s)) if i!=j) for i in range(len(s)))
    if lower>0:
        return {'method':'strict_row_dominance','least_margin':float(lower)}
    h = s.copy()
    pivots = []
    while len(h):
        pivot = h[0,0]
        if pivot<=0:
            raise ArithmeticError('Definiteness check failed')
        pivots.append(pivot)
        h = h[1:,1:] - np.outer(h[1:,0],h[0,1:])/pivot
    return {'method':'exact_LDL','least_pivot':float(min(pivots))}


def uniform_gates(matrix, b, reach):
    base = b@matrix@b
    def corner_extreme(row, fn):
        return sum(fn(row[i] for i in idx) for idx in reach)/2
    derivatives = []
    for d in range(2):
        row = []
        for k in range(3):
            m = matrix[d,k]
            cross = b@m
            start = corner_extreme(cross,max)-base[d,k]
            stop = (1-CAP)*start+CAP*(max(m.flat)-corner_extreme(cross,min))
            row.append(2*max(start,stop))
        assert max(row)<0
        derivatives.append(list(map(float,row)))
    diff = matrix[1]-matrix[0]
    normalized = b@diff@b
    a = [max(abs(b@m-q)) for m,q in zip(diff,normalized)]
    c = [max(abs(m-q).flat) for m,q in zip(diff,normalized)]
    contrast = (2*CAP*(1-CAP)*sum(a)+CAP**2*sum(c))/(sum(abs(normalized))/4)
    assert contrast<1
    return {'strict_success_convexity':[pos_lower(s) for s in matrix[:,:3].sum(axis=1)],
            'negative_success_difference':pos_lower(-diff[:3].sum(axis=0)),
            'bin_derivative_upper_to_006':derivatives,
            'contrast_over_tolerance_upper_to_006':float(contrast)}


def point_array(point, labels, reach):
    parts = []
    for root, offsets in zip(ROOT_NAMES,reach):
        alloc = point[root]
        assert set(alloc) <= {labels[i] for i in offsets}
        assert all(type(v) is int and v>=0 for v in alloc.values()) and sum(alloc.values())==10**9
        parts.append([Q(alloc.get(k,0),10**9) for k in labels])
    return (np.array(parts[0],dtype=object)+parts[1])/2


def precision_data(s,b,v):
    # Exact quadratic coefficients about t=0, with a supporting tangent at each t.
    dv = v-b
    numer = [b@s@b,2*dv@s@b,dv@s@dv]
    h0,h1 = b@s,dv@s
    return numer,h0,h1,h0@v,h1@v


def ratios(data,t,reach):
    (s0,s1,s2),h0,h1,d0,d1 = data
    real = s0+t*s1+t*t*s2
    linear = sum(min(h0[i]+t*h1[i] for i in idx) for idx in reach)/2
    lower = real+2*t*(linear-d0-t*d1)
    return lower/s0,real/s0


def pilot_samples(mats, labels, reach):
    # Each root completing into the pilot spreads weight uniformly over its own
    # reachable pilot shapes; a root with no pilot continuation retains its mass.
    count = len(labels)
    base = np.array([Q(1,2),Q(1,2)]+[Q(0)]*(count-2))
    goal = np.array([Q(0)]*count,dtype=object)
    for i,idx in enumerate(reach):
        included = [j for j in idx if key(labels[j])[0]==6] or [i]
        for j in included:
            goal[j] += Q(1,2*len(included))
    events = []
    P = base@mats@base
    def l1(values):
        return sum(abs(x) for x in values)
    for t in [Q(0),Q(1,20),Q(1,1)]:
        w = (1-t)*base+t*goal
        q = w@mats@w
        assert all(sum(v)==1 and min(v)>=0 for v in q)
        tv = [l1(v-ref)/(2*sum(ref[:3])) for v,ref in zip(q,P)]
        c0 = P[1]-P[0]
        c = q[1]-q[0]
        rel = l1(c-c0)/l1(c0)
        delta = sum(c[:3])
        ok = [max(tv)<=Q(1,10),rel<=Q(1,4),delta*sum(c0[:3])>0]
        events.append({'transfer':str(t),'outcomes':[[float(x) for x in v] for v in q],
                       'N14_weight':str(sum(w[j] for j in range(count) if key(labels[j])[0]==6)),
                       'levels_relative':list(map(float,tv)),'contrast_change_relative':float(rel),
                       'success_delta':float(delta),'gates':ok,'pass':all(ok)})
    return {'target':{label:str(w) for label,w in zip(labels,goal) if w},'samples':events}


def make_points(success, labels, reach):
    # Propose the least successful deterministic destination at the inherited
    # 5% control. The subsequent tangent test includes all mixtures as well.
    b = np.r_[.5,.5,np.zeros(len(labels)-2)]
    t = .05
    points = []
    for s in success:
        def value(pair):
            i,j = pair
            shift = (1-t)*b
            shift[i] += t/2
            shift[j] += t/2
            return shift@s@shift
        pair = min(((i,j) for i in reach[0] for j in reach[1]),key=value)
        points.append({name:{labels[i]:10**9} for name,i in zip(ROOT_NAMES,pair)})
    return points


def crossing(data, reach, lo, hi):
    # Equality of supporting tangent and witness fixes the minimizer.
    # Each corner directional derivative is affine in t, so endpoint checks
    # cover the entire rational bracket for each density.
    for t in (Q(lo,UNIT),Q(hi,UNIT)):
        for quadratic in data:
            lower,witness = ratios(quadratic,t,reach)
            assert lower==witness
    denominator = 10**12
    left,right = lo*(denominator//UNIT),hi*(denominator//UNIT)
    def margin(d,t):
        (s0,s1,s2),*rest = d
        return s0/10+t*s1+t*t*s2
    while right-left>1:
        mid=(left+right)//2
        if min(margin(d,Q(mid,denominator)) for d in data)>0:
            left=mid
        else:
            right=mid
    assert min(margin(d,Q(left,denominator)) for d in data)>0
    failing=[j for j,d in enumerate(data) if margin(d,Q(right,denominator))<0]
    assert failing
    return {'fraction_denominator':denominator,'safe_numerator':left,'failing_numerator':right,
            'failing_density_index':failing,'tangent_attained_across_initial_bracket':True}


def run(clock_file,growth_file,points_file,extra_file=None):
    clock=load(clock_file)
    if extra_file is not None:
        extra=load(extra_file)
        assert clock['widths']==extra['widths']
        assert not (clock['branches'].keys() & extra['branches'].keys())
        clock['branches'].update(extra['branches'])
        clock['selection']=sorted(clock['selection']+extra['selection'])
    labels,reach,grids,checks=assemble(load(growth_file),clock)
    b=np.array([Q(1,2),Q(1,2)]+[Q(0)]*(len(labels)-2),dtype=object)
    effects={tag:exact_effects(modes['coherent']) for tag,modes in grids.items()}
    success={tag:matrix[:,:3].sum(axis=1) for tag,matrix in effects.items()}
    points=load(points_file)['certificate_points'] if points_file else make_points(
        np.asarray(success['fine'],dtype=float),labels,reach)
    by_grid={}
    for tag,m in effects.items():
        cert=uniform_gates(m,b,reach)
        data=[precision_data(s,b,point_array(p,labels,reach)) for s,p in zip(success[tag],points)]
        def values(k):
            return [ratios(row,Q(k,UNIT),reach) for row in data]
        low,high=0,int(CAP*UNIT)
        # Monotonicity of the actual success follows from the bin derivative test.
        # Each tested tangent lower bound and each strict upper witness is certified separately.
        while high-low>1:
            mid=(high+low)//2
            val=values(mid)
            if min(x for x,y in val)>Q(9,10):
                low=mid
            elif min(y for x,y in val)<Q(9,10):
                high=mid
            else:
                break
        lo_vals,hi_vals=values(low),values(high)
        assert min(x for x,y in lo_vals)>Q(9,10) and min(y for x,y in hi_vals)<Q(9,10)
        at_old=values(51179)
        old_result=('guaranteed' if min(x for x,y in at_old)>Q(9,10) else
                    'counterexample' if min(y for x,y in at_old)<Q(9,10) else 'unresolved')
        cert.update(sharp_finite_grid_crossing=crossing(data,reach,low,high),fraction_denominator=UNIT,safe_numerator=low,failing_numerator=high,
                tangent_ratios_lower_at_safe=[float(x) for x,y in lo_vals],
                witness_ratios_at_failure=[float(y) for x,y in hi_vals],
                v04_lower_fraction_test=old_result,
                tangent_and_witness_at_v04_lower=[[float(x),float(y)] for x,y in at_old])
        by_grid[tag]={'uniform':cert,'uniform_reachable_pilot':pilot_samples(m,labels,reach),
                'new_coherent_rows':grids[tag]['coherent'][:,:,30:,:].tolist()}
    return {'branch_order':labels,'reachable_non_root':{r:[labels[i] for i in idx] for r,idx in zip(ROOT_NAMES,reach)},
            'checks':checks,'certificate_point_denominator':10**9,'certificate_points':points,
            'grids':by_grid}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--growth',type=Path,default=ROOT/'growth.json')
    p.add_argument('--clock',type=Path,default=ROOT/'clock14.json')
    p.add_argument('--extra',type=Path,help='Include an independently documented additional clock panel.')
    p.add_argument('--points',type=Path,help='Replay stored rational witnesses from a prior readout JSON.')
    p.add_argument('-o','--output',type=Path,default=ROOT/'readout14.json')
    args=p.parse_args()
    if not __debug__:
        raise RuntimeError('Assertions must be active')
    result=run(args.clock,args.growth,args.points,args.extra)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    for tag,row in result['grids'].items():
        cert=row['uniform']
        print(tag,cert['safe_numerator'],cert['failing_numerator'],cert['v04_lower_fraction_test'])
