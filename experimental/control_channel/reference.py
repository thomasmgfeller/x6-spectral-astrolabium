"""Independent binary reader and model-output oracle; no compiler/firmware imports.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
from pathlib import Path


def read_compiled(data):
    if len(data) < 16 or (len(data)-8) % 8:
        raise ValueError('Invalid compiled length')
    numbers = [int.from_bytes(data[i:i+4], 'little') for i in range(0, len(data), 4)]
    duration, count = numbers[:2]
    if not 1 <= count <= 64 or len(numbers) != 2+2*count or not 10 <= duration <= 5000:
        raise ValueError('Invalid compiled header')
    points = list(zip(numbers[2::2], numbers[3::2]))
    if points[0][0] != 0 or any(code > 3276 or t > duration-10 for t, code in points):
        raise ValueError('Invalid compiled point')
    if any(b[0]-a[0] < 10 for a,b in zip(points, points[1:])):
        raise ValueError('Invalid point order')
    return duration, points


def model_oracle(data, events):
    duration, points = read_compiled(data)
    if len(events) != len(points)+3:
        raise ValueError('Unexpected output event count')
    observed = [(e['code'], e['enabled']) for e in events]
    expected = [(0,False),(0,False)] + [(code,True) for _,code in points] + [(0,False)]
    if observed != expected:
        raise ValueError('Model output differs from independently decoded plan')
    times = [e['model_ms'] for e in events]
    if any(type(t) is not int for t in times) or any(b<a for a,b in zip(times,times[1:])):
        raise ValueError('Invalid model clock')
    base = times[2]
    errors = [events[i+2]['model_ms']-base-t for i,(t,_) in enumerate(points)]
    errors.append(times[-1]-base-duration)
    if any(not 0 <= error <= 20 for error in errors):
        raise ValueError('Model event timing outside specified software allowance')
    return {'status': 'PASS', 'output_events': len(events), 'points': len(points),
            'max_model_lateness_ms': max(errors), 'measurement_class': 'SOFTWARE_MODEL_CLOCK'}


def verify(directory):
    root = Path(directory)
    result = json.loads((root/'result.json').read_bytes())
    if result['schema'] != 'acvm.channel.run/1' or result['status'] not in ('MODEL_EXECUTION_PASS','DEVICE_EXECUTION_REPORTED'):
        raise ValueError('No successful run record')
    expected = result['files']
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'result.json'}
    if set(expected) != actual or any(not p.is_file() or p.is_symlink() for p in root.iterdir()):
        raise ValueError('Run inventory mismatch/symlink/directory')
    for name, digest in expected.items():
        if Path(name).name != name or hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise ValueError('Run digest mismatch: ' + name)
    compiled = (root/'compiled.bin').read_bytes()
    if hashlib.sha256(compiled).hexdigest() != result['plan_sha256']:
        raise ValueError('Compiled plan digest mismatch')
    duration, points = read_compiled(compiled)
    plan = json.loads((root/'plan.json').read_bytes())
    if plan != {'schema':'acvm.channel.plan/1','profile':'pico-mcp4921-code-v1',
                'duration_ms':duration,'points':[{'at_ms':t,'dac_code':c} for t,c in points]}:
        raise ValueError('Source plan differs from independent decoding')
    # Inspect raw frames independently: requests/replies can be fragmented in the log.
    import binascii
    streams = {'tx': bytearray(), 'rx': bytearray()}
    for line in (root/'transport.jsonl').read_text().splitlines():
        record = json.loads(line)
        streams[record['direction']].extend(bytes.fromhex(record['hex']))
    frames = {}
    for direction, stream in streams.items():
        if not stream or len(stream) % 48:
            raise ValueError('Incomplete successful transport transcript')
        frames[direction] = []
        for offset in range(0,len(stream),48):
            frame=stream[offset:offset+48]
            if frame[:4] != b'ACV1' or binascii.crc32(frame[:44]) != int.from_bytes(frame[44:],'little'):
                raise ValueError('Transcript frame integrity failed')
            if frame[5] != (direction == 'rx'):
                raise ValueError('Transcript direction mismatch')
            frames[direction].append(frame)
    sid = result['session']
    if any(int.from_bytes(f[8:12],'little') != sid for fs in frames.values() for f in fs):
        raise ValueError('Transcript session mismatch')
    requests = {}
    for f in frames['tx']:
        seq = int.from_bytes(f[12:16], 'little')
        if f[6:8] != b'\0\0' or (seq in requests and requests[seq] != f):
            raise ValueError('Invalid/reused request identity')
        requests[seq] = f
    if sorted(requests) != list(range(len(requests))):
        raise ValueError('Request sequence gap')
    expected_commands = [(1,[0xAC010001]), (2,[len(points),duration,binascii.crc32(compiled)])]
    expected_commands += [(3,[i,t,c]) for i,(t,c) in enumerate(points)]
    expected_commands += [(4,[]),(5,[])]
    if len(requests) < len(expected_commands):
        raise ValueError('Incomplete command sequence')
    expected_commands += [(6,[])]*(len(requests)-len(expected_commands))
    for seq,(op,args) in enumerate(expected_commands):
        f=requests[seq]
        values=[int.from_bytes(f[i:i+4],'little') for i in range(16,44,4)]
        if f[4] != op or values != args+[0]*(7-len(args)):
            raise ValueError('Transmitted command differs from compiled plan')
    replies = frames['rx']
    declared = result['endpoint'] == 'HARDWARE_DECLARED'
    if any(bool(f[6]&1) != declared or int.from_bytes(f[16:20],'little') != 0 for f in replies):
        raise ValueError('Endpoint class/error mismatch in transcript')
    summaries=[]
    reply_sequences=set()
    for f in replies:
        seq=int.from_bytes(f[12:16],'little'); state=int.from_bytes(f[20:24],'little')
        if (seq not in requests or requests[seq][4] != f[4] or f[6]&~3 or f[7]
                or int.from_bytes(f[40:44],'little') != 0xAC010001 or state > 6):
            raise ValueError('Invalid response identity/profile/state')
        reply_sequences.add(seq)
        summaries.append({'op':f[4],'session':sid,'seq':seq,'error':'OK',
            'state':['IDLE','LOADING','READY','RUNNING','DONE','ABORTED','FAULT'][state],
            'commanded_dac_code':int.from_bytes(f[24:28],'little'),
            'applied_points':int.from_bytes(f[28:32],'little'),
            'elapsed_ms':int.from_bytes(f[32:36],'little'),
            'run_counter':int.from_bytes(f[36:40],'little'),'profile':0xAC010001,
            'endpoint':'HARDWARE_DECLARED' if declared else 'MODEL','replayed':bool(f[6]&2)})
    if reply_sequences != set(requests):
        raise ValueError('Missing acknowledged command')
    cursor=0
    for summary in result['responses']:
        while cursor<len(summaries) and summaries[cursor]!=summary:cursor+=1
        if cursor==len(summaries):raise ValueError('Summary differs from raw transcript')
        cursor+=1
    if not result['responses'] or result['responses'][-1] != summaries[-1]:
        raise ValueError('Missing final response summary')
    last = replies[-1]
    starts = [f for f in replies if f[4] == 5]
    if not starts:
        raise ValueError('Missing START acknowledgement')
    run_number = int.from_bytes(starts[0][36:40], 'little')
    if (int.from_bytes(last[20:24],'little') != 4 or int.from_bytes(last[24:28],'little') != 0
            or int.from_bytes(last[28:32],'little') != len(points) or run_number < 1
            or int.from_bytes(last[36:40],'little') != run_number):
        raise ValueError('Completion not established by raw response')
    if result['electrical_validation'] != 'NOT_PERFORMED' or result['optical_validation'] != 'NOT_PERFORMED':
        raise ValueError('Command receipt cannot establish physical validation')
    if declared:
        if result['status'] != 'DEVICE_EXECUTION_REPORTED':
            raise ValueError('Hardware status mislabelled')
        oracle = {'status':'NOT_APPLICABLE','reason':'No independent electrical measurement in this receipt'}
    else:
        if result['status'] != 'MODEL_EXECUTION_PASS':
            raise ValueError('Model status mislabelled')
        events=[json.loads(line) for line in (root/'model-output.jsonl').read_text().splitlines()]
        oracle=model_oracle(compiled,events)
    return {'status':'VERIFIED', 'execution_status':result['status'], 'independent_oracle':oracle,
            'electrical_validation':'NOT_PERFORMED', 'optical_validation':'NOT_PERFORMED',
            'authenticity':'NOT_ASSESSED', 'scope':'Recorded software execution and integrity; no device re-execution'}
