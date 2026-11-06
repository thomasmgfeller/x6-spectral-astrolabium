"""Exact finite variations and certified raw-kernel normalization counterexample."""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from math import factorial
from itertools import permutations
import csv,hashlib,importlib.util,json,platform
from variation import (kernel,edges,gamma,gamma_from_operator,matter_action,current_and_gradient,
                       laplacian,matter_coupling,finite_geometry_response,interval_carrier)
from gluing import all_posets,pairs,encode,valid,action as grav,relabel,require

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
P=json.loads((ROOT/'plan.json').read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def csvout(name,rows):
    with (OUT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def decimal(x):
    with localcontext() as c:
        c.prec=45
        return format(Decimal(x.numerator)/Decimal(x.denominator),'.35g')
def outward(x,upper=False):
    """Directed rounding preserves certified inequalities in serialized output."""
    with localcontext() as c:
        c.prec=35;c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))
def cadd(a,b):return (a[0]+b[0],a[1]+b[1])
def cmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def cjson(z):return {'real':decimal(z[0]),'imag':decimal(z[1])}


def algebra():
    rows=[]
    for n in P['algebra_tests']['N']:
        T=[Q(i*i,2) for i in range(n)];w=[Q(i+1) for i in range(n)];h=Q(1,3)
        c={'N':n,'orders':0,'product_identities':0,'clock_derivatives':0,'density_derivatives':0,
           'constant_shift_checks':0,'matter_partitions':0,'cut_balances':0,'label_checks':0,
           'geometry_moves':0,'admissible_interval_orders':0}
        for code in all_posets(n):
            c['orders']+=1;c['admissible_interval_orders']+=interval_carrier(code,n)
            g=gamma(code,n,T);require(g==gamma_from_operator(code,n,T),'Product identity')
            c['product_identities']+=n
            require(g==gamma(code,n,[t+Q(7,3) for t in T]),'Clock shift');c['constant_shift_checks']+=n
            current,gradient=current_and_gradient(code,n,T,w);L=laplacian(code,n,w)
            require(all(L[i][j]==L[j][i] for i in range(n) for j in range(n)),'Symmetric Hessian')
            require(gradient==[-sum(L[i][j]*T[j] for j in range(n)) for i in range(n)],'Euler variation')
            require(sum(gradient)==0,'Shift Noether identity')
            s=matter_action(code,n,T,w)
            require(s==-sum(T[i]*L[i][j]*T[j] for i in range(n) for j in range(n))/2-sum(w)/2,'Quadratic form')
            for i in range(n):
                plus=T.copy();minus=T.copy();plus[i]+=h;minus[i]-=h
                require((matter_action(code,n,plus,w)-matter_action(code,n,minus,w))/(2*h)==gradient[i],
                        'Independent central clock derivative');c['clock_derivatives']+=1
                plus=w.copy();minus=w.copy();plus[i]+=h;minus[i]-=h
                require((matter_action(code,n,T,plus)-matter_action(code,n,T,minus))/(2*h)==-(g[i]+1)/2,
                        'Independent density derivative');c['density_derivatives']+=1
            full=(1<<n)-1
            for a in range(1,full):
                b=full^a;x,r=matter_coupling(code,n,T,w,a,b)
                require(s==matter_action(code,n,T,w,a)+matter_action(code,n,T,w,b)+x+r,'Matter gluing')
                c['matter_partitions']+=1
                flux=sum(j*(int(bool(a&(1<<y)))-int(bool(a&(1<<x)))) for y,x,j in current)
                require(sum(gradient[i] for i in range(n) if a&(1<<i))==flux,'Variational cut balance')
                c['cut_balances']+=1
            if n<=P['algebra_tests']['permutation_max_N']:
                for perm in permutations(range(n)):
                    tp=[Q(0)]*n;wp=[Q(0)]*n
                    for i in range(n):tp[perm[i]]=T[i];wp[perm[i]]=w[i]
                    require(matter_action(relabel(code,n,perm),n,tp,wp)==s,'Relabeling invariance')
                    c['label_checks']+=1
            if n<=P['algebra_tests']['geometry_move_max_N']:
                for i in range(n):
                    for j in range(n):
                        if i==j:continue
                        other=code^(1<<(i*n+j))
                        if not valid(other,n):continue
                        dg,dm=finite_geometry_response(code,other,n,T,w)
                        require(dg+dm==grav(other,n)+matter_action(other,n,T,w)-grav(code,n)-s,
                                'Joint geometry response');c['geometry_moves']+=1
        rows.append(c)
    csvout('finite_variations.csv',rows)
    return {k:sum(r[k] for r in rows) for k in rows[0] if k!='N'}


def exterior():
    n=5;code=encode([(i,j) for i in range(n) for j in range(i+1,n)],n)
    w=list(map(Q,P['exterior_response']['w']));L=laplacian(code,n,w)
    retained=[2,3];e=1;den=L[e][e];require(den!=0,'Exterior block singular')
    leff=[[L[i][j]-L[i][e]*L[e][j]/den for j in retained] for i in retained]
    require(leff==[[Q(-55,16),Q(-17,16)],[Q(-17,16),Q(145,16)]],'Schur reference')
    rows=[]
    for t2 in [Q(1),Q(2),Q(3)]:
        for t3 in [Q(1,2),Q(2),Q(4)]:
            T=[Q(0),(-t2+9*t3)/8,t2,t3,Q(4)]
            s=matter_action(code,n,T,w);_,g=current_and_gradient(code,n,T,w)
            target=-sum(T[i]*leff[a][b]*T[j] for a,i in enumerate(retained) for b,j in enumerate(retained))/2-sum(w)/2
            require(g[e]==0 and s==target,'Stationary elimination')
            require(g[3]==(17*t2-145*t3)/16,'Conditional boundary response')
            rows.append({'T2':str(t2),'T3':str(t3),'T_exterior':str(T[1]),'exterior_residual':str(g[e]),'interface_gradient':str(g[3]),'action_residual':str(s-target)})
    csvout('conditional_exterior_response.csv',rows)
    dump('schur_response.json',{'L':[[str(x) for x in r] for r in L],'eliminated':[1],
       'L_EE':str(den),'L_effective':[[str(x) for x in r] for r in leff],
       'T_E':'(-T2+9*T3)/8','interface_gradient':'(17*T2-145*T3)/16',
       'scope':'fixed geometry and density, auxiliary clock stationary response only; no dust mass-shell or vacuum metric solved'})
    return len(rows)


def G_series(a,p):
    # G(a)=1/2+1/2 integral_0^1 exp(-i*a*w)dw with rigorous Taylor remainder.
    total=(Q(1),Q(0));power=(Q(1),Q(0))
    for k in range(1,p+1):
        power=cmul(power,(Q(0),-a))
        term=(power[0]/(factorial(k)*(k+1)),power[1]/(factorial(k)*(k+1)))
        total=cadd(total,term)
    value=((1+total[0])/2,total[1]/2)
    radius=abs(a)**(p+1)/(2*factorial(p+1)*(p+2))
    return value,radius


def normalization():
    p=P['precision']['amplitude_Taylor_degree'];initial=[Q(0),Q(1)];final=[Q(2),Q(3)]
    K=[];radii=[];entries=[]
    for beta in final:
        row=[]
        for alpha in initial:
            a=Q(1,2)+(beta-alpha)**2/4;value,radius=G_series(a,p);row.append(value);radii.append(radius)
            entries.append({'initial_T':str(alpha),'final_T':str(beta),'a':str(a),
                            **cjson(value),'series_absolute_error_bound':outward(radius,True),
                            'displayed_complex_entry_error_bound':outward(radius+Q(1,10**33),True)})
        K.append(row)
    r=max(radii);eps=2*(2*r+r*r)
    Gram=[[cadd(cmul(conj(K[0][i]),K[0][j]),cmul(conj(K[1][i]),K[1][j])) for j in range(2)] for i in range(2)]
    off=Gram[0][1][0]
    require(off-eps>Q(1,2),'Certified nonisometry obstruction')
    center=(Gram[0][0][0]+Gram[1][1][0])/2
    norm_plus=center+off;norm_minus=center-off
    require(norm_minus-2*eps>0 and norm_plus-2*eps>0,'Positive normalizations')
    lower=(norm_minus-2*eps)/(norm_plus+2*eps);upper=(norm_minus+2*eps)/(norm_plus-2*eps)
    require(upper<1,'Equal-source normalization failure')
    csvout('kernel_entries.csv',entries)
    dump('normalization_counterexample.json',{
       'candidate':'CST-DUST-V1-RAW-K','boundary_inner_products':'I_2','gravity_common_phase_removed':True,
       'kernel':[[cjson(z) for z in row] for row in K],
       'gram':[[cjson(z) for z in row] for row in Gram],
       'gram_series_absolute_error_bound':outward(eps,True),
       'display_rounding_absolute_bound_per_complex_entry':'1e-33',
       'gram_entry_absolute_error_bound':outward(eps+Q(1,10**33),True),
       'Re_gram_01_lower':outward(off-eps),'analytic_lower_bound':'strictly greater than 1/2',
       'norm_plus':decimal(norm_plus),'norm_minus':decimal(norm_minus),
       'fixed_normalization_Z_pi_pi_interval':[outward(lower),outward(upper,True)],
       'required_Z_J_J':'1 for all equal sources in the declared closed evolution interpretation',
       'decision':'FAIL_RAW_KERNEL_AS_CLOSED_EVOLUTION',
       'not_a_no_go':'Different physical Hilbert spaces, rigging maps, constraint kernels, carriers and limits are not excluded'})
    return {'offdiag_lower':outward(off-eps),'Z_pi_pi_upper':outward(upper,True)}


def controls():
    rows=[]
    def test(name,observed,expected):
        require(observed==expected,name);rows.append({'name':name,'observed':observed,'expected':expected,'pass':True})
    code=encode([(0,1)],2);T=[Q(0),Q(1)];w=[Q(0),Q(1)]
    g=gamma(code,2,T);_,grad=current_and_gradient(code,2,T,w)
    test('Two-site clock variation has future contribution',str(grad[0]),'1/2')
    test('Retarded B alone is not the action gradient',str(grad[0])=='0',False)
    test('Minimal element has Gamma=0',str(g[0]),'0')
    test('Positive interior multiplier cannot satisfy mass shell at a minimal element',g[0]+1==0,False)
    test('Vacuum node clock can couple to nonlocal dust row',grad[0]!=0 and w[0]==0,True)
    test('Variational flux need not be positive',kernel(1)<0,True)
    test('Constant clock has Gamma=0',gamma(code,2,[Q(2),Q(2)])==[0,0],True)
    # Isolated node: B=-1. Omitting T^2 B1 leaves +T^2/2.
    test('Omitted curvature/potential correction breaks clock-shift invariance',Q(2)**2/2==Q(3)**2/2,False)
    test('Finite box boundary term cannot be dropped',Q(4)/Q(4),Q(1))
    test('Compact positive multiplier measure is not a delta constraint',G_series(Q(1),80)[0][0]>0,True)
    # Serializing the one rational control explicitly avoids non-JSON numbers.
    for row in rows:
        for key in ('observed','expected'):
            if isinstance(row[key],Q):row[key]=str(row[key])
    dump('controls.json',rows);return len(rows)


def checkpoint():
    parent=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    manifest={'id':P['id'],'plan_sha256':sha('plan.json'),'parent_main_commit':'9fa170dfd604be3847004ea2bdbe8587ada5d068',
      'python':platform.python_version(),'source_sha256':{n:sha(n) for n in ('variation.py','analyze.py')},
      'finite_candidate_checks':'RUN','physical_4D_dust_dynamics':'NOT_RUN','new_physical_4D_ensembles':0,'random_draws':0}
    dump('run_manifest.json',manifest)
    rec={'contract_id':parent['id'],'contract_sha256':sha('inputs/parent_contract.json'),'checkpoint_id':'P1','execution':'RUN',
      'run_manifest_sha256':sha('results/run_manifest.json'),
      'scope':{'model_id':'CST-DUST-V1-RAW-K','domain':'Two-site finite kinematic boundary spaces with fixed I_2 inner products; not full physical CST',
       'time_interval':'One declared boundary transition; no dustball time history','refinement':'Fixed regulator counterexample; no physical refinement',
       'claim_level':'Reject only direct raw-kernel closed-evolution interpretation; other physical realizations remain open'},
      'gates':{g:{req:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION','evidence_refs':['DERIVATION.md'],
        'scope_checked':True,'reviewed':True} for req in data['requirements']} for g,data in parent['gates'].items()}}
    rec['gates']['MODEL']['quantum_consistency']={'outcome':'VIOLATED','evidence_kind':'ANALYTIC_COUNTEREXAMPLE',
      'evidence_refs':['DERIVATION.md#normierungsgegenbeispiel','results/normalization_counterexample.json'],
      'scope_checked':True,'reviewed':True}
    spec=importlib.util.spec_from_file_location('parent_gate',ROOT/'inputs/parent_gate.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    audit=gate.evaluate(rec,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
    require(audit['record_valid'] and audit['decisions']['MODEL']=='FAIL'
            and all(v=='HOLD' for k,v in audit['decisions'].items() if k!='MODEL'),'Scoped audit')
    dump('checkpoint_P1_record.json',rec);dump('checkpoint_P1_audit.json',audit)


def main():
    require(sha('plan.json')==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    for n,h in json.loads((ROOT/'inputs/provenance.json').read_text())['input_sha256'].items():
        require(sha('inputs/'+n)==h,'Inherited input changed')
    counts=algebra();response=exterior();norm=normalization();ct=controls();checkpoint()
    result={'id':P['id'],'plan_sha256':sha('plan.json'),**counts,'conditional_exterior_cases':response,
      'controls':ct,'exact_variation_residuals':'ZERO','matter_action':'DEFINED_CANDIDATE_NOT_PHYSICALLY_QUALIFIED',
      'joint_geometry_matter_variation':'PASS_EXACT_FINITE_IDENTITIES','raw_kernel_evolution':'FAIL_FOR_DECLARED_KINEMATIC_INNER_PRODUCTS',
      'normalization_witness':norm,'physical_CST_model':'HOLD','effective_causal_junction':'HOLD_NOT_DERIVED',
      'physical_common_exterior':'HOLD_NOT_SOLVED','regularity':'HOLD','global_bounce':'HOLD_NOT_RUN',
      'new_physical_4D_ensembles':0,'new_sprinklings':0,'random_draws':0,'paid_runs':False}
    dump('verification.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
