"""Directed finite-sample upper bounds; floats only in separate audit/report code."""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json
import sys
from decision import DESIGN, thresholds

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'source/research'
sys.path.insert(0,str(SOURCE/'lorentz_de_sitter_variance'))
sys.path.insert(0,str(SOURCE/'single_order_v01'))
from moments import reference, wedge_bounds
from information import cross,delta

def down(x,scale):
    return (x.numerator*scale)//x.denominator

def up(x,scale):
    return -down(-x,scale)

def round_upper(x,scale=10**9):
    return Q(up(x,scale),scale)

def roots(x,scale=10**14):
    l=isqrt((x.numerator*scale*scale)//x.denominator)
    return Q(l,scale),Q(l+(l*l*x.denominator!=x.numerator*scale*scale),scale)

def parameter_bounds(h):
    pl,pu=reference.probability(h)
    wl,wu=wedge_bounds(h)
    fine=10**13
    pl,pu=Q(down(pl,fine),fine),Q(up(pu,fine),fine)
    wl,wu=Q(down(wl,fine),fine),Q(up(wu,fine),fine)
    vl,vu=wl-pu**2,wu-pl**2
    di=delta(h);zl,zu=cross(di,di)
    dl=1/((1+di[1])**4*zu)
    du=1/((1-di[1])**4*zl)
    return pl,pu,vl,vu,dl,du

def third_moment(pl,pu,dl,du,g):
    # Exact cell masses and outward rounded extrema. Sum on the full symmetric square.
    scale=10**9; g4=g**4
    plo,phi=down(pl,scale),up(pu,scale)
    dlow,dhigh=down(dl,scale),up(du,scale)
    total=mass=0
    for i in range(g):
        for j in range(g):
            lo=(i*j)**2+((g-i-1)*(g-j-1))**2
            hi=((i+1)*(j+1))**2+((g-i)*(g-j))**2
            upper=max(0,phi*g4-dlow*lo,dhigh*hi-plo*g4)
            cell=6*(i-j)**2+1
            total+=cell*upper**3
            mass+=cell
    if mass!=g4:raise ArithmeticError('cell masses')
    return round_upper(Q(dhigh*total,scale*g4*(scale*g4)**3),10**13)

def normal_tail(z):
    # Positive z; exact alternating Taylor lower integral. C=0.3989422 < 1/sqrt(2*pi).
    if z<0:raise ValueError('negative standardized distance')
    z=Q(down(min(z,Q(4)),10**5),10**5)
    term=z; integral=term
    for k in range(1,32):
        term*=-z*z*Q(2*k-1,2*k*(2*k+1))
        integral+=term
    c=Q(3989422,10**7)
    if not (2*Q(355,113)*c*c<1 and integral>=0):raise ArithmeticError('Taylor lower bound')
    return round_upper(Q(1,2)-c*integral,10**12)

def full_tail(n,gap,params,m3):
    pl,pu,vl,vu,dl,du=params
    if vl<=0 or pu>=Q(1,2):raise ArithmeticError('variance or monotonicity assumption')
    snlo,_=roots(Q(n)); siglo,_=roots(vl); _,sighi=roots(vu)
    beta3=m3/(vl*siglo)
    berry=Q(3328,10000)*(beta3+Q(429,1000))/snlo
    residual=2*(pu*(1-pu)-2*vl)/(n*(n-1))
    if residual<=0:raise ArithmeticError('residual upper bound')
    opt=DESIGN['full_order']; a,b=opt['residual_multipliers']
    candidates=[]
    for k in range(a,b+1):
        r=Q(opt['residual_step'])*k
        if r>=gap:continue
        z=(gap-r)*snlo/(2*sighi)
        gauss=normal_tail(z)
        cant=residual/(residual+r*r)
        upper=round_upper(gauss+berry+cant)
        candidates.append((upper,k,round_upper(gauss),round_upper(berry),round_upper(cant)))
    return min(candidates)

def binomial_enclosures(m,p,lo_cut,hi_cut):
    # PMF relative to its mode. No floating normalisation and no tail truncation.
    mode=int((m+1)*p); scale=2**124; mass=[None]*(m+1);mass[mode]=(scale,scale)
    a=p.numerator;b=p.denominator-a
    def step(v,nom,den):
        lo,hi=v
        return lo*nom//den,(hi*nom+den-1)//den
    for k in range(mode,0,-1):
        mass[k-1]=step(mass[k],k*b,(m-k+1)*a)
    for k in range(mode,m):
        mass[k+1]=step(mass[k],(m-k)*a,(k+1)*b)
    L=sum(v[0] for v in mass);U=sum(v[1] for v in mass)
    def block(rows):
        return Q(sum(v[0] for v in rows),U),min(Q(1),Q(sum(v[1] for v in rows),L))
    return block(mass[:lo_cut+1]),block(mass[hi_cut:])

def necessary():
    d0,d1=delta(Q(0)),delta(Q(1,2))
    ell=cross(d0,d1)[0]**2/(cross(d0,d0)[1]*cross(d1,d1)[1])
    scale=10**32
    base=down(ell,scale)
    # Upper bound B^2 at probabilities 1/20 and 4/5; sqrt(.04)=1/5.
    b_upper=(Q(1,5)+roots(Q(19,100),10**20)[1])**2
    def lower(n):
        val=scale;x=base
        while n:
            if n%2:val=val*x//scale
            x=x*x//scale;n//=2
        return Q(val,scale)
    left,right=0,1
    while lower(right)>b_upper:right*=2
    while right>left+1:
        mid=(right+left)//2
        if lower(mid)>b_upper:left=mid
        else:right=mid
    return dict(minimum_not_excluded=right,lower_at_predecessor=str(lower(left)),upper_required=str(b_upper),
                affinity_squared_lower=str(Q(base,scale)))

def main():
    opt=DESIGN['full_order'];n=opt['n']
    high=Q(opt['reject_flat_U_ge']);low=Q(opt['reject_curved_U_le'])
    models=[parameter_bounds(Q(h)) for h in DESIGN['model_h']]
    third=[third_moment(p[0],p[1],p[4],p[5],opt['moment_grid']) for p in models]
    rec=[]
    for i,param in enumerate(models):
        pl,pu,*_=param
        alpha_gap=high-pu if i==0 else pl-low
        miss_gap=low-pu if i==0 else pl-high
        alpha=full_tail(n,alpha_gap,param,third[i]);miss=full_tail(n,miss_gap,param,third[i])
        rec.append(dict(h=DESIGN['model_h'][i],null_error_upper=str(alpha[0]),power_lower=str(1-miss[0]),
             alpha_terms=list(map(str,alpha)),miss_terms=list(map(str,miss)),
             parameter_enclosures=list(map(str,param[:4])),density_enclosure=[str(Q(down(param[4],10**9),10**9)),str(Q(up(param[5],10**9),10**9))],third_abs_upper=str(third[i])))
    m,l,k=thresholds('matching');matched=[]
    for i,p in enumerate(models):
        # For h=1/2 both adverse probabilities use p_lower by monotonicity. Flat p is exact.
        left,right=binomial_enclosures(m,p[0],l,k)
        error=right[1] if i==0 else left[1]
        power=left[0] if i==0 else right[0]
        matched.append(dict(h=DESIGN['model_h'][i],null_error_upper=str(round_upper(error)),
                            power_lower=str(1-round_upper(1-power))))
    if any(Q(r['null_error_upper'])>Q(1,20) or Q(r['power_lower'])<Q(4,5) for r in rec+matched):
        raise ArithmeticError('predeclared directional target missed')
    return dict(full=rec,matching=matched,necessary=necessary(),
                semantics='Each row fixes truth h. Error is rejection of that truth. Power is rejection of the other candidate.',
                thresholds={m:list(thresholds(m)) for m in ['full_order','matching']})

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
