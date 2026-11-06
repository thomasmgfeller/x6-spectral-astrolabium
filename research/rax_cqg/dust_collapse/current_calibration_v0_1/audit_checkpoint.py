#!/usr/bin/env python3
"""Adapter robustness and a contract-format P2 record; does not promote CST gates."""
import hashlib, importlib.util, json, platform
from pathlib import Path
import numpy, scipy
import observables as o

ROOT=Path(__file__).resolve().parent
def write(path,obj):
    (ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

nominal=o.intervals(40000,2,3,(4,4.01),.05/1260)
widened=o.calibrated_intervals(40000,(1.98,2.02),(2.94,3.06),(4,4.01),.05/1260)
for key in ('volume','density'):
    assert widened[key][0] < nominal[key][0] < nominal[key][1] < widened[key][1]
write('results/calibration_systematics.json',{
    'scope':'Supplementary adapter check, not a change to the frozen reference-power plan',
    'lambda_relative_bounds':[-.01,.01],'A_relative_bounds':[-.02,.02],
    'nominal':nominal,'with_deterministic_calibration_bounds':widened,
    'qualification':'NO_NEW_5_PERCENT_QUALIFICATION_WITH_SYSTEMATICS',
    'note':'Unknown detector/mask/clock bias must be bounded before a physical PASS.'})

contract=json.loads((ROOT/'inputs/parent_contract.json').read_text())
manifest={'id':'CST-DUST-CURRENT-CAL-001-P2','scope':'Reference calibration and unresolved CST assessment',
    'parent_main_commit':'0e47038f15d93edef486fbb68da5dad6bf017221',
    'plan_sha256':sha('plan.json'),'contract_sha256':sha('inputs/parent_contract.json'),
    'executed':['graph identities','finite-ball quadrature','Poisson-law evaluation','overlap covariance'],
    'not_executed':['new stochastic sprinklings','coupled CST evolution','physical density/curvature operator construction'],
    'versions':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__}}
write('results/run_manifest.json',manifest)
record={'contract_id':contract['id'],'contract_sha256':sha('inputs/parent_contract.json'),
    'checkpoint_id':'P2','execution':'RUN','run_manifest_sha256':sha('results/run_manifest.json'),
    'scope':{'model_id':'CST-DUST-C1','domain':'Finite dust interior, material boundary and exterior',
        'time_interval':'Common pre-singularity interval [0, 0.5 min Ts] of REF-DUST-FB-01',
        'refinement':'Physical CST refinement not run; reference counting ratios 1,2,4,8 only',
        'claim_level':'No physical CST qualification; separate conditional reference calibration'},
    'gates':{g:{r:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION',
        'evidence_refs':['DERIVATION.md#geltungsgrenzen','results/reference_decisions.json'],
        'scope_checked':True,'reviewed':True} for r in spec['requirements']} for g,spec in contract['gates'].items()}}
write('results/checkpoint_P2_record.json',record)
spec=importlib.util.spec_from_file_location('parent_gate',ROOT/'inputs/parent_gate.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
decision=gate.evaluate(record,ROOT/'inputs/parent_contract.json',ROOT/'results/run_manifest.json')
assert decision['record_valid'] and set(decision['decisions'].values())=={'HOLD'}
write('results/checkpoint_P2_audit.json',decision)
print(json.dumps({'record_valid':decision['record_valid'],'decisions':decision['decisions'],
    'systematic_bounds':'propagated; widen both intervals'},indent=2))
