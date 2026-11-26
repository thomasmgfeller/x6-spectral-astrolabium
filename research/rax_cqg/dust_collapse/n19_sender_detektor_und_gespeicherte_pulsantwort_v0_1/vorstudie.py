"""Load the verified published N19 order, labels and comparison from an isolated copy."""
import json
from contextlib import contextmanager
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent


@contextmanager
def inputs(replay=False):
    with TemporaryDirectory() as tmp, ZipFile(ROOT / 'basis/Pulsvergleich.zip') as z:
        z.extractall(tmp)
        if replay:
            subprocess.run([sys.executable, '-B', 'pruefen.py'], cwd=tmp, check=True)
        sys.path.insert(0, tmp)
        try:
            import ordnung
            bg = ordnung.load_background()
            yield bg, ordnung.select, ordnung.operators(bg), json.loads(z.read('Ergebnisse.json'))
        finally:
            sys.path.remove(tmp)
            sys.modules.pop('ordnung', None)
