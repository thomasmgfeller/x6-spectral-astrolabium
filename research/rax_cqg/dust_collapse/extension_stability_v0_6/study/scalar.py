"""High-precision Gaussian overlaps of the three q7 detector bins."""
from common import HERE, setup, prior
import mpmath as mp
import numpy as np

def run():
    names, _ = setup()
    mp.mp.dps = 70
    geom = prior.growth.geometry
    with prior.growth.scalar_layouts():
        states = []
        for name in names:
            row,state=geom.kernel(prior.key(name))
            assert row['status']=='ADMISSIBLE'
            states.append(state)
    print('169 admissible states reconstructed',flush=True)
    gram=np.empty((3,len(names),len(names)),complex)
    for i,(left,la) in enumerate(states):
        for j in range(i,len(names)):
            right,ra=states[j]
            h=left.conjugate()+right
            root=geom.continued_sqrt(h)
            z=mp.conj(la)*ra*(2*mp.pi)**mp.mpf('1.5')/root
            if i==j: assert abs(z-1)<mp.mpf('1e-45')
            inverse00=(h[1,1]*h[2,2]-h[1,2]*h[2,1])/root**2
            central=z*mp.erf(1/mp.sqrt(2*(1+inverse00)))
            g=np.array([complex((z-central)/2),complex(central),complex((z-central)/2)])
            if i==j:
                assert max(abs(g.imag))<1e-45
                g=g.real
            gram[:,i,j]=g
            gram[:,j,i]=g.conj()
    assert all(np.linalg.eigvalsh(g).min()>-1e-13 for g in gram)
    np.save(HERE/'gram.npy',gram)
if __name__=='__main__': run()
