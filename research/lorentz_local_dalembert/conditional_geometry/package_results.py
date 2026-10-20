"""Package completed raw evidence without changing any record."""
import hashlib
import json
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    files = []
    seeds = []
    for shard in [0, 1]:
        folder = HERE/f'test-{shard}'
        e = json.loads((folder/'execution.json').read_text())
        if e['status'] != 'COMPLETE' or len(e['records']) != 16:
            raise ValueError('complete declared test budget required')
        files.append(folder/'execution.json')
        for record in e['records']:
            p = folder/record['file']
            raw = p.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == record['sha256']
            seeds.append(json.loads(raw)['seed'])
            files.append(p)
    assert sorted(seeds) == list(range(70110000, 70110032))
    manifest = {}
    target = HERE/'test_clouds.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(files):
            raw = p.read_bytes()
            name = str(p.relative_to(HERE))
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, raw)
            manifest[name] = hashlib.sha256(raw).hexdigest()
    manifest[target.name] = hashlib.sha256(target.read_bytes()).hexdigest()
    (HERE/'test_manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(records=32, files=len(files), zip_bytes=target.stat().st_size)))


if __name__ == '__main__':
    main()
