"""Exact action checks and a separate nonlinear reconstruction at validation points."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import product


def rational_action():
    from gemischt import ORDER,PAST
    nodes=set(range(19))
    edges={}
    for i,j in ORDER:
        layer=sum((i,k) in ORDER and (k,j) in ORDER for k in nodes)
        if layer<4:
            edges[i,j]=(1,-9,16,-8)[layer]
    def action(y,w,S,J):
        density=19*sum(w[j] for j in S)
        kinetic=sum(c*w[j]*(y[j]-y[i])**2 for (i,j),c in edges.items() if i in S and j in S)
        return density+kinetic-(J*w[16] if 16 in S else 0)
    count=0
    for lam,J,offset in product((F(1,4),F(2,3),F(7,6)),(F(0),F(-1,10**6),F(1,10**6)),(0,1)):
        y={i:F(13*sum(j==i for _,j in ORDER)+i,19)+F(offset*i*i,700) for i in nodes}
        w={i:F(i+1,53) if i not in (15,17) else F(0) for i in nodes}
        sw={i:(v if i in PAST else v*lam) for i,v in w.items()}
        early=action(y,w,PAST,J)
        assert action(y,sw,nodes,J)==early+lam*(action(y,w,nodes,J)-early)
        count+=1
    return count


def decimal(v):
    v=F(v)
    return D(v.numerator)/D(v.denominator)


def direct(s,t,ratio):
    # Reconstruct the unforced and forced states using the original density
    # row at r and bisection; do not use a factorized response formula.
    u=s-(s*s+6*s+6).sqrt()
    h=t-(8*(t+4)**2-16*(t+3)**2+9*(t-u)**2-(t-s)**2-19).sqrt()
    wz=(D(1)/8)/(s-u)
    wr=wz*ratio
    mz=-(u+3)
    L=wz*mz/(h-s)-wr
    values=[]
    for J in (D('-1e-6'),D('1e-6')):
        S=(u*u-6-J)/(2*(u+3))
        def density(T):
            return 19-8*(T+4)**2+16*(T+3)**2-9*(T-u)**2+(T-S)**2+(T-h)**2
        lo,hi=t-D('1e-7'),t+D('1e-7')
        assert density(lo)>0>density(hi)
        for _ in range(115):
            centre=(lo+hi)/2
            if density(centre)>0:
                lo=centre
            else:
                hi=centre
        T=(lo+hi)/2
        Wr=wr*(t-h)/(T-h)
        Wz=wz+(-(S-s)*L+Wr*(T-S)-wr*(t-s))/mz
        values.append(Wz*(S-u)-wz*(s-u))
    return values,wr


def run(bounds,amplitudes):
    from gemischt import WINDOWS
    from quelle import DATA
    action_tests=rational_action()
    count=cap_count=0
    with localcontext() as ctx:
        ctx.prec=70
        qlo,qhi=map(decimal,bounds['positive_weight_reversal']['Q'])
        for e in map(decimal,DATA[-2].data()):
            trials=[]
            for lo,hi in WINDOWS:
                trials.append([(4-e)*decimal(x)+e-2 for x in (lo,(lo+hi)/2,hi)])
            for s,t,ratio in product(*trials,(D('0.00001'),D(1),D(10),D(100000))):
                changes,wr=direct(s,t,ratio)
                Q=-changes[1]/changes[0]
                assert qlo<=Q<=qhi
                if wr<1:
                    for v,record in zip(changes,bounds['absolute_given_K0']['whole_windows_prefix_setpoint']):
                        low,high=map(decimal,record['magnitude'])
                        assert low<=abs(v)<=high
                    cap_count+=1
                count+=1
        small,large=amplitudes['same_G0_G1']['members']
        for i in (0,1):
            a=abs(decimal(small['delta_K'][i][0]))
            b=abs(decimal(large['delta_K'][i][0]))
            centre=2*a*b/(a+b)
            assert min((centre-a)/a,(b-centre)/b)>D('0.4997')
    return {'exact_rational_action_checks':action_tests,'two_pulse_bisection_pairs':count,
            'in_receiver_weight_domain_pairs':cap_count,'fixed_momenta_minimax_over_49_97_percent':True,
            'extreme_ratios_are_algebraic_window_checks':True}
