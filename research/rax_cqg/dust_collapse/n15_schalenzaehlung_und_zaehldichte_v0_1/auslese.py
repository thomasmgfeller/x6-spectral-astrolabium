"""One-sided spacetime shell counts and confidence bounds for a calibrated radial instrument."""
from math import pi, sqrt, isfinite
import numpy as np
from scipy.special import gammaincinv, gammainccinv

TICKS = 2**18
END = 5*sqrt(5)/3
TAIL = .05/(524*2)
LAMBDA0 = 92.894688446


def membership(pulses, target, width, duration):
    """Rows: integer units of 1/TICKS in x, emission, reception, side (-1 or +1)."""
    raw=np.asarray(pulses)
    if raw.ndim!=2 or raw.shape[1]!=3 or raw.dtype.kind not in 'iu':
        raise ValueError('Erwartet wird eine dreispaltige ganzzahlige Echotabelle.')
    if not (0<target<1 and 0<duration<=min(target,1-target) and width>0 and isfinite(width)):
        raise ValueError('Ungültige Zielzeit, Dicke oder Exposition.')
    if np.any(np.abs(raw.astype(float))>2**40):
        raise ValueError('Zeitstempel ausserhalb des unterstützten Bereichs.')
    send,recv,side=raw.astype(np.int64,copy=False).T
    if np.any(recv<send) or np.any((side!=-1)&(side!=1)):
        raise ValueError('Ungültige Reihenfolge oder Materialseite.')
    mid=(send+recv)/(2*TICKS)
    distance=END*(recv-send)/(2*TICKS)
    eps=.5/TICKS
    # Tighten the lower-count selection, widen the upper-count selection.
    sure=(side==-1)&(mid>=target+eps)&(mid<=target+duration-eps)&(distance<=width-END*eps)
    possible=(side==1)&(mid>=target-duration-eps)&(mid<=target+eps)&(distance<=width+END*eps)
    return sure,possible


def radius(n_inner,n_outer,exposure,width,nominal_density):
    """Exposure is the calibrated duration in physical proper time, not normalized x."""
    if any(isinstance(n,(bool,np.bool_)) or not isinstance(n,(int,np.integer)) or n<0 for n in (n_inner,n_outer)):
        raise ValueError('Ganzzahlige Zählwerte ab null erforderlich.')
    if not all(isfinite(v) and v>0 for v in (exposure,width,nominal_density)):
        raise ValueError('Eine positive endliche Exposition, Dicke und Zähldichte sind erforderlich.')
    lower=gammaincinv(n_inner,TAIL) if n_inner else 0.
    upper=gammainccinv(n_outer+1,TAIL)
    scale=4*pi*exposure*width*nominal_density
    lo,hi=sqrt(lower/(scale*1.01)),sqrt(upper/(scale*.99))
    return {'inner_sure':int(n_inner),'outer_possible':int(n_outer),'lower':lo,'upper':hi,
            'status':'INTERVAL' if lo<=hi else 'INCONSISTENT'}


def readout(pulses,target,width,duration,nominal_density,complete):
    if complete is not True or pulses is None:
        return {'status':'MISSING_EXPOSURE'}
    sure,possible=membership(pulses,target,width,duration)
    return radius(int(sure.sum()),int(possible.sum()),END*duration,width,nominal_density)


def main():
    import argparse
    from fractions import Fraction
    import json
    from pathlib import Path
    parser=argparse.ArgumentParser(description='Geometrieunabhängige Auslese einer Radaraufnahme.')
    parser.add_argument('instrument',type=Path)
    parser.add_argument('aufnahmen',type=Path)
    args=parser.parse_args()
    settings=json.loads(args.instrument.read_text())
    if (settings['quantization_ticks']!=TICKS or settings['density_relative_error']!=.01
        or abs(settings['time_unit']/END-1)>1e-12):
        raise ValueError('Die Instrumentkalibrierung passt nicht zu diesem Ausleser.')
    readings={}
    with np.load(args.aufnahmen,allow_pickle=False) as recorded:
        for key,z in settings['acquisitions'].items():
            data=recorded[key] if key in recorded else None
            readings[key]=readout(data,float(Fraction(z)),settings['width'],settings['normalized_window'],
                                  settings['nominal_density'],settings['complete_reference_exposures'])
    print(json.dumps(readings,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
