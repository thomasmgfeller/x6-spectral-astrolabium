"""X6 polarization/filter/spectral design checks; no instrument control.

All spectral densities are on fixed laboratory ports AFTER the installed
filter/coupling chain and before polarization analysis. Frequency axes in THz.
Input observations must already carry documented exposure/pump/response
normalization. Missing phases produce only an upper bound, never coherence.
"""
import argparse
import cmath
import json
import math
from pathlib import Path

H_PLANCK = 6.62607015e-34
C_LIGHT = 299792458.0


def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"{name}: finite number required")
    return float(x)


def waveplate(theta_deg, delta_rad, field):
    """Jones retarder in a specified transverse basis; mean phase omitted.

    Do not infer the SPDC relative carrier phase from this reduced matrix.
    Reverse physical propagation uses theta -> -theta in u=Z cross k, v=Z.
    """
    t = math.radians(finite(theta_deg, 'theta_deg'))
    d = finite(delta_rad, 'delta_rad')
    c, s = math.cos(t), math.sin(t)
    a, b = cmath.exp(-.5j*d), cmath.exp(.5j*d)
    x, y = field
    return ((a*c*c+b*s*s)*x + (a-b)*c*s*y,
            (a-b)*c*s*x + (a*s*s+b*c*c)*y)


def pbs_port(incident_port, polarization):
    """Ideal reciprocal topology; amplitudes/phases intentionally not implied."""
    table = {'H': {'W':'E','E':'W','N':'S','S':'N'},
             'V': {'W':'N','N':'W','E':'S','S':'E'}}
    return table[polarization][incident_port]


def photon_energy(wavelength_nm):
    lam = finite(wavelength_nm, 'wavelength_nm')
    if lam <= 0:
        raise ValueError('positive wavelength required')
    return H_PLANCK*C_LIGHT/(lam*1e-9)


def filter_budget(power_W, wavelength_nm, eta_upper, background_limit_s, od_lower):
    p = finite(power_W, 'power_W')
    eta = finite(eta_upper, 'eta_upper')
    b = finite(background_limit_s, 'background_limit_s')
    od = finite(od_lower, 'od_lower')
    if p < 0 or not 0 <= eta <= 1 or b <= 0 or od < 0:
        raise ValueError('invalid filter-budget range')
    incident = p/photon_energy(wavelength_nm)
    req = max(0., math.log10(incident*eta/b)) if incident*eta > 0 else 0.
    return {'incident_photons_s':incident, 'required_od':req,
            'pump_background_upper_s':incident*eta*10**(-od),
            'od_margin':od-req, 'calculation_only':True}


def accidental_rate(singles, full_window_s):
    if len(singles) != 4:
        raise ValueError('exactly A+, A-, B+, B- required')
    a = [finite(x,'singles') for x in singles]
    w = finite(full_window_s,'full_window_s')
    if min(a) < 0 or w <= 0:
        raise ValueError('invalid rates/window')
    return (a[0]+a[1])*(a[2]+a[3])*w


def tail_overlap_bounds(gamma_inside_abs, missing_cw, missing_ccw):
    """Exact missing fractions in a common spectral window, arbitrary tail phase.

    Applying upper missing-mass bounds yields a conservative lower bound only.
    This does not account for instrumental blurring or calibration uncertainty.
    """
    g,a,b=[finite(x,'overlap/tail') for x in (gamma_inside_abs,missing_cw,missing_ccw)]
    if any(x<0 or x>1 for x in (g,a,b)):
        raise ValueError('overlap and missing fractions must lie in [0,1]')
    centre=math.sqrt((1-a)*(1-b))*g
    radius=math.sqrt(a*b)
    return {'lower':max(0.,centre-radius),'upper':min(1.,centre+radius)}


def trap_weights(axis):
    x = [finite(v,'frequency axis') for v in axis]
    if len(x) < 2 or any(b <= a for a,b in zip(x,x[1:])):
        raise ValueError('at least two strictly increasing coordinates required')
    return [(x[1]-x[0])/2] + [(x[i+1]-x[i-1])/2 for i in range(1,len(x)-1)] + [(x[-1]-x[-2])/2]


def spectral_overlap(data):
    """Trapezoid quadrature. Intensities: upper bound only. Phase: conditional gamma.

    Upper bound B = integral sqrt(Jcw Jccw)/sqrt(Icw Iccw).
    gamma = integral sqrt(Jcw Jccw) exp(i(phi_ccw-phi_cw))/sqrt(Icw Iccw).
    This assumes coherent amplitudes f=sqrt(J)*exp(i*phi). Mixed states or
    unresolved incoherent modes need a mutual-coherence/density-matrix model;
    a phase array alone does not establish this assumption experimentally.
    No separate spatial overlap factor should be multiplied when these are
    already full complex amplitudes projected into the selected fiber modes.
    """
    if data.get('reference_plane') != 'AFTER_INSTALLED_FILTERS':
        raise ValueError('reference plane must be AFTER_INSTALLED_FILTERS; do not double-filter')
    if data.get('density_units') != 'relative_rate_per_THz2':
        raise ValueError('explicit calibrated relative_rate_per_THz2 required')
    wx, wy = trap_weights(data['nu_A_THz']), trap_weights(data['nu_B_THz'])
    na, nb = len(wx),len(wy)
    def matrix(name, nonnegative):
        raw = data[name]
        if len(raw)!=na or any(len(row)!=nb for row in raw):
            raise ValueError(name+': complete rectangular grid required')
        z=[[finite(x,name) for x in row] for row in raw]
        if nonnegative and any(x<0 for row in z for x in row):
            raise ValueError(name+': negative data require a documented measurement model, not clipping')
        return z
    a,b=matrix('cw_density',True),matrix('ccw_density',True)
    phase = matrix('relative_phase_rad',False) if data.get('relative_phase_rad') is not None else None
    ia=ib=cross_abs=0.; cross=0j
    for i in range(na):
        for j in range(nb):
            weight=wx[i]*wy[j]
            ia+=weight*a[i][j];ib+=weight*b[i][j]
            product=weight*math.sqrt(a[i][j]*b[i][j])
            cross_abs+=product
            if phase is not None: cross+=product*cmath.exp(1j*phase[i][j])
    if min(ia,ib)<=0:
        raise ValueError('both alternatives require nonzero integrated density')
    den=math.sqrt(ia*ib); upper=cross_abs/den; balance=2*den/(ia+ib)
    if upper>1+1e-12: raise ArithmeticError('overlap violates Cauchy-Schwarz')
    gamma=cross/den if phase is not None else None
    required=['response_calibration','pump_normalization','spectral_resolution',
              'out_of_band_weight','uncertainty_budget','phase_evidence','mutual_coherence_model']
    evidence=data.get('evidence',{})
    missing=[x for x in required if not evidence.get(x)]
    return {'scope':'CALCULATION_NOT_HARDWARE_ACCEPTANCE',
            'model_assumption':'COHERENT_AMPLITUDES_NOT_CERTIFIED_FOR_MIXED_STATES',
            'integrated_cw':ia,'integrated_ccw':ib,'rate_ratio_ccw_cw':ib/ia,
            'balance_factor':balance,'intensity_overlap_upper_bound':min(1.,upper),
            'gamma_abs':abs(gamma) if gamma is not None else None,
            'gamma_re':gamma.real if gamma is not None else None,
            'gamma_im':gamma.imag if gamma is not None else None,
            'signed_coherence_before_other_losses':balance*gamma.real if gamma is not None else None,
            'phase_status':'PROVIDED_NOT_CERTIFIED' if phase is not None else 'NOT_MEASURED',
            'missing_evidence':missing,'hardware_status':'NOT_RUN'}


def design_results():
    dtheta=.25; ddelta=2*math.pi/100
    wrong=1-math.cos(2*math.radians(dtheta))**2*math.cos(ddelta/2)**2
    bmin=.995
    b_range=[((1-sign*math.sqrt(1-bmin*bmin))/bmin)**2 for sign in (1,-1)]
    # Explicit separated-factor scenario, not a universal error bound.
    factors={'balance':.995,'spectral':.98,'spatial':.99,'analyzer':.995,
             'phase':math.cos(.1),'signal_fraction':.99}
    return {'origin':'DESIGN_SCENARIOS_ONLY','hardware_status':'NOT_RUN',
      'waveplate_wrong_fraction':wrong,'waveplate_two_photons_any_wrong':1-(1-wrong)**2,
      'pbs_wrong_fraction_ER1000':1/1001,'pbs_wrong_fraction_ER300':1/301,
      'balanced_ratio_range':b_range,'separable_visibility_factors':factors,
      'separable_visibility':math.prod(factors.values()),
      'filter_worst_3mW_OD6':filter_budget(.003,405,1,100,6),
      'filter_worst_3mW_OD10':filter_budget(.003,405,1,100,10),
      'filter_worst_3mW_OD14':filter_budget(.003,405,1,100,14),
      'filter_post_dichroic_1uW_OD10':filter_budget(1e-6,405,1,100,10),
      'filter_transmission_request':{'per_arm':.95*.90*.80,'pair':(.95*.90*.80)**2},
      'filter_angle_shift_nm_scenario_neff2':{str(a):810*(math.sqrt(1-math.sin(math.radians(a))**2/4)-1) for a in (1,2,5)},
      'accidentals_at_3000_each_s':accidental_rate([3000]*4,2e-9),
      'accidentals_at_3100_each_s':accidental_rate([3100]*4,2e-9),
      'accidentals_at_100000_each_s':accidental_rate([100000]*4,2e-9)}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spectral',type=Path,help='normalized AFTER_INSTALLED_FILTERS JSON grid')
    args=p.parse_args()
    result=spectral_overlap(json.loads(args.spectral.read_text())) if args.spectral else design_results()
    print(json.dumps(result,indent=2,allow_nan=False))
