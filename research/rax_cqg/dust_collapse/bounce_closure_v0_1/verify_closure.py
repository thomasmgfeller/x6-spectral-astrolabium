"""Reproduce the closure certificate; Python 3.10+, standard library only.

The finite certificate verifies hypotheses. The universal pointer bound is
proved analytically in the accompanying report, not inferred from a scan.
"""
import argparse
import collections
import csv
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parent
COMMIT = '5f7994400869c921dec5b335f04a384a713e5e64'
SOURCES = [
    ('CST_Staubball_Kopplungsscan_v0_2_Pruefpaket.zip', '93741d09f47c87fc757653886f6c93fb42b8699b9830c66639b195bf05457ee0', '097533f6089fe0d2dadcd6e9261e1e7dab16fffb'),
    ('CST_Staubball_Dichtespur_v0_1_Pruefpaket.zip', 'e687a058e77a686ea40d0eb817981c1213d32a52b79c5eef7fe4915f5ef6760e', '5820f35cf6674d92ad5c68c63c994e88346d41cb'),
    ('Staubball_Bounce_Regularitaet_Pruefpaket.zip', 'b0515a05125a8366daddc1752e4f8bdf23804ccfa83d441f358dd6242b641376', '0796bc5ebef0f405a7aad1cd6dfc03e7c458482c'),
]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def expected_support(name):
    first = (-1, 0, 1) if name == 'development' else (-2, 2)
    paths = []
    for a,b,c in itertools.product(first, (-1,0,1), (-1,0,1)):
        w = (5,4,4+a,4+a+b,4+a+b+c)
        if min(w) > 0:
            paths.append(w)
    return paths

def is_bounce(w):
    v = [F(x**3,125) for x in w]
    return (v[2] >= F(1,20) and v[0]-v[1] >= F(1,20)
            and v[1]-v[2] >= F(1,20) and v[3]-v[2] >= F(1,20)
            and v[4]-v[3] >= F(1,20))

def certificate(folder, name):
    paths = expected_support(name)
    rows = list(csv.DictReader((folder/'source'/f'{name}.csv').open()))
    for level in ('0','1'):
        archived = [tuple(map(int,r['path'].split('-'))) for r in rows if r['level']==level]
        require(len(archived)==len(set(archived)) and set(archived)==set(paths), 'support mismatch')
    bounce = [w for w in paths if is_bounce(w)]
    require(len(bounce)==1, 'not exactly one bounce')
    ends = collections.defaultdict(list)
    for w in paths:
        ends[(4*w[-1]**3)//125].append(w)
    isolated = [ws[0] for ws in ends.values() if len(ws)==1 and not is_bounce(ws[0])]
    require(len(isolated)>=1, 'missing non-bounce singleton')
    # Every singleton contributes a nonnegative protected diagonal norm.
    bound = F(1,1+len(isolated))
    require(bound < F(4,5), 'bound does not exclude dominance')
    return dict(history_count=len(paths), bounce=list(bounce[0]),
                isolated_non_bounce=[list(w) for w in isolated],
                end_channel_sizes={str(k):len(v) for k,v in sorted(ends.items())},
                uniform_amplitude_magnitude=f'1/{len(paths)}',
                pointer_bound=str(bound), required_dominance='4/5',
                ideal_full_path_decoherence_qB=str(F(1,len(paths))))

def main(out):
    out.mkdir(parents=True, exist_ok=True)
    candidate_bytes=(ROOT/'candidate_snapshot.json').read_bytes()
    candidate_sha=sha(candidate_bytes)
    require(candidate_sha=='0a017e1f2ab894578fb5f007a473f480d1460e39fc4369be629dc06ea1d248e0', 'candidate snapshot changed')
    provenance=[]
    with tempfile.TemporaryDirectory(prefix='x6-bounce-closure-') as tmp:
        work=Path(tmp)
        folders=[]
        for i,(name, digest, blob) in enumerate(SOURCES):
            data=(ROOT/'sources'/name).read_bytes()
            require(sha(data)==digest, f'archive SHA256 mismatch: {name}')
            actual_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(actual_blob==blob, f'Git blob mismatch: {name}')
            folder=work/str(i);folder.mkdir()
            with zipfile.ZipFile(ROOT/'sources'/name) as z:
                for m in z.infolist():
                    require(not Path(m.filename).is_absolute() and '..' not in Path(m.filename).parts,'unsafe archive path')
                z.extractall(folder)
            checked=[]
            for line in (folder/'SHA256SUMS').read_text().splitlines():
                h,p=line.split(maxsplit=1);p=p.lstrip('*')
                require(sha((folder/p).read_bytes())==h, f'internal digest mismatch: {p}')
                checked.append(p)
            provenance.append(dict(name=name, sha256=digest, git_blob_sha1=blob,
                repository_path='research/rax_cqg/dust_collapse/packages/'+name,
                verified_member_count=len(checked)))
            folders.append(folder)
        certificates={name:certificate(folders[0],name) for name in ('development','holdout')}
        require(not set(expected_support('development'))&set(expected_support('holdout')),'families overlap')
        commands=[(0,['scan.py','--out',str(work/'scan')]),
                  (0,['audit.py','--out',str(work/'scan')]),
                  (1,['run.py','--out',str(work/'density')]),
                  (2,['finite_checks.py'])]
        logs=[]
        finite_bytes=None
        for i,args in commands:
            proc=subprocess.run([sys.executable,*args],cwd=folders[i],check=True,capture_output=True,text=True)
            logs.append('$ python3 '+' '.join(args).replace(str(work),'<temporary>')+'\n'+proc.stdout+proc.stderr)
            if args==['finite_checks.py']:
                finite_bytes=proc.stdout.encode()
        comparisons=[]
        pairs=[(folders[0]/'results/scan.json',work/'scan/scan.json'),
               (folders[0]/'results/audit.json',work/'scan/audit.json')]
        pairs += [(folders[1]/'results'/p.name,p) for p in sorted((work/'density').iterdir()) if p.is_file()]
        for reference,replay in pairs:
            a,b=reference.read_bytes(),replay.read_bytes()
            # JSON floating fields permit only 1e-12 absolute/relative variation.
            def close(x,y):
                if isinstance(x,float) and isinstance(y,(float,int)):
                    return abs(x-y)<=1e-12*max(1,abs(x))
                if isinstance(x,dict) and isinstance(y,dict):
                    return x.keys()==y.keys() and all(close(x[k],y[k]) for k in x)
                if isinstance(x,list) and isinstance(y,list):
                    return len(x)==len(y) and all(close(u,v) for u,v in zip(x,y))
                return x==y
            valid=a==b or reference.suffix=='.json' and close(json.loads(a),json.loads(b))
            require(valid, f'replay differs: {reference.name}')
            comparisons.append(dict(file=reference.name,byte_identical=a==b,
                                    replay_sha256=sha(b),status='PASS'))
        require(finite_bytes==(folders[2]/'finite.json').read_bytes(),'finite replay differs')
        comparisons.append(dict(file='finite.json',byte_identical=True,replay_sha256=sha(finite_bytes),status='PASS'))
        scan=json.loads((work/'scan/scan.json').read_text())
        audit=json.loads((work/'scan/audit.json').read_text())
        for mode in ('total','split'):
            require(scan['holdout'][mode]['bands']==[['32/45','162/95','FAIL']], 'holdout scan changed')
            require(scan['holdout'][mode]['points']['0']['gate']=='HOLD','zero-gain control changed')
            for level in ('coarse','fine'):
                upper=F(audit['full_band_enclosures']['holdout_'+mode][level+'_qB'][1])
                require(upper<F(682,10000),'6.82 percent bound changed')
        require(audit['transfer_agreements']==1 and len(audit['transfer'])==4,'transfer record changed')
        # Scope counterexamples: removing premises invalidates the 1/2 claim.
        def exact_diagonal_share(rows):
            channels=collections.defaultdict(int)
            for label,channel,amplitude in rows:
                channels[label,channel]+=amplitude
            norms={label:sum(a*a for (c,_),a in channels.items() if c==label) for label in ('B','N')}
            return F(norms['B'],norms['B']+norms['N'])
        unequal_weight_q=exact_diagonal_share([('B',0,2),('N',1,1)])
        protected_q=exact_diagonal_share([('B',0,1),('N',1,1),('N',2,-1)])
        erased_endpoint_q=exact_diagonal_share([('B',0,1),('N',1,1),('N',1,-1)])
        require(protected_q==F(1,3),'protected endpoint control failed')
        require(unequal_weight_q>F(1,2) and erased_endpoint_q>F(1,2),'scope controls failed')
        result=dict(schema='x6-bounce-candidate-closure/v0.1', date='2026-11-05',
            source_commit=COMMIT, sources=provenance,
            candidate_snapshot_sha256=candidate_sha,
            evidence_class='RETROSPECTIVE_FINITE_MODEL_REANALYSIS',
            decision='CLOSED_REJECTED_FOR_DOMINANT_BOUNCE',
            global_cst_bounce='HOLD', singularity_resolution='HOLD',
            original_gate_statuses_preserved=True, certificates=certificates,
            holdout_coupling_interval=['32/45','162/95'],
            holdout_bands={m:scan['holdout'][m]['bands'] for m in ('total','split')},
            holdout_qB_upper_exact=audit['full_band_enclosures']['holdout_total']['coarse_qB'][1],
            transfer=audit['transfer'], independent_statistical_trials=False,
            replay_comparisons=comparisons, direct_pair_comparisons=120,
            scope_controls=dict(unequal_amplitudes_qB=str(unequal_weight_q),
                                protected_endpoints_qB=str(protected_q),
                                removed_endpoint_protection_qB=str(erased_endpoint_q)),
            not_rerun=['full causal-order generation', '18 explicit-order recounts', '70 inverse-moment quadratures'],
            physical_measurements_performed=False, external_preregistration=False)
        (out/'closure_result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
        (out/'replay.log').write_text('\n'.join(logs))
        for f in ('scan.json','audit.json'):
            (out/f).write_bytes((work/'scan'/f).read_bytes())
        print(json.dumps(dict(decision=result['decision'], verified_archives=3,
            verified_members=sum(p['verified_member_count'] for p in provenance),
            replay_files=len(comparisons), point_comparisons=120,
            certificate_bounds={k:v['pointer_bound'] for k,v in certificates.items()}),indent=2))

if __name__=='__main__':
    require(__debug__,'Do not use Python -O; source controls require assertions')
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'replay')
    main(p.parse_args().out)
