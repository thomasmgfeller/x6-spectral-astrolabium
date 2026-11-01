"""Verify a release against its archive and optionally repeat the scientific runs."""
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
PACKAGE = HERE / "package"
REPORT = "Eigenzeit_Trennleistung_Einzelordnung_v0_2.pdf"
ARCHIVE = "Eigenzeit_Trennleistung_Einzelordnung_v0_2_Pruefpaket.zip"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def manifest(data):
    rows = [line.split("  ", 1) for line in data.decode().splitlines()]
    hashes = {name: value for value, name in rows}
    require(len(rows) == len(hashes), "duplicate manifest entry")
    return hashes

def main(replay):
    record = json.loads((HERE / "PUBLICATION.json").read_bytes())
    for name in (REPORT, ARCHIVE):
        require(digest((HERE / name).read_bytes()) == record["files"][name], name)
    with ZipFile(HERE / ARCHIVE) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == record["archive_members"], "archive inventory")
        payloads = manifest(z.read("MANIFEST.sha256"))
        require(len(payloads) == record["manifest_payloads"] and set(names) == set(payloads) | {"MANIFEST.sha256"}, "payload inventory")
        freeze = z.read("FREEZE.sha256")
        require(digest(freeze) == record["freeze_sha256"], "freeze digest")
        for inventory in (payloads, manifest(freeze)):
            for name, sha in inventory.items():
                require(digest(z.read(name)) == sha, name)
        for name in names:
            require((PACKAGE / name).read_bytes() == z.read(name), name)
        embedded = z.read("Bericht.pdf")
        require(digest(embedded) == record["archived_report_sha256"] and
                (HERE / REPORT).read_bytes().startswith(embedded), "PDF prefix")
        print("PASS: PDF, ZIP, all 25 archive members and the study freeze", flush=True)
        if replay:
            with TemporaryDirectory() as tmp:
                z.extractall(tmp)
                env = dict(os.environ)
                env.pop("PYTHONOPTIMIZE", None)
                env["PYTHONDONTWRITEBYTECODE"] = "1"
                for args, expected in [(["certificate.py"], "certificate.json"),
                                       (["audit.py", "certificate.json"], "checks.json"),
                                       (["examples.py"], "examples.json")]:
                    actual = subprocess.check_output([sys.executable, "-B", *args], cwd=tmp, env=env)
                    require(actual == z.read(expected), "replay mismatch: " + expected)
                    print("PASS: byte-identical " + expected, flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    main(parser.parse_args().replay)
