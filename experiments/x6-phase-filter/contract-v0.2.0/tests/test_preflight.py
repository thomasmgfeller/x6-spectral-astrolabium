"""Fixtures test admission logic; their numbers are NOT scientific thresholds."""
import copy
import json
import math
import struct
import tempfile
import unittest
from pathlib import Path

import preflight as p

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.c=p.load_json(p.ROOT/'X6_PF_Experiment_Contract_v0_2_DRAFT.json')
        self.path=self.root/'contract.json';self.request=self.root/'request.json'

    def tearDown(self):self.tmp.cleanup()

    def save(self):
        self.path.write_text(json.dumps(self.c,allow_nan=False)+'\n',encoding='utf-8')
        return p.sha256(self.path.read_bytes())

    def asset(self,name,data):
        path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        return {'path':name,'sha256':p.sha256(data)}

    def fixture(self):
        # Every asset is a software test fixture, not a qualified scientific spec.
        doc=self.asset('fixture-spec.txt',b'TEST FIXTURE ONLY: no scientific validity asserted.\n')
        params=self.asset('params.schema.json',b'{"type":"object","properties":{},"additionalProperties":false}')
        c=self.c;c['experiment']['state']='LOCKED';c['experiment']['created_utc']='2026-10-13T18:00:00Z'
        c['sampling'].update(sample_count=4,duration_s=.004)
        for section,key in [('input','generator_specification'),('input','rng_specification'),
         ('algorithm','source'),('algorithm','mathematical_specification'),('design','split_policy'),
         ('metrics','definition_file'),('statistics','analysis_plan'),('statistics','sample_size_justification'),
         ('gates','definitions'),('portability','reference_solver')]:c[section][key]=doc
        c['input'].update(chirp_law='LINEAR_FREQUENCY',chirp_end_time_convention='LAST_SAMPLE')
        c['algorithm'].update(conjugate_pair_rule='POSITIVE_FREQUENCY_DECIDES_PAIR',dc_policy='PRESERVE',
         nyquist_policy='PRESERVE',zero_magnitude_phase_policy='ZERO_BIN_UNCHANGED',boundary_comparison='LESS_EQUAL')
        c['baselines']=[{'id':'RAW','enabled':True,'version':'test-fixture','source':doc,'parameter_schema':params,'parameters':{}}]
        c['design'].update(noise_models=[{'id':'white','specification':doc}],snr_db=[0],
         filter_center_angle_deg=[40],filter_width_deg=[30],runs_per_input_cell=1,independence_unit='SOURCE_REALIZATION')
        c['metrics'].update(primary_selected='rmse',primary_baseline_id='RAW',minimum_relevant_benefit=.1,
          preservation_limits=[{'metric_id':x,'unit':'TEST_UNIT','upper_bound':.1,'comparison_basis':'ABSOLUTE_ERROR'}
                               for x in c['metrics']['preservation']])
        c['statistics'].update(alpha=.05,multiplicity_policy='PREDECLARED_SINGLE_COMPARISON',
         stopping_rule='FIXED_SAMPLE_SIZE_NO_OPTIONAL_STOPPING',maximum_failure_rate=.01,interval_method='TEST_ONLY')
        for q in c['portability']['profiles']:
            q.update(relative_tolerance=1e-6,absolute_tolerance=1e-6,mask_boundary_policy='MARGIN_OR_INCONCLUSIVE',phase_boundary_margin_rad=1e-5)
        c['budget'].update(max_evaluations=2,max_wall_seconds=30,max_memory_mib=128)
        clean=self.asset('clean.f64le',struct.pack('<4d',1,2,3,4));noisy=self.asset('observed.f64le',struct.pack('<4d',2,3,4,5))
        self.manifest={'schema':'X6-PF-INPUT-MANIFEST','schema_version':'0.2.0',
         'encoding':'IEEE754_BINARY64_LITTLE_ENDIAN_CONTIGUOUS','sample_rate_hz':1000,'sample_count':4,'split':'DEVELOPMENT',
         'cases':[{'case_id':'case-0','source_realization_id':'realization-0','trial_index':0,'noise_id':'white','snr_db':0,
                   'signal_phase_rad':0,'circular_time_shift_samples':0,'clean':clean,'observed':noisy}]}
        self.save_manifest()
        digest=self.save()
        self.r={'schema':'X6-PF-EXECUTION-REQUEST','schema_version':'0.2.0','run_id':'TEST-NOT-RUN','contract_sha256':digest,
         'target':'PYTHON','profile_id':'float64','precision':'float64','implementation':doc,
         'runtime_fingerprint':{'platform':'test','architecture':'test','runtime':'test','runtime_version':'0',
                                'device':'test','dependency_lock':doc},
         'resource_enforcement':{'wall_timeout_seconds':30,'memory_limit_mib':128,'evaluation_limit':2}}
        self.save_request()
        return digest

    def save_manifest(self):
        self.c['input']['dataset_manifest']=self.asset('manifest.json',json.dumps(self.manifest).encode())

    def save_request(self):self.request.write_text(json.dumps(self.r))
    def run_check(self,**kw):return p.check(self.path,'preflight',request_path=self.request,**kw)

    def test_all_schemas_are_valid_2020_12(self):
        for file in (p.ROOT/'schema').glob('*.json'):p.Draft202012Validator.check_schema(p.load_json(file))
    def test_original_preserved_as_v01(self):
        x=p.load_json(p.ROOT/'original/X6_PF_Experiment_Contract_v0_1.json')
        self.assertEqual(x['schema_version'],'0.1.0');self.assertIsNone(x['validation_gates']['PF_G1_SYNTHETIC_BENEFIT']['thresholds']['minimum_delta_snr_db'])
    def test_draft_is_valid_but_not_ready(self):
        self.save();r=p.check(self.path);self.assertEqual(r['status'],'DRAFT_STRUCTURE_VALID');self.assertTrue(r['blockers'])
        self.assertEqual(p.check(self.path,'preflight')['status'],'BLOCKED')
    def test_exact_sweep_count_and_baseline_reuse(self):
        n=p.design_counts(self.c);self.assertEqual(n['input_cases'],72000);self.assertEqual(n['candidate_evaluations'],15552000)
        self.assertEqual(n['total_evaluations_with_reuse'],16128000)
    def test_no_false_scientific_pass(self):
        digest=self.fixture();r=self.run_check(expected_sha256=digest)
        self.assertEqual(r['status'],'READY_FOR_RUNNER_REVIEW');self.assertEqual(r['scientific_claim_status'],'UNVALIDATED')
        self.assertEqual(r['experiments_executed'],0)
    def test_null_threshold_blocks_locked_state(self):
        self.fixture();self.c['metrics']['minimum_relevant_benefit']=None;self.save()
        self.assertEqual(p.check(self.path)['status'],'INVALID')
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(p.ContractError):p.strict_json(b'{"x":1,"x":2}')
    def test_nonfinite_json_and_overflow_rejected(self):
        for raw in [b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e400}']:
            with self.subTest(raw=raw),self.assertRaises(p.ContractError):p.strict_json(raw)
    def test_unsafe_integer_rejected(self):
        with self.assertRaises(p.ContractError):p.strict_json(b'{"x":9007199254740992}')
    def test_bom_and_lone_surrogate_rejected(self):
        for raw in [b'\xef\xbb\xbf{}',b'{"x":"\\ud800"}']:
            with self.subTest(raw=raw),self.assertRaises(p.ContractError):p.strict_json(raw)
    def test_unknown_field_rejected(self):
        self.c['typo']=True;self.save();self.assertEqual(p.check(self.path)['status'],'INVALID')
    def test_unknown_version_rejected(self):
        self.c['schema_version']='9.0.0';self.save();self.assertEqual(p.check(self.path)['status'],'INVALID')
    def test_scalar_type_rejected(self):
        self.c['sampling']['sample_count']=True;self.save();self.assertEqual(p.check(self.path)['status'],'INVALID')
    def test_wrong_duration_rejected(self):
        self.c['sampling']['duration_s']=4.095;self.save();self.assertIn('DURATION_MISMATCH',str(p.check(self.path)['errors']))
    def test_nyquist_rejected(self):
        self.c['input']['frequency_end_hz']=500;self.save();self.assertIn('NYQUIST',str(p.check(self.path)['errors']))
    def test_wrap_endpoint_rejected(self):
        self.c['design']['filter_center_angle_deg'].append(180);self.save();self.assertEqual(p.check(self.path)['status'],'INVALID')
    def test_equivalent_signal_phases_rejected(self):
        self.c['design']['signal_phase_rad']=[0,2*math.pi];self.save();self.assertIn('MODULO',str(p.check(self.path)['errors']))
    def test_out_of_range_shift_rejected(self):
        self.c['design']['circular_time_shifts_samples']=[4096];self.save();self.assertIn('SHIFT',str(p.check(self.path)['errors']))
    def test_preservation_cannot_be_disabled(self):
        self.c['gates']['required_for_scoped_claim'].remove('PF_G5');self.save();self.assertIn('GATE_MISSING',str(p.check(self.path)['errors']))
    def test_individual_preservation_limits_required(self):
        self.fixture();self.c['metrics']['preservation_limits'].pop();self.save()
        self.assertIn('PRESERVATION_LIMITS',str(p.check(self.path)['errors']))
    def test_duplicate_baseline_ids_rejected(self):
        b=copy.deepcopy(self.c['baselines'][0]);b['version']='other';self.c['baselines'].append(b);self.save()
        self.assertIn('DUPLICATE_BASELINE_ID',str(p.check(self.path)['errors']))
    def test_disabled_primary_baseline_rejected(self):
        self.c['metrics']['primary_baseline_id']='UNKNOWN';self.save();self.assertIn('BASELINE_NOT_ENABLED',str(p.check(self.path)['errors']))
    def test_resource_budget_checked_before_inputs(self):
        self.c['budget']['max_evaluations']=10;self.save();self.assertIn('BUDGET_EXCEEDED',str(p.check(self.path)['errors']))
    def test_missing_external_anchor_blocks(self):
        self.fixture();self.assertEqual(self.run_check()['status'],'BLOCKED')
    def test_contract_byte_tamper_detected(self):
        digest=self.fixture();self.path.write_bytes(self.path.read_bytes()+b' ')
        self.assertIn('CONTRACT_HASH_MISMATCH',str(self.run_check(expected_sha256=digest)['errors']))
    def test_asset_tamper_detected(self):
        digest=self.fixture();(self.root/'fixture-spec.txt').write_bytes(b'changed')
        self.assertIn('ASSET_HASH_MISMATCH',str(self.run_check(expected_sha256=digest)['errors']))
    def test_path_escape_rejected(self):
        with self.assertRaises(p.ContractError):p.checked_asset(self.root,{'path':'../outside','sha256':'a'*64})
    def test_absolute_path_rejected(self):
        with self.assertRaises(p.ContractError):p.checked_asset(self.root,{'path':'/etc/passwd','sha256':'a'*64})
    def test_symlink_escape_rejected(self):
        (self.root/'link').symlink_to('/etc/passwd')
        with self.assertRaises(p.ContractError):p.checked_asset(self.root,{'path':'link','sha256':'a'*64})
    def test_manifest_mismatched_split_rejected(self):
        self.fixture();self.manifest['split']='HOLDOUT';self.save_manifest();digest=self.save()
        self.assertIn('SPLIT_MISMATCH',str(self.run_check(expected_sha256=digest)['errors']))
    def test_manifest_wrong_count_rejected(self):
        self.fixture();self.c['design']['runs_per_input_cell']=2;self.c['budget']['max_evaluations']=4;digest=self.save()
        self.assertIn('CASE_COUNT',str(self.run_check(expected_sha256=digest)['errors']))
    def test_manifest_case_outside_design_rejected(self):
        self.fixture();self.manifest['cases'][0]['snr_db']=99;self.save_manifest();digest=self.save()
        self.assertIn('OUTSIDE_DESIGN',str(self.run_check(expected_sha256=digest)['errors']))
    def test_input_array_size_rejected(self):
        self.fixture();self.manifest['cases'][0]['clean']=self.asset('clean.f64le',b'bad')
        self.save_manifest();digest=self.save();self.assertIn('BYTE_COUNT',str(self.run_check(expected_sha256=digest)['errors']))
    def test_nonfinite_array_rejected(self):
        self.fixture();self.manifest['cases'][0]['clean']=self.asset('clean.f64le',struct.pack('<4d',1,2,3,float('nan')))
        self.save_manifest();digest=self.save();self.assertIn('NON_FINITE_INPUT',str(self.run_check(expected_sha256=digest)['errors']))
    def test_reference_parameter_schema_enforced(self):
        self.fixture();self.c['baselines'][0]['parameters']={'undeclared':1};digest=self.save()
        self.assertIn('BASELINE_PARAMETERS',str(self.run_check(expected_sha256=digest)['errors']))
    def test_remote_schema_refs_rejected(self):
        with self.assertRaises(p.ContractError):p.schema_errors({},schema={'$ref':'https://example.org/schema'})
    def test_malformed_parameter_schema_fails_closed(self):
        self.fixture();self.c['baselines'][0]['parameter_schema']=self.asset('bad.schema.json',b'{"type":9}');digest=self.save()
        self.assertEqual(self.run_check(expected_sha256=digest)['status'],'INVALID')
    def test_request_digest_must_match(self):
        digest=self.fixture();self.r['contract_sha256']='a'*64;self.save_request()
        self.assertIn('REQUEST_CONTRACT_HASH',str(self.run_check(expected_sha256=digest)['errors']))
    def test_webgpu_float64_rejected(self):
        digest=self.fixture();self.r['target']='WEBGPU';self.save_request()
        self.assertIn('WEBGPU_FLOAT64',str(self.run_check(expected_sha256=digest)['errors']))
    def test_request_resource_ceiling_enforced(self):
        digest=self.fixture();self.r['resource_enforcement']['wall_timeout_seconds']=31;self.save_request()
        self.assertIn('RESOURCE_LIMIT',str(self.run_check(expected_sha256=digest)['errors']))
    def test_confirmatory_requires_holdout(self):
        self.c['experiment']['evidence_class']='CONFIRMATORY';self.save();self.assertIn('CONFIRMATORY_REQUIRES',str(p.check(self.path)['errors']))
    def test_utc_format_checked(self):
        self.c['experiment']['created_utc']='2026-99-99T10:00:00Z';self.save();self.assertEqual(p.check(self.path)['status'],'INVALID')

if __name__=='__main__':unittest.main()
