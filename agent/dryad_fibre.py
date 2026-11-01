"""Archive the MIT fibre matrix slice from Dryad and model a two-input phase perturbation."""
import argparse
import fcntl
import hashlib
import json
import math
import os
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote, urlsplit

import h5py
import numpy as np

from agent.run_agent import ROOT, require
from agent.source_transport import sha256

BASE = "https://datadryad.org"
DOI = "doi:10.5061/dryad.wdbrv15wk"
VERSION = "/api/v2/versions/296860"
FILE = "/api/v2/files/3201802"
NAME = "complexTM.hdf5"
MIRROR = "https://zenodo.org/api/records/11399077"
SIZE = 773234336
DIGEST = "3006be2727f3e5761219b02c1c28eef2955a04f09f3c01f9c88d1adbe042ae6f"
SCHEMA = "x6-mit-fibre-v1"
DEFAULT_ARCHIVE = ROOT / "app/causal-stability/fibre-data"


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        require(urlsplit(newurl).scheme == "https", "Refusing insecure download redirect")
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and urlsplit(newurl).netloc != urlsplit(req.full_url).netloc:
            redirected.remove_header("Authorization")
        return redirected


def api(path):
    require(path.startswith("/api/v2/") and not urlsplit(path).netloc, "Unexpected Dryad link")
    return BASE + path


def get_json(url):
    with urllib.request.build_opener(SafeRedirect).open(url, timeout=30) as response:
        raw = response.read(2_000_001)
    require(len(raw) <= 2_000_000, "Oversized metadata")
    return json.loads(raw)


def source():
    dataset = get_json(api("/api/v2/datasets/" + quote(DOI, safe="")))
    require(dataset["identifier"] == DOI, "Wrong dataset")
    version = get_json(api(VERSION))
    require(version["_links"]["stash:dataset"]["href"] == dataset["_links"]["self"]["href"],
            "Pinned version belongs to another dataset")
    files = get_json(api(version["_links"]["stash:files"]["href"]))
    matches = [f for f in files["_embedded"]["stash:files"] if f["path"] == NAME]
    require(len(matches) == 1, "Expected one transmission matrix")
    item = matches[0]
    require(item["_links"]["self"]["href"] == FILE and item["_links"]["stash:version"]["href"] == VERSION
            and item["size"] == SIZE and item["digestType"] == "sha-256" and item["digest"] == DIGEST,
            "Dryad identity, size or digest differs from the pinned version")
    return {"doi": DOI, "title": version["title"], "authors": [a["firstName"]+" "+a["lastName"]
            for a in version["authors"]], "published": version["publicationDate"], "license": dataset["license"],
            "version_api": api(VERSION), "file_api": api(FILE), "file": NAME, "size_bytes": SIZE,
            "sha256": DIGEST, "download_url": api(item["_links"]["stash:download"]["href"])}


def checked_file(path):
    require(path.stat().st_size == SIZE and sha256(path) == DIGEST, "Source file size or SHA-256 mismatch")


def mirror_download_url():
    mirror = get_json(MIRROR)
    require("doi:" + mirror["doi"] == DOI and any(c["id"] == "dryad" for c in mirror["metadata"]["communities"]),
            "Wrong Dryad preservation record")
    files = [row for row in mirror["files"] if row["key"] == NAME and row["size"] == SIZE]
    require(len(files) == 1, "Matrix not found in preservation copy")
    url = files[0]["links"]["self"]
    require(url == MIRROR + "/files/" + NAME + "/content", "Unexpected mirror URL")
    return url


def download(cache, url):
    cache.mkdir(parents=True, exist_ok=True)
    saved = cache / NAME
    if saved.exists():
        checked_file(saved)
        return saved, "verified-cache"
    require(url == api(FILE + "/download"), "Unexpected download URL")
    token = os.environ.get("DRYAD_API_TOKEN")
    retrieval_url = url if token else mirror_download_url()
    request = urllib.request.Request(retrieval_url)
    if token:
        request.add_unredirected_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.build_opener(SafeRedirect).open(request, timeout=90) as response:
            with tempfile.TemporaryDirectory(dir=cache) as tmp:
                part = Path(tmp) / NAME
                with part.open("wb") as stream:
                    while block := response.read(1024 * 1024):
                        require(stream.tell() + len(block) <= SIZE, "Oversized payload")
                        stream.write(block)
                checked_file(part)
                os.replace(part, saved)
        return saved, retrieval_url
    except urllib.error.HTTPError as exc:
        if token and exc.code in (401, 403):
            raise ValueError(f"Dryad HTTP {exc.code}: use a valid DRYAD_API_TOKEN locally or --file complexTM.hdf5.") from None
        raise ValueError(f"Dryad download failed (HTTP {exc.code}).") from None


def extract(path):
    channels = {}
    with h5py.File(path, "r") as f:
        for name in ("T1", "T2"):
            d = f[name]
            require(isinstance(d, h5py.Dataset) and len(d.shape) == 2 and d.shape[0] >= 1 and
                    d.shape[1] >= 2 and d.dtype.kind == "c", f"{name}: expected complex output-by-input matrix")
            values = d[0, :2]
            require(np.isfinite(values).all(), f"{name}: nonfinite complex coefficients")
            channels[name] = {"shape": list(d.shape), "dtype": str(d.dtype),
                              "coefficients": [[float(z.real), float(z.imag)] for z in values]}
    require(channels["T1"]["shape"] == channels["T2"]["shape"], "Polarization channel shape mismatch")
    return {"output_row": 0, "input_columns": [0, 1], "channels": channels}


def response(measurement, delta_deg):
    """Unit-power equal input amplitudes. Tune phase on T1; sum orthogonal intensities."""
    rows = [[complex(*z) for z in measurement["channels"][name]["coefficients"]] for name in ("T1","T2")]
    a, b = rows[0]
    require(abs(a) > 0 and abs(b) > 0, "Undefined T1 phase reference")
    phase = -a/abs(a) * (b/abs(b)).conjugate() * np.exp(1j*math.radians(delta_deg))
    p1, p2 = [float(abs(x + phase*y)**2 / 2) for x, y in rows]
    return {"phase_error_deg": delta_deg, "T1_intensity": p1, "T2_intensity": p2,
            "total_intensity": p1+p2, "T1_relative_to_constructive": p1 / ((abs(a)+abs(b))**2/2)}


def persist(path, value):
    # A completed file is published in one rename. No partly written record is visible to the lab.
    with tempfile.TemporaryDirectory(dir=path.parent) as tmp:
        new = Path(tmp) / path.name
        new.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
        os.replace(new, path)


def sync(folder, cache, local=None, metadata_only=False):
    src = source()
    folder.mkdir(parents=True, exist_ok=True)
    fd = os.open(folder, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        target = folder / "record.json"
        if target.exists():
            previous = json.loads(target.read_bytes())
            require(previous["schema"] == SCHEMA and previous["source"]["sha256"] == DIGEST, "Wrong archived record")
        else:
            previous = None
        if previous is None or previous["status"] != "VERIFIED_MATRIX_SLICE":
            persist(target, {"schema": SCHEMA, "status": "METADATA_ONLY", "source": src})
        if metadata_only:
            return json.loads(target.read_bytes())["status"]
        if local is None:
            file, acquisition = download(cache, src["download_url"])
        else:
            file = Path(local)
            checked_file(file)
            acquisition = "verified-local-file"
        measurement = extract(file)
        sweep = [response(measurement, angle) for angle in (-30,-10,0,10,30)]
        trial = {"schema": SCHEMA, "status": "VERIFIED_MATRIX_SLICE", "source": src,
                 "acquisition": acquisition, "measurement": measurement, "model": "two-equal-inputs-phase-error-v1", "predictions": sweep}
        persist(target, trial)
        return trial["status"]
    finally:
        os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--metadata-only", action="store_true")
    choice.add_argument("--file", type=Path, help="Local copy of the original, checksum verified before reading")
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--cache", type=Path, default=ROOT / "runs/dryad-fibre")
    args = parser.parse_args()
    try:
        print(sync(args.archive, args.cache, args.file, args.metadata_only))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Import stopped: {exc}\n")
