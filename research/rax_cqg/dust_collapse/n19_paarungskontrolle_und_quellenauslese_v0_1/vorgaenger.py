"""Pinned, offline PR 389 baseline."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'basis/Polungsvergleich.zip'
DIGEST='33f5353483d74fcf3629bf286f00111dd5ee88d79f2c0906ff4b6403eace6efa'


@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest()==DIGEST
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as z:
        z.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            import grundlage
            with grundlage.inputs() as (_,early):
                yield Path(tmp),early
        finally:
            sys.path.remove(tmp)
