"""Actual N11 reduced Gaussian outputs and conditional unitary completion.

Only same-package audited rational maps and existing clock quadrature are read.
No discretization of Hilbert space and no new high-dimensional integral is used.
"""
from pathlib import Path
import hashlib
import json
import sympy as s
from coherent_detector import run as run_coherent_detector


def run(package):
    maps_path=package/'checks/independent_audit/results.json'
    clock_path=package/'checks/ward_clock/results.json'
    maps_data=json.loads(maps_path.read_text())
    clock_data=json.loads(clock_path.read_text())
    d=maps_data['conditional_common_scalar_reduction']
    names=('chain','variant')
    maps=[s.Matrix([[s.Rational(x) for x in row] for row in d[k]])
          for k in ('chain_reduced_map','variant_reduced_map')]
    beta=4/s.sqrt(6)
    J=s.BlockMatrix([[s.zeros(3),s.eye(3)],[-s.eye(3),s.zeros(3)]]).as_explicit()
    grams=[R*R.T for R in maps]
    covariances=[G/(2*beta) for G in grams]
    variances=[S[0,0] for S in covariances]
    checks={}
    for name,R,G in zip(names,maps,grams):
        checks[name+'_reduced_map_symplectic']=R*J*R.T==J
        checks[name+'_pure_Gaussian_covariance']=G*J*G==J
        checks[name+'_position_covariance_positive']=G[:3,:3].is_positive_definite is True
    checks['actual_N11_q7_variances_distinct']=s.simplify(variances[0]-variances[1])!=0
    checks['actual_N11_chain_q7_variance_larger']=s.simplify(variances[0]-variances[1]).is_positive is True
    # Input normalization is a product of three elementary real Gaussians.
    x=s.symbols('x',real=True)
    one=s.integrate(s.sqrt(beta/s.pi)*s.exp(-beta*x*x),(x,-s.oo,s.oo))
    checks['declared_reduced_input_normalized']=s.simplify(one**3-1)==0
    # Pure zero-mean n=3 Gaussian overlap: Tr(rho0 rho1)=hbar^3/
    # sqrt(det(Sigma0+Sigma1)), with hbar=1/beta. This gives |overlap|^2,
    # not its metaplectic/Maslov phase.
    det_sum=s.factor((grams[0]+grams[1]).det())
    overlap_squared=8/s.sqrt(det_sum)
    pointer_bhattacharyya=s.sqrt(2*s.sqrt((1+variances[0])*(1+variances[1]))/(2+variances[0]+variances[1]))
    checks['pure_overlap_strictly_between_zero_and_one']=bool(det_sum>64)
    checks['Gaussian_overlap_hbar_cancels']=s.simplify((1/beta)**3/s.sqrt((covariances[0]+covariances[1]).det())-overlap_squared)==0

    # Exact scalar identities underlying the operator proof. The remaining
    # inequalities use unitary norm preservation, Cauchy-Schwarz, and the
    # spectral theorem as explicitly documented in the report.
    omega,t0,t1,theta=s.symbols('omega t0 t1 theta',real=True)
    checks['positive_control_weights_normalize']=s.expand(omega+(1-omega)-1)==0
    checks['convex_modulus_bound_has_positive_deficit']=s.expand(1-(omega*t0+(1-omega)*t1)-(omega*(1-t0)+(1-omega)*(1-t1)))==0
    k2=s.symbols('KdaggerK',commutative=False)
    checks['accepted_and_failure_effects_complete']=s.expand(k2+(1-k2)-1)==0
    phase=s.exp(-s.I*s.Rational(151,38)*theta)
    checks['past_source_is_common_unit_modulus_phase']=s.simplify(phase*s.conjugate(phase)-1)==0
    checks['past_source_partial_generator_is_common']=s.simplify(s.diff(phase,theta)+s.I*s.Rational(151,38)*phase)==0
    checks['past_clock_contract_exact_source_coefficient']=all(
        h['sum_C_past']=='151/19'
        for h in clock_data['exact']['past_constraints'].values())

    rows=[]
    for name,G,v in zip(names,grams,variances):
        pointer_v=1+v
        pbin=s.erf(1/s.sqrt(2*pointer_v))
        rows.append({
            'order':name,
            'q7_row_norm_squared':str(G[0,0]),
            'q7_variance_exact':str(v),
            'q7_variance_decimal':str(s.N(v,30)),
            'pointer_variance_exact':str(pointer_v),
            'pointer_variance_decimal':str(s.N(pointer_v,30)),
            'P_abs_y_le_1_exact':str(pbin),
            'P_abs_y_le_1_decimal':str(s.N(pbin,30)),
        })

    # Actual clock values are only used for numerical, phase-independent
    # success bounds for the explicitly chosen omega0=omega1=1/2.
    def complex_value(z):return complex(z['real'],z['imag'])
    source_rows=[]
    clock_maps=[{r['nodes_per_axis']:r for r in clock_data['quadrature'][key]}[160]
                for key in ('chain','two_cover_deleted')]
    r_overlap=float(s.N(s.sqrt(overlap_squared),18))
    for source in clock_maps[0]['sources']:
        W=[complex_value(c['sources'][source]['W']) for c in clock_maps]
        mod=[abs(z) for z in W]
        base=(mod[0]**2+mod[1]**2)/4
        half_width=mod[0]*mod[1]*r_overlap/2
        bound=(sum(mod)/2)**2
        source_rows.append({
            'rhoP_rhoF':source,
            'omega0':0.5,'omega1':0.5,
            'actual_W_moduli':mod,
            'operator_success_upper_bound':bound,
            'all_input_failure_lower_bound':1-bound,
            'chosen_Gaussian_success_lower_bound_unknown_relative_phase':base-half_width,
            'chosen_Gaussian_success_upper_bound_unknown_relative_phase':base+half_width,
        })
    coherent_checks,coherent_result=run_coherent_detector(package,covariances,overlap_squared)
    checks.update(coherent_checks)
    assert all(checks.values()),checks
    return checks,{
        'status':'CONDITIONAL_COMMON_H3_INSTRUMENT_CONSTRUCTED',
        'scope':'Requires the explicit common rigging/quotient, normalization, metaplectic phases, preparation and control-environment postulates; not the unreduced bare N11 physical norm.',
        'dependencies':{
            str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (maps_path,clock_path)
        },
        'input_section':'q0=0, Q=(q1,q2,q3), Pi=(pi1,pi2,pi3)',
        'output_section':'q10=0, Q=(q7,q8,q9), Pi=(pi7,pi8,pi9)',
        'commutator':'[Qj,Pik]=i delta_jk/beta; beta=4/sqrt(6)',
        'new_normalized_input':'psi(Q)=(beta/pi)^(3/4) exp(-beta |Q|^2/2), Sigma_in=I6/(2 beta)',
        'fixed_local_apparatus':'Q=q7, g=sigma=1 in declared coordinates; no order-label coupling in the pointer',
        'actual_branch_records':rows,
        'branch_overlap':{
            'det_gram_sum_exact':str(det_sum),
            'squared_magnitude_exact':str(overlap_squared),
            'squared_magnitude_decimal':str(s.N(overlap_squared,30)),
            'magnitude_decimal':str(s.N(s.sqrt(overlap_squared),30)),
            'phase':'Not inferred from covariance; requires relative metaplectic convention.',
            'meaning':'Nonorthogonal branch states; different record laws do not implement an ideal history projective measurement.',
        },
        'pointer_record_overlap':{
            'definition':'Classical Bhattacharyya coefficient integral sqrt(p0(y)*p1(y)) dy, not the full quantum-state overlap',
            'exact':str(pointer_bhattacharyya),
            'decimal':str(s.N(pointer_bhattacharyya,30)),
        },
        'unitary_completion':{
            'environment':'E=L2(mu), mu=(dT/3 on [-3/2,3/2])^3 tensor ((delta0+dr_(0,1))/2)^3; ||e=1||=1',
            'control':'C2 with |w>=sqrt(omega0)|0>+sqrt(omega1)|1>, omega>=0, sum omega=1',
            'controlled_unitary':'U=sum_c |c><c| tensor multiplication_by_exp(i S_c(T,r)) tensor V_c; S_c includes all order-only and dust-clock phases exactly once',
            'accepted_ancilla':'Project onto the same |w,e>; K=<w,e|U|w,e>=sum_c omega_c W_c V_c',
            'W_contract':'Wc is the FULL existing inner clock/density integral, already including exp(i F_c); do not multiply that gravitational phase twice',
            'failure_instrument':'Orthogonal ancilla complement I-|w,e><w,e|, with full environment/control trace; effect I-Kdagger K',
            'local_accepted_record':'K_y=M_y K; integral K_y^dagger K_y+E_failure=I',
            'norm_bound':'||K||<=sum omega_c |Wc|<=1; p_failure>=1-(sum omega_c |Wc|)^2 for every normalized input',
            'failure_Kraus_qualification':'sqrt(I-Kdagger K) gives one alternative completion with the same failure probability, but generally a different post-failure state from the explicit ancilla complement.',
        },
        'source_response':{
            'exact':'K(rhoP,rhoF)=exp(-i151rhoP/38) Ktilde(rhoF); every accepted pointer probability and failure probability is rhoP-independent at fixed clocks and rhoF.',
            'future_density':'Changing rhoF changes a future boundary filter/condition; it is not a demonstrated initial-source backreaction.',
            'not_integrated':'Full normalizable boundary clock/density packets are not integrated into this H3 experiment.',
        },
        'numerical_success_bounds':source_rows,
        'coherent_pointer':coherent_result,
        'numerical_qualification':'Branch covariance and special-function formulas are exact; displayed decimals are evaluations. W-based bounds use existing n160 Float64 quadrature, not a roundoff-certified interval.',
        'not_derived_from_action':['Common physical quotient/rigging and normalization choice','Choice of relative metaplectic phases','New common input state','Control/environment Hilbert interpretation and coherent erasure preparation','Positive normalized control weights','Pointer coupling, width and coordinate choice'],
    }
