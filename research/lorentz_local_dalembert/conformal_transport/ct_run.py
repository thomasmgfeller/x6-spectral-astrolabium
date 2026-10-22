"""Exact causal-diamond flow and full Poisson-law transport bound.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'shape_coupling'))
from sc_run import inputs,constant,gap
from fl_run import bounds
from pt_common import F,read,save,sqrt_bounds,outward,boosted
from st_certificate import exact_weights,intrinsic_gates,interval

def dot(a,b):return a[0]*b[0]-a[1]*b[1]-a[2]*b[2]
def determinant(a):
    return sum(a[0][j]*(a[1][(j+1)%3]*a[2][(j+2)%3]-a[1][(j+2)%3]*a[2][(j+1)%3]) for j in range(3))

def flow(z,k):
    assert abs(k)<1
    V=[b-a for a,b in zip(z[3],z[0])];center=[(a+b)/2 for a,b in zip(z[3],z[0])];R2=dot(V,V)/4
    out=[];omega=[]
    for row in z:
        X=[v-c for v,c in zip(row,center)];q=dot(X,X);v=dot(V,X)
        D=1+k*v/R2+k*k*q/R2;assert D>0
        f=(k*(R2+q)+k*k*v)/(2*R2)
        out.append([c+((1-k*k)*x+e*f)/D for c,x,e in zip(center,X,V)])
        omega.append((1-k*k)/D)
    assert out[0]==z[0] and out[3]==z[3]
    return out,omega

def order_and_conformal(z,zz,omega,R):
    minimum=None;times=[]
    for i in range(len(z)):
      for j in range(i+1,len(z)):
        q=interval(zz,i,j);dt=zz[j][0]-zz[i][0]
        assert q==omega[i]*omega[j]*interval(z,i,j)
        assert q!=0 and (q>0 and dt>0)==R[i][j] and (q>0 and dt<0)==R[j][i]
        minimum=abs(q) if minimum is None else min(minimum,abs(q))
        if q>0:times.append(abs(dt))
    # General affine frame determinant: the flow does NOT retain triangular gauge.
    A=[[v-b for v,b in zip(zz[i],zz[0])] for i in [1,2,3]];det=determinant(A);assert det!=0
    return dict(exact_order=True,conformal_interval_identities=210,
      minimum_absolute_interval=outward(minimum),actual_affine_frame_determinant=outward(det),
      margin_pass=minimum>=F(99,10**10) and min(times)>=F(99,10**10))

def atanh_bounds(k):
    x=abs(k);n=12
    lo=sum(x**(2*j+1)/F(2*j+1) for j in range(n))
    return lo,lo+x**(2*n+1)/(F(2*n+1)*(1-x*x))

def transport_bound(U,k):
    s=atanh_bounds(k)[1];J=F(9,10)*U[1]*s*s
    return min(F(1),sqrt_bounds(J)[1]),J

def slab_comparison(w,z,zz):
    a,b=boosted(z),boosted(zz);eta=F(0)
    for x,y in zip(a,b):
        d=[v-u for u,v in zip(x,y)]
        eta+=abs(d[0])+sqrt_bounds(d[1]*d[1]+d[2]*d[2])[1]
    return constant(w)*eta

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z=inputs();_,U,_=bounds(w,z);base=exact_weights(z,F(w['scale']))
    records=[];eligible=[]
    for numerator in c['k_numerators']:
        k=F(numerator,c['k_denominator']);zz,omega=flow(z,k)
        order=order_and_conformal(z,zz,omega,w['full_order']);beta,J=transport_bound(U,k)
        record=dict(k=str(k),tv_upper=outward(beta)[1],hellinger_exponent_upper=outward(J)[1],
          order=order,tv_gate=beta<=F(c['tv_upper_gate']))
        if not order['margin_pass']:
            record['status']='MARGIN_REJECTED';records.append(record);continue
        alt=exact_weights(zz,F(w['scale']))
        record.update(status='EXACT_WEIGHTS',**gap(base,alt));records.append(record)
        if record['tv_gate']:eligible.append((F(record['relative'][0]),len(records)-1,zz,alt,beta))
        print(json.dumps(dict(k=str(k),relative=record['relative'],tv_upper=record['tv_upper'])),flush=True)
    assert eligible
    _,i,zz,alt,beta=max(eligible,key=lambda row:row[0]);chosen=records[i]
    gates=[intrinsic_gates(v,wt,F(w['scale'])) for v,wt in [(z,base),(zz,alt)]]
    strong=F(chosen['relative'][0])>F(1,5)
    assert all(not(F(r['relative'][0])<=F(1,5)<=F(r['relative'][1])) for r in records if 'relative' in r)
    old=slab_comparison(w,z,zz)
    summary=dict(status='STRONG_PAIR_FOUND' if strong else 'NO_STRONG_PAIR_IN_FIXED_FAMILY',
      candidates=len(records),exact_order_passes=len(records),margin_passes=sum(r['order']['margin_pass'] for r in records),
      tv_gate_eligible=len(eligible),selected_row=i,selected=chosen,intrinsic_gates=gates,
      previous_slab_bound_raw=outward(old)[1],previous_slab_tv_upper=outward(min(F(1),old))[1],
      outer_endpoints_fixed=True,inner_landmarks_and_root_allowed_to_move=True,
      optimal_equal_prior_classification_accuracy_upper=outward((1+beta)/2)[1],
      minimax_expected_weight_error_over_base_norm_lower=outward(F(chosen['base_normalized'][0])*(1-beta)/2)[0],
      strong_gate_met=strong,
      scope='Conditional count/overlap/optional-total experiment at fixed density. Inner landmarks move; outer endpoints fixed. Exact rational shape and deterministic transport bound. Not physical validation, global stability, full B causal-matrix inference, or 10% impossibility.')
    witness=dict(selected_row=i,k=chosen['k'],coordinates=[[str(v) for v in row] for row in zz],
      weights=[[str(v) for v in row] for row in [base,alt]])
    return records,witness,summary

if __name__=='__main__':
    records,witness,summary=run()
    for name,r in [('candidates.json',records),('witness.json',witness),('summary.json',summary)]:
        if '--verify' in sys.argv:assert r==read(HERE/name)
        else:save(HERE/name,r)
    print(json.dumps(summary))
