"""Fixed-budget reference-point scan with exact rational gates.
SPDX-License-Identifier: Apache-2.0
"""
import sys, json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'conformal_sensitivity'))
from cs_run import exact_local
from ct_run import inputs,bounds,flow,order_and_conformal,transport_bound,F,read,save,boosted,exact_weights,intrinsic_gates,gap

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z=inputs();scale=F(w['scale']);_,U,_=bounds(w,z)
    rows=[];bases=[];eligible=[]
    for a in map(F,c['base_parameters']):
        za,oa=flow(z,a);oaudit=order_and_conformal(z,za,oa,w['full_order'])
        wa=exact_weights(za,scale)
        try:ga=intrinsic_gates(za,wa,scale);base_ok=oaudit['margin_pass']
        except AssertionError:ga=None;base_ok=False
        local,independent,_=exact_local(boosted(za),scale,U)
        assert independent==wa
        bases.append(dict(a=str(a),order=oaudit,intrinsic=ga,admissible=base_ok,
                          local={k:v for k,v in local.items() if k!='derivative'}))
        for d in map(F,c['relative_steps']):
            b=(a+d)/(1+a*d)
            zb,ob=flow(z,b);composed,od=flow(za,d)
            assert composed==zb,'group composition failed'
            assert all(x*y==v for x,y,v in zip(oa,od,ob))
            check=order_and_conformal(za,zb,od,w['full_order'])
            beta,_=transport_bound(U,d);wb=exact_weights(zb,scale)
            try:gb=intrinsic_gates(zb,wb,scale);alt_ok=check['margin_pass']
            except AssertionError:gb=None;alt_ok=False
            r=dict(a=str(a),b=str(b),relative_step=str(d),tv_upper=str(beta),
                   order=check,intrinsic=gb,**gap(wa,wb))
            r['eligible']=base_ok and alt_ok and beta<=F(c['tv_upper_gate'])
            r['strong']=r['eligible'] and F(r['relative'][0])>F(c['strong_gap_gate'])
            assert not F(r['relative'][0])<=F(c['strong_gap_gate'])<=F(r['relative'][1])
            rows.append(r)
            if r['eligible']:eligible.append(len(rows)-1)
        print(json.dumps(dict(base=str(a),completed=len(rows),admissible=base_ok)),flush=True)
    assert len(rows)==c['candidate_count'] and eligible
    selected=max(eligible,key=lambda i:F(rows[i]['relative'][0]));r=rows[selected]
    s=dict(status='STRONG_PAIR_FOUND' if r['strong'] else 'NO_STRONG_PAIR_IN_FIXED_SCAN',
           candidates=len(rows),eligible=len(eligible),base_geometries=len(bases),
           selected_row=selected,selected=r,
           scope='Finite grid only, no continuous or global exclusion. PR97 fixed-base theorem is unchanged. No 10% estimator guarantee.')
    return bases,rows,s

if __name__=='__main__':
    for name,data in zip(['bases.json','candidates.json','summary.json'],run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
