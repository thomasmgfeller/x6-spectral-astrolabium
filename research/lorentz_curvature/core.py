"""Order-only features and split rank tests. Coordinates and curvature are not inputs."""
import base64
import math
import numpy as np
from scipy.stats import beta
from geometry import require


def validate(c):
    c = np.asarray(c)
    require(c.ndim == 2 and c.shape[0] == c.shape[1] and 4 <= len(c) <= 128, 'invalid relation size')
    require(bool(np.all((c == 0) | (c == 1))), 'binary relation required')
    c = c.astype(bool)
    require(not np.any(np.diag(c)), 'self relation')
    require(not np.any(c & c.T), 'two-cycle')
    masks = [sum(1 << int(j) for j in np.flatnonzero(row)) for row in c]
    for i, mask in enumerate(masks):
        todo = mask
        while todo:
            bit = todo & -todo
            j = bit.bit_length()-1
            require(not (masks[j] & ~mask), 'missing transitive relation or longer cycle')
            todo -= bit
    return c


def features(c):
    c = validate(c)
    n = len(c)
    order = np.argsort(c.sum(axis=0), kind='stable')
    paths = np.ones(n, dtype=np.int64)
    a = c.astype(np.int64)
    counts = []
    for k in range(2, 5):
        paths = paths @ a
        counts.append(int(paths.sum()))
    height = np.ones(n, dtype=np.int64)
    for j in order:
        height[j] += height[c[:, j]].max(initial=0)
    return dict(N=n, C2=counts[0], C3=counts[1], C4=counts[2], H=int(height.max()),
                normalized=[counts[k-2]/math.comb(n, k) for k in range(2, 5)])


def fit(training):
    x = np.asarray([r['features']['normalized'] for r in training])
    mean, sd = x.mean(axis=0), x.std(axis=0, ddof=1)
    require(bool(np.all(np.isfinite(mean))) and bool(np.all(sd > 0)), 'invalid training scale')
    return dict(mean=mean.tolist(), sd=sd.tolist())


def score(feature, model):
    value = float(np.max(np.abs((np.asarray(feature['normalized'])-model['mean'])/model['sd'])))
    require(math.isfinite(value), 'nonfinite score')
    return value


def assess(feature, model, calibration):
    q = score(feature, model)
    qs, hs = np.asarray(calibration['scores']), np.asarray(calibration['heights'])
    b = len(qs)
    joint = (1+int(np.count_nonzero(qs >= q)))/(b+1)
    h = feature['H']
    height = min(1., 2*(1+min(int(np.count_nonzero(hs <= h)), int(np.count_nonzero(hs >= h))))/(b+1))
    return dict(score=q, joint_p=joint, height_p=height)


def pack(c):
    return base64.b64encode(np.packbits(c.reshape(-1), bitorder='little').tobytes()).decode('ascii')


def unpack(encoded, n):
    raw = base64.b64decode(encoded, validate=True)
    require(len(raw) == (n*n+7)//8, 'packed relation size')
    return np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder='little')[:n*n].reshape(n, n).astype(bool)


def interval(k, n, tail_alpha):
    return [0. if k == 0 else float(beta.ppf(tail_alpha, k, n-k+1)),
            1. if k == n else float(beta.ppf(1-tail_alpha, k+1, n-k))]


def summarize(records, contract):
    cells = []
    primary = {}
    for n in contract['sizes']:
        for family in contract['families']:
            rows = [r for r in records if r['phase'] == 'test' and r['N'] == n and r['family'] == family['id']]
            item = dict(N=n, family=family['id'], trials=len(rows))
            flags = {}
            for method in ['joint', 'height']:
                flags[method] = [r['assessment'][method+'_p'] <= contract['alpha_test'] for r in rows]
                k = sum(flags[method])
                item[method] = dict(warnings=k, rate=k/len(rows), conditional_rate_CI95=interval(k, len(rows), .025))
                if n == contract['primary']['N'] and family['id'] in [contract['primary']['null'], contract['primary']['alternative']]:
                    bounds = interval(k, len(rows), contract['primary_gate']['family_alpha']/contract['primary_gate']['one_sided_endpoints'])
                    primary.setdefault(method, {})[family['id']] = dict(warnings=k, trials=len(rows), bounds=bounds)
            item['joint_only'] = sum(a and not b for a, b in zip(flags['joint'], flags['height']))
            item['height_only'] = sum(b and not a for a, b in zip(flags['joint'], flags['height']))
            cells.append(item)
    for method, item in primary.items():
        item['null_upper'] = item[contract['primary']['null']]['bounds'][1]
        item['power_lower'] = item[contract['primary']['alternative']]['bounds'][0]
        item['status'] = ('PRIMARY_MODEL_DEVIATION_SENSITIVITY_ESTABLISHED' if
                          item['null_upper'] <= contract['primary_gate']['max_null_rate_upper'] and
                          item['power_lower'] >= contract['primary_gate']['min_power_lower'] else
                          'PRIMARY_SENSITIVITY_NOT_ESTABLISHED')
    return dict(primary=primary, cells=cells,
                curvature_identification='NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY',
                rate_interval_scope='Conditional on fixed training and shared calibration bank; secondary CIs are pointwise only')
