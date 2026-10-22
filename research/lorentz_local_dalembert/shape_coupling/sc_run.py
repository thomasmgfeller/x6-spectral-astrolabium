"""Finite shape search with a deterministic full-channel Poisson coupling.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'full_law_scaling'))
from fl_run import inputs
from pt_common import F,read,save,outward,sqrt_bounds,boosted,setup,UNIT
from st_certificate import exact_weights,certify_order,intrinsic_gates,interval

def norm(v):return sqrt_bounds(sum(x*x for x in v))

def constant(w):
    box=setup(0)
    area=F((box['high'][1]-box['low'][1])*(box['high'][2]-box['low'][2]),UNIT**2)
    return 4*F(w['rho'])*F(w['scale'])**3*area

def deform(z,node,axis,sign,h):
    # Inverse of the determinant-one boost (17t+15x,15t+17x)/8.
    direction=[[F(17,8),F(-15,8),F(0)],[F(-15,8),F(17,8),F(0)],[F(0),F(0),F(1)]][axis]
    zz=[row[:] for row in z]
    zz[node]=[v+sign*h*d for v,d in zip(zz[node],direction)]
    assert zz[:5]==z[:5]
    original=boosted(z);changed=boosted(zz)
    for i in range(len(z)):
      for j in range(3):assert changed[i][j]-original[i][j]==(sign*h if i==node and j==axis else 0)
    return zz

def gap(w0,w1):
    n0,n1=norm(w0),norm(w1);delta=norm([b-a for a,b in zip(w0,w1)])
    return dict(relative=outward(2*delta[0]/(n0[1]+n1[1]),2*delta[1]/(n0[0]+n1[0])),
      base_normalized=outward(delta[0]/n0[1],delta[1]/n0[0]))

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z=inputs();C=constant(w);base=exact_weights(z,F(w['scale']))
    rows=[];candidates=[]
    for budget in map(F,c['tv_budgets']):
      h=F((budget/C*c['step_grid']).numerator//(budget/C*c['step_grid']).denominator,c['step_grid'])
      assert h>0 and C*h<=budget
      for node in c['moved_nodes']:
       for axis in c['axes_in_rational_boost_frame']:
        for sign in c['signs']:
          zz=deform(z,node,axis,sign,h)
          row=dict(node=node,axis=axis,sign=sign,budget=str(budget),step=str(h),tv_upper=outward(C*h)[1])
          try:
            certify_order(zz,w['full_order'])
            alt=exact_weights(zz,F(w['scale']))
          except (AssertionError,StopIteration,ZeroDivisionError):
            row['status']='GEOMETRY_OR_RANK_REJECTED';rows.append(row);continue
          assert interval(zz,3,0)==interval(z,3,0)
          row.update(status='ORDER_AND_RANK_CERTIFIED',**gap(base,alt));rows.append(row)
          candidates.append((F(row['relative'][0]),len(rows)-1,zz,alt,C*h))
      print(json.dumps(dict(budget=str(budget),completed=len(rows))),flush=True)
    assert len(rows)==c['candidate_count'] and candidates
    selected=max(candidates,key=lambda r:r[0]);_,index,zz,alt,tv=selected
    gates=[intrinsic_gates(v,wt,F(w['scale'])) for v,wt in [(z,base),(zz,alt)]]
    selected_gap=gap(base,alt)
    witness=dict(source_geometry=0,selected_row=index,coordinates=[[str(v) for v in row] for row in zz],
                 exact_weight_vectors=[[str(v) for v in row] for row in [base,alt]])
    strong=F(selected_gap['relative'][0])>F(1,5)
    unresolved=any(F(r['relative'][0])<=F(1,5)<=F(r['relative'][1]) for r in rows if 'relative' in r)
    assert not unresolved
    summary=dict(status='STRONG_PAIR_FOUND' if strong else 'NO_STRONG_PAIR_IN_FIXED_SEARCH',
      candidates=len(rows),certified_geometry_candidates=len(candidates),selected_row=index,
      selected=rows[index],exact_intrinsic_gates=gates,outer_interval_and_landmarks_fixed=True,
      optimal_equal_prior_accuracy_upper=outward((1+tv)/2)[1],
      probability_error_at_least_half_gap_lower=outward((1-tv)/2)[0],
      minimax_expected_norm_error_over_base_norm_lower=outward(F(selected_gap['base_normalized'][0])*(1-tv)/2)[0],
      strong_gate_met=strong,
      scope='Conditional finite count/overlap channel at known density, fixed selected-node order and fixed landmarks/root. Deterministic coupling bound; no full-data or global stability claim. Failure of this sufficient bound/search does not exclude other close-law shape pairs.')
    return rows,witness,summary

if __name__=='__main__':
    rows,witness,summary=run()
    for name,data in [('candidates.json',rows),('witness.json',witness),('summary.json',summary)]:
        if '--verify' in sys.argv:assert data==read(HERE/name)
        else:save(HERE/name,data)
    print(json.dumps(summary))
