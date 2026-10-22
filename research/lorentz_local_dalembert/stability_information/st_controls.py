"""Synthetic checks before diagnostic search. SPDX-License-Identifier: Apache-2.0"""
import numpy as np
from st_common import HERE,read,save
from st_model import Stability
from fit import canonical
from selection import pairs_for

def main():
    c=read(HERE/'contract.json');rng=np.random.default_rng(782091)
    anchors=np.array([[-8,0,0],[-10,1,0],[-12,0,1],[-15,.2,.3]])
    supports=np.column_stack((np.r_[-2.,2.,rng.uniform(-4,-1,9),rng.uniform(1,4,9)],rng.uniform(-.4,.4,(20,2))))
    z=canonical(np.vstack((anchors,np.zeros(3),supports)));d=z[None]-z[:,None];q=d[:,:,0]**2-d[:,:,1]**2-d[:,:,2]**2
    p=dict(root=4,support=list(range(5,len(z))),temporal=[5,6],landmarks=[0,1,2,3],scale=1.,pairs=pairs_for([0,1,2,3],4,list(range(5,len(z)))),full_order=(d[:,:,0]>0)&(q>0))
    n=20*np.pi/12*np.array([q[a,b] for a,b in p['pairs']])**1.5
    m=Stability(p,n,np.diag(n),20,c['fit']);x=m.pack(z);w,W=m.weights(x);mu,J=m.means(x)
    direction=rng.normal(size=len(x));direction/=np.linalg.norm(direction);h=1e-6
    checks=[]
    def check(name,ok,value):assert ok,name;checks.append(dict(name=name,passed=bool(ok),value=value))
    error=float(np.max(abs((m.weights(x+h*direction,False)-m.weights(x-h*direction,False))/(2*h)-W@direction))/(1+np.max(abs(W@direction))))
    check('weight_derivative_finite_difference',error<1e-6,error)
    error=float(np.max(abs((m.means(x+h*direction)[0]-m.means(x-h*direction)[0])/(2*h)-J@direction))/(1+np.max(abs(J@direction))))
    check('count_derivative_finite_difference',error<1e-7,error)
    error=float(np.max(abs(m.gate(x)['weights']-w)));check('Minkowski_and_landmark_weights_agree',error<1e-7,error)
    A=np.linalg.solve(m.L,J);U,s,Vt=np.linalg.svd(A,full_matrices=False);P=(Vt.T/s)@U.T
    check('count_Jacobian_full_gauge_rank',s[-1]>1e-9*s[0],dict(rows=len(mu),columns=len(x),minimum=float(s[-1])))
    G=W@P;_,g,V=np.linalg.svd(G,full_matrices=False);dx=P@V[0]
    check('linear_gain_direction_attains_bound',abs(np.linalg.norm(W@dx)-g[0])<1e-8,float(g[0]))
    check('constant_field_conservation',abs(w.sum())<1e-9 and np.max(abs(W.sum(axis=0)))<1e-8,float(abs(w.sum())))
    save(HERE/'controls.json',dict(status='PASS',checks=checks,scope='Exact-mean synthetic fixture; not experimental Poisson data.'))
    print('PASS',len(checks),'synthetic controls')

if __name__=='__main__':main()
