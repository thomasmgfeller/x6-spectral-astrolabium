"""JCGM 100 clause 8 / JCGM 102: joint propagation with exact ratio moments."""
import numpy as np
from scipy.stats import beta,binom


def cp(k,n,alpha=.01):
    return [float(beta.ppf(alpha/2,k,n-k+1)) if k else 0.,float(beta.ppf(1-alpha/2,k+1,n-k)) if k<n else 1.]


def evaluate(blocks,contract,seed):
    n,d=blocks.shape;mu=blocks.mean(axis=0)
    UA=np.cov(blocks,rowvar=False,ddof=1)/n
    nu=n-d;scale=(n-1)/nu*UA;UT=(n-1)/(nu-2)*UA
    common=contract['gum_common_bias_halfwidth'];local=contract['gum_local_bias_halfwidth'];h=contract['gum_gain_halfwidth']
    U=np.zeros((2*d+2,2*d+2));U[:d,:d]=UT
    U[d,d]=common**2/3;U[d+1:2*d+1,d+1:2*d+1]=np.eye(d)*local**2/3;U[-1,-1]=h*h/3
    J=np.zeros((d,2*d+2));J[:,:d]=np.eye(d);J[:,d]=-1;J[:,d+1:2*d+1]=-np.eye(d);J[:,-1]=-mu
    first=J@U@J.T
    # Exactly propagated first two moments for independent rectangular K and Z.
    a=(np.log1p(h)-np.log1p(-h))/(2*h);b=1/(1-h*h)
    VZ=UT+common**2/3*np.ones((d,d))+local**2/3*np.eye(d)
    mean=a*mu;cov=b*VZ+(b-a*a)*np.outer(mu,mu)
    rng=np.random.default_rng(seed);L=np.linalg.cholesky(scale);inv=np.linalg.inv(cov)
    def draw(size):
        z=rng.standard_normal((size,d))@L.T
        z/=np.sqrt(rng.chisquare(nu,size)/nu)[:,None]
        z+=mu
        z-=rng.uniform(-common,common,(size,1))
        z-=rng.uniform(-local,local,(size,d))
        z/=rng.uniform(1-h,1+h,(size,1))
        return z
    def radius(y):
        z=y-mean;return np.einsum('ij,jk,ik->i',z,inv,z)
    M=contract['gum_radius_draws'];p=contract['gum_joint_coverage']
    y=draw(M);r=np.sort(radius(y));idx=int(np.ceil(p*M))-1;cut=float(r[idx])
    lo=max(0,int(binom.ppf(.005,M,p))-1);hi=min(M-1,int(binom.ppf(.995,M,p)))
    N=contract['gum_validation_draws'];hits=int(np.sum(radius(draw(N))<=cut))
    result=dict(n=n,dimension=d,input_order=['D0','D1','D2','D3','c_common','c0','c1','c2','c3','K'],
        input_estimate=np.r_[mu,np.zeros(5),1].tolist(),input_covariance=U.tolist(),jacobian=J.tolist(),
        mean_D=mu.tolist(),type_A_covariance_of_mean=UA.tolist(),t_df=nu,t_covariance=UT.tolist(),
        first_order_estimate=mu.tolist(),first_order_covariance=first.tolist(),
        exact_pdf_mean=mean.tolist(),exact_pdf_covariance=cov.tolist(),standard_uncertainty=np.sqrt(np.diag(cov)).tolist(),
        exact_inverse_gain_moments=[a,b],max_relative_standard_uncertainty_change=float(np.max(np.abs(np.sqrt(np.diag(cov)/np.diag(first))-1))),
        monte_carlo_mean_check=y.mean(axis=0).tolist(),monte_carlo_mean_standard_error=np.sqrt(np.diag(cov)/M).tolist(),
        monte_carlo_covariance_check=np.cov(y,rowvar=False).tolist(),
        joint_ellipsoid=dict(coverage_target=p,radius_squared=cut,quantile_99pct_MC_interval=[float(r[lo]),float(r[hi])],radius_draws=M,
            validation_draws=N,validation_hits=hits,validation_probability_99pct_interval=cp(hits,N),center='exact_pdf_mean',covariance='exact_pdf_covariance'),
        scope='Coverage under assigned joint input PDF; not physical coverage; fixed MC budget, not adaptive JCGM102 7.8')
    return result
