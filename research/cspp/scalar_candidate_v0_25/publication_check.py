"""Check the immutable v0.25 publication and optionally replay in isolation."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "cspp_v025"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot():
    return {str(p.relative_to(PACKAGE)): digest(p)
            for p in PACKAGE.rglob("*") if p.is_file()}


def check():
    meta = read_json(ROOT / "PUBLICATION.json")
    for name, expected in meta["artifacts"].items():
        require(digest(ROOT / name) == expected, "Artifact hash differs: " + name)
    files = snapshot()
    require(len(files) == meta["package_files"] == 29, "Package file count differs")
    with zipfile.ZipFile(ROOT / "CSPP_Skalarer_Kandidat_v0_25_Pruefpaket.zip") as archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        require(len(members) == len(files), "Archive member count differs")
        names = set()
        for item in members:
            path = PurePosixPath(item.filename)
            require(not path.is_absolute() and ".." not in path.parts,
                    "Unsafe archive path")
            require(path.parts[0] == "cspp_v025", "Wrong archive prefix")
            relative = str(PurePosixPath(*path.parts[1:]))
            require(relative not in names, "Duplicate archive member")
            names.add(relative)
            require((PACKAGE / relative).read_bytes() == archive.read(item),
                    "Extracted bytes differ: " + relative)
        require(names == set(files), "Archive inventory differs")
    checksums = {}
    for line in (PACKAGE / "SHA256SUMS").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        require(relative not in checksums, "Duplicate checksum")
        checksums[relative] = expected
    require(len(checksums) == meta["checksum_entries"] == 28, "Checksum count differs")
    require(set(checksums) == set(files) - {"SHA256SUMS"}, "Checksum inventory differs")
    require(all(files[name] == value for name, value in checksums.items()),
            "Package checksum differs")
    require((ROOT / "Skalarer_Kandidat_Zweiskalenpruefung_v0_25.pdf").read_bytes()
            == (PACKAGE / "report/Skalarer_Kandidat_Zweiskalenpruefung_v0_25.pdf").read_bytes(),
            "Report copies differ")
    status = read_json(PACKAGE / "STATUS.json")
    protocol = read_json(PACKAGE / "PROTOCOL.json")
    for document in (meta, status, protocol):
        require(document["METHOD"] == document["G1"] == "HOLD", "Method gates changed")
        require(document["new_random_clouds"] == 0, "New random clouds claimed")
    require(status["candidate_step"] == "COMPLETED_WITH_JUSTIFIED_REJECTION", "Decision changed")
    require(status["publication"] == "NOT_PERFORMED_IN_THIS_STEP", "Historical flag changed")
    require(status["confirmation_design"] == "NOT_STARTED", "Confirmation started")
    for key in ("compact_detector_error", "infinite_past_propagator_stability"):
        require(status[key] == "NOT_RUN_EARLY_ABORT", "Unperformed test promoted: " + key)
    require(status["density_uniform_stability"] == "NOT_CERTIFIED", "Stability claim changed")
    require(protocol["q"] == "3/(16*pi)" and protocol["theta"] == "21", "Candidate changed")
    require(protocol["gaussian_L"] == [2, 4] and protocol["relative_mean_screen"] == "1/10",
            "Screen changed")
    require(protocol["confirmation_seed_used"] is False, "Confirmation seed used")
    for bits in (128, 192):
        cert = read_json(PACKAGE / f"results/CERTIFICATE_{bits}.json")
        require(cert["precision_bits"] == bits, "Wrong precision")
        require(cert["python"] == "3.12.14" and cert["python_flint"] == "0.8.0", "Runtime changed")
        require(cert["decision"] == meta["scientific_result"], "Certificate decision differs")
        require(cert["METHOD"] == cert["G1"] == "HOLD", "Certificate gates changed")
        require(cert["compact_detector_production"] == cert["full_spectral_stability"]
                == "NOT_RUN_EARLY_ABORT", "Certificate promotes unperformed test")
        for section, count in (("rational", 21), ("finite_stability", 7)):
            values = cert[section]["checks"]
            require(len(values) == count and all(v is True for v in values.values()),
                    "Recorded checks failed: " + section)
        require([row["L"] for row in cert["rows"]] == [2, 4], "Certificate scales changed")
        require([row["candidate_passes_mean_screen"] for row in cert["rows"]] == [True, False],
                "Candidate screen changed")
        require(cert["family"]["all_real_theta_excluded_at_fixed_q"] is True,
                "Family exclusion missing")
        require(cert["family"]["scope"] == "two Gaussian scales L=2,4; normalized polynomial degree<=4; full-past mean; fixed q",
                "Family scope changed")
    checks = read_json(PACKAGE / "results/CHECKS.json")
    require(checks["status"] == "PASS" and checks["precision_overlap_targets"] == 40,
            "Recorded precision verification failed")
    require(checks["source_files_verified"] == 9 and checks["binomial_weight_checks"] == 128,
            "Recorded input checks differ")
    require(checks["diagnostic_tolerance_is_not_a_certificate"] is True,
            "Diagnostic promoted to certificate")
    replay = read_json(PACKAGE / "results/REPLAY.json")
    require(replay["status"] == "PASS" and replay["mode"] == "full", "Recorded replay failed")
    require(len(replay["replayed"]) == 2 and all(r["byte_identical"] for r in replay["replayed"]),
            "Recorded byte replay failed")
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    before = check()
    if args.replay:
        require(platform.python_version() == "3.12.14", "Replay requires recorded Python 3.12.14")
        with tempfile.TemporaryDirectory(prefix="cspp025-publication-") as temp:
            copied = Path(temp) / "cspp_v025"
            shutil.copytree(PACKAGE, copied)
            subprocess.run([sys.executable, "-B", str(copied / "reproduce.py")], check=True,
                           cwd=copied)
        require(snapshot() == before, "Published inputs modified by replay")
    print(json.dumps({"status": "PASS", "package_files": len(before),
                      "replay": "PASS" if args.replay else "NOT_EXECUTED",
                      "METHOD": "HOLD", "G1": "HOLD"}))


if __name__ == "__main__":
    main()
