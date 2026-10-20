"""Package completed evidence without rerunning, selecting, or changing any model."""
import hashlib
import json
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    paths=[]; seeds=[]; commits=set()
    for shard in [0,1]:
        folder=HERE/f'test-{shard}'
        e=json.loads((folder/'execution.json').read_text())
        assert e['status']=='COMPLETE'
        commits.add(e['source_commit'])
        paths.append(folder/'execution.json')
        for item in e['records']:
            p=folder/item['file']; raw=p.read_bytes()
            assert hashlib.sha256(raw).hexdigest()==item['sha256']
            seeds.append(json.loads(raw)['seed']); paths.append(p)
    c=json.loads((HERE/'contract.json').read_text())
    assert sorted(seeds)==list(range(c['test_seeds'][0],c['test_seeds'][1]+1))
    assert len(commits)==1
    with zipfile.ZipFile(HERE/'test_clouds.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(paths): z.write(p,p.relative_to(HERE).as_posix())
    names=['test_clouds.zip','residual_calibration.zip','frozen_model.json','summary.json']
    manifest={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(status='PACKAGED',clouds=len(seeds),files=len(paths),
                         archive_bytes=(HERE/'test_clouds.zip').stat().st_size,source_commit=commits.pop()),indent=2))


if __name__=='__main__': main()
