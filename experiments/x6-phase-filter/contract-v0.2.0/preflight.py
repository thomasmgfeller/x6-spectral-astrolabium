#!/usr/bin/env python3
"""Offline preflight only. Never executes an algorithm or awards scientific PASS."""
import argparse
import hashlib
import json
import math
import re
import struct
import sys
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
SCHEMA_NAMES = {
    'contract':'X6_PF_Experiment_Contract_v0_2.schema.json',
    'manifest':'X6_PF_Input_Manifest_v0_2.schema.json',
    'request':'X6_PF_Execution_Request_v0_2.schema.json',
}
MAX_SAFE_INTEGER = 2**53-1
MAX_JSON_BYTES = 64*1024*1024
MAX_MANIFEST_CASES = 100000
MAX_ARRAY_BYTES = 64*1024*1024

class ContractError(ValueError): pass

def sha256(data): return hashlib.sha256(data).hexdigest()

def strict_json(raw):
    if len(raw) > MAX_JSON_BYTES: raise ContractError('JSON_SIZE_LIMIT')
    if raw.startswith(b'\xef\xbb\xbf'): raise ContractError('UTF8_BOM_NOT_ALLOWED')
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise ContractError('DUPLICATE_JSON_KEY: '+k)
            out[k]=v
        return out
    def bad_constant(s): raise ContractError('NON_FINITE_JSON: '+s)
    try: value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad_constant)
    except (UnicodeError,json.JSONDecodeError) as e: raise ContractError('INVALID_JSON: '+str(e)) from e
    def walk(x):
        if isinstance(x,float) and not math.isfinite(x): raise ContractError('NON_FINITE_JSON_NUMBER')
        if type(x) is int and abs(x)>MAX_SAFE_INTEGER: raise ContractError('NON_INTEROPERABLE_INTEGER')
        if isinstance(x,str):
            try:x.encode('utf-8')
            except UnicodeError as e:raise ContractError('INVALID_UNICODE') from e
        if isinstance(x,dict):
            for k,v in x.items():walk(k);walk(v)
        if isinstance(x,list):
            for v in x:walk(v)
    walk(value)
    return value

def load_json(path):
    path=Path(path)
    if path.stat().st_size>MAX_JSON_BYTES:raise ContractError('JSON_SIZE_LIMIT')
    return strict_json(path.read_bytes())

def only_local_schema_refs(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in ('$ref','$dynamicRef') and (not isinstance(v,str) or not v.startswith('#')):
                raise ContractError('REMOTE_OR_EXTERNAL_SCHEMA_REFERENCE_NOT_ALLOWED')
            only_local_schema_refs(v)
    elif isinstance(value,list):
        for v in value:only_local_schema_refs(v)

def schema_errors(value, name=None, schema=None):
    if schema is None:schema=load_json(ROOT/'schema'/SCHEMA_NAMES[name])
    only_local_schema_refs(schema)
    Draft202012Validator.check_schema(schema)
    errors=Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(value)
    return [('/'+'/'.join(map(str,e.absolute_path))+': '+e.message) for e in errors]

def get(d,path):
    for part in path.split('.'):
        d=d[part]
    return d

def design_counts(c):
    d=c['design']
    base=math.prod(len(d[k]) for k in ('noise_models','snr_db','signal_phase_rad','circular_time_shifts_samples'))*d['runs_per_input_cell']
    variants=len(d['filter_center_angle_deg'])*len(d['filter_width_deg'])
    baseline_count=sum(b['enabled'] for b in c['baselines'])
    return {'input_cases':base,'candidate_settings':variants,'candidate_evaluations':base*variants,
            'baseline_evaluations_with_reuse':base*baseline_count,
            'total_evaluations_with_reuse':base*(variants+baseline_count),
            'note':'Logical evaluations; does not include generator, tuning, or reference-solver costs.'}

def semantic_issues(c):
    errors=[];warnings=[]
    s=c['sampling'];d=c['design'];m=c['metrics']
    stamp=c['experiment']['created_utc']
    if stamp is not None:
        try:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z',stamp):
                raise ValueError('UTC timestamp syntax')
            datetime.fromisoformat(stamp)
        except ValueError:errors.append('INVALID_UTC_TIMESTAMP')
    if not math.isclose(s['duration_s'],s['sample_count']/s['sample_rate_hz'],rel_tol=1e-12,abs_tol=1e-12):
        errors.append('DURATION_MISMATCH: duration_s must be N/fs, not last sample time.')
    if max(c['input']['frequency_start_hz'],c['input']['frequency_end_hz'])>=s['sample_rate_hz']/2:
        errors.append('CHIRP_AT_OR_ABOVE_NYQUIST')
    if any(x>=s['sample_count'] for x in d['circular_time_shifts_samples']):errors.append('SHIFT_OUT_OF_RANGE')
    phases=d['signal_phase_rad']
    for i,p in enumerate(phases):
        if any(abs(math.remainder(p-q,2*math.pi))<1e-12 for q in phases[:i]):
            errors.append('DUPLICATE_SIGNAL_PHASE_MODULO_2PI');break
    for key,items in [('BASELINE',c['baselines']),('NOISE_MODEL',d['noise_models']),('PROFILE',c['portability']['profiles'])]:
        ids=[x['id'] for x in items]
        if len(ids)!=len(set(ids)):errors.append('DUPLICATE_'+key+'_ID')
    enabled={b['id'] for b in c['baselines'] if b['enabled']}
    if 'RAW' not in enabled:errors.append('RAW_CONTROL_REQUIRED')
    if m['primary_selected'] is not None and m['primary_selected'] not in m['primary_candidates']:
        errors.append('PRIMARY_METRIC_NOT_DECLARED')
    if m['primary_baseline_id'] is not None and m['primary_baseline_id'] not in enabled:
        errors.append('PRIMARY_BASELINE_NOT_ENABLED')
    if m['preservation_limits'] is not None:
        ids=[x['metric_id'] for x in m['preservation_limits']]
        if len(ids)!=len(set(ids)) or set(ids)!=set(m['preservation']):
            errors.append('PRESERVATION_LIMITS_MUST_COVER_EACH_METRIC_ONCE')
    required=set(c['gates']['required_for_scoped_claim'])
    if not {'PF_G0','PF_G1','PF_G2','PF_G3','PF_G5'}<=required:errors.append('REQUIRED_CLAIM_GATE_MISSING')
    if c['experiment']['evidence_class']=='CONFIRMATORY' and d['split']!='HOLDOUT':errors.append('CONFIRMATORY_REQUIRES_HOLDOUT')
    if c['experiment']['evidence_class']=='EXPLORATORY' and d['split']=='HOLDOUT':errors.append('EXPLORATION_MUST_NOT_CONSUME_HOLDOUT')
    counts=design_counts(c)
    b=c['budget']['max_evaluations']
    if b is not None and counts['total_evaluations_with_reuse']>b:errors.append('EVALUATION_BUDGET_EXCEEDED')
    if len(phases)==1 or len(d['circular_time_shifts_samples'])==1:
        warnings.append('Single phase or shift: cannot establish robustness to arbitrary window origins.')
    if counts['input_cases']>MAX_MANIFEST_CASES:errors.append('PREFLIGHT_MANIFEST_CASE_LIMIT_EXCEEDED')
    warnings.append('Correct hashes establish byte integrity against a trusted anchor, not authorship or scientific validity.')
    return errors,warnings

REQUIRED_PATHS=[
 'experiment.created_utc','input.chirp_law','input.chirp_end_time_convention',
 'input.generator_specification','input.dataset_manifest','input.rng_specification',
 'algorithm.algorithm_version','algorithm.source','algorithm.mathematical_specification',
 'algorithm.conjugate_pair_rule','algorithm.dc_policy','algorithm.nyquist_policy',
 'algorithm.zero_magnitude_phase_policy','algorithm.boundary_comparison',
 'design.split_policy','design.independence_unit','metrics.definition_file','metrics.primary_selected',
 'metrics.primary_baseline_id','metrics.minimum_relevant_benefit','metrics.preservation_limits',
 'statistics.analysis_plan','statistics.alpha','statistics.multiplicity_policy',
 'statistics.sample_size_justification','statistics.stopping_rule','statistics.maximum_failure_rate',
 'statistics.interval_method','gates.definitions','portability.reference_solver',
 'budget.max_evaluations','budget.max_wall_seconds','budget.max_memory_mib'
]

def readiness_blockers(c):
    out=[]
    if c['experiment']['state']!='LOCKED':out.append('CONTRACT_NOT_LOCKED')
    for p in REQUIRED_PATHS:
        if get(c,p) is None:out.append('UNRESOLVED: '+p)
    for b in c['baselines']:
        if b['enabled']:
            for k in ('version','source','parameter_schema','parameters'):
                if b[k] is None:out.append('UNRESOLVED: baseline.'+b['id']+'.'+k)
    for n in c['design']['noise_models']:
        if n['specification'] is None:out.append('UNRESOLVED: noise.'+n['id']+'.specification')
    for p in c['portability']['profiles']:
        for k in ('relative_tolerance','absolute_tolerance','mask_boundary_policy','phase_boundary_margin_rad'):
            if p[k] is None:out.append('UNRESOLVED: profile.'+p['id']+'.'+k)
    if c['design']['split']=='HOLDOUT':
        for k in ('registry_record','independence_evidence'):
            if c['holdout'][k] is None:out.append('UNRESOLVED: holdout.'+k)
    return out

def checked_asset(root, ref, limit=MAX_JSON_BYTES):
    if not isinstance(ref,dict):raise ContractError('MISSING_ASSET_REFERENCE')
    relative=Path(ref['path'])
    if relative.is_absolute() or '..' in relative.parts or '\\' in ref['path'] or ':' in ref['path']:
        raise ContractError('UNSAFE_ASSET_PATH: '+ref['path'])
    root=root.resolve();p=(root/relative).resolve()
    if not p.is_relative_to(root):raise ContractError('ASSET_OUTSIDE_BUNDLE')
    if p.stat().st_size>limit:raise ContractError('ASSET_SIZE_LIMIT: '+ref['path'])
    data=p.read_bytes()
    if sha256(data)!=ref['sha256']:raise ContractError('ASSET_HASH_MISMATCH: '+ref['path'])
    return data

def iter_refs(value):
    if isinstance(value,dict):
        if set(value)=={'path','sha256'}:yield value
        else:
            for v in value.values():yield from iter_refs(v)
    elif isinstance(value,list):
        for v in value:yield from iter_refs(v)

def verify_manifest(c,root):
    manifest=strict_json(checked_asset(root,c['input']['dataset_manifest']))
    errors=schema_errors(manifest,'manifest')
    if errors:raise ContractError('MANIFEST_SCHEMA: '+'; '.join(errors[:5]))
    s=c['sampling'];d=c['design']
    for key in ('sample_rate_hz','sample_count'):
        if manifest[key]!=s[key]:raise ContractError('MANIFEST_'+key.upper()+'_MISMATCH')
    if manifest['split']!=d['split']:raise ContractError('MANIFEST_SPLIT_MISMATCH')
    cases=manifest['cases']
    if len(cases)!=design_counts(c)['input_cases']:raise ContractError('MANIFEST_CASE_COUNT_MISMATCH')
    if len(cases)>MAX_MANIFEST_CASES:raise ContractError('PREFLIGHT_MANIFEST_CASE_LIMIT_EXCEEDED')
    noise_ids={x['id'] for x in d['noise_models']};seen=set();ids=set();byte_count=8*s['sample_count']
    if byte_count>MAX_ARRAY_BYTES:raise ContractError('INPUT_ARRAY_SIZE_LIMIT')
    for case in cases:
        if case['case_id'] in ids:raise ContractError('DUPLICATE_CASE_ID')
        ids.add(case['case_id'])
        key=(case['noise_id'],case['snr_db'],case['signal_phase_rad'],case['circular_time_shift_samples'],case['trial_index'])
        if key in seen:raise ContractError('DUPLICATE_CASE_COORDINATE')
        seen.add(key)
        if (case['noise_id'] not in noise_ids or case['snr_db'] not in d['snr_db'] or
            case['signal_phase_rad'] not in d['signal_phase_rad'] or case['circular_time_shift_samples'] not in d['circular_time_shifts_samples'] or
            case['trial_index']>=d['runs_per_input_cell']):raise ContractError('CASE_OUTSIDE_DESIGN')
        for field in ('clean','observed'):
            data=checked_asset(root,case[field],MAX_ARRAY_BYTES)
            if len(data)!=byte_count:raise ContractError('INPUT_BYTE_COUNT_MISMATCH')
            if any(not math.isfinite(x[0]) for x in struct.iter_unpack('<d',data)):
                raise ContractError('NON_FINITE_INPUT_ARRAY')
    return {'verified_cases':len(cases),'verified_arrays':2*len(cases)}

def verify_request(c,root,path,contract_hash):
    raw=Path(path).read_bytes();r=strict_json(raw);errs=schema_errors(r,'request')
    if errs:raise ContractError('REQUEST_SCHEMA: '+'; '.join(errs[:5]))
    if r['contract_sha256']!=contract_hash:raise ContractError('REQUEST_CONTRACT_HASH_MISMATCH')
    profiles={p['id']:p for p in c['portability']['profiles']}
    if r['profile_id'] not in profiles:raise ContractError('UNKNOWN_NUMERICAL_PROFILE')
    p=profiles[r['profile_id']]
    if p['precision']!=r['precision']:raise ContractError('REQUEST_PRECISION_MISMATCH')
    if r['target']=='WEBGPU' and r['precision']=='float64':raise ContractError('NATIVE_WEBGPU_FLOAT64_UNSUPPORTED_IN_THIS_PROFILE')
    for rk,ck in [('wall_timeout_seconds','max_wall_seconds'),('memory_limit_mib','max_memory_mib'),('evaluation_limit','max_evaluations')]:
        if r['resource_enforcement'][rk]>c['budget'][ck]:raise ContractError('REQUEST_RESOURCE_LIMIT_EXCEEDS_CONTRACT')
    if r['resource_enforcement']['evaluation_limit']<design_counts(c)['total_evaluations_with_reuse']:
        raise ContractError('REQUEST_EVALUATION_LIMIT_TOO_SMALL')
    for ref in iter_refs(r):checked_asset(root,ref)
    return {'request_sha256':sha256(raw),'target':r['target'],'profile_id':r['profile_id']}

def check(path,mode='draft',expected_sha256=None,request_path=None):
    out={'validator_version':'0.2.0','mode':mode,'status':'INVALID','scientific_claim_status':'UNVALIDATED',
         'errors':[],'blockers':[],'warnings':[],'experiments_executed':0}
    try:
        path=Path(path);root=path.parent
        if path.stat().st_size>MAX_JSON_BYTES:raise ContractError('JSON_SIZE_LIMIT')
        raw=path.read_bytes();c=strict_json(raw);digest=sha256(raw);out['contract_sha256']=digest
        out['errors']=schema_errors(c,'contract')
        if out['errors']:return out
        errs,warnings=semantic_issues(c);out['errors'].extend(errs);out['warnings'].extend(warnings)
        out['design_counts']=design_counts(c)
        out['blockers']=readiness_blockers(c)
        if out['errors']:return out
        if mode=='draft':out['status']='DRAFT_STRUCTURE_VALID';return out
        if mode!='preflight':raise ContractError('UNKNOWN_MODE')
        if expected_sha256 is None:out['blockers'].append('TRUSTED_EXTERNAL_CONTRACT_HASH_REQUIRED')
        elif not re.fullmatch('[0-9a-f]{64}',expected_sha256) or expected_sha256!=digest:
            out['errors'].append('CONTRACT_HASH_MISMATCH');return out
        if request_path is None:out['blockers'].append('EXECUTION_REQUEST_REQUIRED')
        if out['blockers']:out['status']='BLOCKED';return out
        for ref in iter_refs(c):checked_asset(root,ref)
        for b in c['baselines']:
            if not b['enabled']:continue
            ps=strict_json(checked_asset(root,b['parameter_schema']))
            errors=schema_errors(b['parameters'],schema=ps)
            if errors:raise ContractError('BASELINE_PARAMETERS: '+b['id']+': '+'; '.join(errors[:5]))
        out['input_verification']=verify_manifest(c,root)
        out['execution_request']=verify_request(c,root,request_path,digest)
        out['status']='READY_FOR_RUNNER_REVIEW'
        out['warnings'].append('No mathematical-specification audit, independence proof, runtime sandbox enforcement, or algorithm qualification is performed by this preflight.')
        return out
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as e:
        out['errors'].append(str(e));out['status']='INVALID';return out
    except Exception as e:
        out['errors'].append('VALIDATOR_ERROR: '+type(e).__name__+': '+str(e))
        out['status']='INVALID';return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract',type=Path)
    parser.add_argument('--mode',choices=['draft','preflight'],default='draft')
    parser.add_argument('--expected-sha256',help='Trusted previously registered digest, not recomputed from an untrusted bundle.')
    parser.add_argument('--request',type=Path)
    args=parser.parse_args()
    result=check(args.contract,args.mode,args.expected_sha256,args.request)
    print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    return 0 if result['status'] in ('DRAFT_STRUCTURE_VALID','READY_FOR_RUNNER_REVIEW') else 2

if __name__=='__main__':sys.exit(main())
