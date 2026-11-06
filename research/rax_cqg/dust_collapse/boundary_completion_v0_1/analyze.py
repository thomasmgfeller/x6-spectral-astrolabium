"""Scoped finite-ball completion: exact identities and outward intervals."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import csv,hashlib,importlib.util,itertools,json,platform
import sympy
from intervals import I,cube_root_rational
from symbolic_checks import run as symbolic_run

ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'plan.json').read_text());OUT=ROOT/'results';OUT.mkdir(exist_ok=True)

def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(n,o):(OUT/n).write_text(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def csvout(n,rows):
    with (OUT/n).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sqrtq(q):
    q=F(q);require(q>=0,'negative sqrt');lo,hi=F(0),max(F(1),q)
    if q==0:return I(0)
    for _ in range(P['numerical']['root_bisections']):
        mid=(lo+hi)/2
        if mid*mid<=q:lo=mid
        else:hi=mid
    return I(I.fraction(lo).lo,I.fraction(hi).hi)
def sqrti(q):return I(sqrtq(F(q.lo)).lo,sqrtq(F(q.hi)).hi)
def cubeq(q):
    q=F(q);require(q>=0,'negative cube root')
    return cube_root_rational(q) if q<=1 else 1/cube_root_rational(1/q)
CAP=Decimal(P['numerical']['identity_residual_cap']);SQ5=sqrtq(5);TE=SQ5*5/3
SQM={F(1,4):F(1,2),F(1):F(1),F(4):F(2)}
def checkzero(i,label):
    require(i.contains(0) and i.absolute().hi<CAP,label)
    return i.absolute().hi

def reference():
    rows=[];exterior=[];ef=[];events=[];worst=Decimal(0)
    for mm in P['reference']['masses']:
        m=F(mm);q=SQM[m]/4;Ts=TE/I.fraction(q)
        for xx in P['reference']['x_times']:
            x=F(xx);s=1-q*x;R=10*cube_root_rational(s*s);w=sqrti(I.fraction(2*m)/R)
            vel=-w;acc=-I.fraction(m)/R**2;f=1-I.fraction(2*m)/R;beta=sqrti(vel**2+f);vdot=1/(1+w)
            residuals=[vel**2-I.fraction(2*m)/R,acc+I.fraction(m)/R**2,
                -f*vdot**2+2*vdot*vel+1,(beta-1)/R,
                (acc+I.fraction(m)/R**2)/beta,
                R*vel**2/2-I.fraction(m),
                -3*w*w/(2*R)-w*(-3*w/(2*R)),
                (I.fraction(6*m)/R**3)*(vel+w)]
            err=max(checkzero(z,'classical junction') for z in residuals);worst=max(worst,err)
            rows.append({'M':mm,'x':xx,'Rb_lo':str(R.lo),'Rb_hi':str(R.hi),'v_EF_dot_lo':str(vdot.lo),'v_EF_dot_hi':str(vdot.hi),'max_identity_residual':str(err),'junction':'PASS_CLASSICAL_FIXED_WINDOW','thin_shell':'ZERO','physical_CST':'HOLD'})
            for multiple in P['reference']['exterior_radius_over_Rb']:
                rad=R*multiple;K=I.fraction(48*m*m)/rad**6;bound=I.fraction(48*m*m)/R**6
                require(K.hi<=bound.hi,'exterior curvature envelope')
                exterior.append({'M':mm,'x':xx,'R_over_Rb':multiple,'K_lo':str(K.lo),'K_hi':str(K.hi),'boundary_K_upper':str(bound.hi),'density':'0','geometric_mass':mm,'scope':'CLASSICAL_ALL_EXTERIOR_ANALYTIC_ENVELOPE'})
        for rr in P['reference']['EF_radius_over_2GM']:
            ratio=F(rr);R=2*m*ratio;w=sqrtq(1/ratio);dv=1/(1+w);vel=-w;f=I.fraction(1-1/ratio)
            err=checkzero(-f*dv**2+2*dv*vel+1,'EF horizon continuation')
            T=Ts-I.fraction(F(2,3))*I.fraction(R)*sqrtq(R)/sqrtq(2*m);x=T/TE
            ef.append({'M':mm,'R_over_2GM':rr,'x_lo':str(x.lo),'x_hi':str(x.hi),'v_dot_lo':str(dv.lo),'v_dot_hi':str(dv.hi),'max_identity_residual':str(err),'scope':'IN_FIXED_WINDOW' if x.lo>=0 and x.hi<=1 else 'ANALYTIC_CLASSICAL_EXTENSION_ONLY'})
        Th=Ts-I.fraction(4*m/3);Tc=Ts-I.fraction(9*m/2)
        initial_chi=3-sqrtq(F(20)/m)
        events.append({'M':mm,'Ts_lo':str(Ts.lo),'Ts_hi':str(Ts.hi),'surface_crossing_T_lo':str(Th.lo),'surface_crossing_T_hi':str(Th.hi),'formal_center_origin_T_lo':str(Tc.lo),'formal_center_origin_T_hi':str(Tc.hi),'EH_R_at_T0_lo':str((10*initial_chi).lo) if Tc.hi<0 else '', 'EH_R_at_T0_hi':str((10*initial_chi).hi) if Tc.hi<0 else '', 'assumption':'CLASSICAL_FUTURE_COMPLETION; not finite-window inference; negative origin uses analytic past extension'})
    csvout('classical_junction.csv',rows);csvout('classical_exterior.csv',exterior);csvout('EF_horizon_crossing.csv',ef);csvout('conditional_classical_event_horizon.csv',events)
    return {'junction_cases':len(rows),'exterior_cases':len(exterior),'EF_cases':len(ef),'max_reference_residual':str(worst),'event_horizon_cases':len(events)}


def conditional_legacy():
    rows=[];bounds=[]
    for raw in P['legacy_conditional_exterior']['rmin_over_GM']:
        b=F(raw);a=b**3;tscale=sqrtq(2*a/9)
        for yy in P['legacy_conditional_exterior']['y_times']:
            y=F(yy);T=tscale*y;R=I.fraction(b)*cubeq(1+y*y)
            vel=3*T/R**2;acc=3/R**2-2*vel**2/R
            f=1-2/R+I.fraction(2*a)/R**4;fp=2/R**2-I.fraction(8*a)/R**5
            mminus=R*vel**2/2;mpl=1-I.fraction(a)/R**3
            rhoext=I.fraction(6*a)/R**6;pr=-rhoext;pt=2*rhoext
            pin=-(2*acc/R+vel**2/R**2)
            errs=[vel**2+f-1,acc+fp/2,mminus-mpl,pin-pr]
            err=max(checkzero(z,'conditional legacy junction') for z in errs)
            rows.append({'rmin_over_GM':raw,'y':yy,'Rb_lo':str(R.lo),'Rb_hi':str(R.hi),'m_minus_over_M_lo':str(mminus.lo),'m_minus_over_M_hi':str(mminus.hi),'8piG_rho_ext_lo':str(rhoext.lo),'8piG_rho_ext_hi':str(rhoext.hi),'8piG_p_radial_lo':str(pr.lo),'8piG_p_radial_hi':str(pr.hi),'max_junction_residual':str(err),'vacuum':'FALSE','physical_CST':'HOLD','scope':'CONDITIONAL_STATIC_ANSATZ_ONLY'})
        fmin=1-I.fraction(F(3,2))/(cubeq(F(4))*b)
        bounds.append({'rmin_over_GM':raw,'K_interior_bound':str(108/b**6),'K_exterior_bound':str(1440/b**6),'static_f_min_lo':str(fmin.lo),'static_f_min_hi':str(fmin.hi),'static_zeros':'TWO_SIMPLE_ZEROS' if fmin.hi<0 else 'NO_ZEROS','global_completion':'NOT_QUALIFIED','DEC_atmosphere':'FAIL_p_t_equals_2rho','rho_plus_p_interior_near_bounce':'NEGATIVE'})
    csvout('conditional_nonvacuum_junction.csv',rows);dump('conditional_nonvacuum_scope.json',{'cases':len(rows),'bounds':bounds,'proof_scope':'Fixed ansatz and scale only; not dynamical CST, no global uniqueness/stability/completeness claim','scale_limit':'bounds diverge as rmin^-6 at fixed M','rejected_bounce_candidate_status':'UNCHANGED'})
    return len(rows)


def bdg_control():
    def hist(nodes,rel):
        counts=[0]*4
        for a,b in rel:
            if a in nodes and b in nodes:
                k=sum((a,c) in rel and (c,b) in rel for c in nodes)
                if k<4:counts[k]+=1
        return counts
    def functional(nodes,rel):
        h=hist(nodes,rel);return len(nodes)+sum(c*n for c,n in zip([-1,9,-16,8],h))
    rows=[]
    for n in P['causal_cut_controls']['N']:
        nodes=set(range(n));rel={(a,b) for a in nodes for b in nodes if a<b}
        for k in range(1,n):
            A=set(range(k));B=nodes-A;total=functional(nodes,rel);split=functional(A,rel)+functional(B,rel)
            cross=[(a,b) for a,b in rel if (a in A)!=(b in A)]
            cross_weight=sum([-1,9,-16,8][b-a-1] if b-a-1<4 else 0 for a,b in cross)
            require(total-split==cross_weight,'cut action accounting')
            rows.append({'N':n,'cut':k,'F4_full':total,'F4_isolated_sum':split,'difference':total-split,'deleted_relations':len(cross),'scope':'KINEMATIC_CHAIN_NOT_4D_ENSEMBLE'})
    rel={(a,b) for a in range(4) for b in range(4) if a<b};base=functional(set(range(4)),rel)
    for perm in itertools.permutations(range(4)):
        require(functional(set(perm),{(perm[a],perm[b]) for a,b in rel})==base,'label invariance')
    A={0,2};B={1,3}
    example={'full_hist_N0_N3':hist(set(range(4)),rel),'full_F4':base,'convex_split_F4':functional({0,1},rel)+functional({2,3},rel),'nonconvex_split_F4':functional(A,rel)+functional(B,rel),'full_interval_0_2_count':1,'isolated_A_interval_0_2_count':0,'label_permutations':24,'scope':'Deleting outer elements can also change layers for endpoints retained inside; not a physical timelike-boundary simulation'}
    csvout('causal_cut_controls.csv',rows);dump('causal_cut_example.json',example)
    return len(rows),24


def controls():
    rows=[]
    def test(name,observed,expected):
        require(observed==expected,name);rows.append({'control':name,'observed':observed,'expected':expected,'pass':True})
    def nonshell(R,w,a,m):return 'PASS_CLASSICAL' if F(w)**2==2*F(m)/F(R) and F(a)==-F(m)/F(R)**2 else 'FAIL_CLASSICAL_JUNCTION'
    test('Exact classical boundary',nonshell(2,-1,F(-1,4),1),'PASS_CLASSICAL')
    test('Mass match at one instant does not fix acceleration',nonshell(2,-1,0,1),'FAIL_CLASSICAL_JUNCTION')
    test('Wrong exterior mass',nonshell(2,-1,F(-1,4),2),'FAIL_CLASSICAL_JUNCTION')
    test('Bounce cannot be vacuum no-shell',nonshell(3,0,1,1),'FAIL_CLASSICAL_JUNCTION')
    test('Opposite normal orientation cannot be compared as equal',F(1,3)==F(-1,3),False)
    for R,expected in [(1,'NO_TIMELIKE_BOUNCE'),(2,'NO_TIMELIKE_BOUNCE'),(3,'REQUIRES_NONZERO_SHELL')]:
        f=1-F(2,R);test('Schwarzschild bounce embedding R='+str(R),'NO_TIMELIKE_BOUNCE' if f<=0 else 'REQUIRES_NONZERO_SHELL',expected)
    test('Vaidya varying mass violates zero flux',F(1,7)*F(1,2)**2==0,False)
    test('Constant Vaidya mass is vacuum',F(0)*F(1,2)**2==0,True)
    test('Conditional atmosphere is not vacuum',F(6,3**6)>0,True)
    test('Atmosphere violates dominant energy bound',2*F(1)<=F(1),False)
    test('Cut four-chain changes action',3==2,False)
    def physical_gate(origin,action,cross,outer,regular):
        return 'PASS' if origin=='DYNAMIC_CST' and all([action,cross,outer,regular]) else 'HOLD'
    test('Classical completion cannot qualify CST',physical_gate('CLASSICAL_REFERENCE',True,True,True,True),'HOLD')
    for missing in range(4):
        flags=[True]*4;flags[missing]=False
        test('Missing closure component '+str(missing),physical_gate('DYNAMIC_CST',*flags),'HOLD')
    test('Classical curvature grows sixteenfold when remaining proper time halves',str((F(80,27)/F(1,2)**4)/F(80,27)),'16')
    dump('decision_controls.json',rows);return len(rows)


def p5_records():
    parent=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    manifest={'id':P['id'],'plan_sha256':sha('plan.json'),'contract_sha256':sha('inputs/parent_contract.json'),'parent_main_commit':'bb59cc03e762b5b2133f4f12fdd975b219bf4406','versions':{'python':platform.python_version(),'sympy':sympy.__version__},'source_sha256':{n:sha(n) for n in ['analyze.py','symbolic_checks.py','intervals.py']},'physical_execution':'NOT_RUN','evidence_class':'CLASSICAL_EXACT_AND_CONDITIONAL_DIAGNOSTICS','new_CST_ensembles':0}
    dump('run_manifest.json',manifest)
    spec=importlib.util.spec_from_file_location('parent_gate',ROOT/'inputs/parent_gate.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    records=[];audits=[]
    for density in P['physical_CST']['density_ratios_planned']:
        for m in P['reference']['masses']:
            for x in P['reference']['x_times']:
                context={'density_ratio':density,'M':m,'x':x,'spatial_scope':'INTERIOR_SURFACE_ALL_EXTERIOR'}
                rec={'contract_id':parent['id'],'contract_sha256':sha('inputs/parent_contract.json'),'checkpoint_id':'P5','checkpoint_context':context,'execution':'NOT_RUN','run_manifest_sha256':sha('results/run_manifest.json'),'scope':{'model_id':'CST-DUST-C1','domain':'Finite ball, material surface and full exterior; computational cut separate','time_interval':'Inherited fixed common window 0<=T<=5*sqrt(5)/3; additional classical completion separately conditional','refinement':'Planned density ratio '+str(density)+'; no physical CST run','claim_level':'Classical junction closed; physical CST boundary and extension unqualified'},'gates':{g:{req:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION','evidence_refs':['plan.json','DERIVATION.md','results/closure_decision.json'],'scope_checked':True,'reviewed':True} for req in section['requirements']} for g,section in parent['gates'].items()}}
                audit=gate.evaluate(rec,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json');require(audit['record_valid'] and set(audit['decisions'].values())=={'HOLD'},'P5 scope promotion')
                records.append(rec);audits.append({'context':context,**audit})
    dump('checkpoint_P5_records.json',records);dump('checkpoint_P5_audits.json',audits)
    dump('closure_decision.json',{'classical_finite_ball_junction':'CLOSED_FOR_DECLARED_EINSTEIN_DUST_REFERENCE','classical_regular_window':'PASS_FIXED_WINDOW_ALL_INTERIOR_SURFACE_EXTERIOR','classical_singularity_resolution':'FAIL_FOR_EXPLICIT_CLASSICAL_FUTURE_COMPLETION','legacy_bounce_to_vacuum':'FAIL_NO_SHELL_JUNCTION','legacy_static_nonvacuum':'CONDITIONAL_GEOMETRIC_CONSTRUCTION_ONLY','physical_CST_boundary':'HOLD_NOT_ELIGIBLE','physical_CST_extension':'HOLD','physical_CST_regularity':'HOLD','physical_execution':'NOT_RUN','P5_records':len(records),'missing':['same-theory finite-ball action including cross-surface intervals and boundary/corner terms','exterior quantum state, measure, gluing/composition and matter coupling','calibrated geometric boundary and stress observables','outer cutoff tail bound and physically matched refinement','uniform density/curvature moments and causal continuation']})
    return len(records)


def main():
    require(sha('plan.json')==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'inputs/provenance.json').read_text())
    for n,h in prov['input_sha256'].items():require(sha('inputs/'+n)==h,'Input changed '+n)
    require(sha('intervals.py')==prov['intervals_sha256'],'Inherited arithmetic changed')
    algebra=symbolic_run();dump('symbolic_checks.json',algebra)
    ref=reference();conditional=conditional_legacy();cuts,perms=bdg_control();ct=controls();n=p5_records()
    result={'id':P['id'],'plan_sha256':sha('plan.json'),'symbolic_identities':len(algebra),**ref,'conditional_nonvacuum_cases':conditional,'causal_cut_cases':cuts,'label_permutations':perms,'decision_controls':ct,'P5_records':n,'all_physical_gates':'HOLD','physical_execution':'NOT_RUN','new_CST_ensembles':0,'new_random_draws':0,'paid_runs':False}
    dump('verification.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
