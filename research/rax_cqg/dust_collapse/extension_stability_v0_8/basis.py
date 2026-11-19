"""Load the unmodified, hash-pinned N15 reference package in a local cache."""
import hashlib
import os
from pathlib import Path
import sys
from zipfile import ZipFile

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "cache_v07"
ARCHIVE = HERE / "input_v07.zip"
if not ARCHIVE.is_file():
    ARCHIVE = HERE.parent / "packages" / "CST_DUST_N15_Erweiterungsstabilitaet_v0_7_Pruefpaket.zip"
if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() != "7ffc9cd7248dede464c56cb36066130456b5feff248d8d5c2511d3c1b2000536":
    raise ValueError("N15 input archive differs from PR 312")
REFERENCE.mkdir(exist_ok=True)
with ZipFile(ARCHIVE) as archive:
    for name in archive.namelist():
        if Path(name).name != name:
            raise ValueError("Unexpected path in the reference package")
        path = REFERENCE / name
        data = archive.read(name)
        if path.exists():
            if data != path.read_bytes():
                raise ValueError(f"Cached input differs: {name}")
        else:
            path.write_bytes(data)
sys.path.insert(0, str(REFERENCE))
import full
from model import layout
from pilot import direct_packet
from quadrature import build
import tails


def save_json(path, value):
    """Publish only a complete JSON object, including for an interrupted rerun."""
    import json
    from tempfile import NamedTemporaryFile
    path = Path(path)
    with NamedTemporaryFile("w", dir=path.parent, delete=False) as temporary:
        json.dump(value, temporary, indent=2, sort_keys=True, allow_nan=False)
        temporary.write("\n")
    os.replace(temporary.name, path)
