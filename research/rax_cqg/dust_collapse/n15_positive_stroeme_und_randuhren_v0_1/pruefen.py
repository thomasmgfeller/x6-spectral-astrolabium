"""Replay the interval certificates, optimal transport construction and optional numerical controls."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import fluss
import ablesung

ROOT=Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_text())


def main(recompute):
    if not __debug__:
        raise ValueError('Für die Nachrechnung Python ohne -O verwenden.')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Abweichende Datei {name}')
    cert=fluss.run()
    assert cert==read('zertifikate.json')
    design=ablesung.design(cert)
    example=read('zaehltest.json')
    assert example['design']==design
    cp=read('basis/quellen/inputs/checkpoints.json')
    assert len(cp)==60 and all(row['checkpoint_id']=='P3' and row['execution']=='NOT_RUN' for row in cp)
    ref=read('gegenrechnung.json')
    if recompute:
        import gegenrechnung
        actual=gegenrechnung.run()
    else:
        actual=ref
    assert actual['rational_source_checks']==90
    assert all(abs(r['relative_phase_rad'])<1e-12 for r in actual['empty_interior'].values())
    for row in actual['linear_programs']:
        assert row['cover']['infeasible']
        for model in ('all','kernel'):
            lo,hi=map(F,cert['levels']['0'][model])
            v=row[model]
            assert float(lo)<v['objective']<float(hi) and abs(v['objective']-v['dual_objective'])<1e-10
    for model in ('all','kernel'):
        lo,hi=map(F,cert['at_midpoint'][model]['minimum'])
        assert float(lo)<actual['linear_programs'][1][model]['objective']<float(hi)
    for tag,rows in actual['quadrature_by_level_order'].items():
        level=tag.split('_')[0]
        assert len(rows)==15
        for g,v in rows.items():
            a,b=map(F,cert['levels'][level]['ports'][g]['range'])
            assert float(a)<v['charge_from_phase']<float(b)
            assert abs(v['charge_from_phase']-ref['quadrature_by_level_order'][tag][g]['charge_from_phase'])<2e-10
            assert 0<v['visibility']<=1
    q=actual['quadrature_by_level_order']
    assert all(abs(q['0_3'][g]['charge_from_phase']-q['0_4'][g]['charge_from_phase'])<1e-9 for g in q['0_3'])
    for factor,channels in actual['future_density_scale_controls'].items():
        for g,v in channels.items():
            assert abs(v['charge_from_phase']/float(factor)-q['0_3'][g]['charge_from_phase'])<1e-8
    if recompute:
        replay=ablesung.simulate(design,actual)
        if replay['numpy_version']==example['counting_example']['numpy_version']:
            assert replay==example['counting_example']
    print('PASS · vier Breiten, zwei scharfe Flussminima, sieben Randaufteilungen, Vakuum und P3-Register.')
    if recompute:
        print('LP-Gegenrechnung, endliche Quellenarme und synthetische Zählung neu ausgeführt.')
    print('Physischer P3-Lauf: 60 NOT_RUN.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--numerik',action='store_true',help='Lineare Programme und Quadratur mit SciPy und NumPy wiederholen')
    main(parser.parse_args().numerik)
