"""Reassemble the byte-identical certificate archive from transport parts.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

HERE=Path(__file__).resolve().parent

def assemble(output=None):
    manifest=json.loads((HERE/'archive_parts.json').read_text())
    assert manifest['schema']=='eigenzeit.certificate-archive-parts/1'
    target=Path(output) if output else HERE/manifest['archive']
    total=hashlib.sha256();size=0;parts=[]
    for entry in manifest['parts']:
        name=entry['file'];assert Path(name).name==name
        data=(HERE/name).read_bytes()
        assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],name
        total.update(data);size+=len(data);parts.append(data)
    assert size==manifest['bytes'] and total.hexdigest()==manifest['sha256']
    if target.exists():
        assert target.stat().st_size==size and hashlib.sha256(target.read_bytes()).hexdigest()==total.hexdigest(),target
    else:
        temporary=None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent,prefix='.certificate-',delete=False) as stream:
                temporary=Path(stream.name)
                for data in parts:stream.write(data)
            os.replace(temporary,target);temporary=None
        finally:
            if temporary is not None:temporary.unlink(missing_ok=True)
    return dict(status='PASS',archive=str(target),bytes=size,sha256=total.hexdigest(),parts=len(parts))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    print(json.dumps(assemble(args.output)))
