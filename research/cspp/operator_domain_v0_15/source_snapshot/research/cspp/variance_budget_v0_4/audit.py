"""Independent identities, direct Poisson enumeration and precision replay."""
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import poisson
from flint import arb, ctx
from variance import C,D,E,weight,palm,joint_kernel,integrated_second_moment,gaussian_tail_moments
from run import compute

HERE=Path(__file__).resolve().parent


def require(ok,message):
    if not ok: raise AssertionError(message)


def exact_controls():
    count=0
    for e in [Q(0),Q(1,16),Q(1,4),Q(1,2),Q(1)]:
        for n in range(25):
            require(weight(n+1,e)-weight(n,e)==e*weight(n,e,D),'exact add-one layer identity')
            require(weight(n+1,e,D)==(1-e)*weight(n,e,D)+e*weight(n,e,E),'exact shifted difference')
            count+=2
    points=[tuple(map(Q,p)) for p in [(-3,0,0,0),(-2,Q(3,10),0,0),
              (-2,Q(-3,10),0,0),(-1,0,0,0),(-1,Q(3,5),0,0)]]
    z=tuple(map(Q,(-Q(3,2),Q(1,5),0,0)));origin=(Q(0),)*4
    def precedes(x,y):
        dt=y[0]-x[0]
        return dt>0 and dt*dt>sum((b-a)**2 for a,b in zip(x[1:],y[1:]))
    phi=lambda x: Q(1)+x[0]/5
    def counts(y,cloud):return sum(precedes(y,v) and precedes(v,origin) for v in cloud)
    for e in [Q(1,8),Q(1,2),Q(1)]:
        def functional(cloud):return sum(phi(y)*weight(counts(y,cloud),e) for y in cloud)
        direct=functional(points+[z])-functional(points)
        analytic=phi(z)*weight(counts(z,points),e)+sum(phi(y)*e*weight(counts(y,points),e,D)
                        for y in points if precedes(y,z))
        require(direct==analytic,'pathwise add-one with shared interval updates')
        count+=1
    return count


def poisson_controls():
    errors=[];negative_controls=0;cases=0
    indices=np.arange(100)
    for ly,lv,overlap in [(2.,3.,0.),(2.,3.,1.),(2.,2.,2.),(5.,4.,3.)]:
        for eps in [.25,.5,1.]:
            for sy,sv in [(0,0),(1,0),(0,1)]:
                pa=poisson.pmf(indices,ly-overlap);pb=poisson.pmf(indices,lv-overlap)
                pc=poisson.pmf(indices,overlap)
                direct=0.
                for k,pk in enumerate(pc):
                    ay=np.array([weight(int(n+k+sy),eps) for n in indices])
                    bv=np.array([weight(int(n+k+sv),eps) for n in indices])
                    direct+=pk*np.dot(pa,ay)*np.dot(pb,bv)
                analytic=float(joint_kernel(palm(C,eps,sy),palm(C,eps,sv),
                                           eps*ly,eps*lv,eps*eps*overlap).mid())
                tail=256*sum(poisson.sf(99,m) for m in [ly-overlap,lv-overlap,overlap])
                error=abs(direct-analytic)
                require(error<=tail+2e-11,'joint kernel versus independent enumeration')
                errors.append(error);cases+=1
                if (ly,lv,overlap,eps,sy,sv)==(2.,3.,1.,.5,1,0):
                    wrong=float(joint_kernel(C,C,eps*ly,eps*lv,eps*eps*overlap).mid())
                    require(abs(wrong-direct)>1e-4,'negative control: omit Palm shift')
                    negative_controls+=1
                if (ly,lv,overlap,eps,sy,sv)==(2.,2.,2.,.5,0,0):
                    wrong=float(joint_kernel(C,C,eps*ly,eps*lv,0).mid())
                    require(abs(wrong-direct)>1e-4,'negative control: assume independence')
                    negative_controls+=1
    return {'cases':cases,'max_absolute_error':max(errors),'negative_controls':negative_controls}


def moment_controls():
    count=0;error_max=0.
    for coeff,power in [(C,0),(D,2)]:
        for eps in [0.,.125,.5,1.]:
            def h(y):
                # Positive representation, independent of signed Gamma expansion.
                t=y*y
                s=0.
                for r in range(len(coeff)):
                    pol=sum(coeff[j+r]*((1-eps)*t)**j/math.factorial(j)
                            for j in range(len(coeff)-r))
                    s+=(t*eps)**r/math.factorial(r)*pol*pol
                return y**power*math.exp(-(2-eps)*t)*s
            numerical,err=quad(h,0,15,epsabs=1e-10,epsrel=1e-11)
            analytic=float(integrated_second_moment(coeff,power,eps).mid())
            error_max=max(error_max,abs(numerical-analytic))
            require(abs(numerical-analytic)<max(2e-9,10*err),'Gamma moment versus positive-integrand quadrature')
            count+=1
    return {'cases':count,'maximum_difference':error_max,'role':'diagnostic cross-check, not certificate'}


def geometry_controls():
    count=0;maximum_error=0.
    # Original Euclidean spherical cap versus the null-coordinate expression.
    for sz,vz in [(0.01,1.9),(0.07,2.1),(.3,1.4)]:
        for sy in [sz*1.01,sz+.1,sz+.8,sz+1.3]:
            for vy in [vz*1.01,vz+.5,vz+2,vz+5]:
                if sy>=vy:continue
                rz=(vz-sz)/2;ry=(vy-sy)/2
                dt=(vy+sy-vz-sz)/2
                cosine=(ry*ry+rz*rz-dt*dt)/(2*ry*rz)
                direct=min(1,max(0,(1-cosine)/2))
                null=min(1,(sy-sz)*(vy-vz)/((vy-sy)*(vz-sz)))
                maximum_error=max(maximum_error,abs(direct-null))
                require(abs(direct-null)<2e-14,'spherical cap geometry')
                xy=sy*vy;xz=sz*vz
                lhs=(xy/vy-xz/vz)*(vy-vz)
                require(lhs<=(math.sqrt(xy)-math.sqrt(xz))**2+1e-12,'AM-GM overlap envelope')
                count+=1
    T=gaussian_tail_moments(3,8)
    analytic=sum(arb(str(c))*(T[k+2]-6*T[k+1]+9*T[k])
                 for k,c in [(0,10),(2,25),(4,12),(6,'4/3')])
    direct,error=quad(lambda x:(x-3)**2*math.exp(-x*x)*(10+25*x*x+12*x**4+4*x**6/3),
                      3,np.inf,epsabs=1e-13,epsrel=1e-12)
    require(abs(direct-float(analytic.mid()))<max(1e-12,10*error),'lower-bound tail integral')
    return {'angular_cases':count,'maximum_difference':maximum_error,
            'lower_tail_cross_check':True,'role':'diagnostic cross-check; proof in METHODS.md'}


def replay():
    low=compute(128);high=compute(192)
    for a,b in zip(low['upper_rows'],high['upper_rows']):
        require(a['ell_k']==b['ell_k'] and a['H']==b['H'],'scope unchanged')
        require(a['single_witness_RMS_at_most_10_percent']==b['single_witness_RMS_at_most_10_percent'],'RMS decisions')
        # Endpoint-derived majorants need not coincide or overlap.
        ratio=int(a['rho_sufficient'])/int(b['rho_sufficient'])
        require(abs(ratio-1)<1e-8,'density replay screen')
        require(a['witness_10_percent_RMS_excluded_by_bias']==b['witness_10_percent_RMS_excluded_by_bias'],'bias exclusions')
    require(arb(low['lower_witness']['coefficient']['ball']).overlaps(
            arb(high['lower_witness']['coefficient']['ball'])),'lower coefficient higher precision overlap')
    require(low['gate_status']==high['gate_status']=={'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'},'science gates')
    require(sum(r['single_witness_RMS_at_most_10_percent'] for r in low['upper_rows'])==1,'one witness within total allocation')
    (HERE/'results/BUDGET_192bit.json').write_text(json.dumps(high,indent=2,ensure_ascii=False)+'\n')
    return {'precisions':[128,192],'upper_budgets':7,'lower_witnesses':1,'decisions_unchanged':True}


def main():
    ctx.prec=128
    result={'status':'PASS','exact_identities':exact_controls(),
            'poisson_kernel':poisson_controls(),'gamma_moments':moment_controls(),
            'geometry':geometry_controls(),
            'replay':replay(),'external_independent_review':False,
            'scope':'implementation controls and deterministic replay; not E4 confirmation'}
    (HERE/'results/AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
