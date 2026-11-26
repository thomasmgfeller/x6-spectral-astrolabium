"""Load the pinned N19 reference instrument without network dependencies."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

ROOT = Path(__file__).resolve().parent
PIN = '4f4b3b55f2755c627197eb42184bb760e370df55ea4d63937db99382b424ed63'


@contextmanager
def instrument():
    archive = ROOT / 'basis' / 'PR395.zip'
    if sha256(archive.read_bytes()).hexdigest() != PIN:
        raise ValueError('PR395 archive digest mismatch')
    with TemporaryDirectory() as tmp, ZipFile(archive) as source:
        source.extractall(tmp)
        sys.path.insert(0, tmp)
        try:
            yield Path(tmp)
        finally:
            sys.path.remove(tmp)
