"""Build the release from an explicit allowlist; no caches or local tooling."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
STEM = 'CST_DUST_Massabhaengigkeit_Zustandstransport_v0_1'
FILES = [
    'README.md', 'NOTICE', 'LICENSE', 'DERIVATION.md',
    'plan.json', 'plan.sha256', 'supplement.json', 'provenance.json',
    'analyze.py', 'transport_controls.py', 'replay.py', 'verify_package.py',
    'package.py', 'build_report.py', STEM + '.pdf',
    'inputs/geometry.py', 'inputs/intervals.py', 'inputs/memory.py', 'inputs/bounds.py',
    'results/measure_certificate.json', 'results/one_element_witnesses.json',
    'results/geometry_moment_controls.json', 'results/robustness_bounds.json',
    'results/verification.json', 'results/transport_controls.json', 'results/replay.json',
]


def main():
    records = {}
    for name in sorted(FILES):
        data = (ROOT / name).read_bytes()
        records[name] = {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    manifest = {'schema': 'cst-dust-measure-audit-manifest-v0.1', 'files': records,
                'manifest_self_hash': 'Excluded; the archive SHA256 is reported separately.'}
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    import verify_package
    verify_package.verify()
    target = ROOT / (STEM + '_Pruefpaket.zip')
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(FILES + ['manifest.json']):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / name).read_bytes(), compresslevel=9)
    print(json.dumps({'archive': str(target), 'size': target.stat().st_size,
                      'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
