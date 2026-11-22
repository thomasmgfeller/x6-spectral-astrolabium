"""Independent full-grid contraction with a Clenshaw-Curtis rule and direct layer counts."""
from fractions import Fraction
import json
import numpy as np
from auslese import settings

def cc(n):
    x=np.cos(np.pi*np.arange(n)/(n-1))
    moments=[0 if k%2 else 1/(1-k*k) for k in range(n)]
    w=np.linalg.solve(np.polynomial.chebyshev.chebvander(x,n-1).T,moments)
    assert min(w)>0 and abs(sum(w)-1)<1e-14
    return x,w

def run(n=4,outer=9):
    states=(1/64,1.)
    rs=(1/8,1/4)
    inner_nodes,node_weights=cc(n);nodes,weights=cc(outer)
    grid=np.indices((n,)*7).reshape(7,-1)
    u=(np.arange(1,8)[:,None]/8)+inner_nodes[grid]/64
    faces=np.vstack([np.zeros(u.shape[1]),(u[:-1]+u[1:])/2,np.ones(u.shape[1])])
    f=np.diff(faces,axis=0)
    measure=np.prod(node_weights[grid]*8*f,axis=0)
    values={(r,m):{label:0j for label in settings()} for r in rs for m in states}
    delta=(3/722)**.25
    for centre in (-1/16,1/16):
        for x,qw in zip(nodes,weights):
            t=centre+x/32;D=4*delta-t;e=t/delta
            fixed=[-5.,-4.,-3.,-2.+e,*(-2+e+(4-e)*u),2.,3.,4.,5.]
            for label,(src,_) in settings().items():
                a,b,p,v,ref=map(float,src)
                y=fixed[:]
                for k,ratio in enumerate((76,47,24,8)):y[k]+=(p+v*ratio/64)/np.sqrt(D)
                # Positions seven and nine in the sorted order correspond to labels 11 and 13.
                y[7]=y[7]+a/np.sqrt(D);y[9]=y[9]+b/np.sqrt(D)
                g=[]
                for j in range(15):
                    s=-.5
                    for i in range(j):
                        count=j-i-1
                        if count<4:s=s-(1,-9,16,-8)[count]*(y[j]-y[i])**2/38
                    g.append(s)
                past=sum(g[:4])
                phase=sum(g[11:])/8-ref*(7/8)/D
                for m in states:
                    dw=m*D*f*np.asarray(g[4:11])
                    response=np.exp(1j*(phase+np.sum(dw,axis=0)))*np.prod(np.sinc(.01*dw/np.pi),axis=0)
                    inner=np.dot(measure,response)*D**14*qw/2
                    for rho in rs:
                        values[rho,m][label]+=inner*np.exp(1j*rho*past)*np.sinc(past/(32*np.pi))
    out={}
    for (r,m),z in values.items():
        # Decode directly by grouping pairs, without using the coefficient-vector decoder.
        ph={k:np.angle(v/z['0']) for k,v in z.items()}
        h=.125
        aa=(ph['A+']+ph['A-'])/h**2
        bb=(ph['B+']+ph['B-'])/h**2
        def mixed(l,r):
            return sum((1 if s==t else -1)*ph[l+s+r+t] for s in ('+','-') for t in ('+','-'))/(4*h*h)
        out[f'{Fraction(r)}|positive|{Fraction(m)}']=float((ph['C+']-ph['C-'])/(2*h)-19*(aa+(10/9)*mixed('A','B')-15*bb-mixed('U','V')))
    return out

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
