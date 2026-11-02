"""Frozen coordinate-free estimator. Nothing here reads planted field labels or coordinates."""
import json
import sys
import numpy as np


def features(case):
    n = case['n']
    edges = np.asarray(case['edges'], dtype=float)
    i, j = edges[:, :2].astype(int).T
    graph = np.zeros((n, n), dtype=bool)
    graph[i, j] = True
    starts = np.flatnonzero(~graph.any(axis=0))
    ends = np.flatnonzero(~graph.any(axis=1))
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError('Unique tips required')
    x, y = starts[0], ends[0]
    U = np.zeros((n, n), dtype=complex)
    U[i, j] = np.exp(1j * edges[:, 2])
    mid = np.flatnonzero(graph[x] & graph[:, y])
    left, right = np.where(graph & graph[x, :, None] & graph[None, :, y])
    paths = [U[x, mid] * U[mid, y], U[x, left] * U[left, right] * U[right, y]]
    counts = [len(p) for p in paths]
    if min(counts) < 2:
        return counts, None
    d = [float(np.sum(np.abs(p-p.mean())**2)/(len(p)-1)) for p in paths]
    return counts, d


def predict(case, matrix):
    counts, d = features(case)
    result = dict(id=case['id'], paths=counts, D=d, J=None, predicted=None, baseline=None)
    if d is not None:
        e2, b2 = np.linalg.solve(matrix, d)
        value = float(e2 - b2)
        result.update(J=value, predicted='E' if value > 0 else ('B' if value < 0 else None),
                      baseline='E' if d[0] > 1e-16 else 'B')
    return result


def main():
    with open('calibration.json') as f:
        matrix = np.array(json.load(f)['C'])
    with open('cases.jsonl') as cases, open('predictions.jsonl', 'x') as out:
        for line in cases:
            out.write(json.dumps(predict(json.loads(line), matrix), allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
