"""Uniform source-perturbation bounds from rational intervals on the full tube."""
from fractions import Fraction as Q
from math import isqrt
from itertools import product
from ordnung import ORDER,PAST,INNER,FUTURE,A,B,pairs_from_intervals

def const(v):return (Q(v),Q(v))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    v=[x*y for x in a for y in b]
    return min(v),max(v)
def scale(a,c):return mul(a,const(c))
def bound(a):return max(abs(a[0]),abs(a[1]))
def recip(a):
    assert a[0]>0
    return 1/a[1],1/a[0]
def sqrt_bounds(a):
    grid=10**12
    result=[isqrt((v*grid**2).__floor__()) for v in a]
    return Q(result[0],grid),Q(result[1]+1,grid)

def phase_bounds(reference,h=Q(1,8)):
    grid=10**12
    d0=isqrt(isqrt(3*grid**4//722))
    delta=Q(d0,grid),Q(d0+1,grid)
    assert delta[0]**4<=Q(3,722)<=delta[1]**4
    directions={'zero':{},'aa':{A:1},'bb':{B:1}}
    for sign in [-1,1]:
        directions['ab'+str(sign)]={A:1,B:sign}
        directions['uv'+str(sign)]={p:1+sign*Q(v,64) for p,v in zip(PAST,(76,47,24,8))}
    edges=pairs_from_intervals()
    ans={}
    for rho in (Q(1,8),Q(1,4)):
        c=Q(reference['by_type']['2097151']['dust'][str(rho)]['amplitude_floor'])
        maxima={k:Q(0) for k in [*directions,'collar']}
        for centre in (Q(-1,16),Q(1,16)):
            for k in range(8):
                left=centre-Q(1,32)+Q(k,128)
                o=(left,left+Q(1,128));e=mul(o,recip(delta))
                du=add(const(4),scale(e,-1));duration=add(scale(delta,4),scale(o,-1))
                ys={j:const(j-5) for j in PAST+FUTURE};ys[3]=add(ys[3],e)
                u={j:(Q(i+1,8)-Q(1,64),Q(i+1,8)+Q(1,64)) for i,j in enumerate(INNER)}
                ys.update({j:add(ys[3],mul(du,s)) for j,s in u.items()})
                # Inner cell fractions are affine; shared middle clock cancels exactly.
                fminmax={j:((Q(3,16) if j in (4,14) else Q(1,8))-Q(1,64),
                             (Q(3,16) if j in (4,14) else Q(1,8))+Q(1,64)) for j in INNER}
                w={j:(rho-Q(1,32),rho+Q(1,32)) for j in PAST};w.update(dict.fromkeys(FUTURE,const(Q(1,8))))
                for j in INNER:w[j]=mul(mul(scale(duration,4),fminmax[j]),(Q(99,100),Q(101,100)))
                for key,v in directions.items():
                    linear=const(0);quadratic=const(0)
                    for j in ORDER:
                        coeff={};square=0
                        for (i,end),b in edges.items():
                            if end!=j:continue
                            dv=v.get(j,0)-v.get(i,0)
                            coeff[j]=coeff.get(j,0)+b*dv;coeff[i]=coeff.get(i,0)-b*dv
                            square+=b*dv**2
                        lin=const(0)
                        for node,x in coeff.items():lin=add(lin,scale(ys[node],x))
                        linear=add(linear,mul(w[j],lin));quadratic=add(quadratic,scale(w[j],square))
                    alpha=bound(linear)*h/(19*sqrt_bounds(duration)[0])+bound(quadratic)*h*h/(38*duration[0])
                    maxima[key]=max(maxima[key],alpha)
                maxima['collar']=max(maxima['collar'],h*Q(7,8)/duration[0])
        assert max(maxima.values())<c
        def up(v):return Q((v*10**9).__ceil__(),10**9)
        def down(v):return Q((v*10**9).__floor__(),10**9)
        ans[str(rho)]={'base_floor':c,'perturbation_upper':{k:up(v) for k,v in maxima.items()},
                       'modulus_floor_all_settings':down(c-max(maxima.values()))}
    return ans

def phase_gain(h):
    # The shared central phase enters with coefficient (38-570)/h².
    coeff=[Q(-532,h*h)]+[Q(-19,h*h)]*2+[Q(285,h*h)]*2
    coeff += [Q(-190*i*j,36*h*h) for i,j in product((-1,1),repeat=2)]
    coeff += [Q(19*i*j,4*h*h) for i,j in product((-1,1),repeat=2)]
    coeff += [Q(1,2*h),Q(-1,2*h)]
    assert len(coeff)==15 and sum(coeff)==0
    gain=sum(map(abs,coeff))
    assert gain==Q(10621,9*h*h)+1/h
    return gain
