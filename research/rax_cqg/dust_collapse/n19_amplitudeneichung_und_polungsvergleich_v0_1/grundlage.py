"""Load immutable prior code and data from the included offline archive."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT/'basis/Stromvorhersage.zip'
DIGEST = 'a3c00e16614e89c6c6348b7790a3bc02f04165a649c0a0def2eb9d1436a5208f'


@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest() == DIGEST
    with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as z:
        z.extractall(tmp)
        sys.path.insert(0,tmp)
        try:
            import referenz
            with referenz.inputs() as (_,early):
                yield Path(tmp),early
        finally:
            sys.path.remove(tmp)
