"""Optional agreement check at the receiver with two contemporaneous precursor clocks."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

from n19_pr395 import instrument
from folgetakt import classify

RASTER = F(1,10**12)


def protected_read(parent, ref, precursor, receiver, memory, received):
    from empfangsbit import K0
    from nulluhr_gegenprobe import loaded_codes
    from referenzprotokoll import association, integer
    # Both records belong to the same trial. Check the clock records before decoding.
    association(ref, precursor)
    if (not integer(precursor.get('target_index')) or ref['device']!='weak_positive_bridge' or
        ref['momentum_bound']!=112 or precursor.get('raster')!=str(RASTER) or
        precursor.get('bias')!='0'):
        raise ValueError('outside the registered precursor and apparatus settings')
    clocks = [precursor.get(k) for k in ('code15','code17')]
    if not all(integer(code) for code in clocks):
        raise ValueError('invalid precursor clock code')
    geometry = json.loads((parent/'Geometrische_Nulluhr.json').read_bytes())
    budgets = json.loads((parent/'Vergleich.json').read_bytes())
    load = next(r['null_load_codes'][str(K0)] for r in budgets if r['m']==112)
    _, band = loaded_codes(*clocks, RASTER, F(0), geometry, load)
    lo,hi = ref['range_codes']
    details = {'kind':ref['kind'],'geometric_range':list(band),'time_range':[lo,hi],
               'shot':ref['shot'],'physical_P3':'60 NOT_RUN'}
    if band[1]<lo or hi<band[0]:
        return {**details,'status':'DISJOINT_REFERENCES'}
    if max(abs(v-ref['baseline_code']) for v in band)>ref['allowed_error_codes']:
        return {**details,'status':'GEOMETRY_OUTSIDE_ERROR_BUDGET'}
    return {**details,'status':'CONDITIONAL_MODEL_CLASSIFICATION',
            'readout':classify(ref,receiver,memory,received)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('decision','precursor','receiver','memory','received'):
        p.add_argument(name,type=Path)
    args=p.parse_args()
    docs=[json.loads(path.read_bytes()) for path in vars(args).values()]
    if docs[0].get('status')!='READY_CONDITIONAL':
        raise ValueError('missing conditional reference')
    with instrument() as parent:
        from n19_archiv394 import inputs
        with inputs():
            result=protected_read(parent,docs[0]['reference'],*docs[1:])
    print(json.dumps(result,sort_keys=True,indent=2))
    if 'readout' not in result:
        raise SystemExit(2)


if __name__=='__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise SystemExit('UNRESOLVED '+str(exc))
