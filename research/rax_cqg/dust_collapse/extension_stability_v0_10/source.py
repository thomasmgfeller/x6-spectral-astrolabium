"""Load the archived, digest-checked v0.9 source."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import sys

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'input_v09.zip'
EXPECTED = '76a4d9f6137eb714e16f211894424214fe84d4dcc57b16a9de4643eb024d4f77'
if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() != EXPECTED:
    raise ValueError('v0.9 ZIP digest')
CACHE = ROOT / 'cache_v09'
CACHE.mkdir(exist_ok=True)
with ZipFile(ARCHIVE) as archive:
    for name in archive.namelist():
        if Path(name).name != name:
            raise ValueError(name)
        target = CACHE / name
        data = archive.read(name)
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError(name)
        else:
            target.write_bytes(data)
sys.path.insert(0, str(CACHE))
import reference
