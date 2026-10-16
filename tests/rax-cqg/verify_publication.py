"""Verify the approved publication bytes without changing or executing them."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / 'docs/research/rax/cqg-benchmark-v0.2.0/PUBLICATION.json'


def main():
    meta = json.loads(META.read_text())
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    archive = ROOT / meta['approved_archive']
    assert digest(archive) == meta['archive_sha256'], 'approved archive changed'
    source = ROOT / meta['source_directory']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None, 'archive CRC failure'
        members = z.namelist()
        assert len(members) == 28 and len(members) == len(set(members))
        for name in members:
            relative = Path(name).relative_to(meta['archive_root'])
            assert not relative.is_absolute() and '..' not in relative.parts
            assert (source / relative).read_bytes() == z.read(name), name
    for line in (source / 'MANIFEST.sha256').read_text().splitlines():
        expected, relative = line.split('  ', 1)
        assert digest(source / relative) == expected, relative
    app = ROOT / meta['browser_app']
    assert digest(app) == meta['browser_app_sha256']
    assert app.read_bytes() == (source / 'rax_cqg_lab.html').read_bytes()
    print(json.dumps({'status':'PASS_APPROVED_PUBLICATION_BYTES', 'package_files':len(members),
                      'archive_sha256':digest(archive), 'browser_copy_identical':True}))


if __name__ == '__main__':
    main()
