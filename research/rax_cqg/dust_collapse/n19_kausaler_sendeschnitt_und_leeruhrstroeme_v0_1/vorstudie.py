"""Pinned repository archive and two embedded source trees, available offline."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'basis/Impulsspeicher.zip'
HASH = 'a85e53c7596219263421193a42923ac7e79d82c132e211a94806db9845e2d5b1'


@contextmanager
def inputs():
    assert sha256(ARCHIVE.read_bytes()).hexdigest() == HASH
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        device, early, dust = [root/s for s in ('device','early','dust')]
        for src, dest in [(ARCHIVE,device),(device/'basis/Anfangsimpuls.zip',early),
                          (early/'basis/Staubantwort.zip',dust)]:
            with ZipFile(src) as z:
                z.extractall(dest)
        sys.path[:0] = [str(early),str(dust)]
        try:
            yield device,early
        finally:
            del sys.path[:2]
