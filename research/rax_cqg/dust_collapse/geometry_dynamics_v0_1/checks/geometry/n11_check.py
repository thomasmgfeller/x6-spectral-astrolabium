#!/usr/bin/env python3
"""Independent static geometry audit of the common-boundary eleven-node pair."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json
import math

ROOT=Path(__file__).resolve().parent
N=tuple(range(11));I=frozenset((4,5,6));B=frozenset((0,1,2,3,7,8,9,10))
chain=frozenset(combinations(N,2))
fork=chain-{(4,5),(5,6)}

def invariant_profile(e):
    assert not any((x,x) in e for x in N)
    assert all((x,z) in e for x,y in e for yy,z in e if y==yy)
    past={x:{y for y in N if (y,x) in e} for x in N}
    future={x:{y for y in N if (x,y) in e} for x in N}
    height={};interior_height={}
    for x in N:
        height[x]=max([height[y]+1 for y in past[x]] or [0])
        if x in I:interior_height[x]=max([interior_height[y]+1 for y in past[x]&I] or [0])
    interval=Counter(len(future[x]&past[y]) for x,y in e)
    layers=[sum(len(past[x])==k for x in N) for k in range(11)]
    filtration=[]
    for k in range(11):
        d={x for x in N if len(past[x])<=k}
        assert all(past[x]<=d for x in d)
        layer={x for x in N if len(past[x])==k}
        assert not any((x,y) in e for x in layer for y in layer)
        filtration.append(len(d))
    return {
      'relation_count':len(e),
      'internal_relation_count':sum(x in I and y in I for x,y in e),
      'internal_height_elements':1+max(interior_height.values()),
      'global_height_elements':1+max(height.values()),
      'interval_histogram_n0_to_n3':[interval[k] for k in range(4)],
      'F4':11-sum(b*interval[k] for k,b in enumerate((1,-9,16,-8))),
      'past_cardinality_layers':layers,
      'past_cardinality_filtration_sizes':filtration,
      'boundary_node_past_cardinalities':{str(x):len(past[x]) for x in sorted(B)},
      'internal_relations':sorted((x,y) for x,y in e if x in I and y in I),
    }

def restrictions(e):
    return {
      'boundary':sorted((x,y) for x,y in e if x in B and y in B),
      'cross_boundary_interior':sorted((x,y) for x,y in e if (x in B)!=(y in B)),
    }

p=invariant_profile(chain);q=invariant_profile(fork)
assert restrictions(chain)==restrictions(fork)
assert p['internal_relation_count']==3 and q['internal_relation_count']==1
assert p['internal_height_elements']==3 and q['internal_height_elements']==2
assert p['past_cardinality_filtration_sizes']==list(range(1,12))
assert q['past_cardinality_filtration_sizes']==[1,2,3,4,6,7,7,8,9,10,11]
assert p['boundary_node_past_cardinalities']==q['boundary_node_past_cardinalities']
# The original pilot clock support [-1,1] cannot contain this affine chain,
# even after a global shift: (10*Delta)^2=50*sqrt(6)/19 > 4.
assert 6*25**2 > 38**2
clock_span=10*math.sqrt(math.sqrt(6)/38)
# Transport the complete marked data by every interior permutation. Geometric
# values, rather than event labels, distinguish the alternatives.
for pp in permutations(sorted(I)):
    m=dict(zip(sorted(I),pp));m.update({x:x for x in B})
    for e,source in [(chain,p),(fork,q)]:
        rel=frozenset((m[x],m[y]) for x,y in e)
        # The all-pair invariants below do not need a numerical-label topological sort.
        counts={x:sum(v==x for u,v in rel) for x in N}
        assert [sum(counts[x]<=k for x in N) for k in range(11)]==source['past_cardinality_filtration_sizes']
        assert sum(x in I and y in I for x,y in rel)==source['internal_relation_count']
        assert restrictions(rel)==restrictions(e)

out={
 'id':'CST-DUST-N11-COMMON-BOUNDARY-GEOMETRY-0.1',
 'status':'PASS_EXACT_STATIC_COMBINATORICS',
 'nodes':list(N),'boundary':sorted(B),'interior':sorted(I),
 'construction':'Full eleven-node chain, versus exactly deleting (4,5) and (5,6) while retaining (4,6). Both relation sets are already transitive.',
 'chain':p,'modified':q,
 'common_induced_boundary':True,'common_cross_boundary_interior_relations':True,
 'boundary_relations_count':len(restrictions(chain)['boundary']),
 'cross_boundary_interior_relations_count':len(restrictions(chain)['cross_boundary_interior']),
 'common_outer_Dirichlet_data':{'clock':'T_j=Delta*j for j in B','density':'r_j=rho for j in B','scalar':'Same chosen scalar boundary data, e.g. q_j=0, must be used for both histories'},
 'proposed_internal_data_for_separate_action_audit':{
   'chain':{'u':[4,5,6],'r_over_rho':[1,1,1]},
   'modified':{'u':[4,4,5],'r_over_rho':[2,1,1]},
   'Delta_squared':'2/(19*beta)','compact_positive_density_domain':'0<rho<1/2 is sufficient for every proposed density to lie strictly in (0,1)'},
 'interior_stationarity':'NOT_TESTED_BY_THIS_GEOMETRY_SCRIPT; delegated to independent action audits',
 'original_pilot_clock_box':{
   'can_fit_after_global_shift':False,
   'exact_clock_span_squared':'50*sqrt(6)/19 > 4',
   'minimum_clock_span_approximate':clock_span,
   'qualification':'Requires an explicit new clock support/contract, or interpretation only as an action-stationary witness outside the old [-1,1] pilot box. A global clock shift is insufficient.'},
 'meaning':'Two distinguishable internal causal geometries can share identical outer Dirichlet data. Geometric probabilities, physical inner product, and global sewing are not established by this combinatorics.',
 'no_new_integrations':True,
}
(ROOT/'n11_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
