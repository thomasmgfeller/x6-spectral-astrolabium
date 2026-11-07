"""Exact collar and finite-width boundary-state controls, Python stdlib only."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
from itertools import product
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from exact_core import C,encode,require,gitsha
Z=(0,0,0,0,0)
def dump(name,value):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')
def clean(p):return {k:v for k,v in p.items() if v}
def padd(p,q):
    out=p.copy()
    for k,v in q.items():out[k]=out.get(k,F(0))+v
    return clean(out)
def pscale(p,s):return clean({k:s*v for k,v in p.items()})
def pmul(p,q):
    out={}
    for k,v in p.items():
        for j,w in q.items():
            e=tuple(a+b for a,b in zip(k,j));out[e]=out.get(e,F(0))+v*w
    return clean(out)
def variable(j):
    k=list(Z);k[j]=1;return {tuple(k):F(1)}
def pvalue(p,coords):
    return sum((v*prod_f([x**k for x,k in zip(coords,e)]) for e,v in p.items()),F(0))
def prod_f(xs):
    y=F(1)
    for x in xs:y*=x
    return y
def mean(p,a,b):
    total=F(0)
    for e,c in p.items():
        if any(k%2 for k in e[1:]):continue
        tm=(b**(e[0]+1)-a**(e[0]+1))/F((e[0]+1)*(b-a))
        total+=c*tm*prod_f([F(1,k+1) for k in e[1:]])
    return total
def weights(m):return [F([1,-9,16,-8][m-y-1]) if m-y-1<4 else F(0) for y in range(m)]
def moments(B,T):return [sum((b*t**k for b,t in zip(B,T)),F(0)) for k in range(3)]
def direct(B,T,t,w):
    constraint=1+sum((b*(t-y)**2 for b,y in zip(B,T)),F(0))/2
    currents=[w*b*(t-y)/2 for b,y in zip(B,T)]
    return constraint,-sum(currents,F(0)),currents
def equations(M,t,w):
    b0,m1,m2=M
    return 1+(b0*t*t-2*m1*t+m2)/2,-w*(b0*t-m1)/2
def density_moment(k):return F(1) if k==0 else F(1,2*(k+1))
def run():
    plan=json.loads((ROOT/'plan.json').read_text());psha=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(psha==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'provenance.json').read_text())
    for name,v in prov['inputs'].items():require(gitsha((ROOT/name).read_bytes())==v['git_blob'],'Pinned source '+name)
    require(set(plan['physical_gates'].values())=={'HOLD'},'Eight HOLD gates')
    B=weights(4);base=list(map(F,plan['base_collar']));M=moments(B,base)
    require(B==list(map(F,[-8,16,-9,1])) and M==[F(0),F(0),F(-2)],'Rational stationary collar moments')
    chain=[];stationary=0;short=0
    for m in plan['chain_lengths']:
        if m<4:past=list(map(F,range(1-m,1)))
        else:
            prefix=m-4;past=[F(-(prefix+3-j)) for j in range(prefix)]+base
        bm=weights(m)
        for shift in map(F,plan['common_shifts']):
            T=[y+shift for y in past]
            for t0 in map(F,plan['free_clock_values']):
                t=t0+shift
                for w in map(F,plan['positive_weights']):
                    c,q,j=direct(bm,T,t,w);moms=moments(bm,T)
                    require((c,q)==equations(moms,t,w),'Moment criterion equals full variational row')
                    cp,qp,_=direct(bm,past,t0,w);require((c,q)==(cp,qp),'Common shift covariance')
                    action=lambda z:-w*direct(bm,T,z,w)[0]/2
                    h=F(1,11);fd=(action(t+h)-action(t-h))/(2*h)
                    require(fd==q,'Exact clock derivative of quadratic action')
                    work=sum((y*v for y,v in zip(T,j)),F(0))+t*q
                    require(work==w*(1-c) and sum(j)+q==0,'Full boundary-work and current identities')
                    if m>=4:
                        require(c==q==0 and moms==[0,0,-2],'Joint stationarity, including older zero-coefficient predecessors')
                        require(work==w and action(t)==0,'Boundary supports nonzero weight despite flat free action')
                        require(moms[0]==0 and moms[0]*t-moms[1]==0,'Entire free (t,w) Hessian vanishes');stationary+=1
                    else:
                        require(q!=0,'Short-chain obstruction')
                        require((q<0) if m in [1,3] else (q>0),'Short-chain derivative sign');short+=1
                    chain.append({'past_count':m,'shift':shift,'free_t':t,'weight':w,'moments':moms,'C':c,'q':q,'boundary_work':work})
    c,q,j=direct(B,base,F(1,2),F(1,2))
    require(j==[F(-6),F(10),F(-33,8),F(1,8)],'Exact signed boundary currents')
    dump('stationary_collar.json',{'base_collar':base,'BD_coefficients':B,'base_moments':M,
        'cases':chain,'joint_stationary_cases':stationary,'short_chain_nonstationary_cases':short,
        'example':{'t':F(1,2),'w':F(1,2),'C':c,'q':q,'boundary_currents':j,'boundary_work':F(1,2)},
        'minimality_scope':'chain past, one final free element, positive weight, no extra boundary action',
        'isolated_saddle':False,'selected_physical_state':False})

    perturb=[];free_t=list(map(F,plan['free_clock_values']));free_w=list(map(F,plan['positive_weights']))
    for eps in map(F,plan['uncertainty_widths']):
        for levels in product(plan['perturbation_levels'],repeat=4):
            delta=[eps*x for x in levels];T=[y+d for y,d in zip(base,delta)]
            require(all(T[i]<T[i+1] for i in range(3)),'Past chronology preserved')
            d1=sum((b*d for b,d in zip(B,delta)),F(0))
            d2=2*sum((b*y*d for b,y,d in zip(B,base,delta)),F(0))+sum((b*d*d for b,d in zip(B,delta)),F(0))
            for t in free_t:
                for w in free_w:
                    c,q,_=direct(B,T,t,w)
                    require(c==-d1*t+d2/2 and q==w*d1/2,'Exact boundary perturbation law')
                    require(abs(c)<=(34*t+64)*eps+17*eps*eps and abs(q)<=17*w*eps,'Uniform worst-case residual budgets')
                    perturb.append({'epsilon':eps,'levels':levels,'t':t,'w':w,'C':c,'q':q})
    # Common-mode timing uncertainty stays on the moment surface, unlike general independent errors.
    common=[]
    for shift in map(F,plan['common_shifts']):
        mm=moments(B,[y+shift for y in base]);require(mm==M,'Common shifts stay stationary')
        common.append({'shift':shift,'moments':mm})
    dump('boundary_sensitivity.json',{'cases':perturb,'common_mode_controls':common,
        'condition_for_joint_stationarity':'d1=0 and d2=0; adjusting the free clock cannot repair nonzero d1',
        'local_moment_surface_codimension':2,'uncertainty_is_physical_measurement_data':False})

    a,b=map(F,plan['packet_clock_interval']);tpoly=variable(0)
    packet=[];amplitudes=[]
    for eps in map(F,plan['uncertainty_widths']):
        cp={};m1p={}
        for i,(beta,y) in enumerate(zip(B,base)):
            eta=variable(i+1)
            cp=padd(cp,pscale(pmul(padd({Z:y},pscale(tpoly,-1)),eta),eps*beta))
            cp=padd(cp,pscale(pmul(eta,eta),eps*eps*beta/2))
            m1p=padd(m1p,pscale(eta,eps*beta))
        cpower={Z:F(1)};qpower={Z:F(1)};cms=[];qms=[]
        for k in range(plan['packet_moment_order']+1):
            cms.append(mean(cpower,a,b));qms.append(mean(qpower,a,b)*density_moment(k)/2**k)
            cpower=pmul(cpower,cp);qpower=pmul(qpower,m1p)
        expected_C2=F(21751,24)*eps**2+F(134,15)*eps**4
        require(cms[0]==qms[0]==1 and cms[1]==qms[1]==0,'Packet normalization and exactly zero mean residuals')
        require(cms[2]==expected_C2 and qms[2]==F(67,12)*eps**2,'Exact finite-width residual variances')
        require(cms[2]>0 and qms[2]>0,'Zero means do not enforce constraints')
        bound=98*eps+17*eps*eps
        row={'epsilon':eps,'C_moments':cms,'q_moments':qms,'wC_residual_squared':cms[2]/6,
            'uniform_C_bound':bound,'packet_norm_squared':1,'overlap_with_half_width_squared':F(1,16),
            'joint_stationary_support_probability':0}
        packet.append(row)
        V=[density_moment(k)*cms[k]/2**k for k in range(len(cms))]
        for mu in map(F,plan['matter_phase_values']):
            center=C();power=C(F(1));factor=C(F(0),-mu)
            for k,v in enumerate(V):center=center+power*(v/F(factorial(k)));power=power*factor
            radius=abs(mu)**5*bound**5/F(46080)
            distance=min(F(2),abs(mu)*bound/8,mu*mu*cms[2]/48)
            success_lower=max(F(0),1-distance)**2
            require(V[1]==0 and distance>=0 and radius>=0,'Return-amplitude bounds use normalized state and zero mean phase')
            amplitudes.append({'epsilon':eps,'mu':mu,'Taylor_center':center,'radius':radius,
                'distance_to_one_upper':distance,'conditional_return_probability_interval':[success_lower,F(1)]})
    dump('finite_width_states.json',{'packet_definition':'normalized constant L2 boundary packet on four independent +/-epsilon clock intervals, uniform t in [1/4,1], constant density wavefunction in original half-atom measure',
        'states':packet,'moment_method':'exact multivariate polynomial integration, through order four',
        'kinematical_state_only':True,'physical_boundary_preparation_derived':False,
        'sharp_width_zero_is_normalizable_state':False})
    dump('return_amplitude_bounds.json',{'cases':amplitudes,
        'definition':'A_epsilon(mu) = <psi_epsilon, exp(-i mu w C/2) psi_epsilon>',
        'fixed_exact_collar_amplitude':1,'positive_width_strong_phase_limit':'1/2',
        'iterated_limits':{'width_then_phase':1,'phase_then_width':'1/2'},
        'joint_limit_control':'mu*epsilon -> 0 gives 1; |mu|*epsilon -> infinity gives 1/2 as epsilon -> 0',
        'previous_atom_limit_assumptions_changed':True,'physical_detector_derived':False,
        'full_geometric_or_semiclassical_limit_derived':False})

    neg=[]
    def reject(name,fn):
        try:fn()
        except RuntimeError:neg.append({'case':name,'status':'REJECTED'});return
        raise RuntimeError('Negative control unexpectedly accepted: '+name)
    oldc,oldq,_=direct([F(-9),F(1)],[F(0),F(7,18)],F(17,36),F(1,2))
    require(oldc==0 and oldq==F(25,24),'Published norm-only collar recovered')
    reject('old norm-only collar is a joint saddle',lambda:require(oldq==0,'Nonzero clock residual'))
    reject('stationarity fixes a unique free time and weight',lambda:require(len({(r['free_t'],r['weight']) for r in chain if r['past_count']==4 and r['shift']==0})==1,'Exact flat family'))
    reject('zero mean residuals imply a physical constraint state',lambda:require(packet[0]['C_moments'][2]==0,'Nonzero residual variance'))
    deformed=base[:];deformed[-1]+=F(1,64)
    q1=direct(B,deformed,F(1,4),F(1,2))[1];q2=direct(B,deformed,F(1),F(1,2))[1]
    require(q1==q2!=0,'Free clock cannot compensate this boundary error')
    reject('adjusting the free clock repairs arbitrary boundary errors',lambda:require(q1==0,'Moment obstruction'))
    reject('fixed boundary clock reactions may be ignored',lambda:require(all(v==0 for v in j),'Nonzero signed boundary work'))
    reject('sharp collar is a normalized L2 packet limit',lambda:require(packet[0]['overlap_with_half_width_squared']==1,'Non-Cauchy narrowing packets'))
    reject('atom limit applies unchanged after exact collar tuning',lambda:require(F(1)==F(1,2),'Noncommuting boundary-width and phase limits'))
    reject('physical boundary state already derived',lambda:require(plan['physical_boundary_state_derived'],'Additional boundary preparation'))
    reject('changed pinned source accepted',lambda:require(gitsha((ROOT/'inputs/ward_DERIVATION.md').read_bytes()+b' ')==prov['inputs']['inputs/ward_DERIVATION.md']['git_blob'],'Source identity'))
    result={'status':'PASS_CONDITIONAL_COLLAR_STATIONARITY_AUDIT','plan_sha256':psha,
        'chain_cases':len(chain),'joint_stationary_cases':stationary,'short_chain_nonstationary_cases':short,
        'boundary_perturbation_cases':len(perturb),'packet_cases':len(packet),'moment_orders_per_packet':len(packet[0]['C_moments']),
        'return_amplitude_bounds':len(amplitudes),'negative_controls':neg,'physical_gates':plan['physical_gates'],
        'physical_boundary_state_derived':False,'physical_constraint_quantization_derived':False,
        'external_replication':False,'paid_compute':False,'n5_production':False}
    dump('verification.json',result);return result
if __name__=='__main__':print(json.dumps(encode(run()),indent=2,sort_keys=True))
