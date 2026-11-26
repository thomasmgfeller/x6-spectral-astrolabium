from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
PIN = '5f44eb0cf785d678d4de498565c1b678c57e1ac9e4d102f415476ad8c40b007c'


@contextmanager
def model():
    pkg = ROOT/'basis'/'Fuenfter_Takt.zip'
    if sha256(pkg.read_bytes()).hexdigest() != PIN:
        raise ValueError('Fifth tick archive digest mismatch')
    with TemporaryDirectory() as tmp, ZipFile(pkg) as src:
        src.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            from n19_pr395 import instrument
            with instrument() as parent:
                from n19_archiv394 import inputs
                with inputs() as (_,previous,early):
                    yield Path(tmp),parent,previous,early
        finally:
            sys.path.remove(tmp)
