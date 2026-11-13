#!/usr/bin/env python3
"""Combine verified components under explicitly equal fixed history weights."""
from pathlib import Path
import cmath
import json

ROOT = Path(__file__).resolve().parent
CHECKS = ROOT.parent

def read(name):
    return json.loads((CHECKS/name/'results.json').read_text())

def z(v):
    return complex(float(v['real']), float(v['imag']))

def pack(v):
    return {'real': v.real, 'imag': v.imag}

def main():
    scalar, weights = read('scalar_response'), read('full_weight')
    g = [z(o['g_at_zero']) for o in scalar['orders']]
    h = [z(o['q0q10']) for o in scalar['orders']]
    gr = z(scalar['g1_over_g0'])
    assert abs(g[1]/g[0]-gr) < 1e-14
    outcomes = {}
    for rho in ['1/8','1/4']:
        entries = [weights['quadrature'][c][-1]['sources'][rho]
                   for c in ['chain','two_cover_deleted']]
        W = [z(e['W']) for e in entries]
        dW = [z(e['dW_drho']) for e in entries]
        a = [g[k]*W[k] for k in range(2)]
        da = [g[k]*dW[k] for k in range(2)]
        R = a[1]/a[0]
        dlogR = dW[1]/W[1]-dW[0]/W[0]
        H = (a[0]*h[0]+a[1]*h[1])/sum(a)
        dH = (h[1]-h[0])*(a[0]*da[1]-a[1]*da[0])/sum(a)**2
        assert abs(dH-(h[1]-h[0])*R*dlogR/(1+R)**2) < 1e-13
        intensity = abs(R)**2
        mean_resolved = (3+intensity)/(1+intensity)
        dmean = -4*intensity/(1+intensity)**2*dlogR.real
        # A common record is a different experiment from orthogonal records.
        dcross = a[0]*a[1].conjugate()
        Z_resolved = sum(abs(v)**2 for v in a)
        Z_coherent = abs(sum(a))**2
        assert abs(Z_coherent-(Z_resolved+2*dcross.real)) < 1e-17
        assert 1 < mean_resolved < 3
        assert abs(1+R) > .4
        # Omission controls change the density measure; not physical predictions.
        positive_only_R = gr*z(entries[1]['stratum_W'][7])/z(entries[0]['stratum_W'][7])
        atom_only_R = gr*z(entries[1]['stratum_W'][0])/z(entries[0]['stratum_W'][0])
        r = eval_fraction(rho)
        phase_only_R = gr*cmath.exp(1j*(8+23*r/19))
        outcomes[rho] = {
            'W': [pack(v) for v in W], 'amplitudes_omega_equal_one': [pack(v) for v in a],
            'relative_amplitude_R': pack(R), 'abs_R': abs(R), 'phase_R_radians': cmath.phase(R),
            'log_R_source_derivative': pack(dlogR), 'abs_1_plus_R': abs(1+R),
            'complex_q0q10_insertion': pack(H), 'insertion_source_derivative': pack(dH),
            'resolved_geometry_mean': mean_resolved, 'resolved_geometry_mean_derivative': dmean,
            'unnormalized_coherent_event_weight': Z_coherent,
            'unnormalized_resolved_event_weight': Z_resolved,
            'coherent_history_cross_term': pack(dcross),
            'density_omission_controls_R': {'positive_only': pack(positive_only_R), 'atom_only':pack(atom_only_R)},
            'uncorrected_stationary_phase_only_R': pack(phase_only_R),
            'phase_only_geometry_mean': (3+abs(gr)**2)/(1+abs(gr)**2),
        }
    low, high = outcomes['1/8'], outcomes['1/4']
    difference = z(high['complex_q0q10_insertion'])-z(low['complex_q0q10_insertion'])
    assert abs(difference) > .05
    assert high['resolved_geometry_mean'] < low['resolved_geometry_mean']
    assert low['phase_only_geometry_mean'] == high['phase_only_geometry_mean']
    output = {
        'id': 'CST-DUST-FULL-WEIGHT-COMBINED-RESPONSE-0.1',
        'assumptions': ['omega0=omega1=1 fixed independently of rho', 'frozen common scalar Gaussian',
                        'fixed Dirichlet boundary clock/density data and chosen inner box measure',
                        'coherent and resolved readouts are separate conditional constructions'],
        'rho_is_time': False, 'physical_history_weights_derived': False,
        'results': outcomes,
        'high_minus_low_complex_insertion': pack(difference),
        'high_minus_low_resolved_geometry_mean': high['resolved_geometry_mean']-low['resolved_geometry_mean'],
        'numerical_status': 'float64 combination of controlled quadrature and high-precision scalar factors; not a rigorous interval enclosure',
        'interpretation': 'Nonzero conditional source response, not a derived physical covariance or four-dimensional geometric evolution.',
        'all_checks_passed': True
    }
    (ROOT/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'all_checks_passed':True, 'insertion_contrast':pack(difference),
                      'resolved_geometry_means':[low['resolved_geometry_mean'],high['resolved_geometry_mean']]}))

def eval_fraction(s):
    p,q=s.split('/')
    return int(p)/int(q)

if __name__ == '__main__':
    main()
