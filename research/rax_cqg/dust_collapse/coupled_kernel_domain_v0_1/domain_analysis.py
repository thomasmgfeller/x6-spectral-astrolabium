"""Exact finite-domain certificate; no production simulation or physical CST claim."""
from pathlib import Path
import hashlib
import json
import sys
import sympy as S
from flint import arb, ctx

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'inputs'))
import prior_core as core

B = (0, 1, 3, 4)
beta = 4 / S.sqrt(6)

def schur(code):
    h = S.Matrix(core.h0(code))
    return h.extract(B, B) - h.extract(B, [2]) * h.extract([2], B) / h[2, 2]

def encode(matrix):
    return [[str(v) for v in row] for row in matrix.tolist()]

def build():
    rows = []
    for code in core.histories():
        h = S.Matrix(core.h0(code))
        k = schur(code)
        x = k[:2, 2:]
        rows.append({'code': code, 'F4': core.f4(code), 'inner_h0': str(h[2,2]),
                     'predecessor_count': sum((i,2) in core.relations(code) for i in (0,1)),
                     'schur_over_beta': encode(k), 'cross_rank': x.rank(),
                     'outgoing_null_basis': [encode(v) for v in x.nullspace()],
                     'antisymmetric_free': x*S.Matrix([1,-1]) == S.zeros(2,1)})
    ctx.prec = 192
    b = 4 / arb(6).sqrt()
    c0 = (2*arb.pi()/b).sqrt()
    c4 = arb.pi()/6*c0
    p2 = 8*arb.pi()**2/(2*b*(arb(1231)/6*arb(581)/3).sqrt())
    lower = arb(1)/8712/8*(arb(3)/16)**2*2/arb(1).exp()*p2
    return {
        'model': 'unchanged coupled AA control; 33 histories; kappa=1; mass=0',
        'history_count': len(rows), 'rank_histogram': {str(r):sum(v['cross_rank']==r for v in rows) for r in (1,2)},
        'histories': rows,
        'persistent_codes': [v['code'] for v in rows if v['antisymmetric_free']],
        'tube': {'s_range':[-1,1], 'a_range':'[-R,R]', 'outgoing_density':'00',
                 'output_measure_factor':'1/8', 'input_history_prefactor_squared':'1/8712',
                 'frequencies_over_beta':['7/4','17/4'],
                 'decay_coefficients':['51484/59785','1225/1231'],
                 'Dp_real_lower_bound':'3/16',
                 'limit_definition':'lim R->infinity ||1_tube K psi||_H^2 / (2R)',
                 'limit_lower_bound':lower.str(35,more=True),
                 'lower_bound_claim':'greater than 4.5e-8; asymptotic, not a finite-R threshold'},
        'rigging': {'V_weight':'(1+|q|^2)^4', 'dual_weight':'(1+|q|^2)^(-4)',
                    'C0':c0.str(35,more=True), 'operator_bound_V_to_dual':c4.str(35,more=True),
                    'Abel_error_coefficient':(c4*(1+1/(2*b))).str(35,more=True),
                    'ground_input_H_norm_squared':1, 'ground_input_V_norm_squared':65},
        'status': {'coupled_control_H_evolution':'COUNTEREXAMPLE',
                   'coupled_control_V_to_dual':'BOUNDED_WITH_NORM_CONVERGENT_ABEL_LIMIT',
                   'physical_CST_kernel':'NOT_CONSTRUCTED', 'all_eight_physical_gates':'HOLD',
                   'infinite_history_sum':'NOT_DEFINED_OR_EVALUATED'}}

def write_result(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build(),ensure_ascii=False,sort_keys=True,indent=2)+'\n')

if __name__ == '__main__':
    write_result(sys.argv[1] if len(sys.argv)>1 else ROOT/'results/domain_certificate.json')
