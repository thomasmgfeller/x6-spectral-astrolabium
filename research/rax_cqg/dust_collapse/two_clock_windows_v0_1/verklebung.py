"""Minimal verklebte AA-Paare, voller linker Dichtemittelwert, rechte Uhr und Dichte als Record."""
import argparse
import cmath
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from schnitt import ROOT, bounds, check_sources
from extended_sewing_v0_1 import sewing

B=math.sqrt(8/3)
OUTER=(0,1,6,7)
OTHER=(0,1,3,4)


def relation(code):
    return {(i,j) for i in range(5) for j in range(i+1,5) if code & 1<<(5*i+j)}


def integer_det(rows):
    """Bruchfreie Elimination mit Zeilenpivot."""
    a=[list(row) for row in rows]
    prev=sign=1
    for k in range(len(a)-1):
        p=next((i for i in range(k,len(a)) if a[i][k]),None)
        if p is None:
            return 0
        if p!=k:
            a[k],a[p]=a[p],a[k]
            sign=-sign
        pivot=a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])//prev
        prev=pivot
    return sign*a[-1][-1]


def determinant_squared(h):
    # det[D-i sqrt(2/3) H] = re + i sqrt(2/3) im for integer H.
    re=im=F(0)
    for n in range(5):
        power=8-n
        coeff=F(2,3)**(power//2) * (1,-1,-1,1)[power%4]
        for fixed in combinations(OUTER,n):
            remaining=[i for i in range(8) if i not in fixed]
            minor=integer_det([[h[i][j] for j in remaining] for i in remaining])
            if power%2: im+=coeff*minor
            else: re+=coeff*minor
    return re*re+F(2,3)*im*im


def amplitude(h, grav, det2):
    diag=np.diag([1 if i in OUTER else 0 for i in range(8)])
    m=diag.astype(complex)-.5j*B*np.asarray(h)
    idx=[0,1,6,7,2,3,4,5]
    m=m[np.ix_(idx,idx)]
    detroot=1+0j
    for k in range(8):
        pivot=m[k,k]
        if abs(pivot)<1e-12 or (pivot.real<0 and abs(pivot.imag)<1e-12):
            raise ArithmeticError('Wurzelzweig')
        detroot*=cmath.sqrt(pivot)
        m[k+1:,k+1:]-=np.outer(m[k+1:,k],m[k,k+1:])/pivot
    if not math.isclose(abs(detroot)**4,float(det2),rel_tol=3e-12):
        raise ArithmeticError('Determinantennorm')
    return math.pi**3/8*cmath.exp(1j*grav)/detroot/1089


@lru_cache(maxsize=None)
def reciprocal_fourth_root(d):
    lo,hi=bounds.root(d)
    return 1/bounds.root(hi)[1],1/bounds.root(lo)[0]


def geometry():
    names=sorted(h['order_code'] for h in json.loads((ROOT.parent/'amplitude_existence_v0_1/inputs/aa_hessians.json').read_text())['histories'])
    left=[sewing.make_packet('left',range(5),relation(code),[3,4],[0,1]) for code in names]
    right=[sewing.make_packet('right',range(3,8),{(i+3,j+3) for i,j in relation(code)},[3,4],[6,7]) for code in names]
    bin_weights=defaultdict(list)
    counts=Counter()
    detcounts=Counter()
    examples={}
    for i,p in enumerate(left):
        for j,q in enumerate(right):
            a=sewing.sew_packets(p,q)['joint_action']
            coeff={(l,k):c for l,k,c in a['pair_terms']}
            cross=coeff.get((2,5),0)
            signature=(cross,tuple(sorted((coeff.get((k,2),0),coeff.get((k,5),0)) for k in OTHER)))
            h=sewing.doubled_hessian(a)
            det2=determinant_squared(h)
            if det2<=0: raise ArithmeticError('singuläre volle Matrix')
            bin_weights[signature].append(amplitude(h,a['F4'],det2))
            counts[cross]+=1
            detcounts[det2]+=1
            examples.setdefault(cross,[names[i],names[j]])
    groups={k:complex(math.fsum(z.real for z in v),math.fsum(z.imag for z in v)) for k,v in bin_weights.items()}
    total=sum(groups.values())
    prior=json.loads((ROOT.parent/'extended_sewing_v0_1/results/verification.json').read_text())['full_1089_sum_all_atom']['0']
    if abs(total-complex(float(prior['real']),float(prior['imag'])))>float(prior['absolute_component_error_bound']):
        raise ArithmeticError('Acht-Atom-Kontrollwert')
    invsum=(F(0),F(0))
    for d,n in detcounts.items():
        invsum=bounds.plus(invsum,bounds.scale(n,reciprocal_fourth_root(d)))
    c=bounds.scale(F(1,2*1089),bounds.times(invsum,bounds.times(bounds.PI,bounds.times(bounds.PI,bounds.PI))))
    diagnostic=dict(pairs=sum(counts.values()),coefficient_counts=dict(sorted(counts.items())),
                    first_examples=examples,signatures=len(groups),
                    four_times_sum_absolute_amplitudes=bounds.decimal_bounds(c,12),
                    small_window_upper_coefficient=bounds.decimal_bounds(bounds.square(c),12))
    return groups,diagnostic


def quadrature(n):
    x,w=leggauss(n)
    return (1+x)/2,w/2


def calculate_grid(groups,n,cut):
    x,weight=quadrature(n)
    # Rows are u=0, then both subwindow grids, then the independent full window grid.
    d=1/8
    u=np.r_[0,cut*x,cut+(d-cut)*x,d*x]
    mark=np.r_[0,x]
    wm=np.r_[.5,weight/2]
    uw=np.exp(-1j*B*mark[None,:,None]*(u[:,None,None]-x[None,None,:])**2)*weight
    zeros=np.ones_like(uw)*weight
    mark_mean=wm*np.exp(-.5j*mark)
    result=np.empty((len(u),len(mark),n),complex)
    channels={(a,c) for _,signature in groups for a,c in signature}
    for j,r in enumerate(mark):
        phases={c:np.exp(-1j*B*c*r*(x[:,None]-x[None,:])**2) for _,c in channels}
        avg={}
        for a,c in channels:
            if a not in (0,1): raise ValueError('lokales Elterngewicht')
            avg[a,c]=(uw if a else zeros) @ phases[c].T
        direct={c:np.exp(-1j*B*c*r*(u[:,None]-x[None,:])**2) for c,_ in groups}
        responses=np.zeros((len(u),n),complex)
        for (cross,sig),am in groups.items():
            prod=avg[sig[0]]*avg[sig[1]]*avg[sig[2]]*avg[sig[3]]
            responses+=am*direct[cross]*np.einsum('uwv,w->uv',prod,mark_mean)
        result[:,j,:]=4*np.exp(-.5j*r)*responses
    record_weights=wm[:,None]*weight
    def scalar(a,b):
        return np.sum(a.conjugate()*b*record_weights)
    early=cut*np.einsum('u,urv->rv',weight,result[1:n+1])
    late=(d-cut)*np.einsum('u,urv->rv',weight,result[n+1:2*n+1])
    whole=d*np.einsum('u,urv->rv',weight,result[2*n+1:])
    if np.max(abs(whole-early-late))>5e-14: raise ArithmeticError('Zeitfensterbilanz')
    ll=scalar(early,early).real
    rr=scalar(late,late).real
    lr=scalar(early,late)
    total=scalar(whole,whole).real
    basic=dict(left=ll,right=rr,real_cross=lr.real,imag_cross=lr.imag,total=total,
               interference_share=2*lr.real/total,normalized_overlap_squared=abs(lr)**2/(ll*rr),
               initial_amplitude_norm_squared=scalar(result[0],result[0]).real,
               initial_right_density_atom_contribution=.5*abs(result[0,0,0])**2)
    for p in (1,2):
        amp=sum(am for (_,sig),am in groups.items() if sum(a for a,c in sig)==p)
        basic[f'parent_group_{p}_real']=amp.real
        basic[f'parent_group_{p}_imag']=amp.imag
    return basic


def run():
    commit=check_sources()
    g,diag=geometry()
    evaluations={}
    for cut in (1/16,1/24):
        last=None
        for n in (30,40,50):
            vals=calculate_grid(g,n,cut)
            if last is not None and n==50:
                if any(not math.isclose(v,last[k],rel_tol=2e-9,abs_tol=2e-17) for k,v in vals.items()):
                    raise ArithmeticError('Quadraturverfeinerung')
            last=vals
        evaluations[str(F(cut).limit_denominator())]={k:format(v,'.12g') for k,v in vals.items()}
    return dict(commit=commit,geometry=diag,quadrature_orders=[30,40,50],readout='L2(dv dnu(r5)); w2 integrated; six remaining densities atomic',
                coherent_full_record=evaluations,physical_pairing='HOLD')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    opt=parser.parse_args()
    opt.out.write_text(json.dumps(run(),sort_keys=True,indent=2)+'\n')
