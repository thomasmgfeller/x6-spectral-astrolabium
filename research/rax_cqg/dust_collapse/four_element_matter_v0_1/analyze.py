"""Reproduce the complete n=4 continuous reference sector and certified tails."""
from fractions import Fraction as F
from itertools import combinations,product
from math import factorial
from pathlib import Path
import hashlib
import json
import tempfile
import native
from native import g,gauss,fp
import readout as r

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text());P=PLAN['controls'];OUT=ROOT/'results'
require=fp.require


def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,r.C):return {'re':str(x.re),'im':str(x.im)}
    raise TypeError(type(x).__name__)
def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,default=encode)+'\n')
def load(name):return json.loads((ROOT/'inputs'/name).read_text())
def center(value):return r.C(value[0].midpoint(),value[1].midpoint())
def radius(value):return value[0].radius()+value[1].radius()
def cparse(x):return r.C(F(x['re']),F(x['im']))
def key(x):return x['alpha'],F(x['h']),F(x['g_over_pi']),F(x['mu'])


def visibility(t,error):
    slack=2*error+error*error
    return [max(F(0),t.abs2()-slack),min(F(1),t.abs2()+slack)]


def sources():
    digest=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(digest==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=load('provenance.json');require(prov['commit']==PLAN['source_commit'],'Source commit')
    for name,x in prov['files'].items():
        b=(ROOT/'inputs'/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['sha'],name)
    return digest,len(prov['files'])


def action_checks(orders):
    checks=0;records=[]
    xs=list(map(F,P['action_control_grid']));ws=list(map(F,P['density_controls']))
    for hs in P['clock_h']:
        h=F(hs)
        for order in orders:
            _,poly=g.action_polynomials(order,h,cube=False)
            gravity=g.v.m.gravity(g.v.m.with_anchor(order))-1
            for clocks in combinations(xs,4):
                for marks in product(ws,repeat=4):
                    state=order,tuple(-2+4*h*x for x in clocks),marks
                    action=g.v.action(state)
                    require(action[1]==g.evaluate(poly,clocks+marks),'Four-element action polynomial')
                    require(action==g.v.action_by_increments(state),'Full-past action increments')
                    require(action[0]-1==gravity,'Geometry gravity sector')
                    checks+=1
            cube=g.low_moments(order,h);ordered=g.low_moments(order,h,cube=False)
            require(cube==ordered,'Independent cube/ordered exact moment integrals')
            records.append({'h':h,'order':order,'G':gravity,'moments_0_to_3':cube})
    require(checks==32400,'Frozen action census')
    require(len(orders)==40 and len(set(orders))==40,'Forty natural orders')
    require(set(g.v.m.natural_orders(4))==set(orders),'Independent natural-order enumeration')
    require(sum((F(1,40) for _ in orders),F(0))==1,'Geometry normalization')
    _,cube_poly=g.action_polynomials((0,0,0,0),F(1,2))
    wrong_moment=F(0)
    for exponents,c in cube_poly.items():
        value=c
        for j in range(4):value/=exponents[j]+1
        for j in range(4,8):value*=g.density_moment(exponents[j])
        wrong_moment+=value
    right_moment=g.low_moments((0,0,0,0),F(1,2))[1]
    require(wrong_moment!=right_moment,'Omitted full Jacobian changes moment despite unit normalization')
    return {'natural_orders':orders,'action_and_increment_checks':checks,
        'exact_moment_checks':4*len(records),'records':records,
        'negative_controls':{
            'omitted_variable_jacobian_factor':{'cube_integral_of_constant':24,'required':1,'status':'REJECTED'},
            'omitted_entire_jacobian':{'cube_integral_of_constant':1,'required_normalization':1,
                'wrong_first_moment':wrong_moment,'required_first_moment':right_moment,
                'normalization_alone_detects_error':False,'status':'REJECTED_BY_MOMENT'},
            'omitted_ordering_factor':{'normalization':F(1,24),'required':1,'status':'REJECTED'},
            'omitted_natural_order':{'normalization':F(39,40),'required':1,'status':'REJECTED'}
        }}


def bridge():
    prior=load('prior_three_amplitudes.json')['records'];records=[]
    for h in map(F,P['clock_h']):
        for mu in [F(1,4),F(1)]:
            orders=g.v.brute_orders(3);values,errors,cert=native.integrate(orders,h,mu)
            for order,value,error in zip(orders,values,errors):
                old=next(x for x in prior if F(x['h'])==h and F(x['mu'])==mu and tuple(x['order'])==order)
                t=center(value);e=radius(value)+error;previous=cparse(old['amplitude_center']);old_e=F(old['total_error'])
                require((t-previous).abs2()<=(e+old_e)**2,'Native bridge to published 160-bit n3 sector')
                records.append({'h':h,'mu':mu,'order':order,'native_center':t,'native_error':e,
                    'previous_center':previous,'previous_error':old_e,'squared_center_difference':(t-previous).abs2(),
                    'quadrature_orders':cert['orders'],'status':'PASS'})
    require(len(records)==28,'All nonzero-matter n3 geometry bridges');return records


def cost_gate(orders):
    configs=[];total=0
    for h in map(F,P['clock_h']):
        bounds=[g.derivative_bounds(o,h) for o in orders]
        unique={tuple(sorted(p.items())) for o in orders for p in g.action_polynomials(o,h)[0]}
        for mu in [F(1,4),F(1)]:
            qs,_=gauss.select_orders(bounds,mu,F(P['per_geometry_amplitude_error_target']),4)
            nodes=__import__('math').prod(qs);calls=nodes*len(unique);total+=calls
            require(nodes<=PLAN['cost_gate']['max_tensor_nodes_per_configuration'],'Pre-integral node budget')
            configs.append({'h':h,'mu':mu,'orders':qs,'nodes':nodes,'density_characteristic_calls':calls})
    require(total<=PLAN['cost_gate']['max_total_density_characteristic_calls'],'Pre-integral operation budget')
    return {'status':'GO','configurations':configs,'total_density_characteristic_calls':total,
            'node_limit':1200000,'density_call_limit':35000000,'runtime_limit_seconds_per_configuration':600,
            'paid_compute':False}


def main():
    OUT.mkdir(exist_ok=True);digest,source_count=sources();orders=g.v.brute_orders(4)
    budget=cost_gate(orders);print("Cost gate GO: "+str(budget["total_density_characteristic_calls"])+" density evaluations",flush=True)
    controls=action_checks(orders);arithmetic_controls=native.audit();dump('geometry_controls.json',controls)
    bridges=bridge();amplitudes=[];certificates=[];lookup={};max_arith=F(0);max_quad=F(0)
    for hs in P['clock_h']:
        h=F(hs)
        for mus in P['matter_couplings']:
            mu=F(mus)
            values,errors,cert=native.integrate(orders,h,mu)
            certificates.append({'h':h,'mu':mu,**cert});lookup[h,mu]=(values,errors)
            for order,value,error in zip(orders,values,errors):
                a=radius(value);max_arith=max(max_arith,a);max_quad=max(max_quad,error)
                amplitudes.append({'h':h,'mu':mu,'order':order,
                    'G':g.v.m.gravity(g.v.m.with_anchor(order))-1,
                    'amplitude_center':center(value),'real_interval':value[0].endpoints(),
                    'imag_interval':value[1].endpoints(),'arithmetic_error':a,
                    'quadrature_error':error,'total_error':a+error})
            print('Integrated h='+str(h)+' mu='+str(mu)+' orders='+str(cert['orders']),flush=True)
    old_cases=load('prior_extended_results.json')['cases']
    old_bounds={key(x):x for x in load('prior_tail_reduction.json')['cases']}
    cases=[];tails=[];reductions={};containment=0
    for old in old_cases:
        alpha,h,gpi,mu=key(old);old_bound=old_bounds[key(old)]
        values,quad_errors=lookup[h,mu];total=(fp.ZERO,fp.ZERO)
        for order,value in zip(orders,values):
            G=g.v.m.gravity(g.v.m.with_anchor(order))-1
            phase=(fp.ONE,fp.ZERO) if gpi==0 else fp.cis(fp.PI*gpi*G)
            total=fp.cadd(total,fp.cmul(phase,value))
        total=fp.cscale(total,fp.I.rational(F(1,40)))
        t4=center(total);arith4=radius(total);quad4=sum(quad_errors,F(0))/40
        if mu==0 and gpi==0:t4=r.ONE;arith4=F(0)
        eps4=arith4+quad4
        require(eps4<=F(P['per_geometry_amplitude_error_target']),'Mixed n=4 amplitude budget')
        t=list(map(cparse,old['number_amplitude_centers']))+[t4]
        eps=list(map(F,old['number_amplitude_errors']))+[eps4]
        vis=[visibility(z,e) for z,e in zip(t,eps)]
        c=[F(1),h,h*h*g.v.number_weight_squared(0,2,alpha),
           F(7,6)*h**3*g.v.number_weight_squared(0,3,alpha),
           F(40,24)*h**4*g.v.number_weight_squared(0,4,alpha)]
        Z3=F(old['Z3']);Z4=sum(c);Z6=g.v.partition((),h,6,alpha)
        delta=g.v.exponential_tail_bound(h,6);Zmax=Z6+delta;Rmax=Zmax-Z4
        require(Z4==Z3+c[4] and Z6==F(old_bound['Z6']),'Pinned normalization agreement')
        require(0<=Z6-Z4<=Rmax and Zmax<2,'Number remainder and vacuum guard')
        known_lo=sum((c[j]*vis[j][0] for j in range(5)),F(0))
        known_hi=sum((c[j]*vis[j][1] for j in range(5)),F(0))
        finite_count=[known_lo/Z4,known_hi/Z4]
        finite_t=sum((c[j]*t[j] for j in range(5)),r.ZERO)/Z4
        finite_eps=sum((c[j]*eps[j] for j in range(5)),F(0))/Z4
        finite_all=visibility(finite_t,finite_eps)
        count_infinite=[known_lo/Zmax,min(F(1),(known_hi+Rmax)/Zmax)]
        rem_prob=Rmax/Zmax
        all_raw=visibility(finite_t,finite_eps+2*rem_prob)
        all_raw[0]=max(all_raw[0],(2/Zmax-1)**2)
        if mu==0 and gpi==0:count_infinite=all_raw=[F(1),F(1)]
        prior_count=list(map(F,old_bound['count_success_infinite_interval']))
        prior_all=list(map(F,old_bound['all_success_infinite_interval']))
        require(prior_count[0]<=count_infinite[0]<=count_infinite[1]<=prior_count[1],
                'New count interval is contained in previous interval');containment+=1
        all_infinite=[max(all_raw[0],prior_all[0]),min(all_raw[1],prior_all[1])]
        accepted=[[c[j]*vis[j][0]/(known_hi+Rmax),min(F(1),c[j]*vis[j][1]/known_lo)] for j in range(5)]
        require(all(0<=lo<=hi<=1 for lo,hi in vis+[finite_count,finite_all,count_infinite,all_infinite]+accepted),
                'Certified probability intervals')
        k={'alpha':alpha,'h':h,'g_over_pi':gpi,'mu':mu}
        cases.append({**k,'number_amplitude_centers':t,'number_amplitude_errors':eps,
            'number_visibility_intervals':vis,'n4_arithmetic_error':arith4,'n4_quadrature_error':quad4,
            'Z4':Z4,'finite_cap_count_success':finite_count,'finite_cap_all_success':finite_all})
        tails.append({**k,'Z6':Z6,'normalization_tail_n_gt_6_upper':delta,
            'unintegrated_n5_to_6_mass':Z6-Z4,'unintegrated_n_ge_5_mass_upper':Rmax,
            'unintegrated_n_ge_5_probability_upper':rem_prob,
            'count_success_infinite_interval':count_infinite,
            'all_success_infinite_raw_interval':all_raw,'all_success_infinite_interval':all_infinite,
            'all_interval_intersected_with_previous':True,
            'accepted_count_0_1_2_3_4_intervals':accepted,
            'accepted_n_ge_5_probability_upper':min(F(1),Rmax/known_lo),
            'previous_count_interval':prior_count,'previous_count_width':prior_count[1]-prior_count[0],
            'new_count_width':count_infinite[1]-count_infinite[0],'count_containment':'PASS'})
        old_r=F(old_bound['unintegrated_n_ge_4_probability_upper'])
        reductions[alpha,h]={'alpha':alpha,'h':h,'old_phase_tail_probability_upper':old_r,
            'new_phase_tail_probability_upper':rem_prob,'fraction_removed':1-rem_prob/old_r}
    require(len(cases)==36 and len(amplitudes)==240 and containment==36,'Frozen output census')
    all_q=sorted({q for c in certificates for q in c['orders']}|
                 {q for b in bridges for q in b['quadrature_orders']})
    dump('quadrature_certificates.json',{'method':'Positive tensor Gauss-Legendre with analytic derivative remainders',
        'native_fraction_bits':60,'node_reference_fraction_bits':fp.BITS,'cost_gate':budget,'pi_interval':fp.PI.endpoints(),'arithmetic_controls':arithmetic_controls,
        'rules':[gauss.rule(q)[2] for q in all_q],'configurations':certificates,'bridges':bridges})
    dump('four_element_amplitudes.json',{'measure':'Forty natural orders; continuous ordered clocks; atom-plus-uniform density',
        'records':amplitudes,'max_arithmetic_error':max_arith,'max_quadrature_error':max_quad})
    dump('extended_results.json',{'integrated_count_cap':4,'cases':cases})
    dump('tail_reduction.json',{'normalization_count_cap':6,'phase_tail_begins_at':5,
        'weight_reductions':list(reductions.values()),'cases':tails,'count_containment_checks':containment})
    dump('verification.json',{'status':'PASS_CERTIFIED_CONTINUOUS_FOUR_ELEMENT_REFERENCE_SECTOR',
        'source_commit':PLAN['source_commit'],'plan_sha256':digest,'sources_verified':source_count,
        'natural_orders':40,'action_and_increment_checks':32400,'exact_four_element_moment_checks':320,
        'previous_method_bridges':28,'continuous_cases':36,'geometry_amplitudes':240,
        'count_interval_containment_checks':containment,'max_arithmetic_error':max_arith,
        'max_quadrature_error':max_quad,'field_phases_n_ge_5':'NOT_INTEGRATED',
        'physical_boundary_or_detector_selected':False,'formal_proof_checker':False,'physical_4D_ensemble':False,
        'physical_gates':{x:'HOLD' for x in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']}})
    print(json.dumps({'status':'PASS','result_files':6,'continuous_cases':36,'physical_gates':'8 HOLD'}))


if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='cst-native-kernel-') as tmp:
        native.compile_kernel(tmp);main()
