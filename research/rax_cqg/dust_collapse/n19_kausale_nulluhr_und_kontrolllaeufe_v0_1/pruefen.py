"""Offline byte-for-byte replay of the N19 null-reference tests and their parent archive."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from n19_archiv394 import ROOT, inputs


def compare(name, result):
    raw = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    if raw != (ROOT/(name+'.json')).read_bytes():
        raise ValueError('abweichendes Ergebnis: '+name)
    print('PASS', name, flush=True)


def must_reject(action, *args):
    try:
        action(*args)
    except ValueError:
        return
    raise AssertionError('ungültige Daten akzeptiert')


def main():
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    for manifest in [ROOT/'SHA256SUMS', *sorted(ROOT.glob('*.sha256'))]:
        for line in manifest.read_text().splitlines():
            value, name = line.split('  ', 1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==value, name
    with inputs() as (parent, previous, early):
        subprocess.run([sys.executable, '-B', 'pruefen.py'], cwd=parent, check=True)
        import geometrische_uhr, doppelwort, kalibriervergleich, kontrollprobe
        import nulluhr_gegenprobe as gegenprobe
        import referenzprotokoll as protocol
        geo = geometrische_uhr.run(previous, early)
        compare('Geometrische_Nulluhr', geo)
        lo, hi = geo['native_null_digits']
        assert hi-lo==1_000_000 and geo['prefix']==[0,1,2,15] and len(geo['backgrounds'])==16
        double = doppelwort.run(previous, early)
        compare('Gleiche_Anzeigen', double)
        assert all(row['same_at_18'] and row['same_at_7'] for row in double['joint'])
        assert sum(F(row['max_abs_y'])<=64 for row in double['joint'])==2
        comp = kalibriervergleich.run(previous, early, geo)
        compare('Vergleich', comp)
        by_m = {row['m']:row for row in comp}
        for radius in (0,48,64,96,112):
            summary = by_m[radius]['paired_summary']
            assert [summary[k]['digital_pass'] for k in ('registered','held_out')]==[144,48]
        assert protocol.model_budgets(96)==38 and protocol.model_budgets(112)==11
        assert [by_m[117]['correlated_rounding'][k]['digital_pass'] for k in ('registered','held_out')]==[144,48]
        assert by_m[117]['correlated_rounding']['registered']['extra_plateau_budget']==0
        ctrl = kontrollprobe.run(previous, early)
        compare('Protokollkontrollen', ctrl)
        assert ctrl['integer_solver']['enumerated_cases']==10125 and ctrl['geometric_finite_trials']==384
        assert len(ctrl['all_arms'])==3 and len(ctrl['bad_controls'])==7
        ex = ctrl['example']
        for name, key in [('Nullserie','control_input'),('Empfang','receiver'),('Speicher','late')]:
            compare('Beispiel_'+name, ex[key])
        forecast = protocol.forecast(ex['control_input'])
        pkt = protocol.emit(forecast, ex['receiver'])
        assert protocol.late_read(forecast,ex['late'],pkt)['source_label']=='1/1000000'
        must_reject(protocol.emit, {**forecast, 'baseline_code':forecast['baseline_code']+1}, ex['receiver'])
        must_reject(protocol.emit, forecast, {**ex['receiver'], 'shot':'other'})
        must_reject(protocol.late_read, forecast, ex['late'], {**pkt,'reference_id':'other'})
        must_reject(protocol.late_read, forecast, ex['late'], {**pkt,'bit':True})
        must_reject(protocol.forecast,{**ex['control_input'],'momentum_bound':118})
        assert protocol.forecast(json.loads((ROOT/'Messstand.json').read_bytes()))['status']=='NOT_MEASURED'
        cross = gegenprobe.run(previous, early, geo, comp, ctrl)
        compare('Gegenprobe', cross)
        assert cross['fourth_null_trials'][1]['intersection'] is None
        assert all(r['tests'][-1]['m']==118 and r['tests'][-1]['result']=='UNRESOLVED'
                   for r in cross['momentum_direction_trials'])
    print('PASS N19-Nulluhr. Physische Eichmessungen: 0. P3: 60 NOT_RUN.', flush=True)


if __name__=='__main__':
    main()
