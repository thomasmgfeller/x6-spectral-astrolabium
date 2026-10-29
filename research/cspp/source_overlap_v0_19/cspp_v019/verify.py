"""Independent norm identities, certified quadrature and Poisson controls."""
import json
import hashlib
import math
from fractions import Fraction as F
from pathlib import Path
from flint import arb, acb, ctx
import source_norms as sn
import kernel
from run import enc

HERE=Path(__file__).resolve().parent


def check(ok,label):
    if not ok:raise AssertionError(label)


def quadrature_norm1():
    def f(t,analytic):
        h_inv=1+t*t
        real=17-8*h_inv**2+48*h_inv**3-16*h_inv**4
        angular=real*real+acb(1024)/3*t*t*h_inv**3
        return acb.pi()/2*t*t*(-2*t*t).exp()*angular/h_inv.sqrt(analytic=analytic)**5
    parts=[acb.integral(f,k,k+1,rel_tol=arb(2)**-100,abs_tol=arb(2)**-100) for k in range(16)]
    val=sum(parts,acb(0))
    tail=arb.pi()/2*8263*256*(arb(512).gamma_upper(arb(19)/2))/(2*arb(2)**(arb(19)/2))
    check(val.imag.contains(0),'quadrature imaginary part encloses zero')
    return val.real+arb(tail/2,tail/2),tail


def main():
    ctx.prec=512
    low=json.loads((HERE/'results/BOUNDS_384.json').read_text())
    high=json.loads((HERE/'results/BOUNDS_512.json').read_text())
    checks=[]
    count=0
    def compare(x,y,path='root'):
        nonlocal count
        if isinstance(x,dict):
            check(x.keys()==y.keys(),path+' keys')
            for k in x:
                if k!='bits':compare(x[k],y[k],path+'/'+k)
        elif isinstance(x,list):
            check(len(x)==len(y),path+' length')
            for i,(a,b) in enumerate(zip(x,y)):compare(a,b,path+f'/{i}')
        elif isinstance(x,str) and '+/-' in x:
            check(arb(x).overlaps(arb(y)),path+' overlap');count+=1
        else:check(x==y,path+' exact')
    compare(low,high)
    polys=sn.polynomials(68)
    norms=[]
    for J in range(35):
        value=sn.norm_squared_by_parts(polys[2*J],512)
        target=arb(high['norm_squared'][str(J)])
        check(value.overlaps(target),f'independent integration by parts J={J}')
        check(value>0,f'positive norm J={J}')
        norms.append({'J':J,'by_parts':enc(value)})
    checks.append('35 squared-polynomial norms agree with integration-by-parts values')
    quad,tail=quadrature_norm1()
    check(quad.overlaps(arb(high['norm_squared']['1'])),'independent analytic quadrature for Hf')
    checks.append('Hf norm agrees with certified direct quadrature plus analytic infinite tail')
    expected={(0,0):17,(2,0):-8,(3,0):48,(4,0):-16,(2,1):64}
    check(polys[1]==expected,'first derivative polynomial from radial Laplacian')
    check(all(isinstance(c,int) for p in polys for c in p.values()),'all derivative coefficients are exact integers')
    checks.append('independent first-order derivative formula and exact integer coefficients')
    positive,signcert=kernel.positive_indices()
    for n in range(129):
        check(kernel.weight(n)==F(15,16)**n*kernel.polynomial(n),'weight polynomial identity')
        check(abs(kernel.weight(n))<=F(4976184375,4294967296),'finite sharp weight bound')
    envelope=F(15,16)**128*(1+F(9*128,15)+F(8*128**2,225)+F(4*128**3,10125))
    check(envelope<F(4976184375,4294967296) and F(15,16)*F(129,128)**3<1,'infinite sharp weight bound')
    check(all(x<0 for x in signcert),'infinite negative-sign region n>=128')
    proto=json.loads((HERE/'PROTOCOL.json').read_text())
    kernel_rows=[]
    for n0 in proto['kernel_n0_values']:
        for mus in proto['kernel_poisson_means']:
            mu=arb(mus)
            exact=kernel.absolute_expectation(n0,mu)
            direct=kernel.direct_sum(n0,mu,proto['kernel_validation_cutoff'])
            check(exact.overlaps(direct),f'Poisson direct sum {n0} {mus}')
            check(exact>=0 and exact<=arb('4976184375/4294967296'),f'bounded conditional kernel {n0} {mus}')
            kernel_rows.append({'n0':n0,'mu':mus,'exact_abs_expectation':enc(exact),'truncated_sum_plus_tail':enc(direct)})
    checks.append('49 exact conditional kernel expectations agree with direct sums and certified tails')
    # y=(-6,0), b=(-5,0), p=(1,0,0,3/2): y precedes b, hence overlap=I(b,p).
    v_full_over_pi=(F(7)**2-F(3,2)**2)**2/24
    overlap_over_pi=(F(6)**2-F(3,2)**2)**2/24
    mu_out=3*(v_full_over_pi-overlap_over_pi)
    check(mu_out==F(2093,16),'exact nested Alexandrov overlap')
    # Lorentz squared interval is nondecreasing from b along a future causal curve.
    caps=[((F(5)+t)**2-1)**2/128 for t in [F(1),F(5,4)]]
    check(caps==[F(1225,128),F(370881,32768)],'two geometric caps')
    checks.append('exact overlap control and both detector-past caps')
    # Negative controls: drop conjugation, use signed kernel as absolute, mistake mean for pathwise.
    check(arb(high['norm_squared']['1'])>sn.norm_squared_by_parts(polys[1],512),'negative: one H is not H squared')
    check(kernel.signed_expectation(8,arb(0))<0 and kernel.absolute_expectation(8,arb(0))>0,'negative: absolute expectation is not signed expectation')
    check(F(1,2)*(1*1+3*3)!=F(1,2)*(1+3)*F(1,2)*(1+3),'negative: dependent products do not factor')
    for w in high['windows']:
        for r in w['archives']:
            bound=arb(r['full_remainder_L1_bound'])
            check(bound>arb(1)/1000,'no inferred numerical accuracy release')
            check(bound<arb(r['improved_v18_split_bound']),'integrated envelope improves volume split')
    check(high['status']==proto['status'] and high['new_random_calls']==0,'unchanged HOLD and no random data')
    for row in json.loads((HERE/'PROVENANCE.json').read_text())['files']:
        data=(HERE/row['path']).read_bytes()
        check(hashlib.sha256(data).hexdigest()==row['sha256'],'evidence SHA256 '+row['path'])
        check(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha'],'pinned Git identity '+row['path'])
    out={'status':'PASS','precision_overlap_count':count,'source_identity_checks':35,'certified_quadrature_checks':1,
         'exact_weight_identities':129,'conditional_kernel_checks':len(kernel_rows),'negative_controls':3,'checks':checks,
         'norms_by_parts':norms,'norm1_direct_quadrature':enc(quad),'norm1_quadrature_tail_bound':enc(tail),
         'positive_weight_indices':positive,'negative_tail_polynomial_coefficients':[str(x) for x in signcert],
         'kernel_rows':kernel_rows,'geometric_control':{'full_volume_over_pi':str(v_full_over_pi),'overlap_volume_over_pi':str(overlap_over_pi),'outside_poisson_mean':str(mu_out),'scope':'deterministic identity; not archive data'},
         'scope':'numerical and algebraic controls; no independent mathematical peer review or statistical validation'}
    (HERE/'results/CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','precision_overlap_count','source_identity_checks','certified_quadrature_checks','conditional_kernel_checks','negative_controls']},indent=2),flush=True)


if __name__=='__main__':main()
