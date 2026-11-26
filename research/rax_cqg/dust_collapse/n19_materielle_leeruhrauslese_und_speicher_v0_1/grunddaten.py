"""Load the exact preceding archive as a private offline dependency."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'basis/Paarung.zip'
DIGEST = '8e65ee888352a4545e96ccab54c6921113ee17ec1815ca951c29d22833cca2a7'


@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest() == DIGEST
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as archive:
        archive.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            from vorgaenger import inputs as baseline
            with baseline() as (previous,early):
                yield Path(tmp),previous,early
        finally:
            sys.path.remove(tmp)
