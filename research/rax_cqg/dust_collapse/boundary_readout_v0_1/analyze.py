"""Boundary readout controls. All calculations use exact rational arithmetic."""
from fractions import Fraction as F
from itertools import combinations,product
from math import factorial
from pathlib import Path
import hashlib
import json
import readout as r

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text());P=PLAN['controls'];OUT=ROOT/'results'
C,ZERO,ONE=r.C,r.ZERO,r.ONE


def require(ok,message):r.require(ok,message)
def encode(x):
    if isinstance(x,C):return {'re':str(x.re),'im':str(x.im)}
    if isinstance(x,F):return str(x)
    raise TypeError(type(x).__name__)
def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,default=encode)+'\n')


def sources():
    digest=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(digest==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    p=json.loads((ROOT/'inputs/provenance.json').read_text())
    require(p['commit']==PLAN['source_commit'],'Source commit')
    for name,x in p['files'].items():
        b=(ROOT/'inputs'/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['sha'],name)
    return digest,len(p['files'])


def continuous():
    N=P['continuous_count_cap'];h=F(P['continuous_clock_h']);histograms=[]
    for n in range(N+1):
        hist={}
        for order in r.v.brute_orders(n):
            G=r.v.m.gravity(r.v.m.with_anchor(order))-1
            hist[G]=hist.get(G,0)+1
        histograms.append(hist)
    cases=[];bounds=[]
    for alpha in P['alpha_values']:
        mass=[F(sum(hist.values()),factorial(n))*h**n*r.v.number_weight_squared(0,n,alpha)
              for n,hist in enumerate(histograms)]
        Z=sum(mass,F(0));tail=r.v.exponential_tail_bound(h,N)
        require(Z==r.v.partition((),h,N,alpha),'Continuous normalization')
        require(Z+tail<2,'Uniform dark-denominator guard for all phases')
        for k in P['gravity_quarter_turns']:
            numer=[sum((r.i_power(k*G)*count for G,count in hist.items()),ZERO)*
                   (h**n*r.v.number_weight_squared(0,n,alpha)/factorial(n))
                   for n,hist in enumerate(histograms)]
            amplitude=sum(numer,ZERO)/Z;single=amplitude.abs2()
            channels=[numer[n].abs2()/mass[n]/Z for n in range(N+1)]
            block=sum(channels,F(0))
            require(0<=single<=block<=1,'Nested bounded terminal projections')
            require(all(0<=channels[n]<=mass[n]/Z for n in range(N+1)),
                    'Success and complement in each number channel')
            if k==0:require(single==block==1,'Phase-free coherent reference')
            cases.append({'alpha':alpha,'gravity_quarter_turn':k,'Z':Z,
                'count_masses':[x/Z for x in mass],'coherent_amplitude':amplitude,
                'all_number_success':single,'number_resolved_success':block,
                'number_success_masses':channels,'conditional_accepted_counts':[x/block for x in channels]})
            t=tail/(Z+tail)
            bounds.append({'alpha':alpha,'gravity_quarter_turn':k,'Z_remainder_upper':tail,
                'coherent_amplitude_error_upper':2*t,
                'all_number_success_interval':[max(F(0),single-4*t),min(F(1),single+4*t)],
                'number_resolved_success_interval':[(1-t)*block,(1-t)*block+t],
                'all_coupling_single_success_lower':(2/(Z+tail)-1)**2,
                'all_coupling_block_success_lower':1/(Z+tail)})
    # Exact continuous two-geometry fringe, with matter phase zero.
    N2=2;alpha=1;Z2=r.v.partition((),h,N2,alpha)
    pn=[c*h**n/Z2 for n,c in enumerate(r.v.coefficients((),N2,alpha))]
    fringe=[]
    for turn,g_over_pi in [(0,'0'),(1,'1/18'),(2,'1/9')]:
        a=(ONE+r.i_power(turn))/2;factor=a.abs2()
        success=[pn[0],pn[1],pn[2]*factor];total=sum(success,F(0))
        fringe.append({'g_over_pi':g_over_pi,'two_geometry_visibility_factor':factor,
            'complete_success':total,'accepted_count_probabilities':[x/total for x in success],
            'complement_probability':1-total})
    require([x['complete_success'] for x in fringe]==[F(1),F(25,26),F(12,13)],
            'Analytic continuous gravity fringe')
    dump('continuous_gravity.json',{'measure':'Continuous ordered clock and inherited normalized density measure; matter coupling is zero in this diagnostic',
        'count_cap':N,'clock_h':h,'gravity_histograms':histograms,'cases':cases,
        'two_geometry_fringe':{'cap':2,'alpha':1,'pre_readout_count_probabilities':pn,'cases':fringe}})
    dump('tail_bounds.json',{'scope':'Fixed-horizon continuum gravity diagnostic; bounds on additional element numbers, not finite-grid quadrature',
        'cases':bounds,'flat_terminal_row':'Unbounded on the infinite local history Hilbert sum; count damping of a tested input does not make the flat row a bounded effect',
        'coherent_boundary_reference':'Normalized phase-free evolved vacuum, fixed while action couplings vary',
        'count_channel_boundary':'Orthogonal projection onto one phase-free normalized vector per number; strong sum is bounded by identity'})


def grid_records():
    grid=tuple(map(F,P['grid_clock_values']));marks=tuple(map(F,P['grid_density_values']))
    records=[]
    for n in range(P['grid_count_cap']+1):
        for order in r.v.brute_orders(n):
            for t in combinations(grid,n):
                for w in product(marks,repeat=n):
                    state=order,t,w
                    require(r.v.action(state)==r.v.action_by_increments(state),'Full action and increments')
                    records.append(state)
    return records


def atomic_audit():
    records=grid_records();N=P['grid_count_cap'];cuts=list(map(F,P['grid_cuts']))
    eventcut=F(P['past_event_cut']);audits=[];functions=[];pullback_checks=0;cut_event_checks=0
    for alpha in P['alpha_values']:
        weights=[r.v.number_weight_squared(0,len(x[0]),alpha)*
                 (F(P['grid_clock_atom_weight'])*F(P['grid_density_atom_weight']))**len(x[0])
                 for x in records]
        Z=sum(weights,F(0));prob=[x/Z for x in weights]
        pn=[sum((q for state,q in zip(records,prob) if len(state[0])==n),F(0)) for n in range(N+1)]
        require(all(pn) and sum(pn)==1,'Finite atomic reference')
        for kg,kd in P['phase_indices']:
            phase_cache={}
            def phase(state):
                if state not in phase_cache:phase_cache[state]=r.phase(state,kg,kd)
                return phase_cache[state]
            layers=[]
            for cut in cuts:
                layer={}
                for state,q in zip(records,prob):
                    x=r.v.cut(state,cut)
                    if x not in layer:layer[x]={'p':F(0),'W':[ZERO]*(N+1)}
                    layer[x]['p']+=q;layer[x]['W'][len(state[0])]+=phase(state)*q
                require(sum(x['p'] for x in layer.values())==1,'Prefix marginal')
                layers.append(layer)
            layer_data=[]
            for cut,layer in zip(cuts,layers):
                norm=sum((sum(x['W'],ZERO).abs2()/x['p'] for x in layer.values()),F(0))
                require(0<=norm<=1,'Unrenormalized coherent pullback contraction')
                H=[[sum((x['W'][n]*x['W'][m].conj()/x['p'] for x in layer.values()),ZERO)
                    for m in range(N+1)] for n in range(N+1)]
                residual=[[C(pn[n] if n==m else F(0))-H[n][m] for m in range(N+1)] for n in range(N+1)]
                pivots=r.psd_pivots(residual)
                layer_data.append({'cut':cut,'prefix_records':len(layer),
                    'coherent_pullback_norm_squared':norm,'channel_contraction_pivots':pivots})
            for j in range(len(cuts)-1):
                old,new=layers[j],layers[j+1]
                aggregate={x:[ZERO]*(N+1) for x in old}
                for z,rec in new.items():
                    x=r.v.cut(z,cuts[j]);ratio=rec['p']/old[x]['p']
                    transition=phase(z)*phase(x).conj()
                    for n in range(N+1):
                        beta=phase(z)*rec['W'][n].conj()/rec['p']
                        aggregate[x][n]+=ratio*transition.conj()*beta
                for x,rec in old.items():
                    for n in range(N+1):
                        require(aggregate[x][n]==phase(x)*rec['W'][n].conj()/rec['p'],
                                'Boundary-vector pullback composition')
                        pullback_checks+=1
            event_amp=[[ZERO]*(N+1) for _ in range(3)];event_p=[F(0)]*3
            for state,q in zip(records,prob):
                e=len(r.v.cut(state,eventcut)[0]);event_p[e]+=q
                event_amp[e][len(state[0])]+=phase(state)*q
            function_data=[]
            for kind in ['all_numbers','number_channels']:
                D=r.gram(event_amp,pn,kind)
                comp=[[C(event_p[i] if i==j else F(0))-D[i][j] for j in range(3)] for i in range(3)]
                plus=r.functional_audit(D);minus=r.functional_audit(comp)
                require(plus['total_mass']+minus['total_mass']==1,'Complete two-outcome readout')
                for cut,layer in zip(cuts,layers):
                    if cut<eventcut:continue
                    a=[[ZERO]*(N+1) for _ in range(3)]
                    for state,x in layer.items():
                        e=len(r.v.cut(state,eventcut)[0])
                        for n in range(N+1):
                            beta=phase(state)*x['W'][n].conj()/x['p']
                            a[e][n]+=x['p']*beta.conj()*phase(state)
                    require(r.gram(a,pn,kind)==D,'Fixed past-cylinder decoherence functional at each cut')
                    cut_event_checks+=1
                function_data.append({'readout':kind,'success_atoms':D,'complement_atoms':comp,
                                      'success_audit':plus,'complement_audit':minus})
            total_w=[sum((x['W'][n] for x in layers[-1].values()),ZERO) for n in range(N+1)]
            count_success=[total_w[n].abs2()/pn[n] for n in range(N+1)]
            count_D=[[C(count_success[n] if n==m else F(0)) for m in range(N+1)] for n in range(N+1)]
            r.psd_pivots(count_D)
            block=sum(count_success,F(0));allp=sum(total_w,ZERO).abs2()
            require(0<=allp<=block<=1,'Nested terminal effects')
            require(layer_data[0]['coherent_pullback_norm_squared']==allp and
                    layer_data[-1]['coherent_pullback_norm_squared']==1,'Pulled effect endpoints')
            if kg==kd==0:require(allp==block==1,'Phase-free boundary match')
            audits.append({'alpha':alpha,'phase_indices':[kg,kd],'Z':Z,'all_number_success':allp,
                'number_channel_success':block,'count_success_masses':count_success,
                'accepted_count_probabilities':[x/block for x in count_success] if block else None,
                'layer_checks':layer_data,'terminal_count_medium_decoherence':True,
                'action_cotransformed_boundary_success':F(1)})
            functions.append({'alpha':alpha,'phase_indices':[kg,kd],
                              'past_event_probabilities_before_readout':event_p,'readouts':function_data})
    dump('boundary_audit.json',{'measure':'Standalone four-clock, two-density atomic control; not a quadrature certification',
        'terminal_records':len(records),'cases':audits,'pullback_component_checks':pullback_checks,
        'fixed_past_functional_cut_checks':cut_event_checks})
    dump('event_functionals.json',{'event_partition':'Number 0,1,2 at T=-1/4; the same cylinder event is compared at later cuts',
        'cases':functions,'warning':'Normalized interference-functional diagonals are not generally probabilities of exclusive measured histories'})


def negatives():
    plus=[[C(F(x,10)) for x in row] for row in [[4,-2],[-2,1]]]
    minus=[[C(F(x,10)) for x in row] for row in [[4,2],[2,1]]]
    p=r.functional_audit(plus);m=r.functional_audit(minus)
    require(p['total_mass']==F(1,10) and m['total_mass']==F(9,10),'Unequal two-geometry interference')
    require(p['normalized_atoms'][0][0]==C(F(4)) and not p['medium_decoherent'],
            'Quantum-measure diagonal is not a classical probability')
    dark=[[C(F(x,4)) for x in row] for row in [[1,-1],[-1,1]]]
    dark_audit=r.functional_audit(dark)
    require(dark_audit['total_mass']==0 and dark_audit['normalized_atoms'] is None,'Zero-success normalization is forbidden')
    flat=[sum((F(len(r.v.brute_orders(n)),factorial(n))*F(1,2)**n for n in range(N+1)),F(0))
          for N in range(7)]
    overscaled=[[ONE,ONE],[ONE,ONE]]
    bad_complement=[[C(int(i==j))-overscaled[i][j] for j in range(2)] for i in range(2)]
    overscaled_probability=sum((sum(row,ZERO) for row in overscaled),ZERO)/2
    require(overscaled_probability==C(2),'Actual overscaled-effect expectation')
    rejected=False
    try:r.psd_pivots(bad_complement)
    except RuntimeError:rejected=True
    require(rejected,'Overscaled effect rejected by complement positivity')
    dump('negative_controls.json',{'unequal_preparation':{'initial_geometry_amplitudes':'(2,1)/sqrt(5)',
        'relative_gravity_phase':'pi (G_chain-G_antichain=9, g=pi/9)',
        'terminal_vector':'(1,1)/sqrt(2)','success':p,'complement':m,
        'unobserved_readout_record_probabilities':['4/5','1/5']},
        'balanced_dark_control':dark_audit,
        'overscaled_effect':{'effect':'2 |b><b|','witness':'psi=b',
            'putative_probability':overscaled_probability.re,
            'complement_positivity_rejected':rejected,'status':'REJECTED'},
        'flat_terminal_row_norm_squared_through_cap_6':flat,
        'flat_row_unbounded':'Analytic: the two-layer lower bound makes the base history volume divergent',
        'renormalized_initial_pullback':'If 0<p_success<1, normalizing the pulled vector changes predicted success to 1',
        'rank_obstruction':'rank(D)<=rank(E); exact medium decoherence with k nonzero atoms requires rank(E)>=k',
        'rank_one_multiple_positive_decoherent_atoms':'FAIL_ANALYTIC',
        'finite_horizon_scope_only':True})


def main():
    OUT.mkdir(exist_ok=True);digest,n=sources()
    continuous();atomic_audit();negatives()
    dump('verification.json',{'source_commit':PLAN['source_commit'],'plan_sha256':digest,
        'sources_verified':n,'status':'PASS_WITH_CONDITIONAL_COHERENT_INSTRUMENTS_AND_SCOPED_NO_GOS',
        'bounded_readout_and_pullback':'PASS_REFERENCE','continuous_gravity_interference':'PASS_REFERENCE_WITH_CERTIFIED_NUMBER_TAIL',
        'continuous_matter_phase_integral':'NOT_EVALUATED','nonzero_matter_phase_atomic_controls':'PASS_STANDALONE_MEASURE',
        'number_channel_decoherence':'PASS_FOR_TERMINAL_NUMBER_PARTITION',
        'all_past_event_algebras_decohere':'NOT_CLAIMED',
        'physical_gates':{k:'HOLD' for k in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']},
        'physical_boundary_or_quantum_law_selected':False,'formal_proof_checker':False,'physical_4D_ensemble':False})
    print(json.dumps({'status':'PASS','result_files':6,'physical_gates':'8 HOLD'}))


if __name__=='__main__':main()
