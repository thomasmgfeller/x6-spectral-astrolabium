"""Extend the published three-bin Gram table, verifying the N15 Gaussian states independently."""
from unittest.mock import patch
import sys
import json
import numpy as np
import mpmath as mp
from model import ROOT, CACHE, layout, geometry, write
sys.path.insert(0,str(CACHE/'study'))
import common
from abel_check import numerical_state

def names_and_reach():
    names,reach=common.setup()
    c=json.loads((ROOT/'catalog.json').read_text())
    pilot=sorted(map(int,c['cheap_orders']))
    for i,r in enumerate(('chain','one')):
        reach[i]+= [len(names)+k for k,m in enumerate(pilot) if str(m) in c['roots'][r]['ends']]
    return names+[f'N15_{m}' for m in pilot],reach

def build():
    names,_=names_and_reach(); old=np.load(CACHE/'study/gram.npy')
    n=old.shape[1];g=np.empty((3,len(names),len(names)),complex)
    g[:,:n,:n]=old
    mp.mp.dps=70
    abel=[];states=[]
    with patch.object(geometry,'order',layout):
        for i,name in enumerate(names):
            key=common.prior.key(name)
            info,state=geometry.kernel(key)
            assert info['status']=='ADMISSIBLE'
            if i>=n:
                prec,phase=numerical_state(key,mp.mpf('1e-28'))
                err=max(max(abs(x) for x in prec-state[0]),abs(phase-state[1]/abs(state[1])))
                assert err<mp.mpf('1e-17'),(name,err)
                abel.append(float(err))
            states.append(state)
    for j in range(n,len(names)):
        rr,rb=states[j]
        for i,(ll,lb) in enumerate(states[:j+1]):
            h=ll.conjugate()+rr
            root=geometry.continued_sqrt(h)
            overlap=mp.conj(lb)*rb*(2*mp.pi)**mp.mpf('1.5')/root
            if i==j: assert abs(overlap-1)<mp.mpf('1e-45')
            central=overlap*mp.erf(1/mp.sqrt(2*(1+(h**-1)[0,0])))
            vals=np.array([complex((overlap-central)/2),complex(central),complex((overlap-central)/2)])
            if i==j:vals=vals.real
            g[:,i,j]=vals;g[:,j,i]=vals.conj()
    assert np.array_equal(g,g.swapaxes(1,2).conj())
    np.save(ROOT/'gram.npy',g)
    write('scalar_checks.json',{'N15':names[n:],'abel_max_errors':abel,'dps':mp.mp.dps})
if __name__=='__main__':build()
