"""Lossless evidence assembly and frozen-analysis adapter after interruption.

No frozen inference/calibration/analysis source is edited. Only resource gates
are conservatively blocked because the original telemetry is incomplete.
"""
import argparse
import hashlib
import importlib.util
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from mb_common import HERE, ROOT, contract, write_json
from resume_run import original_checkpoint
import mb_analyze
from matrix_diagnostics import diagnose

# Inherited modules prepend their own directories to sys.path. Load this
# experiment's frozen verifier explicitly, rather than an ancestor's verify.py.
_spec=importlib.util.spec_from_file_location('metadata_frozen_verifier',HERE/'verify.py')
frozen_verify=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(frozen_verify)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def zip_bytes(path,files):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,20,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,raw)


def package_continuation():
    target=HERE/'continuation_clouds.zip'
    if target.exists(): return
    cp=original_checkpoint(); files={}; seeds=[]
    for shard in [0,1]:
        folder=HERE/f'continuation-{shard}'
        raw=(folder/'execution.json').read_bytes(); e=json.loads(raw)
        assert e['status']=='COMPLETE' and e['current_seed'] is None
        files[f'continuation-{shard}/execution.json']=raw
        for item in e['records']:
            raw=(folder/item['file']).read_bytes(); assert sha(raw)==item['sha256']
            files[f'continuation-{shard}/'+item['file']]=raw
            seeds.append(json.loads(raw)['seed'])
    assert sorted(seeds)==cp['missing_seeds']
    zip_bytes(target,files)


def assemble(dest):
    cp=original_checkpoint(); frozen=json.loads((HERE/'frozen_model.json').read_text())
    assert sha((HERE/'frozen_model.json').read_bytes())==cp['calibration_sha256']
    raw_rows={}; old_logs={}; new_logs={}; files={}
    with zipfile.ZipFile(HERE/'interrupted_clouds.zip') as z:
        for shard in [0,1]:
            name=f'test-{shard}/execution.json'; raw=z.read(name)
            old_logs[shard]=(json.loads(raw),sha(raw))
            for item in old_logs[shard][0]['records']:
                name=f'test-{shard}/'+item['file']; raw=z.read(name)
                assert sha(raw)==item['sha256']==cp['record_sha256'][name]
                row=json.loads(raw); raw_rows[row['seed']]=raw
    assert len(raw_rows)==27
    with zipfile.ZipFile(HERE/'continuation_clouds.zip') as z:
        for shard in [0,1]:
            raw=z.read(f'continuation-{shard}/execution.json'); e=json.loads(raw)
            new_logs[shard]=(e,sha(raw))
            assert e['status']=='COMPLETE' and e['current_seed'] is None
            assert e['source_sha256']==frozen['source_sha256']==cp['source_sha256']
            assert e['original_freeze']==cp['source_commit']
            assert e['checkpoint_sha256']==sha((HERE/'checkpoint.json').read_bytes())
            assert e['calibration_sha256']==cp['calibration_sha256']
            assert e['planned_seeds']==[s for s in cp['missing_seeds'] if s%2==shard]
            for path,h in e['continuation_source_sha256'].items():
                assert sha((ROOT/path).read_bytes())==h,path
            for item in e['records']:
                raw=z.read(f'continuation-{shard}/'+item['file']); assert sha(raw)==item['sha256']
                row=json.loads(raw); seed=row['seed']
                assert seed not in raw_rows and seed in e['planned_seeds']
                raw_rows[seed]=raw
    expected=list(range(contract()['test_seeds'][0],contract()['test_seeds'][1]+1))
    assert sorted(raw_rows)==expected
    for shard in [0,1]:
        old,old_sha=old_logs[shard]; new,new_sha=new_logs[shard]
        entries=[]
        for seed in expected[shard::2]:
            name=f'seed-{seed}.json'; raw=raw_rows[seed]
            files[f'test-{shard}/'+name]=raw
            entries.append(dict(file=name,sha256=sha(raw)))
        old_seconds=sum(json.loads(raw_rows[int(v['file'][5:-5])])['seconds'] for v in old['records'])
        e=dict(status='RESUMED_COMPLETE',shard=shard,source_commit=cp['source_commit'],
            source_sha256=cp['source_sha256'],calibration_sha256=cp['calibration_sha256'],records=entries,
            seconds=old_seconds+new['seconds'],peak_mib=new['peak_mib'],
            resource_fields='LOWER_BOUNDS_ONLY_NOT_FULL_MEASUREMENTS',
            original_execution_sha256=old_sha,continuation_execution_sha256=new_sha,
            continuation_source_commit=new['source_commit'],continuation_seconds=new['seconds'],
            continuation_peak_mib=new['peak_mib'])
        files[f'test-{shard}/execution.json']=(json.dumps(e,indent=2)+'\n').encode()
    for name,raw in files.items():
        p=dest/name; p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    for name in ['frozen_model.json','residual_calibration.zip']:
        shutil.copyfile(HERE/name,dest/name)
    zip_bytes(dest/'test_clouds.zip',files)
    return [json.loads(raw_rows[s]) for s in expected],new_logs


def analyze_at(dest):
    previous=mb_analyze.HERE; mb_analyze.HERE=dest
    try:
        result=mb_analyze.analyze(save=False)
        executions,_=mb_analyze.load_rows()
    finally: mb_analyze.HERE=previous
    # Statistical output is untouched. Unknown interrupted-run resource bounds
    # cannot be passed off as measured total runtime/peak-RSS.
    assert result['gates']['execution_complete'] is False
    result['gates']['budgets']=False
    result['decision']='METADATA_HOLD'
    result['all_planned_cloud_records_present']=result['total']==32
    result['resource_gate_status']='UNVERIFIED_ORIGINAL_PROCESS_TELEMETRY_MISSING'
    result['gate_explanations']={k:'Unverified after original process interruption; no complete resource/execution telemetry.'
                                 for k in ['execution_complete','budgets']}
    result['statistical_gates_passed']=all(v for k,v in result['gates'].items() if k not in ['execution_complete','budgets'])
    for out,e in zip(result['execution'],executions):
        out.update(seconds=None,peak_mib=None,elapsed_lower_bound=e['seconds'],
                   peak_lower_bound=e['peak_mib'],continuation_seconds=e['continuation_seconds'],
                   continuation_peak_mib=e['continuation_peak_mib'],
                   continuation_source_commit=e['continuation_source_commit'])
    result['resumption']=dict(original_records_preserved=27,additional_records=5,
        protocol='RESUMPTION.md',original_raw_archive_sha256=sha((HERE/'interrupted_clouds.zip').read_bytes()),
        continuation_archive_sha256=sha((HERE/'continuation_clouds.zip').read_bytes()),
        statistical_analysis='Unmodified mb_analyze.py; only resource reporting/gates conservatively overridden.')
    return result


def finalize():
    package_continuation()
    with tempfile.TemporaryDirectory(prefix='metadata-complete-') as tmp:
        dest=Path(tmp); rows,_=assemble(dest)
        result=analyze_at(dest);write_json(HERE/'summary.json',result)
        write_json(HERE/'matrix_diagnostics.json',diagnose(rows))
        shutil.copyfile(dest/'test_clouds.zip',HERE/'test_clouds.zip')
    names=['interrupted_clouds.zip','continuation_clouds.zip','test_clouds.zip',
           'frozen_model.json','residual_calibration.zip','summary.json','matrix_diagnostics.json','checkpoint.json']
    write_json(HERE/'manifest.json',{n:sha((HERE/n).read_bytes()) for n in names})
    print(json.dumps({k:result[k] for k in ['decision','complete','comparisons','gates','statistical_gates_passed']},indent=2))


def verify_all(strict=False):
    for name,h in json.loads((HERE/'manifest.json').read_text()).items():
        assert sha((HERE/name).read_bytes())==h,name
    with tempfile.TemporaryDirectory(prefix='metadata-replay-') as tmp:
        dest=Path(tmp); rows,_=assemble(dest)
        with zipfile.ZipFile(HERE/'test_clouds.zip') as saved,zipfile.ZipFile(dest/'test_clouds.zip') as regenerated:
            assert saved.namelist()==regenerated.namelist()
            for name in saved.namelist(): assert saved.read(name)==regenerated.read(name),name
        expected=json.loads((HERE/'summary.json').read_text())
        frozen_verify.compare(analyze_at(dest),expected)
        frozen_verify.compare(diagnose(rows),json.loads((HERE/'matrix_diagnostics.json').read_text()))
        write_json(dest/'summary.json',expected)
        old_here,old_analyze,old_mb=frozen_verify.HERE,frozen_verify.analyze,mb_analyze.HERE
        frozen_verify.HERE=dest; frozen_verify.analyze=lambda save=False:analyze_at(dest);mb_analyze.HERE=dest
        try: frozen_verify.main(strict=strict)
        finally:
            frozen_verify.HERE=old_here;frozen_verify.analyze=old_analyze;mb_analyze.HERE=old_mb
        name='verification_strict.json' if strict else 'verification.json'
        result=json.loads((dest/name).read_text())
        result.update(original_records_preserved=27,additional_records=5,
                      resource_gate_status=expected['resource_gate_status'],
                      resumption_adapter='resume_evidence.py; frozen numerical verifier unchanged')
        write_json(HERE/('verification_strict.json' if strict else 'verification.local.json'),result)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--strict',action='store_true')
    args=p.parse_args()
    if args.verify: verify_all(args.strict)
    else: finalize()
