#!/usr/bin/env python3
"""Build the frozen RP2040 C1 candidate. Never opens or flashes a device."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT/'docs/acvm/c1-e01-target-build/build-lock.json'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def capture(args, cwd=None):
    p = subprocess.run(list(map(str,args)), cwd=cwd, capture_output=True, text=True, timeout=30)
    require(p.returncode == 0, 'Command failed: '+str(args[0])+' '+p.stderr[-1000:])
    return p.stdout.strip()


def uf2_check(uf2, binary):
    data, raw = Path(uf2).read_bytes(), Path(binary).read_bytes()
    require(len(data) > 0 and len(data) % 512 == 0, 'UF2 length')
    count = len(data)//512
    payload = bytearray()
    for i in range(count):
        b = data[i*512:(i+1)*512]
        start, magic, flags, address, size, index, total, family = struct.unpack('<8I',b[:32])
        require((start, magic, flags, size, index, total, family) ==
                (0x0A324655,0x9E5D5157,0x2000,256,i,count,0xE48BFF56), 'UF2 header/family/order')
        require(struct.unpack('<I',b[-4:])[0] == 0x0AB16F30, 'UF2 end magic')
        require(address == 0x10000000 + 256*i and address+size <= 0x10200000, 'RP2040 flash address')
        payload.extend(b[32:32+size])
    require(bytes(payload[:len(raw)]) == raw and len(raw) <= len(payload) < len(raw)+256,
            'UF2 does not encode the complete binary')
    require(not any(payload[len(raw):]), 'Nonzero UF2 padding')
    return {'blocks':count,'family':'RP2040','start_address':'0x10000000','binary_bytes':len(raw)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk',type=Path,required=True)
    parser.add_argument('--picotool-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    created = False
    try:
        require(not out.exists(), 'Output must be new; retain earlier attempts')
        lock=json.loads(LOCK.read_text()); sdk=args.sdk.resolve(); tool_dir=args.picotool_dir.resolve()
        require(capture(['git','rev-parse','HEAD'],sdk) == lock['pico_sdk_commit'], 'SDK commit differs')
        require(not capture(['git','status','--porcelain','--untracked-files=all'],sdk), 'SDK is dirty')
        require(capture(['git','rev-parse','HEAD'],sdk/'lib/tinyusb') == lock['tinyusb_commit'], 'TinyUSB commit differs')
        require(not capture(['git','status','--porcelain','--untracked-files=all'],sdk/'lib/tinyusb'), 'TinyUSB is dirty')
        for name,digest in lock['firmware_sources'].items():
            require(sha(ROOT/name) == digest, 'Frozen firmware changed: '+name)
        executables={name:shutil.which(name) for name in ['cmake','ninja','arm-none-eabi-gcc','arm-none-eabi-g++','arm-none-eabi-readelf','arm-none-eabi-size']}
        require(all(executables.values()), 'CMake, Ninja and GNU Arm tools must be on PATH')
        picotool=tool_dir/'picotool'; require(picotool.is_file(), 'picotool executable missing')
        versions={'gcc':capture([executables['arm-none-eabi-gcc'],'-dumpfullversion']),
                  'cmake':capture([executables['cmake'],'--version']).splitlines()[0].split()[-1],
                  'ninja':capture([executables['ninja'],'--version']),
                  'picotool':capture([picotool,'version']).split()[1].lstrip('v')}
        require(versions == lock['tools'], 'Tool versions differ from build lock: '+str(versions))
        out.mkdir(parents=True)
        created = True
        env=dict(os.environ, PICO_SDK_PATH=str(sdk), SOURCE_DATE_EPOCH=str(lock['source_date_epoch']),
                 TZ='UTC', LC_ALL='C')
        build=out/'build'
        commands=[['cmake','-S',str(ROOT/'experimental/control_channel/firmware'),'-B',str(build),
                   '-G','Ninja','-DPICO_BOARD=pico','-DPICO_PLATFORM=rp2040','-DCMAKE_BUILD_TYPE=Release',
                   '-Dpicotool_DIR='+str(tool_dir)],
                  ['cmake','--build',str(build),'--parallel','2']]
        for label,command in zip(['configure','build'],commands):
            with (out/(label+'.log')).open('xb') as log:
                p=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300)
            require(p.returncode == 0, label+' failed; log retained')
        for suffix in ['uf2','bin','elf']:
            shutil.copyfile(build/('acvm_channel.'+suffix),out/('acvm_channel.'+suffix))
        shape=uf2_check(out/'acvm_channel.uf2',out/'acvm_channel.bin')
        require(sha(out/'acvm_channel.uf2') == lock['expected_uf2_sha256'], 'UF2 differs from frozen candidate')
        require(sha(out/'acvm_channel.bin') == lock['expected_bin_sha256'], 'Binary differs from frozen candidate')
        info=capture([picotool,'info','-a',out/'acvm_channel.uf2'])
        elf=capture([executables['arm-none-eabi-readelf'],'-h',out/'acvm_channel.elf'])
        require('Machine:                           ARM' in elf, 'ELF is not ARM')
        require("family ID 'rp2040'" in info and 'USB stdin / stdout' in info, 'Wrong target/USB feature')
        (out/'picotool-info.txt').write_text(info+'\n'); (out/'elf-header.txt').write_text(elf+'\n')
        report={'schema':'acvm.c1.target-build/1','status':'TARGET_BUILD_PASS',
                'board':'pico','platform':'rp2040','pico_sdk_commit':lock['pico_sdk_commit'],
                'tinyusb_commit':lock['tinyusb_commit'],'tool_versions':versions,
                'tool_executables_sha256':{k:sha(v) for k,v in executables.items()},
                'picotool_sha256':sha(picotool),'build_lock_sha256':sha(LOCK),
                'builder_sha256':sha(Path(__file__)), 'firmware_sources':lock['firmware_sources'],
                'firmware_source_commit':lock['firmware_source_commit'],
                'source_date_epoch':lock['source_date_epoch'],'uf2':shape,
                'outputs':{name:sha(out/name) for name in ['acvm_channel.uf2','acvm_channel.bin','acvm_channel.elf','picotool-info.txt','elf-header.txt','configure.log','build.log']},
                'environment':{'python':platform.python_version(),'platform':platform.platform()},
                'device_opened':False,'flashed':False,'electrical_validation':'NOT_PERFORMED',
                'scope':'CROSS_COMPILED_CANDIDATE_ONLY; NO_PHYSICAL_OUTPUT_MEASURED'}
        (out/'build-report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print(json.dumps(report,indent=2,sort_keys=True))
        return 0
    except (ValueError,OSError,subprocess.SubprocessError,KeyError) as exc:
        if created: (out/'failure.json').write_text(json.dumps({'status':'FAILED','error':str(exc),'electrical_validation':'NOT_PERFORMED'},indent=2)+'\n')
        print('FAIL: '+str(exc),file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
