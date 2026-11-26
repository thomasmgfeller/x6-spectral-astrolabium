"""Independent source-off holdout, precursor cross-check and one explicit failed pulse readout."""
from fractions import Fraction as F
from math import floor
from geometrische_uhr import interval_analog, qcode
from kontrollprobe import stationary


def loaded_codes(u, h, step, bias, geometry, load):
    from quelle import SCALE
    centers = [code*step for code in (u, h)]
    delta = step/2 + bias
    for center, key in zip(centers, ('u_cover', 'h_cover')):
        low, high = map(F, geometry[key])
        if not low <= center-delta <= center+delta <= high:
            raise ValueError('precursor inputs outside certified box')
    _, bare, _ = interval_analog(u, h, step, bias)
    from empfangsbit import STEP
    lo, hi = (floor(F(end, SCALE)/STEP+F(1, 2)) for end in (bare.lo, bare.hi))
    return (lo, hi), (lo+load[0], hi+load[1])


def overlap(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return [lo, hi] if lo <= hi else None


def run(previous, early, geometry, comparison, controls):
    from proben import samples
    from referenzwechsel import displaced
    from empfangsbit import K0, classify, late_code, receiver_bit
    from nullreferenz import digit
    _, y, w = next(row for row in samples(previous, early)[0] if row[0]=='quarter')
    step = F(1, 10**12)
    matched = next(row for row in comparison if row['m']==112)
    load = matched['null_load_codes'][str(K0)]
    time_forecast = controls['example']['forecast']['range_codes']
    result = []
    for shift in (F(0), F(1, 10**6)):
        yy, ww = displaced(y, w, shift) if shift else (y, w)
        u, h = [qcode(yy[i], step) for i in (15,17)]
        bare, loaded = loaded_codes(u, h, step, F(0), geometry, load)
        zero, _, _ = stationary(yy, ww, 0, (-51,19,7), 'positive_bridge', K0, -K0, (0,0,0))
        actual = digit(zero['y'][18])
        assert loaded[0] <= actual <= loaded[1]
        cross = overlap(loaded, time_forecast)
        assert (cross is None) == bool(shift)
        if not shift:
            assert cross[0] <= actual <= cross[1] and actual==controls['true_target_null_code']
            assert overlap(bare, time_forecast) is None
        result.append(dict(shift=str(shift), u_code=u, h_code=h, bare=bare, loaded=loaded,
                           earlier_forecast=time_forecast, intersection=cross, fourth_zero=actual))
    # Trace one concrete momentum direction until a faithfully calibrated reader fails.
    # Every trial uses an exact loaded zero code, zero offsets, and the unchanged comparator.
    z, _, _ = stationary(y, w, 0, (0,0,0), 'positive_bridge', K0, -K0, (0,0,0))
    reference = digit(z['y'][18])
    rows = []
    for sign in (-1, 1):
        source = F(sign, 10**6)
        trials = []
        for m in range(112, 151):
            st, history, _ = stationary(y, w, source, (0,0,sign*m), 'positive_bridge', K0, -K0, (0,0,0))
            b = receiver_bit(digit(st['y'][18]), reference)
            late = late_code(digit(st['y'][7]), digit(history[2][7]), 0, reference)
            label = classify(b, late)
            trials.append(dict(m=m, bit=b, signed_late_code=late,
                               result='UNRESOLVED' if label is None else str(label)))
            if label != source:
                break
        assert len(trials)>1 and trials[-1]['result']!=str(source)
        rows.append(dict(source=str(source), tests=trials))
    return dict(precursor_step=str(step), precursor_bias='0', null_load_codes=load,
                fourth_null_trials=result, momentum_direction_trials=rows)


if __name__=='__main__':
    import json
    from n19_archiv394 import inputs, ROOT
    def read(name):
        return json.loads((ROOT/(name+'.json')).read_bytes())
    with inputs() as (_, previous, early):
        report=run(previous,early,read('Geometrische_Nulluhr'),read('Vergleich'),read('Protokollkontrollen'))
    print(json.dumps(report,indent=2,sort_keys=True))
