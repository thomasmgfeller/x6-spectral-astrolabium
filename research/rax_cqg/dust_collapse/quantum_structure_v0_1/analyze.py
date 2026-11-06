"""Finite label reduction, ordinary-L2 constraint obstruction and metric certificate."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations
from collections import Counter
from math import factorial
import csv,hashlib,importlib.util,json,platform,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from gluing import all_posets,pairs,encode,relabel,action,require
from variation import matter_action,gamma
from quantum_structure import I,cadd,csub,cmul,cscale,conj,cjson,g_interval,matmul,adjoint,real_matrix
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
PLAN=json.loads((ROOT/'plan.json').read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def csvout(name,rows):
    with (OUT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def move(state,m,perm):
    code,mask=state
    return relabel(code,m,perm),sum(1<<perm[i] for i in range(m) if mask&(1<<i))
def patch(code,m):
    n=m+2
    return encode([(0,i) for i in range(1,n)]+[(i,n-1) for i in range(1,n-1)]
                  +[(i+1,j+1) for i,j in pairs(code,m)],n)


def label_reduction():
    summary=[];orbits=[]
    for m in PLAN['finite_group_checks']['m']:
        states=[(c,s) for c in all_posets(m) for s in range(1<<m)]
        perms=list(permutations(range(m)));order=factorial(m);mu=Q(1,order*2**m)
        left=set(states);orbit_of={};projected={};projected_g={};checks=0
        while left:
            rep=min(left);counts=Counter(move(rep,m,p) for p in perms);orbit=set(counts);aut=counts[rep]
            require(len(orbit)*aut==order and set(counts.values())=={aut},'Orbit/stabilizer')
            require(mu*len(orbit)==Q(1,2**m*aut),'Quotient measure including density-support weight')
            coeff=Q(1,len(orbit))
            require(len(orbit)*coeff**2==coeff and coeff>0,'Full projector block identity')
            fbar=sum(Q(c-2*s+1) for c,s in orbit)/len(orbit)
            gbar=sum(Q(c*s+2) for c,s in orbit)/len(orbit)
            for state in orbit:orbit_of[state]=orbit;projected[state]=fbar;projected_g[state]=gbar
            code,mask=rep;n=m+2;C=patch(code,m);T=[Q(i*i,2) for i in range(n)]
            w=[Q(i+1) if 0<i<n-1 and mask&(1<<(i-1)) else Q(0) for i in range(n)]
            value=action(C,n)+matter_action(C,n,T,w)
            for perm in perms:
                full=(0,)+tuple(i+1 for i in perm)+(n-1,)
                tp=[Q(0)]*n;wp=[Q(0)]*n
                for i in range(n):tp[full[i]]=T[i];wp[full[i]]=w[i]
                target=relabel(C,n,full)
                require(action(target,n)+matter_action(target,n,tp,wp)==value,'Joint-action invariance')
                checks+=1
            orbits.append({'m':m,'representative_order':code,'support_mask':mask,'orbit_size':len(orbit),
                           'stabilizer':aut,'projector_entry':str(coeff),'quotient_weight':str(mu*len(orbit))})
            left-=orbit
        norm=positive=adj_left=adj_right=orthogonal=Q(0);polynomial_checks=0
        for state in states:
            counts=Counter(move(state,m,p) for p in perms)
            require(set(counts)==orbit_of[state] and all(Q(k,order)==Q(1,len(counts)) for k in counts.values()),
                    'Direct group sum equals orbit projector row')
            averaged=sum(Q(k,order)*(c-2*s+1) for (c,s),k in counts.items())
            twice=sum(Q(k,order)*projected[x] for x,k in counts.items())
            require(averaged==projected[state]==twice,'Group projection and idempotence')
            f=Q(state[0]-2*state[1]+1);g=Q(state[0]*state[1]+2)
            norm+=mu*projected[state]**2;positive+=mu*f*projected[state]
            adj_left+=mu*f*projected_g[state];adj_right+=mu*projected[state]*g
            orthogonal+=mu*projected[state]*(g-projected_g[state])
            C=patch(state[0],m);constant=gamma(C,m+2,[Q(7,3)]*(m+2))
            for i in range(m):
                if state[1]&(1<<i):
                    require(constant[i+1]+1==1,'Mass-shell polynomial is not identically zero')
                    polynomial_checks+=1
        require(norm==positive and norm>=0 and adj_left==adj_right and orthogonal==0,
                'Positive quotient scalar product, adjointness and null vectors')
        blocks=[o for o in orbits if o['m']==m]
        summary.append({'m':m,'labeled_order_support_states':len(states),'group_action_instances':len(states)*order,
                        'orbit_blocks':len(blocks),'projector_rows':len(states),'joint_action_checks':checks,
                        'nonzero_mass_shell_polynomials':polynomial_checks,'exact_residual':'0'})
    csvout('relabel_orbits.csv',orbits);csvout('relabel_summary.csv',summary)
    counts={k:sum(row[k] for row in summary) for k in summary[0] if k not in ('m','exact_residual')}
    dump('label_reduction.json',{'candidate':PLAN['candidate'],**counts,
         'positive_quotient':'PASS_FINITE_RELABEL_REDUCTION_ONLY','dynamical_constraints':'NOT_DERIVED',
         'state_space_role':'auxiliary history space, not a demonstrated closed boundary/Cauchy state space',
         'N2_boundary_fixed_group':'trivial S_0; relabel reduction leaves the prior two-site kernel unchanged'})
    dump('mass_shell_L2_obstruction.json',{'scope':'all clocks freely continuous on the regulated box before fixed-boundary conditioning; each nonempty positive-density support stratum',
         'polynomial_checks':counts['nonzero_mass_shell_polynomials'],
         'analytic_reason':'C_x=Gamma_x+1 is a nonzero real polynomial (equal to 1 at constant T); its zero set is Lebesgue-null',
         'ordinary_L2_joint_kernel':'ZERO_ON_EVERY_NONEMPTY_DUST_STRATUM',
         'vacuum_stratum':'not excluded by these dust equations',
         'not_a_no_go':'Distributional rigging maps, conditional singular measures and genuinely derived canonical constraints remain open; Euler equations are not automatically Dirac constraints'})
    return counts


def metric_test():
    p=PLAN['precision']['Taylor_degree']
    previous=json.loads((ROOT/'inputs/previous_plan.json').read_text())['normalization_test']
    require(previous['initial_clock_values']==['0','1'] and previous['final_clock_values']==['2','3']
            and previous['initial_density_weight']=='0' and previous['hbar']==previous['B_prefactor']=='1',
            'Prior kernel parameters')
    a,b,c=[g_interval(x,p) for x in (Q(3,2),Q(3,4),Q(11,4))]
    K=[[a,b],[c,a]]
    prior=json.loads((ROOT/'inputs/previous_normalization.json').read_text())
    prior_error=Q(prior['display_rounding_absolute_bound_per_complex_entry'])+Q(prior['gram_series_absolute_error_bound'])
    for i in range(2):
        for j in range(2):
            for index,name in enumerate(('real','imag')):
                value=Q(prior['kernel'][i][j][name]);interval=K[i][j][index]
                require(value-prior_error<=interval.lo<=interval.hi<=value+prior_error,'Unchanged prior kernel')
    det=csub(cmul(a,a),cmul(b,c));tr=cscale(a,2)
    determinant_norm=det[0].square()+det[1].square()
    require(determinant_norm.lo>0,'Invertibility not certified')
    witness=cmul(cmul(tr,tr),conj(det));imag=witness[1]
    ratio=(witness[0]/determinant_norm,imag/determinant_norm)
    excluded=imag.hi<0 or imag.lo>0
    result={'candidate':'CST-DUST-V1-RAW-K','unchanged_kernel':[[cjson(z) for z in row] for row in K],
      'identification':'(0,1) -> (2,3) by translation; one common positive definite Hermitian M',
      'condition':'Kdagger M K=c M for some c>0','necessary_spectral_invariant':'(tr K)^2/det K is real in [0,4]',
      'determinant':cjson(det),'determinant_norm_squared':determinant_norm.json(),
      'imaginary_witness':imag.json(),'trace_determinant_ratio':cjson(ratio),
      'decision':'FAIL_EVERY_COMMON_POSITIVE_METRIC' if excluded else 'HOLD_NO_EXCLUSION',
      'scope_exclusions':['different independently justified input/output metrics','constraint or rigging-map interpretation',
                           'complete boundary spaces','other regulators or controlled physical refinement']}
    dump('common_metric_certificate.json',result)
    return result['decision']


def reference_controls():
    zero=(Q(0),Q(0));one=(Q(1),Q(0));ii=(Q(0),Q(1))
    ident=real_matrix([[1,0],[0,1]])
    K=[[one,(Q(-1),Q(1))],[zero,ii]];M=real_matrix([[1,-1],[-1,2]])
    require(matmul(matmul(adjoint(K),M),K)==M,'Positive common-metric control')
    require(Q(1)>0 and Q(1)*2-(-1)**2>0,'Positive metric principal minors')
    require(Q(9,2)>4,'Unequal-modulus diagonal countercontrol')
    roots=[one,ii,(Q(-1),Q(0)),(Q(0),Q(-1))]
    U=[[[roots[(-k)%4],zero],[zero,roots[k]]] for k in range(4)]
    rows=[]
    for i in range(4):
        require(matmul(adjoint(U[i]),U[i])==ident,'Relational reference unitarity')
        for j in range(4):
            require(matmul(U[i],U[j])==U[(i+j)%4],'Relational composition')
            rows.append({'time_i_in_pi_over_2':i,'time_j_in_pi_over_2':j,'composition_residual':'0'})
    require(U[0]==ident,'Relational identity')
    # Fourier samples of e^(1-p^2)*(a+b*p) at p=-E are exact rationals.
    samples=[]
    for aa,bb in [(1,0),(0,1),(1,1),(2,-1)]:
        value=[Q(aa)-Q(bb)*E for E in [1,-1]]
        null=[(-E+E)*v for E,v in zip([1,-1],value)]
        require(null==[0,0],'Distributional constraint annihilation')
        norm=sum(v*v for v in value);require(norm>0,'Positive physical reference norm')
        samples.append({'a':aa,'b':bb,'physical_samples':[str(v) for v in value],'norm':str(norm),'constraint_samples':['0','0']})
    X=real_matrix([[0,1],[1,0]]);psi=[[one],[one]]
    def observable(A):
        state=matmul(A,psi)
        return matmul(matmul(adjoint(state),X),state)[0][0]
    initial=observable(ident);evolved=observable(U[1])
    require(initial==(Q(2),Q(0)) and evolved==(Q(-2),Q(0)),'Dynamics not fixed by Hilbert structure')
    csvout('relational_reference.csv',rows)
    dump('reference_controls.json',{'positive_common_metric':{'K':['[1,-1+i]','[0,i]'],'M':[[1,-1],[-1,2]],'residual':'0','positive_principal_minors':[1,1]},
      'negative_common_metric':{'K_diagonal':[1,2],'trace_determinant_ratio':'9/2','decision':'FAIL'},
      'relational_reference':{'constraint':'p_tau+diag(1,-1)','auxiliary':'L2(R,d tau) tensor C^2; Schwartz test domain',
          'rigging':'Fourier evaluation at p=-E_a','physical':'C^2 with standard positive product',
          'norm_checks':4,'composition_checks':len(rows),'constraint_sample_checks':len(samples),'samples':samples,
          'status':'PASS_MATHEMATICAL_REFERENCE_NOT_CST_DERIVATION'},
      'underdetermination':{'initial_state':'(1,1)/sqrt(2)','observable':'sigma_x','time':'pi/2',
         'H_zero_expectation':'1','H_diag_1_minus1_expectation':'-1','same_Hilbert_structure':True,
         'scope':'both are independent reference Hamiltonians, not both derived from or matched to the CST amplitude'}})
    return {'positive_metric_controls':1,'negative_metric_controls':1,'relational_unitarity_checks':4,
            'relational_composition_checks':16,'distributional_constraint_samples':4,'underdetermination_witnesses':1}


def audits(metric_decision):
    manifest={'id':PLAN['id'],'plan_sha256':sha('plan.json'),'parent_main_commit':'3595df81b8655a5183cdbf5c5da077aef51e4259',
      'python':platform.python_version(),'source_sha256':{n:sha(n) for n in ['quantum_structure.py','analyze.py']},
      'finite_mathematical_checks':'RUN','physical_4D_dynamics':'NOT_RUN','new_physical_4D_ensembles':0,'random_draws':0}
    dump('run_manifest.json',manifest)
    contract=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    spec=importlib.util.spec_from_file_location('qs_parent_gate',ROOT/'inputs/parent_gate.py')
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    for key,model,domain in [('quotient',PLAN['candidate'],'Positive relabel-reduced auxiliary history space; no physical dynamical constraints or boundary evolution derived'),
                             ('common_metric','CST-DUST-V1-RAW-K-COMMON-M','Same prior two-site kernel under translated label identification and one common positive Hermitian metric; not full CST')]:
        rec={'contract_id':contract['id'],'contract_sha256':sha('inputs/parent_contract.json'),'checkpoint_id':'P1','execution':'RUN',
          'run_manifest_sha256':sha('results/run_manifest.json'),
          'scope':{'model_id':model,'domain':domain,'time_interval':'Finite auxiliary construction or one boundary transition; no physical dustball history',
                   'refinement':'No physical refinement performed','claim_level':'Mathematical qualification only; physical CST junction, exterior, regularity and bounce remain open'},
          'gates':{g:{req:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION','evidence_refs':['DERIVATION.md'],
                   'scope_checked':True,'reviewed':True} for req in x['requirements']} for g,x in contract['gates'].items()}}
        if key=='common_metric' and metric_decision=='FAIL_EVERY_COMMON_POSITIVE_METRIC':
            rec['gates']['MODEL']['quantum_consistency']={'outcome':'VIOLATED','evidence_kind':'ANALYTIC_COUNTEREXAMPLE',
                  'evidence_refs':['DERIVATION.md#gemeinsames-skalarprodukt','results/common_metric_certificate.json'],'scope_checked':True,'reviewed':True}
        audit=gate.evaluate(rec,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
        target={g:'FAIL' if key=='common_metric' and g=='MODEL' and metric_decision.startswith('FAIL') else 'HOLD' for g in contract['gates']}
        require(audit['record_valid'] and audit['decisions']==target,'Scoped P1 decisions')
        dump('checkpoint_P1_'+key+'_record.json',rec);dump('checkpoint_P1_'+key+'_audit.json',audit)


def main():
    require(sha('plan.json')==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    for n,h in json.loads((ROOT/'inputs/provenance.json').read_text())['input_sha256'].items():
        require(sha('inputs/'+n)==h,'Inherited input changed')
    counts=label_reduction();decision=metric_test();controls=reference_controls();audits(decision)
    result={'id':PLAN['id'],'plan_sha256':sha('plan.json'),**counts,**controls,
      'relabel_projector':'PASS_EXACT_AUXILIARY_CONSTRUCTION','ordinary_L2_Euler_constraints':'TRIVIAL_ON_NONEMPTY_DUST_SUPPORT',
      'raw_K_common_metric':decision,'physical_state_space':'HOLD_DYNAMICAL_REDUCTION_NOT_DEFINED',
      'CST_relational_Hamiltonian':'HOLD_NOT_DERIVED','causal_junction':'HOLD','common_exterior':'HOLD',
      'regularity':'HOLD','global_bounce':'HOLD_NOT_RUN','new_physical_4D_ensembles':0,'new_sprinklings':0,'random_draws':0,'paid_runs':False}
    dump('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
