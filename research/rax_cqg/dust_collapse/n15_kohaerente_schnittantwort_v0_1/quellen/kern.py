"""Deterministic product quadratures, interval counting and chronological contraction."""
import math
from functools import lru_cache
import numpy as np
from numpy.polynomial.legendre import leggauss
from ordnung import ORDER,PAST,INNER,FUTURE,A,B,links_to,pairs_from_intervals,source_parts

ETA=0.01
DELTA=(3/722)**0.25
EDGES=pairs_from_intervals()
VISIBLE,HIDDEN=source_parts(EDGES)
COLLAR={7:-127,8:240,9:-120}
U=dict.fromkeys(PAST,1.)
V=dict(zip(PAST,[76/64,47/64,24/64,8/64]))
REGIONS=[(ORDER[:8]),ORDER[8:10],ORDER[10:]]
UNIT=np.ones((1,)*7)

@lru_cache(None)
def gauss(n):
    x,w=leggauss(n)
    return x,w/2

def clocks(n,e):
    x,w=gauss(n)
    u=[(k+1)/8+x.reshape((1,)*k+(n,)+(1,)*(6-k))/64 for k in range(7)]
    ys={v:float(v-5) for v in PAST+FUTURE};ys[3]+=e
    ys.update({j:ys[3]+(4-e)*s for j,s in zip(INNER,u)})
    faces=[0]+[(i+j)/2 for i,j in zip(u,u[1:])]+[1]
    shares={j:right-left for j,left,right in zip(INNER,faces,faces[1:])}
    if any(np.min(f)<=0 for f in shares.values()):raise ValueError("Nonpositive cell")
    return ys,shares

def contract(factors,n,stream):
    """Integrate one axis once its final factor has been inserted."""
    last={}
    for k,f in enumerate(factors):
        for axis,dim in enumerate(f.shape):
            if dim!=1:last[axis]=k
    if set(last)!=set(range(7)):raise ValueError('Incomplete clock integration')
    g=UNIT
    for k,f in enumerate(factors):
        g=g*f
        for axis,done in last.items():
            if (stream and k==done) or (not stream and k==len(factors)-1):
                w=gauss(n)[1].reshape((1,)*axis+(n,)+(1,)*(6-axis))
                g=np.sum(g*w,axis=axis,keepdims=True)
    return g.item()

def sinc(z):
    return np.sinc(z/np.pi)

def moments(z,bar,halfwidth):
    # Exponential tilt of the uniform density jitter; analytic derivatives of log(sinc).
    # Use the local series near zero and the analytic cotangent away from it.
    if np.max(np.abs(z))>=.05:
        if np.min(np.abs(z))<.04 or np.max(np.abs(z))>=1:raise ValueError('Invalid cotangent domain')
        return bar-1j*halfwidth*(1/np.tan(z)-1/z),halfwidth**2*(1/np.sin(z)**2-1/z**2)
    grad=-z/3-z**3/45-2*z**5/945-z**7/4725
    minus_hess=1/3+z*z/15+2*z**4/189+z**6/675+2*z**8/10395
    return bar-1j*halfwidth*grad,halfwidth**2*minus_hess

def site_data(n,offset,shifts,stream,drop_cross=False):
    e=offset/DELTA;D=4*DELTA-offset
    y,fr=clocks(n,e)
    # Keep the integration measure fixed here, including dwell fractions and the old duration.
    y[A]=y[A]+shifts[0]/math.sqrt(D);y[B]=y[B]+shifts[1]/math.sqrt(D)
    for j in PAST:
        if len(shifts)==4:y[j]+=(shifts[2]+V[j]*shifts[3])/math.sqrt(D)
    for k,j in enumerate(ORDER):
        inc=links_to(k) if stream else [(i,c) for (i,end),c in EDGES.items() if end==j]
        if drop_cross:inc=[(i,c) for i,c in inc if any(i in g and j in g for g in REGIONS)]
        g=-.5*UNIT;da=0.;db=0.;du=0.;dv=0.
        for i,c in inc:
            diff=y[j]-y[i]
            g=g-(c/38)*diff*diff
            da=da-(c/19)*(int(j==A)-int(i==A))*diff/math.sqrt(D)
            db=db-(c/19)*(int(j==B)-int(i==B))*diff/math.sqrt(D)
            du=du-(c/19)*(U.get(j,0)-U.get(i,0))*diff/math.sqrt(D)
            dv=dv-(c/19)*(V.get(j,0)-V.get(i,0))*diff/math.sqrt(D)
        yield j,g,da,db,du,dv,fr.get(j)

def integrand(n,offset,rho,shifts=(0,0),tag=0,stream=False,jet=False,extra=0,drop_cross=False,collar_only=False,constant_phase=0):
    D=4*DELTA-offset
    past=0.;factors=[];vel_a=0.;vel_b=0.;conditional_cov=0.;mass=0.;other=0.
    vel_u=vel_v=cond_uv=past_u=past_v=collar=0.
    for j,g,da,db,du,dv,f in site_data(n,offset,shifts,stream,drop_cross):
        if j in PAST:
            past=past+g
            past_u=past_u+du;past_v=past_v+dv
            if j==PAST[-1]:
                factors.append(np.exp(1j*(rho*past+constant_phase))*sinc(past/32))
                if jet:
                    mr,vr=moments(past/32,rho,1/32)
                    vel_u=vel_u+past_u*mr;vel_v=vel_v+past_v*mr;cond_uv=cond_uv+past_u*past_v*vr
            continue
        # For the comparison of ordinary clock responses, extra couples the visible
        # densities and the independently known collar term to a linear reference source.
        marker=float(VISIBLE[j]+HIDDEN[j]) if stream else float(j in INNER)
        ref=float(VISIBLE[j]+COLLAR.get(j,0))
        g=g+(tag*marker+extra*(COLLAR.get(j,0) if collar_only else ref))/D
        if j in FUTURE:
            mean=.125;var=0.
            factors.append(np.exp(1j*mean*g))
        else:
            base=4*D*f
            z=ETA*base*g
            factors.append(8*f*np.exp(1j*base*g)*sinc(z))
            if jet:mean,var=moments(z,base,base*ETA)
        if jet:
            vel_a=vel_a+da*mean;vel_b=vel_b+db*mean
            conditional_cov=conditional_cov+var*(da*da+(10/9)*da*db-15*db*db)
            vel_u=vel_u+du*mean;vel_v=vel_v+dv*mean;cond_uv=cond_uv+du*dv*var
            collar=collar+COLLAR.get(j,0)*mean/D
            mass=mass+marker*mean/D;other=other+ref*mean/D
    if not jet:return D**14*contract(factors,n,stream)
    def av(v):
        return D**14*contract(factors+[UNIT*v],n,False)
    second=vel_a**2+(10/9)*vel_a*vel_b-15*vel_b**2+conditional_cov
    return np.array([av(1),av(vel_a),av(vel_b),av(second),av(mass),av(other),av(vel_u),av(vel_v),av(vel_u*vel_v+cond_uv),av(collar)])

def integrate(n,outer,rho,**args):
    x,w=gauss(outer);s=0.
    for centre in (-1/16,1/16):
        for t,weight in zip(x,w):
            s=s+(weight/2)*integrand(n,centre+t/32,rho,**args)
    return s

def statistics(n,outer,rho):
    z,p,q,second,mass,other,u,v,uv,collar=integrate(n,outer,rho,jet=True)
    p,q,second,mass,other=(v/z for v in (p,q,second,mass,other))
    cov=second-p*p-(10/9)*p*q+15*q*q
    ordinary=mass.real+19*cov.imag
    cov_uv=uv/z-(u/z)*(v/z)
    all_clock=ordinary-19*cov_uv.imag
    arms=[integrate(n,outer,rho,stream=True,tag=tag) for tag in (.25,-.25)]
    reading=np.angle(arms[0]*arms[1].conjugate())/.5
    return {'weak_mass_real':float(mass.real),'weak_mass_imag':float(mass.imag),'covariance_real':float(cov.real),
            'covariance_imag':float(cov.imag),'ordinary_mass':float(ordinary),'ordinary_relative_percent':float(25*(ordinary-4)),
            'outer_covariance_imag':float(cov_uv.imag),'all_clock_mass':float(all_clock),'all_clock_signed_percent':float(25*(all_clock-4)),
            'collar_real':float((collar/z).real),'finite_pointer':float(reading),'finite_signed_percent':float(25*(reading-4)),'other_real':float(other.real),
            'unshifted_complex':[float(z.real),float(z.imag)]}

def finite_difference(n,outer,rho,h,record=False):
    def get(a=0,b=0,u=0,v=0,extra=0,collar=False):
        return integrate(n,outer,rho,stream=True,shifts=(a,b,u,v),extra=extra,collar_only=collar)
    z=get()
    sampled={'Referenz':[0.,1.]}
    def phase(a=0,b=0,u=0,v=0,extra=0,collar=False):
        ratio=get(a,b,u,v,extra,collar)/z
        angle=np.angle(ratio)
        if record:
            settings=(('A',a),('B',b),('U',u),('V',v),('Kragen' if collar else 'Hybrid',extra))
            label=' '.join(name+('+' if step>0 else '-') for name,step in settings if step)
            sampled[label]=[float(angle),float(abs(ratio))]
        if abs(angle)>1.:raise ValueError('Source phase outside local branch')
        return angle
    aa=(phase(h,0)+phase(-h,0))/h**2
    bb=(phase(0,h)+phase(0,-h))/h**2
    ab=sum(i*j*phase(i*h,j*h) for i in (-1,1) for j in (-1,1))/(4*h*h)
    uv=sum(i*j*phase(u=i*h,v=j*h) for i in (-1,1) for j in (-1,1))/(4*h*h)
    base=(phase(extra=h)-phase(extra=-h))/(2*h)
    collar=(phase(extra=h,collar=True)-phase(extra=-h,collar=True))/(2*h)
    inner=-19*(aa+(10/9)*ab-15*bb)
    result={'hybrid_mass':float(base+inner),'all_clock_mass':float(collar+19*uv+inner)}
    if record:result['source_phase_and_relative_modulus']=sampled
    return result
