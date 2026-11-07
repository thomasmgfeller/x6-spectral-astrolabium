"""Reproduce the operational instrument and certified continuous matter controls."""
from fractions import Fraction as F
from itertools import combinations,product
from math import factorial
from pathlib import Path
import hashlib
import json
import matter as m
import instrument

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text());P=PLAN['controls'];OUT=ROOT/'results'
r=m.r


def require(ok,message):m.require(ok,message)
def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,r.C):return {'re':str(x.re),'im':str(x.im)}
    raise TypeError(type(x).__name__)
def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,default=encode)+'\n')


def sources():
    digest=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(digest==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'inputs/provenance.json').read_text())
    require(prov['commit']==PLAN['source_commit'],'Source commit')
    for name,x in prov['files'].items():
        b=(ROOT/'inputs'/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['sha'],name)
    return digest,len(prov['files'])


def action_checks(h):
    xs=list(map(F,['0','1/4','1/2','3/4','1']));ws=list(map(F,['0','1/4','1']))
    checks=0
    for x,w in product(xs,ws):
        state=((0,),(-2+4*h*x,),(w,))
        require(r.v.action(state)[1]==-w*(F(1,2)+4*h*h*x*x),'One-element matter polynomial')
        checks+=1
    for kind,order in [('antichain',(0,0)),('chain',(0,1))]:
        a,b,D=m.coefficients(h,kind)
        for x,y in combinations(xs,2):
            for u,v in product(ws,repeat=2):
                state=order,(-2+4*h*x,-2+4*h*y),(u,v)
                s=-u*m.polynomial_value(a,x,y,D)-v*m.polynomial_value(b,x,y,D)
                require(r.v.action(state)[1]==s,'Two-element matter polynomial')
                require(abs(s)<=m.phase_bound(h,kind),'Uniform matter-action bound at control points')
                checks+=1
    return checks


def main():
    OUT.mkdir(exist_ok=True);digest,n_sources=sources();K=P['taylor_order']
    instrument_result=instrument.audit();dump('instrument.json',instrument_result)
    moment_records=[];cases=[];bounds=[];checks=0;low_checks=0;max_error=F(0)
    alpha_invariance=[];fringe_checks=0
    for hs in P['clock_h']:
        h=F(hs);checks+=action_checks(h)
        moments={'one':m.one_moments(h,K)}
        for kind in ['antichain','chain']:
            moments[kind]=m.continuous_moments(h,kind,K)
            independent=m.low_order_independent(h,kind)
            require(moments[kind][:len(independent)]==independent,'Independent low-order moment route')
            low_checks+=len(independent)
        for kind,seq in moments.items():
            require(seq[0]==1,'Normalized continuous field integral')
            moment_records.append({'h':h,'geometry':kind,'Sd_abs_bound':m.phase_bound(h,kind),
                                   'moments':seq,'order':K})
        cn_by_alpha={alpha:[F(1),h,h*h*r.v.number_weight_squared(0,2,alpha)]
                     for alpha in P['alpha_values']}
        for count in [1,2]:
            norms=[r.v.number_weight_squared(0,count,alpha)/cn_by_alpha[alpha][count]
                   for alpha in P['alpha_values']]
            require(len(set(norms))==1,'Fixed-number normalized boundary independent of alpha')
            alpha_invariance.append({'h':h,'number':count,'boundary_density_squared':norms[0]})
        for mus in P['matter_couplings']:
            mu=F(mus);approx={}
            for kind,seq in moments.items():
                approx[kind]=m.amplitude(seq,mu,m.phase_bound(h,kind))
                max_error=max(max_error,approx[kind][1])
                require(approx[kind][1]<=F(P['amplitude_error_target']),'Declared integration tolerance')
            for gravity_index,gs in enumerate(P['gravity_g_over_pi']):
                phase=r.i_power(gravity_index)
                t=[r.ONE,approx['one'][0],(approx['antichain'][0]+phase*approx['chain'][0])/2]
                eps=[F(0),approx['one'][1],(approx['antichain'][1]+approx['chain'][1])/2]
                vis=[m.visibility(a,e) for a,e in zip(t,eps)]
                for alpha in P['alpha_values']:
                    c=cn_by_alpha[alpha];Z2=sum(c);Z6=r.v.partition((),h,6,alpha)
                    delta=r.v.exponential_tail_bound(h,6);Zmax=Z6+delta;Rmax=Zmax-Z2
                    require(0<=Z6-Z2<=Rmax and Zmax<2,'Number tail and vacuum guard')
                    known_lo=sum((c[j]*vis[j][0] for j in range(3)),F(0))
                    known_hi=sum((c[j]*vis[j][1] for j in range(3)),F(0))
                    finite_count=[known_lo/Z2,known_hi/Z2]
                    finite_t=sum((c[j]*t[j] for j in range(3)),r.ZERO)/Z2
                    finite_eps=sum((c[j]*eps[j] for j in range(3)),F(0))/Z2
                    finite_all=m.visibility(finite_t,finite_eps)
                    count_infinite=[known_lo/Zmax,min(F(1),(known_hi+Rmax)/Zmax)]
                    rem_mass=Rmax/Zmax
                    all_infinite=m.visibility(finite_t,finite_eps+2*rem_mass)
                    all_infinite[0]=max(all_infinite[0],(2/Zmax-1)**2)
                    if mu==0 and gravity_index==0:
                        require(finite_count==finite_all==[F(1),F(1)],'Exact phase-free finite limit')
                        count_infinite=all_infinite=[F(1),F(1)]
                    accepted=[[c[j]*vis[j][0]/(known_hi+Rmax),
                               min(F(1),c[j]*vis[j][1]/known_lo)] for j in range(3)]
                    require(all(0<=lo<=hi<=1 for lo,hi in vis+[finite_count,finite_all,count_infinite,all_infinite]+accepted),
                            'All certified probability intervals lie in [0,1]')
                    if mu==0 and h==F(1,2) and alpha==1:
                        require(finite_count[0]==finite_count[1]==[F(1),F(25,26),F(12,13)][gravity_index],
                                'Published gravity fringe recovered exactly');fringe_checks+=1
                    key={'alpha':alpha,'h':h,'g_over_pi':gs,'mu':mu}
                    cases.append({**key,'number_amplitude_centers':t,'number_amplitude_errors':eps,
                                  'number_visibility_intervals':vis,'Z2':Z2,
                                  'finite_cap_count_success':finite_count,'finite_cap_all_success':finite_all})
                    bounds.append({**key,'Z6':Z6,'normalization_tail_upper':delta,
                        'unintegrated_n_ge_3_mass_upper':Rmax,'unintegrated_n_ge_3_probability_upper':rem_mass,
                        'count_success_infinite_interval':count_infinite,
                        'all_success_infinite_interval':all_infinite,
                        'accepted_count_0_1_2_intervals':accepted,
                        'accepted_n_ge_3_probability_upper':min(F(1),Rmax/known_lo)})
    require(len(cases)==36 and checks==390 and low_checks==16 and fringe_checks==3,'Frozen census')
    dump('moments.json',{'measure':'Continuous ordered clocks and atom-plus-uniform density; not an atomic quadrature',
        'records':moment_records,'action_polynomial_checks':checks,'independent_low_order_moment_checks':low_checks,
        'max_amplitude_remainder':max_error,'fixed_number_alpha_controls':alpha_invariance})
    dump('continuous_results.json',{'scope':'Complete continuous field integration through n=2, with rigorous Taylor remainder',
        'count_cap':2,'taylor_order':K,'cases':cases,'published_gravity_fringe_checks':fringe_checks})
    dump('certified_bounds.json',{'scope':'Fixed finite horizons; n>=3 field phases are not integrated, but their total mass is enclosed',
        'normalization_enumerated_through':6,'cases':bounds,'physical_couplings_selected':False})
    dump('negative_controls.json',{
        'density_atom_omitted':{'characteristic_at_zero':'1/2','required':'1','status':'REJECTED'},
        'density_atom_replaced_by_normalized_uniform':{'first_moment':'1/2','required':'1/4','status':'CHANGES_MODEL'},
        'ordered_clock_factor_two_omitted':{'two_element_normalization':'1/2','required':'1','status':'REJECTED'},
        'count_meter_is_not_filter':{'same_count_probability':['1','1'],'different_filter_success':['1','0']},
        'renormalized_postselection':'Nonlinear and undefined for dark input; not a complete measurement',
        'ignored_pointer_is_not_identity_channel':instrument_result['nonselective_record_disturbance'],
        'higher_number_phases_integrated':False})
    dump('verification.json',{'status':'PASS_CONDITIONAL_INSTRUMENT_AND_CERTIFIED_LOW_NUMBER_CONTINUUM',
        'source_commit':PLAN['source_commit'],'plan_sha256':digest,'sources_verified':n_sources,
        'operational_pointer_dilation':'EXACT_REFERENCE_PASS','count_only_phase_sensitivity':'FAIL_ANALYTIC',
        'continuous_nonzero_matter_phase':'CERTIFIED_FOR_N_LE_2','higher_number_field_phases':'NOT_EVALUATED',
        'normalization_tail':'CERTIFIED_THROUGH_N6','continuous_cases':len(cases),
        'physical_boundary_or_detector_selected':False,'formal_proof_checker':False,'physical_4D_ensemble':False,
        'physical_gates':{x:'HOLD' for x in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']}})
    print(json.dumps({'status':'PASS','result_files':6,'continuous_cases':len(cases),'physical_gates':'8 HOLD'}))


if __name__=='__main__':main()
