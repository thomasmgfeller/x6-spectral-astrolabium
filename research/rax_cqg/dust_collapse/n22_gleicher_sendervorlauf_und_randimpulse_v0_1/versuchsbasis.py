"""Load the pinned N22 source reader and its N19 common preparation."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys,json

ROOT=Path(__file__).resolve().parent
PIN='22c6bbf6d9311a69906a4fc7199456804292eb7b1da6c766cef7ed19bda7b777'
@contextmanager
def inputs():
    archive=ROOT/'basis/Quellenauslese.zip'
    assert sha256(archive.read_bytes()).hexdigest()==PIN
    with TemporaryDirectory() as td, ZipFile(archive) as z:
        z.extractall(td)
        sys.path.insert(0,td)
        from leserbasis import model
        with model() as bundle:
            yield Path(td),bundle,json.loads((Path(td)/'Startwerte.json').read_text())
