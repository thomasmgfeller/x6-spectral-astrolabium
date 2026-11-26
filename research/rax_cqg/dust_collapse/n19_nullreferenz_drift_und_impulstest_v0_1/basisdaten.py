from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
PARENT = ROOT / 'basis/Impulseichung.zip'
PIN = 'e302f3e3f8793eb287ab2baeac37d800144e13064cea1f3cc3811a1b33278d77'


@contextmanager
def inputs():
    if sha256(PARENT.read_bytes()).hexdigest() != PIN:
        raise ValueError('Unexpected PR 392 archive')
    with TemporaryDirectory() as tmp, ZipFile(PARENT) as source:
        source.extractall(tmp)
        sys.path.insert(0, tmp)
        try:
            from herkunft import inputs as older
            with older() as (pr391, previous, early):
                yield Path(tmp), pr391, previous, early
        finally:
            sys.path.remove(tmp)
