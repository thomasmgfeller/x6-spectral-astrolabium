"""Auditable model and adopted-reference checks; optional isolated RTL rerun."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from plvl.__main__ import provenance

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
SGNC=REPO/"experiments/photonic-two-qubit/reference/sagnac_v0_7"


class AuditResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.passed=[]

    def addSuccess(self,test):
        super().addSuccess(test)
        self.passed.append(test.id())


def invoke(command,cwd,env=None):
    r=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=180)
    # Avoid temporary absolute paths in the reproducibility record.
    log=(r.stdout+r.stderr).replace(str(cwd),"<isolated-reference>")
    return {"exit_code":r.returncode,"status":"PASS" if r.returncode==0 else "FAIL","log":log}


def adopted_hashes():
    manifest=json.loads((ROOT/"adoption_manifest.json").read_text())
    result=[]
    for row in manifest["files"]:
        path=REPO/row["repository_path"]
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        result.append({"path":row["repository_path"],"sha256":actual,
                       "status":"PASS" if actual==row["sha256"] else "FAIL"})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--ghdl",help="Executable for full inherited RTL + host tests")
    args=p.parse_args()
    if args.output.exists():
        p.error("Output must be a new path")
    inventory=adopted_hashes()
    log=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"))
    tested=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=AuditResult).run(suite)
    result={"schema":"plvl.validation.v1","reproducibility":provenance(),
            "adopted_files":inventory,
            "model_tests":{"count":tested.testsRun,"passed":tested.passed,
                           "failures":[[t.id(),s] for t,s in tested.failures+tested.errors],
                           "skipped":[[t.id(),s] for t,s in tested.skipped],"log":log.getvalue()},
            "physical_validation":"NOT_ASSESSED","qkd_security":"NOT_ASSESSED",
            "independent_group_replication":"NOT_ASSESSED"}
    with tempfile.TemporaryDirectory(prefix="plvl-reference-") as tmp:
        copied=Path(tmp)/"sagnac"
        shutil.copytree(SGNC,copied,ignore=shutil.ignore_patterns("build","validation","__pycache__"))
        if args.ghdl:
            exe=shutil.which(args.ghdl)
            if exe is None:
                raise ValueError("Requested GHDL executable not found")
            env=os.environ.copy()
            result["rtl"]=invoke([sys.executable,"sim/run_tests.py","--ghdl",exe],copied,env)
            if result["rtl"]["status"]=="PASS":
                rtl=json.loads((copied/"validation/test_summary.json").read_text())
                # Wall-clock runtime is not a reproducible scientific output.
                for case in rtl["rtl_cases"]:
                    case.pop("seconds",None)
                result["rtl"]["summary"]=rtl
                result["rtl"]["ghdl_version"]=(copied/"validation/ghdl_version.txt").read_text()
                result["adopted_host_tests"]=invoke([sys.executable,"-m","unittest","discover","-s","host","-v"],copied)
            else:
                result["adopted_host_tests"]={"status":"NOT_EXECUTED","reason":"RTL fixture generation failed"}
        else:
            result["rtl"]={"status":"NOT_EXECUTED","reason":"GHDL not requested"}
            # Two host tests require RTL-generated fixtures. Report the omission;
            # do not synthesize those fixtures and call them RTL evidence.
            code='''import sys,unittest
sys.path.insert(0,"host")
suite=unittest.defaultTestLoader.discover("host")
omit={"test_no_automatic_five_percent_rule","test_loss_flag_survives_transport"}
def flatten(s):
 for t in s:
  if isinstance(t,unittest.TestSuite): yield from flatten(t)
  else: yield t
selected=unittest.TestSuite(t for t in flatten(suite) if t._testMethodName not in omit)
r=unittest.TextTestRunner(verbosity=2).run(selected)
sys.exit(not r.wasSuccessful())
'''
            result["adopted_host_tests"]=invoke([sys.executable,"-c",code],copied)
            result["adopted_host_tests"]["not_executed"]=["test_no_automatic_five_percent_rule","test_loss_flag_survives_transport"]
    good=(tested.wasSuccessful() and not tested.skipped and
          all(r["status"]=="PASS" for r in inventory) and
          result["adopted_host_tests"]["status"]=="PASS" and
          (not args.ghdl or result["rtl"]["status"]=="PASS"))
    result["status"]=("PASS_FULL_SOFTWARE_SCOPE" if args.ghdl else "PASS_MODEL_AND_PARTIAL_HOST_SCOPE") if good else "FAIL"
    result["file_inventory_sha256"]={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()
           for f in sorted(ROOT.rglob("*")) if f.is_file() and
           not any(part in ("evidence","__pycache__",".venv") for part in f.relative_to(ROOT).parts)}
    with args.output.open("x") as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write("\n")
    print(json.dumps({"status":result["status"],"model_tests":tested.testsRun,
                      "rtl":result["rtl"]["status"],"host":result["adopted_host_tests"]["status"]}))
    return 0 if good else 1


if __name__=="__main__":
    raise SystemExit(main())
