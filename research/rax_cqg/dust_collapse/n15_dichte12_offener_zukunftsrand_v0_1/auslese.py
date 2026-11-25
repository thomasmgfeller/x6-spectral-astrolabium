"""Coherent full dust integral, followed by readout on a flat open future collar."""
import sys
import json
from pathlib import Path
from itertools import product
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from absoluter_schnitt import EDGES_B, EDGES_V, DIFF, split
from randtest import D, K, H, s, WINDOW, a_segments, nodes, waves
from ordnung import ORDER, INNER, FUTURE, pairs_from_intervals
from zertifikat import ORIGIN, CROSS, ETA

ETA=float(ETA)
TAG=255/2048
EDGES=pairs_from_intervals()
MODES=('rel_low','rel_high','abs_low','abs_high')

def rule_segments(method,n):
    q,w=nodes(method,n)
    points=[]
    for vl,vr in split(*EDGES_V,[b-d for b,d in product(EDGES_B,DIFF)]):
        for vn,vw in zip(q,w):
            v=float((vl+vr)/2)+float((vr-vl)/2)*vn
            for bl,br in split(*map(float,EDGES_B),[v+float(d) for d in DIFF]):
                for bn,bw in zip(q,w):
                    b=(bl+br)/2+(br-bl)/2*bn
                    points.append((v,b,vw*bw*float(vr-vl)*(br-bl)/(2*WINDOW)**2))
    vb=np.array(points)
    for al,ar in a_segments(TAG):
        # Integrate clocks at 11,13 and 12,14. All density integrals are analytic.
        v,b,wb=vb.T
        a,c=np.meshgrid((al+ar)/2+(ar-al)*q/2,.875+WINDOW*q,indexing='ij')
        wc=np.outer(w,w).ravel()*(ar-al)/(2*WINDOW)
        v,b,wb=(np.repeat(vec,len(wc)) for vec in (v,b,wb))
        a,c,wa=(np.tile(vec,len(vb)) for vec in (a.ravel(),c.ravel(),wc))
        for i in range(0,len(a),256):
            t=slice(i,i+256)
            yield v[t],a[t],b[t],c[t],(wa*wb)[t]

def coeff(j,y,pulse):
    out=-.5
    for (i,end),weight in EDGES.items():
        if j==end:
            shift=pulse/(8*np.sqrt(D)) if i==6 and j in (12,13,14) else 0
            out=out-weight*(y[j]-y[i]-shift)**2/38
    return out

def columns(method,n,v,a,b,c,pulse,enabled=True):
    q,w=nodes(method,n)
    z=.125+WINDOW*q[None,:,None]
    wzu=np.outer(w,w).ravel()
    f13=(c-a)/2
    f14=1-(b+c)/2
    yl={j:float(j-5) for j in FUTURE}
    yl.update({j:-1.75+K*t for j,t in [(6,.375),(11,v),(12,a),(13,b),(14,c)]})
    lo=np.maximum(TAG-H,.99*(a-.375)/2)
    hi=np.minimum(TAG+H,1.01*(a-.375)/2)
    g=np.column_stack((v,a,b,f13,(lo+hi)/2,np.maximum(hi-lo,0)/2))
    c14=coeff(14,yl,pulse)
    late=(f14*np.sinc(D*f14*c14/100/np.pi)*np.exp(1j*(D*f14*c14+sum(coeff(j,yl,0)/8 for j in FUTURE)))
          if enabled else f14)
    vals=np.zeros((len(v),4),complex)
    for sign in (-1,1):
        u=.25+sign*s+H*q[None,None,:]
        left,f,c12,_,c13=waves(method,g,z,u,pulse,components=True)
        if not enabled:
            left=(g[:,5,None,None]/H)*((z+u)/2)*((.375-z)/2)*((v[:,None,None]-u)/2)
            c12=np.zeros_like(c12)
            c13=np.zeros_like(c13)
        f3=f13[:,None,None]
        base=left*late[:,None,None]*f3*np.exp(1j*D*f3*c13)*np.sinc(D*f3*c13/100/np.pi)
        lo12=.99*f
        hi12=1.01*f
        absolute=np.clip(.125,lo12,hi12)
        for k,(l,r) in enumerate(((lo12,f),(f,hi12),(lo12,absolute),(absolute,hi12))):
            hw=(r-l)/2
            amp=base*(100*hw)*np.sinc(D*hw*c12/np.pi)*np.exp(1j*D*(l+r)/2*c12)
            vals[:,k]+=amp.reshape(len(v),-1)@wzu
    np.testing.assert_allclose(vals[:,0]+vals[:,1],vals[:,2]+vals[:,3],rtol=7e-14,atol=3e-20)
    return vals,yl

def sensitivity(y):
    # Coefficients of the exact centred mixed phase, in dimensionless cube coordinates.
    lin=np.zeros((len(y[11]),7))
    mixed=np.zeros((len(y[11]),3))
    for i,j,b in CROSS:
        t=y[i]-float(ORIGIN[i])
        gap=float(ORIGIN[j]-ORIGIN[i])
        lin[:,j-4]+=ETA*b*(2*gap*t-t*t)/38
        if j!=7:
            lin[:,j-8]+=ETA*b*t/(8*19)
            mixed[:,j-8]+=ETA**2*b*t/19
    return lin,mixed

def coefficients(method,n,pulse,enabled):
    norm=np.zeros(4,complex)
    linear=np.zeros((4,7),complex)
    quad=np.zeros((4,7,7),complex)
    # Independent w7 rotation using expm1, on the matched halves of the interval.
    q,w=nodes('gauss',6)
    dx=np.r_[(q-1)/2,(q+1)/2]
    direct=np.zeros((4,len(dx)),complex)
    for v,a,b,c,wt in rule_segments(method,n):
        val,y=columns(method,n,v,a,b,c,pulse,enabled)
        val=(val*wt[:,None]).T
        lin,mix=sensitivity(y)
        if not enabled:
            lin.fill(0);mix.fill(0)
        norm+=val.sum(axis=1)
        linear+=1j*(val@lin)
        direct+=val@np.expm1(1j*lin[:,3,None]*dx)
        for k in range(4):
            quad[k]-=.5*(val[k,:,None]*lin).T@lin
        for axis in range(3):
            v2=.5j*(val@mix[:,axis])
            quad[:,axis,axis+4]+=v2
            quad[:,axis+4,axis]+=v2
    return norm,linear/norm[:,None],quad/norm[:,None,None],direct/norm[:,None],dx,w

def orthogonal_basis(linear,quad):
    diagonal=np.diag(quad)
    return np.r_[1+sum(diagonal)/3,linear/np.sqrt(3),2*diagonal/(3*np.sqrt(5)),2*quad[np.triu_indices(7,1)]/3]

def trace_distance(a,b):
    # Both constant components are nonzero. Fix this common ray coordinate
    # exactly to 1 before projecting the small *difference* of the columns.
    u=np.r_[1.+0j,a[1:]/a[0]]
    v=np.r_[1.+0j,b[1:]/b[0]]
    delta=v-u
    residual=delta-u*(np.vdot(u,delta)/np.vdot(u,u))
    return float(np.linalg.norm(residual)/np.linalg.norm(v))

def paired_offset(low,high,weights):
    # low/high are small differences from 1, avoiding cancellation in tiny contrasts.
    numer=np.sum(weights*(high-low+low.conj()*high).imag)
    denom=np.sum(weights*(abs(1+low)**2+abs(1+high)**2))
    return float(numer/denom)

def detector_cube(linear,quad):
    q,w=nodes('gauss',3)
    g=np.array(list(product(q,repeat=7)))
    weights=np.prod(np.array(list(product(w,repeat=7))),axis=1)
    low=g.copy();low[:,3]=(g[:,3]-1)/2
    high=low.copy();high[:,3]+=1
    def delta(coords):
        return coords@linear+np.sum((coords@quad)*coords,axis=1)
    return paired_offset(delta(low),delta(high),weights)

def evaluate(method,n,pulse,enabled=True):
    norm,lin,quad,direct,dx,w=coefficients(method,n,pulse,enabled)
    vectors=np.array([orthogonal_basis(l,q) for l,q in zip(lin,quad)])
    offsets=[detector_cube(l,q) for l,q in zip(lin,quad)]
    # Exact w7 phases are integrated inside each clock quadrature evaluation.
    approximate=lin[:,3,None]*dx+quad[:,3,3,None]*dx**2
    assert np.max(abs(approximate-direct))<2e-20
    result={}
    for name,(lo,hi) in {'relative':(0,1),'absolute':(2,3)}.items():
        d=trace_distance(vectors[lo],vectors[hi])
        weights=abs(norm)**2*np.sum(abs(vectors)**2,axis=1)
        # Compute the 1D ray separation on 12 nodes using only small differences.
        da,db=direct[[lo,hi]]
        ww=np.tile(w/2,2)
        a=1+da
        delta=db-da
        projection=np.sum(ww*a.conj()*delta)/np.sum(ww*abs(a)**2)
        dw=np.sqrt(np.sum(ww*abs(delta-projection*a)**2)/np.sum(ww*abs(1+db)**2))
        one_d=[paired_offset(row[:len(w)],row[len(w):],w) for row in (da,db)]
        result[name]={'trace_distance_7d':d,'optimal_success_advantage_over_half':d/2,
            'common_w7_detector_high_minus_low':offsets[hi]-offsets[lo],
            'w7_only_trace_distance':float(dw),'w7_only_detector_high_minus_low':one_d[1]-one_d[0],
            'pairing_two_bins_low_fraction':float(weights[lo]/(weights[lo]+weights[hi])),
            'closed_same_ray_distance':0}
    return result

def main():
    out={}
    for p,active,label in [(0,True,'zero'),(-1,True,'minus'),(1,True,'plus'),(0,False,'action_off')]:
        a=evaluate('gauss',6,p,active)
        b=evaluate('cc',7,p,active)
        errors={s:{k:abs(x-b[s][k]) for k,x in row.items()} for s,row in a.items()}
        for row in errors.values():
            for k,x in row.items():
                lim=5e-12 if k=='pairing_two_bins_low_fraction' else 2e-18
                assert x<lim, (label,k,x,lim)
        out[label]={'reference':a,'quadrature_differences':errors}
    for scenario in out.values():
        for row in scenario['reference'].values():
            assert abs(row['common_w7_detector_high_minus_low']) <= row['trace_distance_7d']+1e-20
            assert abs(row['w7_only_detector_high_minus_low']) <= row['w7_only_trace_distance']+1e-20
    assert all(row['trace_distance_7d']==0 for row in out['action_off']['reference'].values())
    assert out['zero']['reference']['absolute']['trace_distance_7d']>1e-8
    return out

if __name__=='__main__':
    print(json.dumps(main(),indent=2,allow_nan=False))
