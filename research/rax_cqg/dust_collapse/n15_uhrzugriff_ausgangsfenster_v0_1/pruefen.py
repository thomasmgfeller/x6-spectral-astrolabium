"""Replay exact and numerical results. No network connection is needed."""
import argparse,hashlib,json,math
from fractions import Fraction as Q
from pathlib import Path
BASE=Path(__file__).resolve().parent

def load(name):return json.loads((BASE/name).read_bytes())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def compare(value,archive,atol=2e-7):
    if isinstance(value,dict):
        assert value.keys()==archive.keys()
        for k in value:compare(value[k],archive[k],atol)
    elif isinstance(value,list):
        assert len(value)==len(archive)
        for a,b in zip(value,archive):compare(a,b,atol)
    elif isinstance(value,float):assert math.isclose(value,archive,rel_tol=2e-11,abs_tol=atol),(value,archive)
    else:assert value==archive,(value,archive)

def audit_exact():
    from durchlass import run
    for f in ['SHA256SUMS','pruefplan.sha256','ergaenzung.sha256','paarplan.sha256','eichung_streng.sha256','paareichung.sha256']:
        for line in (BASE/f).read_text().splitlines():
            want,file=line.split(maxsplit=1);assert digest(BASE/file)==want,file
    provenance=load('herkunft.json');assert provenance['commit']=='70bad55df756781318fccfd0aec03921a3934fde'
    for f,meta in provenance['files'].items():assert digest(BASE/'quellen'/f)==meta['sha256']
    for f,plan in [('eichung_streng.json','pruefplan.txt'),('paareichung.json','paarplan.txt')]:assert load(f)['plan_sha256']==digest(BASE/plan)
    data=run();assert data==load('durchlass.json')
    for k,row in load('transfer.json').items():
        if not k.endswith('|strict'):continue
        sec='positive' if '|positive|' in k else 'atom'
        for tag,s in data['strict_acceptance'][sec].items():
            val=row['fine']['admitted'][tag];lo,hi=map(Q,s['total']);assert float(lo)-2e-12<=val<=float(hi)+2e-12
            for v,z in zip(row['fine']['admitted_by_lobe'][tag],s['by_lobe']):
                lo,hi=map(Q,z);assert float(lo)-2e-12<=v<=float(hi)+2e-12
    p=load('quellen/p3.json');assert len(p)==60 and all(x['checkpoint_id']=='P3' and x['execution']=='NOT_RUN' for x in p)
    print('PASS: 5040 relabellings, window bounds, interval-certified accepted fractions, source digests. P3: 60 NOT_RUN.',flush=True)

def calibration(result,filename):
    archived=load(filename)
    # Serialized decimal estimates may differ in their last digits across platforms.
    assert abs(float(result['offset'])-float(archived['offset']))<2e-7
    assert result['gain'] is None and archived['gain'] is None
    a={k:v for k,v in result.items() if k!='offset'};b={k:v for k,v in archived.items() if k!='offset'};compare(a,b)

def audit_numeric():
    import eichlauf,transfer,interferenz,paarung
    calibration(eichlauf.run(),'eichung_streng.json');rows=transfer.run();compare(rows,load('transfer.json'))
    for k,row in rows.items():
        for tag,pair in row['fine']['kernels'].items():
            assert abs(complex(*pair))<=row['fine']['admitted'][tag]+1e-13
        if k.endswith('wide'):
            assert row['fine']==rows[k[:-4]+'open']['fine']
        if row['cc_check']:
            assert abs(row['cc_check']['raw']-row['fine']['raw'])<2e-7
    vis=interferenz.run(rows);compare(vis,load('interferenz.json'))
    calibration(paarung.cal(),'paareichung.json');matched=paarung.run();compare(matched,load('paarung.json'))
    assert all(abs(r['raw']-r['cc_control'])<2e-7 for r in matched.values())
    print('PASS: both calibration attempts, 24 model cases, Gauss and Clenshaw-Curtis quadratures, both-arm projection, coherent readout and record control.')
    for k,v in rows.items():
        if '|positive|1|' in k and not k.endswith('open'):print(k,round(v['with_original_calibration'],9))

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O.')
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--nur-exakt',action='store_true');args=ap.parse_args();audit_exact()
    if not args.nur_exakt:audit_numeric()
