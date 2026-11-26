"""Use the published PR 393 ZIP and its pinned dependencies offline."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parent
ZIP=ROOT/'basis/Nullreferenz.zip'
DIGEST='9d2bb2389ab30f1ae5628ea36ff29bab0ceac1b2ca7993c7bd26024494ec9404'

@contextmanager
def inputs():
    if sha256(ZIP.read_bytes()).hexdigest()!=DIGEST:
        raise ValueError('unexpected N19 source archive')
    with TemporaryDirectory() as tmp, ZipFile(ZIP) as z:
        z.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            from basisdaten import inputs as older
            with older() as (_,_,previous,early):
                yield Path(tmp),previous,early
        finally:
            sys.path.remove(tmp)
