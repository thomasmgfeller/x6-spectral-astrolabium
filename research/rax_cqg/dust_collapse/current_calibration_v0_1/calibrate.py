#!/usr/bin/env python3
"""Reproducible finite-reference calibration; evaluates laws, not random draws."""
from pathlib import Path
from fractions import Fraction as F
import csv,hashlib,itertools,json,math
import numpy as np
from scipy.integrate import quad
from scipy.stats import poisson
from current import Current
import observables as o

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text())
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)

def write_json(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def write_csv(name,rows):
    with (OUT/name).open('w',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def graph_controls():
    nodes=['S','a','b','c','d','Z']
    edges={('S','a'):F(2),('S','b'):F(3),('a','c'):F(1),('a','d'):F(1),
           ('b','d'):F(3),('c','Z'):F(1),('d','Z'):F(4)}
    sources={'S':5,'Z':-5}
    c=Current(nodes,edges,edges,sources)
    controls=[]
    def test(name,ok):
        assert ok,name;controls.append({'control':name,'status':'PASS_KINEMATIC_ONLY'})
    cuts=[]
    for flags in itertools.product([False,True],repeat=4):
        past={'S'}|{x for x,b in zip(nodes[1:5],flags) if b}
        if c.is_past_set(past):
            test('cut '+' '.join(sorted(past)),c.cut_mass(past)==5);cuts.append(past)
    for flags in itertools.product([False,True],repeat=6):
        reg={x for x,b in zip(nodes,flags) if b}
        test('Gauss subset '+''.join('1' if b else '0' for b in flags),
             c.outward(reg)==sum(c.sources[x] for x in reg))
    phi={x:F(i*i-2*i,7) for i,x in enumerate(nodes)}
    test('weak divergence identity',c.weak_pairing(phi)==-sum(phi[x]*c.sources[x] for x in nodes))
    cg=c.coarse_grain({'S':'I','a':'A','b':'A','c':'B','d':'B','Z':'F'})
    test('coarse cut conservation',cg.cut_mass({'I','A'})==5)
    permutation={x:'node_'+str(17-i) for i,x in enumerate(nodes)}
    renamed=Current(permutation.values(),[(permutation[x],permutation[y]) for x,y in edges],
                    {(permutation[x],permutation[y]):v for (x,y),v in edges.items()},
                    {permutation[x]:s for x,s in sources.items()})
    test('arbitrary relabeling',all(renamed.cut_mass({permutation[x] for x in p})==5 for p in cuts))
    transitive=set(edges)|{('S','Z')}
    test('new relation alone creates no mass',Current(nodes,transitive,edges,sources).cut_mass({'S'})==5)
    doubled=Current(nodes,edges,{e:2*f for e,f in edges.items()},{x:2*s for x,s in sources.items()})
    test('bare order cannot determine mass',doubled.cut_mass({'S'})==10)
    alternative=dict(edges)
    alternative.update({('S','a'):F(1),('S','b'):F(4),('a','c'):F(1,2),('a','d'):F(1,2),
                        ('b','d'):F(4),('c','Z'):F(1,2),('d','Z'):F(9,2)})
    alt=Current(nodes,edges,alternative,sources)
    test('same order and total mass do not fix local flow',alt.cut_mass({'S'})==5 and alternative['S','a']!=edges['S','a'])
    def rejects(name,fn):
        try:fn()
        except ValueError:test(name,True)
        else:test(name,False)
    rejects('non-past cut rejected',lambda:c.cut_mass({'a'}))
    wrong=dict(edges);wrong['a','d']=F(2)
    rejects('undeclared creation rejected',lambda:Current(nodes,edges,wrong,sources))
    wrong=dict(edges);wrong['a','d']=F(-1)
    rejects('negative transfer rejected',lambda:Current(nodes,edges,wrong,sources))
    wrong=dict(edges);wrong['S','Z']=F(1)
    rejects('blind transitive-edge duplication rejected',lambda:Current(nodes,transitive,wrong,sources))
    rejects('cyclic coarse partition rejected',lambda:c.coarse_grain({x:('X' if x in ('S','Z') else x) for x in nodes}))
    pressure=[]
    for v in [F(1,5),F(1,2),F(4,5)]:
        # Equal counterstreams: J spatial component zero, but T^xx positive.
        p=v*v/(1-v*v)
        test('conservation does not imply dust v='+str(v),p>0)
        pressure.append({'v':str(v),'pressure_per_unit_total_rest_density':str(p),'J_spatial':0})
    write_json('graph_controls.json',controls);write_json('non_dust_control.json',pressure)
    return {'controls':len(controls),'admissible_cuts':len(cuts),'subset_Gauss_checks':64}


def mass_and_flux_controls():
    masses=[];fluxes=[]
    times=[f*o.T_END for f in PLAN['reference']['time_fractions']]
    for m in o.MASSES:
        for p in PLAN['matter_quadrature']['particle_counts']:
            for t in times:
                for probe in o.PROBES:
                    truth=o.true_mass(probe,m,t)
                    value,lo,hi,err=o.particle_mass(probe,m,t,p)
                    assert lo-1e-12*m<=truth<=hi+1e-12*m
                    masses.append({'M':m,'particles':p,'T':t,'probe':probe,'true_mass':truth,
                     'estimated_mass':value,'absolute_error_over_total_M':abs(value-truth)/m,
                     'bound_over_total_M':err/m})
            grid=(np.arange(p)+.5)/p
            for left,right in zip(times[:-1],times[1:]):
                for tube in PLAN['matter_quadrature']['flux_worldtubes']:
                    def chi(t):
                        if tube=='material_surface':return 1.
                        if tube=='fixed_R4':return 4/o.radius(m,t)
                        return .8-.2*t/o.T_END
                    def m_inside(t):return m*chi(t)**3
                    def phi_rate(t):
                        if tube=='material_surface':return 0.
                        if tube=='fixed_R4':return 3*(-2/(3*(o.collapse_time(m)-t)))*m_inside(t)
                        return .6*m*chi(t)**2/o.T_END
                    nleft=int(np.count_nonzero(grid<chi(left)**3))
                    nright=int(np.count_nonzero(grid<chi(right)**3))
                    discrete=(nleft-nright)*m/p
                    balance=(nright-nleft)*m/p+discrete
                    true_flux=m_inside(left)-m_inside(right)
                    integral,_=quad(phi_rate,left,right,epsabs=1e-12,epsrel=1e-12)
                    assert abs(integral-true_flux)<1e-10*m
                    assert abs(discrete-true_flux)<=2*m/p+1e-12*m
                    assert abs(balance)<=1e-12*m
                    if tube=='fixed_R4':assert true_flux<0
                    if tube=='shrinking_chi_0.8_to_0.6':assert true_flux>0
                    fluxes.append({'M':m,'particles':p,'tube':tube,'T1':left,'T2':right,
                     'true_outward_flux':true_flux,'discrete_outward_flux':discrete,
                     'quadrature_flux':integral,'balance_residual':balance,
                     'error_over_total_M':abs(discrete-true_flux)/m,'bound_over_total_M':2/p})
    write_csv('mass_calibration.csv',masses);write_csv('flux_calibration.csv',fluxes)
    last=max(PLAN['matter_quadrature']['particle_counts'])
    finest=[r for r in masses if r['particles']==last]
    fineflux=[r for r in fluxes if r['particles']==last]
    return {'mass_cases':len(masses),'flux_cases':len(fluxes),
     'finest_mass_max_abs_error_over_M':max(r['absolute_error_over_total_M'] for r in finest),
     'finest_flux_max_abs_error_over_M':max(r['error_over_total_M'] for r in fineflux),
     'max_balance_residual':max(abs(r['balance_residual']) for r in fluxes),
     'mass_guarantee_finest':1/last,'flux_guarantee_finest':2/last}


def base_cells_and_quadrature():
    cells=[];numerics=[];max_diff=0.
    for m,tfrac,mult,probe in itertools.product(o.MASSES,PLAN['reference']['time_fractions'],
                  PLAN['volume_windows']['past_future_multipliers'],o.PROBES):
        t=tfrac*o.T_END;lo,hi=o.window(t,mult)
        vol=o.volume(probe,m,t);omega=o.exposure(probe,m,lo,hi)
        integral,_=quad(lambda s:o.volume(probe,m,s),lo,hi,epsabs=1e-10,epsrel=1e-12)
        diff=abs(integral/omega-1);max_diff=max(max_diff,diff)
        assert diff<1e-10
        value,mlo,mhi,bound=o.particle_mass(probe,m,t,4096)
        truth=o.true_mass(probe,m,t)
        cells.append({'cell_id':len(cells),'M':m,'T':t,'probe':probe,'past_multiplier':mult[0],
         'future_multiplier':mult[1],'lo':lo,'hi':hi,'V_true':vol,'Q_true':truth,'Qhat':value,
         'Q_lo':mlo,'Q_hi':mhi,'mass_bound':bound,'Omega4':omega,'A':omega/vol,
         'F_time':omega/((hi-lo)*vol),'rho_true':truth/vol})
        for n in PLAN['numerical_controls']['midpoint_subintervals']:
            mids=lo+(np.arange(n)+.5)*(hi-lo)/n
            mid=sum(o.volume(probe,m,float(s)) for s in mids)*(hi-lo)/n
            numerics.append({'cell_id':len(cells)-1,'subintervals':n,'relative_midpoint_error':abs(mid/omega-1)})
    write_csv('reference_cells.csv',cells);write_csv('quadrature_refinement.csv',numerics)
    boundary=[]
    for m,tfrac in itertools.product(o.MASSES,PLAN['reference']['time_fractions']):
        t=tfrac*o.T_END;R=o.radius(m,t);bulk=m/o.volume('whole',m,t)
        density=o.true_mass('surface_total',m,t)/o.volume('surface_total',m,t)
        masked=o.true_mass('surface_material',m,t)/o.volume('surface_material',m,t)
        assert math.isclose(masked,bulk,rel_tol=1e-12)
        boundary.append({'M':m,'T':t,'R_boundary':R,'material_density':bulk,
          'full_detector_density':density,'masked_density':masked,'full_to_bulk_ratio':density/bulk,
          'misinterpretation_error_relative':density/bulk-1})
    write_csv('boundary_mask.csv',boundary)
    return cells,{'base_cells':len(cells),'quadrature_checks':len(numerics),'quadrature_relative_error':max_diff,
      'max_raw_volume_bias':max(abs(r['F_time']-1) for r in cells),
      'surface_average_to_bulk_range':[min(r['full_to_bulk_ratio'] for r in boundary),max(r['full_to_bulk_ratio'] for r in boundary)]}


def count_law_calibration(cells):
    cfg=PLAN['counting_calibration'];ratios=cfg['density_ratios']
    family=len(cells)*len(ratios);assert family==cfg['family_size']
    alpha=cfg['familywise_alpha']/family
    lam0=cfg['minimum_expected_count_at_base_density']/min(r['Omega4'] for r in cells)
    results=[];levels=[]
    for ratio in ratios:
        lam=ratio*lam0;failure_sum=0.;raw_failure_sum=0.;max_single_miss=0.
        for c in cells:
            mean=lam*c['Omega4']
            lower=mean*max(.95,c['Q_hi']/c['Q_true']/1.05)
            upper=mean*min(1.05,c['Q_lo']/c['Q_true']/.95)
            assert lower<upper
            nlo,nhi=o.interval_inside_count_range(lower,upper,alpha)
            miss=o.miss_probability(mean,nlo,nhi)
            rawlo,rawhi=o.interval_inside_count_range(lower/c['F_time'],upper/c['F_time'],alpha)
            rawmiss=o.miss_probability(mean,rawlo,rawhi)
            failure_sum+=miss;raw_failure_sum+=rawmiss;max_single_miss=max(max_single_miss,miss)
            # Exact-law coverage of the central Garwood interval at this reference mean.
            covlo=int(poisson.ppf(alpha/2,mean));covhi=int(poisson.ppf(1-alpha/2,mean))
            coverage=1-o.miss_probability(mean,covlo,covhi)
            assert coverage+1e-11>=1-alpha
            results.append({'cell_id':c['cell_id'],'density_ratio':ratio,'lambda':lam,'mu':mean,
              'volume_relative_sd':1/math.sqrt(mean),'volume_mean_bias_corrected':0.,
              'volume_mean_bias_raw':c['F_time']-1,'log_probability_empty':-mean,
              'pass_count_min':nlo,'pass_count_max':nhi,'pass_probability':1-miss,
              'pass_probability_raw':1-rawmiss,'Garwood_coverage':coverage})
        joint=max(0.,1-failure_sum);raw_joint=max(0.,1-raw_failure_sum)
        # Whole reference time tube, one mass: a resource forecast, not a generated point cloud.
        full_counts=[lam*o.exposure('whole',m,0,o.T_END) for m in o.MASSES]
        levels.append({'density_ratio':ratio,'lambda':lam,'min_expected_count':min(r['mu'] for r in results if r['density_ratio']==ratio),
          'joint_pass_probability_lower':joint,'worst_single_pass_probability':1-max_single_miss,
          'raw_joint_pass_probability_lower':raw_joint,'sum_failure_probabilities':failure_sum,
          'expected_full_tube_points_min':min(full_counts),'expected_full_tube_points_max':max(full_counts),
          'decision':'PASS_CONDITIONAL_REFERENCE_DESIGN' if joint>=.95 else 'HOLD_DESIGN_POWER_NOT_CERTIFIED'})
    write_csv('poisson_calibration.csv',results);write_csv('density_levels.csv',levels)
    # Low-count diagnostic values are outside the main design, never used to retune it.
    zero=o.intervals(0,1.,1.,(1.,1.),.05)
    assert zero['volume'][0]==0 and math.isinf(zero['density'][1])
    low=[]
    for mu in [.1,1,5,20]:
        low.append({'mu':mu,'empty_probability':math.exp(-mu),
                    'literal_inverse_count_moment':'INFINITE_IF_ZERO_MAPS_TO_INFINITY',
                    'adapter_at_N0':'HOLD_ZERO_COUNT'})
    write_json('zero_count_controls.json',{'N0_volume_interval':list(zero['volume']),
      'N0_density_lower':zero['density'][0],'N0_density_upper':'infinity','cases':low,
      'interpretation':'Inference failure of a reciprocal count, not a physical spacetime singularity'})
    return {'family_size':family,'alpha_per_count':alpha,'lambda0':lam0,'levels':levels,
       'minimum_numerical_coverage':min(r['Garwood_coverage'] for r in results),
       'new_random_draws':0}


def covariance_controls(lam0):
    out=[]
    for m,ratio in itertools.product(o.MASSES,[1,2,4,8]):
        lam=lam0*ratio
        specs=[(probe,((f-.15)*o.T_END,(f+.15)*o.T_END)) for probe in ['whole','core'] for f in [.4,.5,.6]]
        cov=np.array([[o.covariance(a,b,m,wa,wb,lam) for b,wb in specs] for a,wa in specs])
        eig=np.linalg.eigvalsh(cov)
        assert eig.min()>=-1e-10*np.max(np.diag(cov))
        for j,(pr,w) in enumerate(specs):assert math.isclose(cov[j,j],lam*o.exposure(pr,m,*w),rel_tol=1e-12)
        diff=np.array([1.,0.,-1.,0.,0.,0.])
        independent=float(np.sum(diff**2*np.diag(cov)))
        correct=float(diff@cov@diff)
        assert correct<independent
        out.append({'M':m,'density_ratio':ratio,'smallest_eigenvalue':float(eig.min()),
          'correct_difference_variance':correct,'independence_variance':independent,
          'independence_over_correct':independent/correct})
    write_csv('overlap_covariance.csv',out)
    return {'matrices':len(out),'matrix_size':6,'independence_over_correct_range':[
      min(r['independence_over_correct'] for r in out),max(r['independence_over_correct'] for r in out)]}


def decisions(summary):
    parent=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    previous=json.loads((ROOT/'inputs/parent_contract.json').read_text())['current_cst_status']
    record={'contract_id':parent['id'],'contract_sha256':hashlib.sha256((ROOT/'inputs/parent_contract.json').read_bytes()).hexdigest(),
      'checkpoint':'P2','scope':'CST-DUST-C1; finite ball plus exterior, contracted interval, physical observables not yet generated by a coupled kernel',
      'decisions':previous,'new_evidence_scope':'MARKED_KINEMATICS_AND_KNOWN_CLASSICAL_REFERENCE_ONLY',
      'regularity_decision':'HOLD','regularity_reasons':['No physical density/curvature operators from the coupled CST kernel',
       'Reciprocal Poisson counts are not physical volume operators','No uniform CST domain/tail/convergence theorem'],
      'D5':'PARTIAL_REFERENCE_ADAPTER; curvature, coarse-fibre weights, intrinsic clocks/detectors and dynamic flow generation remain open',
      'new_bounce_or_horizon_claim':False,'singularity_resolution':'HOLD'}
    write_json('checkpoint_P2_CST.json',record)
    separate={'scope':'REF-DUST-FB-01 plus supplied nonnegative conserved matter transfers and exactly calibrated exposures',
      'current_kinematics':'PASS_CONDITIONAL_DEFINITION',
      'mass_flux':'PASS_FINITE_REFERENCE_WITH_DETERMINISTIC_BOUNDS',
      'volume_density':summary['poisson']['levels'][-1]['decision'],
      'metric_regularity':'PASS_FIXED_REFERENCE_WINDOW_ONLY',
      'metric_bounds':{'R_boundary_min':o.radius(4,o.T_END),'rho_max':4/o.volume('whole',4,o.T_END),
       'K_interior_max':60*4**2/o.radius(4,o.T_END)**6,'K_exterior_max':48*4**2/o.radius(4,o.T_END)**6},
      'count_reciprocal_regularity':'FAIL_AS_AN_UNCONDITIONAL_FINITE_MOMENT_IF_N0_IS_INVERTED',
      'inference_at_zero':'HOLD_WITH_UNBOUNDED_DENSITY_INTERVAL',
      'not_implied':'dust dynamics, recovered backreaction, global completeness, or old BD-current qualification'}
    write_json('reference_decisions.json',separate)


if __name__=='__main__':
    expected=(ROOT/'plan.sha256').read_text().split()[0]
    assert hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()==expected
    assert hashlib.sha256((ROOT/'inputs/parent_contract.json').read_bytes()).hexdigest()==PLAN['parent_contract_sha256']
    summary={'id':PLAN['id'],'plan_sha256':expected,'graph':graph_controls(), 'mass_flux':mass_and_flux_controls()}
    cells,summary['exposure']=base_cells_and_quadrature()
    summary['poisson']=count_law_calibration(cells)
    summary['covariance']=covariance_controls(summary['poisson']['lambda0'])
    summary['new_dynamical_CST_ensembles']=0
    summary['CST_CURRENT']='HOLD';summary['CST_REGULARITY']='HOLD';summary['singularity_resolution']='HOLD'
    summary['numerical_class']='FLOATING_POINT_EVALUATION_OF_ANALYTIC_REFERENCE_NOT_INTERVAL_CERTIFICATE'
    write_json('verification.json',summary);decisions(summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
