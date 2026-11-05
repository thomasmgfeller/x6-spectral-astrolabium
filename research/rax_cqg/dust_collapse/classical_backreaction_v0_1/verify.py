"""Reduced dust dynamics and audit of two archived CST carriers.

Run: python3 verify.py. Numerical diagnostics use numpy/scipy, not interval bounds.
No CST orders are generated and no physical continuum claim is inferred.
"""
from pathlib import Path
from fractions import Fraction
import cmath
import csv
import hashlib
import json
import math
import platform

import numpy as np
import scipy
from scipy.fft import dst, idst

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text())


def check_inputs():
    digest = hashlib.sha256((ROOT / 'plan.json').read_bytes()).hexdigest()
    require(digest == (ROOT / 'PLAN_SHA256').read_text().split()[0], 'Plan changed')
    provenance = read_json(ROOT / 'provenance.json')
    for path, item in provenance['files'].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == item['sha256'], path)
    return digest


def classical(plan):
    """Integrate acceleration in a, independently compare with affine sqrt(V)."""
    rows = []
    kappa, q0, tend = 1., plan['reference']['q0'], plan['reference']['T_end']
    for mass in plan['reference']['masses_classical_central']:
        exact_q = q0 - 2 * math.sqrt(kappa * mass) * tend
        for steps in plan['reference']['rk_steps']:
            a0 = q0 ** (2 / 3)
            y = np.array([a0, -4 * math.sqrt(kappa * mass) * a0 / (3 * q0)])
            dt = tend / steps
            max_constraint = 0.
            def rhs(state):
                a, adot = state
                return np.array([adot, -8 * kappa * mass / (9 * a * a)])
            for _ in range(steps):
                k1 = rhs(y)
                k2 = rhs(y + dt * k1 / 2)
                k3 = rhs(y + dt * k2 / 2)
                k4 = rhs(y + dt * k3)
                y += dt * (k1 + 2*k2 + 2*k3 + k4) / 6
                a, adot = y
                max_constraint = max(max_constraint, abs(9*a*adot**2/(16*kappa)-mass))
            rows.append(dict(M=mass, steps=steps, q_numeric=float(y[0]**1.5),
                             q_exact=exact_q, q_error=abs(float(y[0]**1.5)-exact_q),
                             max_mass_constraint_error=max_constraint))
    require(max(r['q_error'] for r in rows) < plan['tolerances']['rk_q_max_abs'], 'RK dust dynamics')
    for mass in plan['reference']['masses_classical_central']:
        errors = [r['q_error'] for r in rows if r['M'] == mass]
        require(errors[-1] < errors[0], 'RK refinement failed')
    return rows


def stationary_action():
    """Exact rational first variations on a nonuniform time grid."""
    F = Fraction
    times = list(map(F, ('0', '1/10', '2/5', '1/2')))
    results = []
    for p in (F(1,2), F(1), F(2)):
        q = [4 - 2*p*t for t in times]
        v = [(b-a)/(tb-ta) for a,b,ta,tb in zip(q,q[1:],times,times[1:])]
        gradients = [(v[j]-v[j-1])/2 for j in range(1,len(v))]
        require(all(g == 0 for g in gradients), 'Stationary action')
        # Local finite variation changes S by the quadratic term, not a linear term.
        eps = F(1,1000)
        def action(path):
            return -sum((b-a)**2/(tb-ta)/4 for a,b,ta,tb in zip(path,path[1:],times,times[1:]))
        perturbed = q.copy(); perturbed[1] += eps
        exact_change = -eps**2*(1/(times[1]-times[0])+1/(times[2]-times[1]))/4
        require(action(perturbed)-action(q) == exact_change, 'First variation perturbation')
        results.append({'p':str(p),'M':str(p*p),'gradient':list(map(str,gradients)),
                        'action_change':str(exact_change)})
    return results


def free_gaussian(q, t, q0, p, hbar, sigma2):
    # Exact full-line solution for H=-p^2 (kappa=1), then use images below.
    denom = 1 - 1j*hbar*t/sigma2
    centre = q0 - 2*p*t
    return ((2*np.pi*sigma2)**(-.25) / np.sqrt(denom)
            * np.exp(-(q-centre)**2/(4*sigma2*denom)
                     + 1j*p*(q-q0)/hbar + 1j*p*p*t/hbar))


def semiclassical(plan):
    cfg, tol = plan['reference'], plan['tolerances']
    rows = []
    for n in cfg['interior_grid_points']:
        L, q0 = cfg['dirichlet_interval_L'], cfg['q0']
        dq = L/(n+1)
        q = dq*np.arange(1,n+1)
        k = np.pi*np.arange(1,n+1)/L
        for mass in cfg['masses_classical_central']:
            p = np.sqrt(mass)
            for hbar in cfg['hbar_sequence']:
                s2 = hbar/2
                overlap = np.exp(-q0*q0/(2*s2)-2*s2*p*p/(hbar*hbar))
                norm_exact = np.sqrt(1-overlap)
                initial = (free_gaussian(q,0,q0,p,hbar,s2)-free_gaussian(-q,0,q0,p,hbar,s2))/norm_exact
                coefficients = dst(initial,type=1,norm='ortho')
                mass_numeric = float(dq*np.sum(abs(coefficients)**2*(hbar*k)**2))
                for t in cfg['times']:
                    psi = idst(coefficients*np.exp(1j*hbar*k*k*t),type=1,norm='ortho')
                    analytic = (free_gaussian(q,t,q0,p,hbar,s2)-free_gaussian(-q,t,q0,p,hbar,s2))/norm_exact
                    norm = float(dq*np.sum(abs(psi)**2))
                    centre = q0-2*p*t
                    variance = s2 + (hbar*t)**2/s2
                    mean_q = float(dq*np.sum(q*abs(psi)**2))
                    mean_v = float(dq*np.sum(q*q*abs(psi)**2))
                    row = dict(N=n,hbar=hbar,M_central=mass,M_mean_target=mass+hbar/2,
                               M_mean_numeric=mass_numeric,T=t,norm_error=abs(norm-1),
                               analytic_L2=float(np.sqrt(dq*np.sum(abs(psi-analytic)**2))),
                               q_mean=mean_q,q_classical=float(centre),q_error=abs(mean_q-centre),
                               V_mean=mean_v,V_classical=float(centre**2),
                               V_packet_prediction=float(centre**2+variance),
                               V_packet_error=abs(mean_v-centre**2-variance),
                               V_classical_bias=mean_v-centre**2,
                               sigma_q=float(np.sqrt(variance)),boundary_z=float(centre/np.sqrt(variance)))
                    require(row['norm_error'] < tol['spectral_norm_error'], 'Packet norm')
                    require(row['analytic_L2'] < tol['spectral_vs_analytic_L2'], 'Spectral vs image solution')
                    require(row['V_packet_error'] < tol['spectral_volume_moment_abs'], 'Volume moment')
                    require(abs(mass_numeric-row['M_mean_target']) < tol['spectral_mass_expectation_abs'], 'Mass spectrum')
                    rows.append(row)
    # Convergence is to central classical mass; each normalized packet has finite mass spread.
    for n in cfg['interior_grid_points']:
        for mass in cfg['masses_classical_central']:
            last = [r for r in rows if r['N']==n and r['M_central']==mass and r['T']==cfg['T_end']]
            for a,b in zip(last,last[1:]):
                require(abs(a['V_classical_bias']/b['V_classical_bias']-2) < 1e-7, 'hbar convergence')
    return rows


def carrier_audit():
    rows, counts = [], {}
    dt = .4
    first_slope = ((4/5)**1.5-1)/dt
    for family in ('development','holdout'):
        with (ROOT/'inputs/history_weighting'/f'{family}.csv').open() as f:
            paths = sorted({tuple(map(int,r['path'].split('-'))) for r in csv.DictReader(f)})
        counts[family] = len(paths)
        for w in paths:
            q = np.array([(a/5)**1.5 for a in w])
            slopes = np.diff(q)/dt
            residual = np.diff(slopes)
            rows.append(dict(family=family,path='-'.join(map(str,w)),
                             max_velocity_change=float(max(abs(residual))),
                             relative_slope_error_before_singularity=float(max(abs(slopes[:3]-first_slope))/abs(first_slope)),
                             q_at_T08=float(q[2]),q_at_T12=float(q[3])))
    require(counts=={'development':27,'holdout':17}, 'Carrier size')
    return dict(counts=counts,q1=(4/5)**1.5,initial_slope=first_slope,
                M_for_kappa1=first_slope**2/4,T_singularity=-1/first_slope,
                classical_q_at_T08=1+.8*first_slope,classical_q_at_T12=1+1.2*first_slope,
                final_sampling_T=1.6,all_paths_nonstationary=all(r['max_velocity_change']>0 for r in rows),
                warning='Finite off-shell paths need not individually be stationary. This audit is not a no-go theorem for an oscillatory path integral.',rows=rows)


def family_C_replay(plan):
    """Independent binary64 polynomial evaluation against archived interval midpoints."""
    tables={}
    for filename, tag, field in [('symmetry_orbit.csv','measure','weight'),('growth.csv','scenario','conditional_weight')]:
        with (ROOT/'inputs/family_C'/filename).open() as f:
            for r in csv.DictReader(f):
                name=r[tag]
                if name not in ('symmetry','orbit','p_half_flat'): continue
                tables.setdefault(name,[]).append((tuple(int(r[k]) for k in ('k','signature','h','residue')),Fraction(r[field])))
    archive=read_json(ROOT/'inputs/family_C/amplitudes.json')['results']
    delta=(48/math.pi)**.25-(24/math.pi)**.25
    results={}; max_replay=0.
    for name,table in tables.items():
        total=sum(w for _,w in table)
        results[name]={}
        for mode in ('full','g_zero','blind'):
            scores={}; vectors={}
            for eta in (1,2,4):
                bins=np.zeros((2,5),dtype=complex)
                for (width,sig,h,r),w in table:
                    phase=(0 if mode=='g_zero' else 4*math.pi*r/5)-(0 if mode=='blind' else eta*delta*h)
                    bins[int(width!=1),(0,1,2,4,7).index(sig)] += float(w/total)*cmath.exp(1j*phase)
                u,v=bins; vectors[eta]=bins.ravel(); norm=float(np.vdot(u,u).real+np.vdot(v,v).real)
                scores[str(eta)]={'q23':float(np.vdot(v,v).real/norm),'epsilon':float(2*abs(np.vdot(u,v))/norm)}
                for field,value in scores[str(eta)].items():
                    mid=float(archive[name][mode]['scores'][str(eta)][field].strip('[]').split(' +/- ')[0])
                    max_replay=max(max_replay,abs(value-mid))
            change=scores['4']['q23']-scores['1']['q23']
            a,b=vectors[1],vectors[4]
            distance=float(sum(abs(a[i]*b[j]-a[j]*b[i])**2 for i in range(10) for j in range(i+1,10))
                           /(np.vdot(a,a).real*np.vdot(b,b).real))
            results[name][mode]={'scores':scores,'delta_q23':change,'projective_distance':distance}
            if mode=='blind':require(change==0. and np.array_equal(a,b),'Mass-blind null')
            else:
                require(distance>0.,'Mass response disappeared')
                mid=float(archive[name][mode]['distance'].strip('[]').split(' +/- ')[0])
                max_replay=max(max_replay,abs(distance-mid))
    require(max_replay<plan['tolerances']['family_C_replay_abs'],'Archived mass results mismatch')
    return {'results':results,'max_archived_midpoint_error':max_replay,
            'interval_certification_repeated':False,
            'physical_warning':'g_zero sets the phase coefficient to zero; it is NOT the physical G->0 limit at fixed hbar and ell.'}


def run():
    digest=check_inputs();plan=read_json(ROOT/'plan.json')
    return {'plan_sha256':digest,'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'stationary_action':stationary_action(),'classical_RK':classical(plan),
            'semiclassical':semiclassical(plan),'old_volume_carrier':carrier_audit(),
            'family_C':family_C_replay(plan),
            'decisions':{'reference_classical':'PASS_CONDITIONAL','reference_semiclassical':'PASS_FINITE_BENCHMARK',
                         'reference_mass_response':'PASS_CONDITIONAL','full_CST_classical_limit':'HOLD',
                         'full_CST_backreaction':'HOLD','singularity_resolution':'NOT_ESTABLISHED','new_bounce_test':'NOT_RUN'}}


if __name__=='__main__':
    result=run();out=ROOT/'results';out.mkdir(exist_ok=True)
    (out/'verification.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for field in ('classical_RK','semiclassical'):
        with (out/f'{field}.csv').open('w',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=list(result[field][0]));wr.writeheader();wr.writerows(result[field])
    print(json.dumps({'decisions':result['decisions'],
                      'max_RK_q_error':max(r['q_error'] for r in result['classical_RK']),
                      'max_spectral_L2':max(r['analytic_L2'] for r in result['semiclassical']),
                      'max_V_packet_error':max(r['V_packet_error'] for r in result['semiclassical']),
                      'family_C_replay_error':result['family_C']['max_archived_midpoint_error']},indent=2))
