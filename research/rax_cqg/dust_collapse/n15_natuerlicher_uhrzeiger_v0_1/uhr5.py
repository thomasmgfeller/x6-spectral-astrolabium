"""Unpulsed native clock 5: exact gain and common original support."""
from fractions import Fraction as F
import argparse
import json
from pruefen import (ROOT, EDGES, ETA, E, DELTA, INNER_MEANS, INNER, ORDER, X0, DX,
                     HALF, clocks, dwell, full_action, check, I, source)


def run():
    source()
    check(EDGES[5,11] == -9 and [j for j in ORDER if (5,j) in EDGES] == [6,11,12,13], 'Uhr 5')
    a = F(9,38)
    # With Y11 fixed, the original incoming square gives the entire difference in its x coefficient.
    # Its sign is for upper u5 arm minus lower u5 arm.
    check(4*a*F(1,4)/72 == F(1,304), 'Eichpunkt')
    shift_max = 1/(72*DELTA*(4-F(3,32)/DELTA)**3)
    check(shift_max.hi < I.of(F(3,2500)).lo, 'Verschiebung im Originalfenster')
    margin = F(7,6400) - (1+ETA)*(F(3,2500)+HALF)/2
    check(margin > 0, 'Gemeinsame ursprüngliche Dichten 4 und 6')
    # Direct check as a rational polynomial in s, before substituting s(D).
    tests = 0
    for e in (F(-1,4), E):
        for z in (F(31,64), F(1,2), F(33,64)):
            u=INNER_MEANS.copy(); u[INNER.index(11)]=z
            nominal=dwell(u)
            for shift in (F(1,1024), F(1,900)):
                for stop in (6,11,12,13,14,10):
                    for pulse in (-F(1,5), F(0), F(1,5)):
                        difference=F(0)
                        for sign in (-1,1):
                            v=u.copy(); v[INNER.index(5)]+=sign*shift
                            f=dwell(v)
                            for j in INNER:
                                check((1-ETA)*f[j] < nominal[j] < (1+ETA)*f[j], 'Reale Armfenster')
                            y=clocks(e,v)
                            # The coefficient of x11 in the full action suffices by linearity.
                            w={j:F(j==11) for j in ORDER}
                            difference += sign*full_action(y,w,stop,pulse)
                        expect=-4*a*(4-e)**2*(z-F(1,4))*shift
                        check(difference == (0 if stop==6 else expect), 'Wirkung auf beiden realen Armen')
                        tests+=1
    gain=[F(15,16)*F(1,304), F(17,16)*F(1,304)]
    phase=-(2*DX)/304
    return {'full_polynomial_comparisons':tests,'max_s_upper':shift_max.rounded(12)[1],
            'common_density_margin_lower':str(margin),'abs_gain_interval':list(map(str,gain)),
            'relative_gain_interval':['15/16','17/16'], 'central_mixed_phase':str(phase),
            'central_mixed_phase_radians':float(phase)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--json',action='store_true')
    args=p.parse_args()
    out=json.dumps(run(),indent=2)+'\n'
    if args.json: print(out,end='')
    else:
        check(out==(ROOT/'uhr5.json').read_text(),'Archivierter Uhr-5-Vergleich')
        print('PASS · Reale Uhr-5-Arme, gemeinsamer Träger und vollständige Wirkung')
