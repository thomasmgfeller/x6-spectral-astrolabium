"""Exact action obstruction and matched all-atom kernel control on eight points."""
import json
import sympy as s
from flint import arb,acb,ctx
from inputs import prior_core as pc
from calculus import ROOT,gaussian_data,rational_matrix,summarize

LAYERS=(0,0,1,2,2,3,4,4)
REL={(i,j) for i in range(8) for j in range(8) if LAYERS[i]<LAYERS[j]}
LEFT=(0,1,2,3,4);RIGHT=(3,4,5,6,7);SEAM=(3,4);INNER=(2,3,4,5);OUTER=(0,1,6,7)

def action(vertices):
 h=s.zeros(8);f=len(vertices);pairs=[]
 for i,j in sorted(REL):
  if i not in vertices or j not in vertices:continue
  k=sum((i,z) in REL and (z,j) in REL for z in vertices)
  c=(1,-9,16,-8)[k] if k<4 else 0;f-=c;pairs.append((i,j,k,c))
  h[i,i]-=s.Rational(c,2);h[j,j]-=s.Rational(c,2);h[i,j]+=s.Rational(c,2);h[j,i]+=s.Rational(c,2)
 return h,f,pairs

def dense_positive_regulator(h,order,epsilon):
 """Independent full eight-variable Gaussian elimination at epsilon>0."""
 eps=arb(epsilon)
 if not eps>0:raise ValueError('positive regulator required')
 q=[[acb(arb(1) if i==j and i in OUTER else (eps if i==j else 0),-pc.beta()*arb(str(h[i,j]))) for j in order] for i in order]
 root=acb(1)
 for k in range(8):
  pivot=q[k][k]
  if not pivot.real>0:raise ArithmeticError('regulated Gaussian lost accretivity')
  root*=pivot.sqrt(analytic=True)
  for i in range(k+1,8):
   for j in range(k+1,8):q[i][j]-=q[i][k]*q[k][j]/pivot
 return 16*arb.pi()**3/root

def sequential_schur(h,first,second):
 """Exact block elimination keeps the original joint action throughout."""
 rest=tuple(x for x in range(8) if x not in first)
 a=h.extract(first,first);r=h.extract(rest,rest)-h.extract(rest,first)*a.inv()*h.extract(first,rest)
 middle=tuple(rest.index(x) for x in second);outer=tuple(rest.index(x) for x in OUTER)
 b=r.extract(middle,middle)
 k=r.extract(outer,outer)-r.extract(outer,middle)*b.inv()*r.extract(middle,outer)
 return k,s.factor(a.det()*b.det())

def encode(m):return [[str(m[i,j]) for j in range(m.cols)] for i in range(m.rows)]

def analyze():
 ctx.prec=192
 h,f,pairs=action(tuple(range(8)));hl,fl,_=action(LEFT);hr,fr,_=action(RIGHT);hs,fs,_=action(SEAM)
 sewn=hl+hr-hs;fsewn=fl+fr-fs;delta=h-sewn
 cross=[(i,j,k,c) for i,j,k,c in pairs if i<3 and j>4 and c]
 # All eight densities are at their atoms. The common boundary/packet factor
 # is (1/2)^2 * (sqrt(2)*2)^2 * (1/2)^8 = 1/128.
 density_factor=arb(1)/128
 joint,_,jm=gaussian_data(h,INNER,OUTER);naive,_,nm=gaussian_data(sewn,INNER,OUTER)
 mj=density_factor*acb(0,f).exp()*joint;mn=density_factor*acb(0,fsewn).exp()*naive
 records={'joint':summarize(mj,arb(0)),'sewn_local_action':summarize(mn,arb(0)),
          'difference':summarize(mj-mn,arb(0)),
          'scalar_difference_without_gravity_phase':summarize(density_factor*(joint-naive),arb(0))}
 k,det=sequential_schur(h,(2,5),SEAM)
 if k!=s.Matrix(jm['schur_h0']) or det!=s.Rational(jm['interior_determinant_h0']):raise ArithmeticError('same-action block composition failed')
 first=(2,5);rest=tuple(x for x in range(8) if x not in first)
 a=h.extract(first,first);remaining=h.extract(rest,rest)-h.extract(rest,first)*a.inv()*h.extract(first,rest)
 seam_indices=tuple(rest.index(x) for x in SEAM);second=remaining.extract(seam_indices,seam_indices)
 def signature(mat):
  _,d=mat.LDLdecomposition(hermitian=False)
  return int(sum(s.sign(d[i,i]) for i in range(d.rows)))
 staged_signatures=[signature(a),signature(second)]
 if sum(staged_signatures)!=jm['signature']:raise ArithmeticError('staged Fresnel phases disagree')
 q=s.symbols('q0:8',real=True);t=s.symbols('t0:8',real=True);r=s.symbols('r0:8',real=True)
 dscalar=-sum(s.Rational(c,4)*(q[j]-q[i])**2 for i,j,k,c in cross)
 ddust=-sum(s.Rational(c,4)*r[j]*(t[j]-t[i])**2 for i,j,k,c in cross)
 if s.simplify(dscalar-(s.Matrix(q).T*delta*s.Matrix(q))[0]/2)!=0:raise ArithmeticError('action defect formula mismatch')
 ref=rational_matrix(pc.reference_h0());_,_,refmeta=gaussian_data(ref)
 sk=s.Matrix(refmeta['schur_h0']);v=s.Matrix([0,0,1/s.sqrt(2),-1/s.sqrt(2)])
 out_a=s.simplify((v.T*sk*v)[0]);cross_to_input=[s.simplify((s.eye(4)[:,j].T*sk*v)[0]) for j in (0,1)]
 cross_to_s=s.simplify((s.Matrix([0,0,1/s.sqrt(2),1/s.sqrt(2)]).T*sk*v)[0])
 domain={'reference_outgoing_antisymmetric_chirp_coefficient_over_beta':str(out_a),
         'coupling_to_input_coordinates':[str(x) for x in cross_to_input],
         'coupling_to_outgoing_symmetric_coordinate':str(cross_to_s),
         'reference_ground_input_response_in_boundary_L2':False,
         'reason':'nonzero dust response and undamped exp(i*beta*(28/11)*q_a^2/2); its modulus is independent of q_a on the whole real line',
         'original_coupled_response_L2_status':'NOT_PROVED_OR_DISPROVED_BY_THIS_REFERENCE_CONTROL'}
 return {'geometry':{'layers':list(LAYERS),'left':list(LEFT),'right':list(RIGHT),'seam':list(SEAM),
                     'nonzero_cross_pairs':cross,'left_right_codes':[25500,25500]},
         'gravity':{'joint_F4':f,'left_F4':fl,'right_F4':fr,'seam_F4':fs,'sewn_F4':fsewn,'defect':f-fsewn},
         'h0_joint':encode(h),'h0_sewn':encode(sewn),'h0_defect':encode(delta),
         'scalar_action_defect_over_beta':str(s.expand(dscalar)),
         'dust_action_defect_over_beta':str(s.expand(ddust)),
         'mixed_derivative_q0_q5_over_beta':str(s.diff(dscalar,q[0],q[5])),
         'no_seam_only_counterterm':s.diff(dscalar,q[0],q[5])!=0,
         'joint_gaussian':jm,'sewn_gaussian':nm,'all_atom_density_factor':'1/128',
         'kernel_comparison':records,
         'conditional_inner_kernel_magnitude_ratio_at_zero_outer_field':(arb(7)/101).sqrt().str(25,more=True),
         'same_action_block_elimination_agrees_exactly':True,
         'same_action_staged_interior_signatures':staged_signatures,
         'positive_regulator_order_check':all(dense_positive_regulator(h,INNER+OUTER,e).overlaps(dense_positive_regulator(h,(2,5,3,4)+OUTER,e)) for e in ('1','1/7')),
         'operator_domain_control':domain,
         'scope':'fixed history and density-resolved all-atom contribution; no full 1089-pair or positive-density eight-point sum computed'}

if __name__=='__main__':
 result=analyze();(ROOT/'results/gluing.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:result[k] for k in ('gravity','kernel_comparison','operator_domain_control')},indent=2))
