"""Mass-blind reader for the fixed multi-window experiment (standard library)."""
from fractions import Fraction
from itertools import combinations

F = Fraction
TIME_UNIT = F(1, 10**6)
STAMP = 2 * TIME_UNIT
TICK = TIME_UNIT / 10
EARLY_STAMP = STAMP + TICK / 2
ECHO_ERROR = 2 * EARLY_STAMP
ANGLE_TARGET = F(1, 9200)
BAND = (ANGLE_TARGET * F(199, 200), ANGLE_TARGET * F(201, 200))
WINDOWS = tuple(range(500, 1501, 2))


def material_station(bits):
    if len(bits) != 641 or set(bits) - {'0', '1'}:
        raise ValueError('invalid material record')
    if '1' not in bits:
        return None
    end = bits.rindex('1')
    if end == 640 or '0' in bits[:end]:
        raise ValueError('material support lacks a contiguous interior or an exterior')
    return end


def angle_at_tick(count, scale):
    # PR 382 two-way calibration at R0=10, including reflection lag.
    duration = count * TICK
    radius_max = 10 * scale + 3 * EARLY_STAMP
    radius_min = 10 * scale - 3 * (EARLY_STAMP + duration + ECHO_ERROR)
    if duration <= ECHO_ERROR + TICK or radius_min <= 7:
        raise ValueError('early clock outside its calibration domain')
    return ((duration - ECHO_ERROR - TICK) / (2 * radius_max),
            (duration + ECHO_ERROR) / (2 * radius_min))


def calibrated_pair(early, scale):
    # Every possible integer reading at the chosen precision is considered.
    endpoints = set()
    for pair in early:
        nodes = pair.split('|')
        if len(nodes) != 2 or nodes[0] >= nodes[1]:
            raise ValueError('pair keys must be ordered and distinct')
        endpoints.update(nodes)
    expected = {'|'.join(pair) for pair in combinations(sorted(endpoints), 2)}
    if len(endpoints) != 7 or expected != set(early):
        raise ValueError('incomplete graph of early echoes')
    certain, possible = {}, set()
    for pair, counts in early.items():
        first, last = counts
        if type(first) is not int or type(last) is not int or first > last:
            raise ValueError('invalid early interval')
        accepted = []
        for count in range(first, last + 1):
            lower, upper = angle_at_tick(count, scale)
            accepted.append(BAND[0] <= lower and upper <= BAND[1])
        if any(accepted):
            possible.add(pair)
        if all(accepted):
            certain[pair] = (angle_at_tick(first, scale)[0], angle_at_tick(last, scale)[1])
    if len(possible) == len(certain) == 1 and possible == set(certain):
        return next(iter(certain.items()))
    return None


def both_ends(lower, upper):
    """Relative minimax estimate on a positive interval."""
    if not 0 < lower <= upper:
        raise ValueError('incompatible radius limits')
    return {'lower': str(lower), 'upper': str(upper),
            'estimate': str(2 * lower * upper / (lower + upper)),
            'max_relative_error': str((upper - lower) / (upper + lower))}


def read(frame, *, all_early=True, one_window=False):
    valid_fields = {'id', 'initial_positive', 'final_positive', 'tick_ranges',
                    'ticks', 'observed_pair', 'windows'}
    if set(frame) != valid_fields:
        raise ValueError('unexpected reader input fields')
    j = material_station(frame['initial_positive'])
    end = material_station(frame['final_positive'])
    if j is None and end is None:
        return {'status': 'VACUUM'}
    if j is None or end != j:
        return {'status': 'OPEN_MATERIAL'}
    scale = F(13 * j, 6400)
    if not F(999, 100) <= 10 * scale < 10 <= 10 * scale + F(13, 640):
        return {'status': 'OUTSIDE_CONTROL_COLLAR'}
    if not all_early:
        early = {pair: (count, count) for pair, count in frame['ticks'].items()}
    else:
        early = frame['tick_ranges']
    calibration = calibrated_pair(early, scale)
    if calibration is None:
        return {'status': 'OPEN_PAIR'}
    pair, (theta_low, theta_high) = calibration
    if pair != frame['observed_pair']:
        return {'status': 'OPEN_PAIR'}
    states = frame['windows']
    if len(states) != len(WINDOWS) or set(states) - {'N', '?', 'Y'}:
        raise ValueError('invalid or incomplete late record')
    responses = [(w, state) for w, state in zip(WINDOWS, states)
                 if not one_window or w == 1000]
    negative = [w for w, state in responses if state == 'N']
    positive = [w for w, state in responses if state == 'Y']
    base = {'pair': pair, 'marker': j, 'theta': [str(theta_low), str(theta_high)],
            'last_no': max(negative, default=None), 'first_yes': min(positive, default=None)}
    if negative and positive and max(negative) >= min(positive):
        return {**base, 'status': 'INCONSISTENT'}
    if not negative or not positive:
        return {**base, 'status': 'ONE_SIDED' if negative or positive else 'OPEN'}
    duration_low = max(negative) * TIME_UNIT - 2 * STAMP
    duration_high = min(positive) * TIME_UNIT + 2 * STAMP
    lower = duration_low / theta_high - 2 * STAMP
    upper = duration_high / theta_low + 3 * duration_high + 2 * STAMP
    return {**base, 'status': 'BOUNDED', 'material': both_ends(lower, upper),
            'support': both_ends(lower, upper + 2 * (10 - 10 * scale))}


def predict(data):
    return {f['id']: {'all_early': read(f), 'recorded_early': read(f, all_early=False),
                       'old_window': read(f, one_window=True)} for f in data}
