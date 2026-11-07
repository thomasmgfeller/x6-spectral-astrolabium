"""Replay in isolation and compare all scientific outputs byte for byte."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
RESULTS=['algebra_and_conservation.json','finite_reference_effects.json','reference_budgets.json','verification.json']

def run():
    with tempfile.TemporaryDirectory(prefix='cst-reference-replay-') as td:
        dest=Path(td)
        for name in ['analyze.py','plan.json','plan.sha256','provenance.json','LICENSE']:
            shutil.copyfile(ROOT/name,dest/name)
        shutil.copytree(ROOT/'inputs',dest/'inputs')
        subprocess.run([sys.executable,'-B',str(dest/'analyze.py')],check=True,stdout=subprocess.DEVNULL)
        hashes={}
        for name in RESULTS:
            expected=(ROOT/'results'/name).read_bytes();actual=(dest/'results'/name).read_bytes()
            if actual!=expected:raise RuntimeError('Replay differs: '+name)
            hashes[name]=hashlib.sha256(actual).hexdigest()
    result={'status':'PASS_BYTE_IDENTICAL','scientific_files':len(hashes),'sha256':hashes,
            'external_replication':False,'paid_compute':False,'n5_production':False}
    return result

if __name__=='__main__':
    result=run()
    if '--record' in sys.argv:(ROOT/'results/replay.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
