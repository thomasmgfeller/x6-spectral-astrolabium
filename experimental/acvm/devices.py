"""Explicit ELL14 serial and legacy PM100D VISA adapters. Hardware unqualified.
No discovery, homing, reconnect, persistent settings, or automatic motor retries.
SPDX-License-Identifier: Apache-2.0
"""
import os
import json
import csv
import re
import select
import termios
import time
from experimental.control_channel.channel import Transport
from .signals import finite


class EllSerial(Transport):
    def __init__(self, path, log=None):
        super().__init__(path, log)
        settings = termios.tcgetattr(self.fd)
        settings[4] = settings[5] = termios.B9600
        settings[2] &= ~(termios.PARENB | termios.CSTOPB | termios.CRTSCTS)
        termios.tcsetattr(self.fd, termios.TCSANOW, settings)

    def read_line(self, timeout):
        deadline = time.monotonic()+timeout
        while b'\r\n' not in self.buffer:
            left = deadline-time.monotonic()
            if left <= 0 or not select.select([self.fd], [], [], left)[0]:
                raise TimeoutError('ELL response deadline')
            data = os.read(self.fd, 256)
            if not data:
                raise OSError('ELL disconnected')
            self.record('rx', data); self.buffer.extend(data)
            if len(self.buffer) > 256:
                raise ValueError('ELL oversized response')
        line, _, remaining = self.buffer.partition(b'\r\n')
        self.buffer = bytearray(remaining)
        return line.decode('ascii', errors='strict')


class Ell14:
    def __init__(self, transport, profile):
        required = {'address', 'serial', 'pulses_per_degree', 'zero_deg', 'min_deg',
                    'max_deg', 'tolerance_deg', 'timeout_s', 'scale_evidence'}
        if set(profile) != required or not re.fullmatch('[0-9A-F]', profile['address']):
            raise ValueError('ELL profile/address')
        if not re.fullmatch('[0-9]{8}', profile['serial']) or not profile['scale_evidence']:
            raise ValueError('Serial and independently checked encoder scale required')
        finite(profile['pulses_per_degree'], 'encoder scale', 1, 10**6)
        finite(profile['zero_deg'], 'motor zero', -180, 180)
        finite(profile['min_deg'], 'minimum angle', 0, 180)
        finite(profile['max_deg'], 'maximum angle', profile['min_deg']+1e-6, 180)
        finite(profile['tolerance_deg'], 'position tolerance', .001, 1)
        finite(profile['timeout_s'], 'timeout', .1, 30)
        self.io, self.p, self.identified, self.failed = transport, profile, False, False

    def _read(self, deadline):
        left = deadline-time.monotonic()
        if left <= 0:
            raise TimeoutError('ELL absolute deadline')
        line = self.io.read_line(left)
        if time.monotonic() > deadline:
            raise TimeoutError('ELL response arrived after deadline')
        if not line.startswith(self.p['address']):
            raise ValueError('ELL address mismatch')
        return line[1:]

    def identify(self):
        self.io.write((self.p['address']+'in').encode())
        reply = self._read(time.monotonic()+self.p['timeout_s'])
        if not re.fullmatch(r'IN[0-9A-Fa-f]{30}', reply):
            raise ValueError('ELL information response')
        if int(reply[2:4], 16) != 14 or reply[4:12] != self.p['serial']:
            raise ValueError('ELL model/serial mismatch')
        self.identified = True
        return {'raw_information': reply, 'encoder_scale_source': self.p['scale_evidence']}

    def move(self, motor_deg):
        # The supplied angle is already a MOTOR angle; no hidden HWP factor of two.
        finite(motor_deg, 'motor angle', self.p['min_deg'], self.p['max_deg'])
        if not self.identified or self.failed:
            raise RuntimeError('Identify first; failures require manual recovery')
        pulses = round((motor_deg-self.p['zero_deg'])*self.p['pulses_per_degree'])
        if not -(2**31) <= pulses < 2**31:
            raise ValueError('ELL pulse overflow')
        deadline = time.monotonic()+self.p['timeout_s']
        try:
            self.io.write(f"{self.p['address']}ma{pulses & 0xffffffff:08X}".encode())
            while True:
                reply = self._read(deadline)
                if re.fullmatch(r'PO[0-9A-Fa-f]{8}', reply):
                    actual = int(reply[2:], 16)
                    if actual >= 2**31:
                        actual -= 2**32
                    degrees = self.p['zero_deg']+actual/self.p['pulses_per_degree']
                    if abs(degrees-motor_deg) > self.p['tolerance_deg']:
                        raise ValueError('ELL final position mismatch')
                    return {'requested_deg': motor_deg, 'reported_deg': degrees,
                            'physical_position_verified': False}
                if reply not in ('GS00', 'GS09'):
                    raise RuntimeError('ELL unexpected status: '+reply)
                # GS is not completion. Poll status while busy, then position.
                if time.monotonic() >= deadline:
                    raise TimeoutError('ELL move deadline')
                time.sleep(min(.05, max(0, deadline-time.monotonic())))
                self.io.write((self.p['address']+('gs' if reply == 'GS09' else 'gp')).encode())
        except BaseException:
            self.failed = True
            try:
                self.io.write((self.p['address']+'st').encode())
            except Exception:
                pass
            raise


class PowerMeter:
    """SCPI subset for legacy PM100D; injected VISA-like I/O also allows model tests."""
    def __init__(self, io, serial, sensor_serial, wavelength_nm, max_power_w):
        self.io = io
        finite(wavelength_nm, 'wavelength', 800, 820)
        self.maximum = finite(max_power_w, 'maximum power', 1e-12, .05)
        fields = next(csv.reader([self.io.query('*IDN?').strip()]))
        if len(fields) != 4 or fields[:3] != ['THORLABS', 'PM100D', serial]:
            raise ValueError('PM100D identity mismatch')
        sensor = next(csv.reader([self.io.query('SYST:SENS:IDN?').strip()]))
        if len(sensor) < 2 or sensor[1] != sensor_serial:
            raise ValueError('Power sensor identity mismatch')
        self.identity, self.sensor = fields, sensor
        self.io.write('SENS:POW:UNIT W')
        self.io.write(f'SENS:CORR:WAV {wavelength_nm:.6f}')
        self.io.write('SENS:AVER:COUN 1')
        self.io.write('SENS:POW:RANG:AUTO 1')
        self.error()
        if abs(float(self.io.query('SENS:CORR:WAV?'))-wavelength_nm) > .01:
            raise ValueError('Wavelength readback mismatch')

    def error(self):
        if int(self.io.query('SYST:ERR?').split(',')[0]) != 0:
            raise RuntimeError('Power meter error queue nonzero')

    def read(self):
        start = time.monotonic()
        if self.io.query('SENS:POW:UNIT?').strip() != 'W':
            raise ValueError('Power meter units changed')
        value = finite(float(self.io.query('MEAS:POW?')), 'measured power', 0, self.maximum)
        if self.io.query('SENS:POW:UNIT?').strip() != 'W':
            raise ValueError('Power meter units changed during measurement')
        self.error()
        end = time.monotonic()
        return {'power_w': value, 'request_s': start, 'received_s': end,
                'timestamp_kind': 'HOST_REQUEST_INTERVAL_NOT_DEVICE_SAMPLE_TIME'}


class LoggedVisa:
    def __init__(self, io, log):
        self.io, self.log = io, log

    def record(self, direction, message):
        self.log.write(json.dumps({'monotonic_ns': time.monotonic_ns(),
                                  'direction': direction, 'message': message})+'\n')
        self.log.flush(); os.fsync(self.log.fileno())

    def write(self, message):
        self.record('tx', message)
        return self.io.write(message)

    def query(self, message):
        self.record('tx', message)
        result = self.io.query(message)
        self.record('rx', result)
        return result
