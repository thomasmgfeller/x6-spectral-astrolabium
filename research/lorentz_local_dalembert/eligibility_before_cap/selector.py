"""Intrinsic fourth-landmark search: eligibility precedes the geometry cap.

Only order, marks, interval counts and inherited A metadata enter this module.
The old accepted candidate set is a subset of the new one (see PROTOCOL.md).
SPDX-License-Identifier: Apache-2.0
"""
from collections import Counter
import eb_common
import numpy as np
from selection import pairs_for
from inference import four_geometry, normalize, design

def eligible_prefix(pool, predicate, cap):
    """Stable filtering then capping; also used by the finite proof control."""
    return [a for a in pool if predicate(a)][:cap]

def select_four(g, counts, selected, cfg):
    if selected is None: return dict(status='NO_BASE_SUPPORT', inventory=[])
    root = selected['root']; support = selected['support']; first = selected['landmarks']
    fixed = [root] + support + first
    excluded = set(fixed) | set(getattr(g, 'probes_for_check', []))
    inventory = []; candidates = []; funnel = Counter()
    for side, cones in [('past', g.pred), ('future', g.succ)]:
        common_bits = (1 << g.size)-1
        for b in [root]+support: common_bits &= cones[b]
        pool = []
        while common_bits:
            low = common_bits & -common_bits; common_bits ^= low
            a = low.bit_length()-1
            if a not in excluded: pool.append(a)
        pool.sort(key=lambda a: g.marks[a])
        eligible = []
        for rank, a in enumerate(pool):
            row = dict(candidate=a, side=side, raw_rank=rank, in_old_cap=rank < cfg['candidate_cap_per_side'])
            funnel['pool'] += 1
            bad = [b for b in fixed if not (g.r[a,b] or g.r[b,a])]
            if bad:
                row.update(status='INCOMPARABLE', witness=bad[0])
            else:
                values = [counts.values(a,b) for b in fixed]
                low = [(b, list(v)) for b,v in zip(fixed,values) if v[0] < counts.guards['guard_min_interval']]
                half = [(b, list(v)) for b,v in zip(fixed,values) if min(v[1:]) < counts.guards['guard_min_half_interval']]
                if low or half:
                    row.update(status='FULL_COUNT' if low else 'HALF_COUNT', witness=(low or half)[0])
                else:
                    row.update(status='COUNT_ELIGIBLE', eligible_rank=len(eligible), endpoint_counts=values)
                    eligible.append(a)
            inventory.append(row); funnel[row['status']] += 1
        chosen = eligible_prefix(pool, set(eligible).__contains__, cfg['candidate_cap_per_side'])
        candidates.extend(chosen)
        for row in inventory:
            if row['side'] == side and row['status'] == 'COUNT_ELIGIBLE':
                row['within_geometry_cap'] = row['candidate'] in chosen
    by_id = {r['candidate']:r for r in inventory}
    accepted = []; funnel['geometry_candidates'] = len(candidates)
    for a in candidates:
        row = by_id[a]
        landmarks = first+[a]; pairs = pairs_for(landmarks, root, support)
        nodes = landmarks+[root]+support
        packet = dict(root=root, support=support, temporal=selected['temporal'], landmarks=landmarks,
                      pairs=pairs, scale=selected['scale'], full_order=g.r[np.ix_(nodes,nodes)].astype(bool))
        q = np.array([counts.q(u,v) for u,v in pairs])/selected['scale']**2
        h,z,_,_ = four_geometry(q,packet)
        try:
            _, condition = normalize(h)
            row['landmark_condition'] = condition
            if condition > cfg['maximum_landmark_condition']: raise ValueError('landmark condition')
            funnel['lorentz_eligible'] += 1
            d = design(z[5:]); dc = float(np.linalg.cond(d))
            row['design_condition'] = dc if np.isfinite(dc) else None
            if np.linalg.matrix_rank(d) != 9 or dc > cfg['maximum_design_condition']: raise ValueError('moment rank/condition')
            funnel['moment_eligible'] += 1
            row.update(geometry_status='ELIGIBLE', packet=packet, pair_counts=[counts.values(u,v) for u,v in pairs])
            accepted.append((condition, float(g.marks[a]), packet, [counts.values(u,v)[0] for u,v in pairs], dc))
        except (ValueError,np.linalg.LinAlgError) as exc:
            row.update(geometry_status='GEOMETRY_HOLD', reason=str(exc))
    out = dict(status='NO_FOUR_LANDMARK_FRAME', funnel=dict(funnel), inventory=inventory)
    if accepted:
        accepted.sort(key=lambda r:r[:2]); condition,mark,packet,n,dc = accepted[0]
        out.update(status='SELECTED', packet=packet, selection_counts=n, landmark_condition=condition, design_condition=dc)
    return out
