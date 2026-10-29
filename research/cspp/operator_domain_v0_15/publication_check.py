"""Validate unchanged published deliverables and replay in an isolated directory."""
import argparse,hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
from flint import arb,acb,ctx
HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not bool(ok):raise RuntimeError('PUBLICATION_HOLD: '+msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def safe_name(name):
    p=Path(name);require(not p.is_absolute() and '..' not in p.parts,'safe archive path '+name)
    return p
def interval_items(obj,path=''):
    if isinstance(obj,dict):
        if 'real_ball' in obj and 'imag_ball' in obj:
            yield path,acb(arb(obj['real_ball']),arb(obj['imag_ball']))
        else:
            for k,v in obj.items():yield from interval_items(v,path+'/'+k)
    elif isinstance(obj,list):
        if len(obj)==2 and all(isinstance(v,str) for v in obj):
            try:z=acb(arb(obj[0]),arb(obj[1]))
            except ValueError:z=None
            if z is not None:yield path,z;return
        for i,v in enumerate(obj):yield from interval_items(v,path+'/'+str(i))
def endpoint_bound(path):
    return any(x in path for x in ['relative_bias_lower','covered_bias_lower',
        'all_H_ge_12_bias_lower','history_sup_gain_','history_gain_','residual_gain_'])

def main(replay=False):
    pub=json.loads((HERE/'PUBLICATION.json').read_text())
    for name,h in pub['artifacts'].items():require(digest((HERE/name).read_bytes())==h,'artifact hash '+name)
    zip_path=HERE/'Operator_Gebietsfehler_v0_15_Pruefpaket.zip'
    checked=0
    with zipfile.ZipFile(zip_path) as z:
        require(z.testzip() is None,'ZIP CRC integrity')
        require(len(z.namelist())==len(set(z.namelist())),'unique archive names')
        for name in z.namelist():
            safe_name(name);require((HERE/name).is_file(),'browsable file '+name)
            require(z.read(name)==(HERE/name).read_bytes(),'browsable file equals archived original '+name)
        for line in z.read('operator_gebiet_v0_15/SHA256SUMS').decode().splitlines():
            expected,name=line.split('  ',1);safe_name(name)
            require(digest(z.read(name))==expected,'frozen package hash '+name);checked+=1
        require(checked==145,'complete original hash inventory')
        if replay:
            with tempfile.TemporaryDirectory(prefix='cspp_v015_replay_') as td:
                z.extractall(td)
                work=Path(td);study=work/'operator_gebiet_v0_15'
                for script in ['run.py','domain_certificate.py','residual_gain.py']:
                    for bits in [128,192]:
                        subprocess.run([sys.executable,'-B',str(study/script),'--bits',str(bits)],cwd=work,check=True)
                subprocess.run([sys.executable,'-B',str(study/'verify.py')],cwd=work,check=True)
                ctx.prec=192;comparisons=0;bounds=0
                for label in ['DIAGNOSIS','DOMAIN_CERTIFICATE','RESIDUAL_GAIN']:
                    for bits in [128,192]:
                        name=f'operator_gebiet_v0_15/results/{label}_{bits}.json'
                        old=json.loads(z.read(name));new=json.loads((work/name).read_text())
                        oi=dict(interval_items(old));ni=dict(interval_items(new))
                        require(oi.keys()==ni.keys(),'replay inventory '+name)
                        for key in oi:
                            if endpoint_bound(key):
                                require(ni[key].is_finite(),'finite replay certificate '+key);bounds+=1
                            else:
                                require(oi[key].overlaps(ni[key]),'replay interval '+name+key);comparisons+=1
                        if label=='DIAGNOSIS':require(old['status']==new['status'],'scientific decisions unchanged')
                        if label=='DOMAIN_CERTIFICATE':
                            require(new['decision']==old['decision'],'domain decision unchanged')
                            require(arb(new['all_H_ge_4_relative_bias_lower'][0])>arb('0.4170'),'global 41.70 percent bound retained')
                print('Replay: matched intervals',comparisons,'separate endpoint bounds',bounds,flush=True)
    print('Publication integrity PASS:',checked,'original package hashes; artifacts unchanged',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--replay',action='store_true');main(ap.parse_args().replay)
