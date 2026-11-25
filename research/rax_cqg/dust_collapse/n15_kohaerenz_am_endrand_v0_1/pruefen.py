"""Offline verification of the complete packet, with no external dependencies."""
from hashlib import sha256
import json
from pathlib import Path

from endrand import run as interval_run
from quadratur import run as numerical_run

ROOT=Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_text())


def within(value,interval,tol=0):
    low,high=map(float,interval)
    assert low-tol<=value<=high+tol,(value,interval)


def check_numeric(data,cert):
    assert set(data)=={'single','collective'}
    for kind,domains in data.items():
        expected={'published','wide_control'}
        if kind=='collective':expected.add('same_center_8_9')
        assert set(domains)==expected
        for name,classes in domains.items():
            assert set(classes)=={'-1','1'}
            for side,rows in classes.items():
                assert [x['nodes_per_output'] for x in rows]==[2,3]
                for row in rows:
                    if name!='same_center_8_9':
                        within(row['trace'],cert['distinguishability'][kind][name][side]['trace_distance'])
                    if kind=='collective':
                        b=cert['joint_readout'][name][side]
                        within(row['joint_difference'],b['coherent_minus_mixture_probability'])
                        for ran,line in zip(b['tomography_matrix'],row['tomography_matrix']):
                            for entry,x in zip(ran,line):within(x,entry,1e-14)
                        if row['nodes_per_output']==3 and name!='published':
                            r,i=row['recovered_gamma']
                            assert abs(r-.37)<1e-7 and abs(i+.42)<1e-7


def main():
    if not __debug__:raise RuntimeError('Ohne -O aufrufen.')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert digest==sha256((ROOT/name).read_bytes()).hexdigest(),name
    for name,meta in read('Herkunft.json')['files'].items():
        assert meta['sha256']==sha256((ROOT/name).read_bytes()).hexdigest(),name
    p3=json.loads(next((ROOT/'basis').rglob('p3.json')).read_text())
    assert len(p3)==60 and all(r['execution']=='NOT_RUN' and r['checkpoint_id']=='P3' for r in p3)
    cert=interval_run()
    assert cert==read('ergebnisse.json')
    for data in [read('quadratur.json'),numerical_run()]:check_numeric(data,cert)
    print('PASS – Quellen, 13 exakte Rückrechnungen, Randzustände beider Zweigpaare')
    print('PASS – drei Dichteöffnungen, zwei Klassen, zwei Quadraturen, komplexe Kohärenz aus simulierten Endhäufigkeiten')
    print('P3 – 60 von 60 physischen Prüfpunkten NOT_RUN')


if __name__=='__main__':
    main()
