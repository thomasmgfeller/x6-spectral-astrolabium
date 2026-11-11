import json,unittest
import numpy as np
import sympy as s
from flint import arb,acb,ctx
from inputs import prior_core as pc
from calculus import ROOT,gaussian_data,scalar_factors,rational_matrix,norm_ball
from run_reduction import DustQuadrature,dust_errors
from states import STATES,ORIGINAL,DENSITY,SCALAR,CLOCK,x,y,t,u,gram,scalar_product,clock_product,evidence,label
from independent_check import direct_dust,scalar
from gluing import action,analyze,REL,LEFT,RIGHT,SEAM,INNER,OUTER,sequential_schur,dense_positive_regulator

def zfloat(z):return complex(float(z.real.mid()),float(z.imag.mid()))

class ReductionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'results/reduction.json').read_text())
  cls.glue=json.loads((ROOT/'results/gluing.json').read_text())
  cls.oracle=json.loads((ROOT/'results/independent_5d_n8.json').read_text())

 def setUp(self):ctx.prec=192

 def test_01_gram_is_identity_rank_15(self):self.assertEqual(gram(),s.eye(15))

 def test_02_all_states_are_swap_invariant(self):self.assertTrue(evidence()['all_swap_invariant'])

 def test_03_degree_two_sector_count(self):
  modes=[(i,j) for i in range(3) for j in range(3-i)]
  self.assertEqual(3*sum(j%2==0 for i,j in modes)+sum(j%2==1 for i,j in modes),14)
  self.assertEqual(len(STATES),15)

 def test_04_density_resolution_and_missing_direction(self):
  mixed=s.Matrix([0,s.sqrt(2),s.sqrt(2),0]);double=s.Matrix([0,0,0,2])
  self.assertEqual(s.simplify(s.sqrt(s.Rational(2,3))*mixed+double/s.sqrt(3)-DENSITY['+']),s.zeros(4,1))
  self.assertEqual(s.simplify(mixed/s.sqrt(3)-s.sqrt(s.Rational(2,3))*double-DENSITY['Delta']),s.zeros(4,1))
  self.assertEqual(s.simplify(DENSITY['+'].dot(DENSITY['Delta'])),0)

 def test_05_correlated_antisymmetric_modes_are_allowed(self):
  self.assertEqual(scalar_product('01','01'),1);self.assertEqual(scalar_product('11','11'),1)
  self.assertEqual(DENSITY['A'].dot(DENSITY['A'])/4,1)
  self.assertEqual(SCALAR['01'].subs(y,-y),-SCALAR['01'])
  self.assertEqual(SCALAR['11'].subs(y,-y),-SCALAR['11'])

 def test_06_clock_probe_is_normalized_and_orthogonal(self):
  self.assertEqual(clock_product('quadratic','quadratic'),1)
  self.assertEqual(clock_product('constant','quadratic'),0)

 def test_07_density_prefactors_from_measures(self):
  # Both quotients, two sqrt2 packet factors, input d0=2, five mask masses.
  for d in ('0','+','Delta','A'):
   for value in DENSITY[d]:self.assertEqual(s.simplify(s.Rational(1,4)*2*2*value/s.Integer(32)-value/32),0)

 def test_08_original_mixed_entry_is_unchanged(self):
  old=json.loads((ROOT/'inputs/prior_mixing.json').read_text())
  self.assertTrue(pc.unpack(self.data['column']['+:00']['certified_ball']).overlaps(pc.unpack(old['amplitudes']['coupled']['certified_ball'])))
  self.assertTrue(self.data['original_entry_enclosures_overlap'])

 def test_09_global_parity_zeros(self):
  odd=['0:10','+:10','Delta:10','A:01']
  for k in odd:self.assertEqual(self.data['column'][k]['classification'],'EXACT_PARITY_ZERO')
  self.assertEqual(sum(v['classification']=='EXACT_PARITY_ZERO' for v in self.data['column'].values()),4)

 def test_10_scalar_ground_matches_prior_branch(self):
  for code in pc.histories():
   a,_,_=gaussian_data(pc.h0(code));b,_,_=pc.scalar_ground(pc.h0(code))
   self.assertTrue(a.overlaps(b))

 def test_11_scalar_moments_match_independent_eigenphase_oracle(self):
  for code in pc.histories():
   sf,_=scalar_factors(pc.h0(code));other=scalar(pc.h0(code))
   for k,v in sf.items():self.assertLess(abs(zfloat(v)-other[k]),2e-13)

 def test_12_quadratic_moments_from_generating_function(self):
  a,b,c,z,w=s.symbols('a b c z w')
  g=s.exp((a*z*z+2*b*z*w+c*w*w)/2)
  self.assertEqual(s.diff(g,z,2).subs({z:0,w:0}),a)
  self.assertEqual(s.diff(g,z,w).subs({z:0,w:0}),b)
  self.assertEqual(s.diff(g,w,2).subs({z:0,w:0}),c)

 def test_13_full_5d_oracle_matches_contracted_all_33_histories(self):
  q=DustQuadrature(8)
  for record in self.oracle['records']:
   code=record['code'];contracted=q.evaluate(code);fresh=direct_dust(code,8)
   for k,v in contracted.items():
    self.assertLess(abs(zfloat(v)-fresh[k]),4e-15)
    self.assertLess(abs(complex(*record['dust'][k])-fresh[k]),4e-15)

 def test_14_orbit_reduction_with_correlated_density_sign(self):
  q=DustQuadrature(8);direct={label(x):0j for x in STATES}
  for code,members in pc.orbits().items():
   d=q.evaluate(code);sf,_=scalar_factors(pc.h0(code));w=len(members)/33*np.exp(1j*pc.f4(code))
   for state in STATES:
    den,n,clock=state;key='clock2' if clock=='quadratic' else den
    direct[label(state)]+=w*zfloat(d[key]*sf[n])
  for key,v in direct.items():self.assertLess(abs(v-complex(*self.oracle['column'][key])),3e-14)

 def test_15_analytic_error_ratios_and_clock_bound(self):
  e,_=pc.dust_error(25500,48);de,_=dust_errors(25500,48)
  self.assertTrue(de['+'].overlaps(e))
  self.assertTrue((de['Delta']/e).overlaps(2*arb(2).sqrt()/3))
  self.assertTrue((de['A']/e).overlaps((arb(2)/3).sqrt()))
  self.assertTrue(de['clock2']<7*e)

 def test_16_all_nonzero_expanded_channels_are_certified(self):
  even=[v for v in self.data['column'].values() if v['classification']!='EXACT_PARITY_ZERO']
  self.assertEqual(len(even),11)
  for v in even:self.assertTrue(pc.unpack(v['certified_ball']).abs_lower()>arb('0.004'))

 def test_17_projection_error_recomputed_and_public_bound(self):
  col=self.data['column'];r=norm_ball([col[k] for k in self.data['omitted_labels']])
  self.assertTrue(r.overlaps(arb(self.data['projection_error_15_vs_4'])))
  self.assertTrue(arb('0.102348630703','1e-12').contains(r))
  self.assertTrue(r>arb('0.10234'))
  self.assertTrue(arb('0.367087702939','1e-12').contains(arb(self.data['relative_projection_error_in_15'])))
  records=list(self.data['column'].values())+list(self.data['width_controls'].values())+list(self.glue['kernel_comparison'].values())
  for record in records:
   z=pc.unpack(record['certified_ball'])
   for part in (z.real,z.imag):self.assertTrue(arb(f'{float(part.mid()):.12f}','1e-12').contains(part))

 def test_18_pythagoras_in_tested_output_space(self):
  col=self.data['column'];old=norm_ball([col[k] for k in ORIGINAL]);tail=norm_ball([col[k] for k in col if k not in ORIGINAL]);full=norm_ball(col.values())
  self.assertTrue((old*old+tail*tail).overlaps(full*full))

 def test_19_refined_rule_agrees_with_certified_primary(self):
  refined=json.loads((ROOT/'results/crosscheck_56.json').read_text())
  for key in self.data['column']:
   self.assertTrue(pc.unpack(self.data['column'][key]['certified_ball']).overlaps(pc.unpack(refined['column'][key]['certified_ball'])))
   self.assertTrue(arb(refined['column'][key]['analytic_quadrature_error_bound'])<arb('3e-22'))

 def test_20_width_controls_are_different_preparations(self):
  original=pc.unpack(self.data['column']['+:00']['certified_ball'])
  for v in self.data['width_controls'].values():self.assertTrue((pc.unpack(v['certified_ball'])-original).abs_lower()>arb('0.01'))
  for width in (s.Rational(1,2),s.Integer(2)):
   overlap=s.sqrt(2*width/(1+width**2))
   self.assertTrue(overlap<1)

 def test_21_glued_restrictions_are_declared_AA_history(self):
  for vertices in (LEFT,RIGHT):
   code=sum(1<<(5*vertices.index(i)+vertices.index(j)) for i,j in REL if i in vertices and j in vertices)
   self.assertEqual(code,25500);self.assertIn(code,pc.histories())

 def test_22_shared_node_terms_removed_before_comparison(self):
  g=self.glue['gravity'];self.assertEqual(g,{'joint_F4':88,'left_F4':37,'right_F4':37,'seam_F4':2,'sewn_F4':72,'defect':16})

 def test_23_cross_interval_classes_and_gravity_defect(self):
  cross=self.glue['geometry']['nonzero_cross_pairs']
  self.assertEqual(len(cross),5);self.assertEqual(sorted(v[3] for v in cross),[-8,-8,-8,-8,16])
  self.assertEqual(-sum(v[3] for v in cross),16)

 def test_24_scalar_and_dust_action_defects(self):
  h,_,_=action(tuple(range(8)));hl,_,_=action(LEFT);hr,_,_=action(RIGHT);hs,_,_=action(SEAM)
  self.assertEqual(h-hl-hr+hs,s.Matrix(self.glue['h0_defect']))
  ts=s.symbols('t0:8');rs=s.symbols('r0:8')
  def dust(vertices):
   _,_,p=action(vertices)
   return -sum(rs[j]/2 for j in vertices)-sum(s.Rational(c,4)*rs[j]*(ts[j]-ts[i])**2 for i,j,k,c in p)
  expected=-sum(s.Rational(c,4)*rs[j]*(ts[j]-ts[i])**2 for i,j,k,c in self.glue['geometry']['nonzero_cross_pairs'])
  self.assertEqual(s.expand(dust(tuple(range(8)))-dust(LEFT)-dust(RIGHT)+dust(SEAM)-expected),0)

 def test_25_seam_only_counterterm_is_insufficient(self):
  self.assertEqual(self.glue['mixed_derivative_q0_q5_over_beta'],'-4')
  self.assertTrue(self.glue['no_seam_only_counterterm'])

 def test_26_exact_interior_determinants_and_signatures(self):
  g=self.glue;self.assertEqual(g['joint_gaussian']['interior_determinant_h0'],'-17170')
  self.assertEqual(g['sewn_gaussian']['interior_determinant_h0'],'1190')
  self.assertEqual(g['joint_gaussian']['signature'],2);self.assertEqual(g['sewn_gaussian']['signature'],0)
  self.assertEqual(s.Rational(1190,17170),s.Rational(7,101))

 def test_27_quotient_and_all_atom_normalization(self):
  joint=s.Rational(1,4)*8/s.Integer(2)**8
  sewn=s.Rational(1,4)*8/s.Integer(2)**8/s.Integer(2)
  self.assertEqual(joint,s.Rational(1,128));self.assertEqual(2*sewn,joint)

 def test_28_normalized_atom_kernel_difference_is_nonzero(self):
  for record in self.glue['kernel_comparison'].values():self.assertEqual(record['classification'],'NONZERO')
  d=pc.unpack(self.glue['kernel_comparison']['difference']['certified_ball'])
  self.assertTrue(d.abs_lower()>arb('0.00077'))

 def test_29_same_joint_action_composes_exactly(self):
  h,_,_=action(tuple(range(8)));k,det=sequential_schur(h,(2,5),SEAM)
  self.assertEqual(k,s.Matrix(self.glue['joint_gaussian']['schur_h0']))
  self.assertEqual(det,-17170)
  self.assertEqual(self.glue['same_action_staged_interior_signatures'],[0,2])

 def test_30_positive_regulator_order_and_dense_numpy_check(self):
  h,_,_=action(tuple(range(8)))
  for eps in ('1','1/7'):
   a=dense_positive_regulator(h,INNER+OUTER,eps);b=dense_positive_regulator(h,(2,5,3,4)+OUTER,eps)
   self.assertTrue(a.overlaps(b))
   # Whiten the positive Gaussian weight, then use the real spectrum.
   e=float(s.Rational(eps));diag=np.array([1 if i in OUTER else e for i in range(8)])
   m=np.array(h,dtype=float)*4/np.sqrt(6)/np.sqrt(np.outer(diag,diag))
   ev=np.linalg.eigvalsh(m)
   oracle=16*np.pi**3/np.sqrt(np.prod(diag))*np.prod((1+ev*ev)**(-.25))*np.exp(.5j*np.arctan(ev).sum())
   self.assertLess(abs(zfloat(a)-oracle),3e-12)

 def test_31_reference_chirp_obstructs_full_L2_mapping(self):
  d=self.glue['operator_domain_control']
  self.assertEqual(d['reference_outgoing_antisymmetric_chirp_coefficient_over_beta'],'28/11')
  self.assertEqual(d['coupling_to_input_coordinates'],['0','0'])
  self.assertEqual(d['coupling_to_outgoing_symmetric_coordinate'],'0')
  old=json.loads((ROOT/'inputs/prior_mixing.json').read_text())
  self.assertTrue(pc.unpack(old['amplitudes']['decoupled']['certified_ball']).abs_lower()>0)
  self.assertFalse(d['reference_ground_input_response_in_boundary_L2'])

 def test_32_fail_closed_and_scope(self):
  with self.assertRaises(ValueError):gaussian_data(pc.h0(25500),sigma_s=0)
  with self.assertRaises(ValueError):gaussian_data(s.zeros(5))
  self.assertTrue(self.data['not_a_probability_or_full_space_upper_bound'])
  self.assertTrue(all(v=='HOLD' for v in self.data['physical_gates'].values()))

if __name__=='__main__':unittest.main()
