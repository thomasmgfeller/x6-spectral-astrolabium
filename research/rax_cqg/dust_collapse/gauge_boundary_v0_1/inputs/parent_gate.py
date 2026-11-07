#!/usr/bin/env python3
"""Audit decision completeness. This is not a mathematical proof checker."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PROOF_KINDS={'ANALYTIC_BOUND','COMPUTER_ASSISTED_BOUND'}
KINDS=PROOF_KINDS|{'DEFINITION','FINITE_VALIDATION','ANALYTIC_COUNTEREXAMPLE','REVIEWED_DERIVATION'}
OUTCOMES={'SATISFIED','VIOLATED','UNRESOLVED'}

def evaluate(record, contract_path=ROOT/'contract.json', manifest_path=ROOT/'examples/run_manifest.json'):
    raw=Path(contract_path).read_bytes()
    contract=json.loads(raw)
    expected_hash=hashlib.sha256(raw).hexdigest()
    issues=[]
    if record.get('contract_sha256')!=expected_hash:
        issues.append('contract SHA-256 mismatch')
    if record.get('contract_id')!=contract['id']:
        issues.append('contract id mismatch')
    if record.get('checkpoint_id') not in {c['id'] for c in contract['checkpoint_schedule']}:
        issues.append('unknown checkpoint')
    scope=record.get('scope',{})
    for k in ('model_id','domain','time_interval','refinement','claim_level'):
        if not isinstance(scope.get(k),str) or not scope[k].strip():
            issues.append('missing scope.'+k)
    if record.get('execution') not in contract['decision_rules']['execution_separate']:
        issues.append('invalid execution status')
    try:
        manifest_hash=hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()
    except OSError:
        manifest_hash=None
    if manifest_hash is None or record.get('run_manifest_sha256')!=manifest_hash:
        issues.append('missing or mismatched run manifest SHA-256')
    supplied=record.get('gates',{})
    if not isinstance(supplied,dict):
        supplied={};issues.append('gates must be an object')
    unknown=set(supplied)-set(contract['gates'])
    if unknown: issues.append('unknown gates: '+','.join(sorted(unknown)))
    statuses={}; reasons={}
    for name,spec in contract['gates'].items():
        section=supplied.get(name,{})
        if not isinstance(section,dict): section={}
        reasons[name]=[]
        bad=set(section)-set(spec['requirements'])
        if bad: reasons[name].append('unknown requirements: '+','.join(sorted(bad)))
        assessed=[]
        for req in spec['requirements']:
            item=section.get(req,{})
            if not isinstance(item,dict): item={}
            outcome=item.get('outcome','UNRESOLVED')
            kind=item.get('evidence_kind')
            refs=item.get('evidence_refs',[])
            accepted=(outcome in OUTCOMES and kind in KINDS and
                      isinstance(refs,list) and bool(refs) and
                      all(isinstance(r,str) and bool(r.strip()) for r in refs) and
                      item.get('scope_checked') is True and item.get('reviewed') is True)
            proof_needed=f'{name}.{req}' in contract['decision_rules']['finite_observations_not_accepted_for']
            if accepted and proof_needed:
                allowed=PROOF_KINDS if outcome=='SATISFIED' else PROOF_KINDS|{'ANALYTIC_COUNTEREXAMPLE'}
                accepted=kind in allowed
            if not accepted or outcome=='UNRESOLVED':
                assessed.append('HOLD');reasons[name].append(req+': unresolved or insufficient evidence')
            else:
                assessed.append('PASS' if outcome=='SATISFIED' else 'FAIL')
        statuses[name]='FAIL' if 'FAIL' in assessed else ('PASS' if all(v=='PASS' for v in assessed) and not bad else 'HOLD')
    if issues: statuses={name:'HOLD' for name in contract['gates']}
    return {'contract_id':contract['id'],'checkpoint_id':record.get('checkpoint_id'),
            'scope':scope,'record_valid':not issues,'record_issues':issues,
            'decisions':statuses,'reasons':reasons,
            'physical_claim_automatically_authorized':False,
            'notice':'Only audits declared, reviewed evidence and scope. Does not verify cited proofs or infer singularity resolution.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('record',type=Path)
    p.add_argument('--manifest',type=Path,help='defaults to run_manifest.json beside the record')
    args=p.parse_args()
    result=evaluate(json.loads(args.record.read_text()),manifest_path=args.manifest or args.record.parent/'run_manifest.json')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['record_valid'] else 2)

