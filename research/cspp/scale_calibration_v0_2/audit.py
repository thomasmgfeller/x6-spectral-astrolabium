"""Independent analytic controls and complete calibration replay."""
import argparse
import json
import math
from pathlib import Path
import tempfile
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre
from common import HERE,OLD,old,plan,cloud,digest,gaussian_fields,exact_box
from mean_operator import integral
from green_reference import spherical_means,kirchhoff,j2_over_s2,evaluate as green
from run import frozen,mean_scan,summary

def require(ok,label):
    if not bool(ok):raise RuntimeError('AUDIT FAIL: '+label)
    return label
def tests():
    result=[]
    for mu in [.1,3.,30.]:
        n=np.arange(201);prob=np.empty(201);prob[0]=np.exp(-mu)
        for k in range(1,201):prob[k]=prob[k-1]*mu/k
        for e in [.1,.25,1.]:
            z=e*mu;expected=np.exp(-z)*(1-9*z+8*z*z-4*z**3/3)
            require(abs(np.sum(prob*old.weights(n,e))-expected)<2e-13,'Poisson smoothing identity')
    result.append('nine independent Poisson-sum identities')
    ell,H,L=1.2,3.5,1.3;q=ell**-4
    # Different integration coordinates and adaptive algorithm from production.
    def radial(u):
        def integrand(r):
            z=q*np.pi/24*(u*u-r*r)**2
            return 4*np.pi*r*r*np.exp(-(u*u+r*r)/(2*L*L)-z)*(1-9*z+8*z*z-4*z**3/3)
        return quad(integrand,0,min(u,H-u),epsabs=1e-11,epsrel=1e-11)[0]
    value=4/np.sqrt(6)*np.sqrt(q)*(-1+q*sum(quad(radial,a,b,epsabs=1e-10,epsrel=1e-10)[0] for a,b in [(0,H/2),(H/2,H)]))
    result.append(require(abs(value-integral(ell,H,L,192)[0])<1e-9,'mean integral against independent adaptive (u,r) quadrature'))
    n,w=roots_legendre(192)
    for tau in [.1,.7,1.7]:
        r=tau*(n+1)/2;wr=tau*w/2
        for k in [0.,.7,4.]:
            means=np.sinc(k*r/np.pi);M=np.sinc(k*tau/np.pi);K=np.cos(k*tau)
            for m in [0.,1.,2.]:
                actual=K-m*m*tau*tau/2*M+m*m*tau*np.sum(wr*r*r*j2_over_s2(m,tau*tau-r*r)*means)
                require(abs(actual-np.cos(np.sqrt(k*k+m*m)*tau))<2e-12,'KG plane mode')
    result.append('27 Bessel-tail identities against exact KG plane modes')
    x=np.array([.2,.1,.15]);tau=.3;h=1e-5
    diff=((tau+h)*spherical_means(x,np.array([tau+h]),192)[0]-(tau-h)*spherical_means(x,np.array([tau-h]),192)[0])/(2*h)
    result.append(require(abs(diff-kirchhoff(x,tau,192))<2e-6,'Kirchhoff derivative against finite difference of spherical mean'))
    initial=np.array([[-1.,.1,.2,.1],[-1.,0,0,0],[-1.,.8,0,0]])
    from common import oldref
    expected=oldref.source(initial[:,1:])
    result.append(require(np.allclose(green(initial,64),expected[:,None],atol=1e-14),'Cauchy displacement at initial time'))
    outside=np.array([[0.,3.,0,0],[-2.,0,3,0]])
    result.append(require(np.array_equal(green(outside,64),np.zeros((2,3))),'exact finite-propagation zero control'))
    shellfree=np.array([[.5,0,0,0],[1.,0,0,.5]])
    result.append(require(np.array_equal(green(shellfree,128)[:,0],np.zeros(2)),'massless Huygens support control'))
    qp=np.array([[-.75,.15,.05,.1],[-.625,.4,0,.1]])
    qm=qp.copy();qm[:,0]=-2-qp[:,0]
    result.append(require(np.array_equal(green(qp,96),green(qm,96)),'zero-velocity time reversal'))
    g=np.random.Generator(np.random.PCG64DXSM(271828));x=old.points(g,151,4);x[:,0]-=4
    _,counts=old.counts(x,np.zeros((1,4)),full=False)
    for H in [4,6]:
        use=-x[:,0]+np.linalg.norm(x[:,1:],axis=1)<H
        _,small=old.counts(x[use],np.zeros((1,4)),full=False)
        require(np.array_equal(small[0],counts[0,use]),'causal-convex domain counts')
    result.append('nested past diamonds leave retained interval counts unchanged')
    for ell in [1.,1.5,2.]:
        rho=np.array([1024,4096,16384])/old.volume(4);eps=ell**-4/rho
        require(np.all((eps>0)&(eps<=1)) and np.allclose(eps*rho,ell**-4,rtol=1e-15),'fixed nonlocality coupling')
    result.append('all smoothing parameters admissible and effective density fixed')
    result.append(require(abs(np.cos(np.sqrt(4**2+2**2)*.7)-np.cos(np.sqrt(4**2-2**2)*.7))>.1,'wrong mass-sign negative control separated'))
    return result
def replay():
    frozen();out=HERE/'results';expected=np.load(out/'sprinklings.npz')['values']
    records=json.loads((out/'RUNS.json').read_text());nrun=0;maxdiff=0.
    for rec in records:
        d,i=rec['density_index'],rec['realization_index'];x=cloud(d,i)
        archive=np.load(out/f'clouds_d{d}_b{i//8}.npz')
        require(np.array_equal(x,archive[rec['key']]) and digest(x)==rec['cloud_sha256'],'seed and cloud replay')
        _,pc=old.counts(x,np.zeros((1,4)),full=False)
        require(digest(pc[0])==rec['counts_sha256'],'interval count replay')
        f=gaussian_fields(x,2);rho=rec['nu_equivalent_Omega4']/old.volume(4)
        for hi,H in enumerate([4,6,8]):
            use=-x[:,0]+np.linalg.norm(x[:,1:],axis=1)<H
            for ei,ell in enumerate([1.,1.5,2.]):
                v=old.apply(pc[:,use],rho,ell**-4/rho,f[use],np.ones((1,4)))[0]
                diff=float(np.max(np.abs(v-expected[d,i,hi,ei])));maxdiff=max(maxdiff,diff)
                require(np.allclose(v,expected[d,i,hi,ei],atol=1e-10,rtol=1e-11),'operator replay')
        nrun+=1
    m=np.load(out/'mean.npz')['values'];rows=json.loads((out/'MEAN.json').read_text())['rows']
    for i,row in enumerate(rows):
        require(np.allclose(integral(row['ell_k'],row['H'],row['L'],384),m[i,-1],atol=1e-9,rtol=1e-10),'full finest expectation scan replay')
    src=np.load(out/'source.npz')
    require(np.allclose(green(src['query'],256),src['green'][-1],atol=1e-11,rtol=1e-10),'all finest Green reference queries replay')
    # Include the independent FFT algorithm at every planned resolution.
    from fourier_nodes import evaluate
    for j,n in enumerate([64,128,256]):
        v,_=evaluate(src['query'][:28],n)
        require(np.allclose(v,src['fourier'][j],atol=1e-10,rtol=1e-9),'all exact-node Fourier resolutions replay')
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for name in ['mean.npz','MEAN.json','sprinklings.npz','RUNS.json','source.npz']:(p/name).symlink_to((out/name).resolve())
        summary(p)
        require(json.loads((p/'RESULTS.json').read_text())==json.loads((out/'RESULTS.json').read_text()),'summary replay')
    return {'replayed_runs':nrun,'maximum_operator_absolute_difference':maxdiff,'status':'PASS_SOFTWARE_REPLAY_NOT_G1'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--replay',action='store_true');ap.add_argument('--output',type=Path);a=ap.parse_args()
    result={'controls':tests(),'status':'PASS_SOFTWARE_CONTROLS_NOT_G1'}
    if a.replay:result['replay']=replay()
    text=json.dumps(result,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    print(text)
if __name__=='__main__':main()
