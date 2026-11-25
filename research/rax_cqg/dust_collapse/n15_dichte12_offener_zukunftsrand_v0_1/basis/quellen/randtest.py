"""Positive pullback at the ordinary cut after 13; includes the complete early P/rest test."""
from itertools import product
from pathlib import Path
import json
import math
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from ordnung import ORDER, pairs_from_intervals

D=3.75*(3/722)**.25
K=3.75
s=1/(72*D*K*K)
H=1/16384
WINDOW=1/64
EDGES=pairs_from_intervals()


def nodes(method,n):
    if method=='gauss':
        q,w=leggauss(n)
        return q,w/2
    theta=np.linspace(math.pi,0,n)
    k=np.arange(n)
    moments=np.zeros(n)
    moments[::2]=1/(1-k[::2]**2)
    return np.cos(theta),np.linalg.solve(np.cos(k[:,None]*theta),moments)


def a_segments(tag):
    low,high=tag-H,tag+H
    left,right=5/8-WINDOW,5/8+WINDOW
    cuts={left,right}
    for bound,scale in product((low,high),(.99,1.01)):
        k=3/8+2*bound/scale
        if left<k<right:
            cuts.add(k)
    edges=sorted(cuts)
    result=[]
    for a,b in zip(edges,edges[1:]):
        f=((a+b)/2-3/8)/2
        if min(high,1.01*f)>max(low,.99*f):
            result.append((a,b))
    return result


def endpoint_grid(method,n,tag):
    q,w=nodes(method,n)
    # Marginal measure in x13 from the allowed cell f13=(u14-u12)/2.
    # The u14 integral only supplies the range/Jacobian, with no action past 13.
    for low,high in a_segments(tag):
        grids=np.meshgrid(q,q,q,q,q,indexing='ij')
        v,a,b,jitter,c=[g.ravel() for g in grids]
        v_node=v
        a=(low+high)/2+(high-low)/2*a
        b=.75+WINDOW*b
        c=.875+WINDOW*c
        f13=(c-a)/2
        x13=f13*(1+jitter/100)
        weight=w
        for _ in range(4):
            weight=np.multiply.outer(weight,w)
        weight=weight.ravel()*(high-low)/(2*WINDOW)*f13
        half=np.maximum(0,(np.minimum(tag+H,1.01*(a-.375)/2)-np.maximum(tag-H,.99*(a-.375)/2))/2)
        mid=(np.minimum(tag+H,1.01*(a-.375)/2)+np.maximum(tag-H,.99*(a-.375)/2))/2
        for side in (-1,1):
            v=.5+WINDOW*(v_node+side)/2
            yield side,np.column_stack((v,a,b,x13,mid,half)),weight/2


def waves(method,g,z,u,pulse,components=False):
    v,a,b,x13,mid,half=(g[:,i,None,None] for i in range(6))
    y={j:float(j-5) for j in range(4)}
    y[3]+=.25
    y.update({j:y[3]+K*k for j,k in ((4,z),(5,u),(6,.375),(11,v),(12,a),(13,b))})
    selected=(4,5,6,11,12,13)
    if method=='gauss':
        coeff={}
        for j in selected:
            rank=ORDER.index(j)
            raw=-.5
            for lag,weight in enumerate((1,-9,16,-8),1):
                if rank<lag:
                    break
                i=ORDER[rank-lag]
                shift=pulse/(8*np.sqrt(D)) if i==6 and j in (12,13) else 0.
                raw=raw-(weight/38)*(y[j]-y[i]-shift)**2
            coeff[j]=raw
        f={4:(z+u)/2,5:(.375-z)/2,6:(v-u)/2,12:(b-v)/2}
        def average(centre,hw,c):
            return np.exp(1j*D*centre*c)*np.sinc(D*hw*c/np.pi)
    else:
        coeff={j:-.5 for j in selected}
        for (i,j),weight in EDGES.items():
            if j in coeff:
                coeff[j]=coeff[j]-weight*(y[j]-y[i])**2/38
        shift=pulse/(8*np.sqrt(D))
        for j in (12,13):
            coeff[j]=coeff[j]+EDGES[6,j]*(2*(y[j]-y[6])*shift-shift**2)/38
        faces=[0,(z+u)/2,(u+.375)/2,(.375+v)/2,(v+a)/2,(a+b)/2]
        f={j:faces[k+1]-faces[k] for k,j in ((0,4),(1,5),(2,6),(4,12))}
        # Independent approximation to the symmetric characteristic function.
        # All density arguments are small. Compare against sin(x)/x in the first implementation.
        def average(centre,hw,c):
            t2=(D*hw*c)**2
            cf=1-t2*(1/6-t2*(1/120-t2/5040))
            return np.exp(1j*D*centre*c)*cf
    L=(half/H)*average(mid,half,coeff[11])
    for j in (4,5,6):
        L=L*f[j]*average(f[j],f[j]/100,coeff[j])
    if components:
        return L,f[12],coeff[12],x13,coeff[13]
    R=f[12]*average(f[12],f[12]/100,coeff[12])*np.exp(1j*D*x13*coeff[13])
    return L,R


def amplitudes(method,n,g,pulse):
    q,w=nodes(method,n)
    z=.125+WINDOW*q[None,:,None]
    fields=[waves(method,g,z,.25+arm*s+H*q[None,None,:],pulse) for arm in (-1,1)]
    right_average=(fields[0][1]@w+fields[1][1]@w)/2
    plain=[]
    recorded=[]
    residual=[]
    for idx,(left,right) in enumerate(fields):
        plain.append(((left*right)@w)@w)
        mean_left=left@w
        recorded.append((mean_left*right_average)@w)
        # Independently propagate both outgoing components of (I-P).
        other=fields[1-idx][1]
        vector=(left-mean_left[:,:,None]/2)*right-mean_left[:,:,None]*other/2
        residual.append((vector@w)@w)
    direct,bright,dark=[np.column_stack(col) for col in (plain,recorded,residual)]
    np.testing.assert_allclose(direct,bright+dark,atol=2e-18,rtol=2e-13)
    return direct,bright,dark


def gram(rows):
    return rows.conj().T@rows


def metric(method,n,tag,pulse=0):
    complete=[[],[],[]]
    sides=[]
    for side,g,w in endpoint_grid(method,n,tag):
        for chunk in range(0,len(w),192):
            idx=slice(chunk,chunk+192)
            sides.append(np.full(len(w[idx]),side))
            for result,rows in zip(complete,amplitudes(method,n,g[idx],pulse)):
                result.append(np.sqrt(w[idx,None])*rows)
    direct,bright,dark=(np.concatenate(values) for values in complete)
    g=gram(direct)
    lengths=np.sqrt(g.diagonal().real)
    normalized=direct/lengths
    overlap=np.vdot(normalized[:,0],normalized[:,1])
    residual=normalized[:,1]-overlap*normalized[:,0]
    variance=np.vdot(residual,residual).real  # 1-r^2 without cancellation
    corr=np.abs(overlap)
    kappa=(1+corr)**2/variance
    # A transparent candidate that orthogonalizes the columns: choose eigendirections
    # of their Gram matrix in output space, inversely weight squared singular values.
    left,singular,right=np.linalg.svd(normalized,full_matrices=False)
    np.testing.assert_allclose((singular[0]/singular[1])**2,kappa,rtol=8e-9)
    back=(left.conj().T@normalized)/singular[:,None]
    np.testing.assert_allclose(gram(back),np.eye(2),atol=3e-10,rtol=0)
    phases=np.array([1,1j,-1,-1j])
    # Initial flat packets have equal weight under the incoming clock L2 convention.
    inputs=np.array([np.ones(4),phases])/np.sqrt(2)
    def weights(modes):
        return np.sum(abs(modes@inputs)**2,axis=0)
    original=weights(direct)
    pp=weights(bright)
    rr=weights(dark)
    base_scale=g.trace().real/2
    left=direct[np.concatenate(sides)==-1]
    upper=direct[np.concatenate(sides)==1]
    np.testing.assert_allclose(gram(left)+gram(upper),g,atol=1e-21,rtol=5e-13)
    native_low=weights(left)/original
    np.testing.assert_allclose((weights(left)+weights(upper))/original,np.ones(4),atol=3e-13)
    return dict(native_lower_u11_probabilities=native_low.tolist(),
                raw_column_norm_squares=g.diagonal().real.tolist(),
                normalized_overlap_real_imag=[overlap.real,overlap.imag],
                one_minus_r_squared=variance, condition_equal_norm_gram=kappa,
                singular_values=singular.tolist(), max_orthogonalizing_filter_equal_success=variance/(1+corr),
                four_phase_native_weight_over_mean_arm=(original/base_scale).tolist(),
                four_phase_P_weight_over_mean_arm=(pp/base_scale).tolist(),
                four_phase_rest_weight_over_mean_arm=(rr/base_scale).tolist(),
                four_phase_record_minus_native_over_mean_arm=((pp+rr-original)/base_scale).tolist(),
                four_phase_P_fraction_with_record=(pp/(pp+rr)).tolist())


def main():
    result={}
    for tag_name,tag in [('L',255/2048),('H',257/2048)]:
        primary=metric('gauss',6,tag)
        check=metric('cc',7,tag)
        for k,expected in primary.items():
            np.testing.assert_allclose(expected,check[k],rtol=8e-7,atol=6e-13,err_msg=tag_name+' '+k)
        np.testing.assert_allclose(primary['native_lower_u11_probabilities'],check['native_lower_u11_probabilities'],rtol=0,atol=2e-12)
        result[tag_name]=primary
        result[tag_name]['right_pulse_checks']={}
        for label,pulse in [('minus',-1),('plus',1)]:
            case=metric('gauss',6,tag,pulse)
            other=metric('cc',7,tag,pulse)
            key='native_lower_u11_probabilities'
            np.testing.assert_allclose(case[key],other[key],atol=1e-11,rtol=0)
            result[tag_name]['right_pulse_checks'][label]={
                key:case[key], 'difference_from_zero':(np.array(case[key])-primary[key]).tolist(),
                'max_abs_quadrature_difference':float(np.max(np.abs(np.array(case[key])-other[key])))}
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
