#!/usr/bin/env python3
"""Independent finite-domain audit, with exact arithmetic in Q(sqrt(-6)).

Rebuilds the history Hessians from the frozen generating relations, rather
than importing Dowker's Hessians. No Gaussian determinant branch is selected
and no clock integral is recomputed. Existing interval certificates remain
inherited premises, not independently reintegrated theorems.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


class Quad:
    """a+b*u, u^2=-6, with exact rational coefficients."""
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Quad) else Quad(x)
    def __add__(self, x):
        x = self.coerce(x)
        return Quad(self.a+x.a, self.b+x.b)
    __radd__ = __add__
    def __neg__(self):
        return Quad(-self.a, -self.b)
    def __sub__(self, x):
        return self + -self.coerce(x)
    def __rsub__(self, x):
        return self.coerce(x) + -self
    def __mul__(self, x):
        x = self.coerce(x)
        return Quad(self.a*x.a-6*self.b*x.b, self.a*x.b+self.b*x.a)
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = self.coerce(x)
        d = x.a*x.a+6*x.b*x.b
        assert d > 0
        return self*Quad(x.a/d, -x.b/d)
    def __eq__(self, x):
        x = self.coerce(x)
        return self.a == x.a and self.b == x.b
    def out(self):
        return {'rational_real':str(self.a), 'coefficient_i_sqrt6':str(self.b)}


def solve(matrix, rhs):
    """Exact Gauss-Jordan elimination; verify original system afterward."""
    n = len(rhs)
    augmented = [[Quad.coerce(v) for v in row]+[Quad.coerce(z)]
                 for row,z in zip(matrix,rhs)]
    for j in range(n):
        pivot = next(k for k in range(j,n) if augmented[k][j] != 0)
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        den = augmented[j][j]
        augmented[j] = [v/den for v in augmented[j]]
        for k in range(n):
            if k != j:
                multiplier = augmented[k][j]
                augmented[k] = [v-multiplier*w for v,w in zip(augmented[k],augmented[j])]
    answer = [row[-1] for row in augmented]
    assert all(sum((v*w for v,w in zip(row,answer)),Quad()) == z
               for row,z in zip(matrix,rhs))
    return answer


def closure(edges):
    rel = set(map(tuple, edges))
    while True:
        extra = {(i,l) for i,j in rel for k,l in rel if j == k}
        if extra <= rel:
            return rel
        rel |= extra


def laplacian(rel, coefficients):
    L = [[0]*6 for _ in range(6)]
    for i,j in rel:
        size = sum((i,k) in rel and (k,j) in rel for k in range(6))
        b = coefficients[size]
        L[i][i] += b
        L[j][j] += b
        L[i][j] -= b
        L[j][i] -= b
    return L


def gaussian_polynomial_moment(poly):
    """E[p(x,y)] for iid centered Gaussians with variance 1/2."""
    total = F(0)
    for (a,b),c in poly.items():
        if a % 2 or b % 2:
            continue
        total += c*F(factorial(a),4**(a//2)*factorial(a//2))*F(factorial(b),4**(b//2)*factorial(b//2))
    return total


def mulpoly(a,b):
    out = {}
    for (i,j),c in a.items():
        for (k,l),d in b.items():
            out[i+k,j+l] = out.get((i+k,j+l),F(0))+c*d
    return out


def main():
    checks = {}
    def check(name, value):
        checks[name] = bool(value)
        assert checks[name], name
    pilot_path = ROOT/'sources/pilot.json'
    amps_path = ROOT/'sources/result_64.json'
    check('original_contract_hash', hashlib.sha256(pilot_path.read_bytes()).hexdigest() ==
          '442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3')
    check('inherited_amplitude_hash', hashlib.sha256(amps_path.read_bytes()).hexdigest() ==
          '5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae')
    pilot = json.loads(pilot_path.read_text())
    amps = json.loads(amps_path.read_text())
    rcontract = json.loads((ROOT/'contracts/r_records.json').read_text())
    dowker = json.loads((ROOT/'checks/r_records_results.json').read_text())
    root_audit = json.loads((ROOT/'checks/root_exact_audit.json').read_text())
    root_R_audit = json.loads((ROOT/'checks/root_R_audit.json').read_text())
    informatik = json.loads((ROOT/'checks/interference_results.json').read_text())
    extended = json.loads((ROOT/'checks/extended_R_results.json').read_text())
    h = pilot['history_family']
    ell = [0,0,0,0,1,1]
    boundary = [0,1,2,4,5]
    history_checks = []
    class_variances = {}
    boundary_orders = set()
    for cls in (1,2):
        rep = closure(h['common_generating_relations']+h[f'class_{cls}_added_relations'])
        orbit = set()
        for a,r in product([(1,2),(2,1)],[(4,5),(5,4)]):
            perm = (0,*a,3,*r)
            orbit.add(tuple(sorted((perm[i],perm[j]) for i,j in rep)))
        check(f'class{cls}_orbit_size',len(orbit)==h['class_orbit_sizes'][cls-1])
        for index,relations in enumerate(sorted(orbit)):
            rel = set(relations)
            L = laplacian(rel,pilot['action']['interval_coefficients'])
            # H=-beta*L/2 and beta=2sqrt(6)/3, hence Q=D+i sqrt(6)*L/3.
            Q = [[Quad(int(i==j and i!=3), F(L[i][j],3)) for j in range(6)] for i in range(6)]
            answer = solve(Q,ell)
            variance = answer[4]+answer[5]
            if cls in class_variances:
                check(f'class{cls}_orbit{index}_moment_covariance',variance==class_variances[cls])
            else:
                class_variances[cls] = variance
            QB = [[Q[i][j] for j in boundary] for i in boundary]
            cross = [Q[i][3] for i in boundary]
            inner_solve = solve(QB,cross)
            zeta = Q[3][3]-sum((Q[3][i]*v for i,v in zip(boundary,inner_solve)),Quad())
            check(f'class{cls}_orbit{index}_paired_real_damping',zeta.a>0)
            F4 = 6-sum(pilot['action']['interval_coefficients'][sum((i,k) in rel and (k,j) in rel for k in range(6))] for i,j in rel)
            check(f'class{cls}_orbit{index}_gravity_value',F4==h['gravity_values_F4'][cls-1])
            check(f'class{cls}_orbit{index}_terminal_maximal',all(i not in (4,5) for i,j in rel))
            boundary_orders.add(tuple((i,j) for i,j in relations if i!=3 and j!=3))
            history_checks.append({'class':cls,'relations':relations,'variance':variance.out(),
                                   'boundary_paired_inner_coefficient':zeta.out(),
                                   'F4':F4,'H33_over_beta':str(F(-L[3][3],2))})
    check('all_boundary_orders_equal',len(boundary_orders)==1)
    check('class_moment_factors_distinct',class_variances[1]!=class_variances[2])
    # Independent exact packet moments. P=(x+y)^2-1; f2=P*f0/sqrt2.
    P={(2,0):F(1),(1,1):F(2),(0,2):F(1),(0,0):F(-1)}
    W={(0,0):F(1)}
    for _ in range(4):
        W=mulpoly(W,{(0,0):F(1),(2,0):F(1),(0,2):F(1)})
    v0=gaussian_polynomial_moment(W)
    v2=gaussian_polynomial_moment(mulpoly(mulpoly(P,P),W))/2
    # <f0,f2>_V = cross_numerator/sqrt2.
    cross_numerator=gaussian_polynomial_moment(mulpoly(P,W))
    check('f0_f2_orthogonal',gaussian_polynomial_moment(P)==0)
    check('f2_unit_kinematic_norm',gaussian_polynomial_moment(mulpoly(P,P))/2==1)
    check('f2_terminal_swap_invariant',{(j,i):v for (i,j),v in P.items()}==P)
    check('f2_global_scalar_parity_even',all((i+j)%2==0 for i,j in P))
    check('weighted_f0_norm',v0==65)
    check('weighted_f2_norm',v2==799)
    check('weighted_cross',cross_numerator==196)
    check('weighted_gram_positive',v0*v2-cross_numerator**2/2>0)
    # Compare exact Dowker output, not its interval displays.
    # eta=(variance-1)/sqrt2 = sqrt2*(a-1)/2+i sqrt3*b.
    expected_eta = {1:(F(-64430531,771663506),F(-8175324,385831753)),
                    2:(F(-539495737,10449188518),F(-47339214,5224594259))}
    eta_output = {}
    for cls,z in class_variances.items():
        coefficients=((z.a-1)/2,z.b)
        check(f'class{cls}_independent_exact_eta_agreement',coefficients==expected_eta[cls])
        for component,coefficient,radicand in [('real',coefficients[0],2),('imag',coefficients[1],3)]:
            lo,hi=map(F,dowker['eta_by_class'][str(cls)][component])
            check(f'class{cls}_{component}_eta_interval_certified_by_exact_squares',
                  coefficient<0 and lo<hi<0 and hi*hi<=radicand*coefficient*coefficient<=lo*lo)
        eta_output[str(cls)]={'coefficient_sqrt2_real':str(coefficients[0]),
                              'coefficient_i_sqrt3':str(coefficients[1])}
    check('new_gain_frozen_1_over_1024',rcontract['gain']=='1/1024')
    check('old_gain_unchanged_1_over_256',pilot['records']['gain']=='1/256')
    vin=F(2257,16)
    old_bound=4*F(3,5)**2*vin*v0/256**2
    new_separate=4*F(3,5)**2*vin*(v0+v2)/1024**2
    new_direct=2*new_separate
    check('old_bound_exact',old_bound==F(264069,1310720))
    check('direct_old_f0_full_E_contraction',2*old_bound<1)
    check('new_two_packet_direct_full_E_contraction',new_direct<1)
    check('new_two_packet_bound_agrees_dowker',new_direct==F(dowker['direct_coherent_class_sum_effect_norm_upper_exact']))
    check('cannot_reuse_old_majorant_for_two_packets',new_separate*16>1)
    check('positive_stratum_input_minor_excludes_zero',amps['analysis']['positive_rows_amplitude_minor_excludes_zero'])
    check('two_terminal_rows_full_rank_conditional',dowker['positive_stratum_R_amplitude_minor_excludes_zero'])
    check('root_exact_interval_audit_passed',root_audit['all_checks_pass'])
    check('root_two_R_interval_audit_passed',root_R_audit['all_checks_pass'])
    check('two_R_preparation_contrast_positive',F(root_R_audit['delta_R2_gplus_minus_g0'][0])>0)
    check('informatik_interval_run_passed',informatik['status']=='INTERVAL_PROPAGATION_PASS_FROM_INHERITED_ENCLOSURES')
    check('informatik_extended_R_run_passed',extended['status']=='PASS_INHERITED_INTERVALS_WITH_ANALYTIC_GAUSSIAN_EXTENSION')
    phase_interaction=list(map(F,root_R_audit['source_contrast_kappa1_minus_kappa0']))
    peer_phase_interaction=list(map(F,extended['gravity_phase_contrasts']['1']['source_contrast_kappa1_minus_source_contrast_kappa0']))
    check('exact_Taylor_phase_source_interaction_negative',phase_interaction[1]<0)
    check('independent_phase_source_intervals_overlap',max(phase_interaction[0],peer_phase_interaction[0])<=min(phase_interaction[1],peer_phase_interaction[1]))
    check('dephased_terminal_source_contrast_already_nonzero',
          F(extended['cases']['1']['gamma_cases']['0']['source_difference_gplus_minus_g0_f2_given_success'][0])>0)
    check('no_new_clock_integrals',informatik['new_integrals_evaluated']==0 and dowker['new_clock_integrations']==0)
    # Separate exact algebraic identities from interval consistency checks.
    # Existing exact rational cross enclosures establish distinct gamma responses.
    for i in range(2):
        cross_bounds=list(map(F,root_audit['results'][i]['cross']['real']))
        check(f'input{i}_gamma_nonidentifiability_response_witness',cross_bounds[1]<0)
        ours=root_audit['results'][i]['plus_given_success']
        theirs=informatik['cases']['1']['completed_plus_minus']['1']['inputs'][i]['plus_conditional_on_success']
        check(f'input{i}_independent_interval_results_overlap',max(F(ours[0]),F(theirs[0]))<=min(F(ours[1]),F(theirs[1])))
        rr=root_R_audit['results'][i]['coherent']['R2_given_success']
        ee=extended['cases']['1']['gamma_cases']['1']['inputs'][i]['R_conditional_on_success'][1]
        check(f'input{i}_two_R_independent_interval_results_overlap',max(F(rr[0]),F(ee[0]))<=min(F(rr[1]),F(ee[1])))
        dephased=extended['gravity_phase_contrasts']['0']['phase_contrast_by_input'][i]['kappa1_minus_kappa0_f2_given_success']
        check(f'input{i}_gamma0_phase_blind_interval_consistency',F(dephased[0])<=0<=F(dephased[1]))
        for row in amps['analysis']['amplitudes'][i]:
            check(f'input{i}_source_box_order_{len(checks)}',all(F(row[c][0])<=F(row[c][1]) for c in ('real','imag')))
    result={
      'id':'HILBERT-INDEPENDENT-BOUNDARY-COHERENCE-AUDIT-0.1',
      'status':'PASS_CONDITIONAL_FINITE_INSTRUMENT; PHYSICAL_COHERENCE_AND_GEOMETRY_HOLD',
      'checks':checks,'all_checks_pass':all(checks.values()),
      'independence':'History closures/Hessians/Schur damping and terminal moments rebuilt from pilot.json using rational arithmetic in Q(i sqrt6), independently of Dowker symbolic matrices. Inherited amplitude boxes are not reintegrated.',
      'class_variance_ell_Qinverse_ell':{str(k):v.out() for k,v in class_variances.items()},
      'eta_exact':eta_output,
      'moment_relation':'a_f2(c,s;g)=((ell^T Q_c^-1 ell-1)/sqrt2)*a_f0(c,s;g); ell=(0,0,0,0,1,1)',
      'branch_and_factor_audit':{
        'gaussian_source_identity':'Z(J)=Z(0)*exp(J^2 ell^T Q^-1 ell/2); apply (d_J^2-1)/sqrt2 at J=0.',
        'branch':'No new square-root determinant choice. The polynomial insertion multiplies the inherited Abel-limit Gaussian; all six boundary-first Schur coefficients have strictly positive rational real part.',
        'clock_factors':'f2 changes scalar q4,q5 only. Terminal density atoms and constant clock packets stay fixed, scalar action is clock independent, and there is no scalar-dust coupling; all old clock/density/quotient/history-weight factors survive unchanged.',
        'domain':'Polynomial times Gaussian is Schwartz and has finite inherited weighted norm. All adjoint products and failures here act only on E.'},
      'norms':{'kinematic_Gram':'I_2','weighted_Gram':'[[65,98sqrt2],[98sqrt2,799]]',
               'new_gain':'1/1024','new_separate_bound':str(new_separate),
               'new_direct_bound':str(new_direct),'new_failure_effect_lower':str(1-new_direct),
               'old_gain_two_packet_majorant':str(new_separate*16),
               'old_majorant_warning':'A bound above one does not prove the actual old-gain map fails to contract; it only invalidates transfer of this analytic guarantee.'},
      'two_R_probability_audit':{'source':'checks/root_R_audit.json',
                               'eta_interval_validation':'Both real and imaginary interval endpoints independently certified by exact rational squaring against the derived radical coefficients.',
                               'coherent_R2_given_success':[x['coherent']['R2_given_success'] for x in root_R_audit['results']],
                               'gplus_minus_g0':root_R_audit['delta_R2_gplus_minus_g0'],
                               'source_contrast_kappa1_minus_kappa0':root_R_audit['source_contrast_kappa1_minus_kappa0'],
                               'phase_control_audit':'Independent exact rational Taylor sin/cos with valid real Lagrange remainder through degree160/161 agrees with interval transcendental propagation. Counterfactual action ablation, not a physical control.',
                               'nonzero_source_alone_not_interference_witness':'The dephased two-terminal-record instrument already has a nonzero source contrast. Separate gamma and gravity-phase controls identify the conditional interference dependence.',
                               'scope':'Conditional terminal matter-mode probabilities, not geometric observables.'},
      'full_E_completion':'For any normalized g in E, each row is bounded by (3/5)*||g||_V*||f_r||_V. Summing four class/stratum rows per terminal packet and using |a+b|^2<=2(|a|^2+|b|^2) gives Q_direct<=new_direct_bound I_E. The new failure sqrt(I_E-Q_direct) therefore exists with a separate flag for every input and makes the CP instrument trace preserving.',
      'gamma_nonidentifiability':'In the premeasurement class register choose normalized environment markers with arbitrary overlap gamma_s. Measuring the class gives the same old diagonal CP instrument for every overlap, while the coherent analyzer has the cross term gamma_s*a1s*a2s*. Negative certified real cross sums witness differing predictions for gamma=0 and gamma=1. Thus old data cannot select physical gamma or its phase reference.',
      'rank_scope':{
        'old_terminal':'The fixed f0 projector has rank one in the terminal scalar space. It gives one tested terminal matrix element, not an arbitrary R distribution.',
        'not_global_rank_one':'The old map into class/stratum flags already has rank two on E; terminal-projector rank must not be confused with full instrument rank.',
        'extension':'The quadratic scalar action supplies new information beyond the old f0 matrix: eta1!=eta2 and the certified positive-stratum minor imply rank two for the new coherent f0/f2 map on E.',
        'no_general_impossibility':'The one-packet obstruction restricts recovery from the old fixed-f matrix alone, not all expanded theories or all possible future terminal observables.'},
      'independent_ledger':[
        {'item':'Classical versus coherent sum, gamma and phase transport','decision':'PASS','qualification':'Explicit new instrument assumption; old classical forgetting cannot generate interference.'},
        {'item':'Inherited interval propagation and complete finite instruments','decision':'PASS_CONDITIONAL','qualification':'Depends on inherited source enclosures; exact identity proofs are separate from interval overlap checks.'},
        {'item':'Two normalized invariant even terminal packets and exact moments','decision':'PASS','qualification':'Scalar matter-mode records only; no new clock quadrature.'},
        {'item':'New gain and new Failure on all E','decision':'PASS','qualification':'lambda_R=1/1024; direct coherent sum bound 0.3347479248046875.'},
        {'item':'Physical gamma, relative detector phase and history measure','decision':'HOLD','qualification':'Not identified by the six-history classical instrument or equality of induced boundaries.'},
        {'item':'Geometric R observable / gravitational backreaction','decision':'HOLD','qualification':'Both histories induce the same R antichain; scalar Hermite labels do not supply mass, radius, curvature or physical clock calibration.'}],
      'stop_criteria':['Do not enlarge phase or packet searches to fit an effect while physical coherence and detector meaning remain unspecified.',
                       'Do not transfer the old failure after direct coherent summation or terminal-packet extension.',
                       'Do not infer a physical history scalar product, gravitational backreaction or arbitrary R distribution from this finite kinematic construction.'],
      'history_checks':history_checks,
      'new_clock_integrals':0}
    target=ROOT/'checks/hilbert_audit.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'all_checks_pass':result['all_checks_pass'],
                      'eta':eta_output,'new_direct_bound':str(new_direct)},indent=2))


if __name__=='__main__':
    main()
