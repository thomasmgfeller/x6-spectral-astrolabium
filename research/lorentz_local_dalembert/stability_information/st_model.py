"""Count Jacobian and exact-moment weight sensitivity in a fixed Lorentz gauge.
No truth coordinates, original A cloud or field values enter the search.
SPDX-License-Identifier: Apache-2.0
"""
import numpy as np
from st_common import Alternative,ETA,four

class Stability(Alternative):
    def __init__(self,p,counts,C,rho,cfg):
        super().__init__(p,counts,C,rho,cfg,'full_gls')
        self.C=.95*np.asarray(C)[np.ix_(self.mask,self.mask)]+.05*np.diag(self.counts)
        self.L=np.linalg.cholesky(self.C)
        self.ns=self.n-5
        self.H=np.eye(self.ns)+np.ones((self.ns,self.ns))
        self.target=np.array([0,0,0,-2,2,2,0,0,0.])
        self.dy=np.zeros((self.ns,3,len(self.indices)))
        for k,index in enumerate(self.indices):
            node,axis=divmod(int(index),3)
            if node==4:self.dy[:,axis,k]=-1
            elif node>=5:self.dy[node-5,axis,k]=1

    def means(self,x):
        s,ds,_=self.interval(x,self.a,self.b);q=-s
        if np.any(q<=0):raise ValueError('non-timelike measured interval')
        return self.factor*q**1.5,-1.5*self.factor*np.sqrt(q)[:,None]*ds

    def weights(self,x,derivative=True):
        z=self.unpack(x);y=z[5:]-z[4];t,u,v=y.T
        D=np.array([t,u,v,t*t,u*u,v*v,t*u,t*v,u*v])
        K=np.block([[self.H,D.T],[D,np.zeros((9,9))]])
        solution=np.linalg.solve(K,np.r_[np.zeros(self.ns),self.target]);a=solution[:self.ns]
        scale=self.packet['scale'];w=np.r_[-a.sum(),a]/scale**2
        if not derivative:return w
        dD=np.empty((9,self.ns,len(x)));dD[:3]=self.dy.transpose(1,0,2)
        for axis in range(3):dD[3+axis]=2*y[:,axis,None]*self.dy[:,axis]
        for row,(i,j) in enumerate([(0,1),(0,2),(1,2)],6):dD[row]=y[:,i,None]*self.dy[:,j]+y[:,j,None]*self.dy[:,i]
        rhs=np.vstack((-np.einsum('ink,i->nk',dD,solution[self.ns:]),-np.einsum('ink,n->ik',dD,a)))
        da=np.linalg.solve(K,rhs)[:self.ns]
        W=np.vstack((-da.sum(axis=0),da))/scale**2
        return w,W

    def gate(self,x):
        z=self.unpack(x);nodes=self.packet['landmarks']+[self.packet['root']]+self.packet['support']
        lookup={a:i for i,a in enumerate(nodes)};pairs=np.array([[lookup[a],lookup[b]] for a,b in self.packet['pairs']])
        q=-np.sum((z[pairs[:,1]]-z[pairs[:,0]])**2*ETA,axis=1)
        result=four(q,self.packet)
        if not result['qualified']:raise ValueError('reconstructed order')
        if self.constraints(x)[0].min() < -1e-10:raise ValueError('full order margin')
        return result
