"""Retarded common-noise transfer and rigorous remainder bounds."""
from fractions import Fraction as F
from flint import arb,acb,ctx
from kernel import JointWeights,control_atoms,weight,require
from algebra import Poly,covariance,causal_orders,solve_polynomial


def beta():
    rho=3/arb.pi();a=4*(rho/96).sqrt()
    return a/(16*(a+1))

def skeleton(law,kappa=F(1,5)):
    w=[Poly.variable(i) for i in range(4)]
    mh=law.moment((0,0,0,1));k=arb(kappa.numerator)/kappa.denominator
    h1=(1+k*(w[3]-mh))*acb(1,arb(1)/2)
    h2=(1-k/2*(w[3]-mh))*acb(1,-arb(1)/3)
    K=[[Poly() for _ in range(4)] for _ in range(4)]
    K[2][0]=w[0]*beta();K[3][1]=w[1]*beta();K[3][2]=w[2]*beta()
    b=[h1,h2,Poly(),Poly()]
    return K,b


def remainder_bounds(linear,remainder,law):
    # sigma_R <= ||R||_2; use the latter to also control the mean shift.
    delta=[((p*p.conj()).mean(law).real.upper()).sqrt() for p in remainder]
    _,C,_=covariance(linear,law)
    s=[C[i][i].real.upper().sqrt() for i in range(len(linear))]
    bounds=[[s[i]*delta[j]+s[j]*delta[i]+delta[i]*delta[j] for j in range(len(s))] for i in range(len(s))]
    return delta,bounds


def predict_skeleton(law=None):
    atoms,geom=control_atoms();law=law or JointWeights(atoms)
    K,b=skeleton(law);full=solve_polynomial(K,b)[2:]
    orders=[row[2:] for row in causal_orders(K,b,law)]
    for i,p in enumerate(full):
        diff=p-sum((order[i] for order in orders),Poly())
        require(all(z.contains(0) for z in diff.terms.values()),'exact nilpotent polynomial transfer')
    mu,C,P=covariance(full,law)
    base=[p.mean(law) for p in orders[0]]
    lin=[orders[0][i]+orders[1][i] for i in range(2)]
    rem=[sum((order[i] for order in orders[2:]),Poly()) for i in range(2)]
    ml,Cl,Pl=covariance(lin,law);delta,cb=remainder_bounds(lin,rem,law)
    for i in range(2):
        require((mu[i]-base[i]).abs_upper()<=delta[i],'mean remainder bound')
        for j in range(2):
            require((C[i][j]-Cl[i][j]).abs_upper()<=cb[i][j],'covariance remainder bound')
            require((P[i][j]-Pl[i][j]).abs_upper()<=cb[i][j],'relation remainder bound')
    for i in range(2):
        require(C[i][i].real>0 and C[i][i].imag.contains(0),'positive real variance')
        for j in range(2):
            require((C[i][j]-C[j][i].conjugate()).contains(0),'Hermitian covariance')
            require((P[i][j]-P[j][i]).contains(0),'symmetric relation')
    determinant=C[0][0]*C[1][1]-C[0][1]*C[1][0]
    require(determinant.real>0 and determinant.imag.contains(0),'positive 2x2 covariance determinant')
    # Counterfactuals preserve the marginals where their label says so.
    means=[sum(mean for mask,mean in atoms if i in mask) for i in range(4)]
    independent=JointWeights([({i},m) for i,m in enumerate(means)])
    no_palm=JointWeights(atoms,shifts=(0,0,0,0))
    counter={}
    for name,l in [('independent_intervals',independent),('omit_Palm_insertion',no_palm)]:
        kk,bb=skeleton(l);pp=solve_polynomial(kk,bb)[2:];mm,cc,pr=covariance(pp,l)
        counter[name]={'mean':mm,'covariance':cc,'relation':pr}
    K0=[[Poly.const(k.mean(law)) for k in row] for row in K]
    for name,kk,bb in [('frozen_operator',K0,b),('frozen_history',K,[Poly.const(x.mean(law)) for x in b])]:
        mm,cc,pr=covariance(solve_polynomial(kk,bb)[2:],law)
        counter[name]={'mean':mm,'covariance':cc,'relation':pr}
    centered=[Poly.variable(i)-law.moment(tuple(1 if j==i else 0 for j in range(4))) for i in range(4)]
    third=(centered[0]*centered[1]*centered[3]).mean(law)
    require(not third.contains(0),'nonzero third joint moment rules out Gaussian moment closure')
    return {'geometry':geom,'atom_means':[{'intervals':sorted(mask),'mean':str(m)} for mask,m in atoms],
            'beta':beta(),'mean':mu,'covariance':C,'relation':P,'covariance_determinant':determinant,
            'frozen_mean':base,'mean_shift':[x-y for x,y in zip(mu,base)],
            'order_means':[[p.mean(law) for p in row] for row in orders],
            'linear_covariance':Cl,'linear_relation':Pl,'linear_remainder_L2_upper':delta,
            'linear_covariance_error_upper':cb,'third_joint_centered_moment_ABH':third,
            'counterfactuals':counter,'distinct_exact_weight_moments':len(law.cache)}


def poisson_chernoff_tail(mean,cutoff):
    n=arb(cutoff+1);mean=arb(mean)
    require(n>mean and mean>0,'upper-tail Chernoff regime')
    return (-mean+n*(1+(mean/n).log())).exp()


def original_local_history_envelopes(path_order=128,count_cutoff=1024):
    # Original eps=1/16. A global B=2 is checked, not assumed from samples.
    eps=F(1,16);r=arb(15)/16;u=arb(1)/15;N=128
    finite=max(weight(n,eps).abs_upper() for n in range(N))
    require(N*(-r.log())>3,'every n^j r^n decreases beyond N, j<=3')
    tail=r**N*(1+9*N*u+8*N*N*u*u+arb(4)/3*N**3*u**3)
    B=arb(2);require(finite<B and tail<B,'global layer weight bound')
    b=beta()*B;lam=arb(512)
    # For alpha>1: sum_{j>R} b^j choose(N,j) <= alpha^(-R-1)(1+alpha b)^N.
    alpha=(((1+4*arb(path_order+1)/lam).sqrt()-1)/2)/b
    require(alpha>1,'path-tail tilt')
    path_L2=alpha**(-path_order-1)*(lam*((1+alpha*b)**2-1)/2).exp()
    t=1+b;tilted=lam*t*t
    count_L2=( (lam*(t*t-1)).exp()*poisson_chernoff_tail(tilted,count_cutoff)).sqrt()
    full_L2=(lam*(t*t-1)/2).exp()
    return {'weight_global_upper':B,'finite_weight_max_upper':finite,'analytic_weight_tail_upper':tail,
            'path_order':path_order,'path_tail_tilt':alpha,'path_tail_L2_upper':path_L2,
            'poisson_count_cutoff':count_cutoff,'count_tail_L2_upper':count_L2,'full_response_L2_upper':full_L2,
            'scope':'original normalized compact local H1 source, original nu=512 eps=1/16 m=1, both full windows; conservative majorants only, not evaluated ensemble means/covariances'}


def original_source_predictions():
    # Exact geometric Poisson prediction, not fitted to the eight archive clouds.
    # Omega4 with r<1/2 and t<=-1 has volume 7*pi/16; rho=3/pi.
    p0=(-arb(21)/16).exp()
    # Histories failing even to have four sites occur with positive probability.
    history_lambda=arb(81)
    degenerate=(-history_lambda).exp()*sum(history_lambda**j/arb(j).fac() for j in range(4))
    from pathlib import Path
    import gzip,json
    refpath=Path(__file__).resolve().parent.parent/'full_continuum_v0_12/results/BENCHMARK_192.json.gz'
    doc=json.load(gzip.open(refpath,'rt'));Cref=[acb(arb(w['normalized_value'][0]),arb(w['normalized_value'][1])) for w in doc['reference']['windows']]
    mse_floor=[[p0*x*y.conjugate() for y in Cref] for x in Cref]
    return {'source_history_poisson_mean':arb(21)/16,'zero_response_probability_lower':p0,
            'reference_mean_square_error_PSD_lower_matrix':mse_floor,
            'RMS_error_lower':[p0.sqrt()*z.abs_lower() for z in Cref],
            'covariance_vs_mean_PSD_factor':p0/(1-p0),
            'conditional_mean_accuracy_budget':arb('1/1000'),
            'SD_lower_if_mean_within_budget':[(p0/(1-p0)).sqrt()*max(arb(0),z.abs_lower()-arb('1/1000')) for z in Cref],
            'nonlocal_adapter_fewer_than_four_history_points_probability':degenerate,
            'scope':'unconditional original Poisson ensemble, unchanged normalized compact source, local H1 and both complete detector windows; PSD inequality is E[(A-Cref)(A-Cref)*]>=p0 Cref Cref*, and Cov(A)>=p0/(1-p0) mean(A)mean(A)*; no numerical mean or covariance equality asserted'}
