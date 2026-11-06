#!/usr/bin/env python3
"""Deterministic reference identities and adversarial decision-record controls."""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
from gate import evaluate

ROOT=Path(__file__).resolve().parent
C=json.loads((ROOT/'contract.json').read_text())
def dump(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def reference_controls():
    p=C['reference'];G=p['G'];R0=p['R0']
    ts=lambda m:(2/3)*math.sqrt(R0**3/(2*G*m))
    end=0.5*min(ts(m) for m in p['masses'])
    rows=[];max_residual=0.
    for m in p['masses']:
        for f in p['time_fractions']:
            t=f*end;d=ts(m)-t;a=(d/ts(m))**(2/3);R=R0*a
            V=4*math.pi*R**3/3;rho=m/V;H=-2/(3*d)
            # Compare kinematic and density-based formulae, with independent algebra.
            acc=-2/(9*d*d);rdot=R*H
            Kgeom=12*(acc**2+H**4)
            Kdust=(320/3)*math.pi**2*G**2*rho*rho
            mgeom=H*H*R**3/(2*G)
            vals=[abs(H*H/(8*math.pi*G*rho/3)-1),abs(acc/(-4*math.pi*G*rho/3)-1),
                  abs(mgeom/m-1),abs(Kgeom/Kdust-1),abs(rdot*rdot/(2*G*m/R)-1)]
            max_residual=max(max_residual,*vals)
            assert max(vals)<1e-12
            rows.append(dict(M=m,T=t,Ts=ts(m),R=R,V=V,rho=rho,H=H,K=Kgeom,m_MS=mgeom))
    with (ROOT/'results/reference_values.csv').open('w',newline='') as fp:
        writer=csv.DictWriter(fp,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    # The chosen interval is shared; regularity here says nothing about the later collapse.
    assert end<min(ts(m) for m in p['masses'])
    assert math.isclose(math.sqrt(p['masses'][-1]/p['masses'][0]),4)
    return {'cases':len(rows),'identities_per_case':5,'max_relative_residual':max_residual,
            'T_end':end,'min_R':min(r['R'] for r in rows),'max_rho':max(r['rho'] for r in rows),
            'max_K':max(r['K'] for r in rows),
            'evidence':'FLOATING_POINT_ALGEBRA_CONTROLS_NOT_INTERVAL_CERTIFICATION_OR_CST_DATA'}

def records_and_controls():
    manifest={'id':'P0-CONTRACT-ONLY','execution':'NOT_RUN','new_cst_data':False,
              'scope':'CST-DUST-C1 target; protocol baseline only','open_items':[r['id'] for r in C['candidate_closure']]}
    dump(ROOT/'examples/run_manifest.json',manifest)
    record={'contract_id':C['id'],'contract_sha256':hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest(),
      'checkpoint_id':'P0','execution':'NOT_RUN','run_manifest_sha256':hashlib.sha256((ROOT/'examples/run_manifest.json').read_bytes()).hexdigest(),
      'scope':{'model_id':'CST-DUST-C1','domain':'finite dust ball plus exterior (closure pending)',
       'time_interval':'PST-FB-01 common interval; not yet dynamically generated',
       'refinement':'ratios 1,2,4,8; absolute density and physical matching pending',
       'claim_level':'PROTOCOL_ONLY_NO_PHYSICAL_PASS'},
      'gates':{g:{r:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION','evidence_refs':[],
                    'scope_checked':False,'reviewed':False} for r in spec['requirements']}
               for g,spec in C['gates'].items()}}
    dump(ROOT/'examples/checkpoint_P0.json',record)
    initial=evaluate(record);dump(ROOT/'results/checkpoint_P0_decision.json',initial)
    assert initial['record_valid'] and set(initial['decisions'].values())=={'HOLD'}
    # Synthetic control records exercise decision logic; never physical evidence.
    tests=[]
    def check(label,condition):
        assert condition,label;tests.append({'test':label,'status':'PASS_SOFTWARE_ONLY'})
    def satisfied(g,kind='REVIEWED_DERIVATION'):
        return {r:{'outcome':'SATISFIED','evidence_kind':kind,'evidence_refs':['SOFTWARE_FIXTURE_NOT_A_PROOF'],
                   'scope_checked':True,'reviewed':True} for r in C['gates'][g]['requirements']}
    check('baseline all HOLD',set(initial['decisions'].values())=={'HOLD'})
    r=copy.deepcopy(record);r['scope']['claim_level']='SOFTWARE_FIXTURE_ONLY';r['gates']['BOUNCE']=satisfied('BOUNCE')
    o=evaluate(r);check('bounce PASS never promotes regularity',o['decisions']['BOUNCE']=='PASS' and o['decisions']['REGULARITY']=='HOLD')
    r['gates']['REGULARITY']=satisfied('REGULARITY','FINITE_VALIDATION')
    check('finite samples cannot establish uniform regularity',evaluate(r)['decisions']['REGULARITY']=='HOLD')
    r['gates']['REGULARITY']=satisfied('REGULARITY','ANALYTIC_BOUND')
    o=evaluate(r);check('complete declared proof record accepted in its scope',o['decisions']['REGULARITY']=='PASS')
    check('moment PASS does not imply extension',o['decisions']['EXTENSION']=='HOLD')
    check('no automatic physical claim even with PASS',o['physical_claim_automatically_authorized'] is False)
    r['gates']['REGULARITY']['tails']['reviewed']=False
    check('unreviewed tail proof holds',evaluate(r)['decisions']['REGULARITY']=='HOLD')
    r['gates']['REGULARITY']['bounds']['outcome']='VIOLATED'
    r['gates']['REGULARITY']['bounds']['evidence_kind']='ANALYTIC_COUNTEREXAMPLE'
    o=evaluate(r);check('valid counterexample fails despite another unresolved requirement',o['decisions']['REGULARITY']=='FAIL')
    check('regularity FAIL does not alter bounce decision',o['decisions']['BOUNCE']=='PASS')
    r['gates']['REGULARITY']['bounds']['scope_checked']=False
    check('out of scope counterexample cannot refute target',evaluate(r)['decisions']['REGULARITY']=='HOLD')
    r=copy.deepcopy(record);del r['gates']['REGULARITY']
    check('omitted regularity reported as HOLD',evaluate(r)['decisions']['REGULARITY']=='HOLD')
    r=copy.deepcopy(record);r['contract_sha256']='0'*64
    check('changed contract invalidates record',evaluate(r)['record_valid'] is False)
    r=copy.deepcopy(record);r['run_manifest_sha256']='0'*64
    check('changed run manifest invalidates record',evaluate(r)['record_valid'] is False)
    r=copy.deepcopy(record);r['scope']['domain']=''
    check('missing domain invalidates record',evaluate(r)['record_valid'] is False)
    r=copy.deepcopy(record);r['gates']['BONCE']={}
    check('misspelled gate cannot silently pass',evaluate(r)['record_valid'] is False)
    r=copy.deepcopy(record);r['gates']['REGULARITY']=satisfied('REGULARITY','ANALYTIC_BOUND')
    del r['gates']['REGULARITY']['time_domain']
    check('time coverage cannot be omitted',evaluate(r)['decisions']['REGULARITY']=='HOLD')
    check('every checkpoint requires own regularity',all(c['regularity_required'] for c in C['checkpoint_schedule']))
    dump(ROOT/'results/decision_controls.json',tests)
    return len(tests)

if __name__=='__main__':
    (ROOT/'results').mkdir(exist_ok=True);(ROOT/'examples').mkdir(exist_ok=True)
    ref=reference_controls();n=records_and_controls()
    summary={'contract_id':C['id'],'reference_controls':ref,'decision_control_cases':n,
      'new_cst_ensembles':0,'physical_cst_gates':C['current_cst_status'],
      'singularity_resolution':'HOLD','test_status':'PASS_PROTOCOL_AND_REFERENCE_CONTROLS_ONLY'}
    dump(ROOT/'results/verification.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
