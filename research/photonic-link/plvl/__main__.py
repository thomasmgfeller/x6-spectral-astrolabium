"""Run a reproducible synthetic experiment; failures produce no success report."""
import argparse
import hashlib
import io
import json
import platform
from pathlib import Path
import numpy as np
from . import __version__
from .config import from_dict
from .simulation import run
from .bridge import encode_snapshot


def reject_duplicates(pairs):
    obj = {}
    for k,v in pairs:
        if k in obj:
            raise ValueError(f"Duplicate JSON key: {k}")
        obj[k]=v
    return obj


def provenance():
    root = Path(__file__).resolve().parent
    return {"version":__version__,"python":platform.python_version(),"numpy":np.__version__,
            "rng":"NumPy PCG64 / SeedSequence; bitwise replication requires matching environment",
            "source_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(root.glob("*.py"))}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("config",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--raw-output",type=Path,help="Optional NPZ of local and corrected events; no pair IDs")
    p.add_argument("--snapshot-output",type=Path,help="Optional synthetic SGNCv007 frame, setting label 0")
    a = p.parse_args()
    created = []
    try:
        paths = [v.resolve() for v in (a.output,a.raw_output,a.snapshot_output) if v is not None]
        if len(set(paths)) != len(paths) or a.config.resolve() in paths:
            raise ValueError("Distinct input and output paths required")
        if any(v.exists() for v in paths):
            raise ValueError("Output already exists; choose a new experiment path")
        data = a.config.read_bytes()
        cfg = from_dict(json.loads(data,object_pairs_hook=reject_duplicates))
        report, raw = run(cfg)
        report["reproducibility"] = provenance()
        report["config_file_sha256"] = hashlib.sha256(data).hexdigest()
        text = json.dumps(report,indent=2,allow_nan=False)+"\n"
        outputs = []
        if a.raw_output:
            buffer = io.BytesIO()
            np.savez_compressed(buffer,**raw)
            outputs.append((a.raw_output,buffer.getvalue()))
        if a.snapshot_output:
            outputs.append((a.snapshot_output,encode_snapshot(report)))
        # Publish the report last; remove this invocation's files on failure.
        # A multi-file set is not crash-atomic: require exit status 0 as well.
        outputs.append((a.output,text.encode()))
        for path, content in outputs:
            with path.open("xb") as f:
                created.append(path)
                f.write(content)
    except (ValueError, OSError, KeyError, TypeError, ArithmeticError) as exc:
        for path in created:
            path.unlink(missing_ok=True)
        p.exit(2,f"INVALID_OR_UNWRITABLE: {exc}\n")


if __name__ == "__main__":
    main()
