"""Exact study replay. Usage: python -B pruefen.py"""
import gzip
import hashlib
import json
from pathlib import Path
import sys

import aufnahme
import dynamik
import gegenprobe
import strom
from auslese import read

ROOT=Path(__file__).resolve().parent


def serialized(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()


def main(generate):
    if not __debug__:raise SystemExit('Python ohne -O starten.')
    for name in ('Pruefplan','Zusatzplan','Stromkontrolle'):
        assert hashlib.sha256((ROOT/(name+'.md')).read_bytes()).hexdigest()==(ROOT/(name+'.sha256')).read_text().split()[0]
    for name,row in json.loads((ROOT/'Herkunft.json').read_text())['inputs'].items():
        b=(ROOT/name).read_bytes()
        assert hashlib.sha256(b).hexdigest()==row['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
    geo=dynamik.geometry();r,q,roots=dynamik.selection();audit=gegenprobe.run(roots)
    scan,density=aufnahme.run(r,q);factor=scan['geometric_extension'][-1]['length']//96
    currents,edges=strom.run(r,q,factor)
    snapshots={v['acquisition']:v for v in scan['snapshots']}
    records={'scale':10**10,'density':density,'current':edges}
    encoded=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    raw=ROOT/'Radar_und_Uhrpulse.json.gz'
    if generate:raw.write_bytes(gzip.compress(encoded,mtime=0))
    assert gzip.decompress(raw.read_bytes())==encoded
    # Second pass on the serialized recording, no readout access to generator fields.
    blinded=json.loads(gzip.decompress(raw.read_bytes()))
    for key,d in blinded['density'].items():
        got=read(d['echo_arms'],d['length'],d['time'],d['inner'],d['outer'])
        assert got=={k:v for k,v in snapshots[key].items() if k!='acquisition'}
    current_summaries = {(row['length'], row['ticks']): row for row in currents['smooth']}
    for key, stations in blinded['current'].items():
        length, tick = map(int, key.split('_')[-2:])
        intervals = {int(j): strom.decode(records, tick, int(j)) for j, records in stations.items()}
        assert all(isinstance(value, tuple) for value in intervals.values())
        if key.startswith('sharp_'):
            assert {str(j): list(map(str, pair)) for j, pair in intervals.items()} == currents['sharp_activity_over_h']
            continue
        inner, outer = aufnahme.bands(length // 96)
        summary = current_summaries[length, tick]
        def mean_interval(band):
            return [sum(intervals[j][side] for j in band) / len(band) for side in (0, 1)]
        inner_mean = mean_interval(inner)
        outer_mean = mean_interval(outer)
        assert list(map(str, inner_mean)) == summary['inner_activity_over_h']
        assert list(map(str, outer_mean)) == summary['outer_activity_over_h']
        assert str(outer_mean[0] / inner_mean[1]) == summary['lower']
        assert str(outer_mean[1] / inner_mean[0]) == summary['upper']
    checkpoint=json.loads((ROOT/'basis/checkpoints.json').read_text())
    assert len(checkpoint)==60 and all(v['execution']=='NOT_RUN' for v in checkpoint)
    result={'geometry':geo,'spatial_ratio':str(r),'temporal_root':list(map(str,q)),'root_intervals':roots,
            'independent_checks':audit,'recurrence_check':dynamik.backward_patch(r,q),
            'density_readout':scan,'current_readout':currents,'raw_uncompressed_sha256':hashlib.sha256(encoded).hexdigest(),
            'density_records':sum(len(d['echo_arms']) for d in density.values()),
            'edge_records':sum(len(rec) for block in edges.values() for rec in block.values()),
            'physical_P3':'HOLD_NOT_ELIGIBLE','physical_records_unrun':len(checkpoint)}
    expected=ROOT/'Ergebnisse.json'
    if generate:expected.write_bytes(serialized(result))
    assert serialized(result)==expected.read_bytes()
    print('PASS: räumliche Auslese, 18 ursprüngliche Wirkungstests, unabhängige Wurzelzählung, 3168 Felder aus der Randrekursion.')
    print('Harte Kante verletzt die Uhrgleichung. Positives Vergleichsprofil liegt aussen unter 1 % auf dem erweiterten Träger. P3: 60 x NOT_RUN.')


if __name__=='__main__':
    if sys.argv[1:] not in ([],['--erzeugen']):raise SystemExit('Erwartet: python -B pruefen.py [--erzeugen]')
    main(bool(sys.argv[1:]))
