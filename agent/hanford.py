"""Import and archive actual H1 S6 burst-injection windows. Run as python -m agent.hanford."""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import tempfile
import time
import urllib.request
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlencode, urlsplit

import h5py
import numpy as np

from agent.run_agent import ROOT, require, stamp
from agent.source_transport import SourceRedirect, sha256

CATALOG = "https://gwosc.org/static/injections/s6/burst/H1_s6burst_simple.txt"
API = "https://gwosc.org/api/v2/runs/S6/strain-files"
FAMILY = "sinegaussian-235.0-9.0-0.0-0.0"
RATE = 4096
SECONDS = 4
SCHEMA = "x6-hanford-s6-v1"
PILOT = {
    932196352: "e60f35f5757e6e286c7549577a5c39cf1ded88252919ab6df8ac32e903104a3b",
    932315136: "7424aa74d2f527abfe67cdc277e24cb41791d8cf82fcc5a6b84224daeff40547",
}
DEFAULT_ARCHIVE = ROOT / "app/causal-stability/hanford-data"


def download(url, destination, limit):
    """Only official GWOSC HTTPS. The caller supplies a private temporary directory."""
    require(urlsplit(url).scheme == "https" and urlsplit(url).netloc == "gwosc.org", "Unexpected source")
    opener = urllib.request.build_opener(SourceRedirect)
    request = urllib.request.Request(url, headers={"User-Agent": "X6-Hanford/1", "Accept-Encoding": "identity"})
    for attempt in range(2):
        try:
            with opener.open(request, timeout=45) as response, destination.open("wb") as output:
                require(response.status == 200, "Expected complete GWOSC response")
                length = response.headers.get("Content-Length")
                require(length is None or 0 < int(length) <= limit, "Unexpected GWOSC response size")
                digest = hashlib.sha256()
                size = 0
                deadline = time.monotonic() + 240
                while block := response.read(1024 * 1024):
                    size += len(block)
                    require(size <= limit and time.monotonic() <= deadline, "GWOSC transfer exceeded budget")
                    output.write(block)
                    digest.update(block)
                require(size > 0 and (length is None or size == int(length)), "Truncated GWOSC response")
                return {"sha256": digest.hexdigest()}
        except OSError:
            if attempt:
                raise
            time.sleep(2)


def write_atomic(path, value):
    data = (json.dumps(value, allow_nan=False, separators=(",", ":")) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        tmp = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
    try:
        tmp.chmod(0o644)
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def catalog_rows(raw):
    rows = {}
    for line in raw.decode("ascii").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        gps, hrss, waveform, expected, recovered = [s.strip() for s in next(csv.reader([line]))]
        if waveform != FAMILY or Decimal(hrss) != Decimal("2.08e-21"):
            continue
        key = Decimal(gps)
        require(key not in rows, "Ambiguous catalogue time")
        rows[key] = {"gps": gps, "waveform": waveform, "hrss": hrss,
                     "snr_expected_catalog": float(expected), "snr_recovered_catalog": float(recovered),
                     "source_row": line.strip()}
    return rows


def quality_group(group, prefix, start, duration):
    mask = group[prefix + "mask"]
    names = [s.decode() for s in group[prefix + "Shortnames"][:]]
    require(len(names) == len(set(names)) and len(names) == mask.attrs["Bits"],
            "Inconsistent GWOSC mask legend")
    require(mask.attrs["Xspacing"] == 1 and mask.attrs["Xstart"] == start
            and mask.shape == (duration,), "Wrong quality time axis")
    return mask, names


def summary(values, event_offset):
    """Peak Hann-windowed 235 Hz quadrature amplitude in a fixed +/-0.25 s search."""
    width = 256
    tap = np.hanning(width)
    oscillator = np.exp(-2j * np.pi * 235 * np.arange(width) / RATE)
    lo = math.ceil((event_offset - 0.25) * RATE - (width - 1) / 2)
    hi = math.floor((event_offset + 0.25) * RATE - (width - 1) / 2)
    require(0 <= lo <= hi and hi + width <= len(values), "Search outside waveform")
    response = np.convolve(values[lo:hi + width], (tap * oscillator)[::-1], mode="valid")
    amplitude = 2 * np.abs(response) / tap.sum()
    peak = int(np.argmax(amplitude))
    return {"peak_amplitude_strain": float(amplitude[peak]),
            "peak_offset_from_catalog_s": (lo + peak + (width - 1) / 2) / RATE - event_offset}


def extract(hdf5, row, file_start):
    gps = Decimal(row["gps"])
    start = int(gps) - 2
    with h5py.File(hdf5, "r") as f:
        require(f["meta/Detector"][()] == b"H1" and f["meta/GPSstart"][()] == file_start,
                "Detector or archive time mismatch")
        duration = int(f["meta/Duration"][()])
        offset = start - file_start
        require(0 <= offset and offset + SECONDS <= duration, "Window crosses a source file boundary")
        strain = f["strain/Strain"]
        require(strain.attrs["Xstart"] == file_start and strain.attrs["Xspacing"] == 1 / RATE
                and strain.shape == (duration * RATE,), "Wrong strain time axis")
        dq, dq_names = quality_group(f["quality/simple"], "DQ", file_start, duration)
        inj, inj_names = quality_group(f["quality/injections"], "Inj", file_start, duration)
        dq_values = [int(x) for x in dq[offset:offset + SECONDS]]
        inj_values = [int(x) for x in inj[offset:offset + SECONDS]]
        quality = {"gps_start": start, "step_s": 1, "dq_names": dq_names, "dq_mask": dq_values,
                   "injection_names": inj_names, "injection_mask": inj_values}
        validate_quality(quality, int(gps) - start)
        values = np.asarray(strain[offset * RATE:(offset + SECONDS) * RATE], dtype="<f8")
    require(np.isfinite(values).all(), "Nonfinite strain samples")
    return {"window_gps_start": start, "sample_rate_hz": RATE, "sample_count": len(values),
            "strain_unit": "dimensionless", "quality": quality,
            "strain_sha256_float64_le": hashlib.sha256(values.tobytes()).hexdigest(),
            "analysis": summary(values, float(gps - start)), "strain": values.tolist()}


def validate_quality(q, event_second):
    dq_bits = sum(1 << q["dq_names"].index(n) for n in ("DATA", "BURST_CAT1"))
    inj_bit = 1 << q["injection_names"].index("HW_BURST")
    require(len(q["dq_mask"]) == len(q["injection_mask"]) == SECONDS and
            all((mask & dq_bits) == dq_bits for mask in q["dq_mask"]), "Data quality gate failed")
    require(q["injection_mask"][event_second] & inj_bit, "Missing S6 HW_BURST at the target second")


def import_row(row, catalog_sha, cache, tmp):
    start = int(Decimal(row["gps"])) - 2
    query = API + "?" + urlencode({"detector": "H1", "start": start, "stop": start + SECONDS,
                                  "sample-rate": 4, "format": "json"})
    download(query, tmp / "response.json", 256_000)
    reply = json.loads((tmp / "response.json").read_bytes())
    require(reply["results_count"] == 1 and len(reply["results"]) == 1 and not reply["next"],
            "Expected exactly one covering H1 strain file")
    entry = reply["results"][0]
    file_start, url = int(entry["gps_start"]), entry["hdf5_url"]
    parsed = urlsplit(url)
    pattern = rf"/archive/data/S6/\d+/H-H1_LOSC_4_V\d+-{file_start}-\d+\.hdf5"
    require(entry["detector"] == "H1" and entry["sample_rate_kHz"] == 4
            and parsed.scheme == "https" and parsed.netloc == "gwosc.org"
            and re.fullmatch(pattern, parsed.path), "Unexpected H1 archive response")
    path = cache / Path(parsed.path).name
    pending = not path.is_file()
    if not pending:
        digest = sha256(path)
    else:
        incoming = tmp / "download.hdf5"
        digest = download(url, incoming, 180_000_000)["sha256"]
    require(file_start not in PILOT or PILOT[file_start] == digest, "Pilot source SHA-256 changed")
    result = extract(incoming if pending else path, row, file_start)
    if pending:
        incoming.replace(path)
    return {"schema": SCHEMA, "detector": "H1", "run": "S6", "catalog": row,
            "source": {"catalog_url": CATALOG, "catalog_sha256": catalog_sha, "api_url": query,
                       "hdf5_url": url, "hdf5_sha256": digest, "file_gps_start": file_start,
                       "archived_utc": stamp(), "license": "CC BY 4.0", "provider": "GWOSC"},
            **result}


def verify_entry(folder, entry):
    gps = entry["gps"]
    require(re.fullmatch(r"[0-9]{9}\.[0-9]{2}", gps) and entry["file"] == "H1-" + gps + ".json",
            "Invalid archive filename")
    path = folder / entry["file"]
    require(sha256(path) == entry["sha256"], "Measurement file SHA-256 mismatch")
    record = json.loads(path.read_bytes())
    require(record["schema"] == SCHEMA and record["detector"] == "H1" and record["run"] == "S6"
            and record["catalog"]["gps"] == gps, "Record identity mismatch")
    data = np.asarray(record["strain"], dtype="<f8")
    require(data.shape == (RATE * SECONDS,) and record["sample_count"] == len(data)
            and record["sample_rate_hz"] == RATE and np.isfinite(data).all(), "Invalid stored samples")
    require(hashlib.sha256(data.tobytes()).hexdigest() == record["strain_sha256_float64_le"],
            "Stored strain SHA-256 mismatch")
    start = int(Decimal(gps)) - 2
    require(record["window_gps_start"] == record["quality"]["gps_start"] == start, "Wrong window start")
    validate_quality(record["quality"], 2)
    require(entry["peak_235hz_strain"] == record["analysis"]["peak_amplitude_strain"] and
            entry["gwosc_snr"] == record["catalog"]["snr_recovered_catalog"], "Summary index mismatch")
    expected = summary(data, float(Decimal(gps) - start))
    require(all(math.isclose(value, record["analysis"][key], rel_tol=1e-10, abs_tol=0.0)
                for key, value in expected.items()), "Stored analysis does not replay")


def sync(folder, cache, count, verify_only=False):
    # Directory locking keeps simultaneous writers and a restarted import consistent (POSIX).
    import fcntl
    folder.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(folder, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        index = folder / "index.json"
        if index.exists():
            archive = json.loads(index.read_bytes())
            require(archive["schema"] == SCHEMA, "Incompatible archive index")
            entries = archive["records"]
            require(len({e["gps"] for e in entries}) == len(entries), "Duplicate GPS in index")
            for entry in entries:
                verify_entry(folder, entry)
        else:
            entries = []
        if verify_only:
            require(entries, "No archived measurements")
            return len(entries)
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as scratch:
            tmp = Path(scratch)
            catalog = download(CATALOG, tmp / "catalog.txt", 2_000_000)
            rows = catalog_rows((tmp / "catalog.txt").read_bytes())
            require(1 <= count <= len(rows), f"Choose a count between 1 and {len(rows)}")
            (tmp / "catalog.txt").replace(cache / (catalog["sha256"] + ".txt"))
            known = {e["gps"] for e in entries}
            for key in sorted(rows)[:count]:
                row = rows[key]
                if row["gps"] in known:
                    continue
                record = import_row(row, catalog["sha256"], cache, tmp)
                path = folder / ("H1-" + row["gps"] + ".json")
                write_atomic(path, record)
                entries.append({"gps": row["gps"], "file": path.name, "sha256": sha256(path),
                                "peak_235hz_strain": record["analysis"]["peak_amplitude_strain"],
                                "gwosc_snr": row["snr_recovered_catalog"]})
                entries.sort(key=lambda e: Decimal(e["gps"]))
                write_atomic(index, {"schema": SCHEMA, "method": "hann-quadrature-235hz-v1",
                                     "source": "LIGO H1 / GWOSC S6 hardware injections",
                                     "records": entries})
                print("Archived", path.name, flush=True)
        return len(entries)
    finally:
        os.close(descriptor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=2, help="First N matching catalogue injections")
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--cache", type=Path, default=ROOT / "runs/hanford-hdf5")
    parser.add_argument("--verify", action="store_true", help="Replay saved records offline")
    args = parser.parse_args()
    print(f"{sync(args.archive, args.cache, args.count, args.verify)} archived measurements verified/imported.")
