"""Use the unchanged reference solver in a temporary offline directory."""
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "basis/Anfangsimpuls.zip"
DIGEST = "d2a2d2f49d60cdc1c90e4b9f4771379255ae29bcfa4b3c76a38f1455e4576fa8"


@contextmanager
def reference():
    assert sha256(ARCHIVE.read_bytes()).hexdigest() == DIGEST
    with TemporaryDirectory() as directory, ZipFile(ARCHIVE) as bundle:
        bundle.extractall(directory)
        sys.path.insert(0, directory)
        try:
            yield Path(directory)
        finally:
            sys.path.remove(directory)


def read_json(path):
    return json.loads(path.read_bytes())
