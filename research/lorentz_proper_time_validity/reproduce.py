"""Unpack the original numeric outputs and invoke the unchanged frozen verifier."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from verify import selftest,verify

HERE=Path(__file__).resolve().parent

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--archive-only',action='store_true')
    ns=a.parse_args()
    raw=(HERE/'results.zip').read_bytes()
    archive=json.loads((HERE/'ARCHIVE.json').read_text())
    if hashlib.sha256(raw).hexdigest()!=archive['sha256']:
        raise ValueError('archive digest mismatch')
    selftest()
    with tempfile.TemporaryDirectory() as tmp:
        dest=Path(tmp)
        with zipfile.ZipFile(HERE/'results.zip') as z:
            if sorted(z.namelist())!=sorted(['grid.json','planning.json','execution.json','hashes.json']):
                raise ValueError('unexpected archive entries')
            for name in z.namelist():
                (dest/name).write_bytes(z.read(name))
        verify(dest,replay=not ns.archive_only)
