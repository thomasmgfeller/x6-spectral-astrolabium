"""Reconstruct the inputs of the fixed-past experiment from its published archive."""
from contextlib import contextmanager
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json,subprocess,sys

ROOT=Path(__file__).resolve().parent
PIN='1401aeb3ddb4c7989038ccbbbd1d1c935bb0eb345767fce5e9037568a976f81c'
FUTURE=(('y',8),('y',9),('y',10),('w',7),('w',8),('w',9),('w',10))
def name(axis):return axis[0]+str(axis[1])

@contextmanager
def inputs():
    pkg=ROOT/'basis/Sendervorlauf.zip'
    assert sha256(pkg.read_bytes()).hexdigest()==PIN
    with TemporaryDirectory() as td, ZipFile(pkg) as z:
        z.extractall(td)
        sys.path.insert(0,td)
        from versuchsbasis import inputs as previous
        old=json.loads((Path(td)/'Ergebnisse.json').read_text())
        with previous() as (_,bundle,seeds):
            dirs,_,_,rel,_,coeff,free=bundle
            data=subprocess.check_output([sys.executable,'-B',str(dirs[6]/'eichpunkt.py'),'0','0'])
            assert sha256(data).hexdigest()==old['collar_sha256']['0']
            goals=old['matched_currents'][0]['goals']
            assert all(t['goals']==goals for t in old['matched_currents'])
            yield seeds['0']['0'],json.loads(data),coeff,free,rel,list(map(F,goals)),old
