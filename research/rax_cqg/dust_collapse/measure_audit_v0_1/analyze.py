"""Exact moment-preserving matter-measure audit; no field quadrature."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
import geometry as g
import intervals as v
import memory as m
import bounds

def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def gitsha(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):encode(val) for k,val in x.items()}
    if isinstance(x,(list,tuple)):return [encode(val) for val in x]
    return x
def dump(name,data):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(data),indent=2,sort_keys=True)+'\n')

Q=(F(-1),F(12),F(-30),F(20))
def qeval(w):return sum((c*w**j for j,c in enumerate(Q)),F(0))
def legendre_moment(k):
    return F(k*(k-1)*(k-2),(k+1)*(k+2)*(k+3)*(k+4))
def density_moment(k,theta):
    require(k>=0 and isinstance(k,int),'Nonnegative moment order')
    require(abs(theta)<=1,'Positive-family parameter')
    return (F(1) if k==0 else F(1,2*(k+1)))+theta*legendre_moment(k)/2
def clock_moment(k,h):
    return sum((F(comb(k,j),2*j+1)*F(1,2)**(k-j)*(4*h*h)**j for j in range(k+1)),F(0))
def one_moments(h,theta,K):return [density_moment(k,theta)*clock_moment(k,h) for k in range(K+1)]
def complex_multiply(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])

def one_channel(h,mu,theta,degree):
    require(degree%2==0,'Even visibility polynomial degree')
    moments=one_moments(h,theta,degree)
    difference_moments=[];cosine_coeff=[]
    for k in range(0,degree+1,2):
        d=sum(((-1)**j*comb(k,j)*moments[k-j]*moments[j] for j in range(k+1)),F(0))
        require(d>=0,'Even moments of U-U-prime are nonnegative')
        difference_moments.append(d);cosine_coeff.append(F((-1)**(k//2),factorial(k))*d)
    center=sum((c*mu**(2*j) for j,c in enumerate(cosine_coeff)),F(0))
    amax=F(1,2)+4*h*h
    rem=(abs(mu)*amax)**(degree+2)/factorial(degree+2)
    interval=[max(F(0),center-rem),min(F(1),center+rem)]
    # Independent coefficient convolution of A(mu)*conjugate(A(mu)).
    units=[(F(1),F(0)),(F(0),F(-1)),(F(-1),F(0)),(F(0),F(1))]
    coeff=[tuple(z*moments[k]/factorial(k) for z in units[k%4]) for k in range(degree+1)]
    for k in range(degree+1):
        re=im=F(0)
        for j in range(k+1):
            z=complex_multiply(coeff[j],(coeff[k-j][0],-coeff[k-j][1]))
            re+=z[0];im+=z[1]
        target=cosine_coeff[k//2] if k%2==0 else F(0)
        require(im==0 and re==target,'Difference-moment / amplitude-convolution identity')
    a=[sum((c[j]*mu**k for k,c in enumerate(coeff)),F(0)) for j in range(2)]
    erra=(abs(mu)*amax)**(degree+1)/factorial(degree+1)
    center_a=a[0]**2+a[1]**2;radius_a=2*erra+erra*erra
    require(max(interval[0],center_a-radius_a)<=min(interval[1],center_a+radius_a),'Independent amplitude enclosure intersects visibility enclosure')
    return {'h':h,'mu':mu,'theta':theta,'visibility_interval':interval,
            'visibility_center':center,'visibility_remainder':rem,
            'amplitude_center':a,'amplitude_radius':erra,
            'mu4_coefficient':cosine_coeff[2],'difference_moments':difference_moments}

def clock_integral(poly,n,cube=False):
    return sum((c*g.integrate_monomial(key+(0,)*n,n,cube) for key,c in poly.items()),F(0))

def matter_moments(order,h,theta,K=2):
    n=len(order);_,phase=g.action_polynomials(order,h,cube=False)
    poly={(0,)*(2*n):F(1)};out=[]
    for k in range(K+1):
        result=F(0)
        for key,c in poly.items():
            coeff=c;acc=0;clock=F(factorial(n))
            for j in range(n):acc+=key[j];clock/=acc+j+1
            for exponent in key[n:]:coeff*=density_moment(exponent,theta)
            result+=clock*coeff
        out.append(result)
        if k<K:poly=g.mul(poly,phase)
    return out

def geometry_budget(order,h):
    n=len(order);ordered,_=g.action_polynomials(order,h,cube=False)
    cubed,_=g.action_polynomials(order,h,cube=True)
    rows=[]
    for a,ac in zip(ordered,cubed):
        low,high=g.bernstein_bounds(ac,n);maximum=max(abs(low),abs(high))
        a2=g.mul(a,a)
        if low>=0:
            e3=clock_integral(g.mul(a2,a),n);kind='exact_nonnegative_cube'
        elif high<=0:
            e3=-clock_integral(g.mul(a2,a),n);kind='exact_nonpositive_cube'
        else:e3=maximum*clock_integral(a2,n);kind='sup_abs_times_second_moment'
        require(e3>=0,'Positive absolute-cube bound')
        rows.append({'range':[low,high],'absolute_cube_upper':e3,'method':kind})
    return {'order':order,'coefficients':rows,'sum_absolute_cube_upper':sum((r['absolute_cube_upper'] for r in rows),F(0))}

def rejection(fn):
    try:fn()
    except RuntimeError:return True
    raise RuntimeError('Negative control was not rejected')

def analyze():
    plan=json.loads((ROOT/'plan.json').read_text());planhash=digest((ROOT/'plan.json').read_bytes())
    require(planhash==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan identity')
    provenance=json.loads((ROOT/'provenance.json').read_text())
    for name,info in provenance['inputs'].items():require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Pinned input bytes')
    momentchecks=[]
    for k in range(plan['moment_identity_check_k_max']+1):
        direct=sum((c/F(k+j+1) for j,c in enumerate(Q)),F(0))
        require(direct==legendre_moment(k),'Exact perturbation moment identity')
        momentchecks.append({'k':k,'integral_q_wk':direct})
    # Polynomial identities proving -1<=q<=1, without a floating-point grid.
    # q+1=2w[10(w-3/4)^2+3/8]
    # 1-q=2(1-w)[10(w-1/4)^2+3/8].
    require(Q==(F(-1),F(12),F(-30),F(20)),'Declared polynomial')
    positive_checks=[]
    for w in [F(0),F(1,7),F(1,4),F(1,2),F(3,4),F(6,7),F(1)]:
        require(qeval(w)+1==2*w*(10*(w-F(3,4))**2+F(3,8)),'First positivity identity')
        require(1-qeval(w)==2*(1-w)*(10*(w-F(1,4))**2+F(3,8)),'Second positivity identity')
        positive_checks.append(w)
    require([density_moment(k,F(0)) for k in range(3)]==[F(1),F(1,4),F(1,6)],'Reference moments')
    theta_values=list(map(F,plan['diagnostic_theta']));hs=list(map(F,plan['h']));mus=list(map(F,plan['mu']))
    witnesses=[];channels=[]
    for h in hs:
        lead=(2*clock_moment(4,h)-clock_moment(1,h)*clock_moment(3,h))/3360
        require(lead>0,'Positive leading visibility coefficient')
        for mu in mus:
            rows={theta:one_channel(h,mu,theta,plan['visibility_cosine_degree']) for theta in theta_values}
            channels.extend(rows.values())
            for theta in [F(-1),F(1)]:
                r,ref=rows[theta],rows[F(0)]
                gap=[r['visibility_interval'][0]-ref['visibility_interval'][1],r['visibility_interval'][1]-ref['visibility_interval'][0]]
                require(r['mu4_coefficient']-ref['mu4_coefficient']==theta*lead,'Analytic leading-order identity')
                separated=gap[1]<0 or gap[0]>0
                witnesses.append({'h':h,'mu':mu,'theta':theta,'gap_interval':gap,'separated_from_zero':separated,
                                  'leading_mu4_difference':theta*lead})
    require(any(row['separated_from_zero'] for row in witnesses),'At least one fixed-grid counterexample required')
    geometry=[];moment_rows=[];action_checks=0;counts={}
    for n in plan['geometry_controls_n']:
        orders=m.natural_orders(n);require(set(orders)==set(v.brute_orders(n)),'Independent natural-order enumeration')
        counts[n]=len(orders)
        for h in hs:
            for order in orders:
                moments=[matter_moments(order,h,theta) for theta in theta_values]
                require(all(a==moments[0] for a in moments),'Action moments invariant in theta')
                require(moments[1]==g.low_moments(order,h,K=2,cube=False)==g.low_moments(order,h,K=2,cube=True),'Independent original simplex/cube moments')
                moment_rows.append({'n':n,'h':h,'order':order,'common_action_moments':moments[0]})
                xs=tuple(F(j,n+1) for j in range(1,n+1));ws=tuple(F(j,n) for j in range(1,n+1))
                _,poly=g.action_polynomials(order,h,cube=False)
                times=tuple(-2+4*h*x for x in xs)
                require(g.evaluate(poly,xs+ws)==v.action((order,times,ws))[1]==v.action_by_increments((order,times,ws))[1],'Full action agreement');action_checks+=1
                row=geometry_budget(order,h);row.update({'n':n,'h':h});geometry.append(row)
    require(len(m.natural_orders(5))==357 and len(m.natural_orders(6))==4824,'Tail-sector counts')
    uniform=[]
    for h in hs:
        for mu in mus:
            sector=[]
            for n in range(1,5):
                group=[r for r in geometry if r['n']==n and r['h']==h]
                D=sum((min(F(2),F(n,2),abs(mu)**3*r['sum_absolute_cube_upper']/48) for r in group),F(0))/len(group)
                sector.append({'n':n,'amplitude_change_upper':D,'visibility_change_upper':min(F(1),2*D)})
            for alpha in [1,2]:
                cs=[bounds.coefficient(N,h,alpha,n) for n,N in enumerate([1,1,2,7,40,357,4824])]
                tail=cs[5]+cs[6]+bounds.anchored_tail(4824,h,alpha,6);Z4=sum(cs[:5]);Zmax=Z4+tail
                count_upper=(sum((cs[r['n']]*r['visibility_change_upper'] for r in sector),F(0))+tail)/Zmax
                amplitude_upper=(sum((cs[r['n']]*r['amplitude_change_upper'] for r in sector),F(0))+2*tail)/Zmax
                uniform.append({'h':h,'mu':mu,'alpha':alpha,'theta_distance':F(1),'sectors':sector,
                    'unknown_field_norm_upper':tail,'Zmax':Zmax,'number_channel_change_upper':count_upper,
                    'all_number_coherent_visibility_change_upper':min(F(1),2*amplitude_upper),
                    'interpretation':'UPPER_BOUND_NOT_AN_OBSERVED_CHANGE'})
    negative=[]
    tests=[('wrong perturbation sign',lambda:require(-legendre_moment(3)/2==density_moment(3,F(1))-density_moment(3,F(0)),'Sign mismatch')),
           ('missing half-density factor',lambda:require(legendre_moment(3)==density_moment(3,F(1))-density_moment(3,F(0)),'Half-factor mismatch')),
           ('non-normalized trial law',lambda:require(F(1,2)+F(1,2)*(1+F(1,2))==1,'Normalization mismatch')),
           ('theta outside positivity domain',lambda:density_moment(0,F(2))),
           ('false zero visibility gap',lambda:require(witnesses[-1]['gap_interval'][0]<=0<=witnesses[-1]['gap_interval'][1],'Zero excluded')),
           ('changed source byte',lambda:require(gitsha((ROOT/'inputs/memory.py').read_bytes()+b' ') == provenance['inputs']['inputs/memory.py']['git_blob'],'Input changed'))]
    for name,fn in tests:require(rejection(fn),'Expected rejection');negative.append({'case':name,'status':'REJECTED'})
    dump('measure_certificate.json',{'moments':momentchecks,'common_first_moments':['1','1/4','1/6'],
        'common_variance':F(5,48),'positivity_identity_samples':positive_checks,'theta_domain':['-1','1'],
        'positivity_proof':'Polynomial factorizations in DERIVATION.md, not sampling.'})
    dump('one_element_witnesses.json',{'channels':channels,'comparisons':witnesses,'readout':'Conditional n=1 coherent filter visibility'})
    dump('geometry_moment_controls.json',{'counts':counts,'action_checks':action_checks,'rows':moment_rows})
    dump('robustness_bounds.json',{'geometries':geometry,'uniform_bounds':uniform,'bound_theta_distance':1})
    dump('verification.json',{'status':'PASS_EXACT_ANALYTICAL_AUDIT','constant_boundary_reference_invariance':'REFUTED_BY_CONDITIONAL_N1_WITNESS',
        'plan_sha256':planhash,'moment_formula_checks':len(momentchecks),'fixed_visibility_cases':len(channels),
        'separated_counterexamples':sum(r['separated_from_zero'] for r in witnesses),'action_checks':action_checks,
        'geometry_moment_rows':len(moment_rows),'bernstein_geometry_budgets':len(geometry),'uniform_parameter_bounds':len(uniform),
        'negative_controls':negative,'physical_gates':plan['physical_gates'],'n5_production_run':False,
        'interpretation_supplement':'supplement.json and results/transport_controls.json distinguish state changes from representation changes.',
        'does_not_establish':'Physical admissibility of the family, physical inequivalence after covariant state/readout transport, identical classical dynamics, an infinite-channel measured shift, or a bounce.'})
    return witnesses,uniform

if __name__=='__main__':
    witnesses,uniform=analyze()
    print(json.dumps({'status':'PASS','counterexamples':[{'h':str(r['h']),'mu':str(r['mu']),'theta':str(r['theta']),
        'gap_midpoint_approx':float(sum(r['gap_interval'])/2),'gap_width_approx':float(r['gap_interval'][1]-r['gap_interval'][0])} for r in witnesses]},indent=2))
