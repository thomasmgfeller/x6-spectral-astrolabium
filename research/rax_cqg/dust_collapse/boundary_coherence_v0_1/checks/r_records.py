"""Exact terminal matter-record construction; no new clock quadrature.

The packet and gain are fixed in contracts/r_records.json before evaluation.
Only read the old pilot and artifacts. Write this check's own result file.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import sympy as s
from sympy.polys.matrices import DomainMatrix
from mpmath import iv

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT/'sources'
iv.dps = 80

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def boundary(x, upper=False):
    sign, man, exp, bc = x._mpi_[int(upper)]
    assert bc >= 0
    z = Fraction((-1 if sign else 1)*man)*Fraction(2)**exp
    scale = 10**40
    k = -((-z.numerator*scale)//z.denominator) if upper else z.numerator*scale//z.denominator
    return ('-' if k < 0 else '') + str(abs(k)//scale) + '.' + str(abs(k)%scale).zfill(40)

def enc(z):
    if hasattr(z, '_mpi_'):
        return [boundary(z), boundary(z, True)]
    return {'real': enc(z.real), 'imag': enc(z.imag)}

def algebraic_interval(x):
    """Outward-rounded evaluation of exact real algebraic expressions."""
    x = s.sympify(x)
    if x.is_Rational:
        return iv.mpf(int(x.p))/int(x.q)
    if x.is_Add:
        return sum((algebraic_interval(y) for y in x.args), iv.mpf(0))
    if x.is_Mul:
        z = iv.mpf(1)
        for y in x.args:
            z *= algebraic_interval(y)
        return z
    if x.is_Pow:
        base, exponent = x.args
        if exponent.is_Integer:
            return algebraic_interval(base)**int(exponent)
        if exponent == s.Rational(1, 2):
            return iv.sqrt(algebraic_interval(base))
    raise ValueError(f'unsupported exact expression: {x}')

def complex_interval(z):
    return iv.mpc(algebraic_interval(s.simplify(s.re(z))),
                  algebraic_interval(s.simplify(s.im(z))))

def gaussian_moment(polynomial, x, y):
    """Exact expectation under pi^-1 exp(-x^2-y^2) dx dy."""
    ans = 0
    for (a, b), coeff in s.Poly(s.expand(polynomial), x, y).terms():
        if a % 2 or b % 2:
            continue
        def moment(n):
            return s.factorial(n)/(4**(n//2)*s.factorial(n//2))
        ans += coeff*moment(a)*moment(b)
    return s.simplify(ans)

contract_path = ROOT/'contracts/r_records.json'
contract = json.loads(contract_path.read_text())
PINNED = {
    'pilot.json':'442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3',
    'dowker_history_data.json':'72b42d685400088c19ac58a268333f4c1c281ec6ad54639c49962acb9c0f7210',
    'result_64.json':'5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae',
}
for filename, expected in PINNED.items():
    assert sha(SOURCES/filename) == expected, filename
assert sha(contract_path) == 'd82df374d7aa839c49a8b9acba15835285b99e45cf92a294727d3e3bf8e80e44'
assert sha(SOURCES/'pilot.json') == contract['source_contract_sha256']
assert contract['gain'] == '1/1024'
assert contract['terminal_packets']['f2'] == '[((q4+q5)^2-1)/sqrt(2)] * original R_f'
old = json.loads((SOURCES/'dowker_history_data.json').read_text())
cert = json.loads((SOURCES/'result_64.json').read_text())

x, y = s.symbols('q4 q5', real=True)
P = ((x+y)**2-1)/s.sqrt(2)
assert s.simplify(P.subs({x:y, y:x}, simultaneous=True)-P) == 0
assert s.simplify(P.subs({x:-x, y:-y}, simultaneous=True)-P) == 0
overlap = gaussian_moment(P, x, y)
norm = gaussian_moment(P**2, x, y)
v0 = gaussian_moment((1+x*x+y*y)**4, x, y)
v2 = gaussian_moment(P**2*(1+x*x+y*y)**4, x, y)
v02 = gaussian_moment(P*(1+x*x+y*y)**4, x, y)
assert (overlap, norm, v0, v2, v02) == (0, 1, 65, 799, 98*s.sqrt(2))

beta = 4/s.sqrt(6)
FIELD = s.QQ.algebraic_field(s.I*s.sqrt(6))
ell = s.Matrix([0,0,0,0,1,1])
D = s.diag(1,1,1,0,1,1)
t = s.symbols('t0:6', real=True)
r = s.symbols('r0:6', real=True)
eta = {}
checks = []
for h in old['histories']:
    cls = h['type']
    H0 = s.Matrix([[s.Rational(v) for v in row] for row in h['H0']])
    Q = D-s.I*beta*H0
    inverse = DomainMatrix.from_Matrix(Q).convert_to(FIELD).inv().to_Matrix()
    variance = s.simplify((ell.T*inverse*ell)[0])
    e = s.simplify(s.expand_complex((variance-1)/s.sqrt(2)))
    if cls in eta:
        assert s.simplify(e-eta[cls]) == 0
    else:
        eta[cls] = e
    relations = set(map(tuple, h['relations']))
    assert not any(i in (4,5) and j in (4,5) for i,j in relations)
    # Terminal nodes have no descendants; all their dust dependence carries r4/r5.
    dust = -sum(r)/2-beta*sum(s.Rational(c)*r[j]*(t[j]-t[i])**2
                            for i,j,c in h['coefficient_pairs'])/4
    atom_dust = s.expand(dust.subs({r[4]:0,r[5]:0}))
    assert s.diff(atom_dust, t[4]) == s.diff(atom_dust, t[5]) == 0
    # A source J ell in the Gaussian generates this second moment exactly:
    # Z(J)/Z(0)=exp(J^2 ell^T Q^-1 ell/2), then (d_J^2-1)/sqrt(2).
    checks.append({'class':cls, 'edge_bits':h['edge_bits'],
                   'terminal_order':'two-element antichain',
                   'terminal_clock_derivatives_on_density_atoms':['0','0'],
                   'eta_exact':str(e),
                   'paired_inner_real_damping':h['boundary_paired_inner_real_damping']})

assert len(checks) == 6
assert s.simplify(eta[1]-eta[2]) != 0
eta_iv = {str(c):enc(complex_interval(e)) for c,e in eta.items()}
separate_bound = s.Rational(4)*(s.Rational(3,5))**2*s.Rational(2257,16)*(v0+v2)/1024**2
coherent_bound = 2*separate_bound
old_gain_pair_bound = separate_bound*16
assert coherent_bound < 1 and old_gain_pair_bound > 1

# Old positive-stratum 2x2 amplitude minor has already excluded zero.
minor = cert['analysis']['positive_rows_amplitude_minor']
assert cert['analysis']['positive_rows_amplitude_minor_excludes_zero']
old_minor_iv = iv.mpc(iv.mpf(minor['real']), iv.mpf(minor['imag']))
new_minor_iv = complex_interval(eta[2]-eta[1])*old_minor_iv
assert not (new_minor_iv.real.a <= 0 <= new_minor_iv.real.b and
            new_minor_iv.imag.a <= 0 <= new_minor_iv.imag.b)

result = {
 'id':contract['id'],
 'status':'PASS_TWO_ORTHOGONAL_TERMINAL_MATTER_RECORDS',
 'source_hashes':{str(p.relative_to(ROOT.parent)):sha(p) for p in [
     contract_path, SOURCES/'pilot.json', SOURCES/'dowker_history_data.json',
     SOURCES/'result_64.json']},
 'packet':'f2=[((q4+q5)^2-1)/sqrt(2)]f0',
 'orthonormality':{'f0_norm_squared':'1','f2_norm_squared':str(norm),'inner_product':str(overlap)},
 'terminal_swap_invariant':True, 'global_scalar_parity':'even',
 'weighted_norm_squared':{'f0':str(v0),'f2':str(v2)},
 'weighted_gram_cross':str(v02),
 'eta_definition':'(ell^T Q_C^-1 ell-1)/sqrt(2), ell=(0,0,0,0,1,1)',
 'eta_exact_by_class':{str(c):str(e) for c,e in eta.items()},
 'eta_by_class':eta_iv,
 'eta_independent_of_preparation_and_inner_stratum':True,
 'amplitude_relation':'a_f2(c,s;g)=eta_c*a_f0(c,s;g) for c=1,2; s=atom,positive; g in E',
 'terminal_packet_rank_on_class_response_space':2,
 'class_response_determinant_eta2_minus_eta1':enc(complex_interval(eta[2]-eta[1])),
 'coherent_positive_stratum_input_output_rank':2,
 'positive_stratum_R_amplitude_minor':enc(new_minor_iv),
 'positive_stratum_R_amplitude_minor_excludes_zero':True,
 'minor_identity':'det[[a10+a20, a1plus+a2plus],[eta1*a10+eta2*a20,eta1*a1plus+eta2*a2plus]]=(eta2-eta1)*(a10*a2plus-a1plus*a20), all a at inner positive stratum',
 'atom_stratum_input_output_rank':1,
 'domain_existence':'Polynomial times the original Gaussian is Schwartz; the inherited paired Re(zeta)>0 and Abel/Fresnel branch remain valid. Gaussian differentiation introduces no new clock integral.',
 'gain':contract['gain'],
 'separate_or_unitarily_mixed_classes_effect_norm_upper_exact':str(separate_bound),
 'separate_or_unitarily_mixed_classes_effect_norm_upper_decimal':float(separate_bound),
 'direct_coherent_class_sum_effect_norm_upper_exact':str(coherent_bound),
 'direct_coherent_class_sum_effect_norm_upper_decimal':float(coherent_bound),
 'old_gain_two_packet_majorant':float(old_gain_pair_bound),
 'old_gain_majorant_above_one_is_not_proof_of_actual_noncontraction':True,
 'failure_recomputed_on_E':True,
 'induced_R_geometry_identical_for_all_histories':True,
 'pure_induced_R_order_observables_constant':True,
 'density_record_obstruction':'With original atom packet only the 00 endpoint density sector is probed. Other sectors require new endpoint packets and new dust/clock integrals.',
 'terminal_clock_record_obstruction':'On 00 density support the amplitude is independent of t4,t5; constant-orthogonal clock packets have exactly zero amplitude, and clock bins alone factor identically for every class/preparation.',
 'one_f_matrix_obstruction':'The old matrix gives only <f0,K_C g>. Orthogonal terminal rows are not recoverable from those entries alone. This extension additionally uses the original quadratic scalar action to derive eta_c.',
 'physical_interpretation':'Terminal scalar matter mode projections; neither energy eigenstates of a derived physical Hamiltonian nor radius/curvature measurements.',
 'physical_geometric_eligibility':False,
 'new_clock_integrations':0,
 'history_checks':checks,
 'scope':'Exact finite auxiliary record extension, conditional on the separately declared coherent common-endstate assumption. No source or geometric calibration is supplied.'
}
out = ROOT/'checks/r_records_results.json'
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','eta_exact_by_class','eta_by_class',
  'positive_stratum_R_amplitude_minor','direct_coherent_class_sum_effect_norm_upper_decimal',
  'new_clock_integrations']}, indent=2))
