"""Synthetic regression tests; these never establish a hardware property."""
import copy, hashlib, itertools, json, math, random, tempfile, unittest
from pathlib import Path
import analysis as a
ROOT=Path(__file__).resolve().parent
class Arithmetic(unittest.TestCase):
 def test_poisson_zero(self): self.assertAlmostEqual(a.poisson_upper(0,600),-math.log(.01)/600,14)
 def test_poisson_reference_values(self):
  # Independent inverse-chi-square values, scipy chi2.ppf(.99,2*(n+1))/1200.
  for n,x in [(1,.011063920113323017),(100,.2097310881393421),(60000,100.95385247407138)]:
   self.assertAlmostEqual(a.poisson_upper(n,600),x,8)
 def test_poisson_invalid(self):
  for x in [-1,1.5,True]:
   with self.assertRaises(ValueError): a.poisson_upper(x,600)
  with self.assertRaises(ValueError): a.poisson_upper(0,0)
 def test_zero_failure_bound(self):self.assertAlmostEqual(a.zero_error_upper(1000000),4.605159582098488e-6,15)
 def test_photon_flux(self):self.assertAlmostEqual(a.photon_flux(1e-12,810),4077634.419709594,5)
 def test_pulsed_efficiency(self):
  z=a.pulsed_efficiency(40,1000,1,1000,.1)
  self.assertAlmostEqual(z['eta_point'],(math.log(.999)-math.log(.96))/.1)
  self.assertEqual(z['uncertainty_status'],'NOT_EVALUATED')
 def test_saturation_and_inconsistent_eta(self):
  with self.assertRaises(ValueError):a.pulsed_efficiency(100,100,0,100,.1)
  self.assertEqual(a.pulsed_efficiency(90,100,0,100,.1)['model_status'],'INCONSISTENT_WITH_MODEL')
 def test_no_negative_signal_clipping(self):
  with self.assertRaises(ValueError):a.pulsed_efficiency(0,100,1,100,.1)
 def test_afterpulse_observed_window(self):
  self.assertAlmostEqual(a.secondary_excess(20,1000,10,1000)['observed_window_excess_probability'],.01/.99)
 def test_negative_afterpulse_estimate_preserved(self):self.assertLess(a.secondary_excess(0,1000,10,1000)['observed_window_excess_probability'],0)
 def test_deconvolution_requires_independence(self):self.assertEqual(a.independent_deconvolution(100,20,20)['status'],'HOLD_COVARIANCE_MODEL')
 def test_nonpositive_deconvolution_unresolved(self):self.assertIsNone(a.independent_deconvolution(10,20,5,True)['sigma_dut_ps'])
 def test_conditional_deconvolution(self):self.assertAlmostEqual(a.independent_deconvolution(50,30,0,True)['sigma_dut_ps'],40)
 def test_frozen_linearity(self):self.assertAlmostEqual(a.rate_linearity(100,51,1,.5),0)
 def test_recovery_is_probability_ratio(self):self.assertAlmostEqual(a.recovery_ratio(45,100,.5),.9)
 def test_nonfinite_rejected(self):
  for x in [float('nan'),float('inf'),True]:
   with self.assertRaises(ValueError):a.photon_flux(x,810)
class Timing(unittest.TestCase):
 def test_uint64_difference_before_float(self):
  z=a.timing_groups([{'pulse_id':0,'t_ps':[2**63,2**63+1,2**63+2,2**63+3]}],[0,0,0,0])
  self.assertEqual(z['pairs'][0]['mean_ps'],1)
 def test_offset_is_frozen_not_fitted(self):
  z=a.timing_groups([{'pulse_id':k,'t_ps':[1000*k,1000*k+130,1000*k+20,1000*k]} for k in range(3)],[0,100,20,0])
  self.assertEqual(z['pairs'][0]['mean_ps'],30)
 def test_tails_not_window_cropped(self):
  z=a.timing_groups([{'pulse_id':k,'t_ps':[10000,10000+d,10000,10000]} for k,d in enumerate([0,0,4000])],[0]*4)
  self.assertEqual(z['pairs'][0]['n_pairs'],3); self.assertEqual(z['pairs'][0]['maximum_ps'],4000)
  self.assertGreater(z['pairs'][0]['sigma_ps'],200)
 def test_missing_is_not_zero(self):
  z=a.timing_groups([{'pulse_id':0,'t_ps':[0,None,0,0]}],[0]*4)
  self.assertIsNone(z['pairs'][0]['mean_ps']);self.assertEqual(z['pairs'][0]['missing_groups'],1)
 def test_duplicate_pulse_id_rejected(self):
  with self.assertRaises(ValueError):a.timing_groups([{'pulse_id':0,'t_ps':[0]*4}]*2,[0]*4)
 def test_timestamp_overflow_rejected(self):
  with self.assertRaises(ValueError):a.timing_groups([{'pulse_id':0,'t_ps':[2**64,0,0,0]}],[0]*4)
class Coincidences(unittest.TestCase):
 def run_events(self,ev,**kw):return a.coincidence_components([{'channel':c,'t_ps':t} for c,t in ev],[0]*4,**kw)
 def test_inclusive_window_and_outside(self):
  self.assertEqual(self.run_events([(0,0),(2,1000)])['unique_pairs'],1)
  self.assertEqual(self.run_events([(0,0),(2,1001)])['unique_pairs'],0)
 def test_odd_width(self):self.assertEqual(self.run_events([(0,0),(2,1001)],full_window_ps=2001)['unique_pairs'],0)
 def test_many_to_one_is_not_two_pairs(self):
  z=self.run_events([(0,0),(1,2),(2,1)]);self.assertEqual(z['unique_pairs'],0);self.assertEqual(z['ambiguous_components'],1)
 def test_transitive_component(self):
  z=self.run_events([(0,0),(2,900),(1,1800),(3,2700)]);self.assertEqual(z['ambiguous_components'],1);self.assertEqual(z['unique_pairs'],0)
 def test_same_arm_never_pairs(self):self.assertEqual(self.run_events([(0,0),(1,0)])['unmatched_singles'],2)
 def test_delay_applied_to_b(self):self.assertEqual(self.run_events([(0,50000),(2,0)],b_shift_ps=50000)['unique_pairs'],1)
 def test_offsets_once(self):self.assertEqual(a.coincidence_components([{'channel':0,'t_ps':0},{'channel':2,'t_ps':5000}],[0,0,5000,0])['unique_pairs'],1)
 def test_random_against_naive_graph(self):
  rng=random.Random(231)
  for _ in range(100):
   ev=[(rng.randrange(4),rng.randrange(10000)) for __ in range(20)]
   adj={i:set() for i in range(len(ev))}
   for i,(ci,ti) in enumerate(ev):
    for j,(cj,tj) in enumerate(ev):
     if (ci<2)!=(cj<2) and abs(ti-tj)<=1000:adj[i].add(j)
   seen=set();u=m=0;un=0
   for i in adj:
    if i in seen:continue
    comp=set();q=[i]
    while q:
     j=q.pop()
     if j in comp:continue
     comp.add(j);q.extend(adj[j]-comp)
    seen|=comp
    if len(comp)==1:un+=1
    elif len(comp)==2:u+=1
    else:m+=1
   z=self.run_events(ev);self.assertEqual((z['unique_pairs'],z['ambiguous_components'],z['unmatched_singles']),(u,m,un))
class Screen(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'Referenzvertrag.json').read_text());self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)
  (self.p/'synthetic.txt').write_text('SYNTHETIC fixture, not hardware evidence\n')
  r=json.loads((ROOT/'Referenzmessung.template.json').read_text());r['origin']='SYNTHETIC'
  r['identity']={k:'SYNTHETIC' for k in self.c['required_identity']}
  r['identity']['channel_map']=self.c['channel_map'];r['identity']['detector_serials']=['s0','s1','s2','s3'];r['identity']['cable_ids']=['c0','c1','c2','c3']
  r['configuration']=copy.deepcopy(self.c['required_configuration'])
  for ru in self.c['numeric_rules']:
   v=ru.get('lower',1)
   if 'upper' in ru:v=(v+ru['upper'])/2
   if ru.get('type')=='integer':v=int(v)
   r['bounds'][ru['key']]=[{'lower':v,'upper':v,'basis':'SYNTHETIC_TEST_ONLY'} for _ in range(ru['count'])]
  r['evidence']=[{'path':'synthetic.txt','sha256':hashlib.sha256((self.p/'synthetic.txt').read_bytes()).hexdigest()}]
  r['tests']={t:{'review':'ACCEPTED','reviewer':'SYNTHETIC_FIXTURE','evidence':['synthetic.txt']} for t in self.c['required_tests']};self.r=r
 def tearDown(self):self.tmp.cleanup()
 def screen(self):return a.reference_screen(self.r,self.c,self.p)
 def test_template_stays_hold(self):
  r=json.loads((ROOT/'Referenzmessung.template.json').read_text());z=a.reference_screen(r,self.c,self.p)
  self.assertEqual(z['screen_status'],'HOLD');self.assertEqual(z['physical_qualification'],'NOT_RUN')
 def test_synthetic_never_qualified(self):
  z=self.screen();self.assertEqual(z['screen_status'],'SYNTHETIC_ONLY');self.assertEqual(z['bom_freeze'],'HOLD')
 def test_even_complete_screen_requires_review(self):
  self.r['origin']='MEASURED' # synthetic fixture exercises status logic only
  z=self.screen();self.assertEqual(z['screen_status'],'NUMERICAL_SCREEN_PASS');self.assertEqual(z['physical_qualification'],'REVIEW_REQUIRED')
 def test_missing_measurement_hold(self):
  self.r['bounds']['supply_V'][0]['lower']=None;self.assertEqual(self.screen()['screen_status'],'HOLD')
 def test_upper_uncertainty_crossing_fails(self):
  self.r['bounds']['electrical_pair_sigma_ps'][0]['upper']=201;self.assertEqual(self.screen()['screen_status'],'FAIL')
 def test_wrong_channelmap_fails(self):
  self.r['identity']['channel_map']=['A-','A+','B+','B-'];self.assertEqual(self.screen()['screen_status'],'FAIL')
 def test_silent_filter_fails(self):
  self.r['configuration']['software_filter_enabled']=True;self.assertEqual(self.screen()['screen_status'],'FAIL')
 def test_wrong_identity_vector_rejected(self):
  self.r['identity']['detector_serials']=['only-one']
  with self.assertRaises(ValueError):self.screen()
 def test_tampered_evidence_fails(self):
  (self.p/'synthetic.txt').write_text('changed');self.assertEqual(self.screen()['screen_status'],'FAIL')
 def test_absent_evidence_hold(self):
  (self.p/'synthetic.txt').unlink();self.assertEqual(self.screen()['screen_status'],'HOLD')
 def test_path_traversal_rejected(self):
  self.r['evidence'][0]['path']='../outside'
  with self.assertRaises(ValueError):self.screen()
 def test_duplicate_evidence_rejected(self):
  self.r['evidence']*=2
  with self.assertRaises(ValueError):self.screen()
 def test_nan_rejected(self):
  self.r['bounds']['input_V'][0]['lower']=float('nan')
  with self.assertRaises(ValueError):self.screen()
 def test_noninteger_counter_rejected(self):
  self.r['bounds']['missing_count'][0]['lower']=.5
  with self.assertRaises(ValueError):self.screen()
 def test_count_cancellation_cannot_pass(self):
  self.r['bounds']['missing_count'][0].update(lower=1,upper=1)
  self.r['bounds']['duplicate_count'][0].update(lower=1,upper=1)
  self.assertEqual(self.screen()['screen_status'],'FAIL')
 def test_zero_timestamp_step_fails(self):
  self.r['bounds']['timestamp_step_ps'][0].update(lower=0,upper=0);self.assertEqual(self.screen()['screen_status'],'FAIL')
 def test_manual_rejection_fails(self):
  self.r['tests']['R01']['review']='REJECTED';self.assertEqual(self.screen()['screen_status'],'FAIL')
if __name__=='__main__':unittest.main()
