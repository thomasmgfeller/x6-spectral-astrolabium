"""Referenzwerte und aktueller Zulassungsbefund für M=1, Zähldichte lambda0."""
import csv
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from uhrtest import require

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
META = json.loads((ROOT / 'quellen.json').read_bytes())


def source_path(name):
    return REPO / META['files'][name]['path']


def inputs():
    for name, source in META['files'].items():
        body = source_path(name).read_bytes()
        blob = b'blob ' + str(len(body)).encode() + bytes([0]) + body
        require(hashlib.sha1(blob).hexdigest() == source['git_blob'], 'Quelldatei verändert: ' + name)
    return META['commit']


def enclosed(tube, x):
    if tube == 'material_surface':
        return Q(1)
    if tube == 'fixed_R4':
        return Q(2,5)**3 / (1-x/4)**2
    if tube == 'shrinking_chi_0.8_to_0.6':
        return (Q(4,5)-x/5)**3
    raise ValueError(tube)


def run():
    commit = inputs()
    plan = json.loads(source_path('plan.json').read_bytes())
    current = json.loads(source_path('current_plan.json').read_bytes())
    eligibility = json.loads(source_path('eligibility.json').read_bytes())
    require(eligibility['execution']=='NOT_RUN' and not eligibility['physical_pass']
            and eligibility['decision']=='HOLD_NOT_ELIGIBLE' and eligibility['reasons'],
            'Zulassung hat sich geändert: neuer Vertrag erforderlich')
    require(plan['physical_refinement']['density_ratios'][0] == 1 and plan['family']['total'] == 524,
            'anderer P3-Vertrag')
    times = list(map(Q, plan['reference']['time_fractions']))
    tubes = current['matter_quadrature']['flux_worldtubes']
    rows = []
    tol = plan['primary_tolerances']
    def add(family, quantity, start, end, target, tolerance, scale):
        rows.append(dict(family=family, observable=quantity, x_start=str(start), x_end=str(end),
                         classical_reference=target, tolerance=str(Q(str(tolerance))),
                         error_scale=scale, physical_value=None, status="NOT_RUN"))

    with source_path('reference_comparisons.csv').open(newline='') as f:
        ode = {(Q(r['x']),r['observable']): (Q(r['ODE_enclosure_lo']),Q(r['ODE_enclosure_hi']))
               for r in csv.DictReader(f) if Q(r['M'])==1 and int(r['steps'])==128}
    for x in times:
        s = 1-x/4
        radius_lo, radius_hi = ode[x,'r']
        require(0 < radius_lo and radius_lo**3 <= s*s <= radius_hi**3, 'Radius ausserhalb der Hülle')
        add('dynamics','r',x,x,f'({s*s})^(1/3)',tol['R'],'abs(reference)')
        for obs, val, key in [('rho_over_rho0',1/s**2,'rho'),
                              ('H_times_Tend',-1/(6*s),'H'),
                              ('acceleration_times_Tend_squared',-1/(72*s**2),'a_ddot_over_a')]:
            lo,hi = ode[x,obs]
            require(lo <= val <= hi, 'ODE-Hülle: '+obs)
            add('dynamics',obs,x,x,str(val),tol[key],'abs(reference)')
        add('mass','whole_ball_mass',x,x,'1',tol['mass_or_flux_over_M'],'M')

    with source_path('flux_calibration.csv').open(newline='') as f:
        archive = [r for r in csv.DictReader(f) if Q(r['M'])==1 and int(r['particles'])==4096]
    require(len(archive)==12,'Anzahl Flussreferenzen')
    boundaries = sorted({Q(r[field]) for r in archive for field in ('T1','T2')})
    require(len(boundaries)==len(times) and boundaries[0]==0,'Fluss-Zeitpunkte')
    require(all(abs(t/boundaries[-1]-x) < Q(1,10**13) for t,x in zip(boundaries,times)), 'Zeitzuordnung')
    by_key = {(r['tube'],Q(r['T1']),Q(r['T2'])):Q(r['true_outward_flux']) for r in archive}
    for i,(a,b) in enumerate(zip(times,times[1:])):
        for tube in tubes:
            flux = enclosed(tube,a)-enclosed(tube,b)
            published = by_key[tube,boundaries[i],boundaries[i+1]]
            require(abs(flux-published) < Q(1,10**13), 'Flussvorzeichen oder Weltrohr')
            add('side_flux',tube,a,b,str(flux),tol['mass_or_flux_over_M'],'M')
    add('initial_velocity','dr/dx',0,0,'-1/6',tol['initial_velocity_and_mass_response'],'abs(reference)')
    keys = [(r['observable'],r['x_start'],r['x_end']) for r in rows]
    require(len(set(keys))==len(keys)==38 and len(ode)==20, 'Kohorte unvollständig')
    return dict(source_commit=commit, mass='1', density_ratio=1, familywise_alpha='1/20',
                alpha_per_comparison=str(Q(1,20*plan['family']['total'])),
                physical_eligibility=eligibility, physical_comparisons_performed=0,
                physical_runtime_estimate_seconds=None, rows=rows)
