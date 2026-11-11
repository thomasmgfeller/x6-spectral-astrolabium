#!/usr/bin/env python3
"""Offline integrity and scoped replay; does not promote physical gates."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from package import ROOT, ARCHIVE, MANIFEST, files, archive_bytes

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def read_json(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    manifest = read_json(MANIFEST)
    require(manifest['algorithm'] == 'sha256', 'Unsupported digest algorithm')
    actual = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files()}
    require(actual == manifest['files'], 'Package file inventory or SHA256 mismatch')
    for name in actual:
        if name.endswith('.json'):
            read_json(name)
    source = read_json('source_evidence/manifest.json')
    require(source['count'] == len(source['files']) == 111, 'Source image count mismatch')
    with zipfile.ZipFile(ROOT/'source_evidence/formula_images.zip') as z:
        require(len(z.namelist()) == len(set(z.namelist())) == 111, 'Duplicate/missing source entries')
        require(set(z.namelist()) == {v['archive_path'] for v in source['files']}, 'Source archive inventory mismatch')
        for v in source['files']:
            name = PurePosixPath(v['archive_path'])
            require(not name.is_absolute() and '..' not in name.parts, 'Unsafe archive path')
            data = z.read(v['archive_path'])
            require(data.startswith(b'\x89PNG\r\n\x1a\n'), 'Source is not a PNG')
            require(len(data) == v['bytes'] and hashlib.sha256(data).hexdigest() == v['sha256'], 'Source image digest mismatch')
    status = read_json('status.json')
    results = read_json('results/checks.json')
    require(results['count'] == len(results['controls']) == status['software_controls']['count'] == 32, 'Control count mismatch')
    require(len({x['id'] for x in results['controls']}) == 32, 'Duplicate control IDs')
    require(all(x['result'] == 'PASS' and x['scope'] == 'algebraic_or_finite_control' for x in results['controls']), 'Unexpected result or scope')
    gates = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY', 'BOUNDARY', 'TRAPPING', 'EXTENSION'}
    require(status['physical_gates'] == results['physical_gates'] == {k: 'HOLD' for k in gates}, 'Physical gates were changed without evidence')
    require(status['grid_study'] == results['grid_study'] == 'NOT_RUN', 'Grid study status mismatch')
    require(status['external_replication'] == 'NOT_EXECUTED' and status['paid_compute'] is False, 'Unverified execution claim')
    plan = read_json('study_plan.json')
    require(plan['status'] == 'OPEN_NOT_FROZEN' and plan['outcome'] == 'NOT_RUN', 'Unexpected study plan state')
    require(plan['raw_grid_triplets'] == [[81,91,81],[121,137,121],[161,181,161],[241,271,241]], 'Raw grid values changed')
    for key in ['domain', 'coefficients', 'initial_state', 'integrator', 'solver_commit', 'norm_tolerance', 'energy_tolerance', 'observable_tolerances']:
        require(plan[key] is None, f'Unverified study value: {key}')
    link_count = 0
    for md in ROOT.glob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
            if '://' in target or target.startswith(('#', 'mailto:', '../')):
                continue
            # A distributed ZIP cannot contain itself; this download link is
            # present in the repository but optional after unpacking.
            if target == ARCHIVE and not (ROOT/ARCHIVE).is_file():
                continue
            require((md.parent/target.split('#')[0]).is_file(), f'Broken local link in {md.name}: {target}')
            link_count += 1
    pdf = (ROOT/'N0B_2C_MF_v0_2_Bericht.pdf').read_bytes()
    require(pdf.startswith(b'%PDF-') and pdf.rstrip().endswith(b'%%EOF'), 'Malformed PDF envelope')
    archive_present = (ROOT/ARCHIVE).is_file()
    if archive_present:
        require((ROOT/ARCHIVE).read_bytes() == archive_bytes(), 'ZIP not byte-identical to deterministic rebuild')
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='n0b-replay-') as tmp:
            output = Path(tmp)/'checks.json'
            subprocess.run([sys.executable, '-O', '-B', str(ROOT/'checks/run_checks.py'), '--output', str(output)], check=True, cwd=tmp)
            require(output.read_bytes() == (ROOT/'results/checks.json').read_bytes(), 'Replay result is not byte-identical')
    print(f'PASS: {len(actual)} file hashes, 111 source images, {link_count} local links'
          + (', deterministic ZIP' if archive_present else ', extracted package (outer ZIP not supplied)')
          + (', isolated byte-identical replay' if args.replay else ''))
    print('Physical gates: 8 HOLD; grid study and CST extraction: NOT_RUN')

if __name__ == '__main__':
    main()
