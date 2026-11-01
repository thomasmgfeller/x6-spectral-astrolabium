"""Verify original response artifacts, both freezes and optional complete replay."""
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


def check(replay,portable=False):
    rec=json.loads((HERE/'PUBLICATION.json').read_text())
    for name,sha in rec['files'].items():require(digest((HERE/name).read_bytes())==sha,name)
    with ZipFile(HERE/rec['archive']) as z:
        names=z.namelist()
        require(len(names)==len(set(names))==rec['archive_members'],'archive inventory')
        require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'archive paths')
        hashes=manifest(z.read('MANIFEST.sha256'))
        require(set(names)==set(hashes)|{'MANIFEST.sha256'},'manifest inventory')
        for name,sha in hashes.items():require(digest(z.read(name))==sha,name)
        for freeze in ['FREEZE.sha256','AUDIT_FREEZE.sha256']:
            for name,sha in manifest(z.read(freeze)).items():require(digest(z.read(name))==sha,freeze+' '+name)
        for public,member in rec['archive_copies'].items():require((HERE/public).read_bytes()==z.read(member),public)
        require((HERE/rec['report']).read_bytes().startswith(z.read('Bericht.pdf')),'archived PDF')
        origin=json.loads(z.read('previous/ORIGIN.json'))
        require(origin==rec['previous_source'],'source provenance record')
        for name,sha in origin['files'].items():require(digest(z.read('previous/'+name))==sha,'inherited '+name)
        audit=json.loads(z.read('records/coverage_audit.json'))
        for name in ['M0','M1']:
            original=json.loads(z.read('records/'+name+'.json'))
            require(original['joint_ellipsoid']['radius_squared']==audit['results'][name]['original_radius_squared'],'unchanged radius '+name)
        require(audit['original_data_and_radius_unchanged'],'audit declaration')
        require(not audit['results']['M1']['single_raw_dataset_nominal_vector_inside'],'preserved outlier')
        require(json.loads(z.read('STATUS.json'))['physical_release']=='HOLD_FIELD_TRANSFER','physical hold')
        print(f'PASS: original PDF/ZIP, {len(names)} entries, both freezes, public extracts, source hashes and disclosed audit',flush=True)
        if replay:
            with tempfile.TemporaryDirectory() as work:
                z.extractall(work)
                if portable:
                    from portable_replay import replay as portable_replay
                    portable_replay(Path(work))
                else:
                    subprocess.run([sys.executable,'-B','audit_reproduce.py'],cwd=work,check=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group()
    group.add_argument('--replay',action='store_true')
    group.add_argument('--portable-replay',action='store_true')
    args=p.parse_args();check(args.replay or args.portable_replay,args.portable_replay)
