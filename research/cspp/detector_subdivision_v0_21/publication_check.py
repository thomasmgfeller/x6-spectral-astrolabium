"""Verify immutable v0.21 publication, scientific scope and optional exact replay."""
import argparse,hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def safe(name,package=None):
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and (package is None or p.parts[0]==package),'safe publication path')
def run(replay=False):
    meta=json.loads((HERE/'PUBLICATION.json').read_text());package=HERE/'cspp_v021'
    for name,digest in meta['artifact_sha256'].items():safe(name);require(sha(HERE/name)==digest,'artifact SHA256: '+name)
    with zipfile.ZipFile(HERE/'CSPP_Detektor_Unterteilung_v0_21_Pruefpaket.zip') as z:
        require(z.testzip() is None,'ZIP CRC');names=z.namelist()
        require(len(names)==len(set(names))==meta['package_file_count']==42,'original package inventory')
        for name in names:
            safe(name,package.name);require((HERE/name).read_bytes()==z.read(name),'original package bytes: '+name)
        before={name:sha(HERE/name) for name in names}
    manifest=(package/'SHA256SUMS').read_text().splitlines()
    require(len(manifest)==meta['package_manifest_entries']==41,'manifest inventory')
    checked=set()
    for line in manifest:
        digest,name=line.split('  ',1);safe(name)
        require(name not in checked,'unique manifest path');checked.add(name)
        require(sha(package/name)==digest,'package SHA256: '+name)
    require(checked|{'SHA256SUMS'}=={str(PurePosixPath(n).relative_to(package.name)) for n in names},'complete manifest coverage')
    require((package/'report/Detektor_Unterteilung_v0_21.pdf').read_bytes()==(HERE/'Detektor_Unterteilung_v0_21.pdf').read_bytes(),'same PDF')
    checks=json.loads((package/'results/CHECKS.json').read_text())
    require(checks['status']=='PASS','scientific checks')
    expected={'physical_volume_overlaps':279552,'kernel_majorants_checked':559104,'integer_box_count_checks':224,
              'point_kernel_dominance_checks':224,'direct_poisson_controls':40,'source_blobs':14,'negative_controls':4}
    require(checks['counters']==expected,'declared validation scope')
    require(checks['external_review']=='NOT_CLAIMED' and checks['global_complement']=='NOT_NEWLY_CERTIFIED','claim boundary')
    receipt=json.loads((package/'REPLAY.json').read_text())
    require(receipt['isolated_replay']=='PASS' and receipt['byte_identical_result_files']==7 and receipt['precisions_bits']==[128,192],'replay receipt')
    require(len(receipt['results_sha256'])==7,'numerical result inventory')
    for name,digest in receipt['results_sha256'].items():safe(name);require(sha(package/'results'/name)==digest,'replayed result identity')
    for bits in [128,192]:
        result=json.loads((package/f'results/DETECTOR_{bits}.json').read_text())
        require(result['status']==meta['scientific_status'] and result['new_random_calls']==0,'HOLD and no new random data')
        require(result['root_grid']==4 and result['root_cells']==256 and len(result['archives'])==4,'fixed root and archive inventory')
        require(result['mass_certificate']['fine_grid']==128 and result['monotone_envelope_certificate']['threshold']==95,'fixed analytical construction')
        for row in result['archives']:
            require([w['window'] for w in row['windows']]==[0,1],'both complete detector windows')
            for w in row['windows']:
                require([l['detector_grid'] for l in w['levels']]==[0,2,4],'nested detector domains')
                require([l['endpoint_cells'] for l in w['levels']]==[1,16,256],'complete endpoint inventory')
    if replay:subprocess.run([sys.executable,'-B',str(package/'reproduce.py')],check=True)
    for name,digest in before.items():require(sha(HERE/name)==digest,'publication unchanged: '+name)
    print('Publication integrity PASS: original PDF, ZIP, 42 files, 41 hashes; METHOD_HOLD and G1 HOLD preserved',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');run(p.parse_args().replay)
