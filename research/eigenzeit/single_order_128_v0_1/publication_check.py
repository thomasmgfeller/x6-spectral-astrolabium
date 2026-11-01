"""Verify the published files and replay the decisions from all packed orders."""
import ast
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def counts_from_npy(raw, rows):
    require(raw[:8] == b"\x93NUMPY\x01\x00", "unexpected NPY format")
    offset = 10 + int.from_bytes(raw[8:10], "little")
    header = ast.literal_eval(raw[10:offset].decode("ascii"))
    stride = 128 * 128 // 8
    require(header == {"descr": "|u1", "fortran_order": False, "shape": (rows, stride)}, "unexpected order layout")
    require(len(raw) == offset + rows * stride, "invalid matrix data length")
    return [int.from_bytes(raw[i:i+stride], "little").bit_count() for i in range(offset, len(raw), stride)]

def main():
    record = json.loads((HERE / "PUBLICATION.json").read_text())
    for name, expected in record["files"].items():
        require(digest((ROOT / name).read_bytes()) == expected, f"publication digest: {name}")
    with ZipFile(HERE / "Eigenzeit_Einzelordnung_128_v0_1_Pruefpaket.zip") as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == record["archive_members"], "invalid archive inventory")
        payloads = {row.split("  ", 1)[1]: row.split("  ", 1)[0] for row in z.read("MANIFEST.sha256").decode().splitlines()}
        require(len(payloads) == record["manifest_payloads"] and set(names) == set(payloads) | {"MANIFEST.sha256"}, "manifest inventory")
        for name, expected in payloads.items():
            require(digest(z.read(name)) == expected, f"bad payload: {name}")
        require(digest(z.read("FREEZE.sha256")) == record["local_freeze_sha256"], "freeze")
        for line in z.read("FREEZE.sha256").decode().splitlines():
            expected, name = line.split("  ", 1)
            require(digest(z.read(name)) == expected, f"freeze entry: {name}")
        for entry, public in [("Ansicht.html", ROOT / "app/eigenzeit-einzelordnung/index.html"),
                              ("DERIVATION.md", HERE / "DERIVATION.md"), ("data/result.json", HERE / "result.json"),
                              ("audit.json", HERE / "audit.json")]:
            require(z.read(entry) == public.read_bytes(), f"public copy: {entry}")
        require((HERE / "Eigenzeit_Einzelordnung_128_v0_1.pdf").read_bytes().startswith(z.read("Bericht.pdf")), "PDF prefix")
        results = json.loads(z.read("data/result.json"))
        bands = json.loads(z.read("data/calibration.json"))["bands"]
        for j in range(3):
            for phase, size in [("cal", 1999), ("test", 4096)]:
                base = f"data/{phase}_{j}"
                counts = counts_from_npy(z.read(base + ".npy"), size)
                require(counts == list(map(int, z.read(base + "_C2.csv").decode().splitlines()[1:])), f"counts: {base}")
                if phase == "cal":
                    ordered = sorted(counts)
                    require(bands[j] == [ordered[49], ordered[-50]], f"calibration: {j}")
                else:
                    hist = [0] * 8
                    for count in counts:
                        mask = sum(1 << i for i, (lo, hi) in enumerate(bands) if lo <= count <= hi)
                        hist[mask] += 1
                    require(hist == results["profiles"][j]["histogram_mask"], f"decision histogram: {j}")
                    for i, cell in enumerate(results["cells"][j]):
                        keep = sum(v for mask, v in enumerate(hist) if mask & (1 << i))
                        require(cell["hits"] == (keep if i == j else size - keep), f"decision rate: {j}, {i}")
    print("PASS: 35 immutable payloads, public copies, 5997 calibration and 12288 held-out orders")

if __name__ == "__main__":
    main()
