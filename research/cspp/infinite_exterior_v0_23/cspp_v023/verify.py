"""Independent positive quadratures, exact identities and complete budget checks."""
import gzip,hashlib,math
from fractions import Fraction as F
from flint import arb,acb,ctx
from common import HERE,read,write,ball,enc,require
from bounds import BoundEngine,COEFF,SQUARED,EDGES,gaussian_moment,power_integral

def stable(x,y):
    x,y=arb(x),arb(y);require(x.is_finite() and y.is_finite(),'finite comparison')
    require(abs(x-y)<arb('1e-10')*max(arb(1),abs(x).upper(),abs(y).upper()),'stable bound or decomposition')
def integrate(f,l,u):
    z=acb.integral(f,acb(l),acb(u),abs_tol=arb('1e-30'),rel_tol=arb('1e-30'))
    require(z.is_finite() and z.imag.contains(0),'finite independent quadrature');return z.real
def poly(z):return 1+9*z+8*z*z+arb(4)/3*z*z*z

def analytic_controls(engine):
    counts={};require(SQUARED==list(map(F,[1,18,97]))+[F(440,3),F(88),F(64,3),F(16,9)],'exact square polynomial')
    count=0
    for J in range(1,35):
        n=2*J-2;half_gamma=arb.pi().sqrt()*math.factorial(2*n)/(4**n*math.factorial(n))
        require(half_gamma.overlaps(ball(2*J-F(3,2)).gamma()),'half-integer gamma factorial identity');count+=1
    counts['half_integer_gamma_identities']=count
    count=0;wrong_constant=0
    for J in [1,2,3,8]:
        for lam in [F(1),F(16),F(64)]:
            def f(theta,a):return 4*arb.pi()*theta.sin()**(4*J-4)*theta.cos()**2*(-ball(lam)*theta.sin()**2).exp()
            exact=integrate(f,0,arb.pi()/2);bound=2*arb.pi()*ball(2*J-F(3,2)).gamma()/ball(lam)**ball(2*J-F(3,2))
            require(exact>0 and exact.upper()<bound.lower(),'Fourier radial integral below gamma majorant')
            if exact.lower()>bound.upper()/(2*arb.pi()):wrong_constant+=1
            count+=1
    require(wrong_constant>0,'negative control rejects omitted Fourier factor')
    counts['independent_fourier_integrals']=count;counts['wrong_fourier_constant_rejected']=wrong_constant
    count=0
    for squared in [False,True]:
        for S in [16,52]:
            for m in [0,2,4]:
                B=arb(256);rate=64 if squared else 128;power=2 if squared else 1
                def f(s,a):
                    z=s*s/128;P=poly(z);return s**m*(-s*s/rate).exp()*(P*P if squared else P)
                target=gaussian_moment(m,F(S),squared,ctx.prec)
                value=integrate(f,S,B)+arb(0).union((rate/B*f(acb(B),False).real).upper())
                require(value.overlaps(target),'independent positive kernel moment');count+=1
    counts['independent_kernel_moment_quadratures']=count
    count=0
    for p in [F(0),F(1,4),F(5,4),F(9,4),F(21,4)]:
        for sigma in [arb(0),arb(9)/4]:
            value=integrate(lambda t,a:(t+sigma)*t**(-ball(p)),5,8)
            require(value.overlaps(power_integral(p,F(5),F(8),sigma)),'finite power primitive quadrature');count+=1
    for J in [3,4,8]:
        for L in [F(5),F(8),F(32)]:
            sigma=arb(9)/4
            v=integrate(lambda u,a:4*u**(4*J-12)+4*sigma*u**(4*J-8),0,ball(L)**(-arb(1)/4))
            require(v.overlaps(power_integral(F(J)-F(3,4),L,None,sigma)),'infinite power primitive via compact transform');count+=1
    counts['independent_power_integral_quadratures']=count
    count=0
    for L,S in [(5,16),(8,16),(32,16),(5,52),(8,52),(32,52)]:
        H=arb(S*S);sigma=arb(9)/4;D=16*arb(1).exp();l=arb(L);B=arb(S+256);kappa=engine.kappa
        def primitive(x):return x**4/4+(2*H+sigma)*x**3/3+(H*H+2*H*sigma)*x*x/2+H*H*sigma*x
        def difference(s):
            x=s*s
            return (x-l)*((x**3+x*x*l+x*l*l+l**3)/4+(2*H+sigma)*(x*x+x*l+l*l)/3+(H*H+2*H*sigma)*(x+l)/2+H*H*sigma)
        lo=l.sqrt();v=arb(0)
        if lo<S:v+=integrate(lambda s,a:difference(s)*kappa*kappa,lo,S);lo=arb(S)
        v+=integrate(lambda s,a:difference(s)*D*D*(-s*s/64).exp()*poly(s*s/128)**2,lo,B)
        tail=64/B*primitive(B*B)*D*D*(-B*B/64).exp()*poly(B*B/128)**2
        v+=arb(0).union(tail.upper())
        _,details=engine.far(F(L),S,D,sigma)
        require(v.overlaps(details['polynomial_integral']),'independent positive Cauchy time polynomial integral');count+=1
    counts['independent_far_polynomial_quadratures']=count
    # Rational proof of T-sqrt(T^2-s)<=1/4: at tau=5, 5/2-1/16 > sqrt(5), and the difference increases.
    require(F(39,16)**2>5 and F(1,2)>F(1,4),'uniform near-strip geometric margin')
    require(all(EDGES[i+1]>EDGES[i] for i in range(len(EDGES)-1)) and EDGES[0]==5 and EDGES[-1]==2**48,'complete ordered tail intervals')
    return counts

def poisson_controls(engine):
    count=0
    for n0 in [0,8,40,128]:
        for s,Q,S in [(F(16),F(0),16),(F(52),F(1),52),(F(80),F(10),52)]:
            z=ball(s*s/128);mu=16*(z-ball(Q));require(mu>0,'positive test Poisson mean')
            probability=(-mu).exp();summation=arb(0)
            for k in range(2049):
                n=k+n0;P=1-arb(9)*n/15+arb(8)*n*(n-1)/225-arb(4)*n*(n-1)*(n-2)/10125
                weight=(arb(15)/16)**n*P;summation+=abs(weight)*probability;probability*=mu/(k+1)
            tail=engine.kappa*((arb(2049)*(1+(mu/2049).log())-mu).exp())
            upper=(summation+tail).upper();kernel=engine.kappa if s<=S else 16*ball(Q).exp()*(-z).exp()*poly(z)
            require(upper<kernel,'Poisson sum plus Chernoff remainder under chosen kernel');count+=1
    return count

def verify():
    ctx.prec=192;provenance=read('PROVENANCE.json');tree=read('evidence/MAIN_TREE.json');entries={r['path']:r['sha'] for r in tree['entries']}
    for r in provenance['files']:
        data=(HERE/r['package_path']).read_bytes();require(len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],'unchanged input SHA256')
        h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();require(h==r['git_blob_sha1']==entries[r['repository_path']],'input Git identity')
    source=read('evidence/v19_BOUNDS_512.json');other=read('evidence/v19_BOUNDS_384.json')
    for j in range(35):require(arb(source['norm_squared'][str(j)]).overlaps(arb(other['norm_squared'][str(j)])),'inherited source norm precision overlap')
    engine=BoundEngine(source);counts=analytic_controls(engine);counts['direct_poisson_controls']=poisson_controls(engine)
    low=read('results/GLOBAL_128.json');high=read('results/GLOBAL_192.json');maxdiff=arb(0);decompositions=0;endpoint_count=0
    for bits,result in [(128,low),(192,high)]:
        ctx.prec=bits;engine=BoundEngine(source);finite=read(f'evidence/v22_FINITE_{bits}.json');old=read(f'evidence/v20_LOCAL_{bits}.json')
        audits=__import__('json').loads(gzip.decompress((HERE/f'results/ENDPOINTS_{bits}.json.gz').read_bytes()));require(len(audits)==result['endpoint_audits']==479,'all known and detector endpoint bounds')
        known=[a for a in audits if a['kind']=='known'];require(len(known)==223,'all known first endpoints')
        for wi,window in enumerate(result['windows']):
            det=[a for a in audits if a['kind']=='detector' and a['window']==wi];require(len(det)==128 and sum(F(a['mass']) for a in det)==1,'whole normalized detector')
            direct=sum((ball(F(a['mass']))*arb(a['tail_bounds'][0]['direct_tail_upper']) for a in det),arb(0));stable(direct,window['direct_detector_upper'])
            uniform=window['uniform_active_endpoint'];last=None
            for r in uniform['tail_bounds']:
                v=arb(r['direct_tail_upper']);require(v>0,'positive infinite tail bound')
                if last is not None:require(v<last,'decreasing valid remote-tail bounds')
                last=v
            for k,row in enumerate(window['archives']):
                fs=[arb(a['tail_bounds'][0]['direct_tail_upper']) for a in known if a['archive']==row['key']]
                require(len(fs)==row['active_count'],'known endpoint inventory');aa=[acb(*map(arb,z)) for z in old['archives'][k]['adjoints'][wi]]
                transport=sum((z.abs_upper()*f for z,f in zip(aa,fs)),arb(0));D=arb(uniform['tail_bounds'][0]['direct_tail_upper'])
                unknown=D*(1+engine.gamma)**len(fs)*((engine.gamma*arb(29)/512).exp()-1)
                stable(transport,row['known_active_tail_upper']);stable(unknown,row['unknown_active_tail_upper']);stable(direct,row['direct_tail_upper'])
                tail=direct+transport+unknown;stable(tail,row['complete_tail_upper'])
                fin=arb(finite['levels'][-1]['archives'][k]['windows'][wi]['finite_total_upper']);require(fin.overlaps(arb(row['finite_v022_upper'])),'unchanged finite bound')
                stable(fin+tail,row['complete_global_upper']);require(arb(row['complete_global_upper'])<arb(row['v019_global_upper']),'improved same-scope global bound');decompositions+=1
        for a in audits:
            r=a['tail_bounds'][0];stable(arb(r['near_upper'])+arb(r['far_upper']),r['direct_tail_upper'])
            far=arb(r['far_upper']);v1=arb(r['far_L1_upper']);v2=arb(r['far_L2_upper'])
            require(far>=0 and (far.overlaps(v1) or far.overlaps(v2)),'selected endpoint lies in a certified far enclosure')
            stable(far,min(v1.upper(),v2.upper()))
            if isinstance(a['near_audit'],dict):
                bins=a['near_audit']['bins'];require([F(x['L']) for x in bins]==EDGES and bins[-1]['U']=='infinity','no infinite tail gap')
            else:require(arb(a['C_upper'])<=-arb(1)/2,'exact empty near-source support')
            endpoint_count+=1
        require(result['new_random_calls']==0 and result['status']['METHOD']==result['status']['G1']=='HOLD','unchanged scientific gates')
    ctx.prec=192
    for lw,hw in zip(low['windows'],high['windows']):
        for l,h in zip(lw['archives'],hw['archives']):
            for k in ['direct_tail_upper','known_active_tail_upper','unknown_active_tail_upper','complete_tail_upper','complete_global_upper']:stable(l[k],h[k])
            maxdiff=max(maxdiff,abs(arb(l['complete_global_upper'])-arb(h['complete_global_upper'])).upper())
    counts.update({'source_files':len(provenance['files']),'source_norm_precision_overlaps':35,'endpoint_audits_checked':endpoint_count,'global_decompositions':decompositions})
    # Deliberately wrong integration domain and normalization are caught exactly.
    require(EDGES[0]!=8,'negative control rejects the missing 5<tau<8 strip')
    require(sum(F(a['mass']) for a in audits if a['kind']=='detector' and a['window']==0 and a['radius_bounds']!=['31/16','2'])!=1,'negative control rejects missing detector shell')
    require(any(arb(r['unknown_active_tail_upper'])>0 for w in high['windows'] for r in w['archives']),'negative control rejects omitted unknown paths')
    out={'status':'PASS','counts':counts,'maximum_global_majorant_precision_difference':enc(maxdiff),
      'negative_controls':{'missing_initial_tail_strip':'REJECTED','missing_detector_shell':'REJECTED','omitted_unknown_paths':'REJECTED','wrong_Fourier_constant':'REJECTED'},
      'independent_scientific_review':'NOT_PERFORMED','METHOD':'HOLD','G1':'HOLD','infinite_tail_combined':True,'new_random_calls':0}
    write(HERE/'results/CHECKS.json',out);print(__import__('json').dumps(out,indent=2));return out
if __name__=='__main__':verify()
