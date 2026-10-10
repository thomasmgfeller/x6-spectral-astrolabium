"""Explicit, fixed experimental subsets. No inferred health or qubit-state labels."""
from __future__ import annotations

import io
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

import h5py
import numpy as np

from agent.run_agent import require, write_json
from agent.source_transport import download, read_zip_member, sha256

QUTECH_URL = "https://zenodo.org/records/18470200/files/raw_data.zip?download=1"
QUTECH_MEMBER = "data/ds_1730672289460108893.hdf5"
QUTECH_SHA = "7c42a454d7704cbea3291f59d6f671f6214dfafcf14315c016f512c37428b84c"
NASA_URL = "https://phm-datasets.s3.amazonaws.com/NASA/4.+Bearings.zip"
NASA_SHA = "21001ac266c465f5d345ec42d7b508c6a6328487fd9d4d7774422dd5ea10ad83"
NASA_ETAG = '"a201e36fe558f3f50509701b6d573532-63"'
NASA_FILES = {
    "2004.02.12.10.32.39": "bbbe024d55d76554a087bbbed3974e36505cd67da6cd066c341c6d35ecb68b7a",
    "2004.02.15.20.32.39": "c2bcf60945716c062da83fa411f6544ed867697474c7f0a8ab3130ef936924f3",
    "2004.02.19.06.22.39": "b63bbae7f6e9e7a97b14584fe2645aae13cab7f8f6010643929f3e08c2216a24",
}
NASA_README = "Readme Document for IMS Bearing Data.pdf"
NASA_README_SHA = "cf46d37c21f7f292c11bbbdd4695d876c417ed1d6425e3d87c962ae2182ae6ed"


def normalized(values, metadata):
    a = np.asarray(values, dtype=float)
    require(a.ndim == 1 and 32 <= len(a) <= 1024 and len(a) & (len(a)-1) == 0,
            "Unsupported signal length")
    require(np.isfinite(a).all(), "Missing/nonfinite measurements; no interpolation allowed")
    mean, std = float(a.mean()), float(a.std())
    require(std > 1e-12, "Constant/near-constant measurements")
    return {**metadata, "original_values": a.tolist(), "values": ((a-mean)/std).tolist(),
            "sample_count": len(a), "transform": {"name": "zscore", "mean": mean,
            "population_std": std}, "clean_reference": None,
            "physical_validation": "NOT_CLAIMED"}


def qutech_windows(path):
    """Documented repetition axis, not a continuous waveform or a state label."""
    result = []
    with h5py.File(path, "r") as f:
        require(int(f.attrs["uuid"]) == 1730672289460108893, "Wrong experiment UUID")
        d = f["_m0"]
        require(d.shape == (200, 1000) and d.dtype.kind == "f", "Unexpected readout schema")
        require(d.attrs["units"] == "mV", "Readout units changed")
        require(np.array_equal(f["repetition"][:], np.arange(1000)), "Repetition axis changed")
        wait = f["wait_time"][:]
        require(wait.shape == (200,) and np.allclose(wait, np.linspace(1000, 8000, 200),
                rtol=0, atol=1e-8) and f["wait_time"].attrs["units"] == "ns", "Wait-time axis changed")
        for row in (0, 99, 199):
            result.append(normalized(d[row, :512], {
                "name": f"wait-row-{row:03d}", "dataset": "_m0", "units": "mV",
                "uuid": str(f.attrs["uuid"]), "experiment_title": str(f.attrs["title"]),
                "recorded_at_source_local": str(f.attrs["measurement_time"]),
                "wait_time_ns": float(wait[row]), "row": row,
                "slice": [row, 0, 512], "axis": "repetition index",
                "axis_values": list(range(512)), "sampling_rate_hz": None,
                "interpretation": "Repeated voltage readouts at one wait setting; no state labels",
                "selection": "Fixed rows 0,99,199; first 512 of 1000 repetitions; no flattening"}))
    return result


def fetch_qutech(out, cache):
    source = out / "source"
    source.mkdir()
    with tempfile.TemporaryDirectory(prefix="x6-qubit-") as temp:
        meta = read_zip_member(QUTECH_URL, QUTECH_MEMBER, source / "qubit.hdf5", temp, QUTECH_SHA)
    meta.update({"doi": "10.5281/zenodo.18470200", "license": "CC-BY-4.0",
                 "attribution": "Krzywda, Matsumoto, De Smet et al. (2026), Coherence Protection for Mobile Spin Qubits in Silicon",
                 "mode": "ARCHIVAL_EXPERIMENT_SUBSET", "affiliation_or_endorsement": False})
    write_json(source / "provenance.json", meta)
    return meta, qutech_windows(source / "qubit.hdf5")


def valid_nasa_cache(cache):
    return all((cache/name).is_file() and sha256(cache/name) == digest
               for name, digest in {**NASA_FILES, NASA_README: NASA_README_SHA}.items())


def populate_nasa_cache(cache):
    """One bounded official archive bootstrap; retain only selected original files."""
    import libarchive
    import py7zr
    cache.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="x6-nasa-") as temp:
        work = Path(temp)
        meta = download(NASA_URL, work/"nasa.zip", 1_100_000_000, deadline_seconds=600)
        require(meta["sha256"] == NASA_SHA, "NASA archive changed; reviewed pin required")
        with zipfile.ZipFile(work/"nasa.zip") as z:
            entry = z.getinfo("4. Bearings/IMS.7z")
            require(entry.file_size == 1075320408, "Unexpected inner NASA archive size")
            with z.open(entry) as src, (work/"IMS.7z").open("wb") as dst:
                shutil.copyfileobj(src, dst, 1024*1024)
        with py7zr.SevenZipFile(work/"IMS.7z") as z:
            z.extract(path=work, targets=["2nd_test.rar", NASA_README])
        with libarchive.file_reader(str(work/"2nd_test.rar")) as archive:
            for entry in archive:
                name = entry.pathname.removeprefix("2nd_test/")
                if entry.pathname == "2nd_test/" + name and name in NASA_FILES:
                    require(entry.size <= 1_000_000, "NASA member exceeds cap")
                    data = bytearray()
                    for block in entry.get_blocks():
                        data.extend(block)
                        require(len(data) <= 1_000_000, "NASA member exceeds cap")
                    (work/name).write_bytes(data)
        for name, digest in {**NASA_FILES, NASA_README: NASA_README_SHA}.items():
            require((work/name).is_file() and sha256(work/name) == digest,
                    "Missing/changed NASA member: " + name)
            shutil.copyfile(work/name, cache/name)
    require(valid_nasa_cache(cache), "NASA bootstrap verification failed")
    return meta


def nasa_window(raw, name):
    a = np.loadtxt(io.BytesIO(raw))
    require(a.shape == (20480, 4) and np.isfinite(a).all(), "NASA matrix shape/nonfinite error")
    channel = a[:, 0]
    result = normalized(channel[:1024], {
        "name": name, "recorded_at_source_local": name, "channel": 1, "bearing": 1,
        "units": "source accelerometer amplitude; no additional calibration assumed",
        "sampling_rate_hz": 20000, "axis": "time seconds within record",
        "axis_values": (np.arange(1024)/20000).tolist(), "slice": [0, 1024, 0],
        "selection": "Fixed early/middle/final record of test 2; first 1024 contiguous samples of channel 1",
        "full_record_rows": 20480, "health_label": None,
        "interpretation": "Chronological anchors, not per-record health labels or a trained failure detector"})
    result["full_record_observations"] = {
        "rms": float(np.sqrt(np.mean(channel**2))),
        "population_std": float(channel.std()), "peak_absolute": float(np.abs(channel).max())}
    return result


def fetch_nasa(out, cache):
    source = out/"source"
    source.mkdir()
    # Live transport check is separate from historical measurement acquisition.
    probe = download(NASA_URL, source/"archive-header.bin", 64, "0-63")
    require(probe["content_range"] == "bytes 0-63/1075597174" and probe["etag"] == NASA_ETAG,
            "NASA archive identity changed")
    cache = cache/"nasa-ims-subset-v1"
    hit = valid_nasa_cache(cache)
    bootstrap = None if hit else populate_nasa_cache(cache)
    for name in [*NASA_FILES, NASA_README]:
        shutil.copyfile(cache/name, source/name)
    meta = {"url": NASA_URL, "archive_sha256": NASA_SHA, "archive_sha256_verified_this_run": not hit,
            "mode": "ARCHIVAL_EXPERIMENT_SUBSET", "cache_hit": hit, "transport_probe": probe,
            "bootstrap": bootstrap, "members_sha256": NASA_FILES, "readme_sha256": NASA_README_SHA,
            "attribution": "J. Lee, H. Qiu, G. Yu, J. Lin and Rexnord (2007), IMS, University of Cincinnati; NASA PCoE repository",
            "source_terms": "https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/",
            "affiliation_or_endorsement": False}
    write_json(source/"provenance.json", meta)
    return meta, [nasa_window((source/name).read_bytes(), name) for name in NASA_FILES]
