"""Simulation boundary: nested Poisson shells and coordinate-derived order."""
import math
import numpy as np

VOLUME = math.pi / 12


def uniform_diamond(size, duration, rng):
    h = duration / 2 * rng.random(size)**(1/3)
    t = (duration / 2 - h) * rng.choice([-1, 1], size)
    r = h * np.sqrt(rng.random(size))
    angle = 2 * math.pi * rng.random(size)
    return np.column_stack((t, r * np.cos(angle), r * np.sin(angle)))


def extent(z):
    return 2 * (np.abs(z[:, 0]) + np.linalg.norm(z[:, 1:], axis=1))


def shell(rho, seed, index, lo, hi, c):
    rng = np.random.default_rng(np.random.SeedSequence([seed, index, c['shell_seed_tag']]))
    mean = rho * VOLUME * (hi**3 - lo**3)
    size = int(rng.poisson(mean))
    if size > c['maximum_points']:
        raise MemoryError('shell alone exceeds fixed point budget')
    rows = []
    missing = size
    while missing:
        batch = uniform_diamond(max(32, math.ceil(missing / (1-(lo/hi)**3) * 1.05)), hi, rng)
        keep = batch[extent(batch) > lo][:missing]
        rows.append(keep)
        missing -= len(keep)
    z = np.vstack(rows) if rows else np.empty((0, 3))
    assert np.all((extent(z) > lo) & (extent(z) < hi))
    marks = np.random.default_rng(np.random.SeedSequence([seed, index, c['mark_seed_tag']])).random(size)
    colours = np.random.default_rng(np.random.SeedSequence([seed, index, c['colour_seed_tag']])).integers(0, 2, size=size, dtype=np.uint8)
    return z, marks, colours, dict(lower=lo, upper=hi, expected_count=mean, count=size)


def relation(z, block=32):
    n = len(z)
    r = np.empty((n, n), dtype=np.uint8)
    for start in range(0, n, block):
        delta = z[None, :, :] - z[start:start+block, None, :]
        r[start:start+block] = (delta[:, :, 0] > 0) & (delta[:, :, 0]**2 > np.sum(delta[:, :, 1:]**2, axis=2))
    return r
