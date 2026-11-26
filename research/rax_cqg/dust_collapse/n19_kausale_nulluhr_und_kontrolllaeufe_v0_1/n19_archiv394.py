"""Pinned PR 394 archive and the earlier stationary solver, fully offline."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'basis/Empfangsbit.zip'
PIN='680009b0bf3d99c82ff1a5a64f04980666f3f1a798fc8ca80addf651d6db1ebe'


@contextmanager
def inputs():
    if sha256(ARCHIVE.read_bytes()).hexdigest()!=PIN:
        raise ValueError('Unexpected PR 394 archive')
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as source:
        source.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            from n19_archiv393 import inputs as historical
            with historical() as (_,previous,early):
                yield Path(tmp),previous,early
        finally:
            sys.path.remove(tmp)
