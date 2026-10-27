"""Fourier KG comparison at exact grid nodes and exact requested times."""
import numpy as np
from scipy.fft import fftn, ifftn, fftfreq
from common import oldref

def evaluate(probes,n,length=8.):
    dx=length/n;v=(probes[:,1:]+length/2)/dx;ids=np.rint(v).astype(int)
    if not np.allclose(v,ids,rtol=0,atol=1e-12):raise ValueError('exact grid-node probes required')
    # Populate only the compact source support, avoiding full coordinate meshes.
    q=(np.arange(n)-n//2)*dx;use=np.flatnonzero(np.abs(q)<.5)
    xx=np.stack(np.meshgrid(q[use],q[use],q[use],indexing='ij'),axis=-1)
    f=np.zeros((n,n,n),complex);f[np.ix_(use,use,use)]=oldref.source(xx)
    norm=float(np.sum(np.abs(f)**2)*dx**3)
    fh=fftn(f,overwrite_x=True,workers=1);del f
    k=2*np.pi*fftfreq(n,d=dx);k2=k[:,None,None]**2+k[None,:,None]**2+k[None,None,:]**2
    answer=np.zeros((len(probes),3),complex)
    for j,m in enumerate([0,1,2]):
        om=np.sqrt(k2+m*m)
        for t in np.unique(probes[:,0]):
            ii=np.flatnonzero(probes[:,0]==t)
            field=ifftn(fh*np.cos(om*(t+1)),overwrite_x=True,workers=1)
            answer[ii,j]=field[ids[ii,0]%n,ids[ii,1]%n,ids[ii,2]%n]
            del field
    return answer,{'N':n,'box_length':length,'dx':dx,'initial_grid_norm_squared':norm,
                   'space_interpolation':False,'time_interpolation':False}
