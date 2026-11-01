"""Verify the v0.3 publication, then optionally reproduce the study in a temporary directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PDF = "Eigenzeit_Drei_Geometrien_v0_3.pdf"
ZIP = "Eigenzeit_Drei_Geometrien_v0_3_Pruefpaket.zip"
VIEW = "app/eigenzeit-kruemmungsintervalle/index.html"

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def manifest(data):
    rows = [line.split("  ", 1) for line in data.decode().splitlines()]
    hashes = {name: value for value, name in rows}
    require(len(rows) == len(hashes), "duplicate path in checksum manifest")
    return hashes

def replay(z, workers, baseline):
    import numpy as np
    with TemporaryDirectory() as tmp:
        temp = Path(tmp)
        source = temp / "study"
        generated = temp / "regenerated"
        z.extractall(source)
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"}
        env.pop("PYTHONOPTIMIZE", None)
        def run(*args, environment=env):
            return subprocess.check_output([sys.executable, "-B", *map(str, args)], cwd=source, env=environment)
        for script, expected in [("theorem.py", "records/certificate.json"), ("controls.py", "records/controls.json")]:
            require(run(script) == z.read(expected), "replay mismatch: " + expected)
        print("PASS: exact certificate and mathematical controls", flush=True)
        env_sim = {**env, "NPY_DISABLE_CPU_FEATURES": "AVX512F"} if baseline else env
        run("simulate.py", generated, "--workers", workers, environment=env_sim)
        with np.load(source / "pilot/observations.npz", allow_pickle=False) as a, np.load(generated / "observations.npz", allow_pickle=False) as b:
            require(a.files == b.files == ["blocks"], "unexpected observation arrays")
            original, repeat = a["blocks"], b["blocks"]
            require(original.dtype == repeat.dtype == np.uint8 and original.shape == (120, 112500) and np.array_equal(original, repeat), "pilot block observations changed")
        expected_truth = json.loads(z.read("pilot/truth.json"))
        if baseline:
            pins = json.loads((HERE / "cpu_baseline.json").read_text())
            require(set(pins) == {str(row["id"]) for row in expected_truth}, "invalid baseline inventory")
            for row in expected_truth:
                row["coords_sha256"] = pins[str(row["id"])]
        require(json.loads((generated / "truth.json").read_text()) == expected_truth, "pilot metadata or coordinate hashes changed")
        decisions = run("score.py", generated / "observations.npz")
        require(decisions == z.read("pilot/decisions.json"), "pilot decisions changed")
        (generated / "decisions.json").write_bytes(decisions)
        require(run("pilot_audit.py", generated) == z.read("records/pilot_audit.json"), "pilot audit changed")
        print("PASS: 13,500,000 group counts, pinned case metadata, 120 decisions and pilot audit", flush=True)
        html, vectors = temp / "view.html", temp / "vectors.json"
        run("visual/build.py", html, "--tests", vectors)
        require(html.read_bytes() == z.read("Ansicht.html"), "regenerated viewer changed")
        subprocess.run(["node", "visual/verify.cjs", str(vectors)], cwd=source, env=env, check=True)

def main(args):
    rec = json.loads((HERE / "PUBLICATION.json").read_text())
    for name in ((HERE / PDF).relative_to(ROOT).as_posix(), (HERE / ZIP).relative_to(ROOT).as_posix(), VIEW):
        require(digest((ROOT / name).read_bytes()) == rec["files"][name], name)
    with ZipFile(HERE / ZIP) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == rec["archive_members"], "archive inventory")
        payloads = manifest(z.read("MANIFEST.sha256"))
        require(len(payloads) == rec["manifest_payloads"] and set(names) == set(payloads) | {"MANIFEST.sha256"}, "payload inventory")
        freeze = z.read("FREEZE.sha256")
        require(digest(freeze) == rec["freeze_sha256"], "study freeze")
        for item in (payloads, manifest(freeze)):
            for name, sha in item.items():
                require(digest(z.read(name)) == sha, name)
        for archived, public in [("BEWEIS.md", HERE / "BEWEIS.md"), ("records/certificate.json", HERE / "certificate.json"),
                                 ("records/pilot_audit.json", HERE / "pilot_audit.json"), ("Ansicht.html", ROOT / VIEW)]:
            require(z.read(archived) == public.read_bytes(), archived)
        report = z.read("Bericht.pdf")
        require(digest(report) == rec["archived_pdf_sha256"] and (HERE / PDF).read_bytes().startswith(report), "PDF prefix")
        print("PASS: all three public files, 37 archive entries and the study freeze", flush=True)
        if args.replay:
            replay(z, args.workers, args.cpu_baseline)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--cpu-baseline", action="store_true")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if args.workers < 1 or (args.cpu_baseline and not args.replay):
        parser.error("positive worker count required; --cpu-baseline requires --replay")
    main(args)
