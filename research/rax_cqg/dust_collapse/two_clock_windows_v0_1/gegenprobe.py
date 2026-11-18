"""Eigenwertprodukt, direkte Gesamtordnungen und zusammengesetzte Quadratur für den zweiten Schnitt."""
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from anfangsgrenze import direct_order

ROOT=Path(__file__).resolve().parent
B=math.sqrt(8/3)


def groups_from_spectrum():
    histories=json.loads((ROOT.parent/'amplitude_existence_v0_1/inputs/aa_hessians.json').read_text())['histories']
    result=defaultdict(complex)
    for left in histories:
        for right in histories:
            terms=direct_order(left['order_code'],right['order_code'])
            mat=np.diag([1.,1,0,0,0,0,1,1]).astype(complex)
            f=8
            for (i,j),c in terms.items():
                f-=c
                val=.5j*B*c
                mat[i,i]+=val
                mat[j,j]+=val
                mat[i,j]-=val
                mat[j,i]-=val
            ev=np.linalg.eigvals(mat)
            if min(ev.real)<-1e-10 or min(abs(ev))<1e-11:
                raise ArithmeticError('Gaußmatrix')
            amp=np.pi**3*np.exp(1j*f)/(8*1089*np.sqrt(ev).prod())
            tag=(terms.get((2,5),0),tuple(sorted((terms.get((j,2),0),terms.get((j,5),0)) for j in (0,1,3,4))))
            result[tag]+=amp
    return result


def grid(n, parts=1):
    x,w=leggauss(n)
    return (np.concatenate([(x+1+2*j)/(2*parts) for j in range(parts)]),
            np.tile(w/(2*parts),parts))


def gram(weights,cut):
    y,dy=grid(18,3)
    v,dv=grid(18,3)
    density,density_w=grid(13,3)
    rnodes=np.r_[0,density]
    rweights=np.r_[.5,density_w/2]
    x,dx=grid(13)
    u=np.r_[0,x*cut,cut+x*(1/8-cut)]
    intervals=np.zeros((3,len(u)))
    intervals[0,0]=1
    intervals[1,1:1+len(x)]=dx*cut
    intervals[2,1+len(x):]=dx*(1/8-cut)
    gram=np.zeros((3,3),complex)
    channels={pair for _,s in weights for pair in s}
    # Integrate the earlier density w in the outer sum; v is paired only at the end.
    common={a:np.exp(-1j*B*a*rnodes[:,None,None]*(u[None,:,None]-y[None,None,:])**2)*dy for a,_ in channels}
    for r,wr in zip(rnodes,rweights):
        tail={b:np.exp(-1j*B*b*r*(v[:,None]-y[None,:])**2) for _,b in channels}
        nodes={pair:common[pair[0]]@tail[pair[1]].T for pair in channels}
        record=np.zeros((len(rnodes),len(u),len(v)),complex)
        for (c,sig),value in weights.items():
            direct=np.exp(-1j*B*c*r*(u[:,None]-v[None,:])**2)
            all_factors=np.prod([nodes[pair] for pair in sig],axis=0)
            record+=value*all_factors*direct
        result=4*np.exp(-.5j*r)*np.einsum('w,wuv->uv',rweights*np.exp(-.5j*rnodes),record)
        rows=intervals@result
        gram+=wr*(rows.conjugate()*dv) @ rows.T
    return gram


def main():
    expected=json.loads((ROOT/'verklebung.json').read_text())
    certificate=json.loads((ROOT/'anfangsgrenze.json').read_text())
    if expected['geometry']['coefficient_counts']!=certificate['counts']:
        raise ArithmeticError('Abweichende Rekonstruktionen der Zwischenordnungen')
    groups=groups_from_spectrum()
    for p in (1,2):
        total=sum(z for (_,sig),z in groups.items() if sum(a for a,b in sig)==p)
        for val,pair in zip((total.real,total.imag),certificate['parent_sums'][str(p)]):
            if abs(val-sum(map(float,pair))/2)>1e-15:
                raise ArithmeticError('Elternamplitude ausserhalb der numerischen Kontrolltoleranz')
    for cut,key in ((1/16,'1/16'),(1/24,'1/24')):
        matrix=gram(groups,cut)
        ref=expected['coherent_full_record'][key]
        output={'initial_amplitude_norm_squared':matrix[0,0].real,'left':matrix[1,1].real,
                'right':matrix[2,2].real,'real_cross':matrix[1,2].real,'imag_cross':matrix[1,2].imag}
        for name,v in output.items():
            if not math.isclose(v,float(ref[name]),rel_tol=2e-8,abs_tol=1e-18):
                raise ValueError((name,v,ref[name]))
        share=2*matrix[1,2].real/matrix[1:,1:].sum().real
        print(f'Schnitt {key}, separat berechneter Interferenzanteil {share:.11f}')
    print('Beide Schnittmatrizen und die Anfangsnorm auf zusammengesetzter Quadratur bestätigt.')


if __name__=='__main__':
    main()
