"""Reconstruct the unchanged reference.npz bytes from size-bounded GitHub parts."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
def prepare():
    folder=HERE/'results';spec=json.loads((folder/'REFERENCE_ARCHIVE.json').read_text())
    target=folder/'reference.npz'
    if target.exists():
        if target.stat().st_size!=spec['size'] or hashlib.sha256(target.read_bytes()).hexdigest()!=spec['sha256']:
            raise RuntimeError('HOLD: existing reconstructed reference archive has wrong bytes')
        return target
    tmp=folder/'reference.npz.building'
    try:
        with tmp.open('wb') as stream:
            for part in spec['parts']:
                data=(folder/part['name']).read_bytes()
                if len(data)!=part['size'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
                    raise RuntimeError('HOLD: reference archive part hash mismatch')
                stream.write(data)
        if tmp.stat().st_size!=spec['size'] or hashlib.sha256(tmp.read_bytes()).hexdigest()!=spec['sha256']:
            raise RuntimeError('HOLD: reconstructed reference archive hash mismatch')
        tmp.replace(target)
    finally:
        tmp.unlink(missing_ok=True)
    return target
if __name__=='__main__':print(prepare())
