"""Recompute four result files in isolation and require exact byte identity."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
NAMES=['block_and_graph.json','boundary_identities.json','clock_and_action.json','verification.json']
def main():
    hashes={}
    with tempfile.TemporaryDirectory(prefix='dust-stratum-replay-') as tmp:
        dest=Path(tmp)
        for n in ['analyze.py','plan.json','plan.sha256','provenance.json','LICENSE']:
            shutil.copyfile(ROOT/n,dest/n)
        shutil.copytree(ROOT/'inputs',dest/'inputs',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        subprocess.run([sys.executable,'-B','analyze.py'],cwd=dest,check=True,capture_output=True,timeout=30)
        for n in NAMES:
            b=(dest/'results'/n).read_bytes()
            if b!=(ROOT/'results'/n).read_bytes():raise RuntimeError('Replay mismatch: '+n)
            hashes[n]=hashlib.sha256(b).hexdigest()
    result={'status':'PASS_BYTE_IDENTICAL','scientific_files':4,'sha256':hashes,'external_replication':False,'n5_production':False}
    (ROOT/'results/replay.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
