"""Verify immutable v0.22 publication, finite-domain scope and exact replay."""
import argparse,hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def safe(name,package=None):
    p=PurePosixPath(name)
    require(bool(p.parts) and not p.is_absolute() and '..' not in p.parts and (package is None or p.parts[0]==package),'safe publication path')
def read(path):return json.loads(path.read_text())
def run(replay=False):
    meta=read(HERE/'PUBLICATION.json');package=HERE/'cspp_v022'
    for name,digest in meta['artifact_sha256'].items():safe(name);require(sha(HERE/name)==digest,'artifact SHA256: '+name)
    with zipfile.ZipFile(HERE/'CSPP_Endliche_Aussenhistory_v0_22_Pruefpaket.zip') as z:
        require(z.testzip() is None,'ZIP CRC');names=z.namelist()
        require(len(names)==len(set(names))==meta['package_file_count']==43,'original package inventory')
        for name in names:
            safe(name,package.name);require((HERE/name).read_bytes()==z.read(name),'original package bytes: '+name)
        before={name:sha(HERE/name) for name in names}
    manifest=(package/'SHA256SUMS').read_text().splitlines()
    require(len(manifest)==meta['package_manifest_entries']==42,'manifest inventory')
    checked=set()
    for line in manifest:
        digest,name=line.split('  ',1);safe(name)
        require(name not in checked,'unique manifest path');checked.add(name)
        require(sha(package/name)==digest,'package SHA256: '+name)
    require(checked|{'SHA256SUMS'}=={str(PurePosixPath(n).relative_to(package.name)) for n in names},'complete manifest coverage')
    require((package/'report/Endliche_Aussenhistory_v0_22.pdf').read_bytes()==(HERE/'Endliche_Aussenhistory_v0_22.pdf').read_bytes(),'same PDF')
    checks=read(package/'results/CHECKS.json')
    require(checks['status']=='PASS','scientific checks')
    for key,value in {'source_files_verified':11,'partition_cell_counts':[688,2664,10480],
      'exact_total_volume_over_pi':'110567/384','exact_deep_volume_over_pi':'50087/384','exact_front_volume_over_pi':'315/2',
      'independent_transformed_moment_quadratures':50,'independent_source_mass_quadratures':6,
      'rational_angular_box_probes':1332,'transport_decompositions_checked':48,'fixed_KG_controls_per_precision':30,
      'zero_crossing_square_regression':'PASS','new_random_calls':0,'independent_scientific_review':'NOT_PERFORMED','METHOD':'HOLD','G1':'HOLD'}.items():
        require(checks[key]==value,'declared check scope: '+key)
    require(checks['negative_controls']=={'omitted_wavefront_rejected_at_controls':23,'missing_front_volume':'REJECTED','missing_detector_bin':'REJECTED','corrupt_source':'REJECTED'},'negative controls')
    receipt=read(package/'REPLAY.json')
    require(receipt['isolated_replay']=='PASS' and receipt['byte_identical_result_files']==9 and receipt['precisions_bits']==[128,192],'replay receipt')
    require(len(receipt['files'])==9,'numerical result inventory')
    for name,digest in receipt['files'].items():safe(name);require(sha(package/'results'/name)==digest,'replayed result identity')
    protocol=read(package/'PROTOCOL.json');status=read(package/'STATUS.json')
    require(protocol['base_commit']==meta['base_commit'] and protocol['history_time_cutoff']=='-6','fixed research basis and cutoff')
    require(protocol['new_clouds']==0 and protocol['new_random_calls']==0 and protocol['new_statistical_rules'] is False,'fixed statistical scope')
    require(status['step_1_complete'] is True and status['infinite_tail_combined'] is False,'finite-only completion')
    require(status['individual_realization_guarantee'] is False and status['global_v019_majorant']=='UNCHANGED','global claim boundary')
    require(status['METHOD']==status['G1']=='HOLD' and status['fresh_confirmation']=='NOT_RUN','scientific gates')
    for bits in [128,192]:
        result=read(package/f'results/FINITE_{bits}.json')
        require(result['precision_bits']==bits and result['status']==meta['scientific_status'] and result['new_random_calls']==0,'precision and fixed HOLD')
        require(result['time_cutoff']=='-6' and len(result['field_controls'])==30,'whole finite support and fixed controls')
        require([x['grid_denominator'] for x in result['levels']]==[8,16,32],'three deterministic grids')
        require([x['cells'] for x in result['levels']]==[688,2664,10480],'full cell inventories')
        for level in result['levels']:
            require(level['volume_over_pi']=='110567/384','whole exact volume')
            require([r['key'] for r in level['archives']]==['d0_r00','d0_r01','d0_r02','d0_r03'],'four unchanged archives')
            require([r['active_count'] for r in level['archives']]==[65,49,59,50],'fixed known active points')
            for row in level['archives']:
                require(len(row['first_forcing_upper'])==row['active_count'],'all first forcings')
                require([w['window'] for w in row['windows']]==[0,1],'both whole detector windows')
    if replay:subprocess.run([sys.executable,'-B',str(package/'reproduce.py')],check=True)
    for name,digest in before.items():require(sha(HERE/name)==digest,'publication unchanged: '+name)
    print('Publication integrity PASS: original PDF, ZIP, 43 files, 42 hashes; complete finite exterior, METHOD_HOLD and G1 HOLD preserved',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');run(p.parse_args().replay)
