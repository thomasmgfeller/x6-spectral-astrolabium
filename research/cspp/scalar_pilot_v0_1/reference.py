"""Two-resolution periodic Fourier KG reference: diagnostic, NOT certified error bounds."""
import numpy as np
from scipy.fft import fftn, ifftn, fftfreq
from scipy.integrate import quad

def source_norm():
    integral,error=quad(lambda r:4*np.pi*r*r*np.exp(-2/(1-4*r*r)),0,.5,epsabs=1e-14,epsrel=1e-13)
    return 1/np.sqrt(integral),error
def source(x):
    r2=np.sum(np.asarray(x)**2,axis=-1);out=np.zeros(r2.shape,complex)
    use=r2<.25
    out[use]=source_norm()[0]*np.exp(-1/(1-4*r2[use]))*np.exp(4j*np.asarray(x)[...,2][use])
    return out
def interpolate(grid,xyz,length):
    n=grid.shape[0];v=(xyz+length/2)*(n/length)
    base=np.floor(v).astype(int);f=v-base
    out=np.zeros(len(xyz),complex)
    for i in [0,1]:
        for j in [0,1]:
            for k in [0,1]:
                ijk=(base+[i,j,k])%n
                w=np.prod(np.where(np.array([i,j,k]),f,1-f),axis=1)
                out+=w*grid[ijk[:,0],ijk[:,1],ijk[:,2]]
    return out
def evaluate(x,n,dt,length=12.,progress=None):
    """Stream time planes; trilinear space/linear time interpolation.

    Exact continuum KG spectral multiplier on a sampled periodic source.
    Box radius 6 exceeds support radius .5+max|t+1| for this pilot.
    Source discretization/interpolation errors are not thereby certified.
    """
    q=(np.arange(n)-n//2)*(length/n)
    xx,yy,zz=np.meshgrid(q,q,q,indexing='ij')
    f=source(np.stack([xx,yy,zz],axis=-1));del xx,yy,zz
    initial_grid_norm=float(np.sum(np.abs(f)**2)*(length/n)**3)
    fh=fftn(f,workers=1);del f
    k=2*np.pi*fftfreq(n,d=length/n)
    k2=k[:,None,None]**2+k[None,:,None]**2+k[None,None,:]**2
    tmin=-4.; ts=tmin+np.arange(round(5/dt)+1)*dt
    binid=np.floor((x[:,0]-tmin)/dt).astype(int)
    binid=np.clip(binid,0,len(ts)-2)
    frac=(x[:,0]-ts[binid])/dt
    output=np.zeros((len(x),3),complex)
    for mi,m in enumerate([0,1,2]):
        omega=np.sqrt(k2+m*m)
        for ti,t in enumerate(ts):
            use=np.flatnonzero((binid==ti)|(binid+1==ti))
            if len(use)==0:continue
            grid=ifftn(fh*np.cos(omega*(t+1)),workers=1)
            value=interpolate(grid,x[use,1:],length)
            w=np.where(binid[use]==ti,1-frac[use],frac[use])
            output[use,mi]+=w*value
        if progress:progress(f'Fourier n={n}, mass={m} done')
    return output,{'n':n,'dt':dt,'initial_grid_L2_squared':initial_grid_norm,
                   'reference_status':'REFERENCE_HOLD_NO_CERTIFIED_REMAINDER'}
