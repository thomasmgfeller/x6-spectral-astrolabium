"""Check immutable publication; replay analytic controls in isolated files."""
import argparse,copy,hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(replay=False):
    meta=json.loads((HERE/'PUBLICATION.json').read_text())
    for name,h in meta['artifact_sha256'].items():require(sha(HERE/name)==h,'artifact hash '+name)
    archive=HERE/'Aktive_Huelle_KG_History_v0_17_Pruefpaket.zip'
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'ZIP CRC')
        names=z.namelist()
        require(len(names)==20 and len(set(names))==20,'unique original package inventory')
        for name in names:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts,'safe ZIP path')
            require((HERE/name).read_bytes()==z.read(name),'original file '+name)
        before={name:sha(HERE/name) for name in names}
        pkg=HERE/'causal_closure_v0_17'
        lines=(pkg/'SHA256SUMS').read_text().splitlines()
        require(len(lines)==19,'original manifest inventory')
        for line in lines:
            h,name=line.split('  ',1)
            require(sha(pkg/name)==h,'original manifest '+name)
        require((pkg/'Aktive_Huelle_KG_History_v0_17.pdf').read_bytes()==(HERE/'Aktive_Huelle_KG_History_v0_17.pdf').read_bytes(),'same PDF at publication root')
        if replay:
            expected=json.loads((pkg/'results/ANALYTIC_CHECKS.json').read_text())
            with tempfile.TemporaryDirectory(prefix='cspp-v017-replay-') as td:
                temp=Path(td);z.extractall(temp);work=temp/'causal_closure_v0_17'
                subprocess.run([sys.executable,'-B',str(work/'analytic.py')],cwd=temp,check=True)
                actual=json.loads((work/'results/ANALYTIC_CHECKS.json').read_text())
                require(actual['status']=='PASS' and actual['check_count']==288,'all 288 analytic controls')
                require(actual['runtime']['flint']==expected['runtime']['flint']=='0.8.0','declared arithmetic runtime')
                require(actual['runtime']['python'].startswith('3.12.'),'declared Python minor version')
                normalized=copy.deepcopy(actual)
                normalized['runtime']['python']=expected['runtime']['python']
                require(normalized==expected,'exact scientific results, intervals, checks and claim boundaries')
                print('Replay PASS: 288 controls; exact scientific result equality; Python metadata',expected['runtime']['python'],'->',actual['runtime']['python'],flush=True)
        for name,h in before.items():require(sha(HERE/name)==h,'published file unchanged '+name)
    print('Publication integrity PASS: 20 original package files, 19 manifest entries, PDF and ZIP unchanged',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--replay',action='store_true');run(ap.parse_args().replay)
