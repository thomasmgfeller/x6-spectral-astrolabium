"""Linux drivers for the X6 acquisition console. All device paths originate in the bench profile."""
import contextlib
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import select
import struct
import sys
import termios
import time
import tty

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "vendor"))
from frame_codec import FRAME_BYTES, decode_frame
from analyze import validate

CHANNELS = [1, 2, 3, 4]
ANGLES = {"00": (0, 11.25), "01": (0, -11.25), "10": (22.5, 11.25), "11": (22.5, -11.25)}
SCHEDULE_SHA = "3ceb36b09f84cb82d346a5edf214857601a69402e96be890afa7ca83debccee7"

def utc():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

def save(path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

@contextlib.contextmanager
def port(path, baud, *, write=False, flow=False):
    fd = os.open(path, (os.O_RDWR if write else os.O_RDONLY) | os.O_NOCTTY | os.O_NONBLOCK)
    old = None
    try:
        old = termios.tcgetattr(fd)
        tty.setraw(fd, when=termios.TCSANOW)
        a = termios.tcgetattr(fd)
        a[4] = a[5] = getattr(termios, "B" + str(baud))
        a[2] |= termios.CLOCAL | termios.CREAD
        a[2] &= ~(termios.CSTOPB | termios.CRTSCTS)
        if flow:
            a[2] |= termios.CRTSCTS
        termios.tcsetattr(fd, termios.TCSANOW, a)
        yield fd
    finally:
        try:
            if old:
                termios.tcsetattr(fd, termios.TCSANOW, old)
        finally:
            os.close(fd)

def receive(fd, length, deadline, check=lambda: None):
    data = bytearray()
    while len(data) < length:
        check()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Zeitlimit für Geräteantwort")
        if select.select([fd], [], [], min(remaining, 0.15))[0]:
            chunk = os.read(fd, length - len(data))
            if not chunk:
                raise OSError("Serielle Verbindung beendet")
            data.extend(chunk)
    return bytes(data)

def exchange(fd, address, command, reply, size, check):
    request = (address + command).encode("ascii")
    if os.write(fd, request) != len(request):
        raise OSError("Unvollständiger Gerätebefehl")
    deadline = time.monotonic() + 30
    header = receive(fd, 3, deadline, check).decode("ascii")
    if header != address + reply:
        raise ValueError("Unerwartete ELL14-Antwort " + repr(header))
    rest = receive(fd, size + 2, deadline, check)
    if rest[-2:] != b"\r\n":
        raise ValueError("ELL14-Telegrammabschluss fehlt")
    return rest[:-2].decode("ascii")

def set_axes(axes, setting, check, report):
    results = []
    for axis, angle in zip(axes, ANGLES[setting], strict=True):
        check()
        with port(axis["port"], 9600, write=True) as fd:
            addr = axis["address"]
            info = exchange(fd, addr, "in", "IN", 30, check)
            if info[:2].upper() != "0E" or info[2:10] != axis["serial"] or int(info[18:22],16) != 360:
                raise ValueError("ELL14-Identität oder Stellbereich stimmt nicht")
            pulses = int(info[22:30], 16)
            if not 360 <= pulses < 2**31:
                raise ValueError("Ungültige ELL14-Skalierung")
            target = (axis["zero_deg"] + axis["direction"] * angle) % 360
            steps = round(target / 360 * pulses) % pulses
            check()
            exchange(fd, addr, f"ma{steps:08X}", "PO", 8, check)
            pos = int(exchange(fd, addr, "gp", "PO", 8, check),16)
            if pos >= 2**31:
                pos -= 2**32
            measured = (360 * pos / pulses) % 360
            if abs((measured-target+180) % 360-180) > axis["tolerance_deg"]:
                raise ValueError("ELL14-Positionsrückmeldung außerhalb der Toleranz")
            results.append(dict(serial=axis["serial"], target_deg=target, readback_deg=measured, utc=utc()))
            report(hwp_readback=results.copy())
    return results

def shutter(profile, *, deactivate=False):
    """KSC101 drive output only. No method to energise the solenoid."""
    with port(profile["port"], 115200, write=True, flow=True) as fd:
        deadline = time.monotonic()+2
        os.write(fd, bytes.fromhex("05 00 00 00 50 01"))
        header = receive(fd, 6, deadline)
        msg, size, dst, src = struct.unpack("<HHBB", header)
        if msg != 6 or not 12 <= size <= 256 or (dst,src)!=(0x81,0x50):
            raise ValueError("Unerwartete K-Cube-Identifikation")
        info = receive(fd,size,deadline)
        if str(int.from_bytes(info[:4],"little")) != profile["serial"] or info[4:12].rstrip(b"\x00 ") != b"KSC101":
            raise ValueError("KSC101-Identität stimmt nicht")
        if deactivate:
            if os.write(fd, bytes.fromhex("CB 04 01 02 50 01"))!=6:
                raise OSError("KSC101-Aus-Befehl unvollständig übertragen")
        os.write(fd, bytes.fromhex("CC 04 01 00 50 01"))
        msg,chan,state,dst,src = struct.unpack("<HBBBB",receive(fd,6,deadline))
        if (msg,chan,dst,src)!=(0x04CD,1,1,0x50) or state not in (1,2):
            raise ValueError("Ungültige KSC101-Statusantwort")
        if deactivate and state!=2:
            raise ValueError("KSC101 bestätigt den ausgeschalteten Ausgang nicht")
        return dict(solenoid="ON" if state==1 else "OFF", blade="UNKNOWN", interlock="UNKNOWN", utc=utc())

def snapshots(profile, config, folder, check, report):
    synthetic = profile["source"] == "example"
    path = BASE/"examples/synthetic_chsh_capture.bin" if synthetic else profile["port"]
    context = path.open("rb") if synthetic else port(path, profile["baud"])
    target = config["frames"]
    deadline = time.monotonic()+config["timeout_s"]
    count = total = 0
    pending = bytearray()
    with (folder/"capture.bin").open("xb", buffering=0) as out, context as source:
        report(phase="WAITING", source_open=True)
        while count < target:
            check()
            if time.monotonic() >= deadline:
                raise TimeoutError("Erfassungsfrist überschritten")
            remaining = target*FRAME_BYTES-total
            if synthetic:
                chunk = source.read(min(FRAME_BYTES,remaining))
            elif select.select([source], [], [], 0.1)[0]:
                chunk = os.read(source,min(4096,remaining))
            else:
                continue
            if not chunk:
                raise ValueError("Quelle beendet, bevor alle Frames eingetroffen sind")
            if out.write(chunk) != len(chunk):
                raise OSError("Unvollständiger Schreibvorgang")
            total += len(chunk)
            pending.extend(chunk)
            report(bytes_received=total)
            while len(pending) >= FRAME_BYTES:
                rec = decode_frame(bytes(pending[:FRAME_BYTES]), origin="synthetic" if synthetic else "hardware",
                                   expected_sequence=int(config["first_sequence"])+count)
                report(flags=rec["flags"], last_sequence=rec["transport"]["sequence"])
                _, _, _, counters = validate(rec)
                timing=rec["configuration"]
                duration_ps=int(timing["stop_ps"])-int(timing["start_ps"])
                rates=[v*1e12/duration_ps for v in counters[18:22]]
                report(channel_hz=rates)
                del pending[:FRAME_BYTES]
                count += 1
                report(phase="RECEIVING", frames=count, last_data=utc(), setting=rec["setting_index"])
        os.fsync(out.fileno())

def segment_plan(mode, seconds):
    if mode == "schedule":
        path = BASE/"examples/schedule.csv"
        if digest(path) != SCHEDULE_SHA:
            raise ValueError("Messplan-Prüfsumme falsch")
        with path.open(newline="") as f:
            return [(r["setting"],int(r["duration_s"]),int(r["settle_s"])) for r in csv.DictReader(f)]
    return [(None, seconds, 0)]

def rate_values(meter):
    values=[float(v) for v in meter.getData()]
    if len(values)!=4:
        raise ValueError("Time Tagger liefert keine vier Kanalraten")
    return [v if math.isfinite(v) and v>=0 else None for v in values]

def capture_tags(profile, config, folder, check, report, sdk=None):
    if sdk is None:
        import TimeTagger as sdk
    tagger = sdk.createTimeTagger(serial=profile["serial"])
    try:
        model = str(tagger.getModel())
        if str(tagger.getSerial()) != profile["serial"] or "ultra" not in model.lower():
            raise ValueError("Time-Tagger-Modell oder Seriennummer stimmt nicht")
        for ch, level in zip(CHANNELS,profile["trigger_v"],strict=True):
            if tagger.getTestSignal(ch) or tagger.getEventDivider(ch)!=1:
                raise ValueError("Testsignal oder Ereignisteiler aktiv")
            tagger.setTriggerLevel(ch,level)
            if abs(tagger.getTriggerLevel(ch)-level)>0.02:
                raise ValueError("Eingangsschwelle nicht bestätigt")
        save(folder/"tagger.json", dict(model=model, serial=profile["serial"], sdk_configuration=tagger.getConfiguration(),
                                       channels=dict(zip(CHANNELS,["A+","A−","B+","B−"]))))
        report(source_open=True, phase="DEVICE_READY")
        if tagger.getOverflows():
            raise ValueError("Time Tagger meldet Überlauf vor Segmentbeginn")
        total = 0
        plan = segment_plan(config["mode"], config["seconds"])
        for i, (setting,duration,settle) in enumerate(plan,1):
            check()
            positions = []
            report(phase="POSITIONING" if setting else "DEVICE_READY", segment=i, segments=len(plan), setting=setting)
            if setting is not None:
                positions=set_axes(profile["axes"],setting,check,report)
                end=time.monotonic()+settle
                while time.monotonic()<end:
                    check()
                    time.sleep(0.05)
            check()
            prefix=f"segment-{i:03}"
            meta=dict(segment=i, setting=setting, requested_seconds=duration, axes=positions, started_utc=utc(), complete=False)
            save(folder/(prefix+".json"), meta)
            group=sdk.SynchronizedMeasurements(tagger)
            writer=meter=None
            try:
                writer=sdk.FileWriter(group.getTagger(),str(folder/(prefix+".ttbin")),CHANNELS)
                meter=sdk.Countrate(group.getTagger(),CHANNELS)
                group.startFor(duration*10**12)
                report(phase="ACQUIRING")
                deadline=time.monotonic()+duration+10
                while group.isRunning():
                    check()
                    if time.monotonic()>deadline:
                        raise TimeoutError("Time Tagger hat das Segment nicht beendet")
                    if tagger.getOverflows():
                        report(overflows=True)
                        raise ValueError("Time Tagger meldet Überlauf")
                    report(events=str(total+int(writer.getTotalEvents())),channel_hz=rate_values(meter))
                    time.sleep(0.12)
                n=int(writer.getTotalEvents())
                rates=rate_values(meter)
                channel_counts=[int(v) for v in meter.getCountsTotal()]
                if len(channel_counts)!=4 or any(v<0 for v in channel_counts) or sum(channel_counts)!=n:
                    raise ValueError("Rohdatenzähler und vier Kanalzähler widersprechen sich")
                if tagger.getOverflows():
                    report(overflows=True)
                    raise ValueError("Time Tagger meldet Überlauf")
            finally:
                try:
                    group.stop()
                finally:
                    del writer, meter, group
            if not list(folder.glob(prefix+"*.ttbin")):
                raise OSError("SDK hat keine Rohdatei angelegt")
            check()
            total+=n
            meta.update(complete=True, stopped_utc=utc(), events=str(n), channel_counts=[str(v) for v in channel_counts], channel_hz=rates)
            save(folder/(prefix+".json"),meta)
            report(events=str(total),channel_hz=rates,last_data=utc() if n else None,overflows=False)
    finally:
        sdk.freeTimeTagger(tagger)
