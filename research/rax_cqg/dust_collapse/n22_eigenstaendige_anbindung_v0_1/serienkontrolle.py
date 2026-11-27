"""Replay the original device-only solver for the two unchanged B+ controls."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from importlib.util import spec_from_file_location, module_from_spec


def replay(tmp, cfg, seeds, jobs):
    archive=tmp/'branch'
    spec=spec_from_file_location('archivierter_zweigtest',archive/'pruefen.py')
    module=module_from_spec(spec)
    spec.loader.exec_module(module)
    reference=json.loads((archive/'Ergebnisse.json').read_text())
    binary=tmp/'serienkontrolle'
    subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',
                    '-I',str(tmp/'base'),str(archive/'zweigtest.cpp'),'-o',str(binary)],check=True)
    def check(item):
        cid,sector=item
        row=seeds[cid]['row']
        assert reference['controls'][str(cid)]['equations']==25
        run=subprocess.run([str(binary),'76','3000000',str(sector)],input=module.input_text(cfg,row),
                           text=True,check=True,capture_output=True)
        mask,s,n,c,o,d=map(int,run.stdout.split())
        assert mask==row[1] and sector==s and o==reference['trees'][str(cid)][str(s)]['open']==0
        assert n==2*c-1
        return str(cid),str(s),dict(nodes=n,closed=c,open=o,depth=d)
    result={}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for cid,s,tree in pool.map(check,((k,s) for k in (216427,217269) for s in range(4))):
            result.setdefault(cid,{})[s]=tree
    return result
