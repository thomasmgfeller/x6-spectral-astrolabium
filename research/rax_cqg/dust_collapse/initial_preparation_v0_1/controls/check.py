#!/usr/bin/env python3
"""Finite initial-state controls; exact symplectic algebra and phase-fixed Gaussians."""
from pathlib import Path
import hashlib
import json
import itertools
import math
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parent


def smatrix(rows):
    return s.Matrix([[s.sympify(v) for v in row] for row in rows])


def exact_clock_checks():
    u = s.symbols('u0:11', real=True)
    r = s.symbols('r0:11', real=True)
    rows = []
    coefficients = (1, -9, 16, -8)
    for name, removed in [('C0', set()), ('C1', {(4,5),(5,6)})]:
        rel = {(i,j) for i in range(11) for j in range(i+1,11)} - removed
        b = {(i,j): coefficients[k] if k < 4 else 0 for i,j in rel
             for k in [sum((i,z) in rel and (z,j) in rel for z in range(11))]}
        C = [1+s.Rational(1,19)*sum(v*(u[j]-u[i])**2 for (i,k),v in b.items() if k==j)
             for j in range(11)]
        past = s.expand(sum(C[:4]))
        action = -sum(rj*Cj for rj,Cj in zip(r,C))/2
        cross = s.Matrix([[s.diff(action,u[a],u[b]) for b in range(4)] for a in (4,5,6)])
        assert all(s.diff(past,u[j]) == 0 for j in range(4,11))
        assert past.subs({u[j]:j for j in range(4)}) == s.Rational(151,19)
        assert all(s.simplify(cross[k,j]-r[k+4]*b.get((j,k+4),0)/19)==0 for k in range(3) for j in range(4))
        assert cross[:,3] != s.zeros(3,1)
        rows.append({'history':name,'Bpast_scaled_clock_polynomial':str(past),
                     'inner_past_clock_cross_Hessian_scaled':[[str(v) for v in row] for row in cross.tolist()],
                     'unweighted_cross_coefficients':[[b.get((j,k),0) for j in range(4)] for k in (4,5,6)],
                     'cross_rank_at_positive_equal_density':cross.subs({rr:1 for rr in r}).rank(),
                     'fixed_clock_rhoP_only_common_phase':True})
    assert rows[0]['Bpast_scaled_clock_polynomial']==rows[1]['Bpast_scaled_clock_polynomial']
    return {'exact_pass':True,'clock_convention':'Tj=Delta*(uj-5), beta*Delta^2=2/19',
            'histories':rows,'general_factorization':'Wc(rhoP,uP)=exp(-i*rhoP*Bpast(uP)/2)*Wtilde_c(uP)',
            'rhoP_fixed_clock_record_derivative':'exactly zero for fixed input, instrument and future data',
            'clock_variation':'T3 couples directly to all three inner clocks in both orders; nonzero coupling does not alone prove a nonzero measured response.'}


def compute(dps):
    mp.mp.dps=dps
    canonical=json.loads((ROOT/'sources/canonical_results.json').read_text())
    gaussians=json.loads((ROOT/'sources/gaussian_outputs.json').read_text())
    clocks=json.loads((ROOT/'sources/clock_results.json').read_text())
    contract=json.loads((ROOT/'contract.json').read_text())
    maps=[smatrix(canonical['common_reduction'][k]) for k in ('R0','R1')]
    J=s.zeros(6);J[:3,3:]=s.eye(3);J[3:,:3]=-s.eye(3)
    for R in maps:
        assert R.T*J*R==J
    beta=4/mp.sqrt(6)
    def mscalar(v):
        return mp.mpc(str(s.re(v).evalf(dps+8)),str(s.im(v).evalf(dps+8)))
    def mmat(A):return mp.matrix([[mscalar(v) for v in row] for row in A.tolist()])
    def mz(raw):return mp.mpc(raw['re'],raw['im'])
    def cpack(z):return {'real':mp.nstr(mp.re(z),35),'imag':mp.nstr(mp.im(z),35)}
    def num(v):return mp.nstr(mp.re(v),30)
    def root(A):
        A=mp.matrix(A);out=mp.mpc(1)
        for i in range(A.rows):
            pivot=A[i,i];assert mp.re(pivot)>0
            out*=mp.sqrt(pivot)
            for j in range(i+1,A.rows):
                for k in range(i+1,A.cols):A[j,k]-=A[j,i]*A[i,k]/pivot
        return out
    P=[beta*mmat(smatrix(b['Omega_scaled_exact'])) for b in gaussians['branches']]
    NN=[mz(b['N']) for b in gaussians['branches']]
    cov=[mmat(R*R.T)/(2*beta) for R in maps]
    for c in range(2):
        assert abs(abs(NN[c])**2*mp.pi**mp.mpf('1.5')/mp.sqrt(mp.det(P[c].apply(mp.re)))-1)<mp.mpf('1e-45')
    T=P[0].conjugate()+P[1]; Ti=T**-1
    zbase=mp.conj(NN[0])*NN[1]*(2*mp.pi)**mp.mpf('1.5')/root(T)
    assert abs(zbase-mz(gaussians['overlap_z_equals_integral_conj_psi0_psi1']))<mp.mpf('1e-45')
    cross_u=1+Ti[0,0]
    def bins(mean,variance):
        lo=mp.erfc((mean+1)/mp.sqrt(2*variance))/2
        hi=mp.erfc((1-mean)/mp.sqrt(2*variance))/2
        return [lo,1-lo-hi,hi]
    results=[]; exact_means=[]; checks={}
    for displacement in contract['scalar_displacements']:
        d=s.Matrix([s.Rational(v) for v in displacement]+[0,0,0])
        means=[R*d for R in maps];exact_means.append({'input':displacement,'output_phase_space':[[str(v) for v in m] for m in means]})
        centers=[mmat(m[:3,:]) for m in means];momenta=[mmat(m[3:,:]) for m in means]
        ll=[P[c]*centers[c]+1j*beta*momenta[c] for c in range(2)]
        kk=[-(centers[c].T*P[c]*centers[c])[0]/2-1j*beta*(momenta[c].T*centers[c])[0]/2 for c in range(2)]
        ell=ll[0].conjugate()+ll[1]
        z=zbase*mp.exp(mp.conj(kk[0])+kk[1]+(ell.T*Ti*ell)[0]/2)
        mu=(Ti*ell)[0]
        branch_means=[mp.re(m[0]) for m in centers]
        branch_vars=[mp.re(1+v[0,0]) for v in cov]
        branch_bins=[bins(m,v) for m,v in zip(branch_means,branch_vars)]
        cbins=[z*v for v in bins(mu,cross_u)]
        assert abs(sum(cbins)-z)<mp.mpf('1e-45')
        assert abs(z)<=1
        density=lambda y:z*mp.exp(-(y-mu)**2/(2*cross_u))/mp.sqrt(2*mp.pi*cross_u)
        # Independent real-axis integration checks complex continuation and finite-bin sign.
        bin_residual=abs(mp.quad(density,[-1,0,1])-cbins[1])
        assert bin_residual<mp.mpf('1e-45')
        numeric={}
        for n in (128,160):
            cc=[next(row['sources'] for row in clocks['quadrature'][name] if row['nodes_per_axis']==n)
                for name in ('chain','two_cover_deleted')]
            sources=[]
            for source in ('1/8|1/8','1/4|1/8'):
                amplitudes=[mp.mpc(str(c[source]['W']['real']),str(c[source]['W']['imag']))/2 for c in cc]
                diag=[abs(a)**2 for a in amplitudes];cross=mp.conj(amplitudes[0])*amplitudes[1]
                success=sum(diag)+2*mp.re(cross*z)
                joint=[sum(diag[c]*branch_bins[c][j] for c in range(2))+2*mp.re(cross*cbins[j]) for j in range(3)]
                first=sum(diag[c]*branch_means[c] for c in range(2))+2*mp.re(cross*z*mu)
                second=sum(diag[c]*(branch_vars[c]+branch_means[c]**2) for c in range(2))+2*mp.re(cross*z*(cross_u+mu**2))
                assert 0<success<1 and all(v>0 for v in joint)
                assert abs(sum(joint)-success)<mp.mpf('1e-45')
                mean=first/success;variance=second/success-mean*mean
                assert variance>0
                incoherent_success=sum(diag)
                incoherent_joint=[sum(diag[c]*branch_bins[c][j] for c in range(2)) for j in range(3)]
                sources.append({'rhoP_rhoF':source,'success':num(success),'failure':num(1-success),
                    'joint_pointer_bins':[num(v) for v in joint],
                    'conditional_pointer_bins':[num(v/success) for v in joint],
                    'conditional_pointer_mean':num(mean),'conditional_pointer_variance':num(variance),
                    'history_dephased_control':{'success':num(incoherent_success),'failure':num(1-incoherent_success),
                    'joint_pointer_bins':[num(v) for v in incoherent_joint]},
                    'coherent_success_cross_term':num(2*mp.re(cross*z))})
            numeric[str(n)]=sources
        results.append({'displacement':displacement,'overlap':cpack(z),'cross_pointer_mean':cpack(mu),
                        'cross_pointer_variance':cpack(cross_u),'branch_pointer_means':[num(v) for v in branch_means],
                        'branch_pointer_variances':[num(v) for v in branch_vars],
                        'branch_pointer_bins':[[num(v) for v in row] for row in branch_bins],
                        'finite_bin_direct_integral_residual':num(bin_residual),'quadrature':numeric})
    fields=('success','failure','conditional_pointer_mean','conditional_pointer_variance')
    past_residual=max(abs(mp.mpf(row['quadrature']['160'][0][f])-mp.mpf(row['quadrature']['160'][1][f])) for row in results for f in fields)
    quad_residual=max(abs(mp.mpf(row['quadrature']['160'][k][f])-mp.mpf(row['quadrature']['128'][k][f])) for row in results for f in fields for k in (0,1))
    assert past_residual<mp.mpf('1e-12') and quad_residual<mp.mpf('1e-12')
    minus,zero,plus=[r['quadrature']['160'][0] for r in results]
    assert abs(mp.mpf(minus['success'])-mp.mpf(plus['success']))<mp.mpf('1e-25')
    assert abs(mp.mpf(minus['conditional_pointer_mean'])+mp.mpf(plus['conditional_pointer_mean']))<mp.mpf('1e-25')
    assert abs(mp.mpf(plus['conditional_pointer_mean']))>mp.mpf('1e-8')
    assert max(abs(mp.mpf(minus['joint_pointer_bins'][j])-mp.mpf(plus['joint_pointer_bins'][2-j])) for j in range(3))<mp.mpf('1e-25')
    checks={'maps_exactly_symplectic':True,'input_translation_unitary':True,'inherited_phase_preserved_by_Weyl_covariance':True,
            'output_states_normalized':True,'cross_finite_bin_independently_integrated':True,
            'all_full_probabilities_nonnegative_and_complete':True,'parity_tail_swap':True,
            'nonzero_scalar_translation_record_response':True,'fixed_clock_past_density_null_control':True,
            'quadrature_128_160_consistency':True}
    return {'checks':checks,'exact_output_means':exact_means,'scalar_controls':results,
            'max_past_density_control_residual':num(past_residual),'max_parent_quadrature_spread':num(quad_residual),
            'precision_digits':dps}


def main():
    if __debug__ is False:raise SystemExit('Do not disable assertions.')
    contract=json.loads((ROOT/'contract.json').read_text())
    for item in contract['sources']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
    results=compute(70)
    results.update({'status':'PASS_CONDITIONAL_SCALAR_PREPARATION_RESPONSE',
        'contract_sha256':hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest(),
        'clock_diagnostics':exact_clock_checks(),
        'normalization_scope':'Same explicitly conditional common H3 and normalized input translation; fixed local pointer and omega0=omega1=1/2.',
        'quantum_formula':'V_c D(d,0) psi = D(R_c(d,0)) V_c psi; D(q,p) f(y)=exp(i beta p dot (y-q/2))*f(y-q).',
        'cross_formula':'T=conj(P0)+P1, ell=conj(l0)+l1, mu=(T^-1 ell)_0, u=1+(T^-1)_00; D01(y)=z exp(-(y-mu)^2/(2u))/sqrt(2*pi*u)',
        'dephased_control_scope':'History-control off-diagonal coherence suppressed with each success amplitude Wc/2 retained; not the separate initial-clock incoherent mixture.',
        'physical_backreaction_derived':False,'new_clock_integration':False,
        'qualification':'70-digit Gaussian arithmetic inherits parent Float64 clock weights; n128/n160 agreement is empirical, not a roundoff interval certificate.'})
    (ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'status':results['status'],'checks':len(results['checks']),
                      'max_past_residual':results['max_past_density_control_residual'],
                      'max_quadrature_spread':results['max_parent_quadrature_spread'],
                      'records':[{'d':row['displacement'],'rho_fixed':row['quadrature']['160'][0]} for row in results['scalar_controls']]},indent=2))


if __name__=='__main__':main()
