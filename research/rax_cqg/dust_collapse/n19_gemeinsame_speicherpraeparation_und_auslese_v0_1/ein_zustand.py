"""The same canonical input law in both devices; no rescaling the physical momentum between trials."""
from fractions import Fraction as F
from itertools import product
from ensemble import B,V,FOCUS,certify,local_read
from praeparation import exp_minus_bounds
from staubgeraet import solve,verify
from wege import ROUTES

K_INIT=F(1,10**11)
SHELLS=(F(1),F(5,4),F(3,2),F(2),F(3),F(4))
BITS=tuple(range(39,45))


def run(previous,early):
    from quelle import box,hull,SCALE
    from uhrauslese import LABELS
    from proben import samples
    fixtures,_=samples(previous,early)
    shells={str(b):[] for b in SHELLS}
    binary={str(bits):[] for bits in BITS}
    concrete=0
    examples=[]
    for route in ROUTES:
        for k in (F(1),K_INIT):
            ratio=K_INIT/k
            delta=hull(-K_INIT,K_INIT) if k==1 else box(-k)
            for case,y,w in fixtures:
                for J in LABELS:
                    for m in SHELLS:
                        vel=hull(-m*V*ratio,m*V*ratio)
                        q=hull(-m*(B+FOCUS*V),m*(B+FOCUS*V))
                        state=solve(y,w,J,(vel,)*3,k,delta,route)
                        histories,A=verify(state,J,(vel,)*3,k,delta,route,(q,)*3)
                        result=certify(state,A,J,delta,FOCUS,ratio,m)
                        shells[str(m)].append(min(F(row['margin']) for row in result.values()))
                        if m==1:
                            targets=[state['y'][18],state['y'][7],histories[0][18],histories[1][18],
                                     *[h[7] for h in histories]]
                            assert all(-7*SCALE<v.lo<=v.hi<7*SCALE for v in targets)
                            for bits in BITS:
                                res=certify(state,A,J,delta,FOCUS,ratio,m,F(8,2**bits))
                                binary[str(bits)].append(min(F(row['margin']) for row in res.values()))
                    # Full model, with one common asymmetric preparation for each
                    # field/route combination. Inputs to the reader use only local digits.
                    points=((F(3,5),F(4,5)),(F(4,5),F(-3,5)),(F(-1),F(0)))
                    q=tuple(box(B*a-FOCUS*V*b) for a,b in points)
                    vel=tuple(box(ratio*V*b) for _,b in points)
                    pick=box(-K_INIT)
                    state=solve(y,w,J,vel,k,pick,route)
                    hist,_=verify(state,J,vel,k,pick,route,q)
                    for site in (18,7):
                        assert local_read(state['y'],hist,site)==J
                        assert local_read(state['y'],hist,site,F(16,2**43))==J
                        concrete+=2
                if case=='reference' and k==K_INIT:
                    # The strong preparation at the boundary b=0,v0=+V for the u track.
                    # Its absolute impulse is 10^-14 and its q is unchanged on transfer.
                    vel=(box(V/k),box(0),box(0))
                    q=(box(-FOCUS*V),box(0),box(0))
                    field=solve(y,w,0,vel,k,box(-k),route)
                    hist,_=verify(field,0,vel,k,box(-k),route,q)
                    labels=[local_read(field['y'],hist,i) for i in (18,7)]
                    assert labels[0]!=0 and labels[1]!=0
                    examples.append({'route':route,'null_read_at_18_and_7':list(map(str,labels))})
    def format_rows(rows):
        return {key:{'total':len(vals),'joint_pass':sum(v>0 for v in vals),'minimum_margin':str(min(vals))}
                for key,vals in rows.items()}
    passes=[m for m in SHELLS if min(shells[str(m)])>0]
    bits=[int(b) for b,samples in binary.items() if min(samples)>0]
    assert passes and 43 in bits and len(shells['1'])==144
    safe=max(passes)
    # e^-x bounded via products of a short-series bound to keep all exponents small.
    x=F(9,2)*safe**2
    count=(x.numerator+4*x.denominator-1)//(4*x.denominator)
    qlo,qhi=exp_minus_bounds(x/count)
    prob=(1-qhi**count)**3
    probhi=(1-qlo**count)**3
    # Quantize the bounds outward for compact, machine-readable reporting.
    scale=10**40
    lower=F((prob*scale).__floor__(),scale);upper=F((probhi*scale).__ceil__(),scale)
    return {'fixed_initial_k':str(K_INIT),'shells':format_rows(shells),'adc_bits':format_rows(binary),
            'largest_certified_tested_shell':str(safe),'gaussian_joint_success_lower':str(lower),
            'probability_of_sufficient_shell_upper':str(upper),'smallest_certified_tested_bits':min(bits),
            'concrete_local_decisions':concrete,'strong_preparation_in_weak_device':examples}
