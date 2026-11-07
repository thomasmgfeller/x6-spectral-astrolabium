#!/usr/bin/env python3
"""Exact finite tests with an independently inherited direct-action implementation."""
import hashlib,itertools,json,math,sys
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import memory as m
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
import gluing as reference
import variation as matter_reference
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def fields(n,variant):
    T=[Q(-3)]+[Q(i-2,3) if variant==0 else Q(i*i-3*i,7) for i in range(1,n)]
    w=[Q(0)]+[[Q(0),Q(1,2),Q(3,4)][(i+variant)%3] for i in range(1,n)]
    return T,w
def encode_poly(poly):return {str(k):str(v) for k,v in sorted(poly.items()) if v}
def main():
    plan=json.loads((ROOT/'plan.json').read_text());ph=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(ph==(ROOT/'plan.sha256').read_text().split()[0],'Plan hash')
    prov=json.loads((ROOT/'inputs/provenance.json').read_text())
    for name,d in prov['files'].items():require(hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==d['sha256'],'Input '+name)
    counts=[len(m.natural_orders(n)) for n in range(6)]
    require(counts==[1,1,2,7,40,357],'Natural-order census')
    checks={'ideal_extensions':0,'rational_action_cases':0,'direct_gravity_comparisons':0,'linear_extension_counts':0,
            'growth_exchange_cases':0,'growth_exchange_field_cases':0,'terminal_closures':0}
    for n in range(6):
        for p in m.natural_orders(n):
            brute=sum(all(pos[i]<pos[j] for j,s in enumerate(p) for i in m.bits(s))
                      for order in itertools.permutations(range(n)) for pos in [{v:k for k,v in enumerate(order)}])
            require(m.extensions(p)==brute,'Linear extension independent count');checks['linear_extension_counts']+=1
            a=m.with_anchor(p);cl=m.with_anchor(p,True)
            require(m.gravity(cl)==reference.action(m.code(cl),len(cl)),'Direct gravity closure');checks['direct_gravity_comparisons']+=1
            for variant in range(2):
                T,w=fields(len(a),variant);g,s=m.increment(a,(1<<len(a))-1,T,Q(3),Q(0))
                require(g==m.gravity(cl)-m.gravity(a) and s==m.matter(cl,T+[Q(3)],w+[Q(0)])-m.matter(a,T,w),'Terminal closure')
                checks['terminal_closures']+=1
            if n<5:
                for ideal in m.ideals(p):
                    child=p+(ideal,);a=m.with_anchor(p);b=m.with_anchor(child);past=(ideal<<1)|1
                    require(b==a+(past,),'Anchor extension');checks['ideal_extensions']+=1
                    for variant in range(2):
                        T,w=fields(len(a),variant);t=Q(1,3) if variant==0 else Q(5,4)
                        for new_w in [Q(0),Q(1,2),Q(3,4)]:
                            g,s=m.increment(a,past,T,t,new_w)
                            require(g==reference.action(m.code(b),len(b))-reference.action(m.code(a),len(a)),'Gravity increment')
                            direct=matter_reference.matter_action(m.code(b),len(b),T+[t],w+[new_w])-matter_reference.matter_action(m.code(a),len(a),T,w)
                            require(s==direct and s==m.matter(b,T+[t],w+[new_w])-m.matter(a,T,w),'Matter increment')
                            checks['rational_action_cases']+=1
            if n>=2 and not p[-1]>>(n-2)&1:
                order=tuple(range(n-2))+(n-1,n-2);q=m.relabel(p,order)
                require(q in m.natural_orders(n),'Exchange allowed')
                for endpoint in [p,q]:
                    e=m.extensions(endpoint[:-2]);r1=Q(e,m.extensions(endpoint[:-1]));r2=Q(m.extensions(endpoint[:-1]),m.extensions(endpoint))
                    require(r1*r2==Q(e,m.extensions(p)),'Counting exchange')
                checks['growth_exchange_cases']+=1
                for variant in range(2):
                    a=m.with_anchor(p);T,w=fields(len(a),variant)
                    full_order=(0,)+tuple(i+1 for i in order)
                    tq=[T[i] for i in full_order];wq=[w[i] for i in full_order]
                    g0=m.gravity(a);s0=m.matter(a,T,w)
                    require(m.gravity(m.with_anchor(q))==g0 and m.matter(m.with_anchor(q),tq,wq)==s0,'Exchange full action')
                    base=m.with_anchor(p[:-2]);sumg=Q(0);sums=Q(0)
                    for k in [n-1,n]:
                        before=m.with_anchor(p[:k-1]);now=m.with_anchor(p[:k]);g,s=m.increment(before,now[-1],T[:k],T[k],w[k]);sumg+=g;sums+=s
                    require(sumg==g0-m.gravity(base) and sums==s0-m.matter(base,T[:n-1],w[:n-1]),'Exchange telescope')
                    checks['growth_exchange_field_cases']+=1
    measure=[]
    for n in range(6):
        natural=defaultdict(Q);naive=defaultdict(Q);direct=defaultdict(Q)
        for p in m.natural_orders(n):
            action=m.gravity(m.with_anchor(p,True));natural[action]+=Q(1,m.extensions(p));naive[action]+=1
        for value in reference.all_posets(n):
            p=m.from_code(value,n);c=m.with_anchor(p,True)
            direct[reference.action(m.code(c),len(c))]+=Q(1,math.factorial(n))
        require(dict(natural)==dict(direct),'Exact finite measure polynomial')
        measure.append({'internal_elements':n,'natural_orders':counts[n],'arbitrary_labeled_orders':len(reference.all_posets(n)),
                        'corrected_equals_covariant':True,'naive_equals_covariant':dict(naive)==dict(direct),
                        'covariant_polynomial':encode_poly(direct),'naive_polynomial':encode_poly(naive)})
    collars=[]
    for r in range(1,9):
        # Anchor a, hidden y, visible chain c1..cr; z sees only a,y.
        n=r+2;a=tuple((1<<i)-1 for i in range(n));past=3;b=a+(past,)
        base=[Q(-1),Q(1,4)]+[1+Q(j,r+1) for j in range(1,r+1)]
        changed=base.copy();changed[1]=Q(3,4);old_w=[Q(0)]*n
        s0=m.matter(b,base+[Q(1)],old_w+[Q(1,2)]);s1=m.matter(b,changed+[Q(1)],old_w+[Q(1,2)])
        require(base[2:]==changed[2:] and m.matter(a,base,old_w)==m.matter(a,changed,old_w)==0,'Identical collar and old action')
        require(s1-s0==Q(1,16),'Deep vacuum memory witness')
        require(m.increment(a,past,changed,Q(1),Q(1,2))[1]-m.increment(a,past,base,Q(1),Q(1,2))[1]==Q(1,16),'Signature witness')
        collars.append({'visible_top_layers':r,'hidden_vacuum_clock_before':'1/4','after':'3/4','same_old_action':True,'delta_new_matter_action':'1/16'})
    chain=(0,1);anti=(0,0)
    require(m.norm_factor((0,))==Q(5,4) and m.norm_factor(chain)==Q(49,36) and m.norm_factor(anti)==2,'Norm factors')
    endpoint_a=(0,1,0);endpoint_b=(0,0,1)
    def normalized_square(p):
        out=Q(1,m.extensions(p)**2)
        for k in range(len(p)):out/=m.norm_factor(p[:k])
        return out
    sa,sb=normalized_square(endpoint_a),normalized_square(endpoint_b)
    require(m.extensions(endpoint_a)==m.extensions(endpoint_b)==3 and sa==Q(16,245) and sb==Q(2,45),'Local normalization changes path weights')
    pre=Q(1)/(1+Q(1,4));post=m.norm_factor(chain)/(m.norm_factor(chain)+Q(1,4)*m.norm_factor(anti))
    require(pre==Q(4,5) and post==Q(49,67) and pre!=post,'Reachable growth-record event changes under scalar renormalization')
    metric_rows=[];metric_checks=0
    for horizon in [3,4]:
        for name,terminal in [('unit',lambda p:Q(1)),('one_plus_relations',lambda p:Q(1+sum(x.bit_count() for x in p)))]:
            weights=m.pullback(horizon,terminal)
            for n in range(horizon):
                for p in m.natural_orders(n):
                    direct=sum((Q(m.extensions(p),m.extensions(p+(s,)))**2*weights[n+1,p+(s,)] for s in m.ideals(p)),Q(0))
                    require(weights[n,p]==direct and direct>0,'Positive terminal pullback');metric_checks+=1
            metric_rows.append({'horizon':horizon,'terminal':name,'chain_two':str(weights[2,chain]),'antichain_two':str(weights[2,anti]),'empty':str(weights[0,()])})
    results={
      'finite_growth.json':{'natural_counts':counts,'total_natural_orders':sum(counts),'checks':checks,
                           'field_arithmetic':'rational; A=hbar=1; kappa retained as formal phase coefficient'},
      'counting_measure.json':{'sectors':measure,'statement':'1/m! all-label sum equals natural-label sum weighted 1/e; invariant integrands and symmetric field measures required'},
      'memory_counterexamples.json':{'family':'Same top r internal layers, same initial anchor, same full order and old action; hidden vacuum clock still couples to a new branch','cases':collars,
                                    'scope':'All admissible future ideals; not a no-go for restricted carriers or controlled approximations'},
      'boundary_norms.json':{'counting_product_norm_factors':{'one_internal':'5/4','chain_two':'49/36','antichain_two':'2'},
        'equal_corrected_amplitudes_before_normalization':'1/3',
        'locally_normalized_path_weight_squares':[str(sa),str(sb)],
        'reachable_growth_record_event':{'initial_chain_fraction':str(pre),'after_one_extension':str(post),
          'scope':'Orthogonal natural-label prefix records; not qualified covariant physical events'},
        'fixed_horizon_positive_metrics':metric_rows,'metric_checks':metric_checks,
        'full_past_lift':'Retains old fields; delta-type kernel in old variables; previous bounded-kernel compactness hypotheses do not apply.',
        'physical_terminal_metric':'NOT_SELECTED'},
      'verification.json':{'audit':plan['id'],'source_commit':plan['source_commit'],'plan_sha256':ph,'source_files':len(prov['files']),
        'scoped_decisions':{'FULL_PAST_ACTION_UPDATE':'PASS_EXACT','NATURAL_LABEL_COUNTING_REWRITE':'PASS_CONDITIONAL_ON_INHERITED_MEASURE',
           'FIXED_TOP_LAYER_COLLAR_EXACT_CLOSURE':'FAIL_FOR_ALL_FUTURE_IDEALS','COMMON_SCALAR_COUNTING_NORM':'FAIL',
           'LOCAL_NORMALIZATION_PRESERVES_ORIGINAL_AMPLITUDES':'FAIL','FIXED_HORIZON_PULLBACK':'PASS_CONDITIONAL_ON_CHOSEN_TERMINAL_PRODUCT',
           'PHYSICAL_BOUNDARY_PRODUCT_AND_INFINITE_CONTINUATION':'HOLD'},
        'physical_decisions':plan['physical_decisions'],'formal_proof_checker':False,'new_dynamical_CST_ensembles':False}}
    for name,data in results.items():(ROOT/'results'/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'PASS','natural_counts':counts,'checks':checks,'metric_checks':metric_checks,'collar_cases':len(collars),'norms':results['boundary_norms.json']},indent=2))
if __name__=='__main__':main()
