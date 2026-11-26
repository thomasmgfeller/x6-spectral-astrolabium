"""Prefix-supported identification and same-source stationary witnesses."""
from fractions import Fraction as F
from zipfile import ZipFile
import json
from quelle import DATA,box,ROOT,ARCHIVE,SCALE
from algebra import prod,solve_box

PAST=[0,1,2,3]
FUT=[7,8,9,10]
CLOCK=[4,5,6,11,12,13,14,15,16,17,18]
WEIGHT=[4,5,6,11,12,13,14,16,18]
LIVE=WEIGHT+FUT
Z,R=16,18


def currents(y,b):
    matrix=[[box(0) for _ in y] for _ in y]
    for (i,j),c in b.items():
        v=c*(y[j]-y[i])
        matrix[i][j]+=v;matrix[j][j]-=v
    return matrix


def witness(y,w,b):
    M=currents(y,b)
    rows=[[M[i][j] for j in LIVE] for i in CLOCK]
    total=[sum((M[i][j] for i in PAST),box(0)) for j in LIVE]
    normal=[box(j==7) for j in LIVE]
    T=rows+[total,normal]
    direction=solve_box(T,[box(0)]*(len(T)-1)+[box(1)])
    drift=prod([M[0][j] for j in LIVE],direction)
    assert drift.hi<0 and all(v.lo>0 for v in direction)
    eps=F(1,10**6)
    for j,v in zip(LIVE,direction):
        for amp in (-eps,eps):
            level=w[j]+amp*v
            assert 0<level.lo<=level.hi<SCALE
    return M,direction,drift


def run():
    y,w,rel,b,e,windows=DATA
    M,v,dG=witness(y,w,b)
    baseline=prod(M[0],[w[j] for j in range(19)])
    support=sorted(j for (i,j),c in b.items() if i==0 and c and w[j].lo>0)
    assert support==[1,2,3,4,5,6,Z] and not any(j==0 for i,j in rel)
    needed={0,*support}
    after=[j for j in y if all(i==j or (i,j) in rel for i in needed)]
    minimal=[i for i in after if not any((p,i) in rel for p in after)]
    cp=sorted(i for i,j in rel if j==Z)
    early=sorted(j for j in y if y[j].hi<y[Z].lo)
    assert cp == [0,1,2,15]
    assert minimal==[7] and (R,7) in rel
    assert set(cp+PAST).isdisjoint(LIVE)
    eps=F(1,10**6)
    # Archived controls also match all clock-earlier fields, but use different local sources.
    with ZipFile(ARCHIVE) as z:
        inherited=json.loads(z.read('Anfangsdaten.json'))
    indirect=[]
    for c in inherited['finite']:
        if c['construction']!='matched_sum':continue
        changed=set(map(int,c['future_and_endpoints']))
        assert changed.isdisjoint(early)
        iv=c['delta_boundary_momenta'][0]
        assert not F(iv[0])<=0<=F(iv[1])
        indirect.append({'density_source':c['source_w'],'delta_G0':iv,'sum_equal_by_construction':True})
    assert len(indirect) == 2
    return {'strict_past_sender':cp,'global_clock_earlier':early,'direct_support_positive':support,
            'all_collection_sites':sorted(after),'minimal_collection_sites':minimal,
            'baseline_G0':baseline.data(),'fixed_clocks_and_sum':{'unknown_weights':len(LIVE),
            'independent_stationarity_equations':len(CLOCK),'remaining_dimension':1,
            'dw_per_dw7':{str(k):p.data() for k,p in zip(LIVE,v)},
            'clock_earlier_weight_suffices_on_this_family':[j for j,a in zip(LIVE,v) if j in early and not a.contains_zero()],
            'slope_G0':dG.data(),'amplitudes':list(map(str,(-eps,eps))),
            'G0_plus_minus_separation':(-2*eps*dG).data(),
            'minimax_absolute_error_lower_bound':str(F(-dG.hi,SCALE)*eps)},
            'archived_different_source_same_global_early_records':indirect}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
