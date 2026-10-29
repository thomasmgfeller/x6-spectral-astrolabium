"""Produce seven rigorous sufficient budgets and one necessary budget."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
from fractions import Fraction
import flint
from flint import arb, ctx
from variance import (ball, encode, upper_coefficient, local_lower_coefficient,
                      sufficient_density, volume, EPSILON_CAP)

HERE = Path(__file__).resolve().parent


def compute(bits=128):
    ctx.prec = bits
    baseline_path = HERE/'baseline/BUDGET_v0_3.json'
    baseline = json.loads(baseline_path.read_text())
    rows = []
    for prior in baseline['rows']:
        ell, H = Fraction(str(prior['ell_k'])), prior['H']
        K, detail = upper_coefficient(ell)
        rho = sufficient_density(K, ell)
        bias = arb(prior['relative_bias']['real_ball'])
        tail = arb(prior['relative_boundary_bound']['real_ball'])
        total_RMS = ((bias.upper()+tail.upper())**2 + K/rho/arb('1/2')**2).sqrt()
        old_N = arb(prior['expected_N_at_sufficient_density']['real_ball'])
        N = rho*volume(H)
        row = {'ell_k': str(ell), 'H': H, 'upper_coefficient': encode(K),
               'rho_sufficient': str(rho), 'expected_N_sufficient': encode(N),
               'old_expected_N_sufficient': encode(old_N),
               'improvement_factor': encode(old_N/N),
               'relative_total_RMS_upper': encode(total_RMS),
               'single_witness_RMS_at_most_10_percent': bool(total_RMS <= arb('1/10')),
               'relative_bias_baseline': encode(bias),
               'relative_boundary_bound_baseline': encode(tail),
               'witness_10_percent_RMS_excluded_by_bias': prior['witness_RMS_target_impossible_at_chosen_H'],
               'scope': 'one nonoscillating Gaussian witness; no E4 qualification',
               'upper_bound_components': {k:encode(v) for k,v in detail.items()}}
        rows.append(row)
    k, detail = local_lower_coefficient()
    first = baseline['rows'][0]
    bias_lo = (arb(first['relative_bias']['real_ball']).lower()
               -arb(first['relative_boundary_bound']['real_ball']).upper())*arb('1/2')
    total_allowance = arb('1/20')**2-bias_lo**2
    # Use a fixed lower endpoint; an enclosure midpoint is not a lower bound.
    rho_necessary_stochastic = k.lower()/arb('7/200')**2
    rho_necessary_total = k.lower()/total_allowance.upper()
    lower = {'ell_k':'1/8','H':20,'coefficient':encode(k),
             'valid_for':'all rho >= q=4096, epsilon=q/rho <=1',
             'rho_necessary_for_7_percent_stochastic_RMS':encode(rho_necessary_stochastic),
             'expected_N_necessary_for_7_percent_stochastic_RMS':encode(rho_necessary_stochastic*volume(20)),
             'rho_necessary_for_10_percent_total_RMS':encode(rho_necessary_total),
             'expected_N_necessary_for_10_percent_total_RMS':encode(rho_necessary_total*volume(20)),
             'absolute_bias_lower_from_baseline':encode(bias_lo),
             'box':{'x_sqrt_qV':['3','31/10'],'v':['19/10','21/10']},
             'components':{k:encode(v) for k,v in detail.items()},
             'meaning':'necessary only; does not assert feasibility at these densities'}
    return {'schema':'cspp.variance-budget/0.4','date':'2026-10-27',
            'precision_bits':bits,'python':platform.python_version(),
            'python_flint':flint.__version__,'epsilon_cap':str(EPSILON_CAP),
            'baseline':{'repository':'thomasmgfeller/x6-spectral-astrolabium','PR':135,
                        'merge_commit':'3a200404a23d79bde852b29a49f56c809fb68af4',
                        'file':'research/cspp/certified_budget_v0_3/results/BUDGET.json',
                        'snapshot_sha256':hashlib.sha256(baseline_path.read_bytes()).hexdigest()},
            'upper_rows':rows,'lower_witness':lower,
            'gate_status':{'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'},
            'new_poisson_clouds':0,'confirmation_seed_used':False,
            'full_covariance_spatial_integral':'NOT_EVALUATED',
            'exact_pair_kernel':'IMPLEMENTED_AND_TESTED; overlaps supplied as inputs',
            'scope':'fixed Gaussian witness, homogeneous Poisson sampling, exact geometry; numerical arithmetic of F and full E4 pipeline not certified'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bits',type=int,default=128)
    parser.add_argument('--output',default='results/BUDGET.json')
    args=parser.parse_args()
    result=compute(args.bits)
    out=HERE/args.output;out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    row=result['upper_rows'][0];low=result['lower_witness']
    print(json.dumps({'upper_N':row['expected_N_sufficient'],
                      'lower_N_stochastic':low['expected_N_necessary_for_7_percent_stochastic_RMS'],
                      'lower_N_total':low['expected_N_necessary_for_10_percent_total_RMS'],
                      'G1':'HOLD'},indent=2))

if __name__=='__main__':main()
