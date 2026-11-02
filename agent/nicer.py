"""Archive one public NICER observation of PSR J0030+0451 per invocation."""
import argparse
import fcntl
import gzip
import hashlib
import json
import math
import re
import tempfile
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode

import numpy as np
from astropy.io import fits
from astropy.io.votable import parse_single_table

from agent.run_agent import require, utcnow
from agent.source_transport import download

TARGET = "PSR_J0030+0451"
HOST = "heasarc.gsfc.nasa.gov"
BASE = "https://" + HOST
TAP = BASE + "/xamin/vo/tap/sync"
MJD0 = date(1858, 11, 17)
QUERY = ("SELECT TOP 52 obsid,name,time,exposure,processing_status,public_date,"
         "processing_date,processing_version FROM nicermastr "
         "WHERE name='PSR_J0030+0451' AND processing_status='VALIDATED' "
         "AND exposure>0 AND public_date>0 AND public_date<={today} ORDER BY obsid")
STEP = 64
BAND = (30, 299)  # 0.30 <= E < 3.00 keV, 10 eV per calibrated PI channel
INDEX_SCHEMA = "x6-nicer-index-v1"
RECORD_SCHEMA = "x6-nicer-lightcurve-v1"


def catalog(tmp):
    today = (utcnow().date() - MJD0).days
    query = QUERY.format(today=today)
    url = TAP + "?" + urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "QUERY": query})
    path = tmp / "catalog.xml"
    download(url, path, 512_000, allowed_hosts={HOST})
    statuses = [e.get("value") for e in ET.parse(path).findall(".//{*}INFO[@name='QUERY_STATUS']")]
    require(statuses and all(status == "OK" for status in statuses), "HEASARC TAP query failed")
    rows = []
    for row in parse_single_table(path, verify="exception").to_table(use_names_over_ids=True):
        obsid = str(row["obsid"])
        require(re.fullmatch(r"[0-9]{10}", obsid) and str(row["name"]) == TARGET and
                str(row["processing_status"]) == "VALIDATED" and 0 < int(row["public_date"]) <= today,
                "Unexpected or unreleased observation")
        start_day = MJD0 + timedelta(days=math.floor(float(row["time"])))
        revision = [str(row["processing_date"]), str(row["processing_version"])]
        rows.append({"obsid": obsid, "month": start_day.strftime("%Y_%m"), "revision": revision})
    require(0 < len(rows) <= 52 and len({r["obsid"] for r in rows}) == len(rows),
            "Unexpected catalog size or duplicate ObsID")
    return rows


def lightcurve(times, pi, starts, stops):
    """Use half-open bins and GTIs; store only bins with positive observed time."""
    require(0 < len(starts) == len(stops) and
            np.all(np.isfinite(starts)) and np.all(np.isfinite(stops)) and
            np.all(stops > starts) and np.all(starts[1:] >= stops[:-1]), "Invalid GTIs")
    require(np.all(np.isfinite(times)) and len(times) == len(pi), "Invalid event times")
    origin = float(starts[0])
    span = float(stops[-1] - origin)
    require(0 < span <= 172800, "Observation exceeds the two-day bound")
    n = math.ceil(span / STEP)
    edges = origin + STEP * np.arange(n + 1)
    exposure = np.zeros(n)
    for start, stop in zip(starts, stops):
        left = int((start - origin) // STEP)
        right = math.ceil((stop - origin) / STEP)
        exposure[left:right] += (np.minimum(edges[left + 1:right + 1], stop)
                                 - np.maximum(edges[left:right], start))
    chosen = times[(pi >= BAND[0]) & (pi <= BAND[1])]
    pos = np.searchsorted(starts, chosen, side="right") - 1
    inside = (pos >= 0) & (chosen < stops[pos])
    counts = np.bincount(((chosen[inside] - origin) // STEP).astype(int), minlength=n)
    require(np.all(counts[exposure == 0] == 0) and
            np.isclose(exposure.sum(), (stops - starts).sum(), rtol=1e-12),
            "Exposure or event accounting failed")
    return {"origin_met_tt_s": origin, "span_s": span, "gti_s": float(exposure.sum()),
            "gti_count": len(starts), "bin_s": STEP, "pi_inclusive": list(BAND),
            "counts": int(counts.sum()), "band_events_outside_gti": int((~inside).sum()),
            "bins": [[int(i), int(counts[i]), float(exposure[i])] for i in np.flatnonzero(exposure)]}


def reduce_fits(path, obsid):
    with fits.open(path, memmap=False) as hdus:
        hdus.verify("exception")
        events, gti = hdus["EVENTS"], hdus["GTI"]
        for hdu in [hdus[0], events, gti]:
            require(hdu.verify_checksum() == 1 and hdu.verify_datasum() == 1,
                    "Missing or failed FITS integrity check")
        for hdu in [events, gti]:
            h = hdu.header
            require((h["TELESCOP"], h["INSTRUME"], h["OBS_ID"], h["OBJECT"]) ==
                    ("NICER", "XTI", obsid, TARGET), "Wrong instrument, target or observation")
            require((h["TIMESYS"], h["TIMEREF"], h["TIMEUNIT"]) == ("TT", "LOCAL", "s"),
                    "Unexpected time reference")
        h = events.header
        require(all(h[k] == gti.header[k] for k in ["MJDREFI", "MJDREFF"]),
                "Events and GTIs use different time origins")
        require(events.columns["TIME"].unit == "s" and
                all(gti.columns[k].unit == "s" for k in ["START", "STOP"]), "Unexpected time columns")
        ez, gz = float(h.get("TIMEZERO", 0)), float(gti.header.get("TIMEZERO", 0))
        curve = lightcurve(events.data["TIME"] + ez, events.data["PI"],
                           gti.data["START"] + gz, gti.data["STOP"] + gz)
        return {"schema": RECORD_SCHEMA, "obsid": obsid, "target": TARGET,
                "date_obs": h["DATE-OBS"], "procver": h["PROCVER"], "caldbver": h["CALDBVER"],
                "mjdref_tt": [int(h["MJDREFI"]), float(h["MJDREFF"])], **curve}


def acquire(row, tmp):
    obsid = row["obsid"]
    url = (f"{BASE}/FTP/nicer/data/obs/{row['month']}/{obsid}/xti/event_cl/"
           f"ni{obsid}_0mpu7_cl.evt.gz")
    packed = tmp / "events.gz"
    meta = download(url, packed, 16 * 1024**2, allowed_hosts={HOST})
    path = tmp / "events.fits"
    with gzip.open(packed, "rb") as src, path.open("wb") as dst:
        while block := src.read(1024**2):
            require(dst.tell() + len(block) <= 96 * 1024**2, "Expanded FITS exceeds cap")
            dst.write(block)
    record = reduce_fits(path, obsid)
    record["source"] = {"archive": "NASA NICER / HEASARC", "url": url, "sha256_gzip": meta["sha256"],
                        "retrieved_utc": meta["retrieved_at"], "catalog_revision": row["revision"],
                        "policy": BASE + "/docs/heasarc/data_policy.html"}
    return record


def archive_next(out):
    out.mkdir(parents=True, exist_ok=True)
    index = out / "index.json"
    with (out / ".nicer.lock").open("a") as lock, tempfile.TemporaryDirectory(dir=out) as work:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tmp = Path(work)
        manifest = json.loads(index.read_text()) if index.exists() else {"schema": INDEX_SCHEMA, "entries": []}
        require(manifest["schema"] == INDEX_SCHEMA, "Unknown archive version")
        entries = {e["obsid"]: e for e in manifest["entries"]}
        for row in catalog(tmp):
            obsid = row["obsid"]
            old = entries.get(obsid)
            if old and old["revision"] == row["revision"]:
                continue
            record = acquire(row, tmp)
            data = (json.dumps(record, separators=(",", ":"), allow_nan=False) + "\n").encode()
            digest = hashlib.sha256(data).hexdigest()
            filename = f"{obsid}-{digest[:16]}.json"
            (tmp / "record").write_bytes(data)
            (tmp / "record").replace(out / filename)
            entries[obsid] = {"obsid": obsid, "date": record["date_obs"][:10], "file": filename,
                              "sha256": digest, "revision": row["revision"]}
            manifest["entries"] = [entries[key] for key in sorted(entries)]
            (tmp / "index").write_text(json.dumps(manifest, indent=2) + "\n")
            (tmp / "index").replace(index)
            print(f"Archived {obsid}, {record['counts']} events in {record['gti_s']:.3f} GTI seconds")
            return
        print("All eligible catalog revisions already archived.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    archive_next(parser.parse_args().output)
