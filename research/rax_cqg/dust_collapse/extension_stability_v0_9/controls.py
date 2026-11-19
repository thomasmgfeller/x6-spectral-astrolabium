"""Independent Cartesian sums and direct four-outcome checks for all new clocks."""
from tempfile import TemporaryDirectory
from unittest.mock import patch
from reference import ROOT, full, net, layout, tails, save_json
from bounds import NEW, GRIDS, inputs
from coupled import fork, chain, CHAIN, FORK, build_nested
from pilot import direct
import numpy as np

def cartesian(mask,n,m):
    nodes, weights = net.quadrature(m)
    value = np.zeros(2,complex)
    for s in (-1,1):
        for u,w in zip(nodes,weights):
            p,z=direct((7,mask),-2*net.STEP+s/16+u/32,n)
            value+=w*z*np.sinc(p/(64*np.pi))*np.exp(-.5j*p*np.array(net.RHO))/np.sqrt(3072)
    return value

def calculate():
    small = {}
    with TemporaryDirectory() as tmp, patch.object(tails.prior.growth,"layout",layout):
        lib = build_nested(tmp)
        for mask in NEW:
            if mask==FORK:
                test = fork(5,4)
            elif mask==CHAIN:
                test = chain(5,4,lib)
            else:
                test = tails.packet((7,mask),5,4,lib)
            error = float(max(abs(test-cartesian(mask,5,4))))
            if error>=1e-13:
                raise ValueError(("Direct five-node control",mask,error))
            small[str(mask)] = error
    data={}
    for tag in GRIDS:
        names,reach,B,cols,known,_,_ = inputs(tag)
        data[tag]={}
        for mask in NEW:
            j=names.index("N15_"+str(mask))
            if not all(j in r for r in reach):
                raise ValueError("Unreachable test")
            effects = np.empty((3,3,3),complex)
            effects[:,:2,:2] = B
            col = np.array([[complex(*v) for v in rr] for rr in cols[j]])
            effects[:,:2,2]=col[:,:2]
            effects[:,2,:2]=col[:,:2].conj()
            effects[:,2,2]=col[:,2].real
            def read(state):
                bins=np.einsum('i,kij,j->k',state.conj(),effects,state)
                if max(abs(bins.imag))>1e-16:
                    raise ArithmeticError("Nonreal probability")
                return np.r_[bins.real,1-sum(bins.real)]
            refs=[]; obs=[]
            for d in (0,1):
                b=np.array([complex(*known[k][d])/2 for k in (0,1)]+[0j])
                x=.95*b
                x[-1]=.05*complex(*known[j][d])
                refs.append(read(b)); obs.append(read(x))
            refs,obs=np.array(refs),np.array(obs)
            level=.5*abs(obs-refs).sum(axis=1)/refs[:,:3].sum(axis=1)
            dr=refs[1]-refs[0]
            contrast=sum(abs(obs[1]-obs[0]-dr))/sum(abs(dr))
            diff=sum(obs[1,:3]-obs[0,:3])
            if max(level)>.1 or contrast>.25 or diff>=0:
                raise ArithmeticError((tag,mask))
            data[tag][str(mask)]={"relative_level":level.tolist(),
                "relative_contrast":float(contrast),"success_difference":float(diff)}
    return {"cartesian_5_4":small,"direct_tests_at_five":data}

if __name__=="__main__":
    save_json(ROOT/"controls.json", calculate())
