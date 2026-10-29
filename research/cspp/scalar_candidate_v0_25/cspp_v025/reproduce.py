"""Replay certificates in an isolated temporary directory, then verify inputs."""
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');args=p.parse_args()
    before={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'evidence').iterdir() if x.is_file()}
    replay=[]
    if not args.quick:
        with tempfile.TemporaryDirectory(prefix='cspp025-replay-') as temp:
            for bits in [128,192]:
                out=Path(temp)/f'CERTIFICATE_{bits}.json'
                subprocess.run([sys.executable,str(ROOT/'run.py'),'--bits',str(bits),'--out',str(out)],check=True)
                expected=ROOT/'results'/out.name
                if out.read_bytes()!=expected.read_bytes():raise RuntimeError('Replay differs: '+out.name)
                replay.append({'file':out.name,'byte_identical':True,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
    subprocess.run([sys.executable,str(ROOT/'verify.py')],check=True)
    for name,digest in before.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Evidence modified')
    result={'mode':'quick' if args.quick else 'full','status':'PASS','input_files_unchanged':len(before),'replayed':replay,
      'runtime_note':'Byte identity is required in the recorded Python/flint environment; another Python version changes metadata.'}
    if not args.quick:(ROOT/'results/REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
