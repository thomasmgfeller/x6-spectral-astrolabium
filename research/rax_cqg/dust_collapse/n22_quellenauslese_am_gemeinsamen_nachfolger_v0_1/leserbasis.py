"""Extract the published chain and reconstruct the receiver order."""
from contextlib import contextmanager
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

ROOT = Path(__file__).resolve().parent
PIN = '9f0fb859f2a74897bb753fb890cb46d208347903dc215e8e81d26be8894c7bc0'
KEY = (216141,229383,0)
LIMIT = F(1,10**6)
SOURCES = (-LIMIT,F(0),LIMIT)


@contextmanager
def model():
    archive = ROOT/'basis/Randpraeparation.zip'
    assert sha256(archive.read_bytes()).hexdigest()==PIN
    names=['Gemeinsamer_Nachfolger','Einzelanbindung','Seriell','Nachfolger','Vorstudie','N22','N21','Ankerpaket']
    with TemporaryDirectory() as td:
        dirs=[]
        for index in range(len(names)+1):
            path=Path(td)/str(index)
            with ZipFile(archive) as z:
                z.extractall(path)
            dirs.append(path)
            if index<len(names):
                archive=path/'basis'/(names[index]+'.zip')
        sys.path[:0]=[str(dirs[i]) for i in (0,1,2,6)]+[str(dirs[8]/'basis')]
        from quellenpaket import model as native
        from ordnung22 import structure
        from empfangsordnungen import relation
        from anbindungen import coefficients, floyd
        from zeugnis import FREE, PROBES
        import json
        central=json.loads((dirs[1]/'Zeugenzentrum.json').read_text())
        with native() as (_,__,previous,early):
            from gemischt import ORDER
            from modell import setup
            y,w=setup(previous,early)
            rel,_=structure(ORDER,central['row'],'A')
            rel=relation({e for e in rel if 21 not in e},KEY[1],KEY[2])
            assert rel==floyd(rel) and len(rel)==152 and (19,21) in rel and (20,21) in rel
            assert (19,20) not in rel and (20,19) not in rel
            raw=coefficients(rel)
            assert {i:k for (i,j),k in raw.items() if j==21 and k}=={2:-8,15:16,16:-9,17:1,19:1,20:1}
            coeff=raw.copy()
            for edge in PROBES:
                coeff[edge]=coeff.get(edge,0)-F(1,10**11)
            yield dirs,y,w,rel,raw,coeff,FREE
