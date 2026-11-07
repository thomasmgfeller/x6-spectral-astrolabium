#!/usr/bin/env python3
"""Original-artifact integrity, scope guards and isolated finite replay."""
import argparse,hashlib,json,subprocess,sys,tempfile,zipfile
from fractions import Fraction as F
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
NAME='CST_DUST_Positive_Historien_Schnittkonsistenz_v0_1'
ZIP_HASH='0abb7653154724bca81e850664db7f3015284416b6cacd5d69624438e89f0e28'
PDF_HASH='b0db3a20fad2429921391694aac2b93182acf1a79b65061a77e4c26b5f50373c'
PLAN_HASH='1156cb82360481f8d3de1d4ba316e725157689babf9b578f8a689103c4538e55'
PARENT='d9622fb0423725026fab73d6884a499322cb014f'
EXACT={'continuum_certificates.json','history_events.json','cut_controls.json','joint_relative_measure.json','verification.json'}
GATES={'MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def check_scope(read):
    v=json.loads(read('results/verification.json'))
    require(v['source_commit']==PARENT and v['plan_sha256']==PLAN_HASH,'Source and plan')
    require(set(v['physical_decisions'])==GATES and set(v['physical_decisions'].values())=={'HOLD'},'Eight physical HOLDs')
    require(v['formal_proof_checker'] is False and v['new_dynamical_CST_ensembles'] is False
            and v['reference_tests_are_physical_measurements'] is False,'Claim scope')
    expected={'FINITE_AUXILIARY_STRONGLY_POSITIVE_D':'PASS_CONDITIONAL_ON_DECLARED_BOUNDARY_PRODUCT',
      'SINGLE_CONSTANT_NORMALIZATION_ALL_CONTINUUM_STATES':'FAIL_FOR_RAW_COMPACT_KERNEL_FAMILY',
      'NORMALIZED_D_IS_AUTOMATIC_PROBABILITY':'FAIL_FOR_INTERFERING_PARTITION',
      'MARKOV_CUT_MAP_FOR_FULL_CST':'NOT_DERIVED','PHYSICAL_DECOHERENCE_FUNCTIONAL':'HOLD',
      'INFINITE_HISTORY_EXTENSION':'NOT_EXECUTED'}
    require(v['scoped_decisions']==expected,'Scoped interpretations')
    require(v['source_files_byte_verified']==5 and v['polynomial_evaluation_checks']==25,'Source/evaluation counts')
    require(v['exact_event_checks']=={'hermiticity':64,'biadditivity':432,'normalization':1,
        'grade_two':64,'positive_quadratic_probes':64},'Exact event checks')
    require(v['supplement_01_sha256']==sha(read('supplement_01.json')),'Supplement')
    c=json.loads(read('results/continuum_certificates.json'))
    require(c['L']=='1' and c['p']==40,'Declared regulator and degree')
    z0,z1=c['Z_constant_mode'],c['Z_linear_normalized_mode']
    require(F(z0['exact_lower'])>F(z1['exact_upper'])>0,'Separated norm intervals')
    require(F(c['equal_prior_flag0_after_conditioning']['exact_lower'])>F(1,2),'Conditioned preparation flag')
    h=json.loads(read('results/history_events.json'))
    require(h['events']==8 and F(h['sum_diagonal']['exact_upper'])<1
            and F(h['real_D01']['exact_lower'])>0,'Interference witness')
    require(h['strong_positivity']=='PROVED_BY_GRAM_FORM_NOT_BY_FINITE_PROBES','Positivity proof scope')
    require(json.loads(read('results/joint_relative_measure.json'))['exact_moment_checks']==75,'Shared-clock measure')
    require(json.loads(read('results/cut_controls.json'))['exact_checks']==21,'Cut controls')
    q=json.loads(read('results/quadrature_check.json'))
    require(q['certification'] is False and q['status']=='PASS'
            and [x['order'] for x in q['records']]==[64,96]
            and sum(x['complex_or_real_comparisons'] for x in q['records'])==26
            and all(x['max_absolute_difference']<=q['threshold'] for x in q['records']),'Archived independent supplement')
def run(replay=False):
    archive=ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes())==ZIP_HASH,'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();prefix=NAME+'/'
        require(len(names)==len(set(names))==29 and z.testzip() is None,'Archive inventory')
        for name in names:
            rel=PurePosixPath(name)
            require(not rel.is_absolute() and '..' not in rel.parts and name.startswith(prefix),'Safe archive member')
            require(z.read(name)==(ROOT/name[len(prefix):]).read_bytes(),'Original member bytes: '+name)
        read=lambda p:z.read(prefix+p)
        listed=set()
        for line in read('MANIFEST.sha256').decode().splitlines():
            digest,p=line.split(maxsplit=1)
            require(p not in listed and sha(read(p))==digest,'Original manifest entry: '+p);listed.add(p)
        require({prefix+p for p in listed}==set(names)-{prefix+'MANIFEST.sha256'},'Complete manifest')
        require(sha(read(NAME+'.pdf'))==PDF_HASH and read(NAME+'.pdf')==(ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(),'PDF copies')
        require(sha(read('plan.json'))==PLAN_HASH==read('plan.sha256').decode().split()[0],'Frozen plan')
        prov=json.loads(read('inputs/provenance.json'))
        require(prov['commit']==PARENT and len(prov['files'])==5,'Source provenance')
        for name,entry in prov['files'].items():
            rel=PurePosixPath(entry['path'])
            require(not rel.is_absolute() and '..' not in rel.parts,'Safe source path')
            data=read('inputs/'+name)
            require(data==(REPO/entry['path']).read_bytes() and sha(data)==entry['sha256'],'Byte-identical source: '+name)
        receipt=json.loads(read('results/replay.json'))
        require(receipt['isolated_replay']=='PASS' and receipt['result_files']==5
            and {x['name'] for x in receipt['checks']}==EXACT,'Replay receipt inventory')
        for item in receipt['checks']:
            require(item['byte_identical'] and item['sha256']==sha(read('results/'+item['name'])),'Replay digest')
        check_scope(read)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cst-histories-publication-') as tmp:
                z.extractall(tmp);work=Path(tmp)/NAME
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes()==read('results/replay.json'),'Isolated replay receipt')
    print('PASS: original ZIP, 29 members, PDF, five byte-identical source inputs, scoped claims and eight physical HOLDs'
          + ('; five exact result files reproduced byte-for-byte in isolation' if replay else ''))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');run(p.parse_args().replay)
