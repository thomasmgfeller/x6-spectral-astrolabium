"""A posteriori analytic reduction: total input momentum plus the earliest component."""
from basisdaten import read,hull,box,ROOT,SCALE
from fractions import Fraction as Q
import json


def reduced_gate():
    y,w,rel,b,e,windows=read()
    z,r=16,18
    c0=min((i for i in (0,1,2,3)),key=lambda k:sum(j==k for _,j in rel))
    assert c0==0
    # Difference of D_r is exactly its derivative at the midpoint of the chord.
    envelope=[]
    for window in windows:
        ends=[(4-v)*x+v-2 for v in map(Q,e.data()) for x in window]
        envelope.append(hull(min(ends),max(ends)))
    s,t=envelope
    yr={**y,z:s,r:t}
    m=sum((v*(t-yr[i]) for (i,j),v in b.items() if j==r),box(0))
    ratio=(t-s)/m
    assert m.hi<0 and ratio.hi<0 and (s+5).lo>0 and (y[17]+2).hi<0
    # Sum outgoing weights/first moments for all four past points.
    assert [[sum(b.get((i,j),0) for i in (0,1,2,3)),
             sum(b.get((i,j),0)*Q(y[i].lo,SCALE) for i in (0,1,2,3))]
            for j in (z,r)]==[[-1,3],[8,-16]]
    assert b[c0,z]==-8 and b[c0,r]==0
    data=json.loads((ROOT/'Anfangsdaten.json').read_bytes())
    for case in data['finite']:
        if case['construction']=='matched_sum':
            assert not hull(*case['delta_boundary_momenta'][0]).contains_zero()
    return {'required_comparison':['sum of four G_i','G_0'],'passive_receiver':True,
            'derivative_m_r_on_windows':m.data(),'secant_delta_t_over_delta_s':ratio.data(),
            'h_plus_2':(y[17]+2).data(),'no_endpoint_change':True,
            'sum_only_counterexamples':2,'status':'additional_analytic_test_after_finite_controls'}


if __name__=='__main__':print(json.dumps(reduced_gate(),sort_keys=True,indent=2))
