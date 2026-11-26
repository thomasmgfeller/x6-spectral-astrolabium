"""Analytic inversion of all quantizer cells; no sampling assumption on drift or offset."""
from fractions import Fraction as F
from itertools import groupby
from uhrvergleich import clock_band,decision


def code_range(value,step,bias):
    from geometrische_uhr import qcode
    return range(qcode(value-bias,step),qcode(value+bias,step)+1)


def runs(codes):
    return [(v[0],v[-1]) for _,g in groupby(enumerate(codes),lambda t:t[1]-t[0])
            if (v:=[code for _,code in g])]


def h_bands(good,step,bias,mode):
    # Possible: dilation by bias. Guaranteed: erosion of each connected set.
    expansion=bias if mode=='any' else -bias
    out=[]
    for l,h in runs(good):
        a=(l-F(1,2))*step-expansion
        b=(h+F(1,2))*step+expansion
        if a>=b:
            continue
        if out and a<=out[-1][1]:
            out[-1]=(out[-1][0],max(out[-1][1],b))
        else:
            out.append((a,b))
    return out


def drift_ranges(u,t,hbands):
    from empfangsbit import STEP
    from quelle import SCALE,box
    from geometrische_uhr import root
    def delta(h):
        d=root(u,box(h))[0]-t
        return [str(F(v,SCALE)/STEP) for v in (d.lo,d.hi)]
    return [{'left_open':delta(b),'right_closed':delta(a)} for a,b in reversed(hbands)]


def analyze(y,w,ref,geo,cert):
    from empfangsbit import STEP
    from quelle import SCALE
    from referenzwechsel import displaced
    from uhrvergleich import PRECISIONS
    # The true loaded digit must be inside B±11 for any passed geometric band.
    t=y[18]+6*STEP
    sa,sb=map(F,cert['load_analog'])
    lo,hi=(ref['baseline_code']+sgn*ref['allowed_error_codes'] for sgn in (-1,1))
    outer=[lo-F(1,2)-(F(t.hi,SCALE)+sb)/STEP,
           hi+F(1,2)-(F(t.lo,SCALE)+sa)/STEP]
    assert -20<outer[0]<outer[1]<20
    states={n:displaced(y,w,(6+n)*STEP)[0] for n in (-20,0,20)}
    rows=[]
    for step,bias in PRECISIONS:
        u_codes=list(code_range(y[15],step,bias))
        h_stable=list(code_range(states[0][17],step,bias))
        # Enumerate all possible code cells in the surviving inner interval plus sentinels.
        endpoints=[code_range(states[n][17],step,bias) for n in (-20,20)]
        hc=list(range(min(v.start for v in endpoints)-2,max(v.stop for v in endpoints)+2))
        for method in ('archived_band','corner_band'):
            yes,all_yes=[],[]
            stable=[]
            for h in hc:
                flags=[]
                for u in u_codes:
                    band=clock_band(method,(u,h),step,bias,geo,cert)
                    status=decision(ref,band)
                    flags.append(status=='ACCEPT')
                    if h in h_stable:
                        stable.append({'u':u,'h':h,'band':list(band),'status':status})
                if any(flags):
                    yes.append(h)
                if all(flags):
                    all_yes.append(h)
            assert hc[0] not in yes and hc[-1] not in yes
            windows={k:drift_ranges(y[15],t,h_bands(c,step,bias,k))
                     for k,c in [('any',yes),('all',all_yes)]}
            for ranges in windows.values():
                assert all(-20<F(r['left_open'][0])<=F(r['right_closed'][1])<20 for r in ranges)
            rows.append({'raster':str(step),'bias':str(bias),'method':method,
                         'possible_u_codes':u_codes,'stable':stable,'drift_windows_in_steps':windows})
    return {'necessary_outer_steps':list(map(str,outer)),'profiles':rows}
