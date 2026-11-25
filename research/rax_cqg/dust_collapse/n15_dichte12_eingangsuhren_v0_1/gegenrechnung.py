"""Separate floating-point quadrature of the full two-setting experiment."""
import cmath
import math
from itertools import product

ORDER=(0,1,2,3,4,5,6,11,12,13,14,7,8,9,10)
INS=ORDER[4:11]
D=3.75*(3/722)**0.25
COEFS=(1,-9,16,-8)
PROFILE=(1.25,1.125,1,1)
PRIMES=(2,3,5,7,11,13,17)


def sinc(t):
    return math.sin(t)/t if t else 1.


def node(k,p):
    value=0.
    place=1./p
    while k:
        k,rem=divmod(k,p)
        value+=rem*place
        place/=p
    return 2*value-1.


def full_coeffs(y):
    c=[]
    for j,t in enumerate(y):
        c.append(-.5-sum(COEFS[l-1]*(t-y[j-l])**2
                          for l in range(1,1+min(j,4)))/38)
    return c


def output(nz,nu,rho,second=False):
    numer=[0.,0.]; denom=[0.,0.]
    for iz in range(1,nz+1):
        z=[node(iz,p)/2**20 for p in PRIMES]
        yend=[2.,3.+z[0],4.+z[1],5.+z[2]]
        wend=[.125+t for t in z[3:]]
        amplitudes=[[0j,0j],[0j,0j]]
        for k,lobe in product(range(1,nu+1),(-1,1)):
            jitter=iter(node(k,p)/2**22 for p in PRIMES[:6])
            u=[j/8+(next(jitter) if j!=3 else 0.) for j in range(1,8)]
            u[1]+=lobe/1000
            y=[-5.,-4.,-3.,-1.75]+[-1.75+3.75*t for t in u]+yend
            c0=full_coeffs(y)
            # Solve the three hidden constraints by direct elimination.
            b12,b13,b14=-9.,16.,-8.
            d=[0.]*7
            d[4]=1.
            d[5]=-(b12*(y[8]-y[10]))/(b13*(y[9]-y[10]))
            d[6]=-(b12+b13*d[5])/b14
            mass=sum(d)
            action=sum(a*b for a,b in zip(c0[4:11],d))
            if second:
                d=[v*(-1.25/action) for v in d]
            else:
                d[0]=(mass*c0[5]-action)/(c0[4]-c0[5])
                d[1]=-mass-d[0]
            face=[0]+[(a+b)/2 for a,b in zip(u,u[1:])]+[1.]
            center=[b-a for a,b in zip(face,face[1:])]
            center[3]=255/2048
            for mode in range(2):
                c=full_coeffs([y[i]+mode*PROFILE[i]/(8*math.sqrt(D)) for i in range(4)]+y[4:])
                past=sum(c[:4])
                scale=sinc(past/32)*math.prod(sinc(D*t/2**20) for t in c[4:11])
                for idx,sign in enumerate((-1,1)):
                    mid=[v+sign*dd/2**14 for v,dd in zip(center,d)]
                    phase=rho*past+sum(a*b for a,b in zip(wend,c[11:]))+D*sum(a*b for a,b in zip(mid,c[4:11]))
                    amplitudes[idx][mode]+=scale*cmath.exp(1j*phase)
        for j,(a,b) in enumerate(amplitudes):
            numer[j]+=abs(a-1j*b)**2/2
            denom[j]+=abs(a)**2+abs(b)**2
    p=[x/n for x,n in zip(numer,denom)]
    return p[1]-p[0]


def check(certificate):
    output_rows={}
    for rho in (.125,.25):
        key='1/8' if rho==.125 else '1/4'
        lo,hi=map(float,certificate['source'][key]['plus_probability_high_minus_low'])
        rows={}
        for nz,nu in ((8,12),(21,40)):
            val=output(nz,nu,rho)
            ctrl=output(nz,nu,rho,second=True)
            assert lo<val<hi and abs(ctrl)<1e-13
            rows[f'{nz}x{nu}']={'difference_first_pair':val,'difference_second_pair':ctrl}
        output_rows[key]=rows
    return output_rows
