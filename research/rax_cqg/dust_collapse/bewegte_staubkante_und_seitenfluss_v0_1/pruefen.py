"""Replay the moving-front study using Python 3.10+ with its standard library."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import argparse
import gzip
import pulse
import json
import subprocess
import sys

from fluss import flux_test
from front import front_test

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'source'/'CST_DUST_Innen_und_Aussen_auf_derselben_Historie_Pruefpaket.zip'
SOURCE_HASH = '0317a41ba23a35e5fe14d47a2fc69895909bc25881fc9bbf0231fc7e8c2723e2'


def run(replay_previous, save_frames):
    assert sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
    with ZipFile(SOURCE) as archive:
        for line in archive.read('SHA256SUMS').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            assert sha256(archive.read(name)).hexdigest() == digest
        previous = json.loads(archive.read('Ergebnisse.json'))
        checkpoints = json.loads(archive.read('basis/checkpoints.json'))
        if replay_previous:
            with TemporaryDirectory() as tmp:
                archive.extractall(tmp)
                subprocess.run([sys.executable,'-B','pruefen.py'],cwd=tmp,check=True)
    assert len(checkpoints) == 60 and all(row['execution']=='NOT_RUN' for row in checkpoints)
    r = F(previous['spatial_ratio'])
    qlo, qhi = map(F,previous['temporal_root'])
    stencil = [tuple(row) for row in previous['geometry']['stencil']]
    def residual(q):
        return sum(b*d*(q**d*r**s-1) for d,s,b in stencil)
    assert r == F(511,512) and 0 < qlo < qhi < 1
    assert qhi-qlo < F(1,10**32) and residual(qlo)*residual(qhi) < 0
    flow = flux_test(stencil,r,(qlo,qhi))
    with TemporaryDirectory() as tmp, ZipFile(SOURCE) as archive:
        archive.extractall(tmp)
        frames = pulse.acquire(Path(tmp),r,(qlo,qhi),stencil)
    payload = json.dumps(frames,sort_keys=True,separators=(',',':')).encode()
    raw = ROOT/'Vierarmaufnahmen.json.gz'
    if save_frames:
        raw.write_bytes(gzip.compress(payload,mtime=0))
    stored = gzip.decompress(raw.read_bytes())
    assert stored == payload
    return {'input_sha256':SOURCE_HASH,'front':front_test(stencil),'flow':flow,
            'four_arm_readout':pulse.verify(json.loads(stored),stencil,flow['allocation']),
            'uncompressed_four_arm_sha256':sha256(payload).hexdigest(),
            'physical_P3':previous['physical_P3'],'physical_records_not_run':len(checkpoints)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vorversuch',action='store_true',help='also reproduce the complete original experiment')
    parser.add_argument('--ausgeben',action='store_true',help='print computed JSON to stdout')
    parser.add_argument('--aufnahmen-erzeugen',action='store_true',help='regenerate the compressed acquisition')
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit('Für den Prüflauf Python ohne -O starten.')
    data = json.dumps(run(args.vorversuch,args.aufnahmen_erzeugen),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.ausgeben:
        sys.stdout.write(data)
    else:
        assert data == (ROOT/'Ergebnisse.json').read_text(encoding='utf-8')
        print('PASS: Bewegte Kante, Ein-Ereignis-Variation, Schnittladungen und Seitenflüsse. Physischer P3: 60 × NOT_RUN.')
