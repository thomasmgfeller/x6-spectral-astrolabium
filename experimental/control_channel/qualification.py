"""Reproducible software qualification; all physical gates remain NOT_PERFORMED.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from . import channel, cli, reference


def qualify(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    report={'schema':'acvm.channel.qualification/1','status':'FAILED','checks':{},
            'pico_firmware_build':'NOT_PERFORMED', 'electrical_validation':'NOT_PERFORMED',
            'optical_validation':'NOT_PERFORMED','acvm_V01_V08_full_suite':'NOT_CLAIMED'}
    try:
        with tempfile.TemporaryDirectory(prefix='acvm-tests-') as temp:
            binary=cli.build_native(temp,'core_tests.cpp')
            run=subprocess.run([str(binary)],capture_output=True,text=True,timeout=10)
            (output/'firmware-core-tests.log').write_text(run.stdout+run.stderr)
            if run.returncode:raise RuntimeError(run.stderr)
            report['checks']['firmware_core']=json.loads(run.stdout)
        host=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests/control-channel','-v'],cwd=cli.ROOT,capture_output=True,text=True,timeout=30)
        (output/'host-tests.log').write_text(host.stdout+host.stderr)
        if host.returncode:raise RuntimeError('Host tests failed')
        report['checks']['host_tests']={'status':'PASS','tests':int(re.search(r'Ran (\d+) tests',host.stderr).group(1))}
        result=cli.demo(cli.EXAMPLE,output/'model-run')
        if result['status']!='MODEL_EXECUTION_PASS':raise RuntimeError('End-to-end model run failed')
        report['checks']['end_to_end']=reference.verify(output/'model-run')
        archive=cli.export(output/'model-run',output/'model-run.zip')
        with tempfile.TemporaryDirectory(prefix='acvm-reimport-') as temp:
            # This is our just-generated archive, never an untrusted extraction API.
            import zipfile
            with zipfile.ZipFile(output/'model-run.zip') as z:z.extractall(temp)
            report['checks']['export_reimport']=reference.verify(temp)
            original=Path(temp)/'compiled.bin';data=bytearray(original.read_bytes());data[-1]^=1;original.write_bytes(data)
            try:reference.verify(temp)
            except ValueError:report['checks']['tampered_export_rejected']='PASS'
            else:raise RuntimeError('Tampered export accepted')
        report['archive_sha256']=archive['sha256']
        mutations={}
        for mode in ('summary_value','hardware_relabelling','plan_rehashed','model_output_rehashed'):
            with tempfile.TemporaryDirectory(prefix='acvm-mutation-') as temp:
                target=Path(temp)/'run';shutil.copytree(output/'model-run',target)
                record=json.loads((target/'result.json').read_bytes())
                if mode=='summary_value':record['responses'][-1]['commanded_dac_code']=123
                elif mode=='hardware_relabelling':
                    record['endpoint']='HARDWARE_DECLARED';record['status']='DEVICE_EXECUTION_REPORTED'
                elif mode=='plan_rehashed':
                    plan=channel.read_json(target/'plan.json');plan['points'][1]['dac_code']+=1
                    (target/'plan.json').write_bytes(channel.json_bytes(plan))
                    data=channel.compile_plan(plan);(target/'compiled.bin').write_bytes(data)
                    record['plan_sha256']=hashlib.sha256(data).hexdigest()
                    for name in ('plan.json','compiled.bin'):record['files'][name]=hashlib.sha256((target/name).read_bytes()).hexdigest()
                else:
                    data=(target/'model-output.jsonl').read_text().splitlines();data.pop(3)
                    (target/'model-output.jsonl').write_text('\n'.join(data)+'\n')
                    record['files']['model-output.jsonl']=hashlib.sha256((target/'model-output.jsonl').read_bytes()).hexdigest()
                (target/'result.json').write_bytes(channel.json_bytes(record))
                try:reference.verify(target)
                except ValueError:mutations[mode]='REJECTED'
                else:raise RuntimeError('Mutation accepted: '+mode)
        report['checks']['receipt_mutations']=mutations
        report['sources']=result['sources']
        report['environment']=result['environment']
        report['status']='SOFTWARE_PASS_HARDWARE_OPEN'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    (output/'qualification.json').write_bytes(channel.json_bytes(report))
    return report
