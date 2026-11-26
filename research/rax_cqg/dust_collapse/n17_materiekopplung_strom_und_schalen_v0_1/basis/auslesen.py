"""Enclose a monotone spherical material surface from simultaneous geometric volumes and radar."""
from fractions import Fraction as F
from math import isqrt
import json
import sys


SCALE = 10**14
PI = (F('3.14159265358979323846'), F('3.14159265358979323847'))


def root_bound(value, n):
    if value < 0:
        raise ValueError('Negative Radikanden sind unzulässig.')
    integer = value.numerator * SCALE**n // value.denominator
    if n == 2:
        floor = isqrt(integer)
    elif n == 3:
        hi = 1 << ((integer.bit_length() + 2) // 3)
        lo = 0
        while hi-lo > 1:
            mid = (hi+lo)//2
            if mid**3 <= integer:
                lo = mid
            else:
                hi = mid
        floor = hi if hi**3 <= integer else lo
    else:
        raise ValueError('Erwartet wird eine zweite oder dritte Wurzel.')
    return F(floor,SCALE), F(floor+(F(floor,SCALE)**n != value), SCALE)


def interval(row):
    lo, hi = map(F,row)
    if lo>hi:
        raise ValueError('Vertauschtes Intervall.')
    return lo, hi


def shell(row, xstar, scale, drift):
    volume_lo, volume_hi = interval(row['volume'])
    e_lo, e_hi = interval(row['emission'])
    r_lo, r_hi = interval(row['reception'])
    if volume_lo<=0 or not e_hi<=xstar<=r_lo or r_lo<=e_hi:
        raise ValueError('Volumen oder Radarecho unzureichend aufgelöst.')
    factor = 1-drift*max(xstar-e_lo,r_hi-xstar)
    if factor<=0:
        raise ValueError('Zeitliche Geometrieänderung zu gross für diese Schranke.')
    min_thickness = factor*scale[0]*(r_lo-e_hi)/2
    max_thickness = scale[1]*(r_hi-e_lo)/(2*factor)
    return (volume_lo/max_thickness, volume_hi/min_thickness)


def estimate(data):
    if data.get('verified_assumptions') != True:
        raise ValueError('Materielle Grenze, Geometrie-, Synchronisations- und Monotonieannahmen müssen belegt sein.')
    scale = interval(data['clock_unit'])
    drift, xstar = F(data['log_L_drift_per_x']), F(data['reflection_x'])
    if scale[0]<=0 or drift<0:
        raise ValueError('Ungültige Uhrskala oder Driftschranke.')
    inner = shell(data['inside'],xstar,scale,drift)
    outer = shell(data['outside'],xstar,scale,drift)
    if inner[0]>outer[1]:
        raise ValueError('Schalendaten widersprechen den Voraussetzungen.')
    area = inner[0],outer[1]
    radius = root_bound(area[0]/(4*PI[1]),2)[0],root_bound(area[1]/(4*PI[0]),2)[1]
    return {'area':list(map(str,area)), 'radius':list(map(str,radius))}


if __name__ == '__main__':
    try:
        print(json.dumps(estimate(json.load(sys.stdin)),indent=2))
    except (KeyError,TypeError,ValueError,ZeroDivisionError) as error:
        sys.exit(str(error))
