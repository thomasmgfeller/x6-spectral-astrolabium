"""Verify and reassemble the original closure archives from transport parts.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,hashlib,json,os,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def assemble(output=None):
    m=json.loads((HERE/'archive_parts.json').read_text())
    assert m['schema']=='eigenzeit.closure-archive-parts/1'
    dest=Path(output) if output else HERE;dest.mkdir(parents=True,exist_ok=True)
    reports=[]
    for record in m['archives']:
        assert Path(record['archive']).name==record['archive']
        target=dest/record['archive'];h=hashlib.sha256();size=0;pieces=[]
        for entry in record['parts']:
            assert Path(entry['file']).name==entry['file']
            b=(HERE/entry['file']).read_bytes()
            assert len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256']
            h.update(b);size+=len(b);pieces.append(b)
        assert size==record['bytes'] and h.hexdigest()==record['sha256']
        if target.exists():
            assert target.stat().st_size==size and hashlib.sha256(target.read_bytes()).hexdigest()==h.hexdigest()
        else:
            tmp=None
            try:
                with tempfile.NamedTemporaryFile(dir=dest,prefix='.closure-',delete=False) as f:
                    tmp=Path(f.name)
                    for b in pieces:f.write(b)
                os.replace(tmp,target);tmp=None
            finally:
                if tmp is not None:tmp.unlink(missing_ok=True)
        reports.append(dict(archive=record['archive'],bytes=size,sha256=h.hexdigest()))
    return dict(status='PASS',archives=reports)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    print(json.dumps(assemble(args.output)))
