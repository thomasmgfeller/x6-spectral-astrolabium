"""Reconstruct EPTA DR2full residuals with the frozen release and TEMPO2 environment."""
import json
import math
import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

from agent.run_agent import require
from agent.source_transport import SourceRedirect, sha256

HERE = Path(__file__).resolve().parents[1]
STUDY = HERE / "research/epta_filter_v1"
PROTOCOL = json.loads((STUDY / "protocol.json").read_text())
RECORD = "https://zenodo.org/api/records/8300645"
FILE = "EPTA-DR2.zip"
SIZE = 39275794
CREDIT = {"authors": "J. Antoniadis et al. (EPTA Collaboration)",
          "title": "The second data release from the European Pulsar Timing Array I. The dataset and timing analysis",
          "doi": "https://doi.org/10.5281/zenodo.8300645", "version": "2.1",
          "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
          "changes": "Eight selected pulsars. Fixed-model TEMPO2 residuals, time grouping, simulations and summary by X6."}


def acquire(directory):
    """Read one bounded versioned source, validate access, rights, size and digests."""
    opener = urllib.request.build_opener(SourceRedirect)
    with opener.open(RECORD, timeout=45) as response:
        data = response.read(256001)
        require(len(data) <= 256000, "Oversized Zenodo record")
        meta = json.loads(data)
    desc = meta["metadata"]
    require(desc["doi"] == PROTOCOL["release_doi"] and desc["license"]["id"] == "cc-by-4.0"
            and desc["access_right"] == "open", "Unexpected Zenodo record, access or license")
    files = [e for e in meta["files"] if e["key"] == FILE]
    url = RECORD + "/files/" + FILE + "/content"
    require(len(files) == 1 and files[0]["size"] == SIZE and files[0]["links"]["self"] == url,
            "Unexpected archive file")
    path = directory / FILE
    with opener.open(url, timeout=90) as response, path.open("wb") as dest:
        while block := response.read(1024**2):
            require(dest.tell() + len(block) <= SIZE, "Oversized release")
            dest.write(block)
    require(path.stat().st_size == SIZE and sha256(path) == PROTOCOL["archive_sha256"], "Release SHA-256 mismatch")
    return path


def unpack(path, directory):
    require(sha256(path) == PROTOCOL["archive_sha256"], "Release SHA-256 mismatch")
    base = "EPTA-DR2/EPTA-DR2/"
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.startswith(base):
                continue
            relative = Path(name[len(base):])
            parts = relative.parts
            clock = len(parts) == 2 and parts[0] == "clockfiles" and relative.suffix == ".clk"
            timing = (len(parts) >= 3 and parts[0] == "DR2full" and parts[1] in PROTOCOL["pulsars"]
                      and relative.suffix in {".par", ".tim"})
            if not (clock or timing):
                continue
            require(not relative.is_absolute() and ".." not in parts, "Unsafe archive filename")
            dest = directory / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(archive.read(name))


def sky_unit(params):
    if "RAJ" in params:
        def sexagesimal(s):
            h, m, sec = map(float, s.lstrip("+-").split(":"))
            return (-1 if s.startswith("-") else 1) * (h + m / 60 + sec / 3600)
        lon, lat = np.deg2rad([15 * sexagesimal(params["RAJ"]), sexagesimal(params["DECJ"])])
        tilt = 0
    else:
        lon, lat = np.deg2rad([float(params["ELONG"]), float(params["ELAT"])])
        tilt = math.radians(84381.406 / 3600)
    x, y, z = np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)
    return [x, y*np.cos(tilt)-z*np.sin(tilt), y*np.sin(tilt)+z*np.cos(tilt)]


def reconstruct(directory, prefix):
    # Overlay the three release clocks in a private runtime, so a default clock
    # with the same endpoints cannot be chosen in their place.
    runtime = directory / "runtime"
    default = prefix / "share/tempo2"
    runtime.mkdir()
    for subdir in default.iterdir():
        if subdir.name != "clock":
            (runtime / subdir.name).symlink_to(subdir)
    (runtime / "clock").mkdir()
    for clock in (default / "clock").iterdir():
        (runtime / "clock" / clock.name).symlink_to(clock)
    for clock in (directory / "clockfiles").glob("*.clk"):
        dest = runtime / "clock" / clock.name
        dest.unlink(missing_ok=True)
        shutil.copyfile(clock, dest)
    result = []
    for name in PROTOCOL["pulsars"]:
        root = directory / "DR2full" / name
        par = root / (name + ".par")
        params = {line.split()[0]: line.split()[1] for line in par.read_text().splitlines() if len(line.split()) >= 2}
        require(params["EPHEM"] == "DE440" and params["CLK"] == "TT(BIPM2021)", "Unexpected timing settings")
        output = root / "fixed.dat"
        cmd = [str(prefix / "bin/tempo2"), "-nofit", "-nobs", "40000", "-npsr", "1",
               "-output", "general2", "-s", "{sat} {bat} {pre} {err}\\n", "-outfile", str(output),
               "-f", par.name, name + "_all.tim"]
        proc = subprocess.run(cmd, cwd=root, env={**os.environ, "TEMPO2": str(runtime)},
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
        require(proc.returncode == 0 and output.exists() and
                not any(s in proc.stdout.lower() for s in ("no clock corrections", "unable to open", "fatal error")),
                "TEMPO2 timing failed for " + name + "\n" + proc.stdout[-2500:])
        data = np.loadtxt(output, ndmin=2)
        require(data.shape[1] == 4 and np.isfinite(data).all() and np.all(data[:, 3] > 0), "Invalid TOAs")
        data = data[np.argsort(data[:, 1], kind="stable")]
        residual = data[:, 2] * 1e6
        w = 1 / data[:, 3]**2
        wrms = float(np.sqrt(np.average((residual - np.average(residual, weights=w))**2, weights=w)))
        result.append({"name": name, "bat": data[:, 1], "sat": data[:, 0], "us": residual,
                       "error": data[:, 3], "sky": sky_unit(params), "wrms": wrms})
        print(f"{name}: {len(data)} TOAs, weighted RMS {wrms:.6f} us", flush=True)
    ref, first = PROTOCOL["reference"], result[0]
    require(first["name"] == ref["pulsar"] and len(first["bat"]) == ref["active_toas"] and
            abs(first["wrms"] - ref["weighted_rms_us"]) <= ref["absolute_tolerance_us"],
            "J0030 reference failed, stopping before injections")
    return result
