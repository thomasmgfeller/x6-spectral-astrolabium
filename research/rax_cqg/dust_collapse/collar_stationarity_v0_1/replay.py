"""Recompute all five outputs in a temporary isolated directory."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
RESULTS=['stationary_collar.json','boundary_sensitivity.json','finite_width_states.json','return_amplitude_bounds.json','verification.json']
def run():
    with tempfile.TemporaryDirectory(prefix='cst-collar-replay-') as td:
        d=Path(td)
        for name in ['analyze.py','plan.json','plan.sha256','provenance.json','LICENSE']:shutil.copyfile(ROOT/name,d/name)
        shutil.copytree(ROOT/'inputs',d/'inputs')
        subprocess.run([sys.executable,'-B',str(d/'analyze.py')],check=True,stdout=subprocess.DEVNULL)
        hashes={}
        for name in RESULTS:
            actual=(d/'results'/name).read_bytes();expected=(ROOT/'results'/name).read_bytes()
            if actual!=expected:raise RuntimeError('Replay differs: '+name)
            hashes[name]=hashlib.sha256(actual).hexdigest()
    return {'status':'PASS_BYTE_IDENTICAL','scientific_files':len(hashes),'sha256':hashes,
        'external_replication':False,'n5_production':False,'paid_compute':False}
if __name__=='__main__':
    r=run()
    if '--record' in sys.argv:(ROOT/'results/replay.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps(r,indent=2,sort_keys=True))
