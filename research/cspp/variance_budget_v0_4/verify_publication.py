"""Publication integrity and isolated replay; this guard cannot grant G1."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from flint import arb, ctx

HERE = Path(__file__).resolve().parent
ARCHIVE_SHA256 = '74bf143e53c60cc6fc1905e5cb9c12eee6f5b3f1c8373e6a49f7ab53663c5a7a'
GATES = {'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}


def check(ok, message):
    if not ok:
        raise SystemExit('FAIL: '+message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrity():
    p=json.loads((HERE/'PUBLICATION.json').read_text())
    check(p['scientific_status']==GATES, 'publication science scope')
    check(p['original_archive_sha256']==ARCHIVE_SHA256, 'original archive identity')
    archive=HERE/p['original_archive']
    check(sha(archive)==ARCHIVE_SHA256, 'original archive bytes')
    original=p['original_file_sha256']
    check(len(original)==12, 'original file inventory')
    for name,digest in original.items():
        check(not Path(name).is_absolute() and '..' not in Path(name).parts, 'safe original path')
        check(sha(HERE/name)==digest, 'original source/result '+name)
    with zipfile.ZipFile(archive) as z:
        expected={'CSPP_Varianzbudget_v0_4/'+name for name in original}
        check(set(z.namelist())==expected, 'exact archive inventory')
        for name in original:
            check(z.read('CSPP_Varianzbudget_v0_4/'+name)==(HERE/name).read_bytes(), 'archive equality '+name)
    actual={f.relative_to(HERE).as_posix() for f in HERE.rglob('*')
            if f.is_file() and '__pycache__' not in f.parts}
    check(actual==set(original)|{'PUBLICATION.json','verify_publication.py',p['original_archive']},
          'explicit publication inventory')
    for snapshot,current in [('BUDGET_v0_3.json','results/BUDGET.json'),
                             ('PROTOCOL_v0_3.json','PROTOCOL.json')]:
        check((HERE/'baseline'/snapshot).read_bytes()==
              (HERE.parent/'certified_budget_v0_3'/current).read_bytes(), 'unchanged v0.3 baseline')
    contract=json.loads((HERE.parent/'e4_v0_1/contract.json').read_text())
    check(contract['freeze_status']=='NOT_FROZEN', 'E4 remains unfrozen')
    record=json.loads((HERE/'results/BUDGET.json').read_text())
    check(record['gate_status']==GATES and not record['confirmation_seed_used']
          and record['new_poisson_clouds']==0, 'no new confirmations')
    check(record['full_covariance_spatial_integral']=='NOT_EVALUATED', 'spatial integration remains open')
    check(len(record['upper_rows'])==7, 'seven upper budgets')
    ctx.prec=192
    for row in record['upper_rows']:
        rho=int(row['rho_sufficient'])
        check(arb(row['upper_coefficient']['ball'])/rho<=arb('7/200')**2,
              'archived sufficient inequality')
        check(arb(rho)>=arb(row['upper_bound_components']['rho_regime_min']['ball']),
              'archived smoothing regime')
    lower=record['lower_witness']
    check(arb(lower['coefficient']['ball'])>0, 'positive lower coefficient')
    check(lower['ell_k']=='1/8' and lower['H']==20, 'fixed lower-witness scope')
    audit=json.loads((HERE/'results/AUDIT.json').read_text())
    check(audit['status']=='PASS' and audit['exact_identities']==253
          and audit['poisson_kernel']['cases']==36 and audit['poisson_kernel']['negative_controls']==2
          and audit['geometry']['angular_cases']==47, 'original audit complete')
    return record


def compare_recorded(old,new):
    check(new['gate_status']==GATES and new['baseline']==old['baseline'], 'replay gates and baseline')
    for a,b in zip(old['upper_rows'],new['upper_rows']):
        for key in ['ell_k','H','single_witness_RMS_at_most_10_percent',
                    'witness_10_percent_RMS_excluded_by_bias','scope']:
            check(a[key]==b[key], 'archived replay '+key)
        # Endpoint-derived majorants can differ in last bits; the fresh run
        # independently verifies its own sufficient inequalities.
        check(abs(int(a['rho_sufficient'])/int(b['rho_sufficient'])-1)<1e-8,
              'archived density regression screen')
    check(arb(old['lower_witness']['coefficient']['ball']).overlaps(
          arb(new['lower_witness']['coefficient']['ball'])), 'archived lower coefficient')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    old=integrity()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='cspp-variance-replay-') as tmp:
            work=Path(tmp)/'package'
            shutil.copytree(HERE,work,ignore=shutil.ignore_patterns('original','__pycache__'))
            for script,extra in [('audit.py',[]),('run.py',['--output','results/BUDGET_REPLAY.json'])]:
                outcome=subprocess.run([sys.executable,'-B',str(work/script),*extra],
                                       cwd=work,capture_output=True,text=True)
                if outcome.returncode:
                    raise SystemExit(outcome.stdout+outcome.stderr)
            compare_recorded(old,json.loads((work/'results/BUDGET_REPLAY.json').read_text()))
            compare_recorded(old,json.loads((work/'results/BUDGET_192bit.json').read_text()))
        integrity()
    print(json.dumps({'status':'PASS','original_files':12,'original_zip_unchanged':True,
                      'isolated_replay':args.replay,'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}))


if __name__=='__main__':main()
