"""One frozen octree subdivision of all56 remaining three-support boxes.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,importlib.util
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'triple_overlap_refinement'))
from tor_common import *
from tor_common import combined as source_combined, frozen as source_frozen
from tt_common import cached_overlap,event_coverage
HERE=Path(__file__).resolve().parent

def ensure_source():
    path=HERE.parent/'triple_overlap_refinement/assemble.py'
    spec=importlib.util.spec_from_file_location('_tsd_source_assembly',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.assemble()

def frozen():
    ensure_source();source_frozen()
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

@lru_cache(maxsize=1)
def inputs():
    ensure_source();ar=read(HERE.parent/'triple_overlap_refinement/certificates.json.gz')
    previous=read(HERE.parent/'triple_overlap_refinement/summary.json');source=source_combined(ar)
    pending=[r for r in source if r['status']=='HOLD']
    assert len(source)==960 and len(pending)==56 and previous['excluded_volume_fraction']=='3865/4096'
    return ar,previous,source,pending

@lru_cache(maxsize=1)
def transport_inventory():
    old=read(HERE.parent/'triple_cube/certificates.json.gz')
    return old['projection_sources'],old['node5_strips']

def combined(ar):
    _,_,source,pending=inputs();active={r['path']:r for r in source}
    assert ar['splits']==[r['path'] for r in pending]
    for path in ar['splits']:assert active.pop(path)['status']=='HOLD'
    for r in ar['cells']:
        assert r['path'] not in active;active[r['path']]=r
    for stage in ('marginal','overlap'):
        for r in ar[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    return sorted(active.values(),key=path_key)
