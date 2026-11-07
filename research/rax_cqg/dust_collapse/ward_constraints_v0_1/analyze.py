"""Small exact action/constraint controls and certified characteristic-function balls."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,factorial
from itertools import product
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from exact_core import C,encode,require,gitsha,sqrt_upper
ROUND=10**40
def dump(name,value):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')
def orders(n):
    pairs=[(i,j) for j in range(n) for i in range(j)]
    out=[]
    for mask in range(1<<len(pairs)):
        rel={(i,j) for k,(i,j) in enumerate(pairs) if mask>>k&1}
        if all((i,k) in rel for i,j in rel for jj,k in rel if j==jj):out.append(rel)
    return out
def anchored(rel,n):return {(0,j) for j in range(1,n+1)}|{(i+1,j+1) for i,j in rel}
def coefficients(rel,N,T):
    a=[F(1,2)]*N;links=[]
    for y,x in sorted(rel):
        k=sum((y,z) in rel and (z,x) in rel for z in range(N))
        B=[1,-9,16,-8][k] if k<4 else 0
        a[x]+=F(B,4)*(T[x]-T[y])**2
        links.append((y,x,B))
    return a,links
def action(rel,N,T,w):return -sum((v*a for v,a in zip(w,coefficients(rel,N,T)[0])),F(0))
def rounded(z):
    r=F(z.r.numerator*ROUND//z.r.denominator,ROUND)
    i=F(z.i.numerator*ROUND//z.i.denominator,ROUND)
    return C(r,i),abs(z.r-r)+abs(z.i-i)
def exp_ball(u,degree):
    x=u;s=0
    while abs(x)>1:x/=2;s+=1
    z=C(F(1));term=z
    for k in range(1,degree+1):term=term*C(F(0),-x/F(k));z=z+term
    radius=abs(x)**(degree+1)/factorial(degree+1)
    z,r=rounded(z);radius+=r
    for _ in range(s):
        z,r=rounded(z*z);radius=2*radius+radius*radius+r
        # Outward radius rounding keeps rational denominators small.
        radius=F(-(-radius.numerator*ROUND//radius.denominator),ROUND)
    return z,radius
def characteristic_ball(u,degree):
    if not u:return C(F(1)),F(0)
    z,r=exp_ball(u,degree)
    value=C(F(1,2))+(C(F(1))-z)*C(F(0),-F(1,2)/u)
    value,rr=rounded(value)
    return value,r/(2*abs(u))+rr
def ac(t,b):return F(1,2)+(t-b)**2/4
def integrated_power_derivative(k,b,L):
    # Differentiate the exact integrated polynomial in external b.
    total=F(0)
    for j in range(k+1):
        coeff=F(comb(k,j))*F(1,2)**(k-j)*F(1,4)**j
        for ell in range(0,2*j+1,2):
            power=2*j-ell
            if power:
                total+=coeff*comb(2*j,ell)*(-1)**power*power*b**(power-1)*L**ell/F(ell+1)
    return total
def run():
    plan=json.loads((ROOT/'plan.json').read_text());sha=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(sha==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'provenance.json').read_text())
    for name,info in prov['inputs'].items():require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Pinned source '+name)
    require(set(plan['physical_gates'].values())=={'HOLD'},'Eight physical HOLD gates')
    require(not plan['physical_constraint_quantization_derived'] and not plan['physical_sector_charge_derived'],'No unproved physical promotion')
    rows=[];shift_count=cut_count=gradient_count=0;first_rows=[];order_counts={}
    for n in range(1,plan['max_new_elements']+1):
        allorders=orders(n);order_counts[n]=len(allorders)
        for order_id,rel0 in enumerate(allorders):
            rel=anchored(rel0,n);N=n+1
            for h in map(F,plan['h']):
                for profile in plan['clock_profiles']:
                    raw=[F(j,n+1) for j in range(1,n+1)]
                    x={'linear':raw,'quadratic':[v*v for v in raw],'late':[(1+v)/2 for v in raw]}[profile]
                    T=[F(-2)]+[-2+4*h*v for v in x]
                    a,links=coefficients(rel,N,T)
                    c1=2*a[1]
                    require(c1==1+8*h*h*x[0]**2 and c1>=1,'Earliest free norm constraint has positive gap')
                    require([y for y,z in rel if z==1]==[0],'First free element has only anchor predecessor')
                    first_rows.append({'n':n,'order_id':order_id,'h':h,'profile':profile,'x1':x[0],'C1':c1})
                    for wp in plan['density_profiles']:
                        w=[F(0)]+{'zero':[F(0)]*n,'uniform_half':[F(1,2)]*n,'ramp':raw}[wp]
                        S=action(rel,N,T,w);q=[F(0)]*N;currents=[]
                        for y,z,B in links:
                            j=w[z]*B*(T[z]-T[y])/2;q[y]+=j;q[z]-=j;currents.append((y,z,j))
                        require(sum(q)==0,'Rigid clock-shift identity')
                        eps=F(1,7)
                        for z in range(N):
                            tp=T[:];tm=T[:];tp[z]+=eps;tm[z]-=eps
                            derivative=(action(rel,N,tp,w)-action(rel,N,tm,w))/(2*eps)
                            require(derivative==q[z],'Exact quadratic finite-difference gradient');gradient_count+=1
                        for shift in map(F,plan['shift_values']):
                            require(action(rel,N,[t+shift for t in T],w)==S,'Shift all clocks including anchor');shift_count+=1
                        for mask in range(1<<N):
                            chosen=lambda z:bool(mask>>z&1)
                            boundary=sum((j for y,z,j in currents if chosen(y) and not chosen(z)),F(0))-sum((j for y,z,j in currents if chosen(z) and not chosen(y)),F(0))
                            require(sum((q[z] for z in range(N) if chosen(z)),F(0))==boundary,'Exact cut balance');cut_count+=1
                        rows.append({'n':n,'order_id':order_id,'h':h,'clock_profile':profile,'density_profile':wp,'action':S,'clock_gradient':q})
    require(order_counts=={1:1,2:2,3:7},'Natural-order enumeration')
    dump('clock_symmetry.json',{'order_counts':order_counts,'cases':rows,'action_cases':len(rows),
        'exact_gradient_components':gradient_count,'common_shift_controls':shift_count,'cut_balances':cut_count,
        'sector_charge_identified_with_clock_generator':False})

    approx=[]
    h=F(1,2);mean_C2=1+F(16,3)*h*h+F(64,5)*h**4
    require(mean_C2==F(47,15),'First-element constraint second moment')
    for eps in map(F,plan['approximate_zero_eps']):
        norm2=F(1,2)*(2/eps)*eps
        weighted_norm2=F(1,2)*(2/eps)*(eps**3/3)*mean_C2
        require(norm2==1 and weighted_norm2==F(47,45)*eps*eps,'Normalized positive-stratum approximate zero sequence')
        approx.append({'epsilon':eps,'state_norm_squared':norm2,'positive_stratum_probability':1,
            'atom_projection_norm_squared':0,'C_residual_squared':mean_C2,'wC_residual_squared':weighted_norm2,
            'successive_overlap_squared':F(1,2)})
    # Additional analytic witness, explicitly outside the frozen control grid.
    collar_T=[F(0),F(7,18),F(17,36)];collar_rel={(0,1),(1,2),(0,2)}
    collar_a,collar_links=coefficients(collar_rel,3,collar_T)
    require(2*collar_a[2]==0,'Two fixed predecessor clocks permit the normalization equation')
    collar_w=[F(0),F(0),F(1,2)]
    collar_q2=-sum((collar_w[z]*B*(collar_T[z]-collar_T[y])/2 for y,z,B in collar_links if z==2),F(0))
    require(collar_q2==F(25,24),'Normalization witness is not a full stationary solution')
    dump('constraint_domain.json',{'first_layer_cases':first_rows,'global_lower_bound_C1':1,
        'operator_candidates':{'M_C1':'zero kernel on full kinematical space; wrongly extends atom tangent variation',
            'Pi_positive_M_C1':'kernel is atom subspace; gap at least 1 on positive stratum',
            'M_w1C1':'same atom kernel but no positive-stratum spectral gap'},
        'approximate_zero_sequence':approx,'balanced_target_wC_residual_squared':mean_C2/6,
        'additional_dirac_quantization':'NOT_DERIVED_FROM_REGULATED_AMPLITUDE',
        'supplemental_boundary_witness':{'declared_after_frozen_grid':True,'clock_values':collar_T,'fixed_clocks':[0,1],
             'free_element':2,'C2':2*collar_a[2],'w2':F(1,2),'clock_residual_q2':collar_q2,
             'scope':'Additional analytic witness only; changes boundary data and is not a complete saddle or validated repair'},
        'classical_interior_saddle_first_layer':'ABSENT_IN_DECLARED_BOUNDARY_MODEL',
        'absence_is_not_a_CST_no_go':True})

    ward=[]
    for b in map(F,plan['boundary_b']):
        for L in map(F,plan['boundary_L']):
            for k in range(plan['ward_max_order']+1):
                lhs=integrated_power_derivative(k,b,L)
                rhs=-(ac(L,b)**k-ac(-L,b)**k)/(2*L)
                require(lhs==rhs,'Fixed-box Ward identity coefficient')
                ward.append({'b':b,'L':L,'order':k,'integrated_external_derivative':lhs,'negative_endpoint_difference':rhs})
    b,L=F(1,2),F(1)
    plus,rp=characteristic_ball(ac(L,b),plan['characteristic_degree'])
    minus,rm=characteristic_ball(ac(-L,b),plan['characteristic_degree'])
    derivative=(minus-plus)*F(1,2);radius=(rp+rm)/2
    require(derivative.i+radius<0,'Nonzero fixed-box Ward boundary term certified')
    dump('ward_boundary.json',{'coefficient_controls':ward,'nonzero_example':{'b':b,'L':L,'derivative_center':derivative,'radius':radius},
        'fixed_absolute_box':'external clock derivative equals minus normalized endpoints',
        'translated_relative_window':'joint translation including endpoints preserves amplitude exactly',
        'physical_gauge_generator_derived':False})

    characteristic=[]
    for u in map(F,plan['characteristic_u']):
        z,rad=characteristic_ball(u,plan['characteristic_degree'])
        require(z.r-rad>F(1,3),'Strict positive real floor in exact mixed-measure factor')
        if u:
            upper=sqrt_upper((z-C(F(1,2))).norm2(),10**35)+rad
            require(upper<=1/abs(u),'Density-factor remainder bounded by inverse phase')
        else:upper=F(1,2)
        characteristic.append({'u':u,'center':z,'radius':rad,'real_lower':z.r-rad,'distance_to_half_upper':upper})
    high=[]
    for mu in map(F,plan['high_phase_values']):
        high.append({'mu':mu,'first_positive_stratum_amplitude_upper':min(F(1,2),2/abs(mu)),
            'bound_kind':'analytic uniform upper bound; not a new amplitude evaluation'})
    dump('density_atom_limit.json',{'characteristic_controls':characteristic,
        'per_factor_lower_bound':'Re chi(u) >= (1-1/pi)/2 > 1/3 for all real u',
        'fixed_n_matter_amplitude_limit':[{'n':n,'limit':F(1,2**n)} for n in range(1,4)],
        'limit_assumptions':'fixed finite anchored order; normalized ordered-clock measure; original independent half-atom density measure; all density variables integrated; matter phase mu -> infinity; no n-sum interchange',
        'first_stratum_bounds':high,'density_integration_was_already_in_published_kernel':True,
        'new_dimension_reduction_claimed':False,'physical_semiclassical_limit_derived':False})

    negative=[]
    def reject(name,fn):
        try:fn()
        except RuntimeError:negative.append({'case':name,'status':'REJECTED'});return
        raise RuntimeError('Negative control not rejected: '+name)
    reject('earliest free interior dust-normalization saddle exists',lambda:require(any(v['C1']==0 for v in first_rows),'Positive first-layer constraint'))
    reject('weighted approximate zeros are near atom-kernel states',lambda:require(approx[-1]['atom_projection_norm_squared']>F(9,10),'Unit norm remains in positive stratum'))
    reject('fixed absolute box boundary can be omitted',lambda:require(abs(derivative.i)<=radius,'Certified nonzero Ward boundary'))
    reject('finite density integral is a delta constraint',lambda:require(characteristic[3]['real_lower']==0,'Positive smooth Fourier factor away from zero'))
    reject('strong matter phase removes all density-factor amplitude',lambda:require(F(1,2)==0,'Persistent atom contribution'))
    reject('clock-shift symmetry derives the binary sector charge',lambda:require(plan['physical_sector_charge_derived'],'Independent variable and generator'))
    prior_uses_density_elimination='Die analytische Dichteintegration' in (ROOT/'inputs/four_element_DERIVATION.md').read_text()
    require(prior_uses_density_elimination,'Prior publication establishes existing density elimination')
    reject('density elimination is a newly obtained saving',lambda:require(not prior_uses_density_elimination,'Already present in pinned four-element kernel'))
    reject('changed source byte accepted',lambda:require(gitsha((ROOT/'inputs/variation_DERIVATION.md').read_bytes()+b' ')==prov['inputs']['inputs/variation_DERIVATION.md']['git_blob'],'Pinned source'))
    result={'status':'PASS_CONDITIONAL_SYMMETRY_AND_CONSTRAINT_AUDIT','plan_sha256':sha,
        'action_cases':len(rows),'exact_gradient_components':gradient_count,'common_shift_controls':shift_count,
        'cut_balances':cut_count,'first_layer_cases':len(first_rows),'approximate_zero_cases':len(approx),
        'ward_coefficient_controls':len(ward),'certified_characteristic_cases':len(characteristic),
        'negative_controls':negative,'physical_gates':plan['physical_gates'],
        'physical_constraint_quantization_derived':False,'physical_sector_charge_derived':False,
        'new_density_integration_saving':False,'external_replication':False,'paid_compute':False,'n5_production':False}
    dump('verification.json',result);return result
if __name__=='__main__':print(json.dumps(encode(run()),indent=2,sort_keys=True))
