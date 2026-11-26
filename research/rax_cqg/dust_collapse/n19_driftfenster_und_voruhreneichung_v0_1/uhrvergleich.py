"""Two independent precursor readings at tick 11, at four registered precisions."""
import argparse
from fractions import Fraction as F
from math import floor
import json
from pathlib import Path
from quellenpaket import model

TINY = F(1,10**12)
PRECISIONS = [(r,b) for r in (TINY,2*TINY) for b in (F(0),TINY)]


def quantize(x,step):
    return floor(x/step+F(1,2))


def check_domain(codes,step,biases,geo):
    if (step not in (TINY,2*TINY) or any(not 0<=b<=TINY for b in biases) or
        len(codes)!=2 or len(biases)!=2 or any(type(v) is not int for v in codes)):
        raise ValueError('unsupported clock resolution or code')
    bands=[]
    for v,axis,bias in zip(codes,('u_cover','h_cover'),biases):
        width=step/2+bias
        l,h=step*v-width,step*v+width
        gl,gh=map(F,geo[axis])
        if not gl<=l<=h<=gh:
            raise ValueError('clock reading outside certified domain')
        bands.append((l,h))
    return bands


def clock_band(strategy,codes,step,bias,geo,cert):
    if strategy=='archived_band':
        from nulluhr_gegenprobe import loaded_codes
        check_domain(codes,step,(bias,bias),geo)
        return loaded_codes(*codes,step,bias,geo,[-31,-30])[1]
    if strategy!='corner_band':
        raise ValueError('unknown band method')
    return corner_band(codes,step,(bias,bias),geo,cert)


def corner_band(codes,step,biases,geo,cert):
    from empfangsbit import STEP
    from quelle import box,SCALE
    from geometrische_uhr import root
    (u0,u1),(h0,h1)=check_domain(codes,step,biases,geo)
    # Certified global derivative signs: increasing in u and decreasing in h.
    if F(geo['derivative_u'][0])<=0 or F(geo['derivative_h'][1])>=0:
        raise ValueError('uncertified monotone branch')
    lo=root(box(u0),box(h1))[0]
    hi=root(box(u1),box(h0))[0]
    a,b=map(F,cert['load_analog'])
    return quantize(F(lo.lo,SCALE)+a,STEP),quantize(F(hi.hi,SCALE)+b,STEP)


def decision(ref,band):
    l,h=ref['range_codes']
    if band[1]<l or h<band[0]:
        return 'DISJOINT_REFERENCES'
    if max(abs(v-ref['baseline_code']) for v in band)>ref['allowed_error_codes']:
        return 'GEOMETRY_OUTSIDE_ERROR_BUDGET'
    return 'ACCEPT'


def guarded(ref,prec,receiver,memory,received,geo,cert):
    from referenzprotokoll import association
    from folgetakt import classify
    association(ref,prec)
    if (type(prec.get('target_index')) is not int or ref['target_index']!=11 or
        ref['device']!='weak_positive_bridge' or ref['momentum_bound']!=112 or
        ref['allowed_error_codes']!=11 or ref['baseline_code']!=42180625620 or
        ref['range_codes']!=[42180625615,42180625626]):
        raise ValueError('outside the studied fifth-tick reference')
    step=F(prec['raster'])
    if 'bias' in prec and 'bias15' not in prec and 'bias17' not in prec:
        biases=(F(prec['bias']),)*2
    elif 'bias' not in prec:
        biases=(F(prec['bias15']),F(prec['bias17']))
    else:
        raise ValueError('ambiguous clock offset specification')
    band=corner_band((prec['code15'],prec['code17']),step,biases,geo,cert)
    status=decision(ref,band)
    doc={'status':status,'geometric_band':list(band),'kind':ref['kind'],'physical_P3':'60 NOT_RUN'}
    if status=='ACCEPT':
        doc['readout']=classify(ref,receiver,memory,received)
    return doc


def main():
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('reference','precursor','receiver','memory','received'):
        p.add_argument(k,type=Path)
    args=p.parse_args()
    docs=[json.loads(path.read_bytes()) for path in vars(args).values()]
    if docs[0].get('status')!='READY_CONDITIONAL':
        raise ValueError('missing conditional time forecast')
    # Rebuild the load certificate from the pinned model rather than trust a supplied bound.
    from driftfamilie import certify
    with model() as (_,par,prev,early):
        from modell import setup
        cert=certify(*setup(prev,early))
        geo=json.loads((par/'Geometrische_Nulluhr.json').read_bytes())
        result=guarded(docs[0]['reference'],*docs[1:],geo,cert)
    print(json.dumps(result,sort_keys=True,indent=2))
    if result['status']!='ACCEPT':
        raise SystemExit(2)


if __name__=='__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError) as exc:
        raise SystemExit('UNRESOLVED '+str(exc))
