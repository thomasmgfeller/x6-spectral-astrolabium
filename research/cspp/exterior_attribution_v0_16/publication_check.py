"""Check byte-identical publication and replay in isolated temporary files."""
import argparse,gzip,hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
from flint import arb,acb,ctx

HERE=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def gz(path):
    with gzip.open(path,'rt') as f:return json.load(f)
def ball(x):return acb(arb(x[0]),arb(x[1]))

def run(replay=False):
    ctx.prec=192;meta=json.loads((HERE/'PUBLICATION.json').read_text())
    for name,h in meta['artifact_sha256'].items():require(sha(HERE/name)==h,'artifact hash '+name)
    archive=HERE/'Aeussere_Forcierung_v0_16_Pruefpaket.zip'
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'ZIP CRC')
        names=z.namelist();require(len(names)==167 and len(names)==len(set(names)),'unique original package inventory')
        for name in names:
            require(not Path(name).is_absolute() and '..' not in Path(name).parts,'safe archive path')
            require((HERE/name).read_bytes()==z.read(name),'unchanged original package file '+name)
        before={name:sha(HERE/name) for name in names}
        for line in (HERE/'exterior_attribution_v0_16/SHA256SUMS').read_text().splitlines():
            h,name=line.split('  ',1);require(before[name]==h,'package manifest '+name)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cspp-v016-replay-') as td:
                root=Path(td);z.extractall(root);pkg=root/'exterior_attribution_v0_16'
                original_coeff=gz(pkg/'results/COEFFICIENTS_192.json.gz')
                expected={bits:gz(pkg/f'results/ATTRIBUTION_{bits}.json.gz') for bits in [128,192]}
                def execute(args):subprocess.run([sys.executable,'-B',*args],cwd=root,check=True)
                execute(['exterior_attribution_v0_16/exterior.py','coefficients'])
                new_coeff=gz(pkg/'results/COEFFICIENTS_192.json.gz');ncoef=0
                require(new_coeff['complete'],'complete coefficient replay')
                for old,new in zip(original_coeff['rows'],new_coeff['rows'],strict=True):
                    for field in ['key','retained_coordinates_sha256','retained_counts_sha256','inner_indices','exterior_indices']:
                        require(old[field]==new[field],'same coefficient geometry '+field)
                    for a,b in zip(old['levels'],new['levels'],strict=True):
                        require(a['n']==b['n'] and a['geometry_sha256']==b['geometry_sha256'],'same spatial partition')
                        for aa,bb in zip(a['q'],b['q'],strict=True):
                            for x,y in zip(aa,bb,strict=True):require(ball(x).overlaps(ball(y)),'coefficient interval replay');ncoef+=1
                # The original freeze also locks the geometric coefficient file.
                # Its exact regeneration is checked by exterior.py before solving.
                for bits in [128,192]:execute(['exterior_attribution_v0_16/exterior.py','solve','--bits',str(bits)])
                execute(['exterior_attribution_v0_16/verify.py'])
                compared=0
                for bits in [128,192]:
                    got=gz(pkg/f'results/ATTRIBUTION_{bits}.json.gz');old=expected[bits]
                    require(got['complete'] and got['G1']=='HOLD' and got['METHOD']=='HOLD','scientific gates unchanged')
                    require(got['infinite_domain_attribution']=='NOT_CERTIFIED' and got['new_random_calls']==0,'claim boundary unchanged')
                    for a,b in zip(old['rows'],got['rows'],strict=True):
                        require(a['key']==b['key'],'same archived pair')
                        for x,y in zip(a['history'],b['history'],strict=True):require(ball(x).overlaps(ball(y)),'KG history replay');compared+=1
                        for x,y in zip(a['exterior_active_values'],b['exterior_active_values'],strict=True):
                            require(x['index']==y['index'] and ball(x['discrete_value']).overlaps(ball(y['discrete_value'])),'outer active replay');compared+=1
                        for u,v in zip(a['windows'],b['windows'],strict=True):
                            for x,y in zip(u['external_state_transfer'],v['external_state_transfer'],strict=True):
                                require(x['index']==y['index'] and ball(x['coefficient']).overlaps(ball(y['coefficient'])),'external transfer replay');compared+=1
                            for aa,bb in zip(u['levels'],v['levels'],strict=True):
                                for name in aa['quantities']:
                                    require(ball(aa['quantities'][name]['value']).overlaps(ball(bb['quantities'][name]['value'])),'response replay '+name);compared+=1
                check=json.loads((pkg/'results/CHECKS.json').read_text())
                require(all(r['extended_accuracy_excluded'] and r['KG_prescribed_accuracy_excluded'] for r in check['comparisons']),'eight finite exclusions reproduced')
                require(sum(r['shell_component_radius_pass'] for r in check['comparisons'])==2,'six broad shell enclosures remain visible')
                print('Replay PASS:',ncoef,'coefficient intervals;',compared,'history/response/transfer intervals',flush=True)
        for name,h in before.items():require(sha(HERE/name)==h,'published source remained unchanged '+name)
    print('Publication integrity PASS: 167 original package files; PDF and ZIP unchanged',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--replay',action='store_true');run(ap.parse_args().replay)
