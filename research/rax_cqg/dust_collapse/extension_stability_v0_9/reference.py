"""Load the unmodified offline package from PR 313."""
import hashlib
from pathlib import Path
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "input_v08.zip"
if not PACKAGE.is_file():
    PACKAGE = ROOT.parent / "packages" / "CST_DUST_N15_Uhrantworten_v0_8_Pruefpaket.zip"
SOURCE = ROOT / "cache_v08"
DIGEST = "52ac3f60c7acf3fde998f45b4bd6cdac9b0723de08e7d050379bdb46a794bcc4"
if hashlib.sha256(PACKAGE.read_bytes()).hexdigest() != DIGEST:
    raise ValueError("Unexpected v0.8 archive")
SOURCE.mkdir(exist_ok=True)
with ZipFile(PACKAGE) as archive:
    for name in archive.namelist():
        if Path(name).name != name:
            raise ValueError(name)
        target = SOURCE / name
        data = archive.read(name)
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError(f"Cached input differs: {name}")
        else:
            target.write_bytes(data)
sys.path.insert(0, str(SOURCE))
from basis import full, layout, build, direct_packet, tails, save_json
from pilot import net
