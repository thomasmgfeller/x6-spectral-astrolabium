"""Offline verification of window measurements, the finite candidate census and extension."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

from ordnungsfenster import audit, WINDOWS
from schalenblock import time_block

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_bytes())


def results():
    if not __debug__:
        raise RuntimeError('Python ohne Optimierung starten.')
    for name, source in read('Quellen.json')['files'].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest() == source['sha256']
    geometry = time_block()
    table = read('basis/Zwei_Massen.json')
    for c in geometry['cases']:
        target = tuple(map(F,table['p3_reference_check']['reference'][c['M']]['radius_bounds_exact']))
        assert max(target[0],c['reference_radius'][0]) <= min(target[1],c['reference_radius'][1])
        for t in c['blocks']:
            assert F(95,100)*target[1] <= t['radius'][0] <= target[0] <= target[1] <= t['radius'][1] <= F(105,100)*target[0]
    a = audit(read('basis/Driftzertifikat.json'))
    assert len(a['mixed_pairs']) == 19 and len(a['anchored_quartets']) == 143
    assert len(a['cell_results']) == 21
    assert all(low < F(q) < high for key, low, high in [
        ('mixed_minimum_halfwidth',F('0.66544465213129'),F('0.66544465213130')),
        ('diamond_minimum_halfwidth',F('0.80434782608695'),F('0.80434782608696'))] for q in a[key])
    assert [w['old_past'] for w in a['all_predecessor_ideals']] == [[0,1,2,15,16],[0,1,2,15,16,17]]
    assert F(a['all_predecessor_ideals'][0]['range'][1]) < F('-20.73')
    assert F(a['all_predecessor_ideals'][1]['range'][0]) < 0 < F(a['all_predecessor_ideals'][1]['range'][1])
    assert a['least_extension']['gradient_range'] == a['all_predecessor_ideals'][0]['range']
    for r in a['cell_results']:
        for h in WINDOWS:
            row = r['windows'][str(h)]
            assert row['guaranteed'] == row['not_excluded']
            assert row['guaranteed'] == a['cell_results'][0]['windows'][str(h)]['guaranteed']
            assert row['guaranteed']['mixed'] == row['guaranteed']['diamonds'] == []
        assert r['windows']['1/64']['guaranteed']['events'] == [16,18]
        assert {15,17}.isdisjoint(r['windows']['1/2']['guaranteed']['events'])
        assert F(r['receiver_identity']['receiver_gradient'][0]) > F('2.0853e-10')
        assert F(r['receiver_identity']['slope'][1]) < F('-3.414')
    p3 = read('basis/P3.json')
    rows = [dict(checkpoint_id=r['checkpoint_id'], **r['checkpoint_context']) for r in p3 if r['checkpoint_context']['x']=='1/2' and r['checkpoint_context']['M'] in ('1/4','4')]
    assert len(rows) == 8 and {(r['M'],r['density_ratio']) for r in rows} == {(m,d) for m in ('1/4','4') for d in (1,2,4,8)}
    assert len(p3)==60 and all(r['execution']=='NOT_RUN' for r in p3)
    status = read('basis/Eichstand.json')['physical_CST']
    assert status['independent_mass_pair'] is status['physical_vacuum'] is status['gain'] is None
    assert read('basis/Paar.json')['operational_radius'] is None
    assert all(table['physical'][k] is None for k in ('radius_M_1_4','radius_M_4','weight_uniform_radius_intervals'))
    return {'ltb':geometry,'n19':a,'P3':{'execution':'NOT_RUN','eligibility':'HOLD_NOT_ELIGIBLE',
            'physical_rows_at_target':rows,'register_size':len(p3),'physical_radius':None}}


def serialize(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def raw(report):
    return (json.dumps(report,default=serialize,
                       ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()


if __name__=='__main__':
    for name in ('SHA256SUMS','Pruefplan.sha256','Ergaenzung.sha256','Ergaenzung_Anbindungen.sha256'):
        for line in (ROOT/name).read_text().splitlines():
            digest, path = line.split('  ',1)
            if sha256((ROOT/path).read_bytes()).hexdigest() != digest:
                raise ValueError('Abweichende Datei '+path)
    if raw(results()) != (ROOT/'Ergebnisse.json').read_bytes():
        raise ValueError('Abweichende Ergebnisse')
    print('PASS · 4 klassische Radiusintervalle · 21 N19-Modellzellen · 2 ergänzende Anbindungen geprüft.')
    print('Physische Radiuswerte am Zielschnitt offen. 60 P3-Einträge NOT_RUN.')
