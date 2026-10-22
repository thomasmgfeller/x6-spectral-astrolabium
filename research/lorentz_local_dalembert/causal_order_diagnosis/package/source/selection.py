"""Fourth-landmark selection uses only A order, counts, marks and declared rho."""
import itertools
import numpy as np
from inference import four_geometry,normalize,design

def pairs_for(landmarks,root,support):
    pairs={tuple(sorted(p)) for p in itertools.combinations(landmarks,2)}
    pairs.update(tuple(sorted((a,b))) for a in landmarks for b in [root]+support)
    pairs.update(tuple(sorted((root,b))) for b in support)
    return sorted(pairs)

def select_four(g,counts,selected,cfg):
    if selected is None:return dict(status='NO_BASE_SUPPORT')
    root=selected['root'];support=selected['support'];first=selected['landmarks']
    fixed=[root]+support+first;excluded=set(fixed)|set(getattr(g,'probes_for_check',[]))
    candidates=[]
    for cones in [g.pred,g.succ]:
        common=(1<<g.size)-1
        for b in [root]+support:common&=cones[b]
        pool=[]
        while common:
            low=common&-common;a=low.bit_length()-1;common^=low
            if a not in excluded:pool.append(a)
        pool.sort(key=lambda a:g.marks[a]);candidates.extend(pool[:cfg['candidate_cap_per_side']])
    accepted=[];funnel=dict(candidates=len(candidates),count_eligible=0,lorentz_eligible=0,moment_eligible=0)
    for a in candidates:
        if not all((g.r[a,b] or g.r[b,a]) and counts.good(a,b) for b in fixed):continue
        funnel['count_eligible']+=1
        landmarks=first+[a];pairs=pairs_for(landmarks,root,support)
        packet=dict(root=root,support=support,temporal=selected['temporal'],landmarks=landmarks,pairs=pairs,
                    scale=selected['scale'],full_order=g.r[np.ix_(landmarks+[root]+support,landmarks+[root]+support)].astype(bool))
        q=np.array([counts.q(a,b) for a,b in pairs])/selected['scale']**2
        h,z,_,_=four_geometry(q,packet)
        try:_,condition=normalize(h)
        except ValueError:continue
        if condition>cfg['maximum_landmark_condition']:continue
        funnel['lorentz_eligible']+=1
        d=design(z[5:]);dcondition=float(np.linalg.cond(d))
        if np.linalg.matrix_rank(d)!=9 or dcondition>cfg['maximum_design_condition']:continue
        funnel['moment_eligible']+=1
        accepted.append((condition,float(g.marks[a]),packet,[counts.values(u,v)[0] for u,v in pairs],dcondition))
    if not accepted:return dict(status='NO_FOUR_LANDMARK_FRAME',funnel=funnel)
    accepted.sort(key=lambda row:row[:2]);condition,mark,packet,n,dcondition=accepted[0]
    return dict(status='SELECTED',packet=packet,selection_counts=n,landmark_condition=condition,
                design_condition=dcondition,funnel=funnel)
