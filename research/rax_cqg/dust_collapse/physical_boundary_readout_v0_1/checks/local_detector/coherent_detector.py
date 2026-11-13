"""Low-dimensional coherent q7 records using fixed N11 metaplectic phases."""
import hashlib
import json
from pathlib import Path
import mpmath as mp
import sympy as s


def run(package,covariances,expected_overlap_squared):
    mp.mp.dps=70
    state_path=package/'checks/canonical_scalar/gaussian_outputs.json'
    clock_path=package/'checks/ward_clock/results.json'
    state=json.loads(state_path.read_text())
    clock=json.loads(clock_path.read_text())
    def mc(z):return mp.mpc(z['re'],z['im'])
    def ms(z):return mp.mpc(str(s.re(z).evalf(80)),str(s.im(z).evalf(80)))
    def cm(z):return {'real':mp.nstr(mp.re(z),40),'imag':mp.nstr(mp.im(z),40)}
    def number(z):return mp.nstr(z,35)
    def exact_matrix(raw):return s.Matrix([[s.sympify(z) for z in row] for row in raw])
    def numeric(M):return mp.matrix([[ms(z) for z in row] for row in M.tolist()])
    def positive_real_gaussian_root(M):
        # Successive one-dimensional Gaussian eliminations. Each Schur pivot
        # remains in the right half plane. sqrt(pivot) is continued from its
        # positive real Gaussian, so their product retains the determinant's
        # winding information (unlike a single principal sqrt(det(M))).
        A=mp.matrix(M);root=mp.mpc(1)
        for i in range(A.rows):
            pivot=A[i,i]
            assert mp.re(pivot)>0
            root*=mp.sqrt(pivot)
            for j in range(i+1,A.rows):
                for k in range(i+1,A.rows):
                    A[j,k]-=A[j,i]*A[i,k]/pivot
        return root

    beta=4/s.sqrt(6)
    precision=[beta*exact_matrix(b['Omega_scaled_exact']) for b in state['branches']]
    N=[mc(b['N']) for b in state['branches']]
    checks={}
    for c,P in enumerate(precision):
        realP=P.applyfunc(s.re)
        checks[f'coherent_C{c}_precision_real_part_positive']=realP.is_positive_definite is True
        checks[f'coherent_C{c}_precision_matches_q_covariance']=(realP.inv()/2-covariances[c][:3,:3]).applyfunc(s.simplify)==s.zeros(3)
        norm=abs(N[c])**2*mp.pi**mp.mpf('1.5')/mp.sqrt(mp.det(numeric(realP)))
        checks[f'coherent_C{c}_fixed_phase_state_normalized_numeric']=abs(norm-1)<mp.mpf('1e-48')
    T=precision[0].conjugate()+precision[1]
    Tnumeric=numeric(T)
    z=mp.conj(N[0])*N[1]*(2*mp.pi)**mp.mpf('1.5')/positive_real_gaussian_root(Tnumeric)
    u=1+ms(T.inv()[0,0])
    checks['coherent_overlap_independent_root_continuation_agrees']=abs(z-mc(state['overlap_z_equals_integral_conj_psi0_psi1']))<mp.mpf('1e-48')
    checks['coherent_overlap_matches_pure_covariance_magnitude']=abs(abs(z)**2-ms(expected_overlap_squared))<mp.mpf('1e-48')
    checks['coherent_cross_covariance_independent_exact_reconstruction']=abs(u-mc(state['detector_cross_u_g1_sigma1']))<mp.mpf('1e-48')
    checks['coherent_cross_covariance_in_right_half_plane']=mp.re(u)>1
    cross_bin=z*mp.erf(1/mp.sqrt(2*u))
    D=lambda y:z*mp.exp(-y*y/(2*u))/mp.sqrt(2*mp.pi*u)
    # A one-dimensional detector integral only, no new history/clock integral.
    checks['coherent_record_bin_direct_1D_Gaussian_check']=abs(mp.quad(D,[-1,0,1])-cross_bin)<mp.mpf('1e-48')
    checks['coherent_record_total_direct_1D_Gaussian_check']=abs(2*mp.quad(D,[0,1,mp.inf])-z)<mp.mpf('1e-48')
    checks['coherent_record_second_moment_direct_1D_Gaussian_check']=abs(2*mp.quad(lambda y:y*y*D(y),[0,1,mp.inf])-z*u)<mp.mpf('1e-48')

    record_variances=[1+ms(S[0,0]).real for S in covariances]
    branch_bins=[mp.erf(1/mp.sqrt(2*v)) for v in record_variances]
    quadrature={}
    for n in (128,160):
        source_maps=[next(row['sources'] for row in clock['quadrature'][name] if row['nodes_per_axis']==n)
                     for name in ('chain','two_cover_deleted')]
        source_rows=[]
        for source in source_maps[0]:
            a=[mp.mpc(str(d[source]['W']['real']),str(d[source]['W']['imag']))/2 for d in source_maps]
            diag=[abs(x)**2 for x in a]; cross=mp.conj(a[0])*a[1]
            success=sum(diag)+2*mp.re(cross*z)
            var_num=sum(d*v for d,v in zip(diag,record_variances))+2*mp.re(cross*z*u)
            bin_num=sum(d*p for d,p in zip(diag,branch_bins))+2*mp.re(cross*cross_bin)
            var=var_num/success; binprob=bin_num/success
            assert 0<success<1 and var>0 and 0<binprob<1
            source_rows.append({
                'rhoP_rhoF':source,
                'success_probability':number(success),
                'failure_probability':number(1-success),
                'accepted_pointer_mean':'0 (exact even parity)',
                'accepted_pointer_variance':number(var),
                'accepted_P_abs_y_le_1':number(binprob),
                'joint_accepted_abs_y_le_1':number(bin_num),
                'coherent_success_interference':number(2*mp.re(cross*z)),
            })
        quadrature[str(n)]=source_rows
    fields=('success_probability','failure_probability','accepted_pointer_variance','accepted_P_abs_y_le_1','joint_accepted_abs_y_le_1')
    spread=max(abs(mp.mpf(a[f])-mp.mpf(b[f])) for a,b in zip(quadrature['128'],quadrature['160']) for f in fields)
    source_residual=max(abs(mp.mpf(quadrature['160'][j][f])-mp.mpf(quadrature['160'][j+2][f])) for j in (0,1) for f in fields)
    checks['coherent_clock_128_160_agreement_empirical']=spread<mp.mpf('1e-12')
    checks['coherent_past_source_cancels_in_numeric_records']=source_residual<mp.mpf('1e-12')
    assert all(checks.values()),checks
    return checks,{
        'status':'CONDITIONAL_PHASE_FIXED_COHERENT_N11_POINTER_COMPUTED',
        'dependencies':{str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (state_path,clock_path)},
        'phase_convention':state['phase_convention'],
        'root_rule':'Successive complex Gaussian Schur pivots, each with positive real part; square root continued from positive real Gaussian. Independently checked against canonical-scalar whitening continuation.',
        'omega0':'1/2','omega1':'1/2','g':'1','sigma':'1','bin':'|y|<=1',
        'overlap_z_equals_inner_psi0_psi1':cm(z),
        'cross_variance_u':cm(u),
        'cross_bin_integral':cm(cross_bin),
        'formula':{
            'T':'P0.conjugate()+P1',
            'u':'sigma^2+g^2*(T^-1)[0,0]',
            'cross_record_density':'D01(y)=z*exp(-y^2/(2u))/sqrt(2*pi*u)',
            'amplitudes':'a_c=omega_c*W_c; W contains the gravitational phase exactly once',
            'success':'Z=|a0|^2+|a1|^2+2 Re(conj(a0)*a1*z)',
            'conditional_variance':'[sum_c |ac|^2*(sigma^2+g^2*vc)+2 Re(conj(a0)*a1*z*u)]/Z',
            'conditional_bin':'[sum_c |ac|^2*erf(1/sqrt(2*(sigma^2+g^2*vc)))+2 Re(conj(a0)*a1*z*erf(1/sqrt(2*u)))]/Z',
        },
        'quadrature':quadrature,
        'max_128_160_spread':number(spread),
        'max_past_source_record_residual':number(source_residual),
        'scope':'These are actual coherent accepted scalar records for the explicitly added common H3, input, phase, control/environment and local-pointer contract. They are not fundamental history probabilities.',
        'source_qualification':'Fixed-clock rhoP dependence is exactly a common phase; rhoF dependence changes a future boundary filter. Full physical clock/density boundary packets remain unintegrated.',
        'precision_qualification':'Exact rational/scalar formulas and phase-followed high-precision Gaussian evaluation; final probabilities inherit existing Float64 W quadrature without a certified roundoff interval.',
    }
