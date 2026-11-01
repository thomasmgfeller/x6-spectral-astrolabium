"""Urnerboden 2017. Read open SED data in memory; write only X6 pairwise results."""
import argparse
import hashlib
import io
import itertools
import json
import os
import re
from pathlib import Path
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import build_opener, Request

import numpy as np
from obspy import read, read_events, read_inventory
from scipy.signal import butter, sosfilt

from agent.run_agent import ROOT, require
from agent.source_transport import SourceRedirect

BASE = "https://eida.ethz.ch/fdsnws"
EVENT = "smi:ch.ethz.sed/sc3a/2017epaqsp"
STATIONS = ("LLS", "MUO", "BNALP")
BANDS = ((1, 5), (2, 8), (4, 12))
RATE = 120
NETWORK_DOI = "https://doi.org/10.12686/sed/networks/ch"
METHOD = "x6-sed-pg-variance-v1"


def fetch(service, **params):
    """Fixed SED host, public query endpoint, bounded responses, no on-disk source cache."""
    url = f"{BASE}/{service}/1/query?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "X6-SED-research/1", "Accept-Encoding": "identity"})
    for attempt in range(2):
        try:
            with build_opener(SourceRedirect).open(request, timeout=35) as response:
                require(response.status == 200, f"{service}: no data for selected window")
                payload = response.read(4_000_001)
                require(0 < len(payload) <= 4_000_000, f"{service}: unexpected payload size")
                return io.BytesIO(payload)
        except HTTPError as exc:
            if attempt or exc.code not in (429, 502, 503, 504):
                raise
        except (TimeoutError, URLError):
            if attempt:
                raise
        time.sleep(2)


def event_references():
    catalog = read_events(fetch("event", eventid=EVENT, includearrivals="true", format="xml"), format="QUAKEML")
    require(len(catalog) == 1 and str(catalog[0].resource_id) == EVENT, "Wrong event")
    event = catalog[0]
    origin = event.preferred_origin()
    require(origin is not None and event.event_type == "earthquake", "Missing earthquake origin")
    pick_by_id = {str(pick.resource_id): pick for pick in event.picks}
    references = {}
    for arrival in origin.arrivals:
        if arrival.phase != "Pg" or arrival.time_weight == 0:
            continue
        pick = pick_by_id.get(str(arrival.pick_id))
        if pick is None or pick.evaluation_mode != "manual" or not pick.waveform_id:
            continue
        wave = pick.waveform_id
        if (wave.network_code, wave.location_code or "", wave.channel_code) != ("CH", "", "HHZ"):
            continue
        if wave.station_code in STATIONS:
            require(wave.station_code not in references, "Ambiguous manual Pg reference")
            references[wave.station_code] = pick.time
    require(set(references) == set(STATIONS), "Manual Pg reference missing for selected station")
    return origin.time, references


def open_channel(inv, station, start, end):
    require(len(inv.networks) == 1, "Ambiguous network selection")
    net = inv[0]
    require(net.code == "CH" and len(net.stations) == 1, "Unexpected network or station count")
    sta = net[0]
    require(sta.code == station and len(sta.channels) == 1, "Ambiguous station/channel epoch")
    channel = sta[0]
    for part in (net, sta, channel):
        require(part.restricted_status == "open", "Missing explicit open status at network, station or channel")
        require((part.start_date is None or part.start_date <= start) and
                (part.end_date is None or part.end_date >= end), "Metadata epoch does not cover the window")
    require((channel.code, channel.location_code, channel.sample_rate) == ("HHZ", "", RATE)
            and channel.response is not None and channel.response.instrument_sensitivity is not None,
            "Missing or incompatible vertical velocity response")
    sensitivity = channel.response.instrument_sensitivity
    require(sensitivity.input_units.upper() == "M/S" and np.isfinite(sensitivity.value) and
            sensitivity.value > 0 and channel.response.response_stages, "Invalid instrument response")
    return channel


def calibrated_station(station, origin):
    start, end = origin - 60, origin + 35
    params = dict(net="CH", sta=station, loc="--", cha="HHZ",
                  starttime=start.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  endtime=end.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    inv = read_inventory(fetch("station", **params, level="response", includerestricted="false"), format="STATIONXML")
    open_channel(inv, station, start, end)
    # Fetch waveform bytes only after every applicable metadata epoch passed the open-data gate.
    stream = read(fetch("dataselect", **params), format="MSEED")
    require(len(stream) > 0 and all(tr.id == f"CH.{station}..HHZ" and tr.stats.sampling_rate == RATE
                                   for tr in stream), "Wrong waveform channel or sample rate")
    stream.trim(start, end, nearest_sample=False)
    require(len(stream) > 0 and not stream.get_gaps(), "Gap or overlap inside the analysis interval")
    stream.merge(method=-1)
    require(len(stream) == 1, "Cannot form one continuous trace")
    trace = stream[0]
    require(0 <= trace.stats.starttime - start < 1.01 / RATE and
            0 <= end - trace.stats.endtime < 1.01 / RATE, "Incomplete waveform interval")
    require(trace.data.dtype.kind == "i" and trace.data.dtype.itemsize <= 4 and
            not np.ma.isMaskedArray(trace.data), "Expected signed seismic counts of at most 32 bits")
    fingerprint = hashlib.sha256(trace.data.astype("<i4").tobytes()).hexdigest()
    trace.remove_response(inventory=inv, output="VEL", pre_filt=(0.3, 0.6, 15, 20),
                          water_level=None, zero_mean=True, taper=True, taper_fraction=0.05)
    require(np.isfinite(trace.data).all(), "Nonfinite corrected velocity")
    return trace.data, trace.stats.starttime - origin, fingerprint


def first_crossing(envelope, times, threshold, start, end):
    """Time of first sample in a sustained above-threshold run. Reject an onset outside the left edge."""
    ids = np.flatnonzero((times >= start) & (times <= end))
    hold = round(0.08 * RATE)
    require(len(ids) >= hold and ids[0] > 0, "Search interval outside trace")
    high = envelope[ids] >= threshold
    if high[0] and envelope[ids[0] - 1] >= threshold:
        return "LEFT_EDGE"
    runs = np.convolve(high.astype(int), np.ones(hold, dtype=int), mode="valid")
    hits = np.flatnonzero(runs == hold)
    return float(times[ids[hits[0]]]) if len(hits) else None


def variance_onset(signal, times, center, noise_rms):
    """Local two-variance change point. Return the first sample of the second segment."""
    ids = np.flatnonzero(np.abs(times-center) <= 1)
    x = signal[ids]
    margin = round(0.10 * RATE)
    require(len(x) >= 2*margin+1, "Missing change-point search window")
    # Normalization keeps the log scores independent of the physical unit and numerical scale.
    x = x/noise_rms
    best_score, best = np.inf, None
    for k in range(margin, len(x)-margin+1):
        before, after = np.var(x[:k]), np.var(x[k:])
        if before <= 0 or after <= 0:
            continue
        score = k*np.log(before) + (len(x)-k)*np.log(after)
        if score < best_score:
            best_score, best = score, k
    if best is None or abs(times[ids[best]]-center) >= 0.85:
        return None, "BOUNDARY_OR_FLAT"
    if np.var(x[best:]) < 9*np.var(x[:best]) or np.sqrt(np.mean(x[best:]**2)) < 6:
        return None, "LOW_CONTRAST"
    return float(times[ids[best]]), "OK"


def band_picks(velocity, t0, reference):
    times = t0 + np.arange(len(velocity))/RATE
    noise = (times >= -45) & (times < -15)
    require(np.count_nonzero(noise) >= 29*RATE, "Missing noise baseline")
    picks, checks = [], []
    for low, high in BANDS:
        filt = sosfilt(butter(4, [low, high], btype="bandpass", fs=RATE, output="sos"), velocity)
        width = round(0.1*RATE)
        rms = np.sqrt(np.convolve(filt*filt, np.ones(width)/width, mode="full")[:len(filt)])
        baseline = float(np.median(rms[noise]))
        require(baseline > 0 and np.isfinite(baseline), "Unusable noise baseline")
        quiet_rms = first_crossing(rms,times,6*baseline,-12,-10)
        crossing = first_crossing(rms,times,6*baseline,reference-1,reference+1)
        rms_status = "OK" if isinstance(crossing,float) else (crossing or "NO_TRIGGER")
        quiet_onset, _ = variance_onset(filt,times,-11,baseline)
        pick, status = variance_onset(filt,times,reference,baseline)
        if quiet_onset is not None:
            pick, status = None, "QUIET_TRIGGER"
        checks.append({"variance":status, "rms":rms_status if quiet_rms is None else "QUIET_TRIGGER"})
        picks.append(pick)
    return picks, checks


def compare(picks):
    rows = []
    for a,b in itertools.combinations(STATIONS,2):
        differences = [None if x is None or y is None else y-x for x,y in zip(picks[a],picks[b], strict=True)]
        spread = None if None in differences else round(1000*(max(differences)-min(differences)),3)
        rows.append({"from":a, "to":b, "delay_s":[round(d,6) if d is not None else None for d in differences],
                     "spread_ms":spread})
    return rows


def run():
    origin, references = event_references()
    picks, fingerprints, checks = {}, {}, {}
    for station in STATIONS:
        velocity, t0, fingerprints[station] = calibrated_station(station, origin)
        try:
            picks[station], checks[station] = band_picks(velocity, t0, references[station]-origin)
        except ValueError as exc:
            raise ValueError(f"{station}: {exc}") from exc
    # Only non-reconstructive X6 diagnostics and provenance identifiers enter the public result.
    return {"method": METHOD, "event_id": EVENT, "network_doi": NETWORK_DOI, "sample_rate_hz": RATE,
            "bands_hz": [list(band) for band in BANDS], "pairs": compare(picks),
            "input_counts_sha256_le_i32": fingerprints, "checks": checks}


def verify_public_result(result):
    """Whitelist the public format, including every nested field. Provider payloads stay in memory."""
    require(set(result) == {"method","event_id","network_doi","sample_rate_hz","bands_hz","pairs",
                            "input_counts_sha256_le_i32","checks"}, "Unexpected public result fields")
    require((result["method"], result["event_id"], result["network_doi"], result["sample_rate_hz"]) ==
            (METHOD, EVENT, NETWORK_DOI, RATE) and result["bands_hz"] == [list(b) for b in BANDS],
            "Experimental contract mismatch")
    hashes, checks = result["input_counts_sha256_le_i32"], result["checks"]
    require(set(hashes) == set(checks) == set(STATIONS) and
            all(re.fullmatch("[0-9a-f]{64}", h) for h in hashes.values()), "Invalid provenance")
    for station in STATIONS:
        require(len(checks[station]) == len(BANDS), "Missing station checks")
        for c in checks[station]:
            require(set(c) == {"rms","variance"} and c["rms"] in {"OK","LEFT_EDGE","NO_TRIGGER","QUIET_TRIGGER"}
                    and c["variance"] in {"OK","BOUNDARY_OR_FLAT","LOW_CONTRAST","QUIET_TRIGGER"},
                    "Invalid station status")
    for row,(a,b) in zip(result["pairs"], itertools.combinations(STATIONS,2), strict=True):
        require(set(row) == {"from","to","delay_s","spread_ms"} and (row["from"],row["to"]) == (a,b),
                "Invalid station pair")
        delays = row["delay_s"]
        require(len(delays) == len(BANDS), "Unexpected delay count")
        for i,delay in enumerate(delays):
            valid = checks[a][i]["variance"] == checks[b][i]["variance"] == "OK"
            require((valid and type(delay) in (float,int) and np.isfinite(delay)) or
                    (not valid and delay is None), "Invalid delay for quality status")
        if None in delays:
            require(row["spread_ms"] is None, "Incomplete pair cannot have a three-band spread")
        else:
            require(type(row["spread_ms"]) in (float,int) and row["spread_ms"] >= 0 and
                    abs(row["spread_ms"] - (max(delays)-min(delays))*1000) <= .002,
                    "Inconsistent spread")


def save(result, target):
    verify_public_result(result)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as temp:
        partial = Path(temp)/"summary.json"
        partial.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n",encoding="utf-8")
        os.replace(partial,target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"runs/sed/summary.json",
                        help="Destination of derived X6 results only")
    args = parser.parse_args()
    save(run(),args.output)
    print(f"Three stations, three bands, checks and available differences saved to {args.output}")
