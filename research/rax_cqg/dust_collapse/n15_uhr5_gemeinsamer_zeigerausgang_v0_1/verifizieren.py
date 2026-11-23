"""Verify archive bytes and replay the proof and both quadratures."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent


def run(name):
    result=subprocess.check_output([sys.executable,'-B',str(ROOT/(name+'.py'))],cwd=ROOT,text=True)
    return json.loads(result)


def main():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Datei mit abweichendem SHA-256: '+name)
    if run('schranke')!=json.loads((ROOT/'schranke.json').read_text()):
        raise ValueError('Abweichung bei rationaler Schranke')
    current=run('zeiger')
    archived=json.loads((ROOT/'zeiger.json').read_text())
    assert current.keys()==archived.keys()
    for case,values in current.items():
        assert values.keys()==archived[case].keys()
        for key,computed in values.items():
            np.testing.assert_allclose(computed,archived[case][key],atol=3e-14,rtol=5e-11,
                                       err_msg=case+'/'+key)
    print('PASS: SHA-256, rationaler Einschluss, zwei Quadraturen, vier Phasen und Anschlusszeuge.')


if __name__=='__main__':
    main()
