"""Repeat all exact calculations in isolation and compare deterministic results."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
NAMES=['measure_certificate.json','one_element_witnesses.json','geometry_moment_controls.json',
       'robustness_bounds.json','verification.json','transport_controls.json']

def main():
    with tempfile.TemporaryDirectory(prefix='dust-measure-replay-') as tmp:
        dest=Path(tmp)
        for name in ['analyze.py','transport_controls.py','plan.json','plan.sha256','provenance.json','supplement.json']:
            shutil.copyfile(ROOT/name,dest/name)
        shutil.copytree(ROOT/'inputs',dest/'inputs',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        subprocess.run([sys.executable,'-B',str(dest/'analyze.py')],cwd=dest,check=True,capture_output=True,timeout=60)
        subprocess.run([sys.executable,'-B',str(dest/'transport_controls.py')],cwd=dest,check=True,capture_output=True,timeout=15)
        hashes={}
        for name in NAMES:
            actual=(dest/'results'/name).read_bytes();expected=(ROOT/'results'/name).read_bytes()
            if actual!=expected:raise RuntimeError('Replay mismatch: '+name)
            hashes[name]=hashlib.sha256(actual).hexdigest()
    result={'status':'PASS_BYTE_IDENTICAL','result_files':len(NAMES),'sha256':hashes,
            'external_replication':False,'n5_production_run':False}
    (ROOT/'results/replay.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
