"""Exact conditional full-law bound for a homothety family.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'poisson_testing'))
from pt_common import F,read,save,OLD,input_record,interval,sqrt_bounds,pi_bounds,outward
from st_certificate import exact_weights,certify_order,intrinsic_gates

def inputs():
    w=read(OLD/'witness.json');z=[[F(v) for v in row] for row in w['coordinates'][0]]
    packet,_,_=input_record(w['index']);lookup={v:i for i,v in enumerate(w['nodes'])}
    pairs=[(lookup[a],lookup[b]) for a,b in packet['pairs']];R=w['full_order']
    ends=[(a,b) if R[a][b] else (b,a) for a,b in pairs]
    assert len(ends)==90 and (3,0) in ends
    assert all((a==3 or R[3][a]) and (b==0 or R[b][0]) for a,b in ends)
    return w,z

def bounds(w,z):
    scale=F(w['scale']);q=scale**2*interval(z,3,0)
    pl,pu=pi_bounds();ql,qu=sqrt_bounds(q);rho=F(w['rho'])
    U=(rho*pl*q*ql/12,rho*pu*q*qu/12)
    L=(rho*pl*F(3,2)**3/12,rho*pu*F(3,2)**3/12)
    return q,U,L

def tv_bound(s,U,L):
    a=s**3;assert L[0]>a*U[1]
    # J=sum (sqrt(lambda)-sqrt(mu))^2; TV <= sqrt(1-exp(-J)) <= sqrt(J).
    # Separate interval bounds avoid cancellation of nearby square roots.
    root_lower=sqrt_bounds(a)[0]
    j=U[1]*(a-1)**2/(root_lower+1)**2+(a-1)**2*U[1]**2/(4*(L[0]-a*U[1]))
    return min(F(1),sqrt_bounds(j)[1]),j

def main_result():
    freeze=read(HERE/'freeze.json')
    for name,h in freeze['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z=inputs();q,U,L=bounds(w,z)
    records=[];accepted=[]
    for k in range(c['scale_grid_numerators_added'][0],c['scale_grid_numerators_added'][1]+1):
        s=1+F(k,c['scale_grid_denominator']);assert s*s*q<F(9,4)
        tv,j=tv_bound(s,U,L);ok=tv<=F(c['tv_upper_gate'])
        records.append(dict(k=k,s=str(s),tv_upper=outward(tv)[1],accepted=ok))
        if ok:accepted.append((s,tv,j))
    assert accepted
    s,tv,j=accepted[-1];zz=[[s*v for v in row] for row in z]
    order=[certify_order(v,w['full_order']) for v in [z,zz]]
    weights=[exact_weights(v,F(w['scale'])) for v in [z,zz]]
    assert weights[1]==[v/s**2 for v in weights[0]]
    gates=[intrinsic_gates(v,wt,F(w['scale'])) for v,wt in zip([z,zz],weights)]
    # Relative loss uses the common fixed reference ||w0||, not random norms.
    d=1-1/s**2;relative=2*d/(1+1/s**2)
    error=(1-tv)/2
    expected_loss=d*(1-tv)/2  # coupling/triangle proof, not just nearest-point testing
    # Any disjoint 10%-relative-error balls require s²>11/9, hence s>11/10.
    a0=F(11,10)**3
    error_sum=4*(1+a0)/((a0-1)**2*U[0])
    assert error_sum<1
    large_s=F(111,100);assert large_s**2*q<F(9,4)
    assert large_s**2>F(11,9)
    large_weights=exact_weights([[large_s*v for v in row] for row in z],F(w['scale']))
    assert large_weights==[v/large_s**2 for v in weights[0]]
    return dict(status='CERTIFIED_CONDITIONAL_FULL_LAW_SMALL_PAIR',selected_scale=str(s),grid_points=len(records),accepted_points=len(accepted),
      union_mean=outward(*U),domain_mean=outward(*L),union_equals_recorded_outer_interval=True,
      full_law_tv_upper=outward(tv)[1],hellinger_exponent_upper=outward(j)[1],
      optimal_equal_prior_classification_accuracy_upper=outward((1+tv)/2)[1],
      optimal_equal_prior_testing_error_lower=outward(error)[0],
      weight_gap_over_base_norm=str(d),symmetric_relative_weight_separation=str(relative),
      probability_error_at_least_half_gap_lower=outward(error)[0],half_gap_over_base_norm=str(d/2),
      minimax_expected_norm_error_over_base_norm_lower=outward(expected_loss)[0],
      exact_order=order,exact_intrinsic_gates=gates,exact_weight_scaling=True,
      ten_percent_scaling_family=dict(disjoint_relative_balls_require='s^2>11/9',
        uniform_tv_lower=outward(1-error_sum)[0],
        uniform_achievable_equal_prior_accuracy_lower=outward(1-error_sum/2)[0],
        feasible_large_scale=str(large_s),status='STOP_HOMOTHETY_AS_CLOSE_LAW_10_PERCENT_COUNTEREXAMPLE'),
      grid=records,
      scope='Fixed selected-node causal order and count/overlap/optional-total channel; known density, free absolute landmark scale. Ideal Poisson law, exact deterministic bounds. Not full B causal matrix, observed coordinates, A selection likelihood, original-realization confidence membership, smooth-field error or global reconstruction certification.')

if __name__=='__main__':
    result=main_result()
    if '--verify' in sys.argv:assert result==read(HERE/'certificate.json')
    else:save(HERE/'certificate.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['grid','exact_order','exact_intrinsic_gates']}))
