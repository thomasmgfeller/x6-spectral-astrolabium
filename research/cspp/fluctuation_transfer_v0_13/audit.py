"""Independent deterministic count-sum diagnostic, never an empirical fit.

The excluded Poisson mass has a rigorous analytic bound. NumPy summation is
only a float cross-check of the primary Arb PGF certificates.
"""
import math
import numpy as np
from flint import arb
from kernel import control_atoms
from transfer import poisson_chernoff_tail,beta


def count_sum():
    atoms,_=control_atoms();means=[float(m) for mask,m in atoms];cuts=[];tails=[];probs=[]
    for mean in means:
        n=math.ceil(mean)
        while poisson_chernoff_tail(arb(mean),n)>arb('1e-25'):n+=1
        cuts.append(n);tails.append(poisson_chernoff_tail(arb(mean),n))
        pp=[math.exp(-mean)]
        for j in range(1,n+1):pp.append(pp[-1]*mean/j)
        probs.append(np.array(pp))
    indices=[np.arange(n+1) for n in cuts]
    n1,n2,n3,n4=np.ix_(*indices[1:])
    p1,p2,p3,p4=np.ix_(*probs[1:]);prob=p1*p2*p3*p4
    def w(n):
        u=1/15
        return (15/16)**n*(1-9*n*u+8*n*(n-1)*u*u-4/3*n*(n-1)*(n-2)*u**3)
    uh=means[2]/16;mh=math.exp(-uh)*(1-9*uh+8*uh*uh-4/3*uh**3)
    h1=(1+.2*(w(n2)-mh))*(1+.5j)
    h2=(1-.1*(w(n2)-mh))*(1-1j/3)
    bb=float(beta());wB=w(n1+n2+n3+n4+1);wC=w(n4)
    mu=np.zeros(2,complex);second=np.zeros((2,2),complex);relation=np.zeros((2,2),complex)
    for n0,p0 in enumerate(probs[0]):
        u1=bb*w(n0+n1+n2)*h1
        u2=bb*wB*h2+bb*wC*u1
        values=[u1,u2];p=p0*prob
        for i in range(2):
            mu[i]+=np.sum(p*values[i])
            for j in range(2):
                second[i,j]+=np.sum(p*values[i]*np.conj(values[j]))
                relation[i,j]+=np.sum(p*values[i]*values[j])
    cov=second-mu[:,None]*np.conj(mu[None,:]);rel=relation-mu[:,None]*mu[None,:]
    pair=lambda z:[float(z.real),float(z.imag)]
    return {'mean':[pair(z) for z in mu],'covariance':[[pair(z) for z in row] for row in cov],
            'relation':[[pair(z) for z in row] for row in rel],'atom_count_cutoffs':cuts,
            'count_states':math.prod(n+1 for n in cuts),'omitted_probability_upper':str(sum(tails,arb(0))),
            'omitted_mean_absolute_upper':str(32*sum(tails,arb(0))),
            'omitted_raw_second_moment_absolute_upper':str(1024*sum(tails,arb(0))),
            'status':'FLOAT_DIAGNOSTIC_ONLY; excluded mass bounded, float summation not interval-certified'}

if __name__=='__main__':
    import json
    from pathlib import Path
    from flint import ctx
    ctx.prec=192
    r=count_sum();Path(__file__).with_name('results').joinpath('COUNT_SUM_DIAGNOSTIC.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
