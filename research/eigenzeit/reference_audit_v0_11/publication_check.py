"""Verify the published artifacts and optionally reproduce the frozen v0.11 package."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, label):
    if not ok:
        raise ValueError(f"verification failed: {label}")


def manifest(data):
    rows = [line.split(None, 1) for line in data.decode().splitlines()]
    entries = {name: sha for sha, name in rows}
    require(len(rows) == len(entries), "duplicate manifest entry")
    return entries


def check(replay):
    rec = json.loads((HERE / "PUBLICATION.json").read_text())
    for name, sha in rec["files"].items():
        require(digest((HERE / name).read_bytes()) == sha, name)
    with ZipFile(HERE / rec["archive"]) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == rec["archive_members"], "archive inventory")
        payloads = manifest(z.read("MANIFEST.sha256"))
        require(set(names) == set(payloads) | {"MANIFEST.sha256"}, "manifest inventory")
        for entries in (payloads, manifest(z.read("FREEZE.sha256"))):
            for name, sha in entries.items():
                require(digest(z.read(name)) == sha, name)
        for public, member in rec["archive_copies"].items():
            require((HERE / public).read_bytes() == z.read(member), public)
        require((HERE / rec["report"]).read_bytes().startswith(z.read("Bericht.pdf")), "archived PDF")
        print(f"PASS: original PDF, ZIP, {len(names)} entries, freeze and public extracts", flush=True)
        origin = json.loads(z.read("previous/ORIGIN-v10.json"))
        previous = HERE / rec["previous_archive"]
        require(digest(previous.read_bytes()) == origin["archive_sha256"], "published v0.10 archive")
        with ZipFile(previous) as prior:
            for name, sha in origin["files"].items():
                data = prior.read(name)
                require(data == z.read("previous/" + name) and digest(data) == sha, name)
        print(f"PASS: {len(origin['files'])} inputs compared with the published v0.10 archive", flush=True)
        if replay:
            with tempfile.TemporaryDirectory() as work:
                z.extractall(work)
                subprocess.run(
                    [sys.executable, "-B", "reproduce.py", "--previous-archive", str(previous.resolve())],
                    cwd=work,
                    check=True,
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    check(parser.parse_args().replay)
