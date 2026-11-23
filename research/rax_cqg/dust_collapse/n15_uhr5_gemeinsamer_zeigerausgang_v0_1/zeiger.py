"""Two numerically independent evaluations of the complete auxiliary projection."""
from pathlib import Path
import json
from math import pi
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.linalg import norm

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from ordnung import ORDER, pairs_from_intervals

K = 3.75
D = K*(3/722)**0.25
s = 1/(72*D*K*K)
h = 1/16384
EDGES = pairs_from_intervals()
J = (4,5,6,11)
PHASES = np.array([1,1j,-1,-1j])


def quadrature(method, n):
    if method == 'gauss':
        x,w=leggauss(n)
        return x,w/2
    # Closed Clenshaw-Curtis. Integrals of Chebyshev polynomials on [-1,1]/2.
    theta=np.linspace(pi,0,n)
    k=np.arange(n)
    moments=np.zeros(n)
    moments[::2]=1/(1-k[::2]**2)
    return np.cos(theta),np.linalg.solve(np.cos(k[:,None]*theta),moments)


def wave(method, z, u, v, x):
    y={j:j-5. for j in (0,1,2,3)}
    y[3]+=.25
    y.update({j:y[3]+K*t for j,t in [(4,z),(5,u),(6,.375),(11,v)]})
    if method=='gauss':
        # Lag recurrence and explicit closed-cell widths.
        coeff={}
        for j in J:
            rank=ORDER.index(j)
            coeff[j]=-.5-sum(b*(y[j]-y[ORDER[rank-lag]])**2/38
                              for lag,b in enumerate((1,-9,16,-8),1) if lag<=rank)
        widths=[(z+u)/2,(.375-z)/2,(v-u)/2]
        value=np.exp(1j*D*x*coeff[11])
        for j,f in zip((4,5,6),widths):
            angle=D*f*coeff[j]
            value=value*f*np.exp(1j*angle)*np.sinc(angle/(100*pi))
    else:
        # Enumerate interval-cardinality edges, then explicitly integrate each
        # past density jitter. Cell endpoints and their subtraction are separate.
        coeff={j:-.5 for j in J}
        for (i,j),weight in EDGES.items():
            if j in coeff:
                coeff[j]=coeff[j]-weight*(y[j]-y[i])**2/38
        faces=[0,(z+u)/2,(u+.375)/2,(.375+v)/2]
        jq,jw=leggauss(6)
        value=np.exp(1j*D*x*coeff[11])
        for a,j in enumerate((4,5,6)):
            f=faces[a+1]-faces[a]
            mean=sum(w/2*np.exp(1j*D*f*(1+t/100)*coeff[j]) for w,t in zip(jw,jq))
            value=value*f*mean
    return value


def branch(method,n,x):
    q,w=quadrature(method,n)
    z=.125+q[:,None,None]/64
    t=h*q[None,None,:]
    weight_2d=w[:,None]*w[None,:]/2  # each half of the full pointer window has weight 1/2
    modes=(.25-s+t,.25+s+t)
    direct,bright,rest,common=[],[],[],[]
    control=[]
    for half in (-1,1):
        v=.5+(half+q[None,:,None])/128
        packets=np.array([wave(method,z,u,v,x) for u in modes])
        avg=packets@w
        g=np.array([np.sum(weight_2d*(abs(packet)**2@w)) for packet in packets])
        direct.append(np.diag(g))
        b=np.einsum('aij,bij,ij->ab',avg.conj(),avg,weight_2d)
        common.append(b)
        bright.append(b/2)
        # Keep both packet labels as output coordinates, and integrate the
        # orthogonal residual amplitudes after subtracting the constant mode.
        residual=np.zeros((2,2,n,n,n),dtype=complex)
        for a in range(2):
            for out_arm in range(2):
                residual[a,out_arm]=(packets[a] if out_arm==a else 0)-avg[a,:,:,None]/2
        dark=np.einsum('aoijk,boijk,ij,k->ab',residual.conj(),residual,weight_2d,w)
        rest.append(dark)
        np.testing.assert_allclose(bright[-1]+rest[-1],direct[-1],rtol=1e-12,atol=1e-18)
        assert np.linalg.eigvalsh(bright[-1]).min()>-1e-18 and np.linalg.eigvalsh(dark).min()>-1e-18
        # Direct four preparations in the remaining field coordinates. This
        # cross-check does not use the reconstructed measurement matrices.
        control.append((packets,avg))
    G=sum(direct)
    pscale=1/np.sqrt(G.diagonal())
    normalizer=pscale[:,None]*pscale
    matrix_b=sum(bright)*normalizer
    matrix_r=sum(rest)*normalizer
    in_states=np.column_stack((np.ones(4),PHASES))/np.sqrt(2)
    def prob(m):
        return np.einsum('pi,ij,pj->p',in_states.conj(),m,in_states).real
    pbright=prob(matrix_b)
    pr=prob(matrix_r)
    checked=np.zeros((4,3))
    for i,state in enumerate(in_states*pscale):
        for packets,avg in control:
            mean=np.einsum('a,aij->ij',state,avg)/2
            summed=0
            for arm in range(2):
                output=state[arm]*packets[arm]
                summed+=np.sum(weight_2d*(abs(output-mean[:,:,None])**2@w))
            checked[i,0]+=np.sum(weight_2d*2*abs(mean)**2)
            checked[i,1]+=summed
            checked[i,2]+=np.sum(weight_2d*sum(abs(state[a]*packets[a])**2@w for a in range(2)))
    np.testing.assert_allclose(checked.T,np.array([pbright,pr,np.ones(4)]),rtol=1e-12,atol=3e-14)
    def cross(a):
        return [float(a[0,1].real),float(a[0,1].imag)]
    # Direct scalar product; repeat the small determinant via a positive residual.
    common_sum=sum(common)
    r=common_sum[0,1]/np.sqrt(common_sum.diagonal().prod())
    alpha=common_sum[0,1]/common_sum[0,0]
    residual_norm=sum(np.sum(weight_2d*abs(avg[1]-alpha*avg[0])**2) for _,avg in control)
    r2_loss=residual_norm/common_sum[1,1].real
    np.testing.assert_allclose(1-abs(r)**2,r2_loss,rtol=0,atol=8e-14)
    return dict(aux_input_norms=G.diagonal().tolist(),
                four_phases_bright=pbright.tolist(),four_phases_rest=pr.tolist(),
                four_phases_total=checked[:,2].tolist(),
                native_pointer_low=prob(direct[0]*normalizer).tolist(),
                cross_bright_halves=[cross(b*normalizer) for b in bright],
                cross_rest_halves=[cross(b*normalizer) for b in rest],
                absolute_column_correlation=float(abs(r)),one_minus_corr_squared=float(r2_loss),
                completeness_error=float(norm(matrix_b+matrix_r-np.eye(2),2)))


def continuation(method,n,x):
    q,w=quadrature(method,n)
    rows=[]
    for z in (.125-1/64,.125,.125+1/64):
        first,second=[],[]
        for centre in (.25-s,.25+s):
            u=centre+h*q
            left=wave(method,z,u,.5,x)
            right=np.exp(-1j*16/38*D*K**2/8*(.625-u)**2)
            first.append(w@left)
            second.append(w@(left*right))
        left0=wave(method,z,.25,.5,x)
        minor=first[0]*second[1]-first[1]*second[0]
        value=float(abs(minor/left0**2))
        assert value>.001
        rows.append(value)
    return rows


if __name__=='__main__':
    rows={}
    for name,x in [('low',255/2048),('high',257/2048)]:
        a=branch('gauss',14,x)
        b=branch('clenshaw-curtis',15,x)
        for key,value in a.items():
            np.testing.assert_allclose(value,b[key],rtol=5e-11,atol=3e-14,err_msg=name+'/'+key)
        minor=continuation('gauss',14,x)
        np.testing.assert_allclose(minor,continuation('clenshaw-curtis',15,x),atol=1e-14,rtol=1e-11)
        a['continuation_abs_minor_over_abs_L0_squared']=minor
        rows[name]=a
    print(json.dumps(rows,indent=2,allow_nan=False))
