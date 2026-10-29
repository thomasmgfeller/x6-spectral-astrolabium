"""Independent finite-graph algebra, exact dyadic counts and precision audit."""
import json, sys
from fractions import Fraction as Q
import numpy as np
from flint import arb,acb,ctx
from exterior import HERE,ROOT,loadgz,unpack,pack,require,dump,inventory,can_reach_detector,plan,check_freeze

def rational_control():
    # Order: exterior history, inner history, exterior active, inner active 1/2.
    K=[[Q(0) for _ in range(5)] for _ in range(5)]
    K[2][0]=Q(2,5);K[3][0]=Q(1,3);K[3][1]=Q(-1,4);K[3][2]=Q(1,7)
    K[4][0]=Q(-2,9);K[4][1]=Q(1,5);K[4][2]=Q(1,6);K[4][3]=Q(3,8)
    q=[Q(1,11),Q(-1,13),Q(2,7),Q(1,5),Q(3,10)]
    h=[Q(7,3),Q(-2,5)]
    def evolve(exterior=True,clamp=False):
        v=h.copy()+[Q(0)]*3
        if not exterior:v[0]=0
        for i in range(2,5):
            if i==2 and (clamp or not exterior):continue
            v[i]=sum(K[i][j]*v[j] for j in range(i))
        return v
    v=evolve();old=evolve(False);clamped=evolve(clamp=True)
    delta=sum(q[i]*(v[i]-old[i]) for i in range(5))
    # Independent explicit path expansion, not a reverse recurrence.
    L={j:q[j]+q[3]*K[3][j]+q[4]*(K[4][j]+K[4][3]*K[3][j]) for j in [0,2]}
    rhs=sum(L[j]*v[j] for j in [0,2]);direct=sum(q[j]*v[j] for j in [0,2])
    hist=L[0]*h[0];extra=L[2]*v[2]
    require(delta==rhs==hist+extra,'rational path expansion')
    require(hist==sum(q[i]*(clamped[i]-old[i]) for i in range(5)),'rational clamped exterior control')
    require(delta!=direct,'negative control rejects dropping inner transport')
    require(delta!=-rhs,'negative control rejects reversed sign')
    require(delta!=hist,'negative control rejects substituting zero KG active exterior in full discrete evolution')
    # An arbitrary exterior boundary variable remains arbitrary without a bound.
    # This is algebraic underdetermination, not a counterexample for fixed KG data.
    require(L[0]!=0,'nonzero unconstrained boundary sensitivity')
    return {'delta':str(delta),'direct_only':str(direct),'prescribed_history':str(hist),
            'extra_exterior_dynamics':str(extra),'unbounded_boundary_coefficient':str(L[0]),'controls':6}

def before(a,b):
    d=[y-x for x,y in zip(a,b)]
    return d[0]>0 and d[0]*d[0]>sum(z*z for z in d[1:])

def exact_counts():
    a=np.load(ROOT/'scalar_pilot_v0_1/results/clouds.npz');ncheck=0;summary=[]
    for key in plan()['pairs']:
        x,z,c,inn,ext,ia,ea,nh,_=inventory(key)
        r=[[Q(float(v)) for v in p] for p in z]
        candidates=[(i,j) for i in range(len(z)) for j in ext if j<i and c[i,j]>=0]
        chosen=[candidates[(k*(len(candidates)-1))//15] for k in range(16)]
        for i,j in chosen:
            exact=sum(before(r[j],p) and before(p,r[i]) for p in r)
            require(exact==int(c[i,j]),'Fraction interval count independent of C++ predicate')
            ncheck+=1
        summary.append({'key':key,'exact_intervals':len(chosen),'retained':len(z)})
    return ncheck,summary

def main():
    check_freeze();ctx.prec=192
    a=loadgz(HERE/'results/ATTRIBUTION_128.json.gz');b=loadgz(HERE/'results/ATTRIBUTION_192.json.gz')
    require(a['complete'] and b['complete'],'all four pairs complete at both precisions')
    count=0;comparison=[];endpoint=[]
    for x,y in zip(a['rows'],b['rows']):
        require(x['key']==y['key'],'matching row')
        for aa,bb in zip(x['history'],y['history']):
            require(unpack(aa).overlaps(unpack(bb)),'history precision overlap');count+=1
        for u,v in zip(x['windows'],y['windows']):
            for aa,bb in zip(u['levels'],v['levels']):
                for k in aa['quantities']:
                    require(unpack(aa['quantities'][k]['value']).overlaps(unpack(bb['quantities'][k]['value'])),'response precision overlap '+k);count+=1
            for aa,bb in zip(u['external_state_transfer'],v['external_state_transfer']):
                require(aa['index']==bb['index'] and unpack(aa['coefficient']).overlaps(unpack(bb['coefficient'])),'transfer precision overlap');count+=1
            q=v['levels'][-1]['quantities']
            get=lambda k,f:float(unpack(q[k][f]).real.mid())
            needed=(unpack(q['extended_error']['abs_lower']).real-arb(plan()['existing_comparison_tolerance'])).nonnegative_part()
            comparison.append({'key':x['key'],'window':v['window'],'shell_abs_lower':get('shell_change','abs_lower'),
                'shell_abs_upper':get('shell_change','abs_upper'),'shell_component_radius_upper':get('shell_change','component_radius_upper'),
                'old_error_lower':get('old_error','abs_lower'),'extended_error_lower':get('extended_error','abs_lower'),
                'KG_prescribed_error_lower':get('KG_prescribed_error','abs_lower'),
                'inner_transport_abs_upper':get('inner_transport','abs_upper'),'extra_exterior_dynamics_abs_upper':get('extra_exterior_dynamics','abs_upper'),
                'old_response':q['old_response']['value'],'extended_response':q['extended_response']['value'],
                'shell_change':q['shell_change']['value'],
                'necessary_beyond5_correction_lower':pack(needed),
                'history_uncertainty_effect_upper':float(unpack(v['history_uncertainty_effect_upper']).real.mid()),
                'extended_accuracy_excluded':v['extended_accuracy_excluded'],'KG_prescribed_accuracy_excluded':v['KG_prescribed_accuracy_excluded'],
                'shell_component_radius_pass':v['shell_component_radius_pass']})
    rational=rational_control();nexact,details=exact_counts()
    source=json.loads((HERE/'PUBLIC_SOURCE_TREE.json').read_text());import hashlib
    for f in source['files']:
        data=(HERE.parent/f['path']).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==f['git_blob_sha1'],'public Git blob identity')
    result={'validation_status':'PASS','precision_overlap_comparisons':count,'independent_exact_interval_counts':nexact,
        'rational_controls':rational,'geometry':details,'comparisons':comparison,'public_source_blob_checks':len(source['files']),
        'coefficient_integration':'one shared certified 192-bit stage, not two independent geometry runs',
        'scientific_status':{'METHOD':'HOLD','G1':'HOLD','infinite_domain_remainder':'NOT_CERTIFIED','fresh_confirmation':'NOT_RUN'},
        'interpretation':'finite extension attribution only; any excluded accuracy applies to that finite prescription, not all domains'}
    dump(HERE/'results/CHECKS.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
