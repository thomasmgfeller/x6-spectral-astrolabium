"""Integer prediction and an auditable two-stage N19 readout."""
import argparse
import json
from pathlib import Path
from n19_pr395 import instrument

IDENTITY = ('kind', 'device', 'campaign', 'clock_reference')


def ceildiv(a, b):
    return -((-a) // b)


def third_extrema(bands, curvature, fourth):
    """Return extremal compatible N3 for fixed N4, or None when unreachable."""
    (l1, u1), (l2, u2), (l3, u3) = bands
    ends = []
    for p in (0, 1):
        # z=N3=2s+p. For each s, the possible integer v=N2 form the
        # intersection of three intervals. The first N1 is then existential.
        low = [(0, l2), (1, ceildiv(p+l1-curvature, 2)), (4, 2*p-fourth-curvature)]
        high = [(0, u2), (1, (p+u1+curvature)//2), (4, 2*p-fourth+curvature)]
        lo, hi = ceildiv(l3-p, 2), (u3-p)//2
        for a, b in low:
            for d, e in high:
                slope, bound = a-d, e-b
                if slope > 0:
                    hi = min(hi, bound//slope)
                elif slope < 0:
                    lo = max(lo, ceildiv(bound, slope))
                elif bound < 0:
                    lo, hi = 1, 0
        if lo <= hi:
            ends.extend((2*lo+p, 2*hi+p))
    return (min(ends), max(ends)) if ends else None


def projection(bands, c, fourth_hull):
    rows = {}
    for w in range(fourth_hull[0], fourth_hull[1]+1):
        z = third_extrema(bands, c, w)
        if z is not None:
            rows[w] = (2*w-z[1]-c, 2*w-z[0]+c)
    return rows


def hull(rows):
    return [min(lo for lo, _ in rows), max(hi for _, hi in rows)]


def center_radius(interval):
    lo, hi = interval
    mid = (lo+hi)//2
    return mid, hi-mid


def advance(controls, holdout, shot):
    from referenzprotokoll import digit, fingerprint, forecast, integer
    old = forecast(controls)
    if old['status'] == 'NOT_MEASURED':
        return old
    if (not isinstance(shot, str) or not shot.strip() or shot == old['shot'] or
        any(holdout.get(k) != old[k] for k in (*IDENTITY, 'shot', 'reference_id')) or
        not integer(holdout.get('index')) or holdout['index'] != old['target_index']):
        raise ValueError('fourth shot or frozen reference mismatch')
    if (holdout.get('source_setting') != 'zero' or holdout.get('usable') is not True or
        holdout.get('saturated') is not False):
        raise ValueError('fourth shot must be a usable source-off control')
    w, err = holdout['code'], holdout['extra_error_codes']
    if not digit(w) or not integer(err) or err < 0 or not digit(w-err) or not digit(w+err):
        raise ValueError('invalid holdout band')
    bands = [(r['code']-r['extra_error_codes'], r['code']+r['extra_error_codes'])
             for r in controls['controls']]
    rows = projection(bands, controls['curvature_codes'], old['range_codes'])
    # The forecast budget in PR395 bounds len(rows) even for wide input bands.
    matches = [v for v in rows if w-err <= v <= w+err]
    diag = {'reachable_fourth': sorted(rows), 'fourth_band': [w-err, w+err],
            'fifth_before_holdout': hull(rows.values()), 'physical_P3': '60 NOT_RUN'}
    if not matches:
        return {**diag, 'status': 'INCOMPATIBLE_HOLDOUT'}
    if len(matches) != 2*err+1:
        return {**diag, 'status': 'PARTIAL_HOLDOUT'}
    interval = hull([rows[v] for v in matches])
    mid, rad = center_radius(interval)
    if not all(map(digit, interval)) or rad > old['allowed_error_codes']:
        return {**diag, 'status': 'OUTSIDE_BUDGET_OR_RANGE', 'range_codes': interval}
    ref = {k: old[k] for k in IDENTITY}
    ref.update(status='CONDITIONAL_MODEL_REFERENCE', shot=shot, target_index=old['target_index']+1,
               momentum_bound=old['momentum_bound'], baseline_code=mid, range_codes=interval,
               worst_error_codes=rad, allowed_error_codes=old['allowed_error_codes'],
               control_record_sha256=fingerprint(controls), fourth_record_sha256=fingerprint(holdout),
               previous_reference_id=old['reference_id'])
    ref['reference_id'] = fingerprint(ref)
    return {**diag, 'status': 'READY_CONDITIONAL', 'reference': ref}


def classify(ref, receiver, memory, received):
    from referenzprotokoll import emit, late_read, integer
    if any(not integer(row.get('target_index')) for row in (receiver, memory, received)):
        raise ValueError('invalid shot index')
    sent = emit(ref, receiver)
    if not integer(received.get('bit')) or received != sent:
        raise ValueError('transmitted and received packets differ')
    out = late_read(ref, memory, received)
    return {'shot': ref['shot'], 'reference_id': ref['reference_id'], 'bit': received['bit'],
            'source_label': out['source_label'], 'kind': out['kind'], 'physical_P3': '60 NOT_RUN'}


def main():
    import sys
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action', required=True)
    cal = sub.add_parser('referenz')
    cal.add_argument('controls', type=Path)
    cal.add_argument('holdout', type=Path)
    cal.add_argument('shot')
    read = sub.add_parser('lesen')
    for name in ('decision', 'receiver', 'memory', 'received'):
        read.add_argument(name, type=Path)
    args = p.parse_args()
    def load(path):
        return json.loads(path.read_bytes())
    with instrument():
        if args.action == 'referenz':
            result = advance(load(args.controls), load(args.holdout), args.shot)
        else:
            decision = load(args.decision)
            if decision.get('status') != 'READY_CONDITIONAL':
                raise ValueError('missing conditional reference')
            result = classify(decision['reference'], load(args.receiver), load(args.memory), load(args.received))
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get('status') in {'INCOMPATIBLE_HOLDOUT','PARTIAL_HOLDOUT','OUTSIDE_BUDGET_OR_RANGE'}:
        sys.exit(2)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise SystemExit('UNRESOLVED '+str(exc))
