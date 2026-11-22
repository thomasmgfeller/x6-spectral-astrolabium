"""Uniform finite exclusion, origin obstruction and propagation of calibration errors."""
from fractions import Fraction as Q
from math import comb,isqrt
from pathlib import Path
import json
from intervalle import I,S
from nullgrenze import polynomial,EDGES,PAST,INNER,FUTURE,ORDER,V
from auslese import settings

ROOT=Path(__file__).resolve().parent
GAIN=sum(abs(w) for _,w in settings().values())

def normalization():
    # Positive-tube normalization after removal of its common M^7 factor.
    root=isqrt(isqrt(3*S**4//722));delta=I(root,root+1)
    poly=I.of(0)
    for k,coef in polynomial():
        if any(j%2 for j in k):continue
        for j in k:coef=coef/(j+1)
        poly=poly+coef
    norm=I.of(0)
    for centre in (Q(-1,16),Q(1,16)):
        c=4*delta-centre
        for j in range(0,15,2):
            norm=norm+c**(14-j)*Q(comb(14,j),2*(j+1)*32**j)
    return norm*poly

def single_history_coefficients():
    # The zeroth/linear clock terms of the unwrapped phase stencil cancel.
    st=settings()
    assert sum(w for _,w in st.values())==0
    assert [sum(w*z[k] for z,w in st.values()) for k in range(5)]==[0,0,0,0,1]
    coeff={j:Q({7:-127,8:240,9:-120}.get(j,0)) for j in ORDER}
    for (a,b,u,v,_),weight in st.values():
        shift={j:u+v*V[j] for j in PAST}
        shift.update({11:a,13:b})
        for (i,j),layer in EDGES.items():
            coeff[j]-=Q(layer,38)*weight*(shift.get(j,0)-shift.get(i,0))**2
    assert all(coeff[j]==int(j in INNER) for j in ORDER)
    return {str(k):int(v) for k,v in coeff.items()}

def certify(rows,cal):
    g=Q(cal['gain']);b=Q(cal['offset'])
    norm_hi=Q(normalization().hi,S)
    bound=Q(134)
    # For real shifts |Y_i-Y_j|<11, D<6/5, sum |b_ij|<=34, sum f=1.
    assert Q(6,5)*Q(101,100)*(1+Q(34*11**2,19))/2 < bound
    out={}
    for rho in ('1/8','1/4'):
        r=rows[rho+'|limit']
        lo,hi=map(Q,r['mass_interval']);alo,ahi=map(Q,rows[rho+'|empty']['mass_interval'])
        assert hi<alo<0
        c=Q(r['unnormalized_modulus_floor'])/norm_hi
        residual=g*(hi-b)
        assert c>0 and residual<0
        # Choose a conservative power of two by a deterministic rule.
        k=0
        while True:
            m=Q(1,2**k)
            if m*bound<c/8 and residual+(2*g*GAIN*bound/c)*m<0:break
            k+=1
        out[rho]={'calibrated_limit_bounds':[str(g*(lo-b)),str(residual)],
              'atom_minus_limit_bounds':[str(alo-hi),str(ahi-lo)],
              'strictly_negative_for_all_positive_m_up_to_power_minus':k,
              'normalized_limit_floor':str(Q((10**8*c).__floor__(),10**8))}
    left=Q(rows['1/8|limit']['mass_interval'][0]);right=Q(rows['1/4|limit']['mass_interval'][1])
    assert left>right
    return {'centres':out,'lower_bound_on_minimax_raw_intercept_error':str((left-right)/2),
            'fine_density_coefficients':single_history_coefficients(),'full_vacuum_raw':0,'full_vacuum_after_calibration':str(-g*b),'variation_per_unit_mass':str(bound)}

def noise(transfer,cal):
    g=float(cal['gain']);b=float(cal['offset']);level=cal['levels']['5x10'];distance=level['quarter']-level['empty']
    out={}
    for k,row in transfer.items():
        centre,sector,m=k.split('|')
        if sector!='positive':continue
        mass=float(Q(m));value=row['raw'];est=row['calibrated']
        # Independent phase error budgets on the target, the standard and the zero control.
        unrounded=.25*(value-level['empty'])/distance
        rounding=abs(unrounded-est)
        margin=.02*mass-abs(est-mass)-rounding
        if margin<=0:continue
        out[k]={'sufficient_phase_accuracy_fixed_calibration_rad':margin/(g*float(GAIN)),
                'sufficient_phase_accuracy_three_readouts_rad':margin*distance/(2*float(GAIN)*(.25+abs(unrounded)+margin))}
    return out

if __name__=='__main__':
    def inp(name):return json.loads((ROOT/name).read_bytes())
    print(json.dumps({'exact':certify(inp('nullgrenze.json'),inp('eichung.json')),
                      'projected_noise':noise(inp('transfer.json'),inp('eichung.json'))},sort_keys=True,indent=2))
