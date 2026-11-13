#!/usr/bin/env python3
"""Exact finite conditional readout checks, not a physical CST quantization.
The amplitudes in examples are explicit algebraic fixtures, not N11 solver data.
Actual N11 input is a_c=omega_c*W_c*g_c, with gravity already included in W_c.
"""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
I=s.I
checks=[]
def zero(x):
    if isinstance(x,s.MatrixBase):
        assert all(s.simplify(v)==0 for v in x), x
    else: assert s.simplify(s.expand(x))==0, x

def psd2(M):
    zero(M-M.H)
    return all(s.simplify(v).is_nonnegative is True for v in (M[0,0],M[1,1],M.det()))
def serial(x):
    if isinstance(x,s.MatrixBase):return [[str(s.simplify(v)) for v in x.row(i)] for i in range(x.rows)]
    return str(s.simplify(x))
def eta(gamma):return s.Matrix([[1,gamma],[s.conjugate(gamma),1]])
def D(amplitudes,gamma):return s.diag(*amplitudes)*eta(gamma)*s.diag(*amplitudes).H

a0,a1,g=s.symbols('a0 a1 gamma',complex=True)
M=D([a0,a1],g)
zero(M.det()-a0*s.conjugate(a0)*a1*s.conjugate(a1)*(1-g*s.conjugate(g)))
zero(sum(M)-s.trace(M)-M[0,1]-s.conjugate(M[0,1]))
checks.append('symbolic_Gram_congruence_determinant_and_union_sum_rule')

fixtures=[]
gammas=[s.Integer(0),s.Integer(1),s.Integer(-1),I/2,s.Rational(3,5)+4*I/5]
for av in ([1,1],[1,-s.Rational(1,2)],[1,I],[1+I,2-I]):
    av=list(map(s.sympify,av))
    for gamma in gammas:
        E=s.Matrix([[1,s.conjugate(gamma)],[0,s.sqrt(1-gamma*s.conjugate(gamma))]])
        zero(E.H*E-eta(gamma).T)
        mat=D(av,gamma);assert psd2(mat)
        Z=s.simplify(sum(mat)); trace=s.simplify(s.trace(mat))
        vector=E*s.Matrix(av);ports=[s.simplify(x*s.conjugate(x)) for x in vector]
        zero(sum(ports)-Z)
        assert Z.is_nonnegative is True
        for port in ports:assert port.is_nonnegative is True
        if Z>0:
            normalized=mat/Z
            zero(sum(normalized)-1)
        fixtures.append({'amplitudes':serial(s.Matrix([av])), 'gamma':serial(gamma),
                         'rank':mat.rank(),'Z_union':serial(Z),'trace_D':serial(trace),
                         'physical_detector_port_weights':list(map(serial,ports)),
                         'diagonal_history_entries_sum_to_one_after_union_normalization':bool(Z!=0 and s.simplify(trace/Z-1)==0),
                         'conditional_defined':bool(Z!=0)})
checks.append('twenty_exact_fixture_checks_strong_positivity_record_vectors_ports_and_zero_success')

# Positivity alone does not make history diagonal entries probabilities.
mat=D([1,-s.Rational(1,2)],1);Z=sum(mat)
assert Z==s.Rational(1,4)
assert mat[0,0]/Z==4 and mat[1,1]/Z==1
assert sum(mat)==s.Rational(1,4) and s.trace(mat)==s.Rational(5,4)
checks.append('negative_control_naive_history_probabilities_equal_4_and_1')
# Weak two-event consistency need not imply orthogonal records or zero D01.
mat=D([1,I],1)
assert s.re(mat[0,1])==0 and mat[0,1]!=0 and mat.rank()==1
checks.append('weak_additivity_is_weaker_than_decoherent_records')
# Invalid record Gram must fail the positivity test.
bad=D([1,1],s.Rational(3,2));v=s.Matrix([1,-1])
assert (v.H*bad*v)[0]==-1 and not psd2(bad)
checks.append('negative_control_gamma_outside_unit_disk_rejected')

# Explicit abstract two-preparation instrument; this input norm is an assumption.
A=s.Matrix([[1,s.Rational(1,2)],[s.Rational(1,2),I]])
lam=s.Rational(1,4)
# ||A||_F^2=5/2 and ||record synthesis||^2<=2 imply ||M||^2<=5/16.
zero(s.trace(A.H*A)-s.Rational(5,2))
instruments=[]
for gamma in gammas:
    E=s.Matrix([[1,s.conjugate(gamma)],[0,s.sqrt(1-gamma*s.conjugate(gamma))]])
    accepted=lam*E*A
    effect=s.simplify(accepted.H*accepted)
    failure=s.simplify(s.eye(2)-effect)
    assert psd2(effect) and psd2(failure)
    assert psd2(s.Rational(5,16)*s.eye(2)-effect)
    zero(effect+failure-s.eye(2))
    cases=[]
    for psi in [s.Matrix([1,0]),s.Matrix([0,1]),s.Matrix([1,I])/s.sqrt(2)]:
        av=A*psi;mat=D(av,gamma);Z=s.simplify(sum(mat))
        success=s.simplify((psi.H*effect*psi)[0]);fail=s.simplify((psi.H*failure*psi)[0])
        zero(success-lam**2*Z);zero(success+fail-1)
        out=accepted*psi;ports=[s.simplify(x*s.conjugate(x)) for x in out]
        zero(sum(ports)+fail-1)
        # Augment history labels by an orthogonal failure sector. Its norm
        # represents sqrt(failure)*psi, not a new CST geometry history.
        full=s.diag(lam**2*mat,s.Matrix([[fail]]))
        zero(sum(full)-1)
        assert fail>=s.Rational(11,16)
        cases.append({'input':serial(psi),'success':serial(success),'failure':serial(fail),
                      'port_probabilities':list(map(serial,ports)),
                      'full_D_union_normalized':True})
    instruments.append({'gamma':serial(gamma),'success_effect':serial(effect),
                        'failure_effect':serial(failure),'cases':cases})
checks.append('five_CP_instruments_same_amplitude_map_fixed_gain_complete_failure_and_fifteen_normalized_inputs')

# Arbitrary positive relative weights make resolved history fractions arbitrary
# whenever BOTH paired history amplitudes are nonzero.
u,v,p=s.symbols('u v p',positive=True)
w0=s.sqrt(v*(1-p));w1=s.sqrt(u*p)
prob=s.cancel(w1*w1*v/(w0*w0*u+w1*w1*v))
zero(prob-p)
checks.append('resolved_fraction_arbitrary_in_0_1_for_free_positive_relative_weight')

# Original local mixed density integral is a smooth Fourier factor, not delta(C).
C=s.symbols('C',real=True)
J=s.Rational(1,2)+(1-s.exp(-I*C/2))/(I*C)
assert s.limit(J,C,0)==1
zero((C*J).subs(C,2*s.pi)-(s.pi-2*I))
assert s.simplify(J.subs(C,2*s.pi)**2-J.subs(C,2*s.pi))!=0
checks.append('original_density_factor_has_nonzero_CJ_and_is_not_a_projection')

result={
 'id':'N11-CONDITIONAL-PHYSICAL-READOUT-0.1','all_checks_passed':True,
 'checks':checks,'new_N11_clock_or_density_integrations':0,
 'actual_amplitude_convention':'a_c=omega_c*W_c*g_c; W_c already contains exp(iF_c) and complete inner clock/dust integrals. No extra stationary action phase.',
 'fixture_scope':'Exact finite algebra examples only; fixture amplitudes are not presented as computed N11 amplitudes.',
 'record_Gram_convention':'eta_cd=<e_d|e_c>, eta_01=gamma; E^dagger E=eta^T',
 'determinant_formula':'det D=|a0*a1|^2*(1-|gamma|^2)',
 'normalization':'Z=D(Omega,Omega)=sum_cd D_cd, not trace D; condition only if Z>0',
 'coherent_rank_if_both_amplitudes_nonzero':1,
 'resolved_rank_if_both_amplitudes_nonzero':2,
 'fixtures':fixtures,'conditional_abstract_instruments':instruments,
 'external_assumptions':['chosen physical interpretation of input preparation space and norm','specified omega_c history weights','fixed preparation-independent gamma and phase reference','chosen detector ports','fixed gain and orthogonal failure flag'],
 'N11_boundary_data_limit':'Fixed outer T_B and r_B=rho are Dirichlet kernel data, not normalized physical clock/density packets. Scalar Gaussian pairing alone does not supply the missing physical clock/dust pairing.',
 'derived_physical_history_measure':False,'derived_physical_pairing':False,
 'derived_geometry_dynamics':False,
 'scope':'Constructs internally consistent conditional readouts and demonstrates finite-ansatz underdetermination; not a general impossibility theorem.'}
(HERE/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'all_checks_passed':True,'groups':len(checks),'fixtures':len(fixtures),'instrument_cases':sum(len(r['cases']) for r in instruments),'physical_status':'CONDITIONAL_NOT_DERIVED'}))
