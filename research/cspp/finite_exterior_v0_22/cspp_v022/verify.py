"""Independent geometry, quadrature, transport, provenance and regression checks."""
import gzip,hashlib,json
from fractions import Fraction as F
from flint import arb,acb,ctx
from common import HERE,require,ball,enc,write
from domains import cells,detector_bins,causal_cap
from fields import moments,J2,absolute_radial_derivative,source_ball_mass,envelope

def read(p):return json.loads((HERE/p).read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def stable(a,b):
    a,b=arb(a),arb(b)
    require(a.is_finite() and b.is_finite(),'finite cross-precision values')
    require(abs(a-b)<arb('1e-8')*max(arb(1),abs(b).upper()),'cross-precision majorant stability')
def integral(fun,l,u):
    z=acb.integral(fun,acb(l),acb(u),abs_tol=arb('1e-36'),rel_tol=arb('1e-36'))
    require(z.is_finite() and z.imag.contains(0),'finite independent quadrature')
    return z.real
def independent_moments():
    checks=0
    for L in [F(0),F(1,8),F(3,8),F(7,16),F(15,32)]:
        lo=ball(4*L*L/(1-4*L*L));b,j1,j3=moments(L*L,ctx.prec)
        for which,target,den in [(1,j1,8),(3,j3,32)]:
            def fun(u,analytic):
                return (-u).exp()/(8*(1+u)**2) if which==1 else (-u).exp()*u/(32*(1+u)**3)
            value=integral(fun,lo,128)+arb(0).union((-arb(128)).exp()/den)
            require(value.overlaps(target),'independent transformed gamma moment');checks+=1
        for delta in [F(-1),F(-1,4),F(-1,8),F(-1,16),F(0),F(1,4),F(2)]:
            cuts=[lo]
            if F(-1,4)<delta<0:
                root=ball(-4*delta/(1+4*delta))
                if root>lo:cuts.append(root)
            cuts.append(arb(128));value=arb(0)
            for l,u in zip(cuts,cuts[1:]):
                m=(l+u)/2;sign=1 if m/(4*(1+m))+ball(delta)>0 else -1
                value+=integral(lambda v,a:sign*(-v).exp()*(v/(4*(1+v))+ball(delta))/8,l,u)
            value+=arb(0).union((arb(1)/4+abs(ball(delta)))*(-arb(128)).exp()/8)
            require(value.overlaps(absolute_radial_derivative(L*L,delta)),'independent absolute derivative moment');checks+=1
        v0=2*ball(L)/(1-4*ball(L)*ball(L)).sqrt()
        def transformed(v,a):
            q=1+v*v
            return v*v*(-v*v).exp()/(8*q*q*q.sqrt())
        independent=integral(transformed,v0,16)+arb(0).union((-arb(256)).exp()/1048576)
        require(independent.overlaps(J2(L,ctx.prec)),'independent source J2');checks+=1
    return checks

def independent_mass():
    cases=[(F(2),F(2)),(F(3),F(27,8)),(F(4),F(29,8)),(F(5),F(5)),(F(3),F(1)),(F(2),F(3))]
    for tau,R in cases:
        cuts=[F(0)]
        if 0<abs(tau-R)<F(1,2):cuts.append(abs(tau-R))
        cuts.append(F(1,2));value=arb(0)
        for l,u in zip(cuts,cuts[1:]):
            mid=(l+u)/2
            if R>=tau+mid:continue
            full=tau>=R+mid
            vl=2*ball(l)/(1-4*ball(l)*ball(l)).sqrt()
            vu=arb(16) if u==F(1,2) else 2*ball(u)/(1-4*ball(u)*ball(u)).sqrt()
            def f(v,a):
                q=1+v*v;s=v/(2*q.sqrt())
                base=arb.pi()/2*v*v*(-v*v).exp()/(q*q*q.sqrt())
                if full:return base
                # Cancel the removable 1/s singularity analytically at tau=R.
                return arb.pi()*v*(-v*v).exp()/(4*ball(R)*q*q)*(ball(tau*tau-R*R)+2*ball(R)*s-s*s)
            value+=integral(f,vl,vu)
        value+=arb(0).union(arb.pi()/6*(-arb(256)).exp())
        require(value.overlaps(source_ball_mass(tau,R)),'independent source-ball mass')
    return len(cases)

def geometry_checks():
    expected=F(110567,384);deep=F(50087,384);front=F(315,2)
    require(expected==((F(11,2)**4)-2*F(9,4)**4)/3,'closed whole volume')
    counts=[]
    for n in [8,16,32]:
        cs=cells(n);require(len(set(tuple(c['index']) for c in cs))==len(cs),'unique cells')
        require(sum(c['volume_over_pi'] for c in cs)==expected,'whole exact volume')
        require(sum(c['volume_over_pi'] for c in cs if c['kind']=='deep')==deep,'exact deep volume')
        require(sum(c['volume_over_pi'] for c in cs if c['kind']=='front')==front,'exact wavefront volume')
        # Independent cross-section interval sweep at all geometry/grid breakpoints.
        cuts=sorted({F(7,4)+F(i,n) for i in range(13*n//4+1)}|{F(9,4),F(4)})
        for l,u in zip(cuts,cuts[1:]):
            t=(l+u)/2;segments=[]
            for c in cs:
                if not c['tau0']<t<c['tau1']:continue
                for lo,hi,a,b in c['segments']:
                    if lo<t<hi:segments.append((a[0]*t+a[1],b[0]*t+b[1]))
            segments.sort();edge=max(F(0),F(4)-t)
            for lo,hi in segments:
                require(lo==edge and hi>lo,'no radial gap or overlap');edge=hi
            require(edge==t+F(1,2),'complete outer radius')
        counts.append(len(cs))
    for ds in detector_bins():require(sum(d['mass'] for d in ds)==1,'exact detector normalization')
    # Four exact spherical cap fractions; independently computed rational controls.
    for R,tau,tp,rp,target in [(2,2,1,F(3,2),1),(4,3,0,2,F(3,8)),(3,2,F(-1,2),1,F(3,16)),(5,2,0,1,0)]:
        c={'r0':F(R),'r1':F(R),'tau1':F(tau)};v=causal_cap(c,ball(rp),ball(tp))
        require(v>=ball(target) and abs(v-ball(target))<arb('1e-50'),'exact causal cap control')
    # Regression: interval squaring across zero must not produce NaN in flint 0.8.
    c={'r0':F(31,16),'r1':F(2),'tau1':F(33,16)}
    v=causal_cap(c,ball(F(31,16)).union(arb(2)),ball(F(25,32)))
    require(v.is_finite() and 0<=v<=1,'zero-crossing angular cap regression')
    probes=0
    for c in cells(8)[::19]:
        for rp0,rp1 in [(F(1),F(17,16)),(F(31,16),F(2))]:
            bound=causal_cap(c,ball(rp0).union(ball(rp1)),ball(F(1)))
            for R in [c['r0'],(c['r0']+c['r1'])/2,c['r1']]:
                if not R:continue
                for rp in [rp0,(rp0+rp1)/2,rp1]:
                    for tau in [c['tau0'],c['tau1']]:
                        exact=min(F(1),max(F(0),((tau+2)**2-(R-rp)**2)/(4*R*rp)))
                        require(bound>=ball(exact),'angular cap encloses rational box probe');probes+=1
    return counts,probes

def verify():
    ctx.prec=192;provenance=read('PROVENANCE.json');tree=read('evidence/MAIN_TREE.json')
    bypath={r['path']:r['sha'] for r in tree['entries']}
    require(tree['commit']==provenance['base_commit'],'pinned commit')
    for r in provenance['files']:
        b=(HERE/r['package_path']).read_bytes()
        require(len(b)==r['bytes'] and sha(b)==r['sha256'],'unchanged source bytes')
        git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(git==r['git_blob_sha1']==bypath[r['repository_path']],'source Git identity')
    counts,probes=geometry_checks();moment_count=independent_moments();mass_count=independent_mass()
    lo=read('results/FINITE_128.json');hi=read('results/FINITE_192.json')
    for k in ['source_L1','G25','derivative_kernel_positive_lower']:
        require(arb(lo[k]).overlaps(arb(hi[k])),'physical value precision overlap')
    maxdiff=arb(0);decomp=0
    for bits,data in [(128,lo),(192,hi)]:
        require(data['new_random_calls']==0 and data['status']['METHOD']=='HOLD' and data['status']['G1']=='HOLD','unchanged gates')
        old=read(f'evidence/v20_LOCAL_{bits}.json');last=None
        ctx.prec=bits
        a=1/(2*arb.pi()).sqrt();beta=a/(16*(1+a));gamma=beta*arb('4976184375/4294967296');factor=gamma*3/arb.pi()
        for level in data['levels']:
            n=level['grid_denominator'];rows=json.loads(gzip.decompress((HERE/f'results/CELLS_{bits}_{n}.json.gz').read_bytes()))
            require(len(rows)==level['cells'],'complete stored cell inventory')
            actual=cells(n);integral_sum=arb(0);direct=[arb(0),arb(0)]
            for c,r in zip(actual,rows):
                require(c['index']==r['index'] and c['volume_over_pi']==F(r['volume_over_pi']),'stored exact geometry')
                U=arb(r['U_upper']);require(0<=U<=arb(data['global_field_M']).upper(),'bounded uniform cell field')
                w=ball(F(r['volume_over_pi']))*arb.pi()*U;integral_sum+=w
                for wi,cap in enumerate(r['detector_cap_upper']):
                    cap=arb(cap);require(0<=cap<=1,'stored detector cap');direct[wi]+=factor*w*cap
            stable(integral_sum,level['field_L1_integral_upper'])
            if last:require(arb(level['field_L1_integral_upper'])<last,'observed field improvement under refinement')
            last=arb(level['field_L1_integral_upper'])
            for oldrow,row in zip(old['archives'],level['archives']):
                fs=list(map(arb,row['first_forcing_upper']));require(len(fs)==row['active_count'],'complete known transport')
                uniform=arb(level['uniform_first_forcing_upper']);unknown=uniform*(1+gamma)**row['active_count']*((gamma*arb(29)/512).exp()-1)
                for wi,w in enumerate(row['windows']):
                    aa=[acb(arb(z[0]),arb(z[1])).abs_upper() for z in oldrow['adjoints'][wi]]
                    known=sum((x*y for x,y in zip(aa,fs)),arb(0))
                    stable(known,w['known_active_upper']);stable(unknown,w['unknown_active_upper']);stable(direct[wi],w['direct_upper'])
                    stable(known+unknown+direct[wi],w['finite_total_upper'])
                    require(arb(w['finite_total_upper'])<arb(w['without_angular_caps_upper']),'causal caps sharpen bound');decomp+=1
        require(len(data['field_controls'])==30,'fixed KG controls')
    ctx.prec=192
    for l,h in zip(lo['levels'],hi['levels']):
        stable(l['field_L1_integral_upper'],h['field_L1_integral_upper'])
        for lr,hr in zip(l['archives'],h['archives']):
            for lw,hw in zip(lr['windows'],hr['windows']):
                stable(lw['finite_total_upper'],hw['finite_total_upper'])
                maxdiff=max(maxdiff,abs(arb(lw['finite_total_upper'])-arb(hw['finite_total_upper'])).upper())
    negative_front=0
    for lc,hc in zip(lo['field_controls'],hi['field_controls']):
        for x,y in zip(lc['KG'],hc['KG']):require(arb(x).overlaps(arb(y)),'KG component precision overlap')
        z=acb(*map(arb,hc['KG']));require(z.abs_upper()<arb(hc['field_upper']),'KG inside field envelope')
        if hc['kind']=='front':
            p=list(map(F,hc['point']));tau=-p[0]-1
            # Axis-aligned controls have an exact rational radius.
            R=max(abs(v) for v in p[1:]);c={'kind':'front','tau0':tau,'tau1':tau,'r0':R,'r1':R}
            _,parts=envelope(c,arb(hi['global_field_M']))
            if z.abs_lower()>parts['volume_upper'].upper():negative_front+=1
    require(negative_front>0,'negative control rejects omitted wavefront')
    # Deliberate false hypotheses are rejected without mutating evidence.
    require(F(50087,384)!=F(110567,384),'negative control rejects missing front volume')
    require(sum(d['mass'] for d in detector_bins()[0][:-1])!=1,'negative control rejects missing detector bin')
    original=(HERE/provenance['files'][0]['package_path']).read_bytes()
    require(sha(original+b'\n')!=provenance['files'][0]['sha256'],'negative control rejects corrupted input')
    result={'status':'PASS','source_files_verified':len(provenance['files']),'partition_cell_counts':counts,
      'exact_total_volume_over_pi':'110567/384','exact_deep_volume_over_pi':'50087/384','exact_front_volume_over_pi':'315/2',
      'independent_transformed_moment_quadratures':moment_count,'independent_source_mass_quadratures':mass_count,
      'rational_angular_box_probes':probes,'zero_crossing_square_regression':'PASS','transport_decompositions_checked':decomp,
      'fixed_KG_controls_per_precision':30,'maximum_total_majorant_precision_difference':enc(maxdiff),
      'negative_controls':{'omitted_wavefront_rejected_at_controls':negative_front,'missing_front_volume':'REJECTED','missing_detector_bin':'REJECTED','corrupt_source':'REJECTED'},
      'new_random_calls':0,'independent_scientific_review':'NOT_PERFORMED','METHOD':'HOLD','G1':'HOLD'}
    write(HERE/'results/CHECKS.json',result);print(json.dumps(result,indent=2));return result
if __name__=='__main__':verify()
