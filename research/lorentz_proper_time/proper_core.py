"""Inference API: no coordinates, identities, generator labels or target values."""
import math
import numpy as np


def require(ok, message):
    if not ok:
        raise ValueError(message)


def matrix(packet):
    require(type(packet) is dict and set(packet) == {'N', 'marks', 'relation_rows'}, 'inference fields')
    n, rows, marks = packet['N'], packet['relation_rows'], packet['marks']
    require(type(n) is int and n > 2, 'N includes two marks')
    require(type(rows) is list and len(rows) == n and all(type(r) is str and len(r) == n and set(r) <= {'0', '1'} for r in rows), 'binary full relation')
    require(type(marks) is list and len(marks) == 2 and all(type(i) is int and 0 <= i < n for i in marks) and marks[0] != marks[1], 'two distinct valid marks')
    masks = [int(r[::-1], 2) for r in rows]
    for i, mask in enumerate(masks):
        require(not ((mask >> i) & 1), 'strict diagonal')
        todo = mask
        while todo:
            bit = todo & -todo
            require(masks[bit.bit_length()-1] & ~mask == 0, 'transitive relation')
            todo -= bit
    c = (np.frombuffer(''.join(rows).encode(), dtype=np.uint8)-48).reshape(n, n).astype(bool)
    require(c[marks[0], marks[1]], 'ordered marked endpoints')
    return c


def chain_height(c):
    if not len(c):
        return 0
    heights = np.ones(len(c), dtype=np.int64)
    for j in np.argsort(c.sum(axis=0), kind='stable'):
        heights[j] = 1 + int(heights[c[:, j]].max(initial=0))
    return int(heights.max())


def features(packet):
    c = matrix(packet)
    p, q = packet['marks']
    inner = c[p] & c[:, q]
    n, R, H = len(c), int(c.sum()), chain_height(c)
    K, ell = int(inner.sum()), chain_height(c[np.ix_(inner, inner)])
    return dict(N=n, m=n-2, R=R, H=H, K=K, ell=ell)


def design_row(f):
    r, h = f['R']/math.comb(f['N'], 2), f['H']/f['N']
    return [1.0, r, h, r*r, r*h, h*h]


def fit_D(calibration):
    require(len(calibration) > 0, 'nonempty calibration')
    fs, labels = [], []
    for row in calibration:
        require(type(row) is dict and set(row) == {'split', 'packet', 'theta'} and row['split'] == 'calibration', 'calibration interface and split')
        require(type(row['theta']) in (float, int) and math.isfinite(row['theta']) and 0 < row['theta'] < 1, 'calibration label')
        fs.append(features(row['packet']))
        labels.append(row['theta'])
    require(len({f['N'] for f in fs}) == 1, 'one size per fit')
    x, y = np.asarray([design_row(f) for f in fs]), np.asarray(labels)
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    keep = s > 1e-12*s[0]
    coeff = vt[keep].T @ ((u[:, keep].T @ y)/s[keep])
    residual = x @ coeff-y
    return dict(N=fs[0]['N'], coefficients=coeff.tolist(), singular_values=s.tolist(),
                rank=int(keep.sum()), cutoff_relative=1e-12,
                calibration_count=len(y), calibration_mse=float(np.mean(residual**2)),
                normal_equation_residual=float(np.max(np.abs(x.T @ residual))))


def estimates(f, model):
    require(set(model) >= {'N', 'coefficients'} and model['N'] == f['N'], 'model size')
    coeff = model['coefficients']
    require(len(coeff) == 6 and all(math.isfinite(v) for v in coeff), 'finite model')
    raw = dict(V=math.sqrt(f['K']/f['m']), L=f['ell']/(2*math.sqrt(f['m'])),
               C0=64/225, D=math.fsum(a*b for a, b in zip(design_row(f), coeff)))
    return dict(raw=raw, clipped={k: min(1.0, max(0.0, v)) for k, v in raw.items()})


def predict(packet, model):
    f = features(packet)
    return dict(features=f, **estimates(f, model))
