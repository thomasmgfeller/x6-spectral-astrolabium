"""Absolute x12 threshold, fixed input: equal phase, low early tag, no pulse."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from randtest import nodes, waves, a_segments, D, H, WINDOW, s

X = F(1,8)
EDGES_B = (F(3,4)-F(1,64), F(3,4)+F(1,64))
EDGES_V = (F(1,2)-F(1,64), F(1,2)+F(1,64))
# All changes in the b integration bounds occur at these differences b-v.
DIFF = tuple(2*X/k for k in (F(101,100), F(1), F(99,100)))

def split(lo, hi, breaks):
    edges = sorted({lo,hi} | {t for t in breaks if lo<t<hi})
    return zip(edges,edges[1:])

def grid(method,n):
    q,w = nodes(method,n)
    # Coordinates (a, u14, jitter13); the allowed x11 intersection is piecewise affine in a.
    A,C,J = np.meshgrid(q,q,q,indexing='ij')
    outer = np.einsum('i,j,k->ijk',w,w,w).ravel()
    tag = 255/2048
    for al,ar in a_segments(tag):
        a = (al+ar)/2 + (ar-al)/2*A.ravel()
        c = .875 + WINDOW*C.ravel()
        f13 = (c-a)/2
        x13 = f13*(1+J.ravel()/100)
        low = np.maximum(tag-H,.99*(a-.375)/2)
        high = np.minimum(tag+H,1.01*(a-.375)/2)
        base_weight = outer*(ar-al)/(2*WINDOW)*f13
        for vl,vr in split(*EDGES_V,[F(1,2)]+[b-d for b,d in product(EDGES_B,DIFF)]):
            for vn,vw in zip(q,w):
                v = float((vl+vr)/2)+float((vr-vl)/2)*vn
                for bl,br in split(*map(float,EDGES_B),[v+float(d) for d in DIFF]):
                    # Clenshaw-Curtis includes interval endpoints. The discrete decision
                    # is taken on the interval interior for the correct one-sided integrand.
                    f_mid = ((bl+br)/2-v)/2
                    support = 'L' if 1.01*f_mid<float(X) else 'H' if .99*f_mid>float(X) else 'both'
                    for bn,bw in zip(q,w):
                        b = (bl+br)/2+(br-bl)/2*bn
                        y = np.column_stack((np.full(len(a),v),a,np.full(len(a),b),x13,(high+low)/2,(high-low)/2))
                        weight = base_weight * float(vr-vl)*(br-bl)/(2*WINDOW)**2*vw*bw
                        yield y,weight,support, f_mid<float(X), (vl+vr)/2 < F(1,2)


def evaluate(method,n,pulse, action=True):
    q,w = nodes(method,n)
    z = .125+WINDOW*q[None,:,None]
    win = np.outer(w,w).ravel()
    blocks = []
    for y,weight,support,low_guess,v_low in grid(method,n):
        columns = np.zeros((len(y),2),complex)
        for arm in (-1,1):
            u = .25+arm*s+H*q[None,None,:]
            left,f,coeff,x13,c13 = waves(method,y,z,u,pulse,components=True)
            if not action:
                # Set the phase to one, retaining the early tag and every cell Jacobian.
                v = y[:,0,None,None]
                left = (y[:,5,None,None]/H)*((z+u)/2)*((.375-z)/2)*((v-u)/2)
                coeff = 0*coeff
                c13 = 0*c13
            lo,hi = .99*f,1.01*f
            pivot = np.clip(float(X),lo,hi)
            weight_and_phase = left*np.exp(1j*D*x13*c13)
            for k,(a,b) in enumerate(((lo,pivot),(pivot,hi))):
                hw = (b-a)/2
                term = 100*hw*np.exp(1j*D*(a+b)/2*coeff)*np.sinc(D*hw*coeff/np.pi)
                columns[:,k] += ((weight_and_phase*term).reshape(len(y),-1) @ win)/np.sqrt(2)
        amp = columns*np.sqrt(weight[:,None])
        blocks.append((amp,support,low_guess,v_low))
    vectors = np.vstack([entry[0] for entry in blocks])
    low,high = vectors.T
    norms = np.array([np.linalg.norm(low),np.linalg.norm(high)])
    low,high = low/norms[0],high/norms[1]
    cross = np.vdot(low,high)
    distance = np.linalg.norm(high - low*cross)
    hits = []
    exclusive = []
    early_low_weight = 0.
    for amp,support,low_guess,v_low in blocks:
        if v_low:
            early_low_weight += np.sum(abs(amp)**2)
        w = np.sum(np.abs(amp)**2,axis=0)/norms**2
        hits.append(w[0 if low_guess else 1]/2)
        exclusive.append(w[0]/2 if support=='L' else w[1]/2 if support=='H' else 0)
        if support!='both':
            assert w[1 if support=='L' else 0]<1e-22
    return {'two_bin_u11_low':float(early_low_weight/sum(norms**2)),
            'two_bin_x12_low_weight_fraction':float(norms[0]**2/sum(norms**2)),
            'normalized_overlap_abs':float(abs(cross)), 'optimal_equal_prior_success':float((1+distance)/2),
            'choose_bin_from_f_equal_prior_success':float(sum(hits)),
            'zero_error_conclusive_fraction_from_exclusive_support':float(sum(exclusive)),
            'raw_high_to_low_weight_ratio':float((norms[1]/norms[0])**2)}

def main():
    # Two completions with the same prefix through 12 and even the same absolute x12.
    x = F(1,8)
    factors = [(F(3,4)+sign*F(1,1024)-F(1,2))/2 for sign in (-1,1)]
    jitters = [x/f-1 for f in factors]
    assert jitters==[F(1,255),-F(1,257)] and all(abs(q)<F(1,100) for q in jitters)
    rows, errors = {}, {}
    for label, pulse, action in [('0',0,True),('minus',-1,True),('plus',1,True),('action_off',0,False)]:
        gauss = evaluate('gauss',4,pulse,action)
        cc = evaluate('cc',5,pulse,action)
        errors[label] = {k:abs(gauss[k]-cc[k]) for k in gauss}
        if max(errors[label].values())>2e-9:
            raise ArithmeticError(errors[label])
        rows[label] = gauss
    return {'absolute_threshold':str(X), 'prefix_jitter_witness':list(map(str,jitters)),
            'cut13_flat_reference':rows, 'two_quadrature_differences':errors,
            'pulse_difference':{k:rows['plus'][k]-rows['minus'][k] for k in (
                'two_bin_u11_low', 'two_bin_x12_low_weight_fraction')}}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
