"""Conditional 405/810 nm design calculations. All times are ps and lengths µm unless named otherwise."""
import cmath
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
C = 299.792458  # vacuum µm/ps
FWHM = 2 * math.sqrt(2 * math.log(2))
KTP = {"y": (3.45018, .04341, .04597, 16.98825, 39.43799),
       "z": (4.59423, .06206, .04763, 110.80672, 86.12171)}


def indices(lam, axis):
    """Kato–Takaoka at 20 °C, including analytic group index."""
    if not .43 <= lam <= 3.54:
        raise ValueError("outside the 0.43–3.54 µm dispersion fit")
    a,b,c,d,e = KTP[axis]
    l2 = lam**2
    n = math.sqrt(a + b/(l2-c) + d/(l2-e))
    return n, n + l2/n * (b/(l2-c)**2 + d/(l2-e)**2)


def spectral(p, delay_ps=0., common_delay_ps=0., mismatch_m=(0.,0.), filter_shift_nm=0.,
             group_excess=None, grid=241, extent=6.0):
    """Complex JSA integral in sum/difference frequencies. Centered-crystal reference planes."""
    lam = p["lambda_d_um"]
    L = p["crystal_length_um"]
    pump_width = C / p["lambda_p_um"]**2 * p["pump_fwhm_nm"] / 1000
    filter_width = C / lam**2 * p["bandpass_fwhm_nm"] / 1000
    center_b = -C / lam**2 * filter_shift_nm / 1000
    g = p["pump_group_excess_scenario"] if group_excess is None else group_excess
    dg = indices(lam,"z")[1] - indices(lam,"y")[1]
    u = np.linspace(-extent*pump_width, extent*pump_width, grid)[:,None]
    v = np.linspace(-extent*filter_width, extent*filter_width, grid)[None,:]
    f_a, f_b = u/2 + v, u/2 - v
    transmission = p["bandpass_peak_per_arm"]**2 * np.exp(-4*math.log(2) *
        ((u/pump_width)**2 + (f_a/filter_width)**2 + ((f_b-center_b)/filter_width)**2))
    base = L/C * (g*u + dg*v)
    # np.sinc(t) = sin(pi t)/(pi t); mismatch is rad/m, converted to rad/µm.
    a,b = (np.sinc(base + L*k*1e-6/(2*math.pi)) for k in mismatch_m)
    ia = float(np.sum(transmission*a*a))
    ib = float(np.sum(transmission*b*b))
    phase = 2j*math.pi*(v*delay_ps + u*common_delay_ps)
    cross = np.sum(transmission*a*b*np.exp(phase))
    gamma = complex(cross / math.sqrt(ia*ib))
    r = p["ccw_over_cw_power_ratio"] * ib/ia
    balanced = 2*math.sqrt(r)/(1+r)
    fixed = (gamma * cmath.exp(1j*p["phase_error_rad"])).real
    return {"gamma_abs": abs(gamma), "gamma_re":gamma.real, "gamma_im":gamma.imag,
            "power_balance_factor":balanced,
            "signed_DA_contrast_before_background":balanced * p["residual_spatial_amplitude_overlap"] * fixed,
            "integrated_weight_THz2":(ia+p["ccw_over_cw_power_ratio"]*ib)*float(u[1,0]-u[0,0])*float(v[0,1]-v[0,0])}


def coupling(lam, wf, w0, dx=0., dy=0., z=0., tx=0., ty=0.):
    """Normalized power overlap at the fiber facet in air. Angles in radians."""
    zr=math.pi*w0*w0/lam
    w=w0*math.sqrt(1+(z/zr)**2)
    k=2*math.pi/lam
    a=1/w**2 + 1j*k*z/(2*(z*z+zr*zr))
    den=a+1/wf**2
    exponent=-a*(dx*dx+dy*dy) + ((2*a*dx+1j*k*tx)**2+(2*a*dy+1j*k*ty)**2)/(4*den)
    return abs(2*cmath.exp(exponent)/(w*wf*den))**2


def window_probability(sigma_ps, offset_ps, full_window_ps):
    if sigma_ps <= 0 or full_window_ps <= 0:
        raise ValueError("positive RMS and window required")
    h=full_window_ps/2
    return (math.erf((h-offset_ps)/(math.sqrt(2)*sigma_ps))+
            math.erf((h+offset_ps)/(math.sqrt(2)*sigma_ps)))/2


def timing(p):
    rows=[]
    q=p["tdc_step_ps"]
    for a in (0,1):
        for b in (2,3):
            se=p["electronics_sigma_ps_scenario"]
            sd=p["detector_sigma_ps_scenario"]
            offset=p["offset_residual_ps_scenario"][b]-p["offset_residual_ps_scenario"][a]
            electronic=math.sqrt(se[a]**2+se[b]**2+q*q/6)
            sigma=math.sqrt(electronic**2+sd[a]**2+sd[b]**2)
            retain=window_probability(sigma,offset,p["full_window_ps"])
            tail=window_probability(sigma,offset+1500,p["full_window_ps"])
            singles=p["per_channel_singles_per_s_scenario"]
            rows.append({"ports":[a,b],"pair_offset_ps":offset,"electronics_rms_ps":electronic,
                         "core_fwhm_ps":FWHM*sigma,"core_window":retain,
                         "delayed_5pct_window":.95*retain+.05*tail,
                         "accidentals_per_s":singles[a]*singles[b]*p["full_window_ps"]*1e-12})
    return rows


def evaluate(p):
    lam=p["lambda_d_um"]; L=p["crystal_length_um"]
    ny,gy=indices(lam,"y"); nz,gz=indices(lam,"z")
    w=p["fiber_mfd_um"]/2; f=p["relay_f2_mm"]*1000; eta=p["minimum_relative_coupling"]
    zr=math.pi*w*w/lam
    dx=w*math.sqrt(-math.log(eta))
    eta_joint=coupling(lam,w,w,dx=.35,z=5.,tx=.005)
    nominal=spectral(p)
    cases={"matched":nominal, "delay_0.25ps":spectral(p,.25),"delay_1ps":spectral(p,1),
           "delay_2ps":spectral(p,2), "mismatch_CCW_300rad_m":spectral(p,mismatch_m=(0,300)),
           "common_mismatch_300rad_m":spectral(p,mismatch_m=(300,300)), "filter_B_plus1nm":spectral(p,filter_shift_nm=1),
           "stress_combined":spectral(p,.50,.20,(0,300),1)}
    rows=timing(p); bg=sum(x["accidentals_per_s"] for x in rows)
    rates={}
    for name,s in cases.items():
        rel=s["integrated_weight_THz2"]/nominal["integrated_weight_THz2"]
        good=(p["accepted_pair_flux_before_fibers_per_s_scenario"]*rel*
              (eta_joint*p["other_transmission_per_arm_scenario"]*p["pde_per_detector_scenario"])**2*
              min(x["core_window"] for x in rows))
        rates[name]={"relative_spectral_yield":rel,"true_pairs_per_s_lower_scenario":good,
                     "accidental_to_true":bg/good,"expected_true_pairs_in_600s":good*600,
                     "raw_DA_symmetric_background_scenario":s["signed_DA_contrast_before_background"]/(1+bg/good)}
    background = rates["matched"]["accidental_to_true"]
    def margin(delay):
        return spectral(p,delay)["signed_DA_contrast_before_background"]/(1+background)-.90
    limit = brentq(margin,0,1) if margin(0)>=0 and margin(1)<=0 else None
    return {"nominal_residual_delay_ps_at_90pct":limit, "scope":"DESIGN_ONLY", "hardware_gates":p["hardware_gates"],
            "crystal":{"n_y":ny,"n_z":nz,"ng_y":gy,"ng_z":gz,"full_crystal_dgd_ps":L*(gz-gy)/C,
                       "half_power_delta_k_abs_rad_per_m":2*1.39155737825151/(L*1e-6),
                       "fixed_pump_unfiltered_pm_fwhm_THz":2*1.39155737825151*C/(math.pi*L*abs(gz-gy))},
            "spectral":cases,"pump_slope_sensitivity_at_1ps":
                {str(g):spectral(p,1,group_excess=g)["gamma_abs"] for g in (0,.10,.20)},
            "fiber":{"waist_um":w,"rayleigh_air_um":zr,"relay_magnification":p["relay_f2_mm"]/p["relay_f1_mm"],
                     "collimated_radius_mm":lam*f/(math.pi*w)/1000,"lateral_95_um":dx,
                     "facet_tilt_95_mrad":1000*lam/(math.pi*w)*math.sqrt(-math.log(eta)),
                     "axial_95_um":2*zr*math.sqrt(1/eta-1),"mirror_95_urad":1e6*dx/(2*f),
                     "eta_mirror_20urad":coupling(lam,w,w,dx=2*f*20e-6),
                     "eta_mirror_50urad":coupling(lam,w,w,dx=2*f*50e-6),"eta_joint_example":eta_joint,
                     "collection_zR_y_mm":math.pi*ny*p["collection_waist_um"]**2/lam/1000,
                     "pump_10pct_displacement_um":math.sqrt(-math.log(.90)*(p["collection_waist_um"]**2+2*p["pump_waist_um"]**2)/4)},
            "timing":rows,"coincidence_budget":rates}


if __name__ == "__main__":
    data=evaluate(json.loads((HERE/"design_inputs.json").read_text()))
    print(json.dumps(data,indent=2,sort_keys=True,allow_nan=False))
