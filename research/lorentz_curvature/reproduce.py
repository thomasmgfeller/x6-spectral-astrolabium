"""Replay all frozen seeds in a new temporary directory; never alter evidence."""
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from verify import verify, compare

HERE=Path(__file__).resolve().parent


def main():
    published=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'results'
    print(json.dumps(verify(published),indent=2),flush=True)
    provenance=json.loads((published/'provenance.json').read_text())
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='x6-curvature-replay-') as tmp:
        fresh=Path(tmp)/'results'
        subprocess.run([sys.executable,'-B',str(HERE/'run.py'),str(fresh),'--source-commit',provenance['source_commit']],check=True,env=env)
        print(json.dumps(verify(fresh),indent=2),flush=True)
        for name in ['models.json','summary.json']:
            compare(json.loads((published/name).read_text()),json.loads((fresh/name).read_text()),name)
        before=json.loads(gzip.decompress((published/'records.json.gz').read_bytes()))
        after=json.loads(gzip.decompress((fresh/'records.json.gz').read_bytes()))
        compare(before,after,'all records')
        compare(provenance['source_sha256'],json.loads((fresh/'provenance.json').read_text())['source_sha256'],'frozen sources')
    print(json.dumps(dict(status='PASS_FULL_CURVATURE_REPLAY',records=len(before),scope='Identical seeds, full relation bytes, coordinate hashes, scores and scientific summaries; timing/environment excluded',external_replication=False),indent=2))


if __name__=='__main__':main()
