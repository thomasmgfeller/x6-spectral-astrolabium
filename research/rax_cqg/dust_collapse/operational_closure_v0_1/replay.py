"""Recompute all four scientific outputs in an isolated directory."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parent
NAMES=['continuous_readout.json','instrument_covariance.json','calibration_bounds.json','verification.json']
def main():
    hashes={}
    with tempfile.TemporaryDirectory(prefix='dust-operational-replay-') as temp:
        dest=Path(temp)
        for name in ['analyze.py','plan.json','plan.sha256','provenance.json','LICENSE']:
            shutil.copyfile(ROOT/name,dest/name)
        shutil.copytree(ROOT/'inputs',dest/'inputs')
        subprocess.run([sys.executable,'-B','analyze.py'],cwd=dest,check=True,capture_output=True,timeout=30)
        for name in NAMES:
            actual=(dest/'results'/name).read_bytes()
            if actual!=(ROOT/'results'/name).read_bytes():raise RuntimeError('Replay mismatch: '+name)
            hashes[name]=hashlib.sha256(actual).hexdigest()
    result={'status':'PASS_BYTE_IDENTICAL','scientific_files':len(NAMES),'sha256':hashes,
            'external_replication':False,'n5_production_run':False}
    (ROOT/'results/replay.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
