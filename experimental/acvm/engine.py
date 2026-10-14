"""D01 finite complex sample image and virtual-clock sequencer (not FPGA firmware).
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import re
import struct
from .signals import finite

HEADER = struct.Struct('<8sIIQ')
ROW = struct.Struct('<Qdd')


def compile_plan(plan):
    fields = {'schema', 'run_id', 'unit', 'tick_ns', 'duration_ticks', 'samples'}
    if not isinstance(plan, dict) or set(plan) != fields:
        raise ValueError('Unexpected D01 plan fields')
    if plan['schema'] != 'acvm.d01.plan/1' or plan['unit'] != 'normalized_IQ':
        raise ValueError('Unsupported schema/units')
    if not isinstance(plan['run_id'], str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', plan['run_id']):
        raise ValueError('Invalid run ID')
    duration, tick = plan['duration_ticks'], plan['tick_ns']
    if type(tick) is not int or not 1 <= tick <= 10**9:
        raise ValueError('Invalid integer timebase')
    if type(duration) is not int or not 1 <= duration <= 2**53-1 or duration*tick >= 2**64:
        raise ValueError('Counter overflow/JSON precision')
    rows = plan['samples']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 4096:
        raise ValueError('Buffer capacity')
    image = HEADER.pack(b'ACVMD01\0', len(rows), tick, duration)
    previous = -1
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'tick', 'i', 'q'}:
            raise ValueError('Invalid sample fields')
        at = row['tick']
        if type(at) is not int or not previous < at < duration or (previous == -1 and at != 0):
            raise ValueError('Invalid sample order/start/end')
        image += ROW.pack(at, finite(row['i'], 'I', -1, 1), finite(row['q'], 'Q', -1, 1))
        previous = at
    return image


class Sequencer:
    """Reference state machine; ticks supplied by the caller, no real-time guarantee."""
    def __init__(self, run_id, image, decoded):
        from .archive import read_image
        if read_image(image) != decoded:
            raise ValueError('Execution rows do not match image')
        self.run_id = run_id
        self.digest = hashlib.sha256(image).hexdigest()
        self.rows, self.duration = decoded['rows'], decoded['duration_ticks']
        self.state, self.runs, self.index = 'READY', 0, 0
        self.output, self.events, self.last = (0., 0.), [], None
        self.start_identity = None

    def start(self, run_id, digest, now):
        if type(now) is not int or now < 0 or now+self.duration >= 2**64:
            raise ValueError('Clock overflow')
        identity = (run_id, digest)
        if identity != (self.run_id, self.digest):
            self.fault('IDENTITY'); raise ValueError('Run/image mismatch')
        if self.start_identity == identity:
            return 'DUPLICATE_IGNORED'
        if self.state != 'READY':
            raise ValueError('Start requires READY')
        self.start_identity = identity
        self.epoch = now; self.last = now; self.runs += 1; self.state = 'RUNNING'
        self.advance(now)
        return self.state

    def fault(self, reason):
        self.output = (0., 0.); self.state = 'FAULT'; self.reason = reason

    def advance(self, now, connected=True, clock_valid=True):
        if self.state != 'RUNNING':
            return
        if type(now) is not int or now < self.last or not clock_valid or not connected:
            self.fault('CLOCK_OR_CONNECTION'); return
        self.last = now
        at = now-self.epoch
        # Late samples are rejected rather than silently replayed as a burst.
        if self.index < len(self.rows) and at > self.rows[self.index][0]:
            self.fault('LATE'); return
        if at >= self.duration:
            self.output = (0., 0.); self.state = 'DONE'; return
        if self.index < len(self.rows) and at == self.rows[self.index][0]:
            tick, i, q = self.rows[self.index]
            self.output = (i, q); self.events.append((tick, i, q)); self.index += 1
