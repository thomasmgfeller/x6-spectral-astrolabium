"""Deterministic method-gate reassessment; no random draws or new model fit."""
import argparse
from fractions import Fraction as F
from flint import arb,acb,ctx
from common import read,write,require,enc,close

def compute(bits):
    ctx.prec=bits;p=read('PROTOCOL.json');target=arb(p['unchanged_global_accuracy_target'])
    prior=read(f'evidence/v23_GLOBAL_{bits}.json');audit=read(f'evidence/v23_ENDPOINTS_{bits}.json.gz')
    local=read(f'evidence/v20_LOCAL_{bits}.json');v14=read(f'evidence/v14_DECISION_{bits}.json')
    v14p=read('evidence/v14_PROTOCOL.json');norm=read('evidence/v19_BOUNDS_512.json')
    beta=1/(16*(1+(2*arb.pi()).sqrt()));kappa=arb('4976184375/4294967296');gamma=beta*kappa
    counts={a['key']:a['active_count'] for a in prior['windows'][0]['archives']}
    known={(a['archive'],a['active_index']):a for a in audit if a['kind']=='known'}
    require(len(known)==223 and len(audit)==479,'complete endpoint inputs')
    def split(row):
        r=row['tail_bounds'][0];require(r['tau_cutoff']=='5','entire tail')
        n=arb(r['near_upper']);f=arb(r['far_upper']);close(n+f,r['direct_tail_upper']);return n,f
    windows=[]
    for wi,w in enumerate(prior['windows']):
        require(w['window']==wi,'window order');d=[a for a in audit if a['kind']=='detector' and a['window']==wi]
        require(len(d)==128 and sum((F(a['mass']) for a in d),F(0))==1,'complete detector')
        dn=sum((arb(a['mass'])*split(a)[0] for a in d),arb(0));df=sum((arb(a['mass'])*split(a)[1] for a in d),arb(0))
        un,uf=split(w['uniform_active_endpoint']);rows=[]
        for ai,a in enumerate(w['archives']):
            old=local['archives'][ai];require(a['key']==old['key'] and a['coordinates_sha256']==old['coordinates_sha256'],'same conditioning archive')
            adj=[acb(*map(arb,z)).abs_upper() for z in old['adjoints'][wi]];require(len(adj)==counts[a['key']],'all known paths')
            kn=sum((z*split(known[a['key'],j])[0] for j,z in enumerate(adj)),arb(0))
            kf=sum((z*split(known[a['key'],j])[1] for j,z in enumerate(adj)),arb(0))
            factor=(1+gamma)**len(adj)*((gamma*arb('29/512')).exp()-1)
            xn=un*factor;xf=uf*factor;near=dn+kn+xn;far=df+kf+xf;finite=arb(a['finite_v022_upper']);total=arb(a['complete_global_upper'])
            close(dn+df,a['direct_tail_upper']);close(kn+kf,a['known_active_tail_upper']);close(xn+xf,a['unknown_active_tail_upper']);close(near+far+finite,total)
            require(finite>target and far>target and total>target,'remaining certificate terms exceed inherited target')
            rows.append({'archive':a['key'],'window':wi,'finite_certificate':enc(finite),'near_certificate':enc(near),'far_certificate':enc(far),'complete_v023_certificate':enc(total),
              'near_certificate_fraction':enc(near/(near+far+finite)),
              'fixed_certificate_if_near_term_removed':enc(finite+far),
              'fixed_certificate_if_entire_infinite_term_removed':enc(finite),
              'finite_certificate_to_target_ratio':enc(finite/target),
              'complete_certificate_to_target_ratio':enc(total/target),
              'Markov_failure_probability_upper_at_target':'1',
              'conditional_accuracy_decision':'NOT_CERTIFIED',
              'actual_error_lower_bound_from_this_budget':'0',
              'path_parts':{'direct_near':enc(dn),'direct_far':enc(df),'known_near':enc(kn),'known_far':enc(kf),'unknown_near':enc(xn),'unknown_far':enc(xf)}})
        # Any archive has N active points in a fixed finite causal hull.
        # The common tmax=5/4 enclosure is used for both windows.
        lam=arb('14625/256');lamE=arb('29/512');lamB=lam-lamE;M=arb(norm['source_M0'])
        finite_uniform=gamma*M*arb('110567/128')
        transport=(gamma*lam).exp();tail_uniform=arb(w['uniform_active_endpoint']['tail_bounds'][0]['direct_tail_upper'])
        ensemble_delta=(finite_uniform+tail_uniform)*transport
        finite_response=gamma*M*1250*(gamma*lamB).exp()
        windows.append({'window':wi,'archives':rows,'uniform_finite_first_forcing':enc(finite_uniform),'uniform_infinite_first_forcing':enc(tail_uniform),
          'ensemble_transport_upper':enc(transport),'unconditional_exterior_L1_upper':enc(ensemble_delta),
          'unconditional_A5_L1_upper':enc(finite_response),'unconditional_full_KG_diagnostic_L1_upper':enc(ensemble_delta+finite_response),
          'ensemble_L1_status':'FINITE_UNDER_IDEAL_POISSON_LAW','ensemble_L2_status':'NOT_ESTABLISHED_BY_L1_BOUND','covariance_prediction':'NOT_EVALUATED'})
    candidates={}
    for name,old in v14['candidates'].items():
        evidence=dict(old['method_evidence']);missing=[k for k in v14p['required_method_certificates'] if evidence.get(k)!='PASS']
        require(missing==old['missing_certificates'],'preserve inherited admission rationale')
        candidates[name]={'definition':'UNCHANGED_V014','method_evidence':evidence,'missing_certificates':missing,'decision':'REJECTED_FOR_CONFIRMATORY_RUN'}
    certificate=read(f'evidence/v15_DOMAIN_CERTIFICATE_{bits}.json');diag=read(f'evidence/v15_DIAGNOSIS_{bits}.json')
    witness=arb(certificate['all_H_ge_4_relative_bias_lower'][0]);require(witness>arb('1/10'),'unchanged necessary witness rejects domain-only repair')
    controls=[{'epsilon':c['epsilon'],'relative_infinite_bias':c['relative_infinite_bias'],'necessary_10pct_bias_test':c['necessary_10pct_bias_test']} for c in diag['controls']]
    decision={'schema':p['schema'],'precision_bits':bits,'base_commit':p['base_commit'],'completed_step':3,
      'global_coverage':'COMPLETE_FINITE_PLUS_INFINITE','budget_windows':windows,'legacy_candidates':candidates,
      'full_KG_history_diagnostic':{'identity':'PRESCRIBED_EXACT_KG_HISTORY_NOT_LOCAL_H1_OR_PU_H1','absolute_convergence':'ALMOST_SURE_UNDER_IDEAL_POISSON_LAW','unconditional_L1':'PROVED_WITH_UNIFORM_ACTIVE_HULL_BOUND','joint_original_mean_and_covariance':'NOT_EVALUATED','fourth_moment_or_inference_adequate_tail':'NOT_CERTIFIED','ensemble_numerical_error':'NOT_CERTIFIED','sampling_law_alignment':'NOT_CERTIFIED','confirmatory_candidate_admission':'NOT_A_SUBSTITUTE_FOR_FROZEN_V014_CANDIDATES'},
      'operator_witness':{'all_real_H_ge_4_relative_bias_lower':enc(witness),'necessary_relative_RMS_target':'1/10','infinite_controls':controls,'fixed_cell_domain_only_repair':'REJECTED_BY_INHERITED_NECESSARY_WITNESS','whole_operator_family':'NOT_REJECTED','new_candidate':'NOT_SELECTED'},
      'decision':'NO_ACCURACY_RELEASE_NO_FRESH_ENSEMBLE','METHOD':'HOLD','G1':'HOLD','new_confirmatory_design':v14['new_design'],'fresh_confirmation':'NOT_RUN','new_clouds':0,'new_random_calls':0,
      'priority':'DETERMINISTIC_SCALAR_CANDIDATE_AND_STABILITY_SCREEN_BEFORE_FURTHER_CONFIRMATION','tail_work_role':'OPTIONAL_ORIGINAL_MODEL_ATTRIBUTION_NOT_PRIMARY_RESCUE_OF_REJECTED_FIXED_CELL',
      'independent_scientific_review':'NOT_PERFORMED'}
    require(all(x is None for x in decision['new_confirmatory_design'].values()),'no premature design')
    write(f'results/DECISION_{bits}.json',decision)
    print(bits,[(r['archive'],r['window'],float(arb(r['far_certificate'])),float(arb(r['near_certificate_fraction']))) for w in windows for r in w['archives']],flush=True)
    print('ensemble',bits,[float(arb(w['unconditional_exterior_L1_upper'])) for w in windows],flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bits',type=int,choices=[128,192],required=True);compute(p.parse_args().bits)
