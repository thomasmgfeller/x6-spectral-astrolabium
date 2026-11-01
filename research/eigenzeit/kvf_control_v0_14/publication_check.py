"""Verify original KVF artifacts, inherited sources and optional clean replay."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent


def digest(data):return hashlib.sha256(data).hexdigest()


def require(ok,label):
    if not ok:raise ValueError('verification failed: '+label)


def manifest(data):
    rows=[line.split(None,1) for line in data.decode().splitlines()]
    entries={name:sha for sha,name in rows}
    require(len(rows)==len(entries),'duplicate manifest entry')
    return entries


def check(replay):
    rec=json.loads((HERE/'PUBLICATION.json').read_text())
    for name,sha in rec['files'].items():require(digest((HERE/name).read_bytes())==sha,name)
    with ZipFile(HERE/rec['archive']) as z:
        names=z.namelist()
        require(len(names)==len(set(names))==rec['archive_members'],'archive inventory')
        require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'archive paths')
        hashes=manifest(z.read('MANIFEST.sha256'))
        require(set(names)==set(hashes)|{'MANIFEST.sha256'},'manifest inventory')
        for name,sha in hashes.items():require(digest(z.read(name))==sha,name)
        for name,sha in manifest(z.read('FREEZE.sha256')).items():require(digest(z.read(name))==sha,'final freeze '+name)
        for name,sha in manifest(z.read('development/FREEZE_PRE_RUN.sha256')).items():
            historical={'certificate.py':'development/certificate_pre_review.py','records/certificate.json':'development/certificate_pre_review.json'}.get(name,name)
            require(digest(z.read(historical))==sha,'pre-run freeze '+name)
        review=json.loads(z.read('development/REVIEW.json'))
        for name,sha in review['sha256'].items():require(digest(z.read(name))==sha,'arithmetic review '+name)
        require(json.loads(z.read('development/certificate_pre_review.json'))['decision']==json.loads(z.read('records/certificate.json'))['decision'],'unchanged decision')
        for public,member in rec['archive_copies'].items():require((HERE/public).read_bytes()==z.read(member),public)
        require((HERE/rec['report']).read_bytes().startswith(z.read('Bericht.pdf')),'archived PDF')
        origin=json.loads(z.read('previous/ORIGIN.json'))
        require(origin==rec['previous_source'],'source provenance record')
        for name,sha in origin['files'].items():require(digest(z.read('previous/'+name))==sha,'inherited '+name)
        print(f'PASS: original PDF/ZIP, {len(names)} entries, both freezes, public extracts and four inherited documents',flush=True)
        if replay:
            with tempfile.TemporaryDirectory() as work:
                z.extractall(work)
                subprocess.run([sys.executable,'-B','reproduce.py'],cwd=work,check=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--replay',action='store_true')
    check(p.parse_args().replay)
