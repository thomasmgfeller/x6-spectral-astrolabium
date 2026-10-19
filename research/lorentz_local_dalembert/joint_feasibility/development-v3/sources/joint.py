"""Joint inference accepts order, marks and declared metadata; never coordinates.

Search exhaustion is not a proof that no feasible support exists.
Auxiliary-colour guards are diagnostics, not statistical confidence bounds.
"""
import itertools
import math
import numpy as np
from intrinsic import ETA, design, normalize, gram_and_vectors, noise_guard

VOLUME = math.pi/12


class Counts:
    def __init__(self, g, colours, rho, guards):
        self.g, self.rho, self.guards = g, rho, guards
        colours = np.asarray(colours, dtype=np.uint8)
        if colours.shape != (g.size,) or np.any(colours > 1):
            raise ValueError('one binary colour per event required')
        if not math.isfinite(rho) or rho <= 0:
            raise ValueError('positive known density required')
        self.bits = [int.from_bytes(np.packbits(colours == i, bitorder='little').tobytes(), 'little') for i in (0, 1)]
        self.cache = {}

    def values(self, a, b):
        a, b = int(a), int(b)
        if a == b:
            return (0, 0, 0)
        if self.g.r[b, a]:
            a, b = b, a
        if not self.g.r[a, b]:
            raise ValueError('a counted interval must be causal')
        if (a, b) not in self.cache:
            bits = self.g.succ[a] & self.g.pred[b]
            self.cache[a, b] = (bits.bit_count(), (bits & self.bits[0]).bit_count(), (bits & self.bits[1]).bit_count())
        return self.cache[a, b]

    def good(self, a, b):
        n, h0, h1 = self.values(a, b)
        return n >= self.guards['guard_min_interval'] and min(h0, h1) >= self.guards['guard_min_half_interval']

    def q(self, a, b, half=None):
        values = self.values(a, b)
        n = values[0] if half is None else 2*values[half+1]
        return (n/(self.rho*VOLUME))**(2/3)


def ordered_pairs(g, root, temporal, landmarks, support):
    pairs = set()
    for a in landmarks:
        pairs.add(tuple(sorted((a, root))))
        pairs.update(tuple(sorted((a, b))) for b in support)
    pairs.update(tuple(sorted((root, b))) for b in support)
    pairs.update(tuple(sorted(pair)) for pair in itertools.combinations(landmarks, 2))
    return sorted(pairs, key=lambda p: tuple(sorted(float(g.marks[a]) for a in p)))


def certificate(g, counts, root, temporal, landmarks, support, guards):
    h, v = gram_and_vectors(counts.q, landmarks, root, support, 1.)
    normal = normalize(h, guards['guard_max_condition'])
    if normal is None:
        return {'status': 'bad_signature_or_condition'}
    t, ev, condition = normal
    halves = [gram_and_vectors(lambda a, b, j=j: counts.q(a, b, j), landmarks, root, support, 1.) for j in (0, 1)]
    pairs = ordered_pairs(g, root, temporal, landmarks, support)
    values = [counts.values(a, b) for a, b in pairs]
    guard = noise_guard(h, v, t, halves, [x[0] for x in values],
                        [[x[j+1] for x in values] for j in (0, 1)], condition, guards)
    return dict(status='ok', gram=h, vectors=v, transform=t, eigenvalues=ev,
                condition=condition, features=(t@v).T,
                half_grams=[a for a, b in halves], half_vectors=[b for a, b in halves],
                interval_pairs=pairs, interval_counts=[x[0] for x in values],
                half_interval_counts=[[x[j+1] for x in values] for j in (0, 1)], guard=guard)


def design_check(features, scale, c):
    d = design(np.asarray(features)/scale)
    sv = np.linalg.svd(d, compute_uv=False)
    rank = int(np.sum(sv > c['rank_relative_tolerance']*sv[0])) if len(sv) and sv[0] > 0 else 0
    condition = float(sv[0]/sv[-1]) if len(sv) == 9 and rank == 9 else None
    return dict(rank=rank, condition=condition, singular_values=sv,
                passed=rank == 9 and condition <= c['maximum_design_condition'])


def frames(g, counts, root, temporal, probes, c, guards):
    fixed = [root]+list(temporal)
    pool_records, matrices, triples, directions, half_matrices = [], [], [], [], []
    for side, cones in [('past', g.pred), ('future', g.succ)]:
        common = (1 << g.size)-1
        for b in fixed:
            common &= cones[b]
        candidates = []
        while common:
            low = common & -common
            a = low.bit_length()-1
            common ^= low
            if a not in probes and all(counts.good(a, b) for b in fixed):
                candidates.append(a)
        candidates.sort(key=lambda a: g.marks[a])
        pool_records.append(dict(side=side, eligible=len(candidates), kept=min(len(candidates), c['frame_candidates_per_side'])))
        candidates = candidates[:c['frame_candidates_per_side']]
        edges = set()
        for a, b in itertools.combinations(candidates, 2):
            if (g.r[a, b] or g.r[b, a]) and counts.good(a, b):
                edges.add((a, b))
        # Every chain has exactly one middle event. Count-good adjacent
        # intervals imply a count-good outer interval by inclusion; check all
        # three anyway, and retain the original mark order for algebra/ties.
        before = {b: [] for b in candidates}; after = {b: [] for b in candidates}
        for a, b in edges:
            low, high = (a, b) if g.r[a, b] else (b, a)
            after[low].append(high); before[high].append(low)
        chain_triples = []
        for middle in candidates:
            for a in before[middle]:
                for b in after[middle]:
                    triple = tuple(sorted((a, middle, b), key=lambda x: g.marks[x]))
                    if all(pair in edges for pair in itertools.combinations(triple, 2)):
                        chain_triples.append(triple)
        chain_triples.sort(key=lambda row: tuple(g.marks[a] for a in row))
        for triple in chain_triples:
            h, _ = gram_and_vectors(counts.q, triple, root, [], 1.)
            hh = [gram_and_vectors(lambda a, b, j=j: counts.q(a, b, j), triple, root, [], 1.)[0] for j in (0, 1)]
            matrices.append(h); half_matrices.append(hh); triples.append(triple); directions.append(side)
    funnel = dict(pools=pool_records, count_qualified_triples=len(triples), signature_condition=0, stable_gram=0)
    if not triples:
        return [], funnel
    matrices = np.asarray(matrices)
    ev, u = np.linalg.eigh(matrices)
    absolute = np.abs(ev)
    with np.errstate(divide='ignore', invalid='ignore'):
        condition = np.max(absolute, axis=1)/np.min(absolute, axis=1)
    valid = (ev[:, 0] < 0) & (ev[:, 1] > 0) & (condition <= guards['guard_max_condition'])
    valid_ids = np.flatnonzero(valid)
    funnel['signature_condition'] = len(valid_ids)
    out = []
    for i in valid_ids:
        t = (u[i]/np.sqrt(absolute[i])[None, :]).T
        errors = [float(np.linalg.norm(t@hh@t.T-ETA)/np.sqrt(3)) for hh in half_matrices[i]]
        signatures = [bool(np.linalg.eigvalsh(hh)[0] < 0 < np.linalg.eigvalsh(hh)[1]) for hh in half_matrices[i]]
        if not all(signatures) or max(errors) > guards['guard_max_gram_error']:
            continue
        out.append(dict(landmarks=list(triples[i]), side=directions[i], condition=float(condition[i]),
                        gram=matrices[i], transform=t, half_gram_errors=errors))
    out.sort(key=lambda f: (f['condition'], tuple(float(g.marks[a]) for a in f['landmarks'])))
    funnel['stable_gram'] = len(out)
    return out, funnel


def construct(g, counts, root, temporal, inner, probes, frame, pool, scale, c, guards):
    lm = frame['landmarks']
    # One certificate with all point counts would reject otherwise usable subsets.
    # Evaluate point admissibility before forming the complete support certificate.
    points = list(temporal)+[b for side in pool for b in side]
    admissible = [b for b in points if all((g.r[a, b] or g.r[b, a]) and counts.good(a, b) for a in lm)]
    diagnostic = dict(count_compatible=len(admissible), radius_compatible=[0, 0], stable_features=[0, 0])
    if any(b not in admissible for b in temporal):
        return None, {**diagnostic, 'reason': 'temporal_count'}
    h, v = gram_and_vectors(counts.q, lm, root, admissible, 1.)
    t = frame['transform']; z = (t@v).T
    half_z = [(t@gram_and_vectors(lambda a, b, j=j: counts.q(a, b, j), lm, root, admissible, 1.)[1]).T for j in (0, 1)]
    lookup = {b: i for i, b in enumerate(admissible)}
    axis = z[lookup[temporal[1]]]-z[lookup[temporal[0]]]
    norm = float(axis@ETA@axis)
    if norm >= 0:
        return None, {**diagnostic, 'reason': 'observer_not_timelike'}
    times = -(z@ETA@axis)/math.sqrt(-norm)
    if not times[lookup[temporal[0]]] < 0 < times[lookup[temporal[1]]]:
        return None, {**diagnostic, 'reason': 'temporal_not_straddling'}
    errors = np.maximum(*[np.linalg.norm(zz-z, axis=1)/np.maximum(np.linalg.norm(z, axis=1), 1e-12) for zz in half_z])
    if any(errors[lookup[b]] > guards['guard_max_feature_error'] for b in temporal):
        return None, {**diagnostic, 'reason': 'temporal_feature'}
    transverse = np.sqrt(np.maximum(0., times**2+np.einsum('ni,ij,nj->n', z, ETA, z)))
    chosen = []
    for side_index, candidates in enumerate(pool):
        kept = []
        for b in candidates:
            if b not in lookup:
                continue
            i = lookup[b]
            tau = math.sqrt(counts.q(root, b))
            if transverse[i] > (2/3)*tau:
                continue
            diagnostic['radius_compatible'][side_index] += 1
            if errors[i] > guards['guard_max_feature_error']:
                continue
            diagnostic['stable_features'][side_index] += 1
            kept.append(b)
        chosen.append(kept[:c['maximum_support_per_side']])
    if min(map(len, chosen)) < c['minimum_support_per_side']:
        return None, {**diagnostic, 'reason': 'insufficient_support'}
    support = sorted(list(temporal)+chosen[0]+chosen[1], key=lambda b: g.marks[b])
    cert = certificate(g, counts, root, temporal, lm, support, guards)
    if cert['status'] != 'ok' or not cert['guard']['passed']:
        return None, {**diagnostic, 'reason': 'complete_guard'}
    dc = design_check(cert['features'], scale, c)
    if not dc['passed']:
        return None, {**diagnostic, 'reason': 'design', 'design_rank': dc['rank'], 'design_condition': dc['condition']}
    witness = dict(root=root, temporal=list(temporal), landmarks=lm, frame_side=frame['side'],
                   support=support, support_sides=chosen, scale=scale, certificate=cert,
                   design=dc, point_feature_errors=[float(errors[lookup[b]]) for b in support])
    return witness, {**diagnostic, 'reason': 'passed'}


def select(g, root, chain, inner, probes, colours, rho, c, guards, old_scale):
    counts = Counts(g, colours, rho, guards)
    out = dict(status='search_exhausted', selected=None, shells=[], old_scale=old_scale)
    middle = chain.index(root)
    paths = [list(reversed(chain[:middle])), chain[middle+1:]]
    for k in c['count_shell_lower_bounds']:
        scale = (k/(rho*VOLUME))**(1/3)
        temporal = [next((b for b in path if b not in probes and counts.values(root, b)[0] >= c['temporal_count_multiplier']*k and counts.good(root, b)), None) for path in paths]
        if any(b is None for b in temporal):
            out['shells'].append(dict(lower_count=k, scale=scale, scale_ratio=scale/old_scale,
                                     temporal=temporal, status='temporal_count_obstruction', tested_frames=0,
                                     reasons={'temporal_count_obstruction': 1}, trials=[]))
            continue
        candidates, funnel = frames(g, counts, root, temporal, probes, c, guards)
        pool, available = [], []
        for future in (False, True):
            row = []
            for b in inner:
                if b == root or b in temporal or b in probes:
                    continue
                if not (g.r[root, b] if future else g.r[b, root]):
                    continue
                if k <= counts.values(root, b)[0] < c['shell_upper_multiplier']*k and counts.good(root, b):
                    row.append(int(b))
            row.sort(key=lambda b: g.marks[b])
            available.append(len(row)); pool.append(row[:c['support_candidates_per_side']])
        record = dict(lower_count=k, scale=scale, scale_ratio=scale/old_scale, temporal=temporal,
                      status='searched', frames=funnel,
                      candidates=available, kept=list(map(len, pool)), tested_frames=0,
                      stable_frames_omitted=max(0, len(candidates)-c['maximum_frames_per_shell']),
                      reasons={}, trials=[])
        out['shells'].append(record)
        if min(map(len, pool)) < c['minimum_support_per_side']:
            record['reasons']['insufficient_count_pool'] = 1
            continue
        for f in candidates[:c['maximum_frames_per_shell']]:
            witness, diagnostic = construct(g, counts, root, temporal, inner, probes, f, pool, scale, c, guards)
            record['tested_frames'] += 1
            reason = diagnostic['reason']; record['reasons'][reason] = record['reasons'].get(reason, 0)+1
            record['trials'].append(dict(landmarks=f['landmarks'], condition=f['condition'], **diagnostic))
            if witness is not None:
                witness.update(lower_count=k, scale_ratio=scale/old_scale)
                return {**out, 'status': 'selected', 'selected': witness}
    return out


def audit(g, selected, colours, rho, guards):
    if selected is None:
        return dict(status='not_selected', passed=False)
    counts = Counts(g, colours, rho, guards)
    result = certificate(g, counts, selected['root'], selected['temporal'],
                         selected['landmarks'], selected['support'], guards)
    return dict(status=result['status'], passed=result['status'] == 'ok' and result['guard']['passed'], certificate=result)
