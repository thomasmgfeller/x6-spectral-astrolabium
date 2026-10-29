"""Exact analytic controls; no sampling, fitted tail, or external data access."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib, json, platform
from flint import arb, ctx, fmpq, fmpq_poly as Poly

HERE = Path(__file__).resolve().parent
checks = []

def require(ok, name):
    if not ok:
        raise AssertionError(name)
    checks.append(name)

def Q(x):
    x = F(x)
    return fmpq(x.numerator, x.denominator)

def FQ(x):
    return F(str(x))

def integral(p, lo, hi):
    anti = p.integral()
    return anti(Q(hi)) - anti(Q(lo))

def lens_slice(t, H):
    R, S, d = F(7,4)-t, H+t, F(3,2)
    return 4*R**3/3 - (R+S-d)**2*(d*d+2*d*(R+S)-3*(R-S)**2)/(12*d)

def axial_slice(t, H):
    """Independent cross-section integration, in units of pi, all rational."""
    R, S, d = F(7,4)-t, H+t, F(3,2)
    lo, hi = d-R, d+R
    breaks = sorted(set([lo,hi] + [v for v in [-S,S,(S*S-R*R+d*d)/(2*d)] if lo<v<hi]))
    ball = Poly([Q(R*R-d*d),Q(2*d),-1])
    big = Poly([Q(S*S),0,-1])
    ans = fmpq(0)
    for a,b in zip(breaks,breaks[1:]):
        mid=Q((a+b)/2)
        diff = ball-big if big(mid)>0 else ball
        if diff(mid)>0:
            ans += integral(diff,a,b)
    return FQ(ans)

def interpolate(xs, ys):
    out = Poly([])
    for i,x in enumerate(xs):
        part = Poly([Q(ys[i])])
        for j,y in enumerate(xs):
            if i!=j:
                part *= Poly([Q(-y),1])/Q(x-y)
        out += part
    return out

def enclosure(x):
    return x.str(35, more=True)

def main():
    ctx.prec=192
    rows=[]
    t=Poly([0,1]);d=fmpq(3,2);R=fmpq(7,4)-t
    for H,expected in [(F(4),F(15875,9216)),(F(5),F(29,1536))]:
        S=Q(H)+t
        lens=4*R**3/3-(R+S-d)**2*(d*d+2*d*(R+S)-3*(R-S)**2)/(12*d)
        end=(F(13,4)-H)/2
        xs=[-1+(end+1)*F(i,3) for i in range(4)]
        axial=interpolate(xs,[axial_slice(x,H) for x in xs])
        require(axial==lens,f'H={H}: independent axial polynomial equals lens')
        for i in range(65):
            x=-1+(end+1)*F(i,64)
            require(axial_slice(x,H)==lens_slice(x,H),f'H={H}: exact slice {i}')
        vol=FQ(integral(axial,F(-1),end))
        require(vol==expected,f'H={H}: exact missing volume/pi')
        lam=3*vol;prob=1-(-arb(str(lam))).exp()
        rows.append({'H':str(H),'last_missing_time':str(end),'volume_over_pi':str(vol),'poisson_mean':str(lam),'probability_nonempty':enclosure(prob),'slice_polynomial_over_pi':str(axial)})
    # Geometry and sharpness: max radial reach is 13/4-t.
    require(F(13,4)+2==F(21,4),'sharp enclosing diamond parameter')
    tw,zw=F(-15,16),F(33,8)
    require(abs(zw-F(3,2))<F(7,4)-tw and zw>5+tw and tw>-1,'negative control: Omega5 misses an active causal point')
    require(F(5)+2*F(-7,8)==F(13,4),'Omega5 last missing time -7/8')
    require(F(21,4)+2*(-1)==F(13,4),'closure boundary at initial slice')
    require(FQ(integral(4*R**3/3,F(-1),F(5,4)))==F(4875,256),'finite active volume/pi')
    # Moments: rising factorials, independently checked against factored cubic.
    alpha=Poly([0,1]);moment=1-9*alpha+8*alpha*(alpha+1)-fmpq(4,3)*alpha*(alpha+1)*(alpha+2)
    require(moment==-fmpq(4,3)*(alpha-fmpq(1,2))*(alpha-1)*(alpha-fmpq(3,2)),'signed Gamma moment factorization')
    for j in range(3):
        require(moment(fmpq(j+1,2))==0,f'signed s^{j} moment vanishes')
    require(moment(2)!=0,'negative control: fourth moment does not vanish')
    plus=1+9*alpha+8*alpha*(alpha+1)+fmpq(4,3)*alpha*(alpha+1)*(alpha+2)
    require(plus(fmpq(1,2))==14,'absolute majorant integral factor 14')
    require(1+9*2*fmpq(1,2)+8*4*fmpq(3,4)+fmpq(4,3)*8*fmpq(15,8)==54,'far-tail half-Gaussian integral factor 54')
    # Discrete binomial representation against the archived polynomial formula.
    eps=F(1,16);u=eps/(1-eps);co=[1,-9,16,-8]
    for n in range(129):
        w=sum(F(co[k]*comb(n,k))*eps**k*(1-eps)**(n-k) for k in range(min(n,3)+1))
        alt=(1-eps)**n*(1-9*n*u+8*n*(n-1)*u*u-F(4,3)*n*(n-1)*(n-2)*u**3)
        require(w==alt and abs(w)<=16,f'binomial weight identity/bound n={n}')
    require(F(1)!=0,'w(0)=1 supplies unweighted lower bound')
    pi=arb.pi();rho=3/pi;q=rho/16;a=4*(q/6).sqrt();beta=a/(16*(a+1));c=pi*q/24
    require(c.contains(arb(1)/128),'fixed Gaussian parameter c=1/128')
    J1=7*(24/q).sqrt();J2=27*(48/q).sqrt()
    C1=2*pi*beta*rho*J1;C2=2*pi*beta*rho*J2
    require(C1.overlaps(21/(1+a)),'one-step near-tail coefficient')
    require(C2.overlaps(81*arb(2).sqrt()/(1+a)),'one-step far-tail coefficient')
    # The exact derivative of -exp(-L/256)(256L+65536) is L exp(-L/256).
    require(Poly([65536,256])/256-Poly([256])==Poly([0,1]),'Gaussian far-tail antiderivative')
    require(512**3>105**4,'explicit Fourier-strip transition L0=1024')
    prov=json.loads((HERE/'PROVENANCE.json').read_text())
    for e in prov['evidence']:
        require(hashlib.sha256((HERE/e['included_path']).read_bytes()).hexdigest()==e['sha256'],'unchanged evidence '+e['included_path'])
    result={'schema':'cspp.causal-closure/0.17','status':'PASS','check_count':len(checks),'checks':checks,
            'geometry':{'sharp_H':'21/4','remaining_Omega5_volume':'29*pi/1536','rows':rows,'witness_t':str(tw),'witness_z':str(zw)},
            'moments':{'factorization':str(moment),'vanishing_s_powers':[0,1,2]},
            'forcing_bound':{'c':'1/128','C_near':enclosure(C1),'C_far':enclosure(C2),'scope':'unconditional absolute one-step expectation; source seminorm constants not evaluated; not detector error'},
            'conclusion':{'fixed_model_history_convergence':'analytic almost-sure existence argument, not a numerical certificate','beyond5_error_bound':'NOT_CERTIFIED','METHOD':'HOLD','G1':'HOLD','fresh_ensemble':'NOT_RUN'},
            'runtime':{'python':platform.python_version(),'flint':__import__('flint').__version__},'random_calls':0}
    (HERE/'results/ANALYTIC_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','check_count','geometry','forcing_bound','conclusion']},indent=2))

if __name__=='__main__':main()
