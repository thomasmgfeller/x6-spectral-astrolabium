"""Independent arithmetic identities, source integrity and scope controls."""
import hashlib,json
from fractions import Fraction as F
from flint import arb,acb,ctx
from common import HERE,read,write,require,enc,close

def frac(x):return arb(x.numerator)/x.denominator
def check():
    ctx.prec=192;counts={};provenance=read('PROVENANCE.json');tree={r['path']:r['sha'] for r in read('evidence/MAIN_TREE.json')['entries']}
    for row in provenance['files']:
        b=(HERE/row['package_path']).read_bytes()
        require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'input SHA256')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']==tree[row['repository_path']],'input Git identity')
    counts['source_files']=len(provenance['files'])
    require(read('evidence/v23_CHECKS.json')['status']=='PASS','v0.23 numerical checks')
    replay=read('evidence/v23_REPLAY.json')
    for name,h in replay['files'].items():require(hashlib.sha256((HERE/'evidence'/('v23_'+name)).read_bytes()).hexdigest()==h,'v0.23 replay identity')
    counts['v023_replay_files']=len(replay['files'])
    protocol=read('PROTOCOL.json');require(protocol['base_commit']==provenance['base_commit'],'correct merged basis')
    # Independent exact antiderivative for the entire active causal hull.
    lam=F(11,4)**4-F(1,2)**4;lamE=F(29,512);lamB=lam-lamE
    require(lam==F(protocol['active_hull_count_mean_cap'])==F(14625,256),'active hull mean')
    require(lamB==F(protocol['known_active_count_mean'])==F(29221,512),'inner active count mean')
    require(3*F(110567,384)==F(protocol['finite_history_root_intensity_volume']),'finite exterior intensity volume')
    require(F(3,24)*10**4==F(protocol['whole_Omega5_count_mean']),'whole Omega5 mean')
    counts['exact_geometry_identities']=4
    beta=1/(16*(1+(2*arb.pi()).sqrt()));gamma=beta*arb('4976184375/4294967296');M=arb(read('evidence/v19_BOUNDS_512.json')['source_M0'])
    # Positive Poisson sum through 1023 plus a Chernoff bound for its full tail.
    quadratures=[]
    for mean in [F(0),lamE,lamB,lam]:
        for s in [arb(1),1+gamma,arb('3/2')]:
            l=frac(mean);tilt=l*s;term=arb(1);total=term
            for k in range(1,1024):term*=tilt/k;total+=term
            total*=(-l).exp();exact=(l*(s-1)).exp()
            tail=arb(0) if mean==0 else exact*(-tilt+1024*(1+(tilt/1024).log())).exp()
            require(tilt<1024 and tail<arb('1e-200'),'Poisson tail explicitly closed')
            enclosure=arb(total.mid(),total.rad()+tail.upper())
            require(exact.overlaps(enclosure),'independent positive PGF sum')
            close(exact,total,'1e-45');quadratures.append({'lambda':str(mean),'s':enc(s),'series_plus_tail':enc(enclosure),'formula':enc(exact),'tail_upper':enc(tail)})
    counts['independent_Poisson_PGF_sums']=len(quadratures)
    comparison=[];nodes=0;decompositions=0;method_rows=0
    data=[read(f'results/DECISION_{bits}.json') for bits in [128,192]]
    for bits,d in zip([128,192],data):
        ctx.prec=192
        require(d['precision_bits']==bits and d['completed_step']==3,'decision precision')
        require(d['METHOD']==d['G1']=='HOLD' and d['fresh_confirmation']=='NOT_RUN','unchanged gates')
        require(all(x is None for x in d['new_confirmatory_design'].values()),'no new design')
        require(d['new_clouds']==d['new_random_calls']==0,'no random draws')
        old=read(f'evidence/v14_DECISION_{bits}.json')
        for name,r in d['legacy_candidates'].items():
            require(r['method_evidence']==old['candidates'][name]['method_evidence'],'no certificate transfer across candidate maps')
            require(r['missing_certificates']==old['candidates'][name]['missing_certificates'],'same missing prerequisites');method_rows+=len(r['method_evidence'])
        p23=read(f'evidence/v23_GLOBAL_{bits}.json')
        for wi,w in enumerate(d['budget_windows']):
            f0=gamma*M*arb('110567/128');factor=(gamma*frac(lam)).exp();D=arb(p23['windows'][wi]['uniform_active_endpoint']['tail_bounds'][0]['direct_tail_upper'])
            close(w['uniform_finite_first_forcing'],f0);close(w['ensemble_transport_upper'],factor)
            close(w['unconditional_exterior_L1_upper'],(f0+D)*factor)
            close(w['unconditional_A5_L1_upper'],gamma*M*1250*(gamma*frac(lamB)).exp())
            require(arb(w['unconditional_exterior_L1_upper'])>arb('1/1000'),'L1 existence is not accuracy')
            for ai,r in enumerate(w['archives']):
                f=arb(r['finite_certificate']);n=arb(r['near_certificate']);g=arb(r['far_certificate']);t=arb(r['complete_v023_certificate'])
                close(f+n+g,t);close(t,p23['windows'][wi]['archives'][ai]['complete_global_upper'])
                close(r['fixed_certificate_if_near_term_removed'],f+g);close(r['fixed_certificate_if_entire_infinite_term_removed'],f)
                close(r['near_certificate_fraction'],n/t)
                require(f>arb('1/1000') and g>arb('1/1000') and n/t>arb('0.999999'),'retained certificate obstacle')
                require(r['Markov_failure_probability_upper_at_target']=='1' and r['actual_error_lower_bound_from_this_budget']=='0','no false stochastic attribution')
                parts=r['path_parts'];close(sum((arb(parts[k]) for k in ['direct_near','known_near','unknown_near']),arb(0)),n)
                close(sum((arb(parts[k]) for k in ['direct_far','known_far','unknown_far']),arb(0)),g);decompositions+=1
        # Reassemble the inherited continuous-H certificate from its full node cover.
        cert=read(f'evidence/v15_DOMAIN_CERTIFICATE_{bits}.json');slope=arb(cert['global_H_derivative_bound'][0]).upper()
        cover=cert['covering_nodes'];require(len(cover)==129,'complete continuous-H cover');lower=[]
        for i,row in enumerate(cover):
            require(arb(row['H'][0]).contains(arb(4)+arb(i)/16),'fixed H grid')
            mu=acb(*map(arb,row['mean']));v=(mu+arb('1/2')).abs_lower()-slope/32
            close(v,row['covered_bias_lower'][0],'1e-17');lower.append(v);nodes+=1
        value=2*min(min(lower),arb(cert['all_H_ge_12_bias_lower'][0]));close(value,cert['all_H_ge_4_relative_bias_lower'][0],'1e-17')
        require(arb(cert['all_H_ge_4_relative_bias_lower'][0])>arb('0.4170'),'inherited necessary witness remains valid')
        require(d['operator_witness']['whole_operator_family']=='NOT_REJECTED','no universal operator rejection')
    for wa,wb in zip(data[0]['budget_windows'],data[1]['budget_windows']):
        for a,b in zip(wa['archives'],wb['archives']):
            for key in ['finite_certificate','near_certificate','far_certificate','complete_v023_certificate','near_certificate_fraction']:
                x=arb(a[key]);y=arb(b[key]);q=abs(x-y)/(1+abs(y));tol='1e-12' if key=='finite_certificate' else '1e-20'
                require(q.upper()<arb(tol),'cross precision stability');comparison.append(q)
    counts.update({'global_decompositions':decompositions,'legacy_method_entries':method_rows,'inherited_H_cover_nodes':nodes,'cross_precision_comparisons':len(comparison)})
    # Exact counterexamples: finite L1 alone need not give finite L2 or a unique covariance.
    identities=0
    for B in [F(1,1000),F(1),F(10)]:
        for N in [1,2,8,64]:
            mass=sum((3*F(1,4)**k for k in range(1,N+1)),F(0));l1=sum((3*F(1,4)**k*(B*2**k/3) for k in range(1,N+1)),F(0));l2=sum((3*F(1,4)**k*(B*2**k/3)**2 for k in range(1,N+1)),F(0))
            require(mass==1-F(1,4)**N and l1==B*(1-F(1,2)**N) and l2==N*B*B/3,'geometric L1-not-L2 counterexample');identities+=3
        for probability in [F(1),F(1,4),F(1,1024),F(1,2**32)]:
            amplitude=B/probability;require(probability*amplitude==B and probability*amplitude**2==B*B/probability,'same L1, unbounded variance');identities+=2
    counts['exact_counterexample_identities']=identities
    # These rejected conclusions are mathematical counterexamples, not a new test design.
    negative={'large_upper_bound_implies_large_error':'REJECTED_BY_ZERO_RANDOM_VARIABLE',
      'finite_L1_implies_finite_L2':'REJECTED_BY_GEOMETRIC_HEAVY_TAIL',
      'marginal_L1_bounds_determine_covariance':'REJECTED_BY_SIGN_FLIPPED_PAIRED_CHANNELS',
      'removing_only_infinite_certificate_qualifies_accuracy':'REJECTED_BY_RETAINED_FINITE_CERTIFICATE',
      'KG_history_certificates_repair_local_H1_or_PU_H1':'REJECTED_BY_DISTINCT_MODEL_DEFINITIONS',
      'finite_Gaussian_witness_rejects_entire_operator_family':'REJECTED_BY_RESTRICTED_WITNESS_SCOPE'}
    # Explicit paired-channel covariance signs with identical zero means and marginals.
    for sign in [-1,1]:
        pairs=[(F(1),F(sign)),(F(-1),F(-sign))];cross=sum((x*y/2 for x,y in pairs),F(0))
        require(cross==sign and sum((x/2 for x,y in pairs),F(0))==0 and sum((y/2 for x,y in pairs),F(0))==0,'paired covariance sign control')
    counts['paired_covariance_sign_controls']=2
    out={'schema':protocol['schema'],'status':'PASS','counts':counts,'negative_controls':negative,'max_relative_precision_difference':enc(max(x.upper() for x in comparison)),
      'METHOD':'HOLD','G1':'HOLD','fresh_confirmation':'NOT_RUN','new_random_calls':0,'independent_scientific_review':'NOT_PERFORMED'}
    write('results/POISSON_PGF_CHECKS.json',quadratures);write('results/CHECKS.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':check()
