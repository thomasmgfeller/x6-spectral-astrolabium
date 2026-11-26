"""Initialize the pinned offline studies without installing any dependencies."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT/'basis/Sendeschnitt.zip'
DIGEST = 'c4b68fb2584fd76027d46cea9bb92b502365fbaacab2d5dc90bd9d723745c019'


@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest()==DIGEST
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as z:
        z.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            import vorstudie
            with vorstudie.inputs() as (_,early):
                yield Path(tmp),early
        finally:
            sys.path.remove(tmp)
