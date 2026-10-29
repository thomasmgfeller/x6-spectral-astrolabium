"""Check immutable v0.23 publication, complete global scope and exact replay."""
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
    meta=read(HERE/'PUBLICATION.json');package=HERE/'cspp_v023'
    for name,digest in meta['artifact_sha256'].items():safe(name);require(sha(HERE/name)==digest,'artifact SHA256: '+name)
    with zipfile.ZipFile(HERE/'CSPP_Unendlicher_Rest_Globale_Bilanz_v0_23_Pruefpaket.zip') as z:
        require(z.testzip() is None,'ZIP CRC');names=z.namelist()
        require(len(names)==len(set(names))==meta['package_file_count']==41,'original package inventory')
        for name in names:
            safe(name,package.name);require((HERE/name).read_bytes()==z.read(name),'original package bytes: '+name)
        before={name:sha(HERE/name) for name in names}
    manifest=(package/'SHA256SUMS').read_text().splitlines()
    require(len(manifest)==meta['package_manifest_entries']==40,'manifest inventory');checked=set()
    for line in manifest:
        digest,name=line.split('  ',1);safe(name);require(name not in checked,'unique manifest path');checked.add(name)
        require(sha(package/name)==digest,'package SHA256: '+name)
    require(checked|{'SHA256SUMS'}=={str(PurePosixPath(n).relative_to(package.name)) for n in names},'complete manifest coverage')
    require((package/'report/Unendlicher_Rest_Globale_Bilanz_v0_23.pdf').read_bytes()==(HERE/'Unendlicher_Rest_Globale_Bilanz_v0_23.pdf').read_bytes(),'same PDF')
    checks=read(package/'results/CHECKS.json');require(checks['status']=='PASS','scientific checks')
    require(checks['counts']=={'source_files':14,'source_norm_precision_overlaps':35,'half_integer_gamma_identities':34,'independent_fourier_integrals':12,'wrong_fourier_constant_rejected':9,'independent_kernel_moment_quadratures':12,'independent_power_integral_quadratures':19,'independent_far_polynomial_quadratures':6,'direct_poisson_controls':12,'endpoint_audits_checked':958,'global_decompositions':16},'declared check scope')
    require(checks['negative_controls']=={'missing_detector_shell':'REJECTED','missing_initial_tail_strip':'REJECTED','omitted_unknown_paths':'REJECTED','wrong_Fourier_constant':'REJECTED'},'negative controls')
    require(checks['infinite_tail_combined'] is True and checks['new_random_calls']==0 and checks['independent_scientific_review']=='NOT_PERFORMED','complete scope and limits')
    receipt=read(package/'REPLAY.json')
    require(receipt['isolated_replay']=='PASS' and receipt['byte_identical_result_files']==5 and receipt['precisions_bits']==[128,192],'replay receipt')
    require(len(receipt['files'])==5,'numerical result inventory')
    for name,digest in receipt['files'].items():safe(name);require(sha(package/'results'/name)==digest,'replayed result identity')
    protocol=read(package/'PROTOCOL.json');status=read(package/'STATUS.json')
    require(protocol['base_commit']==meta['base_commit']==status['base_commit'],'fixed research basis')
    require(protocol['new_clouds']==0 and protocol['new_random_calls']==0 and protocol['new_statistical_rules'] is False,'fixed statistical scope')
    require(status['step_2_complete'] is True and status['infinite_tail_combined'] is True,'complete finite plus infinite scope')
    require(status['finite_v022_contribution']=='UNCHANGED_ADDED_EXACTLY_ONCE' and status['old_patch_included_once'] is True,'disjoint complete combination')
    require(status['global_error_target']=='1/1000_UNCHANGED_NOT_PROVED','unchanged unproved target')
    require(status['individual_realization_guarantee'] is False and status['observed_error_claim'] is False and status['operator_rejection_claim'] is False,'scientific claim boundary')
    require(status['METHOD']==status['G1']==checks['METHOD']==checks['G1']=='HOLD' and status['fresh_confirmation']=='NOT_RUN','scientific gates')
    for bits in [128,192]:
        result=read(package/f'results/GLOBAL_{bits}.json')
        require(result['precision_bits']==bits and result['status']==meta['scientific_status'] and result['new_random_calls']==0,'precision and fixed HOLD')
        require(result['history_partition']=={'finite':'0<=tau<=5','infinite':'tau>5','finite_exterior_zero':'0<=tau<=7/4'},'complete root partition')
        require(result['endpoint_audits']==479 and [w['window'] for w in result['windows']]==[0,1],'whole endpoint inventory')
        for w in result['windows']:
            require(w['detector_bins']==128,'whole detector bins')
            require([r['key'] for r in w['archives']]==['d0_r00','d0_r01','d0_r02','d0_r03'],'four unchanged archives')
            require([r['active_count'] for r in w['archives']]==[65,49,59,50],'fixed known active points')
            require(w['uniform_active_endpoint']['tail_bounds'][0]['tau_cutoff']=='5','whole infinite tail')
            for row in w['archives']:
                require(len(row['known_first_tail_upper'])==row['active_count'],'all first forcings')
                for key in ['finite_v022_upper','direct_tail_upper','known_active_tail_upper','unknown_active_tail_upper','complete_tail_upper','complete_global_upper']:
                    require(isinstance(row[key],str) and bool(row[key]),'all path contributions: '+key)
    if replay:subprocess.run([sys.executable,'-B',str(package/'reproduce.py')],check=True)
    for name,digest in before.items():require(sha(HERE/name)==digest,'publication unchanged: '+name)
    print('Publication integrity PASS: original PDF, ZIP, 41 files, 40 hashes; complete finite plus infinite global budget; METHOD and G1 HOLD preserved',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');run(p.parse_args().replay)
