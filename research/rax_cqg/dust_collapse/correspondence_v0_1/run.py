#!/usr/bin/env python3
"""Predeclared correspondence eligibility and finite classical reference audit."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import csv,copy,hashlib,importlib.util,json,math,platform
from importlib.metadata import version
from intervals import I,cube_root_rational
from acceptance import interval_decision,complete_comparison,matching_guard,cst_eligibility

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text())
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
MASSES=[F(x) for x in PLAN['reference']['masses']]
TIMES=[F(x) for x in PLAN['reference']['time_fractions']]
SQRT_M={F(1,4):F(1,2),F(1):F(1),F(4):F(2)}


def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')


def csv_write(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def observables(r,u,k):
    return {'r':r,'rho_over_rho0':1/(r**3),'H_times_Tend':u/r,
            'acceleration_times_Tend_squared':-I.fraction(k)/(r**3)}


def exact(m,x):
    q=SQRT_M[m]/4;s=1-q*x;r=cube_root_rational(s*s,PLAN['numerical_reference']['root_bisections'])
    u=I.fraction(-SQRT_M[m]/6)*r/I.fraction(s)
    return observables(r,u,m/72)


def reference_audit():
    rows=[];levels=[];states={};energy=[]
    for n in PLAN['numerical_reference']['steps']:
        relative_bounds=[];decisions=[];all_domain=True
        for m in MASSES:
            k=m/72;h=I.fraction(F(1,n));B=I.fraction(F(125,27)*k)
            r,u=I(1),I.fraction(-SQRT_M[m]/6);E=I(0)
            for step in range(n+1):
                require(r.lo>=Decimal('0.6') and r.hi<=Decimal('1.05')
                        and u.lo>=Decimal('-0.5') and u.hi<=0,'Euler iterate outside declared domain')
                x=F(step,n)
                if x in TIMES:
                    target=exact(m,x);nominal=observables(r,u,k)
                    enclosed=observables(r.inflate(E),u.inflate(E),k)
                    for name,truth in target.items():
                        require(enclosed[name].contains(truth),'analytic ODE not enclosed: '+name)
                        error=(enclosed[name]-truth)/truth.absolute()
                        actual=(nominal[name]-truth)/truth.absolute()
                        decision=interval_decision(error,'0.005')
                        rows.append({'steps':n,'M':str(m),'x':str(x),'observable':name,
                            'reference_lo':str(truth.lo),'reference_hi':str(truth.hi),
                            'Euler_interval_lo':str(nominal[name].lo),'Euler_interval_hi':str(nominal[name].hi),
                            'ODE_enclosure_lo':str(enclosed[name].lo),'ODE_enclosure_hi':str(enclosed[name].hi),
                            'relative_error_lo':str(error.lo),'relative_error_hi':str(error.hi),
                            'actual_Euler_error_upper':str(actual.absolute().hi),
                            'global_state_error_upper':str(E.hi),'numerical_cap_decision':decision})
                        relative_bounds.append(float(error.absolute().hi));decisions.append(decision)
                        states[n,m,x,name]=(enclosed[name],truth)
                    energy_res=(u**2-2*I.fraction(k)/r)/(2*I.fraction(k))
                    energy.append({'steps':n,'M':str(m),'x':str(x),'constraint_residual_lo':str(energy_res.lo),
                                   'constraint_residual_hi':str(energy_res.hi),'scope':'Euler diagnostic only'})
                if step<n:
                    r,u=r+h*u,u-h*I.fraction(k)/(r**2)
                    E=(1+h)*E+B*h*h/2
        levels.append({'steps':n,'comparisons':len(decisions),'passed_numerical_cap':decisions.count('PASS'),
                       'max_relative_enclosure_error':max(relative_bounds),
                       'decision':'PASS_NUMERICAL_REFERENCE_ONLY' if set(decisions)=={'PASS'} else 'HOLD_NUMERICAL_CAP_NOT_MET'})
    comparison=[];n1,n2=PLAN['numerical_reference']['steps'][-2:]
    for m in MASSES:
        for x in TIMES:
            for name in exact(m,x):
                a,t=states[n1,m,x,name];b,_=states[n2,m,x,name]
                error=(a-b)/t.absolute();d=interval_decision(error,'0.025')
                comparison.append({'M':str(m),'x':str(x),'observable':name,'relative_difference_lo':str(error.lo),
                                   'relative_difference_hi':str(error.hi),'decision':d,
                                   'scope':'NUMERICAL_STEPS_ONLY_NOT_PHYSICAL_DENSITY'})
    csv_write('reference_comparisons.csv',rows);csv_write('numerical_levels.csv',levels)
    csv_write('numerical_last_two.csv',comparison);csv_write('Euler_constraint_diagnostic.csv',energy)
    dump('numerical_reference_decision.json',{'scope':'Inserted classical ODE on fixed common physical time interval',
        'levels':levels,'last_two_comparisons':len(comparison),'last_two_pass':all(r['decision']=='PASS' for r in comparison),
        'exact_ODE_enclosed':True,'roundoff_control':'outward Decimal arithmetic for rational operations and exact rational root bisection',
        'no_physical_density_evolution':True})
    return levels


def stencil(i):
    h=F(1,4)
    if i==0:return [(0,-3/(2*h)),(1,2/h),(2,-1/(2*h))],[(0,1/h**2),(1,-2/h**2),(2,1/h**2)]
    if i==4:return [(2,1/(2*h)),(3,-2/h),(4,3/(2*h))],[(2,1/h**2),(3,-2/h**2),(4,1/h**2)]
    return [(i-1,-1/(2*h)),(i+1,1/(2*h))],[(i-1,1/h**2),(i,-2/h**2),(i+1,1/h**2)]


def sensitivity(m,i,eps):
    q=SQRT_M[m]/4;v=[(1-q*x)**2 for x in TIMES];w1,w2=stencil(i)
    d1=sum(w*v[j] for j,w in w1);d2=sum(w*v[j] for j,w in w2)
    q1=d1/v[i];q2=d2/v[i]
    H=q1/3;A=q2/3-F(2,9)*q1*q1
    s1=sum(abs(w)*v[j] for j,w in w1)/v[i]
    s2=sum(abs(w)*v[j] for j,w in w2)/v[i]
    f=eps/(1-eps);b1=f*(s1+abs(q1));b2=f*(s2+abs(q2))
    hbound=b1/(3*abs(H));abound=(b2/3+F(2,9)*(2*abs(q1)*b1+b1*b1))/abs(A)
    return hbound,abound


def derivative_budget():
    # Exact rational propagation of fixed simultaneous relative volume errors.
    cells=[];fixed=[]
    for raw in PLAN['volume_derivative_budget']['fixed_relative_volume_errors']:
        eps=F(str(raw));allH=[];allA=[]
        for m in MASSES:
            for i,x in enumerate(TIMES):
                hb,ab=sensitivity(m,i,eps);allH.append(hb);allA.append(ab)
                cells.append({'epsilon':str(eps),'M':str(m),'x':str(x),'H_relative_bound':str(hb),
                    'A_relative_bound':str(ab),'H_bound_decimal':float(hb),'A_bound_decimal':float(ab)})
        fixed.append({'epsilon':str(eps),'epsilon_decimal':float(eps),'max_H_bound':float(max(allH)),
                      'max_A_bound':float(max(allA)),'full_5_percent_sufficient':max(allH+allA)<=F(1,20),
                      'sampling_2_percent_sufficient':max(allH+allA)<=F(1,50)})
    csv_write('derivative_exact_bounds.csv',cells);csv_write('derivative_fixed_epsilon.csv',fixed)
    spec=importlib.util.spec_from_file_location('inherited_observables',ROOT/'inputs/current_observables.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    inherited=json.loads((ROOT/'inputs/current_verification.json').read_text())
    lam0=inherited['poisson']['lambda0'];exposures=[]
    for m in MASSES:
        for x in TIMES:
            t=float(x)*prior.T_END;lo,hi=prior.window(t,(1,1))
            exposures.append(prior.exposure('whole',float(m),lo,hi))
    minOmega=min(exposures);J=PLAN['volume_derivative_budget']['event_family'];alpha=.05
    log=math.log(2*J/alpha);levels=[]
    for ratio in [1,2,4,8]:
        mu=ratio*lam0*minOmega
        eps=(log/3+math.sqrt(log*log/9+2*mu*log))/mu
        # Inflate the decimal approximation before rational sensitivity evaluation.
        epsF=F(str(math.nextafter(eps,math.inf)))
        bounds=[sensitivity(m,i,epsF) for m in MASSES for i in range(5)]
        maxH=max(b[0] for b in bounds);maxA=max(b[1] for b in bounds)
        levels.append({'prior_density_ratio':ratio,'min_mu_whole_window':mu,'sufficient_common_epsilon':eps,
            'max_H_relative_bound':float(maxH),'max_A_relative_bound':float(maxA),
            'certification':'SUFFICIENT_BOUND_PASSES' if max(maxH,maxA)<=F(1,50) else 'HOLD_SUFFICIENT_BOUND_TOO_WIDE'})
    csv_write('inherited_density_diagnostic.csv',levels)
    resources=[]
    for e in [F(1,200000),F(1,1000000)]:
        eps=float(e);mu=2*(1+eps/3)*log/(eps*eps);lam=mu/minOmega
        expected=[lam*prior.exposure('whole',float(m),0,prior.T_END) for m in MASSES]
        resources.append({'epsilon':str(e),'sufficient_min_mu':mu,'sufficient_lambda':lam,
            'ratio_to_prior_lambda0':lam/lam0,'expected_full_tube_min':min(expected),
            'expected_full_tube_max':max(expected),'run':'NOT_RUN_RESOURCE_FORECAST_ONLY'})
    dump('derivative_budget.json',{'fixed_error_results':fixed,'prior_density_diagnostic':levels,'resources':resources,
        'scope':'conditional whole-volume finite-difference adapter; exactly calibrated exposure, no other error sources',
        'not_a_necessary_lower_bound':True,'not_a_physical_correspondence_test':True,
        'finite_difference_reference_bias':0,'why_zero':'reference volume is quadratic in the common proper time',
        'general_CST_derivative_bias':'UNRESOLVED unless independent third/fourth time-derivative or direct-operator bounds are supplied',
        'numerical_status':'fixed-epsilon sensitivity rational exact; logarithmic probability/resource evaluation floating point'})
    return fixed,levels,resources


def guard_controls():
    out=[]
    def test(name,observed,expected):
        require(observed==expected,name);out.append({'control':name,'observed':observed,'expected':expected,'test':'PASS'})
    for name,error,expected in [('contained interval',I('-.02','.02'),'PASS'),
                                ('disjoint six percent deviation',I('.06','.07'),'FAIL'),
                                ('overlapping interval',I('.04','.06'),'HOLD'),
                                ('closed tolerance endpoint',I('-.05','.05'),'PASS')]:
        test(name,interval_decision(error,'.05'),expected)
    fractions={k:str(v) for k,v in PLAN['error_budget_fractions'].items()}
    components={k:'0' for k in fractions};components['boundary']=None
    test('unknown boundary error cannot be zero',complete_comparison(I(0),components,'.05',fractions)['decision'],'HOLD')
    components={k:'0' for k in fractions};components['sampling']='.021'
    test('component cap cannot be silently reallocated',complete_comparison(I(0),components,'.05',fractions)['decision'],'HOLD')
    closure={k:'CLOSED_WITH_REVIEWED_EVIDENCE' for k in ['D1','D2','D3','D4','D5','D6','D7']}
    nominal_run={k:'FIXTURE_SUPPLIED' for k in ['lambda0','Lk','Lcg','ensemble_size','seed_manifest',
                 'matched_couplings','physical_observable_adapters','total_uncertainty_method']}
    test('perfect reference data cannot qualify CST',cst_eligibility(closure,nominal_run,'CLASSICAL_REFERENCE')['decision'],'HOLD_NOT_ELIGIBLE')
    keys=PLAN['physical_refinement']['invariants'];base={k:'FIXTURE_FIXED_'+k for k in keys}
    base.update({'Lk':'1','Lcg':'1/2','G':'1','physical_time_grid':['0','1/4','1/2','3/4','1'],
                 'refinement_mode':'regulated_physical_matching'})
    manifests=[]
    for ratio in [1,2,4,8]:
        m=copy.deepcopy(base);m.update({'lambda':128*ratio,'ell_power4':F(1,128*ratio)});manifests.append(m)
    test('fixed physical metadata',matching_guard(manifests,keys)['decision'],'PASS_METADATA_ONLY')
    mutations=[('shrinking averaging scale','Lcg','1/4'),('shrinking domain at fixed expected N','domain_definition','ONE_EIGHTH_VOLUME'),
               ('mass-dependent proper-time rescaling','physical_time_grid','T/Ts(M)'),('changed physical coupling','G','6/5'),
               ('retuned tolerances','tolerances_hash','NEW_TOLERANCES'),('missing matching trajectory','renormalization_trajectory_hash',None),
               ('wrong density-to-length conversion','ell_power4',F(1,1024**2))]
    for label,key,value in mutations:
        bad=copy.deepcopy(manifests);bad[-1][key]=value
        test(label,matching_guard(bad,keys)['decision'],'HOLD')
    bad=copy.deepcopy(manifests);bad[-1]['lambda']=512
    test('wrong density ratio',matching_guard(bad,keys)['decision'],'HOLD')
    for m in MASSES:
        desired=-SQRT_M[m]/6;shared=F(-1,6)
        error=(I.fraction(shared)-I.fraction(desired))/I.fraction(abs(desired))
        test('shared velocity M='+str(m),interval_decision(error,'.05'),'PASS' if m==1 else 'FAIL')
        truth=-m/72;modified=F(6,5)*truth
        test('six-fifths force acceleration M='+str(m),
             interval_decision((I.fraction(modified)-I.fraction(truth))/I.fraction(abs(truth)),'.05'),'FAIL')
    # Independent arithmetic controls against exact rational results.
    from intervals import cube_root_rational
    checks=[(I.fraction(F(1,3))+I.fraction(F(1,7)),F(10,21)),
            (I.fraction(F(-5,9))*I.fraction(F(7,11)),F(-35,99)),
            (I.fraction(F(-2,3))/I.fraction(F(-7,13)),F(26,21))]
    for i,(v,q) in enumerate(checks):
        # Fraction(Decimal) is exact, so this is independent of Decimal rounding.
        test('directed rational arithmetic '+str(i),F(v.lo)<=q<=F(v.hi),True)
    root=cube_root_rational(F(1,4),100)
    test('exact rational root enclosure',F(root.lo)**3<=F(1,4)<=F(root.hi)**3,True)
    dump('guard_controls.json',out)
    return len(out)


def physical_records():
    closure=PLAN['physical_eligibility'].copy()
    closure={k:v for k,v in closure.items() if k.startswith('D')}
    eligibility=cst_eligibility(closure,{},'NO_COUPLED_CST_DATA')
    eligibility.update({'execution':'NOT_RUN','regularity':'HOLD','candidate':'CST-DUST-C1',
        'reference_checks_cannot_close_eligibility':True})
    dump('eligibility.json',eligibility)
    manifest={'id':PLAN['id'],'plan_sha256':sha('plan.json'),'contract_sha256':sha('inputs/parent_contract.json'),
              'physical_execution':'NOT_RUN','classical_reference_execution':'RUN','new_random_draws':0,
              'new_CST_ensembles':0,'numerical_steps':PLAN['numerical_reference']['steps'],
              'physical_density_ratios_planned':[1,2,4,8],'physical_absolute_densities':None,
              'versions':{'python':platform.python_version(),'numpy':version('numpy'),'scipy':version('scipy')},
              'source_sha256':{name:sha(name) for name in ['run.py','intervals.py','acceptance.py']},
              'evidence_class':'CLASSICAL_REFERENCE_AND_PROTOCOL_CONTROLS'}
    dump('run_manifest.json',manifest)
    parent=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    spec=importlib.util.spec_from_file_location('parent_gate',ROOT/'inputs/parent_gate.py')
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    records=[];audits=[]
    for ratio in [1,2,4,8]:
        for m in MASSES:
            for x in TIMES:
                context={'density_ratio':ratio,'M':str(m),'x':str(x)}
                record={'contract_id':parent['id'],'contract_sha256':sha('inputs/parent_contract.json'),
                    'checkpoint_id':'P3','checkpoint_context':context,'execution':'NOT_RUN',
                    'run_manifest_sha256':sha('results/run_manifest.json'),
                    'scope':{'model_id':'CST-DUST-C1','domain':'Finite dust interior, material surface and exterior',
                      'time_interval':'[0,5*sqrt(5)/3], with declared readout x='+str(x),
                      'refinement':'Planned physical density ratio '+str(ratio)+'; no actual coupled-CST run',
                      'claim_level':'Eligibility HOLD; reference controls do not qualify physical correspondence'},
                    'gates':{g:{r:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION',
                              'evidence_refs':['plan.json','results/eligibility.json','DERIVATION.md'],
                              'scope_checked':True,'reviewed':True} for r in s['requirements']}
                             for g,s in parent['gates'].items()}}
                result=gate.evaluate(record,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
                require(result['record_valid'] and set(result['decisions'].values())=={'HOLD'},'P3 gate promotion')
                records.append(record);audits.append({'context':context,**result})
    dump('checkpoint_P3_records.json',records);dump('checkpoint_P3_audits.json',audits)
    dump('checkpoint_P3_summary.json',{'records':len(records),'all_records_valid':True,
        'physical_decisions':{g:'HOLD' for g in parent['gates']},'regularity_reassessed_at_each_record':True,
        'no_physical_data_generated':True,'singularity_resolution':'HOLD'})
    dump('reference_regularity.json',{'scope':'Inserted deterministic REF-DUST-FB-01 on 0<=x<=1; not the CST candidate',
        'rho_scale':'M/V0','K_scale':'(G*M/R0^3)^2','rho_squared_normalized_upper':16,
        'K_interior_normalized_upper':960,'K_exterior_normalized_upper':768,
        'proof':'q<=1/2 gives s=1-q*x>=1/2; rho/rho0=s^-2, K_in/K_scale=60*s^-4; K_out maximal at the surface equals 48*s^-4',
        'density_at_surface':'one-sided finite limits; no extra thin shell in this reference',
        'counting_density':'not present in the inserted classical metric',
        'reference_decision':'PASS_FIXED_CLASSICAL_WINDOW','physical_CST_regularity':'HOLD'})
    return eligibility


if __name__=='__main__':
    require(sha('plan.json')==(ROOT/'plan.sha256').read_text().split()[0],'Plan changed')
    require(sha('inputs/parent_contract.json')==PLAN['parent_contract_sha256'],'Contract changed')
    provenance=json.loads((ROOT/'inputs/provenance.json').read_text())
    for name,digest in provenance['sha256'].items():require(sha('inputs/'+name)==digest,'Input changed: '+name)
    controls=guard_controls();numerical=reference_audit();fixed,levels,resources=derivative_budget();elig=physical_records()
    result={'id':PLAN['id'],'plan_sha256':sha('plan.json'),'guard_controls':controls,
        'numerical_reference_levels':numerical,'volume_derivative_fixed_epsilon':fixed,
        'inherited_density_derivative_budget':levels,'resource_forecasts':resources,
        'physical_correspondence':elig['decision'],'physical_execution':'NOT_RUN',
        'regularity':'HOLD','new_random_draws':0,'new_CST_ensembles':0,'paid_runs':False}
    dump('verification.json',result);print(json.dumps(result,indent=2))
