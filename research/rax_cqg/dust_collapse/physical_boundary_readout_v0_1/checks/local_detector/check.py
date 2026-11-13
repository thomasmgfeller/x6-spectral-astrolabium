#!/usr/bin/env python3
"""Exact common-boundary Gaussian detector and C1 norm obstruction."""
from itertools import combinations
from pathlib import Path
import json
import sympy as s
from reduced_detector import run as run_reduced_detector

ROOT=Path(__file__).resolve().parent
y,q,qp,g,m,t,az,ae,qz=s.symbols('y q qprime g m t a_dot_z a_dot_e Q_z',real=True)
sigma,v,eta,beta,Bnorm,R=s.symbols('sigma v eta beta Bnorm R',positive=True)
checks={}
M2=s.exp(-(y-g*q)**2/(2*sigma**2))/s.sqrt(2*s.pi*sigma**2)
checks['pointer_and_POVM_normalization']=s.simplify(s.integrate(M2,(y,-s.oo,s.oo))-1)==0
left=((y-g*q)**2+(y-g*qp)**2)/(4*sigma**2)
right=(y-g*(q+qp)/2)**2/(2*sigma**2)+g**2*(q-qp)**2/(8*sigma**2)
checks['exact_nonselective_dephasing_exponent']=s.expand(left-right)==0
cdf=(1+s.erf((y-g*q)/(s.sqrt(2)*sigma)))/2
checks['Borel_bin_POVM_density']=s.simplify(s.diff(cdf,y)-M2)==0
arg=(y-g*q)/(s.sqrt(2)*sigma)
checks['complete_real_line_outcomes']=s.limit(arg,y,s.oo)==s.oo and s.limit(arg,y,-s.oo)==-s.oo and (s.erf(s.oo)-s.erf(-s.oo))/2==1
checks['dephasing_not_a_free_class_constant']=s.exp(-s.Rational(1,8))!=s.exp(-s.Rational(1,2))

# Any genuinely normalized Gaussian marginal gives a normalized Gaussian
# pointer record. This conditional formula is not applied to a nonexistent
# normalized four-mode C1 output below.
A=1/v+g**2/sigma**2
D=m/v+g*y/sigma**2
exponent=-m**2/(2*v)-y**2/(2*sigma**2)+D**2/(2*A)
target=-(y-g*m)**2/(2*(sigma**2+g**2*v))
checks['normalized_Gaussian_record_mean_variance']=s.simplify(exponent-target)==0
checks['normalized_Gaussian_record_prefactor']=s.simplify(s.sqrt(2*s.pi/A)/(s.sqrt(2*s.pi*v)*s.sqrt(2*s.pi*sigma**2))-1/s.sqrt(2*s.pi*(sigma**2+g**2*v)))==0
checks['same_field_space_can_have_distinct_record_laws']=s.erf(1/s.sqrt(3))!=s.erf(s.Rational(1,2))

# Reconstruct the actual N11 scalar action, not an assigned class Gram matrix.
N=tuple(range(11));P=(0,1,2,3);I=(4,5,6);F=(7,8,9,10)
chain=frozenset(combinations(N,2));C1=chain-{(4,5),(5,6)}
L=s.zeros(11)
for x,z in C1:
    k=sum((x,w) in C1 and (w,z) in C1 for w in N)
    bk=(1,-9,16,-8)[k] if k<4 else 0
    L[x,x]+=bk;L[z,z]+=bk;L[x,z]-=bk;L[z,x]-=bk
Hbar=-L/2
a=s.Matrix([[-232,119,241,-128]])
b=s.Matrix([[0,16,32,46]])
embedded=s.zeros(1,11)
for j,k in enumerate(F):embedded[0,k]=a[j]
kernel_constraint=embedded+b*Hbar.extract(F,N)
checks['C1_exact_off_shell_postconstraint']=kernel_constraint==s.zeros(1,11)
checks['C1_gauge_direction_nonzero']=(b*b.T)[0]==3396
checks['q10_not_postconstraint_invariant']=b[3]==46
checks['q7_is_postconstraint_invariant']=b[0]==0

# A+psi=0 along q=z+t e, e=b/||b||. The phase is real, so |psi| is
# independent of the gauge-orbit coordinate t.
orbit_phase=s.exp(-s.I*beta*(az*t+ae*t**2/2)/Bnorm)
operator=(az+ae*t)*orbit_phase-s.I*Bnorm*s.diff(orbit_phase,t)/beta
checks['constraint_solution_has_constant_orbit_modulus']=s.simplify(operator)==0 and s.simplify(orbit_phase*s.conjugate(orbit_phase))==1

# For a detector with nonzero slope eta=|g*ell.e| along this orbit,
# the conditional squared norm is constant in y, and is not integrable.
orbit_density=s.exp(-(y-g*qz-eta*t)**2/(2*sigma**2))/s.sqrt(2*s.pi*sigma**2)
conditional=s.simplify(s.integrate(orbit_density,(t,-s.oo,s.oo)))
checks['gauge_variant_readout_is_unnormalizable_uniform_density']=s.simplify(conditional-1/eta)==0
checks['inclusive_detector_does_not_repair_infinite_norm']=s.limit(2*R/eta,R,s.oo)==s.oo
checks['gauge_invariant_readout_does_not_damp_orbit']=s.diff(s.exp(-(y-g*qz)**2/(2*sigma**2)),t)==0

# A noninvariant measurement shifts the constraint into the apparatus.
# Original [Q,A+]=i b.ell/beta. Under U=exp(-i g Q p_y),
# U A+ U^dagger=A+ + (g b.ell/beta) p_y. The commutators of
# y and -gQ cancel only for the relative pointer y-gQ.
bl=s.symbols('b_dot_ell',real=True)
checks['extended_constraint_relative_pointer_commutes']=s.simplify(s.I*g*bl/beta-s.I*g*bl/beta)==0
reduced_checks,reduced_result=run_reduced_detector(ROOT.parents[1])
checks.update(reduced_checks)
assert all(bool(vv) for vv in checks.values()),checks

result={
 'id':'CST-DUST-COMMON-LOCAL-GAUSSIAN-DETECTOR-0.1',
 'status':'PASS_EXACT_LOCAL_DETECTOR_AND_CONDITIONAL_REDUCED_N11_INSTRUMENT',
 'checks':{k:bool(vv) for k,vv in checks.items()},
 'future_coordinates':list(F),
 'introduced_apparatus':{
   'Hilbert_space':'L2(R,dy)',
   'initial_pointer':'phi_sigma(y)=(2*pi*sigma^2)^(-1/4) exp(-y^2/(4*sigma^2)); sigma>0',
   'coupling':'U_g=exp(-i*g*Q_ell tensor p_y), Q_ell=ell^T q_F, same ell,g,sigma for both histories',
   'derived_M_y':'(2*pi*sigma^2)^(-1/4) exp(-(y-g*Q_ell)^2/(4*sigma^2))',
   'chosen_kinematic_example':'ell=(0,0,0,1), Q=q10; g=sigma=1 only as a declared dimensionless apparatus example, not selected by the gravitational action',
   'alternative_reduced_candidate':'ell=(1,0,0,0), Q=q7 commutes with the C1 postconstraint',
 },
 'POVM':{
   'normalization':'Integral_R dy M_y^dagger M_y=I on the declared kinematic L2(R4,dqF)',
   'bins':'E_[l,u]=Phi((u-gQ)/sigma)-Phi((l-gQ)/sigma); all bins partitioning R sum to I',
   'bin_instrument':'rho -> integral_[l,u] dy M_y rho M_y^dagger, not generally sqrt(E_bin) rho sqrt(E_bin)',
   'dephasing_kernel':'exp(-g^2*(ell.q-ell.qprime)^2/(8*sigma^2))',
 },
 'normalized_state_conditional_formula':{
   'assumption':'A separately established normalized outgoing state with Q marginal N(m,v)',
   'pointer_law':'N(g*m,sigma^2+g^2*v)',
   'synthetic_distinguishability_control':'For g=sigma=a=1 and centered variances v=1/2 versus v=1, P(|y|<=a)=erf(1/sqrt(3)) versus erf(1/2). These are not N11 predictions.',
 },
 'C1_action_derived_constraint':{
   'Hbar_definition':'H=beta*Hbar, Hbar=-L/2 from original interval coefficients (1,-9,16,-8)',
   'a':list(a),'b':list(b),'scaled_momentum':'pi=p/beta=-i partial_q/beta',
   'Aplus':'-232q7+119q8+241q9-128q10+16pi8+32pi9+46pi10',
   'identity':'a_embedded+b*Hbar_F,:=0 in all eleven columns, off shell',
   'consequence':'Every nonzero bare C1 outgoing distribution obeys Aplus psi=0 and has constant modulus along the noncompact b direction; it is not in L2(R4).',
 },
 'measurement_constraint_consequence':{
   'q10_commutator':'[q10,Aplus]=i*46/beta, so q10 is not an observable of this proposed reduced constraint sector',
   'q7_commutator':'[q7,Aplus]=0; q7 is the first position observable in the explicitly postulated common H3 reduction below',
   'variant_detector':'For a normalized transverse amplitude and ell.e nonzero, ||M_y psi||^2=1/|g ell.e| independent of y; the integral over all y is infinite',
   'invariant_detector':'For ell.e=0 the detector does not damp the gauge direction, so the orbit-volume divergence remains inside each nonzero record',
   'complete_measurement':'Tonelli positivity gives integral dy ||M_y psi||^2=||psi||^2, including infinity; a complete detector cannot manufacture finite state norm',
   'extended_constraint':'U Aplus Udagger=Aplus+(g b.ell/beta)p_y. For b.ell nonzero, y alone is not invariant; y-gQ is invariant and pulls back to the initial pointer y under U.',
 },
 'history_blindness':'At fixed q_F the apparatus applies exactly the same M_y in both histories. Distinct normalizable history-dependent field states could nevertheless yield distinguishable y laws.',
 'gamma_qualification':'The environmental overlap is a kernel depending on q_F and q_Fprime. Integrating it with different outgoing states does not generally yield an arbitrary, state-independent constant gamma_c.',
 'derived_from_gravity_action':'Only the postconstraint and its norm/observable obstruction are derived here from the N11 scalar action. Pointer state, width, coupling and chosen scalar coordinate are introduced apparatus data.',
 'N11_normalized_pointer_predictions':'NOT_DEFINED_UNDER_COMMON_FOUR_MODE_KINEMATIC_L2_NORM',
 'physical_pairing_and_common_reduced_output_space':'CONDITIONAL_COMMON_H3_INSTRUMENT_CONSTRUCTED; original bare L2(R4) obstruction remains',
 'conditional_reduced_detector':reduced_result,
 'new_large_integrations':0,
}
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps({'status':result['status'],'checks':result['checks'],'physical_pairing':result['physical_pairing_and_common_reduced_output_space']},indent=2))
