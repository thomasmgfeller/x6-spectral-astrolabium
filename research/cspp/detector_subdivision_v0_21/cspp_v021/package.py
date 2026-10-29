"""Build the verified deterministic ZIP and copy the standalone report."""
import hashlib,json,shutil,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=json.loads((HERE/'results/CHECKS.json').read_text())
    replay=json.loads((HERE/'REPLAY.json').read_text())
    if checks['status']!='PASS' or replay['isolated_replay']!='PASS':raise ArithmeticError('unfinished validation')
    report=HERE/'report/Detektor_Unterteilung_v0_21.pdf'
    if not report.is_file():raise FileNotFoundError(report)
    def included(p):return p.is_file() and '__pycache__' not in p.parts and p.suffix!='.log' and p.name not in ['SHA256SUMS','PACKAGE.json']
    files=sorted(p for p in HERE.rglob('*') if included(p))
    package={'schema':'cspp.detector-subdivision.package/0.21','date':'2026-10-29',
      'base_commit':'22eab46877dc03b1c0f1bee81c2d1d65bbf45d65','file_count':len(files)+2,
      'replay_result_files':replay['byte_identical_result_files'],'METHOD':'HOLD','G1':'HOLD',
      'repository_publication':'NOT_PERFORMED_FOR_V021'}
    (HERE/'PACKAGE.json').write_text(json.dumps(package,indent=2)+'\n');files.append(HERE/'PACKAGE.json');files.sort()
    (HERE/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(HERE).as_posix()}\n' for p in files))
    files.append(HERE/'SHA256SUMS');files.sort()
    output=HERE.parent/'output';(output/'pdf').mkdir(parents=True,exist_ok=True)
    pdf=output/'pdf'/report.name;shutil.copyfile(report,pdf)
    target=output/'CSPP_Detektor_Unterteilung_v0_21_Pruefpaket.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            info=zipfile.ZipInfo('cspp_v021/'+p.relative_to(HERE).as_posix(),date_time=(2026,10,29,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None or len(z.namelist())!=package['file_count']:raise ArithmeticError('ZIP integrity')
        for p in files:
            if z.read('cspp_v021/'+p.relative_to(HERE).as_posix())!=p.read_bytes():raise ArithmeticError('ZIP content')
    result={'file_count':len(files),'checksummed_files':len(files)-1,'deliverables':[
        {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in [pdf,target]]}
    print(json.dumps(result,indent=2));return result
if __name__=='__main__':main()
