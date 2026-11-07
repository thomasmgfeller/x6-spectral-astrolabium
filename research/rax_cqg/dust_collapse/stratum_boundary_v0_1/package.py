"""Create an explicit release manifest and a deterministic ZIP archive."""
import json,zipfile
from verify_package import ROOT,FILES,SOURCE_MAIN,STEM,sha256,verify
def main():
    files={}
    for name in sorted(FILES):
        data=(ROOT/name).read_bytes();files[name]={'bytes':len(data),'sha256':sha256(data)}
    manifest={'schema':'cst-dust-stratum-boundary-manifest-v0.1','source_main':SOURCE_MAIN,'files':files,
              'integrity_scope':'Checksums detect accidental changes; this is not a cryptographic signature.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    validation=verify();target=ROOT/(STEM+'_Pruefpaket.zip')
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted((*FILES,'manifest.json')):
            info=zipfile.ZipInfo('stratum_boundary_v0_1/'+name,date_time=(2026,11,7,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,(ROOT/name).read_bytes(),compresslevel=9)
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:raise RuntimeError('Archive CRC failure')
    print(json.dumps({'package':target.name,'bytes':target.stat().st_size,'sha256':sha256(target.read_bytes()),'verification':validation},indent=2,sort_keys=True))
if __name__=='__main__':main()
