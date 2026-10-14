"""Jones optics, calibration lookup and analyzer coordinates; radians != motor degrees.
SPDX-License-Identifier: Apache-2.0
"""
import cmath
import math
from .signals import finite


def retarder(angle_deg, retardance_rad):
    angle = math.radians(finite(angle_deg))
    phase = cmath.exp(1j*finite(retardance_rad))
    c, s = math.cos(angle), math.sin(angle)
    return ((c*c+phase*s*s, c*s*(1-phase)), (c*s*(1-phase), s*s+phase*c*c))


def multiply(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def qhq_phase(phi_rad):
    """Ideal Q(45)-H(theta)-Q(45); relative V/H phase, irrelevant common phase.

    Actual 808 nm plates at 810 nm require measured retardance and axis offsets.
    This ideal map is not a hardware calibration.
    """
    theta = ((finite(phi_rad)-math.pi) % (2*math.pi))*180/(4*math.pi)
    q = retarder(45, math.pi/2)
    return {'q1_deg': 45., 'h_deg': theta, 'q2_deg': 45.,
            'matrix': multiply(q, multiply(retarder(theta, math.pi), q))}


def linear_analyzer_angle(axis_deg, motor_zero_deg, direction=1):
    if direction not in (-1, 1):
        raise ValueError('Direction must be +1 or -1')
    return finite(motor_zero_deg)+direction*finite(axis_deg)/2


def calibration(table, expected_kind=None):
    required = {'schema', 'calibration_id', 'evidence_kind', 'unit', 'wavelength_nm',
                'device_serial', 'run_ids', 'points', 'settle_s', 'max_power_w'}
    if not isinstance(table, dict) or set(table) != required or table['schema'] != 'acvm.optical.calibration/1':
        raise ValueError('Calibration schema/fields')
    if table['evidence_kind'] not in ('SIMULATED', 'MEASURED') or (expected_kind and table['evidence_kind'] != expected_kind):
        raise ValueError('Calibration evidence class mismatch')
    if table['unit'] != 'transmission_fraction' or not table['calibration_id'] or not table['device_serial']:
        raise ValueError('Calibration identity/units')
    if not table['run_ids'] or len(set(table['run_ids'])) != len(table['run_ids']):
        raise ValueError('Calibration run identity')
    finite(table['wavelength_nm'], 'wavelength', 800, 820)
    finite(table['settle_s'], 'settling time', .5, 60)
    finite(table['max_power_w'], 'maximum optical power', 1e-12, .05)
    points = table['points']
    if not isinstance(points, list) or not 3 <= len(points) <= 1000:
        raise ValueError('Calibration needs 3..1000 points on one monotonic branch')
    direction = None
    for index, p in enumerate(points):
        if set(p) != {'fraction', 'motor_deg', 'uncertainty_fraction'}:
            raise ValueError('Calibration point fields')
        finite(p['fraction'], 'fraction', 0, 1)
        finite(p['motor_deg'], 'angle', 0, 180)
        finite(p['uncertainty_fraction'], 'uncertainty', 0, 1)
        if index:
            prev = points[index-1]
            delta = p['motor_deg']-prev['motor_deg']
            if p['fraction'] <= prev['fraction'] or delta == 0:
                raise ValueError('Nonmonotonic calibration')
            sign = 1 if delta > 0 else -1
            if direction is not None and sign != direction:
                raise ValueError('Ambiguous calibration branch')
            direction = sign
    return table


def fraction_to_angle(table, fraction):
    calibration(table)
    points = table['points']
    finite(fraction, 'fraction', points[0]['fraction'], points[-1]['fraction'])
    for left, right in zip(points, points[1:]):
        if left['fraction'] <= fraction <= right['fraction']:
            w = (fraction-left['fraction'])/(right['fraction']-left['fraction'])
            return left['motor_deg']+w*(right['motor_deg']-left['motor_deg'])
    raise ValueError('No extrapolation')


def phase_motor_angles(phi_rad, phase_calibration):
    """Map ideal QHQ axes through measured mount zero/direction; check Jones residual.

    Only accepts a calibration sufficiently close to this limited QHQ construction.
    A rejected target needs a general calibrated optimizer, not an unchecked move.
    """
    c = phase_calibration
    if (set(c) != {'calibration_id', 'evidence_kind', 'wavelength_nm', 'axes', 'max_phase_error_rad', 'max_crosstalk_amplitude'}
            or c['evidence_kind'] != 'MEASURED' or not c['calibration_id']):
        raise ValueError('Measured QHQ calibration required')
    finite(c['wavelength_nm'], 'phase wavelength', 800, 820)
    tolerance = finite(c['max_phase_error_rad'], 'phase acceptance', 1e-6, .1)
    leakage = finite(c['max_crosstalk_amplitude'], 'cross amplitude acceptance', 1e-6, .05)
    if set(c['axes']) != {'q1', 'h', 'q2'}:
        raise ValueError('Three calibrated QHQ axes required')
    ideal, angles = qhq_phase(phi_rad), {}
    j = ((1, 0), (0, 1))
    for key in ('q1', 'h', 'q2'):
        axis = c['axes'][key]
        if set(axis) != {'zero_deg', 'direction', 'retardance_rad'} or type(axis['direction']) is not int or axis['direction'] not in (-1, 1):
            raise ValueError('QHQ axis calibration')
        angle = ideal[key+'_deg']
        angles[key] = finite(axis['zero_deg'])+axis['direction']*angle
        j = multiply(retarder(angle, finite(axis['retardance_rad'], 'retardance', 0, 2*math.pi)), j)
    if abs(j[0][0]) < 1e-12 or max(abs(j[0][1]), abs(j[1][0])) > leakage:
        raise ValueError('QHQ calibrated crosstalk exceeds acceptance')
    error = cmath.phase(j[1][1]/j[0][0]*cmath.exp(-1j*phi_rad))
    if abs(error) > tolerance:
        raise ValueError('QHQ calibrated phase residual exceeds acceptance')
    return angles


def fit_hwp_zero(rows):
    """Fit power/reference = a+b*cos(4θ)+c*sin(4θ) on calibration rows only.

    Estimates a HWP axis zero modulo 90°, not QWP retardance or absolute phase.
    Reference power must be measured per row to suppress source-intensity drift.
    """
    if not isinstance(rows, list) or not 6 <= len(rows) <= 10000:
        raise ValueError('HWP calibration requires 6..10000 observations')
    design, response = [], []
    for row in rows:
        if set(row) != {'angle_deg', 'power_w', 'reference_w', 'dark_w'}:
            raise ValueError('HWP calibration row fields')
        theta = math.radians(finite(row['angle_deg']))
        power = finite(row['power_w'], 'power W', 0)
        dark = finite(row['dark_w'], 'dark W', 0)
        reference = finite(row['reference_w'], 'reference W', 1e-15)
        if power < dark:
            raise ValueError('Below dark baseline')
        design.append((1., math.cos(4*theta), math.sin(4*theta)))
        response.append((power-dark)/reference)
    augmented = [[sum(x[i]*x[j] for x in design) for j in range(3)]+
                 [sum(x[i]*y for x, y in zip(design, response))] for i in range(3)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda row: abs(augmented[row][col]))
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        if abs(divisor) < 1e-10:
            raise ValueError('HWP scan is unidentifiable')
        augmented[col] = [v/divisor for v in augmented[col]]
        for row in range(3):
            if row != col:
                multiplier = augmented[row][col]
                augmented[row] = [a-multiplier*b for a, b in zip(augmented[row], augmented[col])]
    a, b, c = [row[3] for row in augmented]
    amplitude = math.hypot(b, c)
    if amplitude < 1e-6 or a <= 0:
        raise ValueError('Insufficient HWP modulation contrast')
    residuals = [y-(a+b*x[1]+c*x[2]) for x, y in zip(design, response)]
    return {'zero_deg_modulo_90': math.degrees(math.atan2(c, b))/4,
            'offset': a, 'cos4_coefficient': b, 'sin4_coefficient': c,
            'visibility': amplitude/a, 'rmse': math.sqrt(sum(r*r for r in residuals)/len(rows)),
            'residuals': residuals, 'uncertainty': 'NOT_ESTIMATED_FROM_INDEPENDENT_RUNS',
            'physical_qualification': 'NOT_PERFORMED'}
