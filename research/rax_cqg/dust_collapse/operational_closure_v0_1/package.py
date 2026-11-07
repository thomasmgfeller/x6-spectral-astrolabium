"""Package the explicit release allowlist with deterministic ZIP timestamps."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
STEM='CST_DUST_Praeparation_Rueckkehrtest_Fehlerbudget_v0_1'
FILES=['README.md','NOTICE','LICENSE','DERIVATION.md','plan.json','plan.sha256',
       'provenance.json','operational_contract.json','analyze.py','replay.py',
       'verify_package.py','package.py','build_report.py',STEM+'.pdf',
       'inputs/previous_measure_derivation.md','inputs/previous_operational_derivation.md',
       'inputs/previous_boundary_derivation.md','inputs/previous_one_element_witnesses.json',
       'results/continuous_readout.json','results/instrument_covariance.json',
       'results/calibration_bounds.json','results/verification.json','results/replay.json']
def main():
    entries={}
    for name in sorted(FILES):
        b=(ROOT/name).read_bytes();entries[name]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    manifest={'schema':'cst-dust-operational-closure-manifest-v0.1','files':entries,
              'manifest_self_hash':'Excluded; the archive hash is recorded separately.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    import verify_package
    verify_package.main()
    target=ROOT/(STEM+'_Pruefpaket.zip')
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(FILES+['manifest.json']):
            info=zipfile.ZipInfo(name,date_time=(2026,11,7,0,0,0))
            info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(ROOT/name).read_bytes(),compresslevel=9)
    print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,
                      'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
