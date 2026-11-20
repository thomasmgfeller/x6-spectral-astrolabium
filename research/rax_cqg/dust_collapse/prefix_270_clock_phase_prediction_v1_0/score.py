"""Rational prospective decision for the prefix-270 transfer test."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from study import HERE,TYPES,DENSITIES,REF_RADIUS,TARGET_RADIUS,digest
from reference270 import root_bounds


def unique(pairs):
    result={}
    for k,v in pairs:
        if k in result:raise ValueError('Duplicate JSON key '+k)
        result[k]=v
    return result


def load_json(path):
    return json.loads(path.read_text(),object_pairs_hook=unique)


def checked_registration():
    path=HERE/'registration.json'
    reg=load_json(path)
    for name,value in reg['frozen_files_sha256'].items():
        if digest(HERE/name)!=value:raise ValueError('Frozen file mismatch: '+name)
    if reg['end_types']!=list(TYPES) or reg['densities']!=list(DENSITIES):
        raise ValueError('Unexpected target domain')
    decision=reg['decision']
    if decision['threshold_ratio']!='1/100' or decision['target_disk_radius']!=str(TARGET_RADIUS):
        raise ValueError('Unexpected scoring geometry')
    return digest(path)


def frac(v):
    if type(v) is not str:raise ValueError('Expect rational string')
    return F(v)


def unpack_center(row,key):
    a=row[key]
    if type(a) is not list or len(a)!=2:raise ValueError('Expect complex pair')
    return tuple(map(frac,a))


def classify(by_density):
    if any(lo>F(1,100) for lo,hi in by_density.values()):return 'FAIL'
    if all(hi<=F(1,100) for lo,hi in by_density.values()):return 'PASS'
    return 'HOLD'


def score(packet,lock,ref,gram):
    if packet['registration_sha256']!=lock or packet['prefix']!=270:
        raise ValueError('Registration or prefix mismatch')
    if set(packet['densities'])!=set(DENSITIES):
        raise ValueError('Require both densities')
    g,G=frac(gram['gram_lower']),frac(gram['gram_upper'])
    ratios={}
    for i,rho in enumerate(DENSITIES):
        rows=packet['densities'][rho]
        if set(rows)!=set(map(str,TYPES)):raise ValueError('Require all eleven end types')
        lows,ups=[],[]
        for j in map(str,TYPES):
            row=rows[j]
            rad=frac(row['complex_disk_radius'])
            if rad!=TARGET_RADIUS:raise ValueError('Require the sealed evaluator error radius')
            z=unpack_center(row,'complex_center')
            control=unpack_center(row,'unmodulated_split_center')
            reference=ref['packets'][j]['densities'][i]
            old=unpack_center(reference,'complex_center')
            if sum((a-b)**2 for a,b in zip(control,old))>(rad+REF_RADIUS)**2:
                raise ValueError('Unmodulated split control outside reference at '+rho+', type '+j)
            m,M=map(frac,reference['modulus_interval'])
            if m<=0:raise ValueError('Unqualified denominator')
            lower,upper=root_bounds(sum(x*x for x in z))
            lows.append((max(F(0),lower-rad)/M)**2)
            ups.append(((upper+rad)/m)**2)
        ratios[rho]=(max(lows),G/g*max(ups))
    return {'prefix':270,'status':classify(ratios),'qualified_controls':22,
            'ratio_intervals':{rho:[str(lo),str(hi)] for rho,(lo,hi) in ratios.items()},
            'registration_sha256':lock}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('raw',type=Path)
    a=ap.parse_args()
    try:
        lock=checked_registration()
        result=score(load_json(a.raw),lock,load_json(HERE/'reference.json'),load_json(HERE/'gram/gram.json'))
    except (OSError,ValueError,KeyError,TypeError,ArithmeticError) as exc:
        result={'prefix':270,'status':'HOLD','reason':str(exc)}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Keep assertions enabled.')
    main()
