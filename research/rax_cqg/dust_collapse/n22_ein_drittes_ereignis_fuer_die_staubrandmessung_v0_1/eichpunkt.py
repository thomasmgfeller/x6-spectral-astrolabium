"""Specific published N19 collar for an exact N22 existence test."""
from pathlib import Path
from fractions import Fraction as F
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
import json,sys

def calculate(drift=F(0),strength=F(0)):
    assert abs(drift)<=F(1,10**6) and strength in (F(0),F(1,10**6),F(-1,10**6))
    base=Path(__file__).resolve().parent
    with TemporaryDirectory() as td, ZipFile(base/'basis/N21.zip') as parent:
        with ZipFile(BytesIO(parent.read('basis/Ankerpaket.zip'))) as z:
            z.extractall(td)
        sys.path[:0]=[td,str(Path(td)/'basis')]
        from quellenpaket import model
        with model() as (_,__,previous,early):
            from modell import setup
            from referenzwechsel import displaced
            from empfangsbit import K0,STEP
            from staubgeraet import solve,verify
            from quelle import box
            y,w=setup(previous,early)
            y,w=displaced(y,w,box(6*STEP+drift))
            zeros=(box(0),)*3
            state=solve(y,w,strength,zeros,K0,box(-K0),'positive_bridge')
            verify(state,strength,zeros,K0,box(-K0),'positive_bridge',zeros)
            return {j:[state['y'][j].data(),state['w'][j].data()] for j in (0,1,2,3,7,8,9,10)}

if __name__=='__main__':print(json.dumps(calculate(*map(F,sys.argv[1:]))))
