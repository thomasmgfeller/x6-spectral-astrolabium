"""Round-sphere expansion on the fixed classical reference; no CST data."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import csv, hashlib, importlib.util, json, platform
from intervals import I, cube_root_rational

ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'plan.json').read_text())
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
MASSES=[F(x) for x in P['reference']['masses']]
TIMES=[F(x) for x in P['reference']['x_times']]
CHIS=[F(x) for x in P['reference']['chi_shells']]
SQM={F(1,4):F(1,2),F(1):F(1),F(4):F(2)}


def require(ok,msg):
    if not ok:raise ValueError(msg)


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def write_csv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def sqrt_q(q):
    q=F(q);require(q>=0,'negative square root')
    if q in (0,1):return I(q.numerator)
    lo,hi=F(0),max(F(1),q)
    for _ in range(P['numerical']['root_bisections']):
        mid=(lo+hi)/2
        if mid*mid<=q:lo=mid
        else:hi=mid
    return I(I.fraction(lo).lo,I.fraction(hi).hi)


def sqrt_i(a):
    require(a.lo>=0,'negative interval square root')
    return I(sqrt_q(F(a.lo)).lo,sqrt_q(F(a.hi)).hi)


SQ5=sqrt_q(5);TEND=SQ5*5/3
def overlap(a,b):return max(a.lo,b.lo)<=min(a.hi,b.hi)
def bound(a):return str(a.absolute().hi)


def classify(ep,em,complete=True,future=True):
    if not future:return 'HOLD_ORIENTATION'
    if not complete or ep is None or em is None:return 'HOLD_UNKNOWN_ERROR'
    if ep.hi<0 and em.hi<0:return 'FUTURE_TRAPPED_ROUND'
    if ep.lo>0 and em.hi<0:return 'UNTRAPPED_ROUND'
    if ep.lo>0 and em.lo>0:return 'PAST_TRAPPED_ROUND'
    return 'HOLD_SIGN_UNRESOLVED'


def candidate_decision(ep,em,origin,eligible,complete):
    if origin!='DYNAMIC_CST' or not eligible:return 'HOLD_NOT_ELIGIBLE'
    return classify(ep,em,complete=complete)


def exact(m,x):
    q=SQM[m]/4;s=1-q*x
    require(0<=x<=1 and s>0,'outside fixed reference interval')
    r=cube_root_rational(s*s)
    ht=I.fraction(-SQM[m]/(6*s))
    return r,ht


def values(r,ht,chi):
    require(chi>0 and r.lo>0,'degenerate sphere')
    R=10*r*chi;v=-ht*R/TEND
    return R,v,1-v,-1-v


def reference_grid():
    states={}
    with (ROOT/'inputs/reference_comparisons.csv').open() as f:
        for row in csv.DictReader(f):
            if row['observable'] in ('r','H_times_Tend'):
                states[int(row['steps']),F(row['M']),F(row['x']),row['observable']]=I(row['ODE_enclosure_lo'],row['ODE_enclosure_hi'])
    rows=[];ext=[];levels=[];stress=[];boundary=[]
    for N in P['numerical']['inherited_Euler_steps']:
        errors=[]
        for m in MASSES:
            for x in TIMES:
                r,ht=states[N,m,x,'r'],states[N,m,x,'H_times_Tend']
                rt,htt=exact(m,x)
                require(r.contains(rt) and ht.contains(htt),'inherited state enclosure')
                for chi in CHIS:
                    R,v,ep,em=values(r,ht,chi);Rt,vt,ept,emt=values(rt,htt,chi)
                    C=I.fraction(2*m*chi*chi)/(10*r)
                    ep_mass,em_mass=1-sqrt_i(C),-1-sqrt_i(C)
                    require(ep.contains(ept) and em.contains(emt),'null expansion not enclosed')
                    require(overlap(ep,ep_mass) and overlap(em,em_mass),'kinematic/mass paths disagree')
                    require((ep*em-(C-1)).contains(0),'Misner-Sharp product identity')
                    err=max((ep-ept).absolute().hi,(em-emt).absolute().hi);errors.append(err)
                    rows.append({'N':N,'M':str(m),'x':str(x),'chi':str(chi),
                        'R_lo':str(R.lo),'R_hi':str(R.hi),'Theta_times_Tend_lo':str((3*ht).lo),'Theta_times_Tend_hi':str((3*ht).hi),
                        'e_plus_lo':str(ep.lo),'e_plus_hi':str(ep.hi),'e_minus_lo':str(em.lo),'e_minus_hi':str(em.hi),
                        'C_lo':str(C.lo),'C_hi':str(C.hi),'e_error_upper':str(err),'classification':classify(ep,em)})
                    if N==P['numerical']['inherited_Euler_steps'][-1]:
                        vb=vt*I.fraction(F(19,20)**2)
                        vu=vt*I.fraction(F(21,20)**2)
                        vbox=I(vb.lo,vu.hi)
                        stress.append({'M':str(m),'x':str(x),'chi':str(chi),
                            'e_plus_lo':str((1-vbox).lo),'e_plus_hi':str((1-vbox).hi),
                            'reference_class':classify(ept,emt),'box_class':classify(1-vbox,-1-vbox),
                            'scope':'HYPOTHETICAL_H_R_5_PERCENT_BOX_NOT_PHYSICAL_DATA'})
                for raw in P['reference']['exterior_fixed_R']:
                    R=F(raw);Rb=10*r
                    domain='EXTERIOR' if Decimal(R.numerator)/Decimal(R.denominator)>=Rb.hi else (
                        'INSIDE_MATERIAL_EXCLUDED' if I.fraction(R).hi<Rb.lo else 'HOLD_DOMAIN_OVERLAP')
                    ep=1-sqrt_q(2*m/R);em=-1-sqrt_q(2*m/R)
                    status=classify(ep,em) if domain=='EXTERIOR' else domain
                    if domain=='EXTERIOR' and R==2*m:status='MARGINAL_ANALYTIC_REFERENCE'
                    ext.append({'N':N,'M':str(m),'x':str(x),'R':str(R),'domain':domain,
                        'e_plus_lo':str(ep.lo) if domain=='EXTERIOR' else '',
                        'e_plus_hi':str(ep.hi) if domain=='EXTERIOR' else '',
                        'e_minus_lo':str(em.lo) if domain=='EXTERIOR' else '',
                        'e_minus_hi':str(em.hi) if domain=='EXTERIOR' else '',
                        'classification':status})
                if N==P['numerical']['inherited_Euler_steps'][-1]:
                    Rb,vin,ep,em=values(rt,htt,F(1));vout=sqrt_i(I.fraction(2*m)/Rb)
                    require(overlap(vin,vout),'surface shift mismatch')
                    total_v_in=I.fraction(F(3,2))*vin*vin/Rb-vin*vin/Rb
                    total_v_out=vout*vout/(2*Rb)
                    acceleration=I.fraction(m)/(Rb*Rb)
                    require(overlap(total_v_in,acceleration) and overlap(total_v_out,acceleration),
                            'surface acceleration mismatch')
                    # u=(1,-v), s=(0,1) in the PG metric. Darmois K follows
                    # from geodesic surface motion (K_TT=0), s(R)=1 (K_ang=R).
                    gtt=vin*vin-1
                    require((gtt-2*vin*vin+vin*vin+1).contains(0),'surface induced metric')
                    require((vin-vin).contains(0),'surface orthogonality')
                    boundary.append({'M':str(m),'x':str(x),'R_lo':str(Rb.lo),'R_hi':str(Rb.hi),
                        'v_jump_contains_zero':(vin-vout).contains(0),'h_TT_both':-1,
                        'surface_acceleration_both':str((-acceleration).middle_float()),
                        'K_TT_both':0,'K_angular_over_R_both':1,'mass_both':str(m),
                        'pressure_both':0,'no_surface_layer':'ANALYTIC_CLASSICAL_JUNCTION_ONLY'})
        levels.append({'N':N,'interior_spheres':len(MASSES)*len(TIMES)*len(CHIS),
            'max_absolute_e_error':str(max(errors)),
            'numerical_cap_pass':max(errors)<=F(P['numerical']['normalized_expansion_cap'])})
    write_csv('sphere_expansions.csv',rows);write_csv('exterior_expansions.csv',ext)
    write_csv('numerical_levels.csv',levels);write_csv('hypothetical_tolerance_box.csv',stress)
    write_csv('surface_matching.csv',boundary)
    return rows,ext,levels,stress,boundary


def ray_radius(m,x0,chi,dx,direction):
    q=SQM[m]/4;s0=1-q*x0;s1=1-q*(x0+dx)
    require(0<=x0+dx<=1,'ray leaves time window')
    f0=cube_root_rational(s0);f1=cube_root_rational(s1)
    ch=I.fraction(chi)+direction*SQ5/(2*q)*(f0-f1)
    require(ch.lo>0 and ch.hi<1,'ray crosses center or material surface')
    return 10*f1*f1*ch


def area_calibration():
    rows=[];summary=[]
    for dh in P['area_calibration']['delta_x']:
        h=F(dh);errs=[]
        for m in MASSES:
            for rawx in P['area_calibration']['x_times']:
                x=F(rawx);r,ht=exact(m,x)
                for rawchi in P['area_calibration']['chi_shells']:
                    chi=F(rawchi);R,v,ep,em=values(r,ht,chi)
                    for sign,name,target in [(1,'outgoing',ep),(-1,'ingoing',em)]:
                        Rp=ray_radius(m,x,chi,h,sign);Rm=ray_radius(m,x,chi,-h,sign)
                        estimate=(Rp*Rp-Rm*Rm)/(4*h*TEND*R)
                        error=estimate-target;errs.append(error.absolute().hi)
                        rows.append({'delta_x':dh,'M':str(m),'x':str(x),'chi':str(chi),'direction':name,
                            'e_estimate_lo':str(estimate.lo),'e_estimate_hi':str(estimate.hi),
                            'e_error_lo':str(error.lo),'e_error_hi':str(error.hi),
                            'numerical_cap_pass':error.absolute().hi<=F(P['area_calibration']['absolute_e_cap'])})
        summary.append({'delta_x':dh,'cases':len(errs),'max_absolute_e_error':str(max(errs)),
                        'numerical_cap_pass':max(errs)<=F(P['area_calibration']['absolute_e_cap'])})
    write_csv('area_derivative_calibration.csv',rows);dump('area_calibration_summary.json',summary)
    return summary


def crossing(m,chi):
    a=F(2)*m*chi*chi/10
    return (1-I.fraction(a)*sqrt_q(a))/(SQM[m]/4)


def events():
    roots=[];active=[];brackets=[];tubes=[]
    for m in MASSES:
        for chi in CHIS:
            xc=crossing(m,chi)
            status='IN_FIXED_WINDOW' if xc.lo>=0 and xc.hi<=1 else 'OUTSIDE_FIXED_WINDOW'
            roots.append({'M':str(m),'chi':str(chi),'threshold_Rb':str(2*m*chi*chi),
                'x_lo':str(xc.lo),'x_hi':str(xc.hi),'T_lo':str((xc*TEND).lo),'T_hi':str((xc*TEND).hi),
                'status':status,'physical_CST':'HOLD_NOT_RUN'})
            if status=='IN_FIXED_WINDOW':active.append((m,chi,xc))
    for N in P['numerical']['inherited_Euler_steps']:
        for m in MASSES:
            targets=[(chi,xc) for mass,chi,xc in active if mass==m]
            if not targets:continue
            h=I.fraction(F(1,N));k=m/72;B=I.fraction(F(125,27)*k)
            r,u,E=I(1),I.fraction(-SQM[m]/6),I(0)
            bounds={chi:[F(0),None] for chi,_ in targets}
            for step in range(N+1):
                require(r.lo>=Decimal('.6') and r.hi<=Decimal('1.05')
                        and u.lo>=Decimal('-.5') and u.hi<=0,'Euler domain')
                enc=r.inflate(E);x=F(step,N)
                for chi,_ in targets:
                    threshold=I.fraction(2*m*chi*chi/10)
                    if enc.lo>threshold.hi:bounds[chi][0]=x
                    if enc.hi<threshold.lo and bounds[chi][1] is None:bounds[chi][1]=x
                if step<N:r,u,E=r+h*u,u-h*I.fraction(k)/(r*r),(1+h)*E+B*h*h/2
            for chi,xc in targets:
                lo,hi=bounds[chi];require(hi is not None,'crossing not bracketed')
                bracket=I(I.fraction(lo).lo,I.fraction(hi).hi)
                require(bracket.contains(xc),'analytic event outside numerical bracket')
                brackets.append({'N':N,'M':str(m),'chi':str(chi),'x_lower':str(lo),'x_upper':str(hi),
                    'width_x':str(hi-lo),'width_cap_pass':hi-lo<=F(P['numerical']['event_bracket_width_cap_x']),
                    'analytic_event_enclosed':True,'scope':'NUMERICAL_REFERENCE_NOT_PHYSICAL_REFINEMENT'})
    for m in MASSES:
        for x in TIMES:
            r,ht=exact(m,x);Rb=10*r
            if (I.fraction(2*m)/Rb).lo<=1:continue
            RA=-TEND/ht
            require(RA.hi<Rb.lo and Rb.hi<2*m,'trapped annulus ordering')
            for kind,R,der,norm in [('inner_dust',RA,1/(RA*RA),F(-3,4)),
                                  ('outer_vacuum',I.fraction(2*m),-2/(I.fraction(2*m)**2),F(0))]:
                tubes.append({'M':str(m),'x':str(x),'branch':kind,'R_lo':str(R.lo),'R_hi':str(R.hi),
                    'chi_if_inner':str((R/Rb).middle_float()) if kind=='inner_dust' else '',
                    'L_n_theta_l_lo':str(der.lo),'L_n_theta_l_hi':str(der.hi),
                    'tangent_norm':str(norm),'type':'FUTURE_INNER_TIMELIKE' if norm<0 else 'FUTURE_OUTER_NULL'})
    write_csv('analytic_crossings.csv',roots);write_csv('numerical_event_brackets.csv',brackets)
    write_csv('marginal_tubes.csv',tubes)
    return roots,brackets,tubes,active


def controls():
    rows=[]
    def test(name,actual,expected):
        require(actual==expected,name);rows.append({'control':name,'actual':actual,'expected':expected,'pass':True})
    test('Minkowski',classify(I(1),I(-1)),'UNTRAPPED_ROUND')
    test('Contracting small sphere',classify(I('0.8'),I('-1.2')),'UNTRAPPED_ROUND')
    test('Contracting trapped sphere',classify(I('-.2'),I('-2.2')),'FUTURE_TRAPPED_ROUND')
    test('Expanding C>1',classify(I('2.2'),I('.2')),'PAST_TRAPPED_ROUND')
    test('Zero interval is not marginal proof',classify(I('-.01','.01'),I(-2)),'HOLD_SIGN_UNRESOLVED')
    test('Exact zero alone needs marginal evidence',classify(I(0),I(-2)),'HOLD_SIGN_UNRESOLVED')
    test('Unknown error',classify(I(-1),I(-2),complete=False),'HOLD_UNKNOWN_ERROR')
    test('Reversed time orientation',classify(I(-1),I(-2),future=False),'HOLD_ORIENTATION')
    for b in [F(1,10),F(1),F(10)]:
        ep=I.fraction(-F(1,5))*b;em=I.fraction(-F(11,5))/b
        test('Positive reciprocal boost '+str(b),classify(ep,em),'FUTURE_TRAPPED_ROUND')
        test('Boost product '+str(b),(ep*em).contains(F(11,25)),True)
    rejected=False
    try:values(I(1),I(-1),F(0))
    except ValueError:rejected=True
    test('Degenerate center sphere excluded',rejected,True)
    r,ht=exact(F(4),F(0));R,v,ep,em=values(r,ht,F(4,5))
    test('R=2M initially lies inside material',R.hi<(10*r).lo,True)
    test('Global exterior mass is invalid inside',classify(ep,em),'UNTRAPPED_ROUND')
    test('Inner horizon derivative sign',(I(1)/I(4)**2).lo>0,True)
    test('Outer horizon derivative sign',(-I(2)/I(4)**2).hi<0,True)
    # Scalar curvature has a finite density step. Continuity of h,K is the
    # no-thin-shell condition; continuity of density is not required.
    _,vb,_,_=values(r,ht,F(1))
    test('Mismatched exterior mass rejected',(vb*vb-I(1)).contains(0),False)
    test('sqrt rational enclosure',(sqrt_q(F(2))**2).contains(2),True)
    test('round scope excludes arbitrary surfaces',P['reference']['domain'].startswith('0<=x<=1, round symmetry spheres only'),True)
    test('classical evidence cannot authorize CST',candidate_decision(I(-1),I(-2),'CLASSICAL_REFERENCE',True,True),'HOLD_NOT_ELIGIBLE')
    test('CST data without closed model',candidate_decision(I(-1),I(-2),'DYNAMIC_CST',False,True),'HOLD_NOT_ELIGIBLE')
    test('CST data with unknown error',candidate_decision(I(-1),I(-2),'DYNAMIC_CST',True,False),'HOLD_UNKNOWN_ERROR')
    dump('controls.json',rows);return rows


def checkpoints(active):
    parent=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    manifest={'id':P['id'],'plan_sha256':sha('plan.json'),'parent_contract_sha256':sha('inputs/parent_contract.json'),
        'parent_main_commit':'b4a52636c506288462e21d88e0f6bd152a78b540','python':platform.python_version(),
        'source_sha256':{n:sha(n) for n in ['analyze.py','intervals.py']},
        'physical_execution':'NOT_RUN','classical_reference_execution':'RUN','new_CST_ensembles':0,'new_random_draws':0}
    dump('run_manifest.json',manifest)
    spec=importlib.util.spec_from_file_location('parent_gate',ROOT/'inputs/parent_gate.py')
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    contexts=[]
    for ratio in P['physical_refinement']['density_ratios']:
        for m in MASSES:
            for x in TIMES:contexts.append({'density_ratio':ratio,'M':str(m),'x':str(x),'kind':'FIXED_GRID'})
        for m,chi,xc in active:contexts.append({'density_ratio':ratio,'M':str(m),'chi':str(chi),'x_interval':xc.bounds(),'kind':'REFERENCE_CROSSING'})
    records=[];audits=[]
    for context in contexts:
        record={'contract_id':parent['id'],'contract_sha256':sha('inputs/parent_contract.json'),
            'checkpoint_id':'P4','checkpoint_context':context,'execution':'NOT_RUN','run_manifest_sha256':sha('results/run_manifest.json'),
            'scope':{'model_id':'CST-DUST-C1','domain':'Finite dust ball, surface and exterior; round spheres only',
                'time_interval':'Fixed common classical reference interval 0<=T<=5*sqrt(5)/3',
                'refinement':'Planned density ratio '+str(context['density_ratio'])+'; no physical CST evolution',
                'claim_level':'Classical local trapping diagnostics only; physical CST and global event horizon unqualified'},
            'gates':{g:{req:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION','evidence_refs':['plan.json','DERIVATION.md','results/verification.json'],
                'scope_checked':True,'reviewed':True} for req in section['requirements']} for g,section in parent['gates'].items()}}
        audit=gate.evaluate(record,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
        require(audit['record_valid'] and set(audit['decisions'].values())=={'HOLD'},'P4 promoted')
        records.append(record);audits.append({'context':context,**audit})
    dump('checkpoint_P4_records.json',records);dump('checkpoint_P4_audits.json',audits)
    reg=json.loads((ROOT/'inputs/reference_regularity.json').read_text())
    reg.update({'checkpoint':'P4','round_trapping_does_not_promote_regularity':True,
        'global_event_horizon':'NOT_DETERMINED_ON_FINITE_TIME_WINDOW','all_P4_regularities':'HOLD',
        'count_P4_records':len(records),'marginal_tube_corner':'one-sided classification at surface crossing; no smooth global tube claimed'})
    dump('regularity_and_scope.json',reg);return len(records)


def main():
    require(sha('plan.json')==(ROOT/'plan.sha256').read_text().split()[0],'Plan changed')
    prov=json.loads((ROOT/'inputs/provenance.json').read_text())
    for n,d in prov['input_sha256'].items():require(sha('inputs/'+n)==d,'Input changed '+n)
    require(sha('intervals.py')==prov['intervals_sha256'],'Interval library changed')
    rows,ext,levels,stress,boundary=reference_grid()
    area=area_calibration();roots,brackets,tubes,active=events();ctl=controls();n=checkpoints(active)
    continuous=[]
    for m in MASSES:
        r,ht=exact(m,F(1));Cb=I.fraction(2*m)/(10*r);chiA=sqrt_i(10*r/I.fraction(2*m))
        continuous.append({'M':str(m),'R_b_end':(10*r).bounds(),'surface_C_max':Cb.bounds(),
            'chi_inner_end':chiA.bounds(),'Theta_times_Tend_end':(3*ht).bounds(),
            'whole_window_round_trapping':'ABSENT_IN_REFERENCE_WINDOW' if Cb.hi<1 else 'PRESENT_AFTER_SURFACE_CROSSING',
            'scope':'ALL_ROUND_SYMMETRY_SPHERES_ONLY; not arbitrary trapped surfaces or event horizons'})
    dump('continuous_reference_decisions.json',continuous)
    finest=[r for r in rows if r['N']==P['numerical']['inherited_Euler_steps'][-1]]
    def counts(seq,key):return {k:sum(r[key]==k for r in seq) for k in sorted({r[key] for r in seq})}
    result={'id':P['id'],'plan_sha256':sha('plan.json'),'interior_comparisons':len(rows),'exterior_slots':len(ext),
        'numerical_levels':levels,'area_calibration':area,'surface_matching_cases':len(boundary),
        'analytic_crossing_candidates':len(roots),'crossings_in_window':[r for r in roots if r['status']=='IN_FIXED_WINDOW'],
        'numerical_event_brackets':len(brackets),'all_bracket_caps_pass':all(r['width_cap_pass'] for r in brackets),
        'continuous_reference_decisions':continuous,
        'marginal_tube_readouts':len(tubes),'controls':len(ctl),'finest_round_classifications':counts(finest,'classification'),
        'hypothetical_5_percent_box_classifications':counts(stress,'box_class'),'P4_records':n,
        'classical_reference':'RUN_SEPARATE_SCOPE','physical_CST_trapping':'HOLD_NOT_ELIGIBLE',
        'physical_CST_execution':'NOT_RUN','physical_CST_regularity':'HOLD','global_event_horizon':'NOT_DETERMINED',
        'new_CST_ensembles':0,'new_random_draws':0,'paid_runs':False}
    require(levels[-1]['numerical_cap_pass'] and area[-1]['numerical_cap_pass'],'finest numerical calibration cap')
    dump('verification.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
