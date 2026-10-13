"""Build the portable schemas and the deliberately non-executable draft."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def write(name, value):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')

def obj(p, required=None):
    return {'type':'object','properties':p,'required':list(p) if required is None else required,'additionalProperties':False}
def enum(*xs): return {'enum':list(xs)}
def nullable(x): return {'anyOf':[x,{'type':'null'}]}
def arr(x, minimum=1): return {'type':'array','items':x,'minItems':minimum,'uniqueItems':True}
def num(lo=None, hi=None):
    d={'type':'number'}
    if lo is not None:d['minimum']=lo
    if hi is not None:d['maximum']=hi
    return d
def integer(lo=0):return {'type':'integer','minimum':lo,'maximum':9007199254740991}
def text():return {'type':'string','minLength':1}
SHA={'type':'string','pattern':'^[0-9a-f]{64}$'}
POS={'type':'number','exclusiveMinimum':0}
REF=obj({'path':text(),'sha256':SHA})
NREF=nullable(REF)
STAMP={'type':'string','format':'date-time','pattern':'Z$'}
ANGLE={'type':'number','minimum':-180,'exclusiveMaximum':180}
WIDTH={'type':'number','exclusiveMinimum':0,'maximum':360}
BASELINE=obj({'id':text(),'version':nullable(text()),'enabled':{'type':'boolean'},'source':NREF,
              'parameter_schema':NREF,'parameters':nullable({'type':'object'})})
PROFILE=obj({'id':text(),'precision':enum('float32','float64'),
             'relative_tolerance':nullable(num(0)),'absolute_tolerance':nullable(num(0)),
             'mask_boundary_policy':nullable(enum('MARGIN_OR_INCONCLUSIVE')),
             'phase_boundary_margin_rad':nullable(POS)})
contract=obj({
 'schema':{'const':'X6-PF-EXPERIMENT-CONTRACT'},'schema_version':{'const':'0.2.0'},
 'experiment':obj({'experiment_id':text(),'title':text(),'state':enum('DRAFT','LOCKED'),
                   'evidence_class':enum('EXPLORATORY','CONFIRMATORY'),'created_utc':nullable(STAMP),
                   'parent_experiment_id':nullable(text())}),
 'claim':obj({'claim_id':text(),'statement':text(),'scope':{'const':'synthetic_signal_processing'},
             'preservation_required':{'const':True},'boundaries':arr(text())}),
 'integrity':obj({'hash_policy':{'const':'SHA256_EXACT_FILE_BYTES_V1'},
                  'anchor_policy':{'const':'EXTERNAL_TRUSTED_CONTRACT_SHA256'},
                  'results_location':{'const':'SEPARATE_EXECUTION_RECORD'}}),
 'sampling':obj({'sample_rate_hz':POS,'sample_count':integer(2),'duration_s':POS,
                 'duration_convention':{'const':'N_OVER_FS'},'sample_times':{'const':'n/fs; n=0..N-1'}}),
 'input':obj({'source_type':{'const':'synthetic'},'signal_class':{'const':'chirp'},'amplitude':POS,
              'frequency_start_hz':POS,'frequency_end_hz':POS,
              'chirp_law':nullable(enum('LINEAR_FREQUENCY')),
              'chirp_end_time_convention':nullable(enum('LAST_SAMPLE','DURATION_BOUNDARY')),
              'generator_specification':NREF,'dataset_manifest':NREF,
              'input_encoding':{'const':'IEEE754_BINARY64_LITTLE_ENDIAN_CONTIGUOUS'},
              'pairing':{'const':'SAME_MATERIALIZED_INPUT_ACROSS_METHODS_AND_FILTER_SETTINGS'},
              'master_seed':integer(),'rng_specification':NREF}),
 'algorithm':obj({'algorithm_id':{'const':'X6-PF-A'},'algorithm_version':nullable(text()),
                  'source':NREF,'mathematical_specification':NREF,
                  'filter_type':{'const':'binary_phase_gate'},'mode':enum('pass','stop'),
                  'phase_interval':{'const':'[-pi,pi)'},
                  'conjugate_pair_rule':nullable(enum('POSITIVE_FREQUENCY_DECIDES_PAIR','SYMMETRIC_ANGLE_UNION')),
                  'dc_policy':nullable(enum('PRESERVE','FILTER_REAL_BIN')),
                  'nyquist_policy':nullable(enum('PRESERVE','FILTER_REAL_BIN')),
                  'zero_magnitude_phase_policy':nullable(enum('ZERO_BIN_UNCHANGED')),
                  'boundary_comparison':nullable(enum('LESS_EQUAL','STRICT_LESS'))}),
 'baselines':arr(BASELINE),
 'design':obj({'noise_models':arr(obj({'id':text(),'specification':NREF})),
               'snr_db':arr(num()),'signal_phase_rad':arr(num()),
               'circular_time_shifts_samples':arr(integer()),
               'filter_center_angle_deg':arr(ANGLE),'filter_width_deg':arr(WIDTH),
               'runs_per_input_cell':integer(1),
               'split':enum('DEVELOPMENT','VALIDATION','HOLDOUT'),
               'split_policy':NREF,'baseline_reuse':{'const':'ONCE_PER_INPUT_CASE'},
               'independence_unit':nullable(enum('SOURCE_REALIZATION'))}),
 'metrics':obj({'definition_file':NREF,'primary_candidates':arr(text()),
                'primary_selected':nullable(text()),'preservation':arr(text()),'secondary':arr(text()),
                'comparison':{'const':'PAIRED_AGAINST_PREDECLARED_BASELINE'},
                'primary_baseline_id':nullable(text()),
                'benefit_direction':{'const':'POSITIVE_MEANS_CANDIDATE_BETTER'},
                'minimum_relevant_benefit':nullable(POS),
                'preservation_limits':nullable(arr(obj({'metric_id':text(),'unit':text(),
                    'upper_bound':num(0),'comparison_basis':enum('ABSOLUTE_ERROR','EXCESS_HARM_VS_BASELINE')})))}),
 'statistics':obj({'analysis_plan':NREF,'alpha':nullable({'type':'number','exclusiveMinimum':0,'exclusiveMaximum':1}),
                   'multiplicity_policy':nullable(enum('PREDECLARED_SINGLE_COMPARISON','HOLM','SIMULTANEOUS_INTERVALS')),
                   'sample_size_justification':NREF,'stopping_rule':nullable(enum('FIXED_SAMPLE_SIZE_NO_OPTIONAL_STOPPING')),
                   'maximum_failure_rate':nullable(num(0,1)),
                   'interval_method':nullable(text())}),
 'gates':obj({'required_for_scoped_claim':arr(enum('PF_G0','PF_G1','PF_G2','PF_G3','PF_G5')),
             'definitions':NREF,'missing_required_result':{'const':'INCONCLUSIVE'},
             'execution_failure':{'const':'ERROR_NOT_SCIENTIFIC_FAIL'},
             'real_signal':{'const':'NOT_APPLICABLE'},'cross_domain':{'const':'NOT_APPLICABLE'}}),
 'holdout':obj({'registry_record':NREF,'independence_evidence':NREF,
                'selection_uses_holdout':{'const':False},'reuse_after_inspection':{'const':'NEW_EXPLORATORY_STUDY_REQUIRED'}}),
 'portability':obj({'profiles':arr(PROFILE),'reference_solver':NREF,
                   'status':{'const':'NOT_VALIDATED'},'native_webgpu_float64':{'const':False}}),
 'budget':obj({'max_evaluations':nullable(integer(1)),'max_wall_seconds':nullable(POS),
               'max_memory_mib':nullable(integer(1)),'on_exceed':{'const':'BLOCK_OR_ABORT_WITHOUT_PASS'}})
})
contract.update({'$schema':'https://json-schema.org/draft/2020-12/schema',
 '$id':'urn:x6:pf:experiment-contract:0.2.0',
 'title':'X6 PF Experiment Contract v0.2.0',
 '$comment':'Structure is not readiness. Apply preflight.py and scientific review. No defaults modify instances.'})
contract['allOf']=[{'if':{'properties':{'experiment':{'properties':{'state':{'const':'LOCKED'}}}}},
 'then':{'properties':{
  'experiment':{'properties':{'created_utc':STAMP}},
  'metrics':{'properties':{'primary_selected':text(),'primary_baseline_id':text(),
                         'minimum_relevant_benefit':POS,'preservation_limits':{'type':'array','minItems':1}}},
  'statistics':{'properties':{'alpha':{'type':'number','exclusiveMinimum':0,'exclusiveMaximum':1},
                            'maximum_failure_rate':num(0,1)}},
  'budget':{'properties':{'max_evaluations':integer(1),'max_wall_seconds':POS,'max_memory_mib':integer(1)}}}}}]
write('schema/X6_PF_Experiment_Contract_v0_2.schema.json',contract)

manifest=obj({'schema':{'const':'X6-PF-INPUT-MANIFEST'},'schema_version':{'const':'0.2.0'},
 'encoding':{'const':'IEEE754_BINARY64_LITTLE_ENDIAN_CONTIGUOUS'},
 'sample_rate_hz':POS,'sample_count':integer(2),'split':enum('DEVELOPMENT','VALIDATION','HOLDOUT'),
 'cases':arr(obj({'case_id':text(),'source_realization_id':text(),'trial_index':integer(),
                  'noise_id':text(),'snr_db':num(),'signal_phase_rad':num(),
                  'circular_time_shift_samples':integer(),
                  'clean':REF,'observed':REF}))})
manifest.update({'$schema':contract['$schema'],'$id':'urn:x6:pf:input-manifest:0.2.0'})
write('schema/X6_PF_Input_Manifest_v0_2.schema.json',manifest)

request=obj({'schema':{'const':'X6-PF-EXECUTION-REQUEST'},'schema_version':{'const':'0.2.0'},
 'run_id':text(),'contract_sha256':SHA,'target':enum('LOCAL_JS','PYTHON','WASM','WEBGPU','EXTERNAL_SOLVER'),
 'profile_id':text(),'precision':enum('float32','float64'),'implementation':REF,
 'runtime_fingerprint':obj({'platform':text(),'architecture':text(),'runtime':text(),'runtime_version':text(),
                           'device':text(),'dependency_lock':REF}),
 'resource_enforcement':obj({'wall_timeout_seconds':POS,'memory_limit_mib':integer(1),'evaluation_limit':integer(1)})})
request.update({'$schema':contract['$schema'],'$id':'urn:x6:pf:execution-request:0.2.0'})
write('schema/X6_PF_Execution_Request_v0_2.schema.json',request)

draft={
 'schema':'X6-PF-EXPERIMENT-CONTRACT','schema_version':'0.2.0',
 'experiment':{'experiment_id':'X6-PF-EXP-000001','title':'X6 Phase Filter Validation',
               'state':'DRAFT','evidence_class':'EXPLORATORY','created_utc':None,'parent_experiment_id':None},
 'claim':{'claim_id':'X6-PF-C01','statement':'Test scoped quality benefit over a declared baseline subject to signal-preservation limits.',
          'scope':'synthetic_signal_processing','preservation_required':True,
          'boundaries':['No diagnostic claim','No universal superiority claim','No physical validation',
                        'No novelty claim','No hardware portability claim from schema validation']},
 'integrity':{'hash_policy':'SHA256_EXACT_FILE_BYTES_V1','anchor_policy':'EXTERNAL_TRUSTED_CONTRACT_SHA256',
              'results_location':'SEPARATE_EXECUTION_RECORD'},
 'sampling':{'sample_rate_hz':1000,'sample_count':4096,'duration_s':4.096,
             'duration_convention':'N_OVER_FS','sample_times':'n/fs; n=0..N-1'},
 'input':{'source_type':'synthetic','signal_class':'chirp','amplitude':1.0,'frequency_start_hz':5.0,
          'frequency_end_hz':120.0,'chirp_law':None,'chirp_end_time_convention':None,
          'generator_specification':None,'dataset_manifest':None,
          'input_encoding':'IEEE754_BINARY64_LITTLE_ENDIAN_CONTIGUOUS',
          'pairing':'SAME_MATERIALIZED_INPUT_ACROSS_METHODS_AND_FILTER_SETTINGS',
          'master_seed':104729,'rng_specification':None},
 'algorithm':{'algorithm_id':'X6-PF-A','algorithm_version':'0.1.0','source':None,
              'mathematical_specification':None,'filter_type':'binary_phase_gate','mode':'pass',
              'phase_interval':'[-pi,pi)','conjugate_pair_rule':None,'dc_policy':None,
              'nyquist_policy':None,'zero_magnitude_phase_policy':None,'boundary_comparison':None},
 'baselines':[{'id':x,'version':None,'enabled':True,'source':None,'parameter_schema':None,'parameters':None}
              for x in ['RAW','MOVING_AVERAGE','SAVITZKY_GOLAY','BUTTERWORTH','LINEAR_PHASE_FIR','WIENER','WAVELET','ADAPTIVE_LMS']],
 'design':{'noise_models':[{'id':x,'specification':None} for x in
                          ['white','pink','red','blue','narrowband','impulse','baseline_drift','mixed']],
           'snr_db':[-20,-15,-10,-5,0,5,10,20,30],'signal_phase_rad':[0.0],
           'circular_time_shifts_samples':[0],'filter_center_angle_deg':list(range(-180,180,10)),
           'filter_width_deg':[10,20,30,45,60,90],'runs_per_input_cell':1000,
           'split':'DEVELOPMENT','split_policy':None,'baseline_reuse':'ONCE_PER_INPUT_CASE',
           'independence_unit':None},
 'metrics':{'definition_file':None,'primary_candidates':['delta_snr_db','rmse','correlation'],
            'primary_selected':None,'preservation':['amplitude_error','peak_time_error','phase_error','spectral_distortion','energy_ratio'],
            'secondary':['spectral_entropy','ringing','overshoot','processing_latency'],
            'comparison':'PAIRED_AGAINST_PREDECLARED_BASELINE','primary_baseline_id':None,
            'benefit_direction':'POSITIVE_MEANS_CANDIDATE_BETTER','minimum_relevant_benefit':None,
            'preservation_limits':None},
 'statistics':{'analysis_plan':None,'alpha':None,'multiplicity_policy':None,'sample_size_justification':None,
               'stopping_rule':None,'maximum_failure_rate':None,'interval_method':None},
 'gates':{'required_for_scoped_claim':['PF_G0','PF_G1','PF_G2','PF_G3','PF_G5'],
          'definitions':None,'missing_required_result':'INCONCLUSIVE','execution_failure':'ERROR_NOT_SCIENTIFIC_FAIL',
          'real_signal':'NOT_APPLICABLE','cross_domain':'NOT_APPLICABLE'},
 'holdout':{'registry_record':None,'independence_evidence':None,'selection_uses_holdout':False,
            'reuse_after_inspection':'NEW_EXPLORATORY_STUDY_REQUIRED'},
 'portability':{'profiles':[{'id':p,'precision':p,'relative_tolerance':None,'absolute_tolerance':None,
                             'mask_boundary_policy':None,'phase_boundary_margin_rad':None}
                            for p in ['float64','float32']],
                'reference_solver':None,'status':'NOT_VALIDATED','native_webgpu_float64':False},
 'budget':{'max_evaluations':None,'max_wall_seconds':None,'max_memory_mib':None,
           'on_exceed':'BLOCK_OR_ABORT_WITHOUT_PASS'}
}
write('X6_PF_Experiment_Contract_v0_2_DRAFT.json',draft)

if __name__=='__main__':
    print('Wrote 3 schemas and the unqualified DRAFT; no experiments executed.')
