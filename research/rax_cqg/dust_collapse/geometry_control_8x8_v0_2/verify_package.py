#!/usr/bin/env python3
"""Integrity, array semantics and isolated replay of the formal control package."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import numpy as np
import cst_dust_geometry_kernel_8x8 as g
from package import ROOT, ARCHIVE, MANIFEST, files, archive_bytes

PAIRS=[('1','z1'),('-1','zm1'),('i','zi')]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def read_json(path):
    def invalid(value):raise ValueError('Nonstandard JSON: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8'),parse_constant=invalid)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--replay',action='store_true');args=parser.parse_args()
    manifest=read_json(ROOT/MANIFEST)
    actual={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files()}
    require(manifest['algorithm']=='sha256' and actual==manifest['files'],'Package inventory or SHA256 mismatch')
    for name in actual:
        if name.endswith('.json'):read_json(ROOT/name)
    prov=read_json(ROOT/'provenance.json');src=(ROOT/prov['polynomial_source']['local_path']).read_bytes()
    require(hashlib.sha1(b'blob '+str(len(src)).encode()+b'\0'+src).hexdigest()==prov['polynomial_source']['git_blob_sha'],'Source blob mismatch')
    require(hashlib.sha256(src).hexdigest()==g.SOURCE_SHA256,'Source SHA256 mismatch')
    status=read_json(ROOT/'status.json');tests=read_json(ROOT/'results/tests.json')
    require(tests['test_count']==len(set(tests['passed']))==status['software_tests']['count']==19 and tests['errors']==tests['failures']==0,'Test evidence mismatch')
    gates={x:'HOLD' for x in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']}
    require(status['physical_gates']==gates and status['physical_8x8_matter_matrix']=='NOT_CONSTRUCTED','Physical status promoted')
    producer_hash=hashlib.sha256((ROOT/'cst_dust_geometry_kernel_8x8.py').read_bytes()).hexdigest()
    for phase,tag in PAIRS:
        path=ROOT/'data'/f'cst_dust_geometry_kernel_8x8_{tag}.npz';report=read_json(path.with_suffix('.json'))
        require(report['npz_sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),'NPZ digest mismatch')
        require(report['generator_sha256']==producer_hash and report['source_sha256']==g.SOURCE_SHA256,'Producer provenance mismatch')
        require(report['source_commit']==prov['base_commit'],'Source commit mismatch')
        require(report['physical_kernel'] is False and report['physical_gates']==gates,'Fixture promoted to physical data')
        require(report['physical_8x8_matter_matrix']=='NOT_CONSTRUCTED' and report['physical_K_0plus']=='NOT_COMPUTED','Physical matter claim changed')
        require(report['physical_gram'] is None and report['physical_clock'] is None and report['delta_chi'] is None,'Unsupported physical product or clock')
        require(report['basis']==g.BASIS and report['basis_layout']=='stratum_geometry_matter','Basis sidecar mismatch')
        require(report['exact_source_phase_data']==g.exact_phase_data(phase),'Exact phase certificate mismatch')
        with np.load(path,allow_pickle=False) as arrays:
            require('channel_dim' not in arrays.files and 'G_in' not in arrays.files and 'G_out' not in arrays.files,'Ambiguous or physical field leaked')
            for name in arrays.files:
                a=arrays[name]
                if a.dtype.kind in 'biufc':require(np.isfinite(a).all(),'Nonfinite NPZ field '+name)
            require(arrays['z'].item()==g.PHASES[phase],'Phase mismatch')
            require(arrays['basis'].tolist()==g.BASIS and np.array_equal(arrays['original_to_output_indices'],g.PERMUTATION),'NPZ basis mismatch')
            require(arrays['n_channels'].item()==2 and arrays['states_per_channel'].item()==4,'Channel dimensions mismatch')
            require(np.array_equal(arrays['stratum_index'],g.STRATUM) and np.array_equal(arrays['geometry_index'],g.GEOMETRY) and np.array_equal(arrays['matter_index'],g.MATTER),'Index array mismatch')
            require(arrays['role'].item()=='GEOMETRY_SPECTATOR_CONTROL','Wrong role')
            require(np.array_equal(arrays['G_in_diagnostic'],np.eye(8)) and np.array_equal(arrays['G_out_diagnostic'],np.eye(8)),'Undeclared diagnostic product')
            values,defect=g.validate_fixture(arrays['K_geom'],arrays['K'])
            require(np.array_equal(arrays['K_geom'],g.kernels(g.PHASES[phase])),'Polynomial matrix mismatch')
            require(np.array_equal(defect,arrays['defect_diagnostic_I8']),'Diagnostic defect mismatch')
    links=0
    for doc in ROOT.glob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            if '://' in target or target.startswith(('#','../','mailto:')):continue
            if target==ARCHIVE and not (ROOT/ARCHIVE).is_file():continue
            require((ROOT/target.split('#')[0]).is_file(),'Broken local link '+target);links+=1
    archive_present=(ROOT/ARCHIVE).is_file()
    if archive_present:require((ROOT/ARCHIVE).read_bytes()==archive_bytes(),'ZIP differs from deterministic rebuild')
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='cst-geometry8-replay-') as tmp:
            destination=Path(tmp);pairs=[]
            for phase,tag in PAIRS:
                name=f'cst_dust_geometry_kernel_8x8_{tag}.npz'
                subprocess.run([sys.executable,'-O','-B',str(ROOT/'cst_dust_geometry_kernel_8x8.py'),'--phase',phase,'--output',str(destination/name)],check=True,cwd=tmp)
                pairs.extend([(ROOT/'data'/name,destination/name),(ROOT/'data'/name.replace('.npz','.json'),destination/name.replace('.npz','.json'))])
            subprocess.run([sys.executable,'-O','-B',str(ROOT/'test_geometry_control.py'),'--output',str(destination/'tests.json')],check=True,cwd=tmp)
            pairs.append((ROOT/'results/tests.json',destination/'tests.json'))
            for expected,replayed in pairs:require(expected.read_bytes()==replayed.read_bytes(),'Replay differs: '+expected.name)
    print(f'PASS: {len(actual)} file hashes, 3 pickle-free NPZ/JSON pairs, 19 regression tests, {links} local links'
          + (', deterministic ZIP' if archive_present else ', extracted package')
          + (', 7 replay files byte-identical' if args.replay else ''))
    print('Role: formal geometry/spectator control. Physical matter matrix: NOT_CONSTRUCTED; physical gates: 8 HOLD.')

if __name__=='__main__':main()
