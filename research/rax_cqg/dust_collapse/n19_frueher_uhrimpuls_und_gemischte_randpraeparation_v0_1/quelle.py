"""Read the pinned study once and reuse its outward-rounded arithmetic."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'basis/Staubantwort.zip'
with TemporaryDirectory() as tmp, ZipFile(ARCHIVE) as bundle:
    for name in ('basisdaten.py','basis/Zeigerstudie.zip'):
        bundle.extract(name,tmp)
    spec=importlib.util.spec_from_file_location('pinned_interval',Path(tmp)/'basisdaten.py')
    old=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    DATA=old.read()
box,hull,Box,SCALE=old.box,old.hull,old.Box,old.SCALE
