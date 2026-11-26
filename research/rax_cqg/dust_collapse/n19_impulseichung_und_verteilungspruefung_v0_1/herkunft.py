"""Pinned published predecessor. Only the early collar is used for calibration."""
from contextlib import contextmanager
from pathlib import Path
from hashlib import sha256
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'basis/Speicherpraeparation.zip'
DIGEST='3a78d5168f73292618a69401e34f9e7ee07ab92640af765bdf890853b59bcc8f'

@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest()==DIGEST
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as z:
        z.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            from archiv import inputs as predecessor
            with predecessor() as (_,prev,early):
                yield Path(tmp),prev,early
        finally:
            sys.path.remove(tmp)
