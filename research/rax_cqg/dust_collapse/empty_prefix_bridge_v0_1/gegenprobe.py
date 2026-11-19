"""Independent floating-point check using full Gaussian matrices and direct quadratures."""
from collections import Counter
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent
B=np.sqrt(8/3)
D=1/8


def verify(ok, message):
    if not ok:
        raise ValueError(message)


def modes(h, diagonal, amplitude):
    # Accretive Gaussian matrix. The inner undamped coordinate is its Abel limit.
    matrix=np.diag(diagonal)-1j*B*h
    detroot=np.prod(np.sqrt(np.linalg.eigvals(matrix)))
    inverse=np.linalg.inv(matrix)
    s=np.zeros(len(h))
    a=np.zeros(len(h))
    s[-2:]=[1,1]
    a[-2:]=[1,-1]
    return amplitude/detroot*np.array([1,(s@inverse@s-1)/np.sqrt(2),(a@inverse@a-1)/np.sqrt(2)])


def coefficients():
    histories=json.loads((ROOT/'quellen/aa_hessians.json').read_bytes())['histories']
    from fractions import Fraction
    vacuum=np.zeros(3,complex)
    groups=np.zeros((2,3),complex)
    restrictions=Counter()
    for row in histories:
        code=row['order_code']
        edges=tuple((i,j-1) for i in (0,1) for j in (3,4) if code & 1<<(5*i+j))
        restrictions[edges]+=1
        mat=np.array([[float(Fraction(x)) for x in line] for line in row['H0_over_va']])
        amplitude=4*np.pi*np.sqrt(2*np.pi)*np.exp(1j*row['F4'])/264
        groups[row['p']-1]+=modes(mat,[1,1,0,1,1],amplitude)
    for edges,n in restrictions.items():
        h=np.zeros((4,4))
        for i,j in edges:
            e=np.eye(4)[i]-np.eye(4)[j]
            h-=np.outer(e,e)/2
        vacuum+=modes(h,[1,1,1,1],4*np.pi*n/(8*33)*np.exp(1j*(4-len(edges))))
    return vacuum,groups


def clock(u,y,wy):
    v=B*(y-u)**2
    def averaged(phase):
        return (1+np.exp(-0.5j*phase)*np.sinc(phase/(2*np.pi)))/2
    return np.array([wy@averaged(.5+v),wy@averaged(.5+v[:,None]+v)@wy])


def evaluate(order, data):
    vacuum,groups=coefficients()
    y,wy=leggauss(order)
    y,wy=(y+1)/2,wy/2
    for regulator in (1,4):
        result=data['cases'][str(regulator)]
        weights=2*np.pi*np.sqrt(1+B**2)/81*np.array([
            4*np.sqrt(9/12871), np.sqrt(9/1423450)+2*np.sqrt(1370/(841*regulator**2+529))*np.sqrt(9/69185)])
        rem=1-np.vdot(vacuum,vacuum).real
        g0=np.r_[vacuum,np.sqrt(rem),0,0]
        basis=np.column_stack([groups,np.zeros(2),np.diag(np.sqrt(rem*weights))])
        intervals=[]
        covariance=np.zeros((6,6),complex)
        for lo,hi in ((0,1/24),(1/24,1/16),(1/16,D)):
            values=np.array([clock(lo+(hi-lo)*node,y,wy)@basis for node in y])
            weights_u=(hi-lo)*wy
            intervals.append(weights_u@values)
            covariance+=values.T@(weights_u[:,None]*values.conj())
        total=sum(intervals)
        verify(abs(np.vdot(g0,total)-complex(*result['vacuum_birth']))<1e-13,'mixed packet response')
        verify(abs(np.vdot(total,total)-result['relative_one_weight'])<1e-13,'one-birth weight')
        for split,c in [(1,'1/24'),(2,'1/16')]:
            left,right=sum(intervals[:split]),sum(intervals[split:])
            r=result['cuts'][c]
            for z,expected in [(np.vdot(left,right),complex(*r['LR'])),
                               (np.vdot(g0,left),complex(*r['0L'])),(np.vdot(g0,right),complex(*r['0R']))]:
                verify(abs(z-expected)<1e-13,'complex cut data')
        for name,beta in [('5/4',1.25),('4/3',4/3)]:
            kappa=(np.exp(-D)+beta-1)/(np.exp(-D)+(1-beta)*D)
            largest=np.linalg.eigvalsh(np.outer(g0,g0.conj())+covariance/kappa)[-1]
            eta=1/largest
            lo,hi=map(float,result['candidate_clocks'][name]['continuum_eta_bracket'])
            verify(lo<eta<hi,'independent complete-time threshold')
            print(f'Gauss {order:2d}  t={regulator}  beta={name}  eta_max={eta:.10f}')


if __name__=='__main__':
    data=json.loads((ROOT/'ergebnis.json').read_bytes())
    for order in (16,24):
        evaluate(order,data)
