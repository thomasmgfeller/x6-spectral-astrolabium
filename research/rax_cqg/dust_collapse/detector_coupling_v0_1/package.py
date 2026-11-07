"""Build a fixed-timestamp ZIP from an explicit release allowlist."""
import json
import zipfile
from verify_package import ROOT, FILES, SOURCE_MAIN, sha256, verify

def main():
    files = {}
    for name in sorted(FILES):
        data = (ROOT / name).read_bytes()
        files[name] = {'sha256': sha256(data), 'bytes': len(data)}
    manifest = {'schema': 'cst-dust-coupling-manifest-v0.1', 'source_main': SOURCE_MAIN,
                'files': files, 'integrity_scope': 'Checksums detect accidental changes; this manifest is not a cryptographic signature.'}
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    result = verify()
    target = ROOT / 'CST_DUST_Detektorkopplung_Historienmischung_v0_1_Pruefpaket.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted((*FILES, 'manifest.json')):
            info = zipfile.ZipInfo('detector_coupling_v0_1/' + name, date_time=(2026, 11, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / name).read_bytes(), compresslevel=9)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('Archive CRC failure')
    print(json.dumps({'package': target.name, 'bytes': target.stat().st_size,
                      'sha256': sha256(target.read_bytes()), 'verification': result}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
