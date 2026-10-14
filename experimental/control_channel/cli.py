"""x6.py control entry point. SPDX-License-Identifier: Apache-2.0."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import pty
import shutil
import subprocess
import sys
import tempfile
import zipfile
from . import channel, reference

ROOT = channel.ROOT
HERE = Path(__file__).resolve().parent
EXAMPLE = HERE/'examples/step-plan.json'


def build_native(directory, source='native.cpp'):
    compiler = shutil.which('g++')
    if not compiler:
        raise RuntimeError('Install g++ with C++17 support')
    binary = Path(directory)/Path(source).stem
    cmd = [compiler,'-std=c++17','-O2','-Wall','-Wextra','-Werror','-pedantic',
           str(HERE/'firmware'/source),'-o',str(binary)]
    completed = subprocess.run(cmd,capture_output=True,text=True,timeout=60)
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return binary


def demo(plan, output):
    with tempfile.TemporaryDirectory(prefix='acvm-model-') as temp:
        binary = build_native(temp)
        master, slave = pty.openpty()
        # Hold slave open until host has configured it; no boot bytes on this channel.
        with (Path(temp)/'model.jsonl').open('w') as events:
            proc = subprocess.Popen([str(binary)],stdin=master,stdout=master,stderr=events,close_fds=True)
            os.close(master)
            try:
                result = channel.run(plan,os.ttyname(slave),output,'MODEL')
            finally:
                proc.terminate()
                proc.wait(timeout=3)
                os.close(slave)
        target = Path(output)
        shutil.copyfile(Path(temp)/'model.jsonl',target/'model-output.jsonl')
        result['native_binary_sha256'] = hashlib.sha256(binary.read_bytes()).hexdigest()
        sources = [p for p in HERE.rglob('*') if p.is_file() and p.suffix in ('.py','.cpp','.hpp','.txt','.json')]
        sources += list((ROOT/'tests/control-channel').glob('*.py'))
        sources += [p for p in (ROOT/'x6.py',ROOT/'tools/workflow/cli.py') if p.is_file()]
        result['sources'] = {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}
        result['environment'] = {'python':platform.python_version(), 'platform':platform.platform(),
                                 'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0]}
        result['files']['model-output.jsonl'] = hashlib.sha256((target/'model-output.jsonl').read_bytes()).hexdigest()
        (target/'result.json').write_bytes(channel.json_bytes(result))
        if result['status'] == 'MODEL_EXECUTION_PASS':
            reference.verify(target)
        return result


def export(directory, output):
    verified = reference.verify(directory)
    output = Path(output)
    if output.resolve().is_relative_to(Path(directory).resolve()):
        raise ValueError('Export must be outside the run directory')
    output.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive creation; existing reports cannot be silently overwritten.
    try:
        with output.open('xb') as file:
            with zipfile.ZipFile(file,'w',compression=zipfile.ZIP_DEFLATED) as archive:
                for p in sorted(Path(directory).iterdir()):
                    archive.writestr(p.name,p.read_bytes())
    except FileExistsError:
        raise
    except BaseException:
        output.unlink(missing_ok=True)
        raise
    return {'status':'EXPORTED','output':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'verification':verified}


def main(argv=None):
    parser=argparse.ArgumentParser(description='ACVM bounded DAC channel; model proof and explicit serial execution')
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('doctor')
    p=commands.add_parser('compile'); p.add_argument('plan',type=Path); p.add_argument('--output',type=Path,required=True)
    p=commands.add_parser('demo'); p.add_argument('--plan',type=Path,default=EXAMPLE); p.add_argument('--output',type=Path,required=True)
    p=commands.add_parser('run'); p.add_argument('--plan',type=Path,required=True); p.add_argument('--port',required=True); p.add_argument('--output',type=Path,required=True)
    p=commands.add_parser('verify'); p.add_argument('directory',type=Path)
    p=commands.add_parser('export'); p.add_argument('directory',type=Path); p.add_argument('--output',type=Path,required=True)
    p=commands.add_parser('qualify'); p.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='doctor':
            result={'status':'READY' if os.name=='posix' and shutil.which('g++') else 'NOT_READY',
                    'scope':'Host/model prerequisites only','python':platform.python_version(),
                    'g++':shutil.which('g++'),'pico_sdk':bool(os.getenv('PICO_SDK_PATH')),
                    'physical_hardware':'NOT_PROBED','electrical_validation':'NOT_PERFORMED'}
        elif args.command=='compile':
            data=channel.compile_plan(channel.read_json(args.plan))
            reference.read_compiled(data)
            args.output.parent.mkdir(parents=True,exist_ok=True)
            with args.output.open('xb') as f: f.write(data)
            result={'status':'COMPILED','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        elif args.command=='demo': result=demo(args.plan,args.output)
        elif args.command=='run': result=channel.run(args.plan,args.port,args.output,'HARDWARE_DECLARED')
        elif args.command=='verify': result=reference.verify(args.directory)
        elif args.command=='export': result=export(args.directory,args.output)
        else:
            from .qualification import qualify
            result=qualify(args.output)
        print(json.dumps(result,indent=2,allow_nan=False))
        return 1 if result['status'] in ('FAILED','NOT_READY') else 0
    except (ValueError,OSError,RuntimeError,subprocess.SubprocessError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'FAILED','error':f'{type(exc).__name__}: {exc}'}),file=sys.stderr)
        return 1
