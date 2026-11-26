"""Pinned offline entry point for the original stationary solutions and checks."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'basis/Empfangsspeicher.zip'
DIGEST='c7a33024210db5ac7be9c3d195695ffae2d9312efe2b0e7b7066bbb78dbfeefc'


@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest()==DIGEST
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as z:
        z.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            from grunddaten import inputs as previous
            with previous() as (_,pr389,early):
                yield Path(tmp),pr389,early
        finally:
            sys.path.remove(tmp)
