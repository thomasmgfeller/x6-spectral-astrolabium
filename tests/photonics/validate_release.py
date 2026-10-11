#!/usr/bin/env python3
"""Reproduce existing reference checks in temporary copies; no hardware claims."""
import argparse
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'experiments/photonic-two-qubit'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ghdl', action='store_true', help='Require GHDL; never silently skip')
    parser.add_argument('--cad', action='store_true', help='Regenerate and check nominal CAD geometry')
    args = parser.parse_args()
    out = args.output.resolve()
    if out == PUB or PUB in out.parents:
        parser.error('Keep fresh evidence outside the publication sources')
    out.mkdir(parents=True, exist_ok=True)
    report = {'schema': 'x6.photonic.reference-validation/1',
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'physical_claim': 'NOT_ASSESSED',
              'data_origin': 'synthetic_or_mechanical_model', 'checks': [],
              'requested': {'ghdl': args.ghdl, 'cad': args.cad},
              'status': 'RUNNING'}
    for name in ('numpy', 'scipy', 'cadquery', 'ezdxf', 'Pillow'):
        try:
            report.setdefault('dependencies', {})[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            pass

    def run(name, command, cwd):
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=360)
        log = proc.stdout + proc.stderr
        (out / (name + '.log')).write_text(log)
        item = {'name': name, 'status': 'PASS' if proc.returncode == 0 else 'FAIL',
                'returncode': proc.returncode, 'command': command}
        count = re.search(r'Ran (\d+) tests? in', log)
        if count:
            item['unittest_count'] = int(count.group(1))
        report['checks'].append(item)
        if proc.returncode:
            raise RuntimeError(f'{name} failed; see {out / (name + ".log")}')
        print(name + ': PASS', flush=True)

    try:
        provenance = json.loads((PUB / 'PROVENANCE.json').read_text())
        for item in provenance['files']:
            assert hashlib.sha256((PUB / item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
        report['checks'].append({'name': 'primary_artifact_hashes', 'status': 'PASS', 'count': len(provenance['files'])})
        with tempfile.TemporaryDirectory(prefix='x6-photonic-') as tmp:
            work = Path(tmp)
            packages = {}
            count = 0
            for archive in sorted((PUB / 'downloads').glob('*.zip')):
                target = work / archive.stem
                with zipfile.ZipFile(archive) as z:
                    for member in z.infolist():
                        path = Path(member.filename)
                        if path.is_absolute() or '..' in path.parts or (member.external_attr >> 16) & 0o170000 == 0o120000:
                            raise ValueError('Unsafe archive member: ' + member.filename)
                    z.extractall(target)
                roots = [p for p in target.iterdir() if p.is_dir()]
                assert len(roots) == 1, archive.name
                packages[archive.name] = roots[0]
                for manifest in target.rglob('SHA256*'):
                    for line in manifest.read_text().splitlines():
                        if not line.strip():
                            continue
                        digest, rel = line.split(None, 1)
                        rel = rel.strip().lstrip('*')
                        candidate = (manifest.parent / rel).resolve()
                        assert candidate.is_relative_to(target), rel
                        assert hashlib.sha256(candidate.read_bytes()).hexdigest() == digest, (archive.name, rel)
                        count += 1
            report['checks'].append({'name': 'archive_internal_checksums', 'status': 'PASS', 'entries': count, 'archives': len(packages)})
            sagnac = packages['Sagnac_v0_7_UART_Host_und_Hardwareplan.zip']
            jig = packages['JIG_F1_FabLab_Baupaket_v0_1_1.zip']
            old_jig = packages['JIG_F1_FabLab_Baupaket_v0_1.zip']
            for p in (PUB / 'reference/sagnac_v0_7').rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts:
                    assert p.read_bytes() == (sagnac / p.relative_to(PUB / 'reference/sagnac_v0_7')).read_bytes(), p
            for name in ('analyze.py', 'frame_codec.py', 'capture_serial.py'):
                assert (ROOT / 'device/vendor/sagnac_v0_7' / name).read_bytes() == (sagnac / 'host' / name).read_bytes(), name
            geometry_count = 0
            for folder in ('cad', 'drawings', 'print'):
                assert (old_jig / folder).is_dir() and (jig / folder).is_dir(), folder
                assert {p.relative_to(old_jig) for p in (old_jig / folder).rglob('*') if p.is_file()} == {p.relative_to(jig) for p in (jig / folder).rglob('*') if p.is_file()}, folder
                for p in (old_jig / folder).rglob('*'):
                    if p.is_file():
                        assert p.read_bytes() == (jig / p.relative_to(old_jig)).read_bytes(), p
                        geometry_count += 1
            assert (jig / 'JIG_F1_Bauanleitung.pdf').read_bytes() == (PUB / 'manuals/JIG_F1_Bauanleitung_v0_1_1.pdf').read_bytes()
            report['checks'].append({'name': 'reference_identity_and_unchanged_jig_geometry', 'status': 'PASS', 'geometry_files': geometry_count})
            suites = [
                ('sagnac_v07_host', sagnac / 'host', 'test_*.py'),
                ('sagnac_v06_host', packages['Sagnac_v0_6_Referenzkern_und_Pruefprotokoll.zip'] / 'host', 'test_*.py'),
                ('legacy_v01_statistics', packages['Photonische_Messkette_v0_1_Auswertung.zip'], 'test_photon_stats.py'),
                ('legacy_v01_host', packages['Photonische_Messkette_v0_1_Digitalkern.zip'] / 'host', 'test_host.py'),
                ('single_channel_v02', packages['Photonische_Messkette_v0_2_Einkanal.zip'], 'test_channel_tools.py'),
            ]
            for name, cwd, pattern in suites:
                run(name, [sys.executable, '-m', 'unittest', 'discover', '-s', '.', '-p', pattern, '-v'], cwd)
            run('jig_analytic', [sys.executable, 'src/check_design.py'], jig)
            shutil.copy2(jig / 'validation/analytic_checks.json', out / 'jig_analytic_checks.json')
            if args.cad:
                run('jig_cad', [sys.executable, 'src/build_cad.py'], jig)
                for name in ('cad_solids.json', 'nominal_collisions.json', 'release_checks.json'):
                    p = jig / 'validation' / name
                    if p.exists():
                        shutil.copy2(p, out / ('jig_' + name))
            if args.ghdl:
                run('ghdl_version', ['ghdl', '--version'], sagnac)
                run('sagnac_v07_rtl', [sys.executable, 'sim/run_tests.py'], sagnac)
                summary = json.loads((sagnac / 'validation/test_summary.json').read_text())
                assert summary['case_count'] == 28, summary
                shutil.copy2(sagnac / 'validation/test_summary.json', out / 'sagnac_v07_rtl_summary.json')
                for entity in ('sagnac_core', 'snapshot_framer', 'uart_tx', 'sagnac_uart_top'):
                    run('generic_synthesis_' + entity, ['ghdl', '--synth', '--std=08', entity], sagnac / 'build')
            report['not_run'] = [name for name, enabled in [('GHDL RTL and generic synthesis', args.ghdl), ('CAD regeneration', args.cad)] if not enabled]
        report['status'] = 'PASS_REQUESTED_SOFTWARE_AND_MODEL_CHECKS'
    except Exception as exc:
        report['status'] = 'FAIL'
        report['error'] = str(exc)
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (out / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
        print(report['status'], flush=True)


if __name__ == '__main__':
    main()
