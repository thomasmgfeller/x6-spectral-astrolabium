"""Eigenständige Kontrolle. Volle Wirkungen aus Ordnungsrelationen, ohne Schur-Blöcke der Hauptrechnung."""
import json
import math
from pathlib import Path
from collections import Counter

import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT/'ergebnis.json').read_text())
B=4/math.sqrt(6)


def check(x,y,tol,name):
    if abs(x-y)>tol: raise ArithmeticError(f'{name}: {x} gegen {y}')


def time_factor(p,d):
    nodes,w=leggauss(25)
    nodes,w=(nodes+1)/2,w/2
    def chi(k):
        return (1+np.exp(-.5j*k)*np.sinc(k/(2*np.pi)))/2
    result=0j
    for u,wu in zip(d*nodes,w):
        delta=B*(nodes-u)**2
        if p==1:
            result+=wu*(w@chi(.5+delta))
        else:
            result+=wu*(w@chi(.5+delta[:,None]+delta[None,:])@w)
    return result*d


def geometry(rel,n):
    h=np.zeros((n,n))
    grav=n
    for i,j in rel:
        inside=sum((i,k) in rel and (k,j) in rel for k in range(n))
        coefficient=(1,-9,16,-8)[inside] if inside<4 else 0
        vec=np.eye(n)[i]-np.eye(n)[j]
        h-=coefficient*np.outer(vec,vec)/2
        grav-=coefficient
    return h,grav


def rows():
    hist=json.loads((ROOT.parent/'amplitude_existence_v0_1/inputs/aa_hessians.json').read_text())['histories']
    d=1/8
    time={p:time_factor(p,d) for p in (1,2)}
    small=Counter()
    all_rows=[]
    for item in hist:
        rel=frozenset((i,j) for i in range(5) for j in range(i+1,5) if item['order_code'] & (1<<(5*i+j)))
        small[frozenset((i,j-1) for i,j in rel if i in (0,1) and j in (3,4))]+=1
        h,f=geometry(rel,5)
        all_rows.append((1,h,np.exp(1j*f)*time[item['p']]/(33*8)))
    for rel,n in small.items():
        h,f=geometry(rel,4)
        all_rows.append((0,h,np.exp(1j*f)*n/(33*8)))
    return all_rows


def continuous_root(mat):
    ev=np.linalg.eigvals(mat)
    if min(ev.real) < -1e-9 or min(abs(ev))<1e-12:
        raise ArithmeticError('ungeklärter Wurzelzweig')
    return np.prod(np.sqrt(ev))


def packet_check(items):
    modes=np.zeros((2,3),dtype=complex)
    amplitudes=[]
    zlist=[]
    for sector,h,pref in items:
        n=len(h)
        damp=np.array([1,1]+[0]*(n-4)+[1,1])
        mat=np.diag(damp)-1j*B*h
        base=pref*(2*np.pi)**(n/2)/(np.pi*continuous_root(mat))
        even=[]
        for sign in (1,-1):
            v=np.array([0]*(n-2)+[1,sign])
            even.append(v@np.linalg.solve(mat,v)-1)
        modes[sector]+=base*np.array([1,even[0]/np.sqrt(2),even[1]/np.sqrt(2)])
        if sector==0:
            amplitudes.append(base)
            zlist.append(even[1])
    for i in (0,1):
        for j,z in enumerate(modes[i]):
            check(z,complex(*map(float,REF['packet_amplitudes'][str(i)][j])),1e-11,'Randpaket')
    # Direct iteration of all seven original complex terms; cumulative weights are monotone.
    c=np.array(amplitudes); z=np.array(zlist)
    total=0.
    for k in range(2238):
        total+=abs(c.sum())**2
        if k in (2236,2237):
            lo,hi=map(float,REF['bessel']['axial_partial_sums'][str(k)])
            check(total,(lo+hi)/2,2e-12,'Bessel-Summe')
        c*=z*np.sqrt((2*k+1)/(2*k+2))
    return modes


def direct_matrix(items,t,eps):
    # Independent block integral over BOTH incoming copies, their inner fields and shared y.
    out=np.zeros((2,2),dtype=complex)
    w=np.array([[(t+1/t)/2,(t-1/t)/2],[(t-1/t)/2,(t+1/t)/2]])
    for p,h,left in items:
        for q,g,right in items:
            n=len(h)+len(g)-2
            seam=[n-2,n-1]
            li=list(range(len(h)-2))+seam
            ri=list(range(len(h)-2,n-2))+seam
            mat=np.zeros((n,n),dtype=complex)
            mat[np.ix_(li,li)]+=1j*B*h
            mat[np.ix_(ri,ri)]-=1j*B*g
            for v in li[:2]+ri[:2]:
                mat[v,v]+=1
            mat[np.ix_(seam,seam)]+=2*eps*w
            out[p,q]+=left.conjugate()*right*(2*np.pi)**(n/2)/(np.pi*continuous_root(mat))
    return out


def main():
    items=rows()
    packet_check(items)
    worst=0.
    for t in (1,4):
        for eps in (4.,.001):
            x=direct_matrix(items,t,eps)
            r=REF['finite_regulator_grams'][str(t)][str(eps)]
            c=complex(*map(float,r['cross']))
            target=np.array([[float(r['zero']),c],[c.conjugate(),float(r['one'])]])
            error=float(np.max(abs(x-target)))
            worst=max(worst,error)
            check(error,0,6e-11,'direkte volle Grammatrix')
    print('Sechs Paketwerte, zwei Bessel-Summen und vier volle Gram-Matrizen geprüft.')
    print(f'Grösste Abweichung bei den 6.400 Paarintegralen nach Summation: {worst:.3g}')


if __name__=='__main__':
    main()
