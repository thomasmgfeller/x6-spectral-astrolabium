#!/usr/bin/env python3
"""Publication integrity and isolated finite audit; no physical proof checker."""
import argparse,hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
NAME='CST_DUST_Eichstruktur_Randkonsistenz_v0_1'
PREFIX=NAME+'/'
ZIP_HASH='80c948a0e53ca2c0f6a29e8e2354ad97b92dd1df786a0f0b3fbcc59fa0024606'
PDF_HASH='dcb47289b9ad298f2846aaa92553a79d927a6c2e7aa89af8c1680dd043658272'
PLAN_HASH='f1075751c5a170bfb9d531a431c6e094214ab4bd2b2781f3eca32c09afa751c5'
PARENT='374acc67cb0e6cc510ec3852fd9fe9ef2b5ed20a'
DEPS={
 'variation.py':'variation_v0_1/variation.py','gluing.py':'gluing_v0_1/gluing.py',
 'parent_contract.json':'model_contract_v0_1/contract.json','parent_gate.py':'model_contract_v0_1/gate.py',
 'variation_DERIVATION.md':'variation_v0_1/DERIVATION.md',
 'quantum_structure_DERIVATION.md':'quantum_structure_v0_1/DERIVATION.md',
 'gluing_DERIVATION.md':'gluing_v0_1/DERIVATION.md'}
EXACT=['enumeration.csv','rank_histogram.csv','relative_measure.csv',
 'amplitude_certificates.json','amplitude_certificates_interior.json','witnesses.json','verification.json']
GATES={'MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def check_scope(read):
    v=json.loads(read('results/verification.json'))
    require(v['source_commit']==PARENT and v['plan_sha256']==PLAN_HASH,'Source/plan')
    require(v['new_dynamical_CST_ensembles'] is False and v['formal_proof_checker'] is False,'Claim scope')
    require(set(v['physical_decisions'])==GATES and set(v['physical_decisions'].values())=={'HOLD'},'Physical decisions')
    require(v['finite']['checks']['marked_cases']==3670 and v['finite']['checks']['relabel_checks']==85034,'Finite checks')
    require(v['finite']['boundary_splits']=={'cuts':49992,'flat_for_all_T':19172,'relative_mode_coupled':30820},'Cut checks')
    require(v['finite']['vacuum_columns']=={'sites':7249,'flat_columns':4708,'coupled_columns':2541},'Vacuum checks')
    require(v['relative_measure']['exact_checks']==2508,'Measure checks')
    expected={'NAIVE_RESET_KEEPING_BOX':'FAIL_AS_EQUIVALENT_REWRITE',
      'ALL_VACUUM_CLOCKS_ARE_FREE_GAUGE':'FAIL_FOR_INHERITED_ACTION',
      'INDEPENDENT_BLOCK_ORIGIN_RESET':'FAIL_WITHOUT_RELATIVE_DATA',
      'PHYSICAL_GAUGE_QUANTIZATION':'HOLD','GRAVITATIONAL_ANOMALY':'NOT_ESTABLISHED'}
    require(all(v['scoped_decisions'].get(k)==val for k,val in expected.items()),'Scoped interpretations')
    for key in ['amplitudes','interior_density_amplitudes']:
        require(v[key]['certified_checks']==24 and v[key]['fixed_box_counterexamples']==9
                and v[key]['relative_measure_counterexamples']==3,'Amplitude controls')
    require(v['supplement_01_sha256']==sha(read('supplement_01.json')),'Supplement hash')
    interior=json.loads(read('results/amplitude_certificates_interior.json'))
    require(interior['w']=='1/2','Interior-stratum witness')
    w=json.loads(read('results/witnesses.json'))
    require(w['vacuum']['interior_density_delta_S']=='1/16','Interior vacuum counterexample')
    q=json.loads(read('results/quadrature_check.json'))
    require(q['checks']==66 and q['max_absolute_difference']<1e-11 and q['certification'] is False,'Supplementary quadrature scope')

def run(replay=False):
    archive=ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes())==ZIP_HASH,'Original archive hash')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        require(len(names)==len(set(names))==33 and z.testzip() is None,'Original archive inventory')
        for name in names:
            p=PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(PREFIX),'Unsafe archive member')
            require(z.read(name)==(ROOT/name[len(PREFIX):]).read_bytes(),'Original member bytes: '+name)
        read=lambda p:z.read(PREFIX+p)
        listed=set()
        for line in read('MANIFEST.sha256').decode().splitlines():
            digest,p=line.split(maxsplit=1)
            require(p not in listed and sha(read(p))==digest,'Original manifest member: '+p);listed.add(p)
        require({PREFIX+p for p in listed}==set(names)-{PREFIX+'MANIFEST.sha256'},'Complete original manifest')
        require(sha(read(NAME+'.pdf'))==PDF_HASH and read(NAME+'.pdf')==(ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(),'Report bytes')
        require(sha(read('plan.json'))==PLAN_HASH==read('plan.sha256').decode().split()[0],'Frozen plan')
        provenance=json.loads(read('inputs/provenance.json'))
        require(provenance['commit']==PARENT and set(provenance['files'])==set(DEPS),'Inherited input inventory')
        # Disclosed publication clarification: the seven archived input copies
        # contain exactly one additional final LF. Never strip arbitrary whitespace.
        for name,path in DEPS.items():
            data=read('inputs/'+name);original=(ROOT.parent/path).read_bytes()
            require(data==original+b'\n' and sha(data)==provenance['files'][name],'Inherited bytes and exact LF note: '+name)
        receipt=json.loads(read('results/replay.json'))
        require(receipt['isolated_replay']=='PASS' and receipt['result_files']==7
                and {x['name'] for x in receipt['checks']}==set(EXACT),'Original replay receipt')
        for item in receipt['checks']:
            require(item['byte_identical'] and item['sha256']==sha(read('results/'+item['name'])),'Original replay digest')
        check_scope(read)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cst-gauge-publication-') as temp:
                z.extractall(temp);work=Path(temp)/NAME
                # replay.py creates an isolated source-only working directory and
                # requires byte-identical regeneration of all seven exact outputs.
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes()==read('results/replay.json'),'Replay receipt equality')
    print('PASS: original ZIP, 33 members, PDF, complete hashes, exact inherited-input LF clarification, '
          'scoped counterexamples and eight physical HOLD decisions'
          + ('; isolated replay regenerates all seven exact result files byte-for-byte' if replay else ''))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');run(p.parse_args().replay)
