"""Exact independence of scalar outputs and nonzero charge sectors in the H3 reference."""
import json
import sys
from fractions import Fraction as F
import numpy as np
import sympy as sp
from model import BASE,combined_laws,edges,I,P,F as FUTURE
from tube import template
from coherence import phase_box
from support import geometry,WINDOWS,DELTA

def gaussian_key(code):
    # Eliminate hidden variables only after adding the inherited Gaussian input.
    # The two external gauge coordinates are included as in the original H3 chart.
    b=edges(code).astype(int)
    h=sp.Matrix((b+b.T-np.diag(b.sum(0)+b.sum(1))).tolist())/2
    e=sp.zeros(15)
    e[1:4,:3]=sp.eye(3);e[7:10,3:6]=sp.eye(3)
    for j,v in enumerate(I): e[int(v),6+j]=1
    am=sp.Matrix([-128,241,119,-232]);ap=sp.Matrix([-232,119,241,-128])
    bm=sp.Matrix([-46,-32,-16,0]);bp=sp.Matrix([0,16,32,46])
    e[:4,-2]=bm;e[7:11,-1]=bp
    g=e.T*h*e
    g[-2,:3]-=am[1:,:].T;g[:3,-2]-=am[1:,:]
    g[-1,3:6]+=ap[:3,:].T;g[3:6,-1]+=ap[:3,:]
    g[-2,-2]-=am.dot(bm);g[-1,-1]+=ap.dot(bp)
    hidden=[0,1,2,*range(6,15)]
    block=(g[hidden,hidden]+sp.I*sp.diag(1,1,1,*([0]*9))).to_DM().convert_to(sp.QQ_I)
    cross=g[hidden,[3,4,5]].to_DM().convert_to(sp.QQ_I)
    piv=list(block.rref()[1])
    selected=cross.extract(piv,[0,1,2])
    sol,den=block.extract(piv,piv).solve_den(selected)
    assert block.extract(list(range(12)),piv)*sol==cross.scalarmul(den)
    eff=g[[3,4,5],[3,4,5]].to_DM().convert_to(sp.QQ_I)-(selected.transpose()*sol).scalarmul(1/den)
    omega=eff.scalarmul(sp.QQ_I(0,-1)).to_Matrix()
    assert omega==omega.T and omega.applyfunc(sp.re).is_positive_definite
    return [str(omega[i,j]) for i in range(3) for j in range(i,3)]

def phase_witness(code):
    _,c,r,_,lo,hi=template(code)
    profile={'clock_center':{str(v):str(val) for v,val in c.items()},'clock_halfwidth':str(r),
             'dwell_affine_ranges_per_vertex':{str(v):list(map(str,z)) for v,z in zip(I,zip(lo,hi))}}
    _,rel=geometry(code)
    lower={}
    for m in (F(1,4),F(1),F(4)):
        for rho in (F(1,8),F(1,4)):
            pts=[]
            left_margin=F(0)
            for a,b in WINDOWS:
                h=(b-a)/8
                boxes=[phase_box(rel,(a+j*h,a+(j+1)*h),rho,m,profile) for j in range(8)]
                pts.extend(boxes)
                if a<0:
                    width_left=max(x[1] for x in boxes)-min(x[0] for x in boxes)
                    c_left=1-width_left**2/8
                    # These sign-certified types have full tubes on both lobes. The
                    # auxiliary tube volume at fixed offset is proportional to D^14.
                    ratio=(1-F(1,8)/(4*DELTA[1]+F(3,32)))**14
                    left_margin=(c_left-ratio)/(1+ratio)
            width=max(x[1] for x in pts)-min(x[0] for x in pts)
            lower[str(m)+'/'+str(rho)]=str(max(F(0),1-width*width/8,left_margin))
    return lower
def run():
    keys,_=combined_laws()
    shapes={str(k):gaussian_key(k) for k in keys}
    distinct=len(set(tuple(vals) for vals in shapes.values()))
    assert distinct==len(keys)
    bins=json.loads((BASE/'inputs/sync/census.json').read_text())['by_type']
    proofs={}
    for sign in ('++','--'):
        for k in keys:
            if bins[str(k)].get('signs')!=sign: continue
            v=phase_witness(k)
            if all(F(x)>0 for x in v.values()):
                proofs[sign]={'type':k,'phase_modulus_lower':v};break
    return {'distinct_exact_scalar_shapes':distinct,'by_type':shapes,'witnesses':proofs}
if __name__=='__main__': print(json.dumps(run(),sort_keys=True))
