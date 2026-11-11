#!/usr/bin/env python3
"""Exact finite CST-DUST source benchmark; standard library only, offline."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations, product
from collections import Counter
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'inputs'))
import gluing as g
import variation as v
import quantum_structure as q

def canonical(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2)+'\n'

def matrix_product(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def rational_matrix(a):
    return [[str(x) for x in row] for row in a]

def exact_complex_matrix(a):
    return [[{'real': str(x[0]), 'imag': str(x[1])} for x in row] for row in a]

def quadratic(x, a):
    return sum(x[i]*a[i][j]*x[j] for i in range(len(x)) for j in range(len(x)))

def run():
    controls = []
    def check(name, condition, scope):
        if not condition:
            raise RuntimeError('FAILED: '+name)
        controls.append({'id': name, 'result': 'PASS', 'scope': scope})

    provenance = json.loads((ROOT/'provenance.json').read_text())
    for src in provenance['sources']:
        if src['local_copy']:
            b=(ROOT/src['local_copy']).read_bytes()
            sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            check('SOURCE:'+src['local_copy'], sha==src['git_blob_sha'], 'exact_upstream_blob_identity')

    # Recompute the four fixed-representative fibers, not a probability matrix.
    prior=json.loads((ROOT/'inputs/gluing_kernels_2_plus_2.json').read_text())
    types=[('antichain', 0, 2), ('chain', g.encode([(0,1)],2), 1)]
    orders=g.all_posets(4)
    check('GEOM:219-orders', len(orders)==219, 'finite_order_enumeration')
    kernels=[]
    for an, a, aa in types:
        for bn, b, ab in types:
            poly=Counter()
            for c in orders:
                if g.induced(c,4,3)==a and g.induced(c,4,12)==b:
                    delta=g.action(c,4)-g.action(a,2)-g.action(b,2)
                    cross,regrade=g.coupling(c,4,3,12)
                    if delta!=cross+regrade:
                        raise RuntimeError('Full interval correction lost')
                    poly[delta]+=1
            row={'A':an,'B':bn,'Aut_A':aa,'Aut_B':ab,'F_A':g.action(a,2),'F_B':g.action(b,2),
                 'admissible_cross_orders':sum(poly.values()),
                 'kernel':[{'power':e,'coefficient':str(poly[e])} for e in sorted(poly)],
                 'readouts':{z:[str(x) for x in g.poly_readout(poly,z)] for z in ['1','-1','i']}}
            old=next(x for x in prior['kernels'] if x['A']==an and x['B']==bn)
            check('GEOM:fiber:'+an+':'+bn, row==old, 'full_polynomial_and_readouts_against_archived_result')
            kernels.append(row)
    direct=Counter()
    for c in orders: direct[g.action(c,4)]+=Q(1,4)
    composed=Counter()
    for row in kernels:
        for term in row['kernel']:
            composed[term['power']+row['F_A']+row['F_B']]+=Q(term['coefficient'])/(row['Aut_A']*row['Aut_B'])
    check('GEOM:weighted-composition', dict(direct)==dict(composed), 'fixed_marked_counting_measure_only')
    K=[[(Q(-13),Q(0)),(Q(5),Q(-11))],[(Q(5),Q(-11)),(Q(2),Q(8))]]
    KdagK=q.matmul(q.adjoint(K),K)
    expected=[[(Q(315),Q(0)),(Q(-143),Q(205))],[(Q(-143),Q(-205)),(Q(214),Q(0))]]
    check('GEOM:raw-I2-diagnostic',KdagK==expected,'diagnostic_with_declared_I2_not_physical_metric')
    check('GEOM:single-phase-zero',kernels[1]['readouts']['-1']==['0','0'] and kernels[1]['readouts']['i']==['5','-11'],
          'geometric_cancellation_not_stratum_superselection')
    geometry={'dataset_id':'CST-DUST-RKB1-GEOM','interpretation':'combinatorial_bilinear_gluing_kernel',
              'boundary_index_meaning':'fixed induced inner order types A/B, not initial/final time slices',
              'physical_clock':None,'geometric_basis':['antichain','chain'],'enumerated_labeled_orders':219,
              'kernels':kernels,'K_at_i':exact_complex_matrix(K),'raw_I2_adjoint_product':exact_complex_matrix(KdagK),
              'physical_metric':'NOT_DERIVED','hamiltonian':'NOT_EXTRACTED'}

    # Exact label averaging for m=0,1,2, including all discrete support marks.
    # The continuous clocks/positive weights are integrated out only for
    # functions constant within each stratum, as in the source construction.
    quotient=[]
    total_states=0;total_orbits=0
    for m in range(3):
        n=m+2
        carrier=[c for c in g.all_posets(n) if v.interval_carrier(c,n)]
        states=[(c,mask) for c in carrier for mask in range(1<<m)]
        idx={state:i for i,state in enumerate(states)}
        group=list(permutations(range(1,m+1)))
        def moved(state, perm):
            c,mask=state; full=(0,)+perm+(n-1,)
            newmask=sum(1<<(full[j]-1) for j in range(1,m+1) if mask & (1<<(j-1)))
            return g.relabel(c,n,full),newmask
        orbits=[];remaining=set(states)
        while remaining:
            rep=min(remaining); orbit=sorted({moved(rep,p) for p in group})
            stabilizer=sum(moved(rep,p)==rep for p in group)
            orbits.append({'representative':list(rep),'indices':[idx[x] for x in orbit],
                           'orbit_size':len(orbit),'stabilizer':stabilizer,
                           'positive_marks':rep[1].bit_count(),
                           'indicator_norm_squared':str(Q(len(orbit),len(group)*(1<<m)))})
            remaining.difference_update(orbit)
        N=len(states);P=[[Q(0) for _ in states] for _ in states]
        for j,state in enumerate(states):
            for p in group:P[idx[moved(state,p)]][j]+=Q(1,len(group))
        symmetric=all(P[i][j]==P[j][i] for i in range(N) for j in range(N))
        check(f'LABEL:m{m}:projector',symmetric and matrix_product(P,P)==P,'finite_label_constraints_only')
        for orbit in orbits:
            check(f'LABEL:m{m}:orbit{orbit["indices"][0]}',
                  orbit['orbit_size']*orbit['stabilizer']==len(group) and
                  Q(orbit['indicator_norm_squared'])==Q(1,(1<<m)*orbit['stabilizer']),
                  'orbit_stabilizer_measure_identity')
        indicator_gram=[]
        point_weight=Q(1,len(group)*(1<<m))
        for a in orbits:
            indicator_gram.append([point_weight*sum(P[i][j] for i in a['indices'] for j in b['indices']) for b in orbits])
        expected_gram=[[Q(a['indicator_norm_squared']) if i==j else Q(0) for j in range(len(orbits))] for i,a in enumerate(orbits)]
        check(f'LABEL:m{m}:Gram',indicator_gram==expected_gram,'orbit_indicators_in_auxiliary_history_space')
        normal_gram=[[Q(int(i==j)) for j in range(len(orbits))] for i in range(len(orbits))]
        check(f'LABEL:m{m}:support-preserved',all(P[i][j]==0 for i in range(N) for j in range(N)
              if states[i][1].bit_count()!=states[j][1].bit_count()),'label_average_does_not_mix_support_counts')
        quotient.append({'m':m,'N':n,'states':[{'order_code':c,'positive_mask':mask} for c,mask in states],
                         'point_weight':str(point_weight),'orbits':orbits,'P_in_normalized_point_basis':rational_matrix(P),
                         'Gram_projected_delta_functions':rational_matrix([[point_weight*x for x in row] for row in P]),
                         'Gram_orbit_indicators':rational_matrix(indicator_gram),
                         'Gram_normalized_orbits':rational_matrix(normal_gram)})
        total_states+=N;total_orbits+=len(orbits)
    label={'dataset_id':'CST-DUST-RKB1-LABEL','role':'auxiliary_history_space_not_physical_boundary_space',
           'discrete_function_subspace':'constant on each continuous clock/density stratum',
           'free_internal_elements':[0,1,2],'labeled_support_states':total_states,'orbits':total_orbits,
           'cases':quotient,'constraint_scope':'internal relabeling only','common_map_to_GEOM':'NOT_CONSTRUCTED',
           'superselection':'NOT_ESTABLISHED'}

    # Reproduce the SAME old two-site clock kernel, not the geometry matrix.
    a=q.g_interval(Q(3,2),80);b=q.g_interval(Q(3,4),80);c=q.g_interval(Q(11,4),80)
    raw=[[a,b],[c,a]]
    tr=q.cadd(a,a);det=q.csub(q.cmul(a,a),q.cmul(b,c))
    norm2=det[0].square()+det[1].square()
    numerator=q.cmul(q.cmul(tr,tr),q.conj(det))
    ratio=(numerator[0]/norm2,numerator[1]/norm2)
    cert=json.loads((ROOT/'inputs/common_metric_certificate.json').read_text())
    check('CLOCK:interval-certificate',q.cjson(ratio)==cert['trace_determinant_ratio'] and norm2.json()==cert['determinant_norm_squared'],
          'same_kernel_same_identification_same_Taylor_bound')
    check('CLOCK:no-common-positive-metric',norm2.lo>0 and ratio[1].hi<0,'necessary_spectral_condition_violated')
    gram=q.matmul(q.adjoint(raw),raw)
    check('CLOCK:original-I2-failure',gram[0][1][0].lo>Q(1,2),'raw_clock_kernel_only')
    # Qualify the test with the two reference matrices from the old source.
    positive=[[(Q(1),Q(0)),(Q(-1),Q(1))],[(Q(0),Q(0)),(Q(0),Q(1))]]
    metric=q.real_matrix([[1,-1],[-1,2]])
    check('CLOCK:positive-control',q.matmul(q.matmul(q.adjoint(positive),metric),positive)==metric,'synthetic_nontrivial_metric_control')
    check('CLOCK:negative-control',Q(3)**2/Q(2)>4,'synthetic_diag_1_2_spectral_obstruction')
    clock={'dataset_id':'CST-DUST-RKB1-CLOCK','parent_candidate':'CST-DUST-V1-RAW-K',
           'kernel_convention':'coefficient_map_on_declared_finite_orthonormal_clock_labels',
           'input_labels':[0,1],'output_labels':[2,3],'identification':'translation by +2',
           'hbar':'1','B_prefactor':'1','density_measure':'1/2 delta_0 + 1/2 dw on (0,1)',
           'initial_density':'0','final_density':'integrated','common_gravity_phase':'omitted; invariant irrelevant',
           'K':[[q.cjson(z) for z in row] for row in raw], 'determinant_norm_squared':norm2.json(),
           'trace_determinant_ratio':q.cjson(ratio),'I2_offdiagonal_real_lower':str(gram[0][1][0].lo),
           'Taylor_degree':80,'decision':'FAIL_EVERY_COMMON_POSITIVE_METRIC',
           'scope_exclusions':cert['scope_exclusions']}

    # Reproduce a fixed-density stationary Schur response; no scalar Fock mode.
    chain=g.encode([(i,j) for i in range(5) for j in range(i+1,5)],5)
    w=[Q(0),Q(0),Q(1),Q(1),Q(0)];L=v.laplacian(chain,5,w);X=[2,3];E=1
    eff=[[L[i][j]-L[i][E]*L[E][j]/L[E][E] for j in X] for i in X]
    target=[[Q(-55,16),Q(-17,16)],[Q(-17,16),Q(145,16)]]
    check('SCHUR:matrix',L[E][E]==-4 and eff==target,'fixed_geometry_density_stationary_response')
    samples=[]
    for t2,t3 in product(map(Q,[-1,0,1]),repeat=2):
        t1=(-t2+9*t3)/8;T=[Q(0),t1,t2,t3,Q(4)]
        current,gradient=v.current_and_gradient(chain,5,T,w)
        action=v.matter_action(chain,5,T,w)
        reduced=-quadratic([t2,t3],eff)/2-sum(w)/2
        if gradient[1]!=0 or action!=reduced:raise RuntimeError('Schur substitution mismatch')
        samples.append({'T2':str(t2),'T3':str(t3),'T1':str(t1),'action':str(action)})
    check('SCHUR:nine-substitutions',len(samples)==9,'new_exact_replay_samples_not_physical_solutions')
    check('SCHUR:full-zero-density',v.laplacian(chain,5,[Q(0)]*5)==[[Q(0)]*5 for _ in range(5)],
          'all_weights_zero_not_merely_one_boundary_atom')
    check('SCHUR:local-atom-still-couples',w[E]==0 and L[E][E]!=0,'zero_local_density_does_not_remove_positive_neighbor_coupling')
    schur={'dataset_id':'CST-DUST-RKB1-SCHUR','geometry':'five_element_chain','w':[str(x) for x in w],
           'held_indices':X,'eliminated_indices':[1],'fixed_clock_values':{'0':'0','4':'4'},
           'L':rational_matrix(L),'L_EE':'-4','L_eff':rational_matrix(eff),'substitution_samples':samples,
           'classification':'STATIONARY_RESPONSE_ONLY','quantum_compact_integral':'NOT_EVALUATED',
           'scalar_matter_modes':'NOT_DERIVED','all_zero_density_L':'zero; ordinary Schur inverse unavailable'}
    results={'gluing.json':geometry,'label_quotient.json':label,'raw_clock_kernel.json':clock,'schur.json':schur}
    results['verification.json']={'dataset_id':'CST-DUST-RKB1','control_count':len(controls),'controls':controls,
         'evidence':'exact rational and certified rational interval calculations',
         'eight_state_matter_matrix':'NOT_CONSTRUCTED','K_0plus':'NOT_COMPUTED','K_Schur_0':'NOT_COMPUTED','K_Schur_plus':'NOT_COMPUTED',
         'physical_gates':{x:'HOLD' for x in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']},
         'parent_raw_kernel_decision':'FAIL_EVERY_COMMON_POSITIVE_METRIC','external_replication':'NOT_EXECUTED','paid_compute':False}
    return results

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();results=run();args.output.mkdir(parents=True,exist_ok=True)
    for name,data in results.items():(args.output/name).write_text(canonical(data),encoding='utf-8')
    print(f"PASS: {results['verification.json']['control_count']} scoped controls, 5 result files; physical gates HOLD")

if __name__=='__main__':main()
