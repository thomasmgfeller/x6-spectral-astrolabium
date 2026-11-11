"""Independent global-order oracle, exact reconstruction checks and Arb controls."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json
import sympy as sp
from flint import arb, acb, ctx
from inputs import prior_core as pc
from sewing import make_packet, sew_packets, local_action, transitive_closure, doubled_hessian, action_components, influence_components

ROOT=Path(__file__).resolve().parent
LEFT=(0,1,2,3,4); RIGHT=(3,4,5,6,7); SEAM=(3,4)
INNER=(2,3,4,5); OUTER=(0,1,6,7)

def write(path,value):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')

def packets(l,r):
    return (make_packet('left',LEFT,pc.relations(l),SEAM,(0,1)),
            make_packet('right',RIGHT,{(i+3,j+3) for i,j in pc.relations(r)},SEAM,(6,7)))

def oracle(l,r):
    rel=transitive_closure(range(8),pc.relations(l)|{(i+3,j+3) for i,j in pc.relations(r)})
    return local_action(range(8),rel),rel

def matrix(action):return sp.Matrix(doubled_hessian(action))/2

def gaussian_atom(action,epsilon='0',order=OUTER+INNER):
    """Entire eight-field integral, including 1/128 and the gravity phase.

    Outer h0*h0 contributes 1/pi. (2*pi)^4/pi=16*pi^3.
    Product square roots of accretive Gaussian pivots fixes the phase.
    The epsilon=0 value is the continuous Abel limit, certified pivotwise.
    """
    h=doubled_hessian(action);eps=arb(epsilon)
    if eps<0:raise ValueError('negative regulator')
    q=[[acb((arb(1) if i in OUTER else eps) if i==j else 0,
             -pc.beta()*arb(h[i][j])/2) for j in order] for i in order]
    root=acb(1)
    for k in range(8):
        pivot=q[k][k]
        if eps>0:
            if not pivot.real>0:raise ArithmeticError('positive-regulator accretivity failed')
        elif not(pivot.real>0 or pivot.imag>0 or pivot.imag<0):
            raise ArithmeticError('Abel pivot touches zero or the square-root cut')
        root*=pivot.sqrt(analytic=True)
        for i in range(k+1,8):
            for j in range(k+1,8):q[i][j]-=q[i][k]*q[k][j]/pivot
    return (arb.pi()**3/8)*acb(0,action['F4']).exp()/root

def packed(z):
    return {'real':z.real.str(32,more=True),'imag':z.imag.str(32,more=True)}

def display(z):
    real=format(float(z.real.mid()),'.12f');imag=format(float(z.imag.mid()),'.12f')
    er=max(float(abs(z.real-arb(real)).upper()),float(abs(z.imag-arb(imag)).upper()))
    if er>=1e-12:raise ArithmeticError('printed component error exceeds 1e-12')
    return {'real':real,'imag':imag,'absolute_component_error_bound':'1e-12','arb_enclosure':packed(z)}

def bypass_witness():
    for l in pc.histories():
        for r in pc.histories():
            action,rel=oracle(l,r)
            for a in (0,1,2):
                for b in (5,6,7):
                    if (a,b) in rel:continue
                    more=transitive_closure(range(8),rel|{(a,b)})
                    if {x for x in more if x[0] in LEFT and x[1] in LEFT}!=pc.relations(l):continue
                    if {x for x in more if x[0] in RIGHT and x[1] in RIGHT}!={(i+3,j+3) for i,j in pc.relations(r)}:continue
                    other=local_action(range(8),more)
                    if other!=action:
                        return {'codes':[l,r],'added_relation':[a,b],
                                'minimal_F4':action['F4'],'alternative_F4':other['F4'],
                                'minimal_pair_terms':action['pair_terms'],
                                'alternative_pair_terms':other['pair_terms'],
                                'same_local_restrictions':True}
    raise ArithmeticError('expected bypass ambiguity not found')

def run():
    ctx.prec=192
    codes=pc.histories();records=[];singular=[];counts=Counter();sums={e:acb(0) for e in ('0','1','1/7')}
    positive_checks=0;max_field_error=Fraction(0)
    fields={kind:{str(i):str(value(i)) for i in range(8)} for kind,value in
            [('t',lambda i:Fraction(i-4,5)),('r',lambda i:Fraction(i,8)),('q',lambda i:Fraction(i*i-5,7))]}
    for l in codes:
        for r in codes:
            left,right=packets(l,r);joined=sew_packets(left,right)
            direct,rel=oracle(l,r)
            if joined['joint_action']!=direct:raise ArithmeticError('global-order reconstruction differs')
            # Equality of pair coefficients gives every monomial of all three sectors,
            # not merely agreement at the sample fields below.
            a=action_components(direct,fields);b=action_components(joined['joint_action'],fields)
            max_field_error=max(max_field_error,max(abs(Fraction(a[k])-Fraction(b[k])) for k in a))
            h=matrix(direct);hi=h.extract(INNER,INNER);det=hi.det();rank=4
            if det==0:
                rank=hi.rank();stack_rank=hi.col_join(h.extract(OUTER,INNER)).rank()
                if rank!=3 or stack_rank!=4:raise ArithmeticError('unsupported scalar null mode')
                singular.append({'codes':[l,r],'rank_inner':rank,'rank_with_boundary_coupling':stack_rank,
                                 'null_vector':[str(x) for x in hi.nullspace()[0]]})
            nonzero=sum(x['coefficient']!=0 for x in joined['cross_intervals']);counts[nonzero]+=1
            row={'codes':[l,r],'F4':direct['F4'],'delta_F4':joined['delta_F4'],
                 'nonzero_cross_pairs':nonzero,'det_HII':str(det),'rank_HII':rank}
            for eps in sums:
                value=gaussian_atom(direct,eps)
                if eps!='0':
                    staged=gaussian_atom(joined['joint_action'],eps,(2,5,3,4)+OUTER)
                    if not value.overlaps(staged):raise ArithmeticError('integration order control failed')
                    positive_checks+=1
                sums[eps]+=value/1089
            records.append(row)
    left,right=packets(25500,25500);joined=sew_packets(left,right);direct,_=oracle(25500,25500)
    naive={'vertices':list(range(8)),
           'pair_terms':sorted(left['local_action']['pair_terms']+right['local_action']['pair_terms']),
           'F4':left['local_action']['F4']+right['local_action']['F4']-2}
    joint_value=gaussian_atom(direct);naive_value=gaussian_atom(naive)
    cross_nonzero=[x for x in joined['cross_intervals'] if x['coefficient']]
    prior=json.loads((ROOT/'inputs/prior_gluing.json').read_text())
    if [(x['source'],x['target'],x['interval_count_capped'],x['coefficient']) for x in cross_nonzero]!=[tuple(x) for x in prior['geometry']['nonzero_cross_pairs']]:
        raise ArithmeticError('frozen five-term result changed')
    for name,value in [('joint',joint_value),('sewn_local_action',naive_value)]:
        old=prior['kernel_comparison'][name]['certified_ball']
        if not value.overlaps(acb(arb(old['real']),arb(old['imag']))):raise ArithmeticError('frozen scalar control differs')
    null_example=singular[0];ha,_=oracle(*null_example['codes']);hh=matrix(ha)
    null_vector=sp.Matrix([sp.Rational(x) for x in null_example['null_vector']])
    null_example=dict(null_example,boundary_constraint_over_beta=[str(x) for x in (null_vector.T*hh.extract(INNER,OUTER))])
    results={'status':'PASS','scope':'minimal transitive completions of the 33 x 33 labelled AA controls; product weight 1/1089',
             'pair_count':len(records),'exact_joint_action_matches':len(records),
             'exact_action_residual':'0 for all real fields and all density strata',
             'sample_rational_field_residual':str(max_field_error),
             'nonzero_cross_pair_histogram':dict(sorted(counts.items())),
             'nonsingular_inner_blocks':len(records)-len(singular),'singular_inner_blocks':len(singular),
             'singular_rank':3,'all_singular_null_modes_couple_to_boundary':True,
             'singular_example':null_example,'positive_regulator_integration_order_checks':positive_checks,
             'fixed_25500':{'five_nonzero_cross_intervals':cross_nonzero,'delta_F4':joined['delta_F4'],
                 'joint_F4':direct['F4'],'naive_F4':naive['F4'],
                 'joint_all_atom':display(joint_value),'naive_all_atom':display(naive_value),
                 'difference_all_atom':display(joint_value-naive_value),
                 'measure_without_factor_two':display(joint_value/2)},
             'full_1089_sum_all_atom':{eps:display(value) for eps,value in sums.items()},
             'all_atom_regulator_errors_vs_Abel':{eps:abs(value-sums['0']).str(24,more=True) for eps,value in sums.items() if eps!='0'},
             'numerical_scope':'all eight densities at atoms and normalized atom/ground outer packets; clocks integrate to 1. Positive-density sectors are covered by the exact action identity, not numerically integrated here.',
             'bypass_ambiguity':bypass_witness()}
    write('examples/left.json',left);write('examples/right.json',right);write('examples/fields.json',fields)
    joined['bound_action']=action_components(joined['joint_action'],fields)
    joined['sewing_phase_components']=influence_components(joined,fields)
    write('results/reconstructed_full_layer.json',joined)
    write('results/verification.json',results);write('results/history_pairs.json',records);write('results/singular_pairs.json',singular)
    print(json.dumps({k:results[k] for k in ('status','pair_count','exact_joint_action_matches','singular_inner_blocks','positive_regulator_integration_order_checks','full_1089_sum_all_atom')},indent=2))

if __name__=='__main__':run()
