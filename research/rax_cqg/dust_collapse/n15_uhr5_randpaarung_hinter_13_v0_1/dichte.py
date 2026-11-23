"""Compare coherent closure, recorded bins and a resolved density at 12."""
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from randtest import D,K,H,s,WINDOW,nodes,endpoint_grid,waves

PHASES=np.array([1,1j,-1,-1j])


def compare(method,n):
    q,w=nodes(method,n)
    z=.125+WINDOW*q[None,:,None]
    weights=np.outer(w,w).ravel()
    inputs=np.array([np.ones(4),PHASES])/np.sqrt(2)
    nx,nw=leggauss(5)
    # Entries are (bin centre, halfwidth, weight) in normalized density jitter.
    rules={str(k):[((2*j+1)/k-1,1/k,1/k) for j in range(k)] for k in (1,2,4)}
    rules['resolved']=[(a,0,b/2) for a,b in zip(nx,nw)]
    sums={(side,size,pulse):np.zeros(4) for side in (-1,1) for size in rules for pulse in (-1,0,1)}
    for side,grid,outer in endpoint_grid(method,n,255/2048):
        for start in range(0,len(outer),256):
            part=slice(start,start+256)
            g=grid[part]; wg=outer[part]
            for pulse in (-1,0,1):
                parts=[]
                for arm in (-1,1):
                    u=.25+arm*s+H*q[None,None,:]
                    L,f,c,x13,c13=waves(method,g,z,u,pulse,components=True)
                    # Exp(i D f c) and the event-13 phase are common to all jitter bins.
                    amp=L*f*np.exp(1j*D*(f*c+x13*c13))
                    rate=D*f*c/100
                    parts.append((amp.reshape(len(g),-1),np.broadcast_to(rate,amp.shape).reshape(len(g),-1)))
                for size,rule in rules.items():
                    total=sums[side,size,pulse]
                    for a,b,bw in rule:
                        cols=[]
                        for amp,rate in parts:
                            arg=b*rate
                            if method=='gauss':
                                cf=np.sinc(arg/np.pi)
                            else:
                                cf=1-arg**2*(1/6-arg**2*(1/120-arg**2/5040))
                            cols.append((amp*np.exp(1j*a*rate)*cf)@weights)
                        amplitudes=np.column_stack(cols)@inputs
                        total+=bw*(wg@abs(amplitudes)**2)
    out={}
    for size in rules:
        out[size]={}
        for pulse in (0,-1,1):
            a=sums[-1,size,pulse]
            p=a/(a+sums[1,size,pulse])
            out[size][str(pulse)]=p
    return out


def pointwise():
    # Explicit check of the free common phase against two independently recomputed kernels.
    g=np.array([[.491,.624,.743,.121,255/2048,H],[.507,.626,.758,.127,257/2048,H]])
    y12,y13=g[:,1,None,None],g[:,2,None,None]
    z=np.array([.110,.125,.14])[None,:,None]
    u=np.array([.25-s-H,.25-s+H,.25+s-H,.25+s+H])[None,None,:]
    tests=0
    for pulse in (-1,1):
        step=pulse/(8*np.sqrt(D))
        def shift(j,b):
            return (b/38)*(2*K*(j-.375)*step-step**2)
        left,fc,c0,x13,e0=waves('gauss',g,z,u,0,components=True)
        _,_,c1,_,e1=waves('cc',g,z,u,pulse,components=True)
        for jitter in (-1,0,1):
            x12=fc*(1+jitter/100)
            expected=np.exp(1j*D*(x12*shift(y12,-9)+x13*shift(y13,16)))
            actual=np.exp(1j*D*(x12*(c1-c0)+x13*(e1-e0)))
            np.testing.assert_allclose(actual,np.broadcast_to(expected,actual.shape),rtol=0,atol=2e-15)
            tests+=actual.size
    return tests


def main():
    primary=compare('gauss',5)
    check=compare('cc',6)
    result={'factorization_checks':pointwise(),'tag':'255/2048','bins':{}}
    for key,values in primary.items():
        err=max(np.max(np.abs(p-check[key][pulse])) for pulse,p in values.items())
        if err>4e-12:
            raise ValueError((key,err))
        result['bins'][key]=dict(native_prob_zero=values['0'].tolist(),
                                  plus_minus_difference=(values['1']-values['-1']).tolist(),
                                  max_two_quadrature_difference=float(err))
    resolved=result['bins']['resolved']['plus_minus_difference']
    assert max(map(abs,resolved))<3e-13
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
