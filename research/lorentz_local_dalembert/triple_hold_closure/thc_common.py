"""Bounded recursive closure of PR122's exact 38 HOLD boxes.
SPDX-License-Identifier: Apache-2.0
"""
import sys, hashlib, importlib.util
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'triple_subdivision'))
from tsd_common import *
import tsd_common as source
HERE=Path(__file__).resolve().parent

def assemble_source():
    path=HERE.parent/'triple_subdivision/assemble.py'
    spec=importlib.util.spec_from_file_location('_thc_assembly',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.assemble()

def frozen():
    assemble_source();source.frozen()
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

@lru_cache(maxsize=1)
def original():
    assemble_source()
    ar=read(HERE.parent/'triple_subdivision/certificates.json.gz')
    rows=source.combined(ar)
    pending=[r for r in rows if r['status']=='HOLD']
    assert len(rows)==1352 and len(pending)==38
    assert sum(volume(r) for r in pending)==F(19,256000)
    return rows,pending

def replace_round(active,ar):
    active=dict(active)
    for path in ar['splits']:assert active.pop(path)['status']=='HOLD'
    for r in ar['cells']:
        assert r['path'] not in active;active[r['path']]=r
    for stage in ('marginal','overlap'):
        for r in ar[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box']
            active[r['path']]=r
    return active
