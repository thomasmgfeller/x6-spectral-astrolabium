"""Bounded two-terminal-mode extension, with no new clock quadrature.

Inherit old amplitude rectangles and independently derived Gaussian moment
rectangles. This changes the output instrument and uses its separate gain.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

from interference import (iv, ROOT, SOURCE, EXPECTED_SOURCE, require, real,
    read_complex, read_real, enc, norm2, conj, zero_inside, effect, failure,
    rows_from_inputs, matrix_enc, madd, mscale, matrix_equal_enclosure)

MOMENTS = ROOT / 'checks/r_records_results.json'
CONTRACT = ROOT / 'contracts/r_records.json'


def class_amplitudes(inputs, eta, kappa):
    # Order remains class1 atom, class1 positive, class2 atom, class2 positive.
    modes = []
    for a in inputs:
        phase = [iv.exp(iv.j * (kappa - 1) * f) for f in [9, 9, -7, -7]]
        f0 = [v * p for v, p in zip(a, phase)]
        f2 = [v * eta[j // 2] for j, v in enumerate(f0)]
        modes.append([f0, f2])
    return modes


def run_instrument(modes, gamma, gain, separated_bound):
    """E_gamma=(1-gamma)E_dephased+gamma E_coherent, real 0<=gamma<=1."""
    require(0 <= gamma <= 1, 'Only declared real environmental overlap allowed')
    gi = real(gamma)
    g2 = real(gain) ** 2
    # Entire two-dimensional input E is covered, including off-diagonal effects.
    mode_effects = []
    all_coherent_rows = []
    all_separate_rows = []
    joint_effects = []
    for r in range(2):
        rows = rows_from_inputs([m[r] for m in modes])
        separate = effect(rows, gain)
        coherent_rows = [[rows[s][i] + rows[s + 2][i] for i in range(2)] for s in range(2)]
        coherent = effect(coherent_rows, gain)
        mode_effects.append(madd(mscale(1 - gi, separate), mscale(gi, coherent)))
        all_separate_rows.extend(rows)
        all_coherent_rows.extend(coherent_rows)
        for s in range(2):
            es = effect([rows[s], rows[s+2]], gain)
            ec = effect([coherent_rows[s]], gain)
            joint_effects.append(madd(mscale(1-gi, es), mscale(gi, ec)))
    accepted = madd(*mode_effects)
    separated_effect = effect(all_separate_rows, gain)
    coherent_effect = effect(all_coherent_rows, gain)
    require(matrix_equal_enclosure(accepted, madd(mscale(1-gi,separated_effect), mscale(gi,coherent_effect))),
            'Full-E CP mixture consistency check failed')
    distributions = []
    f2p = []
    for mode in modes:
        q = []
        cross = []
        for amps in mode:
            for s in range(2):
                cc = amps[s] * conj(amps[s+2])
                cross.append(cc)
                q.append(norm2(amps[s]) + norm2(amps[s+2]) + 2*gi*cc.real)
        require(all(v.a >= 0 for v in q), 'Unresolved positive joint R weight')
        z = sum(q)
        require(z.a > 0, 'Unresolved two-mode success')
        probability = (q[2]+q[3])/z
        f2p.append(probability)
        distributions.append({'joint_raw_weights': list(map(enc,q)),
            'joint_unconditional': [enc(g2*v) for v in q],
            'joint_conditional_on_success': [enc(v/z) for v in q],
            'R_conditional_on_success': [enc((q[0]+q[1])/z), enc(probability)],
            'R_unconditional': [enc(g2*(q[0]+q[1])), enc(g2*(q[2]+q[3]))],
            'success': enc(g2*z), 'failure': enc(1-g2*z),
            'cross_by_joint_record': list(map(enc,cross))})
        require(zero_inside(sum(g2*v for v in q)+(1-g2*z)-1), 'Probability conservation failed')
    delta = f2p[1]-f2p[0]
    uniform_bound = (1+gamma)*separated_bound
    return {'gamma_real':str(gamma), 'gain':str(gain),
        'accepted_effect':matrix_enc(accepted),
        'joint_record_effects': [matrix_enc(m) for m in joint_effects],
        'R_effects': [matrix_enc(m) for m in mode_effects],
        'analytic_uniform_accepted_effect_upper_bound':str(uniform_bound),
        'failure':failure(accepted,uniform_bound),
        'inputs':distributions,
        'source_difference_gplus_minus_g0_f2_given_success':enc(delta),
        'source_difference_excludes_zero':not zero_inside(delta),
        'probability_conservation_and_effect_mixture_enclosure_checks':True}


def main():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED_SOURCE,'Source changed')
    contract = json.loads(CONTRACT.read_text())
    moments = json.loads(MOMENTS.read_text())
    contract_hash = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
    require(moments['source_hashes']['boundary_coherence_v0_1/contracts/r_records.json']==contract_hash,
            'Moment and output-instrument contracts disagree')
    require(moments['eta_independent_of_preparation_and_inner_stratum'], 'Factorization not established')
    require(moments['orthonormality']=={'f0_norm_squared':'1','f2_norm_squared':'1','inner_product':'0'},
            'Declared terminal output basis not orthonormal')
    require(contract['gain']=='1/1024' and moments['gain']=='1/1024', 'Wrong extension gain')
    source = json.loads(SOURCE.read_text())
    inputs = [[read_complex(z) for z in row] for row in source['analysis']['amplitudes']]
    eta = [read_complex(moments['eta_by_class'][c]) for c in ['1','2']]
    gain = F(1,1024)
    bound = F(548451,3276800)
    require(bound==4*F(3,5)**2*F(2257,16)*(65+799)*gain**2,'Majorant derivation mismatch')
    cases = {}
    inherited_modes = class_amplitudes(inputs, eta, 1)
    for kappa in [1,0]:
        modes = class_amplitudes(inputs, eta, kappa)
        cases[str(kappa)] = {'interpretation': 'inherited gravitational phases' if kappa==1 else
            'counterfactual gravity-phase removal; not an observed setting or calibrated physical control',
            'gamma_cases':{str(g):run_instrument(modes,g,gain,bound) for g in [F(0),F(1,2),F(1)]}}
    contrasts = {}
    for gamma in ['0','1/2','1']:
        phase_diffs=[]
        for i in range(2):
            p1 = read_real(cases['1']['gamma_cases'][gamma]['inputs'][i]['R_conditional_on_success'][1])
            p0 = read_real(cases['0']['gamma_cases'][gamma]['inputs'][i]['R_conditional_on_success'][1])
            d = p1-p0
            phase_diffs.append({'kappa1_minus_kappa0_f2_given_success':enc(d),
                'excludes_zero':not zero_inside(d)})
        d1 = read_real(cases['1']['gamma_cases'][gamma]['source_difference_gplus_minus_g0_f2_given_success'])
        d0 = read_real(cases['0']['gamma_cases'][gamma]['source_difference_gplus_minus_g0_f2_given_success'])
        interaction = d1-d0
        contrasts[gamma]={'phase_contrast_by_input':phase_diffs,
            'source_contrast_kappa1_minus_source_contrast_kappa0':enc(interaction),
            'interaction_excludes_zero':not zero_inside(interaction)}
    coherence_contrasts = {}
    for kappa in ['1','0']:
        coherent = cases[kappa]['gamma_cases']['1']
        dephased = cases[kappa]['gamma_cases']['0']
        by_input=[]
        for i in range(2):
            p1=read_real(coherent['inputs'][i]['R_conditional_on_success'][1])
            p0=read_real(dephased['inputs'][i]['R_conditional_on_success'][1])
            d=p1-p0
            by_input.append({'gamma1_minus_gamma0_f2_given_success':enc(d),
                'excludes_zero':not zero_inside(d)})
        d=read_real(coherent['source_difference_gplus_minus_g0_f2_given_success'])-read_real(dephased['source_difference_gplus_minus_g0_f2_given_success'])
        coherence_contrasts[kappa]={'by_input':by_input,
            'coherent_source_contrast_minus_dephased_source_contrast':enc(d),
            'excludes_zero':not zero_inside(d),
            'interpretation':'The dephased instrument already has a matter-record source contrast. A nonzero source contrast alone is not an interference witness.'}
    # Exact common-multiplier statement is algebraic; below is a consistency test.
    m = iv.mpc(2,1)
    control_inputs=[inputs[0],[m*v for v in inputs[0]]]
    control_modes=class_amplitudes(control_inputs,eta,1)
    for gamma in [F(0),F(1,2),F(1)]:
        # These synthetic columns are not the original orthonormal input basis.
        # Test normalized responses only; do not reuse E's operator majorant.
        control_probs=[]
        for mode in control_modes:
            q=[]
            for amps in mode:
                for s in range(2):
                    q.append(norm2(amps[s])+norm2(amps[s+2])+
                        2*real(gamma)*(amps[s]*conj(amps[s+2])).real)
            control_probs.append((q[2]+q[3])/sum(q))
        require(zero_inside(control_probs[1]-control_probs[0]),
                'Fixed-clock common multiplier control failed')
    result={'id':'BOUNDARY-TWO-R-MATTER-RECORD-PROPAGATION-0.1',
        'status':'PASS_INHERITED_INTERVALS_WITH_ANALYTIC_GAUSSIAN_EXTENSION',
        'sources':{'amplitudes_sha256':EXPECTED_SOURCE,'moment_results_sha256':hashlib.sha256(MOMENTS.read_bytes()).hexdigest(),
                   'contract_sha256':contract_hash},
        'arithmetic':{'engine':'mpmath.iv','decimal_precision':iv.dps,'export_digits':40,'rounding':'outward'},
        'new_clock_integrals_evaluated':0,
        'assumptions':'Inherits original amplitude enclosures and independently derived Gaussian moment enclosures. The common-endstate coherence is a new instrument assumption, not inferred from these numbers.',
        'joint_record_order':[['f0','atom'],['f0','positive'],['f2','atom'],['f2','positive']],
        'input_order':['g0','gplus'],'R_order':['f0','f2'],
        'gain':'1/1024','gamma':['0','1/2','1'],'theta_or_phase_search':False,
        'class_to_R_amplitude_rule':'a_f2(c,s;g)=eta_c a_f0(c,s;g); B_(r,s)=gain*(a_r,1,s+a_r,2,s)',
        'amplitudes_by_input_mode':[[list(map(enc,a)) for a in modes] for modes in inherited_modes],
        'cases':cases,'gravity_phase_contrasts':contrasts,'coherence_contrasts':coherence_contrasts,
        'controls':{'gamma_zero_gravity_phase_blind':'Exactly, by squared moduli; propagated differences enclose zero.',
            'classical_postprocessing_not_used_to_create_coherence':True,
            'fixed_clock_common_multiplier_normalized_R_response_unchanged':True,
            'common_multiplier_check_is_not_a_new_clock_state_or_quadrature':True,
            'probability_conservation':'All joint probabilities plus the separately recomputed failure sum to one.',
            'full_input_space':'All accepted effects and principal failure roots are evaluated on E=span(g0,gplus), not just separately on the two input states.'},
        'interpretation':'Two actual terminal scalar matter mode records within the finite auxiliary model. They are not the +/- analyzer flags, geometric observables, or evidence of backreaction.',
        'stop_rule':'Do not extend the model on these numerical contrasts alone: stop the physical claim if environmental coherence, a source calibration, or a geometric response observable cannot be independently justified.'}
    for item in contrasts['0']['phase_contrast_by_input']:
        require(not item['excludes_zero'],'Dephased R control has spurious phase signal')
    target=Path(__file__).with_name('extended_R_results.json')
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':result['status'],
        'coherent_R_f2_probabilities':[i['R_conditional_on_success'][1] for i in cases['1']['gamma_cases']['1']['inputs']],
        'coherent_R_source_contrast':cases['1']['gamma_cases']['1']['source_difference_gplus_minus_g0_f2_given_success'],
        'coherent_R_phase_controls':contrasts['1'], 'output':str(target)},indent=2))


if __name__=='__main__':
    main()
