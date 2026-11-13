"""Propagate sibling full-weight data into a conditional geometry diagnostic."""
import hashlib
import json


def evaluate(root):
    weight_path=root.parent/'full_weight/results.json'
    scalar_path=root.parent/'scalar_response/results.json'
    weights=json.loads(weight_path.read_text())
    scalars=json.loads(scalar_path.read_text())
    assert weights['clock_order_theta_restriction'] is False
    assert weights['no_stationary_phase_double_count'] is True
    def cx(d):return complex(float(d['real']),float(d['imag']))
    gr=cx(scalars['g1_over_g0']);gr2=abs(gr)**2
    records=[]
    for rho in ('1/8','1/4'):
        by_order=[]
        for nodes in sorted({z['nodes_per_axis'] for z in weights['quadrature']['chain']}):
            c0=next(z for z in weights['quadrature']['chain'] if z['nodes_per_axis']==nodes)['sources'][rho]
            c1=next(z for z in weights['quadrature']['two_cover_deleted'] if z['nodes_per_axis']==nodes)['sources'][rho]
            w0,w1=cx(c0['W']),cx(c1['W']);d0,d1=cx(c0['dW_drho']),cx(c1['dW_drho'])
            R=gr*w1/w0;lam=abs(R)**2;mean=(3+lam)/(1+lam)
            logmod=(d1/w1-d0/w0).real
            derivative=-4*lam*logmod/(1+lam)**2
            q0,q1=abs(w0)**2,gr2*abs(w1)**2
            q0p,q1p=2*(d0*w0.conjugate()).real,2*gr2*(d1*w1.conjugate()).real
            derivative_direct=((3*q0p+q1p)*(q0+q1)-(3*q0+q1)*(q0p+q1p))/(q0+q1)**2
            assert abs(derivative-derivative_direct)<1e-12
            assert abs(mean-(3*q0+q1)/(q0+q1))<1e-14
            unit_R=gr*(w1/abs(w1))/(w0/abs(w0))
            phase_only=(3+abs(unit_R)**2)/(1+abs(unit_R)**2)
            assert abs(phase_only-(3+gr2)/(1+gr2))<1e-14
            weak=(3+R)/(1+R)
            by_order.append({'nodes_per_axis':nodes,'lambda_intensity':lam,
              'resolved_conditional_O':mean,'d_resolved_O_drho':derivative,
              'd_log_modulus_Wratio_drho':logmod,
              'relative_amplitude_R':{'real':R.real,'imag':R.imag},
              'accepted_additivity_defect_divided_by_abs_a0_squared':2*R.real,
              'coherent_amplitude_ratio_O':{'real':weak.real,'imag':weak.imag},
              'phase_only_unit_modulus_W_control_O':phase_only})
        records.append({'rho':rho,'quadrature_orders':by_order,'selected':by_order[-1]})
    lo,hi=[r['selected'] for r in records]
    contrast=hi['resolved_conditional_O']-lo['resolved_conditional_O']
    contrast_identity=2*(lo['lambda_intensity']-hi['lambda_intensity'])/((1+lo['lambda_intensity'])*(1+hi['lambda_intensity']))
    assert abs(contrast-contrast_identity)<1e-14
    spread=max(max(abs(z['resolved_conditional_O']-r['selected']['resolved_conditional_O']) for z in r['quadrature_orders']) for r in records)
    checks={
      'full_weight_resolved_source_contrast_numerically_nonzero':abs(contrast)>max(100*spread,1e-4),
      'phase_only_ablation_resolved_source_contrast_zero':abs(hi['phase_only_unit_modulus_W_control_O']-lo['phase_only_unit_modulus_W_control_O'])<1e-14,
      'computed_class_alternatives_not_numerically_weakly_decoherent':all(abs(r['selected']['accepted_additivity_defect_divided_by_abs_a0_squared'])>1e-4 for r in records),
      'full_weight_quadrature_orders_empirically_agree':spread<1e-11,
    }
    assert all(checks.values()),checks
    numeric={
     'history_weight_assumption':{'omega0':1,'omega1':1,'physical_measure_derivation':False},
     'source_files_sha256':{'full_weight/results.json':hashlib.sha256(weight_path.read_bytes()).hexdigest(),'scalar_response/results.json':hashlib.sha256(scalar_path.read_bytes()).hexdigest()},
     'g1_over_g0_used':{'real':gr.real,'imag':gr.imag},'g_ratio_modulus_squared':gr2,
     'source_results':records,
     'resolved_O_source_contrast_1over4_minus_1over8':contrast,
     'maximum_observed_resolved_mean_spread_across_quadrature_orders':spread,
     'phase_only_control':{'rule':'Replace each complete W_c by W_c/|W_c| while retaining its actual phase and the fixed scalar factor; this is a diagnostic ablation, not a new derived action.',
        'resolved_O_at_both_sources':(3+gr2)/(1+gr2),'source_contrast':0},
     'modulus_frozen_control':{'rule':'Freeze both |W_c| to their rho=1/8 values while retaining each source-dependent phase.',
        'resolved_O_at_both_sources':lo['resolved_conditional_O'],'source_contrast':0},
     'qualification':'Float64 diagnostic propagated from the full-weight quadrature and high-precision scalar factor. Analytic quadrature truncation bounds do not certify floating-point evaluation; the contrast is numerically stable, not a rigorous interval certificate.',
     'causal_source_qualification':'rho is changed on all eight outer boundary densities, including the later boundary. This is a two-sided Dirichlet boundary-parameter response, not an isolated initial-source change with fixed final filter.',
    }
    return checks,numeric
