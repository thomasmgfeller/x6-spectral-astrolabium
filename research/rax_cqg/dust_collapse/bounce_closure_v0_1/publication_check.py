"""Verify the unchanged closure release and optionally replay its finite model."""
import argparse,hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent
ZIP='CST_Staubball_Bounce_Kandidat_Abschluss_v0_1_Pruefpaket.zip'
PDF='CST_Staubball_Bounce_Kandidat_Abschluss_v0_1.pdf'
def require(ok,message):
    if not ok:raise ValueError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def run(replay):
    require(__debug__,'Use Python without -O')
    archive=P.parent/'packages'/ZIP
    require(digest(archive.read_bytes())=='9585f130b13f7eaec481177c572027948db24a4b4634d4dcd55235fb93167553','release archive changed')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        require(len(names)==15 and len(set(names))==15 and z.testzip() is None,'invalid ZIP inventory')
        for name in names:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe path')
            require((P/name).read_bytes()==z.read(name),'expanded artifact differs: '+name)
        for line in z.read('SHA256SUMS').decode().splitlines():
            h,n=line.split(maxsplit=1)
            require(digest(z.read(n))==h,'internal hash differs: '+n)
        require(z.read(PDF)==(P.parent/'reports'/PDF).read_bytes(),'report copy differs')
        sources=json.loads(z.read('source_snapshot.json'))
        for item in sources['sources']:
            require(z.read('sources/'+item['name'])==(P.parent/'packages'/item['name']).read_bytes(),'previously published source differs')
        result=json.loads(z.read('results/closure_result.json'))
        require(result['decision']=='CLOSED_REJECTED_FOR_DOMINANT_BOUNCE','closure decision changed')
        require(result['global_cst_bounce']=='HOLD' and result['singularity_resolution']=='HOLD','claim boundary changed')
        require(all(c['pointer_bound']=='1/2' for c in result['certificates'].values()),'bound changed')
        require(all(c['byte_identical'] for c in result['replay_comparisons']),'reference replay differs')
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-bounce-publication-') as tmp:
                work=Path(tmp);z.extractall(work)
                subprocess.run([sys.executable,str(work/'verify_closure.py'),'--out',str(work/'fresh')],check=True)
                fresh=json.loads((work/'fresh/closure_result.json').read_text())
                for key in ['candidate_snapshot_sha256','decision','global_cst_bounce','singularity_resolution','certificates','holdout_bands','transfer']:
                    require(fresh[key]==result[key],'fresh closure differs: '+key)
    print('PASS: immutable closure package, 15 members, 3 original sources, PDF and claim boundaries'+('; finite-model replay passed' if replay else ''))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
